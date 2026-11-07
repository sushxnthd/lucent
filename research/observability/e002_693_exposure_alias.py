from fractions import Fraction as F
from itertools import product

def aperture(t, center, depth, halfwidth):
    return F(1)-depth*max(F(0), F(1)-abs(t-center)/halfwidth)

def exposure_mean(center,depth,halfwidth,start,end):
    # Exact integration of a piecewise-linear physical aperture.
    knots=sorted(set([start,end]+[q for q in (center-halfwidth,center,center+halfwidth) if start<q<end]))
    return sum((aperture(x,center,depth,halfwidth)+aperture(y,center,depth,halfwidth))*(y-x)/2 for x,y in zip(knots,knots[1:]))/(end-start)

def run():
    total=hidden=naive=0
    examples=[]
    for gap,width,depth in product((F(1,2),F(1),F(2)),(F(1,8),F(1,4),F(1,2)),(F(3,4),F(1))):
        center=gap/2
        left=exposure_mean(center,depth,width,F(-1),F(0))
        right=exposure_mean(center,depth,width,gap,gap+1)
        true_min=aperture(center,center,depth,width)
        total+=1
        if true_min<=F(1,4):
            hidden+=1
            # INVALID estimator deliberately tested: exposure averages are not instantaneous endpoint apertures.
            if min(left,right)>F(1,4):
                naive+=1
                examples.append((str(gap),str(width),str(depth),str(left),str(right),str(true_min)))
    assert total==18 and hidden==18 and naive==18
    print({'cases':total,'hidden_closures':hidden,'false_no_closure_from_exposure_means':naive,'example':examples[0]})

if __name__=='__main__':run()
