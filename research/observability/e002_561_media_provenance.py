#!/usr/bin/env python3
"""E002-560/561 real FFV1 media-provenance falsification. Synthetic, not human evidence."""
import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
from fractions import Fraction
from pathlib import Path

FPS, N, W, H = 240, 240, 64, 64
CLOSED = {3, 4}

def frame(closed):
    gap = 0 if closed else 16
    top = (H-gap)//2
    bottom = top+gap
    return b''.join(bytes([200 if y < top or y >= bottom else 0])*W for y in range(H))

def raw_frames(phase=None):
    if phase is not None and (type(phase) is not int or not 0 <= phase < 8):
        raise ValueError("invalid phase")
    opened, shut = frame(False), frame(True)
    return [shut if (i if phase is None else phase+8*(i//8)) in CLOSED else opened
            for i in range(N)]

def command(args, data=None):
    p = subprocess.run(args, input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode:
        raise RuntimeError("external command failed: " + " ".join(args) +
                           "\n" + p.stderr.decode(errors="replace")[-2000:])
    return p.stdout

def encode(frames, path):
    command(["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-y",
             "-f", "rawvideo", "-pixel_format", "gray", "-video_size", "64x64",
             "-framerate", "240", "-i", "pipe:0", "-frames:v", "240",
             "-c:v", "ffv1", "-level", "3", str(path)], b"".join(frames))

def inspect(path):
    probe = json.loads(command(["ffprobe", "-v", "error", "-select_streams", "v:0",
                                "-show_entries",
                                "stream=r_frame_rate,avg_frame_rate,time_base:frame=best_effort_timestamp_time",
                                "-show_frames", "-of", "json", str(path)]))
    streams = probe.get("streams", [])
    if len(streams) != 1:
        raise AssertionError("expected one video stream")
    s = streams[0]
    pts = [float(f["best_effort_timestamp_time"]) for f in probe.get("frames", [])]
    if len(pts) != N:
        raise AssertionError("wrong frame count")
    if not all(b > a for a, b in zip(pts, pts[1:])):
        raise AssertionError("nonmonotone PTS")
    if Fraction(s["avg_frame_rate"]) != FPS or Fraction(s["r_frame_rate"]) != FPS:
        raise AssertionError("wrong declared fps")
    raw = command(["ffmpeg", "-nostdin", "-v", "error", "-i", str(path),
                   "-f", "rawvideo", "-pix_fmt", "gray", "-vsync", "0", "pipe:1"])
    if len(raw) != N*W*H:
        raise AssertionError("wrong decoded byte count")
    frames = [raw[i*W*H:(i+1)*W*H] for i in range(N)]
    hashes = [hashlib.sha256(f).digest() for f in frames]
    centers = [f[32*W+32] for f in frames]
    if any(x not in (0, 200) for x in centers):
        raise AssertionError("unexpected center pixel")
    return {
        "decoded_sha256": hashlib.sha256(raw).hexdigest(),
        "decoded_frames": N,
        "declared_fps": FPS,
        "time_base": s["time_base"],
        "closed_frames": centers.count(200),
        "unique_decoded_frames": len(set(hashes)),
        "identical_adjacent_pairs": sum(a == b for a,b in zip(hashes, hashes[1:])),
        "max_pts_error_us": round(max(abs(t-i/FPS) for i,t in enumerate(pts))*1e6, 4),
        "pts_steps_us": sorted({round((b-a)*1e6) for a,b in zip(pts,pts[1:])})
    }

def run_experiment():
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise RuntimeError("ffmpeg/ffprobe absent: abstain")
    results = {}
    with tempfile.TemporaryDirectory(prefix="lucent-e002-561-") as d:
        for ext in ("mkv", "nut"):
            group = {}
            for phase in [None] + list(range(8)):
                name = "authentic_240" if phase is None else "phase_"+str(phase)
                frames = raw_frames(phase)
                path = Path(d)/(ext+"_"+name+"."+ext)
                encode(frames, path)
                got = inspect(path)
                if got["decoded_sha256"] != hashlib.sha256(b"".join(frames)).hexdigest():
                    raise AssertionError("lossless decode mismatch: "+name)
                expected = 2 if phase is None else (8 if phase in (3,4) else 0)
                if got["closed_frames"] != expected:
                    raise AssertionError("event mismatch: "+name)
                if ext == "nut" and got["max_pts_error_us"] > .51:
                    raise AssertionError("corrected timestamp precision failed")
                del got["decoded_sha256"]
                group[name] = got
            results[ext] = group
    mkv_steps = sorted({x for g in results["mkv"].values() for x in g["pts_steps_us"]})
    nut_steps = sorted({x for g in results["nut"].values() for x in g["pts_steps_us"]})
    if mkv_steps != [4000,5000] or nut_steps != [4166,4167]:
        raise AssertionError("unexpected container PTS pattern")
    missed = sum(results["nut"]["phase_"+str(p)]["closed_frames"] == 0 for p in range(8))
    if missed != 6:
        raise AssertionError("phase prediction failed")
    return {
        "experiment": "E002-560/561",
        "e002_560_frozen_exact_pts_condition": "FALSIFIED_MKV_QUANTIZATION",
        "e002_561_corrected_container_condition": "PASS_SYNTHETIC_REAL_CODEC",
        "evidence_tier": "synthetic moving aperture; real FFV1 encoding and decoding",
        "event_high_rate_closed_samples": 2,
        "low_rate_phase_trials": 8,
        "low_rate_phases_missing_event": missed,
        "low_rate_phases_witnessing_event": 8-missed,
        "nominal_240fps_and_240frames_all_files": True,
        "metadata_only_reference_gate": "FALSIFIED",
        "mkv_pts_steps_us": mkv_steps,
        "nut_pts_steps_us": nut_steps,
        "mkv_max_pts_error_us": max(g["max_pts_error_us"] for g in results["mkv"].values()),
        "nut_max_pts_error_us": max(g["max_pts_error_us"] for g in results["nut"].values()),
        "per_file": results,
        "physical_sensor_acquisition_verified": False,
        "continuous_time_closure_verified": False,
        "human_validation": False,
        "product": "ABSTAIN_UNCALIBRATED",
        "release": "BLOCKED"
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output")
    args = parser.parse_args()
    result = json.dumps(run_experiment(), indent=2, sort_keys=True)+"\n"
    if args.output:
        Path(args.output).write_text(result, encoding="utf-8")
    print(result)
