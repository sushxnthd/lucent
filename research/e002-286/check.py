import random
r=random.Random(20261018)
for f in (10,24,30,60):
 P=1000/f
 for _ in range(10000):
  d=r.random()*2*P;s=r.random()*1e6
  p=sum(((-(s-i*P/128)%P)%P)<d for i in range(128))/128
  assert abs(p-min(1,d/P))<=1/128+1e-9
print('40000 checks passed: phase arithmetic only')
