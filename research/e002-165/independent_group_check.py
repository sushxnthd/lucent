# Independent exact group/color design check using the GitHub Actions artifact RAW_CHROMA.csv
import csv,collections
from pathlib import Path
rows=list(csv.DictReader(Path("RAW_CHROMA.csv").open()))
assert len(rows)==480
g=collections.defaultdict(set)
for r in rows:g[r["group"]].add(float(r["all_exact_gray"])==1.0)
assert len(g)==26 and all(len(v)==1 for v in g.values())
colored={k for k,v in g.items() if v=={False}}
assert colored=={"eye","eye 2","eye 3","eye 4"}
assert sum(float(r["all_exact_gray"])==1.0 for r in rows)==441
assert sum(r["group"] in colored for r in rows)==39
print("PASS: exact chroma-group confounding, 480 images")
