"""Independent E002-110 original-Zenodo CRC-checked IR PFT replication.
Run: python replicate.py > e002_110_results.json
"""
import csv, io, itertools, json, struct, zlib
import numpy as np
import requests

API = 'https://zenodo.org/api/records/18429496'
FREQS = [1., 1.1111, 1.25, 1.4286, 1.6667, 2., 2.5, 3.3333, 5.]
OFF = FREQS[1:]
PUBLISHED = {
 'sub1': {'area_contrast':.36567870448941875,'y_ratio':.5339794176212431,'active_retention':.4838838202078867},
 'sub2': {'area_contrast':.34673175165780423,'y_ratio':.6975857975918501,'active_retention':.4737959426164722},
 'sub3': {'area_contrast':.3758042065446744,'y_ratio':1.0936118934536991,'active_retention':.5996964615440776}}

def range_get(session,url,start,n):
    r=session.get(url,headers={'Range':f'bytes={start}-{start+n-1}'},timeout=120)
    if r.status_code!=206 or len(r.content)!=n:
        raise RuntimeError(f'HTTP Range integrity failed: {r.status_code}, {len(r.content)} expected {n}')
    return r.content

def directory(fetch,total):
    tail=fetch(total-min(total,131072),min(total,131072));i=tail.rfind(b'PK\x05\x06')
    if i<0:raise ValueError('Missing ZIP EOCD')
    _,disk,cd_disk,on_disk,count,size,off,comment=struct.unpack_from('<4s4H2IH',tail,i)
    if disk or cd_disk or on_disk!=count or off==0xffffffff:raise ValueError('Unsupported ZIP')
    b=fetch(off,size); p=0; out={}; fmt='<4s6H3I5H2I';h=struct.calcsize(fmt)
    while p<len(b):
        a=struct.unpack_from(fmt,b,p)
        if a[0]!=b'PK\x01\x02':raise ValueError('Bad ZIP central directory')
        fn,ex,com=a[10:13];name=b[p+h:p+h+fn].decode('utf-8')
        out[name]=(a[16],a[8],a[9],a[7],a[4]);p+=h+fn+ex+com
    if len(out)!=count:raise ValueError('Directory entry count mismatch')
    return out

def member(fetch,entry):
    off,compressed,uncompressed,crc,method=entry
    hdr=fetch(off,30)
    if hdr[:4]!=b'PK\x03\x04':raise ValueError('Bad ZIP member header')
    fn,ex=struct.unpack_from('<HH',hdr,26)
    b=fetch(off+30+fn+ex,compressed)
    raw=zlib.decompress(b,-15) if method==8 else b if method==0 else None
    if raw is None or len(raw)!=uncompressed or zlib.crc32(raw)&0xffffffff!=crc:
        raise ValueError('Member CRC32/size failed')
    return raw

def read_runs(raw):
    rows=list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))))
    if len(rows)!=4500:raise ValueError('Expected 4500 frames')
    groups=[list(g) for _,g in itertools.groupby(rows,key=lambda r:r['signal'])]
    stim=[g for g in groups if g[0]['signal']]
    if len(stim)!=9 or any(len(g)!=400 for g in stim):raise ValueError('Invalid stimulus runs')
    runs={round(float(g[0]['signal']),4):g for g in stim}
    if sorted(runs)!=FREQS:raise ValueError('Unexpected stimulus frequencies')
    return runs

def arrays(run,channel):
    w=run[:100];t=np.array([float(r['timestamp']) for r in w]);t-=t[0]
    a=np.array([float(r['pupilSize']) if r['pupilSize'] else np.nan for r in w]);p=np.array([float(r[channel]) if r[channel] else np.nan for r in w])
    valid=np.isfinite(t)&np.isfinite(a)&np.isfinite(p)&(a>0)
    if sum(valid)<80:raise ValueError('Insufficient valid frames')
    t,a,p=t[valid],a[valid],p[valid]
    X=np.column_stack((np.ones(len(t)),t,np.sin(2*np.pi*t),np.cos(2*np.pi*t)))
    return X,t,a,p

def amplitude(X,y):
    b=np.linalg.lstsq(X,y,rcond=None)[0]
    return float(np.hypot(b[-2],b[-1]))

def placebos(run,channel):
    X,t,a,p=arrays(run,channel);T=t[-1];ref=amplitude(X,p)
    xf=np.column_stack((X[:,:2],np.exp(-t/1.5),X[:,2:]))
    xr=np.column_stack((X[:,:2],np.exp(-(T-t)/1.5),X[:,2:]))
    return amplitude(xf,p)/ref,amplitude(xr,p)/ref

def slope(groups):
    num=den=0.
    for X,t,a,p in groups:
        ar=a-X@np.linalg.lstsq(X,a,rcond=None)[0]
        pr=p-X@np.linalg.lstsq(X,p,rcond=None)[0]
        num+=float(ar@pr);den+=float(pr@pr)
    return num/den

def score(runs):
    area=[placebos(runs[f],'pupilSize') for f in OFF]
    y=[placebos(runs[f],'pupCntr_y') for f in OFF]
    area_contrast=float(np.median([v[1] for v in area])-np.median([v[0] for v in area]))
    y_contrast=float(np.median([v[1] for v in y])-np.median([v[0] for v in y]))
    y_wins=sum(f<1 and r>1 for f,r in y)
    off={f:arrays(runs[f],'pupCntr_y') for f in OFF}
    ratios=[]
    for f in OFF:
        b=slope([off[q] for q in OFF if q!=f]);X,t,a,p=off[f]
        ratios.append(amplitude(X,a-b*(p-np.median(p)))/amplitude(X,a))
    b=slope(list(off.values()));X,t,a,p=arrays(runs[1.],'pupCntr_y')
    retention=amplitude(X,a-b*(p-np.median(p)))/amplitude(X,a)
    return {'area_contrast':area_contrast,'area_directional_wins':sum(f<1 and r>1 for f,r in area),
            'y_contrast':y_contrast,'y_directional_wins':y_wins,'y_mimic':bool(y_contrast>=.1 and y_wins>=6),
            'y_heldout_median_ratio':float(np.median(ratios)),'y_heldout_improved':sum(x<1 for x in ratios),
            'active_retention':float(retention),'y_correction_gate':bool(np.median(ratios)<=.75 and sum(x<1 for x in ratios)>=6 and retention>=.8)}

def main():
    with requests.Session() as s:
        r=s.get(API,timeout=60);r.raise_for_status()
        f=next(f for f in r.json()['files'] if f['key']=='data.zip')
        fetch=lambda start,n:range_get(s,f['links']['self'],start,n)
        entries=directory(fetch,int(f['size']))
        scores={}
        for sub in ('sub1','sub2','sub3'):
            path=f'data/pft/{sub}.csv';scores[sub]=score(read_runs(member(fetch,entries[path])))
    checks={sub:{'area_contrast_match_1e-5':abs(scores[sub]['area_contrast']-PUBLISHED[sub]['area_contrast'])<1e-5,
                 'y_ratio_match_0p01':abs(scores[sub]['y_heldout_median_ratio']-PUBLISHED[sub]['y_ratio'])<.01,
                 'active_retention_match_0p01':abs(scores[sub]['active_retention']-PUBLISHED[sub]['active_retention'])<.01}
            for sub in scores}
    out={'experiment':'E002-110','source':'Zenodo 18429496','modality':'IR, NOT RGB',
         'original_member_crc32_verified':True,'full_archive_md5_verified':False,
         'independent_original_replication_pass':all(all(x.values()) for x in checks.values()),
         'checks':checks,'subjects':scores,'no_fatigue_or_RGB_claim':True}
    print(json.dumps(out,indent=2))
    if not out['independent_original_replication_pass']:raise SystemExit(2)
if __name__=='__main__':main()
