from parser import parse
from count import windows
from stats import summarize
def tag(ids):
    return "#start\n"+"\n".join(f"{i+1}:{v}:"+":".join(["X"]*17) for i,v in enumerate(ids))+"\n#end"
rows=parse(tag([-1,0,0,-1,1,-1,-1,-1,-1,-1]))
assert [w[2] for w in windows(rows,width=5)]==[2,0]
s=summarize([[2,0]],reps=100)
assert abs(s["conditional_expected_zero"]-0.25)<1e-12
assert abs(s["observed_zero"]-0.5)<1e-12
print("FIXTURE_PASS")
