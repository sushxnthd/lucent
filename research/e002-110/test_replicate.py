import io, zipfile
import numpy as np
import replicate as r

def test_zip_member_crc():
    mem=io.BytesIO()
    with zipfile.ZipFile(mem,'w',compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr('data/pft/sub1.csv','signal,timestamp,pupilSize,pupCntr_y\n')
    blob=mem.getvalue()
    fetch=lambda start,n:blob[start:start+n]
    d=r.directory(fetch,len(blob))
    assert r.member(fetch,d['data/pft/sub1.csv'])==b'signal,timestamp,pupilSize,pupCntr_y\n'

def test_sine():
    t=np.arange(100)/20
    X=np.c_[np.ones(100),t,np.sin(2*np.pi*t),np.cos(2*np.pi*t)]
    assert abs(r.amplitude(X,4+3*t+2*np.sin(2*np.pi*t)+5*np.cos(2*np.pi*t))-np.hypot(2,5))<1e-10

def test_slope():
    t=np.arange(100)/20
    X=np.c_[np.ones(100),t,np.sin(2*np.pi*t),np.cos(2*np.pi*t)]
    p=np.sin(2*np.pi*.73*t);a=1500-4*p+20*np.sin(2*np.pi*t)
    assert abs(r.slope([(X,t,a,p)])+4)<1e-8
