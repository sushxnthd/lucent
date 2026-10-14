import json, math, sys
from pathlib import Path
x=json.loads(Path(sys.argv[1]).read_text())
assert x['summary']['gauge_pass']==18
print('passed')
