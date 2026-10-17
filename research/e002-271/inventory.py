"""E002-271 public archive provenance; metadata only, no extraction."""
import collections, hashlib, json, pathlib, subprocess, tempfile, urllib.request
URL = "https://zenodo.org/records/17046553/files/Eye-tracking%20records%20of%20patients%20with%20visual%20disorders.rar?download=1"
EXPECTED_MD5 = "59dbd3de85b2eee54345c7d14c9629c9"
OUT = pathlib.Path(__file__).with_name("RUN_RESULT.json")
result = {"run": "E002-271", "source": "10.5281/zenodo.17046553",
          "source_md5_expected": EXPECTED_MD5,
          "status": "ACCESS_BLOCKED", "human_waveform_evaluated": False,
          "rgb_reference_clock_certified": False}
try:
    with tempfile.TemporaryDirectory() as td:
        dest = pathlib.Path(td) / "source.rar"
        md5, sha = hashlib.md5(), hashlib.sha256()
        with urllib.request.urlopen(URL, timeout=90) as response, dest.open("wb") as out:
            while True:
                block = response.read(1048576)
                if not block:
                    break
                out.write(block)
                md5.update(block)
                sha.update(block)
        result.update(source_bytes=dest.stat().st_size,
                      source_md5_actual=md5.hexdigest(),
                      source_sha256=sha.hexdigest())
        if md5.hexdigest() != EXPECTED_MD5:
            result["status"] = "HASH_MISMATCH"
        else:
            p = subprocess.run(["7z", "l", "-slt", str(dest)],
                               capture_output=True, text=True, timeout=120)
            if p.returncode:
                result.update(status="ARCHIVE_LIST_BLOCKED",
                              listing_exit_code=p.returncode)
            else:
                paths = [line[7:].strip() for line in p.stdout.splitlines()
                         if line.startswith("Path = ")]
                paths = paths[1:] if paths else []
                ext = collections.Counter(pathlib.PurePosixPath(n).suffix.lower()
                                          or "<none>" for n in paths)
                result.update(status="INVENTORY_COMPLETE_NOT_CERTIFIED",
                              file_count=len(paths),
                              extension_counts=dict(sorted(ext.items())),
                              video_candidates=sum(ext[x] for x in
                                  (".mp4", ".mov", ".avi", ".mkv", ".webm")),
                              reference_candidates=sum(ext[x] for x in
                                  (".csv", ".tsv", ".json", ".edf", ".txt", ".h5", ".mat")))
except Exception as exc:
    result["error_class"] = type(exc).__name__
    result["status"] = "ACCESS_BLOCKED"
finally:
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
if result["status"] not in ("INVENTORY_COMPLETE_NOT_CERTIFIED",):
    raise SystemExit(1)
