"""E002-034: identical pupil/iris observations, opposite true waveforms.
No human measurements or novel-normalization claim. Python standard library only.
"""
import math

def std(x):
    m = sum(x) / len(x)
    return (sum((v-m)**2 for v in x) / len(x))**0.5

def experiment():
    t = [k/30 for k in range(150)]
    x = [-0.08*math.exp(-((v-1.9)/0.75)**2)+0.015*math.sin(2*math.pi*0.37*v) for v in t]
    d = [0.06*math.sin(2*math.pi*0.19*v+0.3) for v in t]
    x = [v-sum(x)/len(x) for v in x]
    d = [v-sum(d)/len(d) for v in d]
    p = [a+b for a,b in zip(x,d)]
    i = d
    # World A: true pupil=x, scale=d, iris bias=0.
    # World B: true pupil=p, scale=0, iris bias=d.
    # The two worlds have IDENTICAL observed p and i.
    return {
        'A_raw': std([a-b for a,b in zip(p,x)]),
        'A_ratio': std([a-b-c for a,b,c in zip(p,i,x)]),
        'B_raw': 0.0,
        'B_ratio': std(i),
    }

if __name__ == '__main__':
    r = experiment()
    print(r)
    assert abs(r['A_raw']-r['B_ratio']) < 1e-12
    assert r['A_ratio'] < 1e-12 and r['B_raw'] == 0
    assert r['A_raw'] > 0.02
