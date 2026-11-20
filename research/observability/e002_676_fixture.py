"""E002-676 synthetic shutter-gap instrument challenge. Standard library only."""
import csv, argparse
from fractions import Fraction as F

def aperture(t, gap, speed):
    return max(F(0), F(1)-speed*min(t,gap-t))

def run():
    p=argparse.ArgumentParser()
    p.add_argument('--out',default='e002_676_fixture.csv')
    a=p.parse_args()
    rows=[]
    for gap_ms in (20,30,40,50):
      for speed in (20,30,40):
       for clock_ms in (0,1,3):
        gap=F(gap_ms,1000); v=F(speed); e=F(clock_ms,1000)
        certified = v*(gap+2*e) < F(14,10)
        midpoint=aperture(gap/2,gap,v)
        hidden=midpoint<=F(3,10)
        assert not (certified and hidden)
        rows.append((gap_ms,speed,clock_ms,str(midpoint),int(certified),int(hidden)))
    with open(a.out,'w',newline='') as f:
      w=csv.writer(f)
      w.writerow(('gap_ms','speed_aperture_per_s','clock_error_ms_each_end','min_aperture','gap_exclusion','hidden_closure_possible'))
      w.writerows(rows)
    print('cases',len(rows),'certified',sum(r[4] for r in rows),'hidden',sum(r[5] for r in rows))
    gap=F(40,1000)
    assert F(20)*gap < F(14,10) and aperture(gap/2,gap,F(40))<=F(3,10)
    print('wrong-speed falsifier: V_claim=20, V_true=40, gap_ms=40')
if __name__=='__main__':run()
