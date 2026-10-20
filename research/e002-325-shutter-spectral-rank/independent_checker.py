"""Independent E002-325 checker: numerical antiderivative, rank and stability."""
import json
import numpy as np

def integrated_sinusoid(f, n, fps, E):
    H=np.sinc(f*E)*np.exp(1j*np.pi*f*E)
    t0=n/fps
    t1=t0+E
    return .5+.03*(np.sin(2*np.pi*f*t1-np.angle(H))-
                     np.sin(2*np.pi*f*t0-np.angle(H)))/(2*np.pi*f*E*abs(H))

def design(indices,N,K,E):
    k=np.arange(-K,K+1)
    H=np.array([(np.exp(2j*np.pi*f*E)-1)/(2j*np.pi*f*E)
                if f else 1 for f in k])
    return np.exp(2j*np.pi*np.outer(indices,k)/N)*H

n=np.arange(10)
y4=np.array([integrated_sinusoid(4,i,10,.01) for i in n])
ym6=np.array([integrated_sinusoid(-6,i,10,.01) for i in n])
alias_error=float(np.max(abs(y4-ym6)))
assert alias_error<1e-12

N=30; K=6; E=.012
spaced=np.round(np.linspace(0,29,13)).astype(int)
clustered=np.arange(13)
rank12=int(np.linalg.matrix_rank(design(spaced[:12],N,K,E)))
rank13=int(np.linalg.matrix_rank(design(spaced,N,K,E)))
assert rank12==12 and rank13==13
s_spaced=float(np.linalg.svd(design(spaced,N,K,E),compute_uv=False)[-1])
s_cluster=float(np.linalg.svd(design(clustered,N,K,E),compute_uv=False)[-1])
assert s_spaced>.5 and s_cluster<1e-4
assert .1*s_spaced>2*.001 and .1*s_cluster<2*.001

rng=np.random.default_rng(3252026)
worst=0
for i in range(300):
    c=np.zeros(2*K+1,dtype=complex)
    c[K]=rng.normal()
    for j in range(1,K+1):
        v=rng.normal()+1j*rng.normal()
        c[K+j]=v
        c[K-j]=np.conj(v)
    A=design(np.arange(N),N,K,E)
    rec=np.linalg.lstsq(A,A@c,rcond=None)[0]
    worst=max(worst,float(np.linalg.norm(rec-c)/np.linalg.norm(c)))
assert worst<1e-10

# Unknown per-frame positive gain is a gauge, not an ocular measurement.
t=np.arange(N)
x1=.5+.02*np.cos(2*np.pi*3*t/N)
x2=.5+.02*np.cos(2*np.pi*4*t/N)
g=x1/x2
assert np.max(abs(g*x2-x1))<1e-14

result=dict(status="PASS",alias_error=alias_error,rank12=rank12,
            rank13=rank13,sigma_spaced=s_spaced,sigma_clustered=s_cluster,
            condition_ratio=s_spaced/s_cluster,recovery_trials=300,
            worst_recovery_error=worst,gain_deviation=float(max(abs(g-1))),
            human_evidence=False)
print(json.dumps(result,indent=2))
