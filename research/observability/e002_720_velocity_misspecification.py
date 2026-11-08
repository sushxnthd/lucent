"""E002-720: exact rational adversarial velocity-bound sensitivity; synthetic only."""
from fractions import Fraction as F

def certificate(a0,a1,v,dt):
    return v*dt < a0+a1

def oracle_closure(a0,a1,v_true,dt):
    return v_true*dt >= a0+a1

def run():
    grid=[F(i,4) for i in range(1,9)]
    total=correct=wrong=wrong_false=correct_false=0
    witnesses=[]
    for a0 in grid:
      for a1 in grid:
       for dt in grid:
        for vtrue in grid:
         closure=oracle_closure(a0,a1,vtrue,dt)
         claimed=vtrue/2
         c_ok=certificate(a0,a1,vtrue,dt)
         c_bad=certificate(a0,a1,claimed,dt)
         total+=1;correct+=c_ok;wrong+=c_bad
         correct_false+=int(c_ok and closure)
         wrong_false+=int(c_bad and closure)
         if c_bad and closure and len(witnesses)<5:
          witnesses.append((str(a0),str(a1),str(dt),str(vtrue),str(claimed)))
    assert total==4096 and correct_false==0 and wrong_false>0
    assert not certificate(F(1),F(1),F(2),F(1))
    print(dict(total=total,valid_certificates=correct,valid_false_exclusions=correct_false,
               underestimated_certificates=wrong,underestimated_false_exclusions=wrong_false,
               examples=witnesses))
if __name__=='__main__':run()
