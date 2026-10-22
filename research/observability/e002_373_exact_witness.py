from fractions import Fraction as Q
from math import sqrt

# Time ms; acceleration aperture/ms^2. Exact C1 trajectory.
segments=[
 (Q(15,2),Q(0)),(Q(5,2),-Q(1,50)),
 (Q(5,2),-Q(1,50)),(Q(25,6),Q(0)),
 (Q(5),Q(1,50)),(Q(5),Q(1,50)),
 (Q(25,6),Q(0)),(Q(5,2),-Q(1,50)),
 (Q(5,2),-Q(1,50)),(Q(15,2),Q(0))]
def verify():
 t=Q(-10);a=Q(1);v=Q(0);out=[];values=[];velocities=[]
 for dt,u in segments:
  area=a*dt+v*dt*dt/2+u*dt**3/6
  out.append((t,t+dt,a,v,u,area))
  pts=[Q(0),dt]
  if u:
   z=-v/u
   if 0<z<dt:pts.append(z)
  values += [a+v*z+u*z*z/2 for z in pts]
  velocities += [v,v+u*dt]
  assert abs(u)<=Q(1,50)
  a=a+v*dt+u*dt*dt/2;v=v+u*dt;t+=dt
 assert (t,a,v)==(Q(100,3),Q(1),Q(0))
 assert min(values)==Q(1,12) and max(values)==1
 assert max(map(abs,velocities))==Q(1,10)
 left=sum(row[5] for row in out[:2])/10
 right=sum(row[5] for row in out[-2:])/10
 assert left==right==Q(191,192)
 assert out[4][1]==Q(35,3)
 # The constant comparator a(t)=191/192 gives identical shutter means.
 closure_duration_ms=2*sqrt(35/3)
 # Frozen unseen synthetic 40fps prediction:
 bound=1-sqrt(2*.1*10*.001)-.1*15/2
 assert bound>.2
 print('PASS',left,'minimum',min(values),'closed_ms',closure_duration_ms,'40fps_bound',bound)
if __name__=='__main__':verify()
