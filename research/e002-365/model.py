"""Sharp PERCLOS intervals from calibrated rectangular shutter moments.
Requires scipy, numpy. Conditional synthetic measurement model only."""
import numpy as np
from scipy.optimize import linprog

def make_windows(T=1., fps=30., exposure=.010, offsets=(0.,)):
    windows=[]
    for k in range(int(np.ceil(T*fps))+1):
        for off in offsets:
            a=k/fps+off; b=a+exposure
            if a >= T-1e-11 or b <= 0: continue
            windows.append((max(0.,a),min(T,b)))
    return np.asarray(windows)

def atoms_matrix(windows,T=1.):
    edges=np.unique(np.round(np.r_[0.,T,windows.ravel()],12))
    lo=edges[:-1]; hi=edges[1:]; widths=hi-lo
    A=np.maximum(0.,np.minimum(windows[:,1,None],hi[None,:])-np.maximum(windows[:,0,None],lo[None,:]))
    return edges,widths,A

def binary_truth_integrals(windows,closures):
    return np.array([sum(max(0.,min(b,d)-max(a,c)) for c,d in closures) for a,b in windows])

def bounds(windows,y,T=1.,eta=0.):
    edges,widths,A=atoms_matrix(windows,T)
    constraints=(dict(A_ub=np.vstack([A,-A]),b_ub=np.r_[y+eta,-y+eta]) if eta else dict(A_eq=A,b_eq=y))
    solutions=[]
    for sign in (1,-1):
        r=linprog(sign*widths,bounds=(0,1),method='highs',**constraints)
        if not r.success:raise RuntimeError(r.message)
        solutions.append(r.x)
    lo,hi=[float(widths@x/T) for x in solutions]
    return dict(lower=lo,upper=hi,width=hi-lo,edges=edges,widths=widths,A=A,solutions=solutions)

def realize_binary(edges,occupancies):
    return [(float(a),float(a+(b-a)*x)) for a,b,x in zip(edges[:-1],edges[1:],occupancies) if x>1e-10]

if __name__=='__main__':
    closures=[(.12,.24),(.42,.56),(.70,.78)]
    for name,fps,offs in [('10hz',10.,(0.,)),('30hz',30.,(0.,)),('rolling_8ms',30.,(0.,.004,.008)),('rolling_16ms',30.,(0.,.004,.008,.012,.016))]:
        w=make_windows(1.,fps,.010,offs)
        z=bounds(w,binary_truth_integrals(w,closures))
        print(name,z['lower'],z['upper'])
    w=make_windows(1.,30.,.010,np.arange(7)*.004)
    e,d,A=atoms_matrix(w); y=A@(.5*np.ones(len(d)))
    z=bounds(w,y)
    assert np.all(A.sum(axis=0)>1e-12)
    for x in z['solutions']:
        assert np.allclose(binary_truth_integrals(w,realize_binary(e,x)),y,atol=1e-9)
    print('complete coverage collision',z['lower'],z['upper'])
