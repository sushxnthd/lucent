# Synthetic aperture/shutter phase sweep. No human data.
T0=.150; T1=.190; T2=.248; T3=.3105; w=.010
knots=[(0.,1.),(T0,1.),(T1,0.),(T2,0.),(T3,1.),(2.,1.)]
def a(t):
 for (x,v),(y,z) in zip(knots[:-1],knots[1:]):
  if x<=t<=y:return v+(z-v)*(t-x)/(y-x)
 return 1.
def mean(t):
 pts=[t]+[x for x,v in knots if t<x<t+w]+[t+w]
 return sum((y-x)*(a(x)+a(y))/2 for x,y in zip(pts[:-1],pts[1:]))/w
def run(fps,decimate=1,n=2000):
 F=decimate/fps;full=0;anyhit=0;worst=w
 for i in range(n):
  p=F*i/n
  times=[p+k*F for k in range(int(1/F)+2)]
  overlap=[max(0.,min(t+w,T2)-max(t,T1)) for t in times]
  m=max(overlap)
  full+=m>=w-1e-10;anyhit+=m>1e-10;worst=min(worst,m)
 return full/n,anyhit/n,round(worst*1000,5)
if __name__=='__main__':
 for f,d in [(10,1),(20,1),(25,1),(30,1),(60,1),(30,3)]:
  print(f,d,run(f,d))
