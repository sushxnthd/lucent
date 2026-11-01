#!/usr/bin/env python3
"""E002-580: frozen pupil-center index-alias control on genuine LPW labels.

This is NOT an eyelid, blink, physiological velocity or shutter experiment.
No source images, raw coordinates, individual indices or tracks are published.
"""
import argparse
import hashlib
import io
import json
import math
import zipfile

import numpy as np
import e002_577_lpw_range_probe as lpw

EXPERIMENT = "E002-580"
VIDEO = "LPW/1/1.avi"
LABEL = "LPW/1/1.txt"
VIDEO_SHA_PREVIOUSLY_VERIFIED = "158d8654ff9e19162ec7f1316eee3d3046024ad81b355b2b3e5f9e566f5abe86"
NATIVE_FRAMES = 2000
WIDTH, HEIGHT = 640, 480
E_MIN, D_MAX, PIXEL_ERROR = 0.020, 0.010, 1.0
VIDEO_UNCOMPRESSED = 59663314


class Reject(Exception):
    pass


class RangeReader(io.RawIOBase):
    """Read-only seekable ZIP range view; never downloads the full archive."""
    def __init__(self, total, get):
        self.total, self.get, self.pos = total, get, 0

    def readable(self):
        return True

    def seekable(self):
        return True

    def tell(self):
        return self.pos

    def seek(self, offset, whence=io.SEEK_SET):
        new = (offset if whence == io.SEEK_SET else
               self.pos + offset if whence == io.SEEK_CUR else
               self.total + offset if whence == io.SEEK_END else -1)
        if not 0 <= new <= self.total:
            raise Reject("ZIP_SEEK_OUT_OF_BOUNDS")
        self.pos = new
        return new

    def read(self, size=-1):
        if size is None or size < 0:
            raise Reject("UNBOUNDED_ZIP_READ")
        n = min(size, self.total - self.pos)
        if n <= 0:
            return b""
        result = self.get(self.pos, self.pos + n - 1)
        self.pos += n
        return result


def parse_labels(data):
    if len(data) > 500000 or not data:
        raise Reject("LABEL_BYTES_UNSAFE")
    try:
        decoded = data.decode("utf-8-sig")
        rows = []
        for line in decoded.splitlines():
            if not line.strip():
                raise Reject("EMPTY_LABEL_ROW")
            cols = line.split()
            if len(cols) != 2:
                raise Reject("AMBIGUOUS_LABEL_COLUMNS")
            rows.append([float(c) for c in cols])
        x = np.asarray(rows, dtype=np.float64)
    except (UnicodeDecodeError, ValueError, OverflowError) as e:
        raise Reject("UNREADABLE_LABELS") from e
    if x.shape != (NATIVE_FRAMES, 2):
        raise Reject("LABEL_FRAME_COUNT_OR_GEOMETRY_MISMATCH")
    # Reject undocumented invalid/sentinel labels instead of inventing meaning.
    if not np.all(np.isfinite(x)):
        raise Reject("NONFINITE_UNDOCUMENTED_LABEL")
    if not np.all((x[:, 0] >= 0) & (x[:, 0] < WIDTH) &
                  (x[:, 1] >= 0) & (x[:, 1] < HEIGHT)):
        raise Reject("OUT_OF_IMAGE_UNDOCUMENTED_LABEL")
    return x


def geometry(p, width=WIDTH, valid=None):
    p = np.asarray(p, dtype=np.float64)
    if p.ndim != 2 or p.shape[1] != 2 or len(p) < 4 or width <= 0:
        raise Reject("INVALID_TRAJECTORY")
    good = np.all(np.isfinite(p), axis=1)
    if valid is not None:
        if len(valid) != len(p):
            raise Reject("VALIDITY_LENGTH_MISMATCH")
        good &= np.asarray(valid, dtype=bool)
    eligible = good[:-3] & good[1:-2] & good[2:-1] & good[3:]
    start, end = p[:-3], p[3:]
    e1 = np.linalg.norm(p[1:-2] - (2 * start + end) / 3, axis=1)
    e2 = np.linalg.norm(p[2:-1] - (start + 2 * end) / 3, axis=1)
    e = np.maximum(e1, e2) / width
    d = np.linalg.norm(end - start, axis=1) / width
    flags = eligible & (e >= E_MIN) & (d <= D_MAX)
    # Each coordinate point may independently move by <=1 pixel in Euclidean norm.
    # Interpolation weights sum to one; deviation error <=2 px, endpoint <=2 px.
    robust = eligible & (e - 2 * PIXEL_ERROR / width >= E_MIN) & (
        d + 2 * PIXEL_ERROR / width <= D_MAX)
    if np.any(robust & ~flags):
        raise Reject("ROBUST_SUBSET_INVARIANT_BROKEN")
    return e, d, eligible, flags, robust


def summary(p):
    e, d, good, flags, robust = geometry(p)
    phases = []
    for phase in range(3):
        indices = np.arange(phase, len(e), 3)
        use = indices[good[indices]]
        percentiles = lambda x: [round(float(v), 7) for v in
                                 np.percentile(x[use], [50, 90, 99])] if len(use) else None
        phases.append({
            "phase": phase, "windows": int(len(indices)),
            "eligible": int(len(use)), "abstained": int(len(indices) - len(use)),
            "alias_witnesses": int(flags[indices].sum()),
            "robust_1px_witnesses": int(robust[indices].sum()),
            "interior_E_p50_p90_p99": percentiles(e),
            "endpoint_D_p50_p90_p99": percentiles(d)
        })
    return {
        "native_annotation_rows": int(len(p)),
        "windows": int(len(e)), "eligible": int(good.sum()),
        "abstained": int((~good).sum()),
        "alias_witnesses": int(flags.sum()),
        "robust_1px_witnesses": int(robust.sum()),
        "phase": phases
    }


def fetch_labels():
    total = lpw.remote_size(lpw.URL)
    get = lpw.remote_getter(lpw.URL, total)
    with zipfile.ZipFile(RangeReader(total, get), "r") as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise Reject("DUPLICATE_ZIP_NAMES")
        if VIDEO not in names or LABEL not in names:
            raise Reject("EXACT_SOURCE_OR_LABEL_MEMBER_ABSENT")
        v = archive.getinfo(VIDEO)
        a = archive.getinfo(LABEL)
        if (v.file_size != VIDEO_UNCOMPRESSED or
                v.compress_size > lpw.MAX_COMPRESSED or
                a.file_size > 500000 or a.file_size <= 0 or
                a.compress_size > 500000 or a.flag_bits & 1):
            raise Reject("SOURCE_MEMBER_METADATA_MISMATCH")
        # ZipFile.read verifies CRC of the label; no video download is required.
        raw = archive.read(a)
    return raw, {"label_member": LABEL,
                 "label_sha256": hashlib.sha256(raw).hexdigest(),
                 "archive_bytes": total,
                 "video_sha256_previously_verified": VIDEO_SHA_PREVIOUSLY_VERIFIED,
                 "video_sha256_reverified_this_run": False}


def execute():
    raw, provenance = fetch_labels()
    coords = parse_labels(raw)
    return {
        "experiment": EXPERIMENT,
        "status": "SOURCE_ANNOTATION_ALIAS_CONTROL_EXECUTED",
        "evidence_tier": "REAL_HUMAN_SOURCE_PUPIL_CENTER_ANNOTATION_ONLY",
        "reported_native_fps_not_shutter_authenticated": 95,
        "three_to_one_index_sampling_rate_fps": 95 / 3,
        "thresholds": {"E_min_width_fraction": E_MIN,
                       "D_max_width_fraction": D_MAX,
                       "independent_per_frame_perturbation_px": PIXEL_ERROR},
        **provenance, "result": summary(coords),
        "independent_human_eyelid_rater_pairs": 0,
        "anatomical_closure_labels": 0,
        "physical_shutter_authenticated": False,
        "certified_continuous_eyelid_speed": False,
        "heldout_physical_predictions": 0,
        "product": "ABSTAIN_UNCALIBRATED", "release": "BLOCKED"
    }


def self_test():
    p = np.array([[40., 40.], [70., 40.], [40., 40.], [40., 40.]])
    e, d, good, flag, robust = geometry(p)
    assert good[0] and flag[0] and robust[0]
    assert math.isclose(e[0], 30 / WIDTH) and d[0] == 0
    assert np.allclose(geometry(p + [20, 30])[0:2], (e, d))
    assert np.allclose(geometry(p / 2, width=WIDTH / 2)[0:2], (e, d))
    linear = np.array([[0, 0], [3, 0], [6, 0], [9, 0]], dtype=float)
    assert not geometry(linear)[3][0]
    uncertain = p.copy()
    uncertain[1, 0] = 53
    assert geometry(uncertain)[3][0] and not geometry(uncertain)[4][0]
    assert not geometry(p, valid=[True, False, True, True])[2][0]
    assert not geometry(np.array([[0, 0], [float("nan"), 0], [0, 0], [0, 0]]))[2][0]
    for invalid in (b"1 2\n" * (NATIVE_FRAMES - 1),
                    b"1 2 3\n" * NATIVE_FRAMES,
                    b"nan 2\n" * NATIVE_FRAMES,
                    b"640 2\n" * NATIVE_FRAMES):
        try:
            parse_labels(invalid)
        except Reject:
            pass
        else:
            raise AssertionError("Invalid annotation accepted")
    # Range-only ZIP and CRC corruption checks, no network.
    blob = io.BytesIO()
    with zipfile.ZipFile(blob, "w", compression=zipfile.ZIP_STORED) as z:
        z.writestr("LPW/1/1.txt", b"1 2\n" * NATIVE_FRAMES)
    data = blob.getvalue()
    def get(a, b):
        return data[a:b + 1]
    with zipfile.ZipFile(RangeReader(len(data), get)) as z:
        assert len(z.read("LPW/1/1.txt")) == 4 * NATIVE_FRAMES
    damaged = bytearray(data)
    at = damaged.find(b"1 2\n")
    assert at > 0
    damaged[at] = ord("9")
    with zipfile.ZipFile(io.BytesIO(damaged)) as z:
        try:
            z.read("LPW/1/1.txt")
        except zipfile.BadZipFile:
            pass
        else:
            raise AssertionError("CRC corruption accepted")
    print(json.dumps({"experiment": EXPERIMENT, "self_test": "PASS",
                      "checks": ["loop and linear control", "translation",
                                 "scale", "1px robust certificate", "missing",
                                 "nonfinite", "row and column mismatch",
                                 "source coordinate bounds", "range ZIP",
                                 "CRC corruption"]}, sort_keys=True))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    try:
        print(json.dumps(execute(), sort_keys=True))
    except Exception as exc:
        print(json.dumps({"experiment": EXPERIMENT, "status": "ABSTAIN",
                          "reason": type(exc).__name__ + ":" + str(exc)[:100],
                          "product": "ABSTAIN_UNCALIBRATED", "release": "BLOCKED"},
                         sort_keys=True))
        raise SystemExit(2)


if __name__ == "__main__":
    main()
