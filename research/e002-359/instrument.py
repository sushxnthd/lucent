"""E002-359 exact reduced instrument equations; numpy optional for pixel templates."""
import math
def cap(r,h):
 if h<=-r:return math.pi*r*r
 if h>=r:return 0.
 return r*r*math.acos(h/r)-h*math.sqrt(r*r-h*h)
def visible_annulus(r0,r1,h):
 assert 0<r0<r1
 return max(0,cap(r1,h)-cap(r0,h))
def worst_phase_norm(F,w,D):
 assert 0<w<=F and 0<D<=F
 return max(0,D-(F-w))/(math.sqrt(2)*w)
def separation(F,w,D,c,spatial_norm):
 return abs(c)*spatial_norm*worst_phase_norm(F,w,D)
def certified(F,w,D,c,spatial_norm,epsilon):
 return separation(F,w,D,c,spatial_norm)>2*epsilon
def critical_duration(F,w,c,spatial_norm,epsilon):
 if abs(c)*spatial_norm==0:return math.inf
 return F-w+2*math.sqrt(2)*epsilon*w/(abs(c)*spatial_norm)
if __name__=="__main__":
 F=1000/30;w=10;D=30;c=.3;eps=.1
 for h in [-6,0,2,4,5]:
  A=visible_annulus(5,5.5,h)
  print(h,A,critical_duration(F,w,c,math.sqrt(A),eps))
