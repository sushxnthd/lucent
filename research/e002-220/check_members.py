import json
from pathlib import Path
m=json.loads(Path("research/e002-220/MEMBER_HASHES.json").read_text())
assert set(m)=={"P_33","P_54"}
for p,files in m.items():
 assert set(files)=={"video","tracker","events"}
 for x in files.values():
  assert len(x["sha256"])==64 and x["bytes"]>0 and isinstance(x["crc32"],int)
print("E002-220 CRC-verified source member manifest schema PASS")
