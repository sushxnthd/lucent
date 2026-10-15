#!/usr/bin/env python3
"""Independent nonempty and per-eye count integrity check; not a physiological gate."""
import json,sys
from pathlib import Path
p=Path(__file__).resolve().parent/"results/RAW_VALIDITY_AUDIT.json"
if not p.exists():raise SystemExit("MISSING_RAW_RESULT")
d=json.loads(p.read_text());a=d["selected"]
assert len(a)==30 and not d["errors"],"EMPTY_OR_INCOMPLETE_ORIGINAL_HUMAN"
assert len(set((r["pid"],r["eye"]) for r in a))==30
assert all(r["n_equal"] and r["n_tsv"]>=600 for r in a)
for r in a:
 for k,v in r["counts"].items():
  assert 0<=v<=r["n_tsv"]
  assert r["matches"][k]==(r["n_equal"] and v==r["valid_metadata"])
for k,s in d["summary"].items():
 eligible=[r for r in a if k in r["counts"]]
 assert s["available_rows"]==len(eligible)
 assert s["exact_matches"]==sum(r["matches"][k] for r in eligible)
assert d["rgb_waveform"]=="NOT_TESTED"
print("PASS raw 30-eye semantic audit integrity; RGB physiology NOT TESTED")
