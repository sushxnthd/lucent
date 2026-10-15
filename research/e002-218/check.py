#!/usr/bin/env python3
import json, pathlib, re, sys

def validate(obj):
    assert obj["run"] == "E002-218"
    assert obj["human_waveform_evaluated"] is False
    assert obj["frozen_gates_changed"] is False
    assert obj["native_paired_reference_certified"] is False
    archive = obj["archive"]
    listing = obj["listing"]
    assert archive["native_paired_reference_certified"] is False
    assert listing["status"] in ("blocked", "partial", "complete")
    assert listing["complete"] == (listing["status"] == "complete")
    assert len(listing["pages"]) <= 4
    for page in listing["pages"]:
        assert 0 <= page["count"] <= 200
        assert re.fullmatch("[0-9a-f]{64}", page["sha256"])
    if archive["status"] == "complete":
        assert archive["central_directory_complete"] is True
        assert archive["declared_entries"] == archive["entry_count"]
        assert archive["entry_count"] == sum(archive["extension_counts"].values())
        assert re.fullmatch("[0-9a-f]{64}", archive["central_directory_sha256"])
    else:
        assert archive["central_directory_complete"] is False

path = pathlib.Path(sys.argv[1] if len(sys.argv)>1 else "research/e002-218/PROVENANCE.json")
data = json.loads(path.read_text())
validate(data)
for key in ("native_paired_reference_certified", "human_waveform_evaluated"):
    modified = dict(data)
    modified[key] = True
    try:
        validate(modified)
    except AssertionError:
        continue
    raise AssertionError("unsupported scientific admission")
print("Independent E002-218 gate: PASS")
