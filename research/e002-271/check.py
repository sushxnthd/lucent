import json
from pathlib import Path
p = Path(__file__).parent
m = json.loads((p / 'DATASET_MANIFEST.json').read_text())
r = json.loads((p / 'RUN_RESULT.json').read_text())
assert m['expected_archive_md5'] == r['source_md5_expected']
assert r['status'] == 'ACCESS_BLOCKED'
assert not r['human_waveform_evaluated']
assert not m['source_bytes_verified']
assert m['admission'] == 'REJECT_PENDING_PROVENANCE'
print('PASS: source and human gates remain explicitly unverified')
