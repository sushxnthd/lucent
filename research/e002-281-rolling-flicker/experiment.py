import math

def sinc(x):
    return math.sin(x)/x if x else 1.0

def H(f,T,d,a):
    b=abs(a*sinc(math.pi*f*T))
    g=math.pi*f*d
    return 2*math.atanh(b*abs(math.sin(g))/math.sqrt(1-b*b*math.cos(g)**2))

if __name__=='__main__':
    print(H(100,1/120,.005,.6))
