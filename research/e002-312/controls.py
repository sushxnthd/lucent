"""Four synthetic nuisance controls for full-image temporal ambiguity."""
import json
import numpy as np
from scipy.integrate import quad
from scipy.special import ndtr
from model import weight,edge,identified_interval

T=1/60;D=4.;sigma=.8
def image(x,v,shift=0,gain=1):
    a=quad(lambda z:gain*weight(z,v)*ndtr((x-shift-edge(z,v,D))/sigma),0,1)[0]
    b=quad(lambda z:gain*weight(z,v),0,1)[0]
    return a/b
xs=np.linspace(-2,6,51)
geo=max(abs(image(float(x),"early")-image(float(x+1.1),"early",shift=1.1)) for x in xs)
bright=max(abs(image(float(x),"early")-image(float(x),"early",gain=7.3)) for x in xs)
lo,hi=identified_interval(.5,1e-10,T)
smooth=max(abs(image(float(x),"early")-image(float(x),"late")) for x in xs)
assert geo<1e-12 and bright<1e-12 and (hi-lo)/T>.999999999 and smooth<1e-12
print(json.dumps({"geometry_error":geo,"brightness_error":bright,"missingness_fraction":(hi-lo)/T,"smoothness_collision_error":smooth,"passed":True},indent=2))
