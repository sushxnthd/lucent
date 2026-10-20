"""E002-330: ideal linear RGB exposure; NumPy required. Synthetic only."""
import numpy as np, json, hashlib
from pathlib import Path
N=64; H=W=80; center=40; iris_radius=20
yy,xx=np.ogrid[:H,:W]; d2=(xx-center)**2+(yy-center)**2
skin=np.array([220,200,180],dtype=np.int64)
iris=np.array([120,100,80],dtype=np.int64)
pupil=np.array([20,20,20],dtype=np.int64)
def image(r):
    z=np.broadcast_to(skin,(H,W,3)).copy()
    z[d2<=iris_radius**2]=iris
    z[d2<=int(r)**2]=pupil
    return z
def integrate(rs):
    a=np.zeros((H,W,3),dtype=np.int64)
    for r in rs: a+=image(r)
    return a
def run():
    rows=[]
    for base,amp in [(10,4),(11,3),(9,2)]:
        t=2*np.pi*np.arange(N)/N
        a=base+np.rint(amp*np.sin(t)).astype(int)
        b=np.roll(a,N//2)
        A,B=integrate(a),integrate(b)
        assert np.array_equal(A,B) and a[N//4]!=b[N//4]
        for k in range(1,iris_radius):
            num=int(N*iris[0]-A[center,center+k,0])
            den=int(N*(iris[0]-pupil[0]))
            assert num*N==den*int(np.sum(a>=k))
        rows.append(dict(base=base,amplitude=amp,quarter=[int(a[N//4]),int(b[N//4])],sha256=hashlib.sha256(A.tobytes()).hexdigest(),max_pixel_diff=0))
    rng=np.random.default_rng(330)
    for _ in range(300):
        rs=rng.integers(4,18,size=32)
        assert np.array_equal(integrate(rs),integrate(rs[rng.permutation(32)]))
    print(json.dumps(dict(status="PASS",human="NOT RUN",collisions=rows,random_permutations=300),indent=2))
if __name__=="__main__":run()
