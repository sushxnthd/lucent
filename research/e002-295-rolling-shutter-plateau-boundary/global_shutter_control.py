import json
from pathlib import Path
H=40.;T=.02;tau=20e-6;v=1600.
g=v*T;r=v*T/(1-v*tau)
out=dict(global_width_px=g,rolling_width_px=r,rolling_correction=r/g-1,
 global_critical=H/T,rolling_critical=H/(T+tau*H),
 interpretation='Motion blur is primary; rolling shutter is correction')
Path(__file__).with_name('global_shutter_control.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))