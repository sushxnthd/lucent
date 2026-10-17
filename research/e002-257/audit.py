#!/usr/bin/env python3
"""Source-pinned per-eye bias audit for public participant summaries."""
import csv,hashlib,io,json,math,pathlib,statistics,urllib.request
COMMIT='aa9bddf498a3b6e4104c2c000d2cc0c06a816aae'
PINS={'left':'509e14d61455dc6ee119a0fc2ba9e7448eedc9fc','right':'9f55dd52fc6c11c9903ec9c7b0c735192cd4a790'}
D=pathlib.Path('research/e002-257')
def load(eye):
    name=f'per_participant_{eye}_eye.csv'
    url=f'https://raw.githubusercontent.com/CondadosAI/pupil-diameter-webcam/{COMMIT}/output/{name}'
    with urllib.request.urlopen(url,timeout=40) as f: raw=f.read()
    got=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    if got!=PINS[eye]: raise ValueError('SOURCE_IDENTITY_FAIL')
    return [{k:float(v) for k,v in row.items()} for row in csv.DictReader(io.StringIO(raw.decode('utf-8-sig')))],{'sha256':hashlib.sha256(raw).hexdigest(),'git_blob':got,'url':url}
def metric(x):
    n,b,sy,sx,r=[x[k] for k in ('n','bias_mm','gt_std_mm','pred_std_mm','pearson_r')]
    centered=(n-1)/n*(sx*sx+sy*sy-2*r*sx*sy)
    raw=math.sqrt(b*b+centered)
    if x['mae_mm']>raw+1e-8: raise ValueError('MAE_EXCEEDS_RMSE')
    return raw/sy,math.sqrt(centered)/sy,abs(b)/sy
def run():
    left,lm=load('left');right,rm=load('right')
    a={int(x['participant']):metric(x) for x in left}
    b={int(x['participant']):metric(x) for x in right}
    if set(a)!=set(b) or len(a)!=51: raise ValueError('UNPAIRED')
    d=[b[i][0]-a[i][0] for i in a]
    def summarize(v):return {'raw_median':statistics.median(x[0] for x in v),'offset_median':statistics.median(x[1] for x in v),'bias_median':statistics.median(x[2] for x in v),'raw_le_0p7':sum(x[0]<=.7 for x in v)}
    pos=sum(x>0 for x in d);neg=sum(x<0 for x in d);n=pos+neg
    p=min(1,2*sum(math.comb(n,k) for k in range(min(pos,neg)+1))/2**n)
    out={'classification':'third_party_posthoc','left':summarize(a.values()),'right':summarize(b.values()),'paired':{'right_worse':pos,'right_better':neg,'median_diff':statistics.median(d),'sign_p':p},'human_waveform':'NOT_RUN'}
    D.mkdir(parents=True,exist_ok=True)
    (D/'RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    (D/'SOURCE_MANIFEST.json').write_text(json.dumps({'commit':COMMIT,'files':{'left':lm,'right':rm}},indent=2)+'\n')
if __name__=='__main__':run()
