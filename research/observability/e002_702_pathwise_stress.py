"""E002-702: independent pathwise randomized falsification of joint-uncertainty bound.
Synthetic only. Standard library. Reproducible fixed seed.
"""
import random, json
R=random.Random(702)
N=100000
naive=robust=naive_false=robust_false=0
examples=[]
for _ in range(N):
    v=R.uniform(.3,1.0); gap=R.uniform(.4,.7)
    a=R.uniform(0,1); b=max(0,min(1,a+R.uniform(-v*gap,v*gap)))
    mid=max(0,min(1,(a+b)/2-R.uniform(0,v*gap/2)))
    if max(abs(mid-a),abs(b-mid))>v*gap/2+1e-12: continue
    err_a=R.uniform(-.1,.1); err_b=R.uniform(-.1,.1)
    ma=a+err_a; mb=b+err_b
    nominal=(ma+mb-.5*.5)/2>.5
    conservative=(ma-.1+mb-.1-1.0*.7)/2>.5
    closure=mid<=.5
    naive+=nominal; robust+=conservative
    naive_false+=nominal and closure; robust_false+=conservative and closure
    if nominal and closure and len(examples)<3:
        examples.append(dict(a=a,b=b,mid=mid,v=v,gap=gap,ma=ma,mb=mb))
print(json.dumps(dict(attempts=N,naive_certificates=naive,naive_false_exclusions=naive_false,robust_certificates=robust,robust_false_exclusions=robust_false,examples=examples),indent=2))
assert robust_false==0
