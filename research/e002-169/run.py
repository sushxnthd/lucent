import json, math
from pathlib import Path
# Published EyeBlink8 Table 3: video ID, annotated blink count, rate/minute
rows=[(1,38,4.4),(2,88,14.3),(3,65,12.7),(4,31,10.3),(8,30,5.3),(9,41,16.2),(10,72,14.2),(11,43,17.6)]
def metrics(rate):
    mean=rate/12
    return dict(mean=mean,p_zero=math.exp(-mean),crlb_relative_sd=1/math.sqrt(mean),seconds_for_20pct_sd=1500/rate)
result=dict(experiment="E002-169",source="https://www.mdpi.com/2078-2489/9/4/93 Table 3",model="homogeneous Poisson; perfect event counting",window_seconds=5,rows=[dict(video=v,gt_blinks=n,rate_per_minute=r,**metrics(r)) for v,n,r in rows],example_12_per_minute=metrics(12),reference="published summary only; no original event timestamps or video")
Path(__file__).with_name("RESULTS.json").write_text(json.dumps(result,indent=2)+"\n")
print("PASS",len(rows))
