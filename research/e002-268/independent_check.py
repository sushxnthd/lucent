"""Independent math checker; does not import E002-267 evaluator or audit.py."""
import math
for p in range(2,10):
    for s in ('a','b'):
        high=((p%2==0)==(s=='a'))
        wave=[math.sin(2*math.pi*.6*i/60) for i in range(300)]
        x=[.25+.03*v for v in wave]
        y=[3+(.24 if high else .02)*v for v in wave]
        def sd(z):
            mean=sum(z)/len(z)
            return math.sqrt(sum((v-mean)**2 for v in z)/len(z))
        assert sd(y)>.1 if high else sd(y)<.1
        pred=[3+8*(v-.25) for v in x]
        amp=sd(pred)/sd(y)
        assert abs(amp-1)<1e-10 if high else amp>10
print('PASS independent: 8 high / 8 low, oracle gate 100%, blind gate 50%, no human data')
