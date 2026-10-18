#!/usr/bin/env python3
"""E002-280: phase-blind blink sampling test; synthetic only."""
import json
from pathlib import Path
P=Path(__file__).resolve().parent
q=21/26
cases=[("30fps_half",30,1/60),("10fps_short",10,1/60),
       ("60fps_half",60,1/120),("30fps_full",30,1/30),
       ("unseen_24fps_quarter",24,1/96)]
def overlap(x,d,a,b):
    return max(0,min(x+d,b)-max(x,a))
def max_fraction(x,d,f,T):
    period=1/f
    return max(overlap(x,d,k*period,k*period+T)/T for k in range(-1,4))
def run():
    rows=[]
    for name,f,T in cases:
        period=1/f
        critical=period-T+2*q*T
        tests={}
        for side,delta in [("below",-0.001),("above",0.001)]:
            d=critical+delta
            detected=sum(max_fraction(j*period/4096,d,f,T)>q+1e-12 for j in range(4096))
            worst_start=(period+T-d)/2
            worst=max_fraction(worst_start,d,f,T)
            tests[side]={"duration_ms":1000*d,"detected":detected,"total":4096,"worst_fraction":worst}
        assert tests["below"]["worst_fraction"]<q
        assert tests["above"]["detected"]==4096
        rows.append({"camera":name,"fps":f,"exposure":T,"critical_ms":1000*critical,"tests":tests})
    output={"human_data":False,"model":{"q":q,"R0":0.25,"Rref":0.75,"Delta":0.65,"noise":0.01,"min_slope":0.8},"cases":rows}
    (P/"results.json").write_text(json.dumps(output,indent=2)+"\n")
    return output
if __name__=="__main__":
    for x in run()["cases"]:
        print(x["camera"],round(x["critical_ms"],3),x["tests"]["below"]["detected"],x["tests"]["above"]["detected"])
