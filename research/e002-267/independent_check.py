"""Independent synthetic numeric check. Does not import evaluator."""
import tempfile, math
from test_evaluate import fixture
with tempfile.TemporaryDirectory() as d:
    path,m,rows=fixture(d)
    rows=[r for r in rows if r["participant_id"]=="test_a"]
    x=[float(r["rgb_ratio"]) for r in rows]
    y=[float(r["reference_mm"]) for r in rows]
    mx=sum(x)/len(x);my=sum(y)/len(y)
    r=sum((a-mx)*(b-my) for a,b in zip(x,y))/math.sqrt(
      sum((a-mx)**2 for a in x)*sum((b-my)**2 for b in y))
    assert len(rows)==300 and r>.99
print("PASS: independent synthetic Pearson, no human claim")
