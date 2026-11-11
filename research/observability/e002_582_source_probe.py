#!/usr/bin/env python3
"""E002-582 one-shot Silesian5 annotation source inspection; no private data logging.

Only source-structure information, never row values, is printed. The freeze
E002_582_FROZEN.md precedes this file and all source access.
"""
import collections
import hashlib
import io
import json
import pathlib
import re
import urllib.request
import zipfile

URL = "https://www.blinkingmatters.com/files/upload/research/Silesian5%28Basler5%29Annotations.zip"
MAX_DOWNLOAD = 50_000_000
MAX_MEMBER = 30_000_000
MAX_TOTAL = 120_000_000


def retrieve():
    req = urllib.request.Request(URL, headers={"User-Agent": "Lucent-E002-582-scientific-research/1.0"})
    with urllib.request.urlopen(req, timeout=45) as response:
        data = response.read(MAX_DOWNLOAD + 1)
    if len(data) > MAX_DOWNLOAD:
        raise ValueError("DOWNLOAD_TOO_LARGE")
    if not zipfile.is_zipfile(io.BytesIO(data)):
        raise ValueError("NOT_ZIP")
    return data


def inspect(data):
    output = {"experiment": "E002-582", "evidence_tier": "SOURCE_FORMAT_INSPECTION_ONLY",
              "archive_sha256": hashlib.sha256(data).hexdigest(), "archive_bytes": len(data)}
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        infos = z.infolist()
        if len(infos) > 500 or sum(x.file_size for x in infos) > MAX_TOTAL:
            raise ValueError("ZIP_SIZE_LIMIT")
        extensions = collections.Counter()
        summaries = []
        for info in infos:
            name = info.filename
            path = pathlib.PurePosixPath(name)
            if path.is_absolute() or ".." in path.parts or "\\" in name or info.file_size > MAX_MEMBER:
                raise ValueError("UNSAFE_ARCHIVE_MEMBER")
            if info.is_dir():
                continue
            if info.flag_bits & 1:
                raise ValueError("ENCRYPTED_ARCHIVE")
            raw = z.read(info)
            if len(raw) != info.file_size:
                raise ValueError("MEMBER_SIZE_MISMATCH")
            ext = path.suffix.lower()
            extensions[ext or "none"] += 1
            # No values or filenames are printed, only shape metadata.
            lines = raw[:10000].decode("utf-8-sig", errors="replace").splitlines()[:4]
            shapes = []
            for line in lines:
                if not line.strip():
                    continue
                shapes.append({"line_bytes": len(line.encode("utf-8")), "whitespace_fields": len(line.split()),
                               "comma_fields": len(line.split(",")), "semicolon_fields": len(line.split(";")),
                               "colon_fields": len(line.split(":")), "tab_fields": len(line.split("\t"))})
            summaries.append({"member_digest_prefix": hashlib.sha256(name.encode()).hexdigest()[:12],
                              "extension": ext, "uncompressed_bytes": info.file_size,
                              "lines_preview_shapes": shapes})
        output["file_count"] = len(summaries)
        output["extensions"] = dict(sorted(extensions.items()))
        output["members"] = summaries[:40]
    return output


if __name__ == "__main__":
    print(json.dumps(inspect(retrieve()), sort_keys=True))
