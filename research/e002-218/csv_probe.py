#!/usr/bin/env python3
"""Inspect only bounded public Kaggle session CSV schemas; never publish sample values."""
import csv,hashlib,io,json,pathlib,urllib.parse,urllib.request,zipfile
BASE='https://www.kaggle.com/api/v1/datasets/download/vijuls/PupilDiameterDatasets/'
FILES=['eyedentify/eyedentify/left_eyes/20/50/session_data.csv','eyedentify/eyedentify/right_eyes/41/5/session_data.csv']
report={'run':'E002-218c','status':'partial','native_time_verified':False,'human_waveform_evaluated':False,'files':[]}
for name in FILES:
    row={'path':name,'status':'blocked'}
    try:
        url=BASE+urllib.parse.quote(name,safe='/')
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Lucent-Research/1.0'}),timeout=30) as response:
            data=response.read(1000001)
        if len(data)>1000000: raise ValueError('bounded transfer exceeded')
        if data[:2]==b'PK':
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                names=z.namelist()
                if len(names)!=1 or z.getinfo(names[0]).file_size>1000000:raise ValueError('unexpected ZIP')
                payload=z.read(names[0])
        else:payload=data
        lines=list(csv.reader(io.StringIO(payload.decode('utf-8-sig'))))
        row.update(status='ok',sha256=hashlib.sha256(payload).hexdigest(),header=lines[0],rows=len(lines)-1)
    except Exception as e:row['error']={'type':type(e).__name__,'message':str(e)[:200]}
    report['files'].append(row)
report['status']='complete' if all(x['status']=='ok' for x in report['files']) else 'partial'
root=pathlib.Path('research/e002-218')
(root/'CSV_SCHEMAS.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
samples=json.loads((root/'SAMPLES.json').read_text())
samples['selective_csv_schemas']=report
(root/'SAMPLES.json').write_text(json.dumps(samples,indent=2,sort_keys=True)+'\n')
print(json.dumps({'csv_schema_status':report['status'],'headers':[(x['status'],x.get('header')) for x in report['files']]}))
