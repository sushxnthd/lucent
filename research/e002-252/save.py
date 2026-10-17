import json
from pathlib import Path
p=Path("research/e002-234")
o=Path("research/e002-228/E002_252_RAW.json")
o.write_text(json.dumps({"raw_csv":(p/"RAW_BOUNDARY.csv").read_text(),"result":json.loads((p/"RESULTS.json").read_text()),"source":json.loads(Path("research/e002-228/E002_252_SOURCES.json").read_text())}))
print("E002-252 raw and provenance saved")
