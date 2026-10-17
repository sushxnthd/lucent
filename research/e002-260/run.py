from fractions import Fraction as F
import json
from pathlib import Path
N=90
x=[F(i,90) for i in range(3*N)]
z=[sum((x[i+k*N] for k in range(3)),F(0))/3 for i in range(N)]
y=[x[3*i] for i in range(N)]
e=[z[i]-y[i] for i in range(N)]
a=[F(i*(N-i),N*N) for i in range(N)]
h=a+[-v for v in a]+[F(0)]*N
assert any(h) and all(sum((h[i+k*N] for k in range(3)),F(0))==0 for i in range(N))
assert max(map(abs,e))==1
ms=sum((v*v for v in e),F(0))/N
assert ms==F(N*N+2,3*N*N)
bound=[sum((abs(2*i-N*k) for k in range(3)))/F(3*N) for i in range(N)]
assert max(bound)==1
r={"run":"E002-260","data_type":"exact_synthetic","N":N,"raw_reference_samples":3*N,"folded_labels":N,"operator_rank":N,"operator_nullity":2*N,"kernel_nonzero":True,"kernel_folds_to_zero":True,"linear_drift_L_units_per_second":1,"max_absolute_label_error_units":str(max(map(abs,e))),"mean_squared_error_units_squared":str(ms),"rms_error_units":float(ms)**0.5,"tight_worst_case_error_coefficient_seconds":str(max(bound)),"human_waveform_tested":False,"released_dataset_bytes_tested":False,"source_paper_confirms_method":True,"product_certified":False}
Path(__file__).with_name('RESULTS.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
