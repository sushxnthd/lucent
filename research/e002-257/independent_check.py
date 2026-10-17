#!/usr/bin/env python3
"""Independent uncentered-moment checker for E002-257; source-pinned."""
import csv,hashlib,io,json,math,pathlib,statistics,urllib.request
C='aa9bddf498a3b6e4104c2c000d2cc0c06a816aae'
P={'left':'509e14d61455dc6ee119a0fc2ba9e7448eedc9fc','right':'9f55dd52fc6c11c9903ec9c7b0c735192cd4a790'}
out=json.loads(pathlib.Path('research/e002-257/RESULTS.json').read_text())
for eye in P:
    u=f'https://raw.githubusercontent.com/CondadosAI/pupil-diameter-webcam/{C}/output/per_participant_{eye}_eye.csv'
    with urllib.request.urlopen(u,timeout=40) as f: raw=f.read()
    assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==P[eye]
    rows=list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))))
    v=[]
    for q in rows:
        n=float(q['n']);ym=float(q['gt_mean_mm']);xm=ym+float(q['bias_mm'])
        sy=float(q['gt_std_mm']);sx=float(q['pred_std_mm']);r=float(q['pearson_r'])
        ex2=((n-1)*sx*sx+n*xm*xm)/n
        ey2=((n-1)*sy*sy+n*ym*ym)/n
        exy=((n-1)*r*sx*sy+n*xm*ym)/n
        v.append(math.sqrt(max(0,ex2+ey2-2*exy))/sy)
    assert len(v)==51
    assert math.isclose(statistics.median(v),out[eye]['raw_median'],abs_tol=1e-8)
print('INDEPENDENT_HUMAN_AGGREGATE_MOMENT_CHECK_PASS')
