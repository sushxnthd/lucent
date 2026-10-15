#!/usr/bin/env python3
"""E002-210 wildcard: periodic waveform aliasing, synthetic only."""
import json,math
f,fs,n,delta=2.0,30.0,150,0.5
x=[math.sin(2*math.pi*f*i/fs) for i in range(n)]
y=[math.sin(2*math.pi*f*(i/fs-delta)) for i in range(n)]
err=math.sqrt(sum((a-b)**2 for a,b in zip(x,y))/n)
mx=sum(x)/n;my=sum(y)/n
r=sum((a-mx)*(b-my) for a,b in zip(x,y))/math.sqrt(sum((a-mx)**2 for a in x)*sum((b-my)**2 for b in y))
assert err<1e-12 and abs(r-1)<1e-12
print(json.dumps({"kind":"SYNTHETIC_WILDCARD","frequency_hz":f,"fps":fs,"samples":n,"clock_shift_ms":delta*1000,"pearson_r":r,"rmse":err,"human_pairs":0,"claim":"periodic waveform is unchanged by an integer-period clock shift"},indent=2))
