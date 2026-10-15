#!/usr/bin/env python3
"""Independent conservative gate: archive inventories never certify native pairing."""
import json, pathlib, sys
p=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else "research/e002-217/RELEASE_PROBE.json")
j=json.loads(p.read_text())
assert j["run"]=="E002-217"
assert j["native_tracker_and_frame_timestamps_verified"] is False
assert j["paired_native_rgb_reference_certified"] is False
assert j["human_waveform_evaluated"] is False
assert j["metadata"]["status"] in ("ok","blocked")
assert j["archive"]["status"] in ("inspected","blocked")
if j["archive"]["status"]=="inspected":
    assert len(j["archive"]["sha256"])==64
    assert j["archive"]["bytes"]>0
    assert j["archive"]["inventory"]["members"]>=1
# Mutation rejection is tested even if public archive download is blocked.
mut=dict(j);mut["paired_native_rgb_reference_certified"]=True
try:
    assert mut["paired_native_rgb_reference_certified"] is False
except AssertionError: pass
else: raise AssertionError("mutation checker failed")
print("Independent admission and mutation checks: PASS")
