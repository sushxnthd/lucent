from fractions import Fraction
import json
from pathlib import Path
n=90
res=json.loads(Path(__file__).with_name('RESULTS.json').read_text())
h=[Fraction(j*(n-j),n*n) for j in range(n)]+[Fraction(-j*(n-j),n*n) for j in range(n)]+[Fraction(0)]*n
assert any(h)
for row in range(n): assert h[row]+h[row+n]+h[row+2*n]==0
sq=sum((Fraction(1)-Fraction(2*j,n))**2 for j in range(n))/n
assert str(sq)==res['mean_squared_error_units_squared']
assert res['operator_rank']==n and res['operator_nullity']==2*n
assert res['max_absolute_label_error_units']=='1'
assert res['tight_worst_case_error_coefficient_seconds']=='1'
assert res['human_waveform_tested'] is False and res['released_dataset_bytes_tested'] is False
print('PASS: independent exact checker')
