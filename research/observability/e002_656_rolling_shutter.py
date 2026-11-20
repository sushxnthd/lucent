"""E002-656: deterministic rolling-shutter timing falsification; synthetic only."""
import json

def aperture(t):
    return 0.2 + 4.0 * abs(t - 0.5)

def mean(center, exposure):
    lo, hi, c = center-exposure/2, center+exposure/2, 0.5
    if hi <= c: distance = c-center
    elif lo >= c: distance = center-c
    else: distance = ((c-lo)**2+(hi-c)**2)/(2*exposure)
    return 0.2+4*distance

def run():
    V, threshold, e = 4., 0.3, 0.02
    nominal=(0.46,0.54)
    actual=(0.42,0.58)
    ys=[mean(t,e) for t in actual]
    naive=min(ys)-V*(nominal[1]-nominal[0])/2-threshold
    timing_error=max(abs(a-b) for a,b in zip(nominal,actual))
    corrected=naive-V*(timing_error+e/4)
    assert aperture(.5)<threshold and naive>0 and corrected<0
    return dict(evidence='deterministic_synthetic_only', threshold=threshold,
      true_minimum=aperture(.5), nominal_centers=nominal, actual_centers=actual,
      exposure=e, measured_averages=ys, naive_margin=naive,
      corrected_margin=corrected, naive_false_certificate=True,
      corrected_decision='ABSTAIN', timing_error=timing_error)

if __name__=='__main__': print(json.dumps(run(),indent=2))
