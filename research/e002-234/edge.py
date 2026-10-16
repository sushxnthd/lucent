import cv2,numpy as np
R=np.linspace(.20,.78,30)
A=np.arange(48)*2*np.pi/48
def profile(g,x,y,scale,angles=A):
 out=[]
 for r in R:
  samples=[]
  for dr in (-.07,.07):
   xx=(x+(r+dr)*scale*np.cos(angles)).astype('float32').reshape(1,-1)
   yy=(y+(r+dr)*scale*np.sin(angles)).astype('float32').reshape(1,-1)
   samples.append(cv2.remap(g,xx,yy,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT_101)[0])
  out.append(float(np.median(samples[1]-samples[0])))
 return np.array(out)
def fit(g,x,y,s,a=A):
 v=profile(g,x,y,s,a);i=int(np.argmax(v));p=float(v[i])
 return float(R[i]),p,p/(float(np.median(np.abs(v)))+1e-6)
def evaluate(gray,points):
 h,w=gray.shape;x,y=points[0];s=float(np.median(np.linalg.norm(points[1:]-points[0],axis=1)))
 d={'iris_diameter_px':round(2*s,5),'center_x':round(float(x),4),'center_y':round(float(y),4)}
 if not np.isfinite(s) or s<4 or x<s or y<s or x>w-s or y>h-s:
  return {**d,'eligible':0,'reason':'geometry'}
 g=gray.astype('float32');r,p,m=fit(g,x,y,s)
 a=abs(fit(g,x,y,s,A[:24])[0]-fit(g,x,y,s,A[24:])[0])
 gamma=max(abs(fit(255*np.power(g/255.,v),x,y,s)[0]-r) for v in (.75,1.25))
 placebo=max(max(0.,fit(g,x+dx*s,y+dy*s,s)[1]) for dx,dy in ((.65,0),(-.65,0),(0,.65),(0,-.65)))/(max(0.,p)+1e-6)
 ok=(s>=6 and p>0 and m>=1.5 and a<=.12 and gamma<=.05 and placebo<.8)
 return {**d,'eligible':int(ok),'reason':'pass' if ok else 'edge_gate',
 'radius_ratio':round(r,6),'peak':round(p,6),'edge_margin':round(m,6),
 'split_disagreement':round(a,6),'gamma_disagreement':round(gamma,6),
 'placebo_ratio':round(placebo,6)}
