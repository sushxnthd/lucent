#!/usr/bin/env python3
"""E002-577: bounded range-only extraction of one source-linked LPW video.

No full-archive fallback, no human frame publication, no anatomical labels.
"""
import argparse
import binascii
import hashlib
import io
import json
import os
import re
import struct
import subprocess
import tempfile
import urllib.request
import zipfile
import zlib
from pathlib import Path

URL = "https://datasets.d2.mpi-inf.mpg.de/tonsen/LPW.zip"
MAX_COMPRESSED = 100 * 1024 * 1024
MAX_UNCOMPRESSED = 400 * 1024 * 1024
MAX_CENTRAL = 4 * 1024 * 1024
EXTENSIONS = (".avi", ".mp4", ".mkv", ".mov")
CONTENT_RANGE = re.compile(r"^bytes (\d+)-(\d+)/(\d+)$")


class AcquisitionError(Exception):
    pass


def remote_size(url):
    req = urllib.request.Request(url, method="HEAD",
                                 headers={"User-Agent": "Lucent-research-E002-577/1.0"})
    with urllib.request.urlopen(req, timeout=25) as response:
        n = int(response.headers.get("Content-Length", "0"))
    if not 65557 <= n <= 5 * 1024**3:
        raise AcquisitionError("HEAD_LENGTH_UNAVAILABLE_OR_UNSAFE")
    return n


def remote_getter(url, total):
    def get(start, end):
        if not (0 <= start <= end < total):
            raise AcquisitionError("RANGE_OUT_OF_BOUNDS")
        req = urllib.request.Request(
            url, headers={"Range": f"bytes={start}-{end}",
                          "Accept-Encoding": "identity",
                          "User-Agent": "Lucent-research-E002-577/1.0"})
        with urllib.request.urlopen(req, timeout=90) as response:
            status = response.status
            content_range = response.headers.get("Content-Range", "")
            m = CONTENT_RANGE.fullmatch(content_range)
            if status != 206 or not m or tuple(map(int, m.groups())) != (start, end, total):
                raise AcquisitionError("RANGE_NOT_HONORED")
            body = response.read(end - start + 2)
        if len(body) != end - start + 1:
            raise AcquisitionError("SHORT_RANGE_RESPONSE")
        return body
    return get


def archive_entries(total, get):
    tail_start = max(0, total - 65557)
    tail = get(tail_start, total - 1)
    loc = tail.rfind(b"PK\x05\x06")
    if loc < 0 or len(tail) - loc < 22:
        raise AcquisitionError("EOCD_NOT_FOUND")
    _, disk, cd_disk, entries_disk, entries_total, cd_size, cd_offset, comment_len = (
        struct.unpack_from("<IHHHHIIH", tail, loc))
    if (disk or cd_disk or entries_disk != entries_total or
            entries_total == 65535 or cd_size == 0xffffffff or
            cd_offset == 0xffffffff or loc + 22 + comment_len > len(tail)):
        raise AcquisitionError("ZIP64_OR_MULTIDISK_UNSUPPORTED")
    if cd_size > MAX_CENTRAL or cd_offset + cd_size > total:
        raise AcquisitionError("CENTRAL_DIRECTORY_UNSAFE")
    cd = get(cd_offset, cd_offset + cd_size - 1)
    pos, entries = 0, []
    for _ in range(entries_total):
        if pos + 46 > len(cd):
            raise AcquisitionError("CENTRAL_TRUNCATED")
        fields = struct.unpack_from("<IHHHHHHIIIHHHHHII", cd, pos)
        (sig, made, needed, flags, method, mtime, mdate, crc,
         comp, uncomp, fnlen, exlen, comlen, diskstart, internal, external, localoff) = fields
        if sig != 0x02014b50 or pos + 46 + fnlen + exlen + comlen > len(cd):
            raise AcquisitionError("CENTRAL_MALFORMED")
        raw_name = cd[pos+46:pos+46+fnlen]
        name = raw_name.decode("utf-8" if flags & 0x800 else "cp437")
        pos += 46 + fnlen + exlen + comlen
        if (name.lower().endswith(EXTENSIONS) and not flags & 1 and
                method in (0, 8) and 0 < comp <= MAX_COMPRESSED and
                0 < uncomp <= MAX_UNCOMPRESSED and localoff < cd_offset):
            entries.append({"name": name, "flags": flags, "method": method,
                            "crc": crc, "comp": comp, "uncomp": uncomp,
                            "localoff": localoff})
    if pos != len(cd):
        raise AcquisitionError("CENTRAL_TRAILING_DATA")
    if not entries:
        raise AcquisitionError("NO_BOUNDED_ELIGIBLE_VIDEO")
    return sorted(entries, key=lambda e: e["name"])[0], len(entries)


def extract_member(total, get, entry):
    off = entry["localoff"]
    header = get(off, off + 29)
    (sig, version, flags, method, mtime, mdate, crc, comp, uncomp,
     name_len, extra_len) = struct.unpack("<IHHHHHIIIHH", header)
    if sig != 0x04034b50 or method != entry["method"] or flags != entry["flags"]:
        raise AcquisitionError("LOCAL_HEADER_MISMATCH")
    name = get(off + 30, off + 30 + name_len - 1)
    if name.decode("utf-8" if flags & 0x800 else "cp437") != entry["name"]:
        raise AcquisitionError("LOCAL_FILENAME_MISMATCH")
    data_start = off + 30 + name_len + extra_len
    data_end = data_start + entry["comp"] - 1
    raw = get(data_start, data_end)
    if method == 0:
        output = raw
    else:
        d = zlib.decompressobj(-15)
        output = d.decompress(raw, entry["uncomp"] + 1)
        if not d.eof or d.unconsumed_tail or d.unused_data:
            raise AcquisitionError("DEFLATE_STREAM_UNSAFE")
        output += d.flush()
    if len(output) != entry["uncomp"]:
        raise AcquisitionError("UNCOMPRESSED_LENGTH_MISMATCH")
    if zlib.crc32(output) & 0xffffffff != entry["crc"]:
        raise AcquisitionError("MEMBER_CRC_MISMATCH")
    return output


def probe_video(data, suffix):
    with tempfile.TemporaryDirectory(prefix="lucent-e002-577-") as folder:
        path = Path(folder) / ("private_source" + suffix)
        path.write_bytes(data)
        p = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height,r_frame_rate,avg_frame_rate,nb_frames,duration",
             "-of", "json", str(path)],
            capture_output=True, text=True, timeout=60, check=True)
        streams = json.loads(p.stdout).get("streams", [])
        if len(streams) != 1:
            raise AcquisitionError("VIDEO_STREAM_NOT_UNIQUE")
        q = subprocess.run(
            ["ffmpeg", "-nostdin", "-v", "error", "-i", str(path),
             "-vf", "select=eq(n\\,0)+eq(n\\,10)+eq(n\\,20)",
             "-vsync", "0", "-f", "framemd5", "-"],
            capture_output=True, text=True, timeout=120, check=True)
        frames = [line for line in q.stdout.splitlines() if line and not line.startswith("#")]
        if len(frames) != 3:
            raise AcquisitionError("THREE_NATIVE_FRAMES_NOT_DECODED")
        return streams[0], len(frames)


def self_test():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("01/readme.txt", "no imagery")
        z.writestr("01/eye.avi", b"fake video data for range extraction")
    archive = buf.getvalue()
    def get(a, b):
        return archive[a:b+1]
    entry, eligible = archive_entries(len(archive), get)
    assert eligible == 1 and entry["name"] == "01/eye.avi"
    assert extract_member(len(archive), get, entry) == b"fake video data for range extraction"
    bad = dict(entry, crc=0)
    try:
        extract_member(len(archive), get, bad)
    except AcquisitionError as e:
        assert str(e) == "MEMBER_CRC_MISMATCH"
    else:
        raise AssertionError("CRC corruption was accepted")
    print(json.dumps({"experiment": "E002-577", "self_test": "PASS",
                      "tests": ["ZIP central parsing", "range extraction", "CRC corruption"]}))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    result = {"experiment": "E002-577", "evidence_tier": "SOURCE_ACQUISITION_ONLY",
              "source": URL, "human_anatomical_labels": 0,
              "physical_shutter_authenticated": False,
              "product": "ABSTAIN_UNCALIBRATED", "release": "BLOCKED"}
    try:
        total = remote_size(URL)
        get = remote_getter(URL, total)
        entry, eligible = archive_entries(total, get)
        data = extract_member(total, get, entry)
        stream, decoded = probe_video(data, Path(entry["name"]).suffix.lower())
        result.update(status="AUTHENTIC_SOURCE_MEMBER_DECODED", archive_bytes=total,
                      eligible_entries=eligible, selected_member=entry["name"],
                      compressed_bytes=entry["comp"], uncompressed_bytes=len(data),
                      member_sha256=hashlib.sha256(data).hexdigest(),
                      native_video_stream=stream, selected_native_frames_decoded=decoded)
    except Exception as exc:
        result.update(status="ACQUISITION_BLOCKED",
                      failure_type=type(exc).__name__,
                      failure_reason=str(exc)[:240])
    print(json.dumps(result, sort_keys=True))
    if result["status"] != "AUTHENTIC_SOURCE_MEMBER_DECODED":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
