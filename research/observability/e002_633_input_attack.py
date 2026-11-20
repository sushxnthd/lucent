#!/usr/bin/env python3
"""E002-633 negative adversarial audit of E002-632; standard library only."""
import csv
import io
import importlib.util
from pathlib import Path

p = Path(__file__).with_name("e002_632_blind_trial_scorer.py")
spec = importlib.util.spec_from_file_location("scorer632", p)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
base = dict(zip(m.REQUIRED, ("trial-1", "not-a-real-hash", "1/100", "2", "2", "0",
                             "100", "100", "YES", "YES", "YES", "UNKNOWN")))
assert m.decide(base)[0] == "EXCLUDE", "expected demonstration of unverified self-attestation"
header = list(m.REQUIRED) + ["independent_velocity_certified"]
row = [base[k] for k in m.REQUIRED] + ["YES"]
row[list(m.REQUIRED).index("independent_velocity_certified")] = "NO"
buf = io.StringIO()
w = csv.writer(buf)
w.writerow(header)
w.writerow(row)
buf.seek(0)
parsed = list(csv.DictReader(buf))
assert parsed[0]["independent_velocity_certified"] == "YES"
assert m.decide(parsed[0])[0] == "EXCLUDE", "expected duplicate-column overwrite"
duplicates = [dict(base), dict(base)]
out, failures = m.score(duplicates)
assert len(out) == 2 and out[0]["trial_id"] == out[1]["trial_id"] and failures == 0
print("NEGATIVE FINDING: 3/3 adversarial input attacks reproduced")
print("Evidence: software/parser attack only; NO physical/human validation")
