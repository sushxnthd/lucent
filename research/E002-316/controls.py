"""Four synthetic nuisance controls, separate from primary checker."""
import numpy as np
from model import observed_profile,moments,anatomical_ratio_interval
def main():
    rng=np.random.default_rng(3316)
    k1=rng.dirichlet(np.ones(13));k2=rng.dirichlet(np.ones(9))
    assert abs(moments(observed_profile(12,.4,k1))[0]/60-moments(observed_profile(18,.4,k2))[0]/90)<1e-12 # geometry
    a=moments(observed_profile(15,.4,k1))[0]
    b=moments(observed_profile(15,.44,k1))[0]
    lo,hi=anatomical_ratio_interval(a,60,b,60,.9)
    assert lo<1<hi # brightness
    y=observed_profile(15,.4,np.ones(9)/9)
    assert moments(y[3:-3])[0]<moments(y)[0] # missingness
    assert np.allclose(observed_profile(3,.5,np.ones(5)/5),observed_profile(5,.3,np.ones(3)/3),atol=1e-15,rtol=0) # static worlds, temporal smoothness
    print("geometry, brightness, missingness, temporal smoothness: PASS")
if __name__=="__main__":main()
