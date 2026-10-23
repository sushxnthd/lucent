#!/usr/bin/env python3
"""Independent E002-388 interval oracle and real encoded-file verification."""
import json, sys, subprocess
from pathlib import Path
p=Path(sys.argv[1] if len(sys.argv)>1 else 'e002_388_out')
d=json.loads((p/'e002_388_results.json').read_text())
checks=0
for r in d['rows']:
    if r['kind']=='open': expected=0.
    else:
        entry=.015 if r['kind']=='long' else .004
        dwell=.05 if r['kind']=='long' else .008
        begin=.55+r['phase_ms']/1000+entry; end=begin+dwell
        expected=0.
        for i in range(60):
            a=i/30; b=a+.01
            if begin<b and a<end:
                expected=max(expected,min(b,end)-max(a,begin))
    assert abs(r['max_full_plateau_overlap_ms']-1000*expected)<.00001
    assert r['source_full_exposure']==(expected>=.01-1e-10)
    assert r['source_overlap_ge_4ms']==(expected>=.004-1e-10)
    checks+=3
for name in ('example_clean_long_h264.mp4','example_adverse_open_h264.mp4'):
    q=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0',
      '-show_entries','stream=codec_name,nb_frames,r_frame_rate','-of','json',str(p/name)]))
    s=q['streams'][0]
    assert s['codec_name']=='h264' and s['nb_frames']=='60' and s['r_frame_rate']=='30/1'
    checks+=3
assert all(d['frozen_predictions'].values())
print(f'PASS {checks} independent interval/codec checks across {len(d["rows"])} conditions')
