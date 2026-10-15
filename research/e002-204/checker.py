import json
from pathlib import Path
p=Path(__file__).resolve().parent/'results/RAW_PUPIL_AUDIT.json'
assert p.exists(), 'NO_RAW_HUMAN_RESULT'
r=json.loads(p.read_text())
assert not r['errors'] and len(r['participants'])==15, 'INCOMPLETE_RAW_HUMAN'
assert r['rgb_waveform']=='NOT_TESTED'
print('PASS original-human reference integrity; RGB NOT TESTED')
