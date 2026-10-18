"""Independent no-numpy analytic check for E002-276."""
import json,math,pathlib
d=json.loads(pathlib.Path(__file__).with_name('RESULTS.json').read_text())
n=60;sig=.5
for row in d['rows']:
 a=row['alpha']
 c=[math.cos(-a+2*a*i/(n-1)) for i in range(n)]
 sd=sig/math.sqrt(n-sum(c)**2/sum(z*z for z in c))
 p=math.erf(1/(math.sqrt(2)*sd))
 assert abs(sd-row['sd_px'])<1e-7
 assert abs(p-row['p_pred'])<1e-9
 assert abs(p-row['p_observed'])<5*math.sqrt(p*(1-p)/4000)+.002
assert d['exact_gauge']['r1']+d['exact_gauge']['b1']==d['exact_gauge']['r2']+d['exact_gauge']['b2']
assert abs(d['transition']['total_arc_degrees']-77.8276020742)<1e-5
print('PASS: 11 analytic checks, synthetic holdout calibration, gauge counterexample')
