"""E002-371 exact-rational boxcar shutter instrument surrogate (synthetic only)."""
from fractions import Fraction as F
import csv, io

def aperture(t, center, a, speed):
    return min(a, speed * abs(t-center))

def mean_aperture(center, a, speed, start, duration):
    end=start+duration
    knots=sorted(set([start,end,center,center-a/speed,center+a/speed]))
    knots=[t for t in knots if start<=t<=end]
    total=sum((aperture(x,center,a,speed)+aperture(y,center,a,speed))*(y-x)/2 for x,y in zip(knots,knots[1:]))
    return total/duration

def run():
    V=F(100) # hypothetical mm/s, NOT physiological certification
    A=F(2) # mm
    E=F(1,100) # 10ms
    rows=[]
    for gap_ms in [10,20,29,30,31,40,50]:
        G=F(gap_ms,1000)
        center=G/2
        left=mean_aperture(center,A,V,-E,E)
        right=mean_aperture(center,A,V,G,E)
        l=max(F(0),left-V*E/2)
        r=max(F(0),right-V*E/2)
        naive=left+right>V*G
        corrected=l+r>V*G
        actual_closed=aperture(center,center,A,V)==0
        rows.append((gap_ms,str(left),str(right),str(l),str(r),int(naive),int(corrected),int(actual_closed)))
        assert not (corrected and actual_closed), 'unsafe corrected exclusion'
    assert any(row[5] and row[7] for row in rows), 'expected naive counterexample absent'
    output=io.StringIO()
    w=csv.writer(output)
    w.writerow(['gap_ms','left_mean_mm','right_mean_mm','left_lower_mm','right_lower_mm','naive_excludes','corrected_excludes','actual_hidden_closure'])
    w.writerows(rows)
    print(output.getvalue())

if __name__=='__main__':
    run()
