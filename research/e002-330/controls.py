"""E002-330 negative controls, synthetic only."""
import numpy as np,json
def main():
    geom=(abs(11-0)<=10)!=(abs(11-2)<=10)
    naive=(120-.8*(.5*120+.5*20))/100
    w=np.array([1,1,0,0]);q1=np.array([0,0,1,1]);q2=np.zeros(4)
    missing=np.dot(w,q1)==np.dot(w,q2) and q1.mean()!=q2.mean()
    t=np.arange(1024)/1024
    a=10+3*np.sin(2*np.pi*t);b=10-3*np.sin(2*np.pi*t)
    smooth=np.allclose(np.sort(a),np.sort(b)) and np.isclose(np.sum(np.gradient(a)**2),np.sum(np.gradient(b)**2))
    assert geom and naive==.64 and missing and smooth
    print(json.dumps(dict(status="PASS",geometry_only=geom,brightness_wrong_gain=naive,missingness_only=missing,smoothness_only=smooth,human="NOT RUN")))
if __name__=="__main__":main()
