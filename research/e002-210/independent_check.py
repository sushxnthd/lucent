#!/usr/bin/env python3
"""Independent brute-force integer clock-offset and complex-plane phase checker."""
import json, math
from pathlib import Path

def check(results):
    assert results["kind"] == "EXACT_THEOREM_AND_SYNTHETIC_CONTROLS"
    assert results["human_RGB_tracker_pairs"] == 0
    for case in results["cases"]:
        lag,e,c = case["apparent_ms"],case["offset_bound_ms"],case["certificate"]
        if e is None:
            assert not c["admit"] and c["interval_ms"] is None
            continue
        possibilities = [lag-d for d in range(-int(e),int(e)+1)]
        assert c["interval_ms"] == [min(possibilities),max(possibilities)]
        assert c["admit"] == all(-100 <= t <= 100 for t in possibilities)
        assert abs(c["worst_ms"]-max(map(abs,possibilities))) < 1e-10
    for row in results["frequency_table"]:
        f,e = row["frequency_hz"],row["clock_bound_ms"]
        chord = [abs(complex(math.cos(2*math.pi*f*d/1000),math.sin(2*math.pi*f*d/1000))-1)
                 for d in [-e+2*e*i/2000 for i in range(2001)]]
        assert abs(max(chord)-row["max_error_in_signal_amplitudes"]) < 1e-8
    assert results["EVE_admission"]["webcam_lag_certificate"] == "REJECT_UNTIL_BOUND_ESTABLISHED"

if __name__=="__main__":
    import timebase_certificate as model
    results = model.run()
    check(results)
    stored = json.loads(Path(__file__).with_name("RESULTS.json").read_text())
    check(stored)
    assert stored["cases"] == results["cases"]
    assert all(abs(a["max_error_in_signal_amplitudes"]-b["max_error_in_signal_amplitudes"]) < 1e-12 for a,b in zip(stored["frequency_table"],results["frequency_table"]))
    corrupted = json.loads(json.dumps(stored))
    corrupted["cases"][1]["certificate"]["admit"] = True
    try:
        check(corrupted)
    except AssertionError:
        pass
    else:
        raise AssertionError("corrupted result accepted")
    print("PASS: brute-force lag, phase geometry, mutation rejection; human N=0")
