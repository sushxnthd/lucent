"""E002-655 synthetic exposure-integration counterexample (not human data)."""
import json

def aperture(t):
    return 1.0 - 0.8 * max(0.0, 1.0 - abs(t - 0.5) / 0.12)

def exposure_average(center, duration, samples=20000):
    if duration == 0:
        return aperture(center)
    return sum(aperture(center-duration/2+(i+0.5)*duration/samples)
               for i in range(samples))/samples

def run():
    V = 0.8 / 0.12
    cases = []
    for duration in (0, 0.02, 0.05, 0.1, 0.2, 0.4):
        y0, y1 = (exposure_average(t, duration) for t in (0.3, 0.7))
        naive_margin = min(y0, y1) - V * 0.4 / 2 - 0.3
        safe_margin = naive_margin - V * duration / 4
        cases.append(dict(duration=duration, observed=[y0, y1],
                          naive_margin=naive_margin, safe_margin=safe_margin))
        assert safe_margin <= naive_margin + 1e-12
    broad = exposure_average(0.5, 0.4)
    assert broad > 0.3 and aperture(0.5) < 0.3
    assert abs(broad - 0.76) < 1e-5
    return dict(evidence='synthetic_only', speed_ceiling=V, threshold=0.3,
                center_aperture=aperture(0.5), integrated_aperture=broad,
                false_open_if_threshold_integrated=True, cases=cases)

if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
