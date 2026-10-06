"""Bounded, outcome-blind archive qualification for Lucent E002.

Inspects ZIP central-directory metadata only. It never extracts images and never
computes pupil outcomes. Intended to prevent recursive-extraction/log explosions
before the frozen E002 waveform analysis.
"""
from __future__ import annotations
import argparse, json, zipfile
from collections import Counter
from pathlib import PurePosixPath

def qualify(path: str) -> dict:
    with zipfile.ZipFile(path) as z:
        infos = z.infolist()
        files = [i for i in infos if not i.is_dir()]
        suffix = Counter(PurePosixPath(i.filename).suffix.lower() or "<none>" for i in files)
        meta = [i.filename for i in files if (
            PurePosixPath(i.filename).suffix.lower() in {".csv",".json",".txt",".md"}
            or "readme" in i.filename.lower() or "session" in i.filename.lower()
        )]
        nested = [i.filename for i in files if PurePosixPath(i.filename).suffix.lower()==".zip"]
        return {
            "schema":"lucent-e002-archive-preflight-v1",
            "archive_entries":len(infos),
            "file_entries":len(files),
            "suffix_counts":dict(suffix.most_common(30)),
            "metadata_candidates_count":len(meta),
            "metadata_candidates_first_100":meta[:100],
            "nested_archives_count":len(nested),
            "nested_archives_first_100":nested[:100],
        }

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("archive")
    ap.add_argument("--json-out")
    a=ap.parse_args()
    out=qualify(a.archive)
    s=json.dumps(out,indent=2)
    print(s)
    if a.json_out:
        open(a.json_out,"w",encoding="utf-8").write(s+"\n")
