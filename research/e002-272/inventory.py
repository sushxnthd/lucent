#!/usr/bin/env python3
"""E002-272: range-only inventory of public AFFEC ZIPs; no subject data exported."""
import collections
import hashlib
import io
import json
import os
import pathlib
import re
import urllib.request
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent
BASE = "https://zenodo.org/records/19408373/files/"
FILES = {
    "videostream.zip": "b7efc90ca02bc4e571fa90fe2634f0f4",
    "pupil.zip": "8a1a218003e8ded0698bcf239a23baae",
}
RAW_RGB = {".mp4", ".webm", ".mov", ".avi", ".mkv", ".jpg", ".jpeg", ".png", ".bmp"}
MAX_REQUEST = 8 * 1024 * 1024
MAX_TOTAL = 128 * 1024 * 1024

class RangeFile(io.RawIOBase):
    def __init__(self, url):
        self.url = url
        self.pos = 0
        self.total_fetched = 0
        req = urllib.request.Request(url, headers={
            "Range": "bytes=0-0", "Accept-Encoding": "identity",
            "User-Agent": "Lucent-provenance-audit/1.0"})
        with urllib.request.urlopen(req, timeout=60) as response:
            h = response.headers.get("Content-Range", "")
            match = re.fullmatch(r"bytes 0-0/(\d+)", h)
            if response.status != 206 or not match:
                raise ValueError("RANGE_UNSUPPORTED")
            self.size = int(match.group(1))
            if response.read(1) is None:
                raise ValueError("RANGE_EMPTY")
        self.total_fetched += 1
    def seekable(self):
        return True
    def readable(self):
        return True
    def tell(self):
        return self.pos
    def seek(self, offset, whence=0):
        self.pos = int(offset + (self.pos if whence == 1 else self.size if whence == 2 else 0))
        if not 0 <= self.pos <= self.size:
            raise ValueError("INVALID_SEEK")
        return self.pos
    def read(self, n=-1):
        n = min(self.size - self.pos, n if n >= 0 else self.size - self.pos)
        if n <= 0:
            return b""
        if n > MAX_REQUEST or self.total_fetched + n > MAX_TOTAL:
            raise ValueError("RANGE_BUDGET_EXCEEDED")
        start = self.pos
        end = start + n - 1
        req = urllib.request.Request(self.url, headers={
            "Range": f"bytes={start}-{end}", "Accept-Encoding": "identity",
            "User-Agent": "Lucent-provenance-audit/1.0"})
        with urllib.request.urlopen(req, timeout=90) as response:
            cr = response.headers.get("Content-Range", "")
            if response.status != 206 or not cr.startswith(f"bytes {start}-{end}/"):
                raise ValueError("RANGE_RESPONSE_MISMATCH")
            block = response.read(n + 1)
        if len(block) != n:
            raise ValueError("RANGE_LENGTH_MISMATCH")
        self.pos += n
        self.total_fetched += n
        return block

def inventory_one(name):
    url = BASE + name + "?download=1"
    remote = RangeFile(url)
    with zipfile.ZipFile(remote) as archive:
        entries = [x for x in archive.infolist() if not x.is_dir()]
        exts = collections.Counter(pathlib.PurePosixPath(x.filename).suffix.lower() or "<none>"
                                   for x in entries)
        raw = sum(exts[e] for e in RAW_RGB)
        # Names may contain subject IDs: persist only hashes, counts and format totals.
        manifest = "\n".join(f"{x.filename}|{x.file_size}|{x.CRC:08x}" for x in entries)
        return {
            "archive": name,
            "published_archive_md5_unverified": FILES[name],
            "remote_archive_size_bytes": remote.size,
            "archive_file_count": len(entries),
            "extension_counts": dict(sorted(exts.items())),
            "raw_rgb_candidate_count": raw,
            "json_count": exts[".json"],
            "tsv_count": exts[".tsv"],
            "member_listing_sha256": hashlib.sha256(manifest.encode()).hexdigest(),
            "remote_bytes_read": remote.total_fetched,
            "archive_md5_verified": False,
            "individual_member_crc_verified": False,
        }

def classify(inventories):
    if len(inventories) != len(FILES):
        return "ACCESS_BLOCKED"
    video = inventories["videostream.zip"]
    pupil = inventories["pupil.zip"]
    if video["raw_rgb_candidate_count"] == 0:
        return "NOT_RGB_ELIGIBLE"
    if pupil["json_count"] + pupil["tsv_count"] == 0:
        return "NO_PUPIL_REFERENCE"
    return "CANDIDATE_PENDING_PAIR_AND_CLOCK"

def main():
    result = {
        "run": "E002-272",
        "source": "10.5281/zenodo.19408373",
        "source_published": "2026-04-03",
        "human_waveform_evaluated": False,
        "rgb_reference_clock_certified": False,
        "original_source_bytes_verified": False,
        "inventories": {},
        "errors": {},
    }
    for name in FILES:
        try:
            result["inventories"][name] = inventory_one(name)
        except Exception as exc:
            result["errors"][name] = type(exc).__name__ + ":" + str(exc)[:120]
    result["status"] = classify(result["inventories"])
    (ROOT / "RUN_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("E002_272_RESULT=" + json.dumps(result, sort_keys=True))
    return result

if __name__ == "__main__":
    main()
