"""Frozen synthetic tests. Human RGB/reference: NOT RUN."""
import json
import numpy as np
from model import (circle_conic,project_conic,random_homography,
                   conic_radius_ratio,true_ratio_interval,certify_increase,
                   full_image_world)
rng=np.random.default_rng(318)
out={"experiment":"E002-318","model_only":True,"human_reference":"NOT RUN"}

errs=[]
for _ in range(1000):
    q=rng.uniform(.25,.82)
    H=random_homography(rng)
    Cp=project_conic(circle_conic(q),H)*rng.uniform(.1,8)
    Ci=project_conic(circle_conic(1),H)*rng.uniform(.1,8)
    errs.append(abs(conic_radius_ratio(Cp,Ci)-q))
out["geometry_only"]={"n":len(errs),"max_abs_error":max(errs),
                      "passed":max(errs)<1e-10}
assert out["geometry_only"]["passed"]

H=random_homography(rng)
base=full_image_world(.53,1,H)
gains=[.1,.5,1.,1.5]
bias=.035
err=max(float(np.max(abs(((base*g+bias)-bias)/g-base))) for g in gains)
clipped=np.clip(base*1.5+bias,0,1)
clipped_err=float(np.max(abs((clipped-bias)/1.5-base)))
out["brightness_only"]={"gains":gains,"calibrated_max_error":err,
                        "clipped_uncorrectable_error":clipped_err,
                        "passed":err<1e-12 and clipped_err>0}
assert out["brightness_only"]["passed"]

H0,H1=random_homography(rng),random_homography(rng)
rho=.94
qa1,qb1=.53/rho,.53*rho
ma1,mb1=rho,1/rho
a=[full_image_world(.5,1,H0),full_image_world(qa1,ma1,H1)]
b=[full_image_world(.5,1,H0),full_image_world(qb1,mb1,H1)]
pixel_error=max(float(np.max(abs(x-y))) for x,y in zip(a,b))
out["full_rgb_opposite_trend_collision"]={
  "calibrated_rho":rho,
  "q_true_world_A":[.5,qa1],"q_true_world_B":[.5,qb1],
  "m_world_A":[1,ma1],"m_world_B":[1,mb1],
  "max_rgb_pixel_error":pixel_error,
  "bitwise_identical":all(np.array_equal(x,y) for x,y in zip(a,b))}
assert out["full_rgb_opposite_trend_collision"]["bitwise_identical"]
assert qa1>.5>qb1

out["frozen_prediction"]={
 "critical_rho":.5/.53,
 "rho_094":{"interval":true_ratio_interval(.5,.53,.94),
            "certify":certify_increase(.5,.53,.94)},
 "rho_095":{"interval":true_ratio_interval(.5,.53,.95),
            "certify":certify_increase(.5,.53,.95)}}
assert not out["frozen_prediction"]["rho_094"]["certify"]
assert out["frozen_prediction"]["rho_095"]["certify"]

identity=np.eye(3)
small=full_image_world(.45,1,identity)
large=full_image_world(.65,1,identity)
c=np.linspace(-2,2,128)
x,y=np.meshgrid(c,c)
mask=x*x+y*y>.68**2
out["missingness_only"]={
 "hidden_pixel_fraction":float((~mask).mean()),
 "distinct_true_ratios":[.45,.65],
 "visible_rgb_max_error":float(np.max(abs(small[mask]-large[mask]))),
 "visible_images_identical":bool(np.array_equal(small[mask],large[mask]))}
assert out["missingness_only"]["visible_images_identical"]

t10=np.arange(0,2,.1)
t30=np.arange(0,2,1/30)
pulse=lambda t:.5+.04*np.sin(np.pi*t/.1)**2
out["temporal_smoothness"]={
 "loader_rate_hz":10,"native_rate_hz":30,
 "loader_max_deviation_from_constant":float(np.max(abs(pulse(t10)-.5))),
 "native_max_deviation_from_constant":float(np.max(abs(pulse(t30)-.5))),
 "qualification":"Instantaneous samples only; shutter integration not modeled"}
assert out["temporal_smoothness"]["loader_max_deviation_from_constant"]<1e-12
assert out["temporal_smoothness"]["native_max_deviation_from_constant"]>.02

with open("results.json","w") as f:json.dump(out,f,indent=2)
print(json.dumps(out,indent=2))
