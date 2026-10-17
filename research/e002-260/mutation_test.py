import json,shutil,subprocess,tempfile
from pathlib import Path
p=Path(__file__).parent
with tempfile.TemporaryDirectory() as d:
    for f in ['RESULTS.json','independent_check.py']: shutil.copy2(p/f,Path(d)/f)
    q=Path(d)/'RESULTS.json'
    obj=json.loads(q.read_text());obj['mean_squared_error_units_squared']='0'
    q.write_text(json.dumps(obj))
    x=subprocess.run(['python3',str(Path(d)/'independent_check.py')],capture_output=True,text=True)
    assert x.returncode!=0
print('PASS: corrupted result rejected')
