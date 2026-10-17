#!/usr/bin/env python3
import json,subprocess,sys,tempfile,zipfile
from pathlib import Path
with zipfile.ZipFile(sys.argv[1]) as z:
    data={n:z.read(n) for n in z.namelist()}
name='e002-221/VALID_ONLY.json'
r=json.loads(data[name])
r['participants']['P_54']['eyes']['left']['offsets']['1']['coverage']=0.5
data[name]=json.dumps(r).encode()
with tempfile.TemporaryDirectory() as d:
    p=Path(d)/'modified.zip'
    with zipfile.ZipFile(p,'w') as z:
        for n,b in data.items():z.writestr(n,b)
    out=subprocess.run([sys.executable,str(Path(__file__).with_name('verify.py')),str(p)],capture_output=True,text=True)
    assert out.returncode!=0
print('tamper rejected')
