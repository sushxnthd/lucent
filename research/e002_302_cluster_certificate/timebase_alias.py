import math

def sinc(x):
    return 1 if x == 0 else math.sin(x)/x

fs=10.0
T=1/60
A=-sinc(math.pi*2*T)/sinc(math.pi*8*T)
low=[sinc(math.pi*2*T)*math.sin(2*math.pi*2*n/fs) for n in range(100)]
high=[A*sinc(math.pi*8*T)*math.sin(2*math.pi*8*n/fs) for n in range(100)]
assert max(abs(a-b) for a,b in zip(low,high)) < 1e-12
print('Exact exposure-integrated 2Hz/8Hz alias at 10fps verified')
