#!/usr/bin/env python3
"""Algebra and tampering checks without external data."""
from audit import metric
import math
q={'n':101.,'bias_mm':.1,'gt_std_mm':.2,'pred_std_mm':.2,'pearson_r':.5,'mae_mm':.01}
a=metric(q)
expected=math.sqrt(.1**2+100/101*(.2**2+.2**2-2*.5*.2*.2))/.2
assert math.isclose(a[0],expected,abs_tol=1e-12)
assert math.isclose(a[1],math.sqrt(100/101),abs_tol=1e-12)
q['mae_mm']=5
try: metric(q)
except ValueError as e: assert 'MAE_EXCEEDS_RMSE' in str(e)
else: raise AssertionError('MUTATION_UNDETECTED')
print('SYNTHETIC_IDENTITY_AND_MUTATION_PASS')
