#!/usr/bin/env python3
"""E002-388: prospectively frozen synthetic H264 video instrument. Not human evidence."""
import json, subprocess, tempfile, argparse
from pathlib import Path
from functools import lru_cache
import numpy as np
import cv2

FPS=30.; EXPO=.010; NFRAMES=60; NSUB=10; W=96; H=64
ROI=np.s_[20:44,25:71]

def aperture(t, phase, kind):
    if kind=='open': return 1.
    start=.55+phase; enter=.015 if kind=='long' else .004
    dwell=.050 if kind=='long' else .008
    if t<start: return 1.
    if t<start+enter: return 1.-(t-start)/enter
    if t<start+enter+dwell: return 0.
    if t<start+2*enter+dwell: return (t-start-enter-dwell)/enter
    return 1.

@lru_cache(maxsize=2000)
def render(ap, adverse=False):
    yy,xx=np.mgrid[0:H,0:W]
    skin=.73+.025*np.cos((xx-48.)/25.)
    cx=48+(17 if adverse else 0)
    cy=32+(8 if adverse else 0)
    pupil=(abs(yy-cy)<12*ap)&(abs(xx-cx)<31)
    arr=np.where(pupil,.12+.012*np.sin(xx*.17),skin).astype(np.float64)
    arr+=.008*np.sin(xx*.41+yy*.22)
    if adverse:
        arr*=1.18
        glare=(xx>=38)&(xx<=53)&(yy>=15)&(yy<=49)
        arr[glare]=.98
        arr=cv2.GaussianBlur(arr,(5,5),1.2)
    return np.clip(arr,0,1)

def frames_for(kind,phase,adverse):
    frames=[]; means=[]
    for k in range(NFRAMES):
        times=k/FPS+(np.arange(NSUB)+.5)*EXPO/NSUB
        aps=np.array([aperture(float(t),phase,kind) for t in times])
        im=np.mean([render(round(float(a),6),adverse) for a in aps],axis=0)
        frames.append(np.repeat(np.rint(im*255).astype(np.uint8)[:,:,None],3,axis=2))
        means.append(float(aps.mean()))
    return frames,means

def encode_decode(frames,crf,path):
    raw=b''.join(x.tobytes() for x in frames)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo',
         '-pix_fmt','rgb24','-s',f'{W}x{H}','-r','30','-i','pipe:0',
         '-c:v','libx264','-preset','ultrafast','-threads','1',
         '-crf',str(crf),'-pix_fmt','yuv420p',str(path)]
    p=subprocess.run(cmd,input=raw,capture_output=True)
    if p.returncode: raise RuntimeError(p.stderr.decode())
    cap=cv2.VideoCapture(str(path));out=[]
    while True:
        ok,frame=cap.read()
        if not ok:break
        out.append(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
    cap.release()
    assert len(out)==len(frames)
    return out

def signal(frames):
    return np.array([float(np.mean(f[ROI]))/255 for f in frames])

def overlap(phase,kind):
    if kind=='open':return 0.
    start=.55+phase;enter=.015 if kind=='long' else .004
    lo=start+enter;hi=lo+(.05 if kind=='long' else .008)
    return max(max(0.,min(k/FPS+EXPO,hi)-max(k/FPS,lo)) for k in range(NFRAMES))

def gate(adverse=False,timing=True,optics=True,human_speed=False):
    return not adverse and timing and optics and human_speed

def run(out,nphase=20):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    rows=[];phases=[k/FPS/nphase for k in range(nphase)]
    with tempfile.TemporaryDirectory() as temp:
      temp=Path(temp)
      for crf in (18,40):
        cals={}
        for kind,ap in (('open',1.),('closed',0.)):
            im=np.repeat(np.rint(render(ap)*255).astype(np.uint8)[:,:,None],3,axis=2)
            cals[kind]=float(np.median(signal(encode_decode([im]*NFRAMES,crf,temp/f'cal_{kind}_{crf}.mp4'))))
        den=cals['open']-cals['closed']
        assert abs(den)>.01
        for adverse in (False,True):
          for kind in ('long','short','open'):
            for pi,phase in enumerate(phases):
                frames,meanap=frames_for(kind,phase,adverse)
                path=temp/f'{kind}_{crf}_{int(adverse)}_{pi}.mp4'
                decoded=encode_decode(frames,crf,path)
                est=np.clip((signal(decoded)-cals['closed'])/den,0,1)
                error=np.abs(est-np.array(meanap))
                ov=overlap(phase,kind)
                rows.append({'kind':kind,'crf':crf,'adverse':adverse,
                  'phase_index':pi,'phase_ms':round(phase*1000,6),
                  'max_full_plateau_overlap_ms':round(ov*1000,6),
                  'source_full_exposure':bool(ov>=EXPO-1e-10),
                  'source_overlap_ge_4ms':bool(ov>=.004-1e-10),
                  'encoded_threshold_detected':bool(np.any(est<=.2)),
                  'max_abs_aperture_error':round(float(error.max()),6),
                  'mean_abs_aperture_error':round(float(error.mean()),6)})
                if kind=='long' and pi==0 and crf==18 and not adverse:
                    (out/'example_clean_long_h264.mp4').write_bytes(path.read_bytes())
                if kind=='open' and pi==0 and crf==40 and adverse:
                    (out/'example_adverse_open_h264.mp4').write_bytes(path.read_bytes())
    groups={}
    for crf in (18,40):
      for adverse in (False,True):
        for kind in ('long','short','open'):
          a=[r for r in rows if r['crf']==crf and r['adverse']==adverse and r['kind']==kind]
          groups[f'{kind}_crf{crf}_{"adverse" if adverse else "clean"}']={
             'n':len(a),'source_full_exposure_rate':sum(x['source_full_exposure'] for x in a)/len(a),
             'source_overlap_ge_4ms_rate':sum(x['source_overlap_ge_4ms'] for x in a)/len(a),
             'encoded_detection_rate':sum(x['encoded_threshold_detected'] for x in a)/len(a),
             'max_aperture_error':max(x['max_abs_aperture_error'] for x in a)}
    checks={
      'P1_long_source_full_exposure_all_phases':all(r['source_full_exposure'] for r in rows if r['kind']=='long'),
      'P2_short_source_4ms_overlap_not_all_phases':any(not r['source_overlap_ge_4ms'] for r in rows if r['kind']=='short'),
      'P3_unseen_nuisance_exceeds_clean_error':all(
        max(v['max_aperture_error'] for k,v in groups.items() if f'crf{crf}_adverse' in k)>
        max(v['max_aperture_error'] for k,v in groups.items() if f'crf{crf}_clean' in k) for crf in (18,40)),
      'P4_fail_closed_qualified_metadata':not gate() and not gate(adverse=True,human_speed=True) and gate(human_speed=True)}
    result={'experiment':'E002-388','evidence':'synthetic encoded video; not a physical camera or human validation',
      'frozen_predictions':checks,'groups':groups,'rows':rows,
      'ffmpeg_version':subprocess.check_output(['ffmpeg','-version'],text=True).splitlines()[0],
      'opencv_version':cv2.__version__}
    (out/'e002_388_results.json').write_text(json.dumps(result,indent=2))
    assert all(checks.values())
    print(json.dumps({'checks':checks,'groups':groups},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default='e002_388_out')
    p.add_argument('--nphase',type=int,default=20);a=p.parse_args()
    run(a.output,a.nphase)
