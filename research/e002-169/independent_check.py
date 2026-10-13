import json,math
from pathlib import Path
x=json.loads(Path(__file__).with_name("RESULTS.json").read_text())
assert len(x["rows"])==8
assert sum(row["gt_blinks"] for row in x["rows"])==408
for row in x["rows"]:
    rate=row["rate_per_minute"]
    T=5/60
    mu=rate*T
    assert math.isclose(row["p_zero"],math.exp(-mu),rel_tol=1e-12)
    # Independently derive variance of N/T from Var(N)=E[N].
    assert math.isclose(row["crlb_relative_sd"],math.sqrt(mu/T**2)/rate,rel_tol=1e-12)
    assert math.isclose(row["seconds_for_20pct_sd"],60/(rate*.2**2),rel_tol=1e-12)
print("PASS: eight summaries and independent count-variance check")
