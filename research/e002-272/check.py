#!/usr/bin/env python3
"""Independent fail-closed checks; a passing script does not imply scientific admission."""
import copy
import json
from pathlib import Path

def verify(r):
    assert r["run"] == "E002-272"
    assert r["human_waveform_evaluated"] is False
    assert r["rgb_reference_clock_certified"] is False
    assert r["original_source_bytes_verified"] is False
    inv = r["inventories"]
    assert set(inv).issubset({"videostream.zip", "pupil.zip"})
    for v in inv.values():
        assert v["archive_file_count"] == sum(v["extension_counts"].values())
        assert v["raw_rgb_candidate_count"] == sum(
            v["extension_counts"].get(e, 0) for e in
            (".mp4", ".webm", ".mov", ".avi", ".mkv", ".jpg", ".jpeg", ".png", ".bmp"))
        assert not v["archive_md5_verified"]
    if len(inv) < 2:
        expected = "ACCESS_BLOCKED"
    elif inv["videostream.zip"]["raw_rgb_candidate_count"] == 0:
        expected = "NOT_RGB_ELIGIBLE"
    elif inv["pupil.zip"]["json_count"] + inv["pupil.zip"]["tsv_count"] == 0:
        expected = "NO_PUPIL_REFERENCE"
    else:
        expected = "CANDIDATE_PENDING_PAIR_AND_CLOCK"
    assert r["status"] == expected
    return expected

if __name__ == "__main__":
    p = Path(__file__).with_name("RUN_RESULT.json")
    r = json.loads(p.read_text())
    print("PASS:", verify(r))
    bad = copy.deepcopy(r)
    bad["human_waveform_evaluated"] = True
    try:
        verify(bad)
    except AssertionError:
        print("PASS: human-claim mutation rejected")
    else:
        raise AssertionError("HUMAN_CLAIM_MUTATION_ESCAPED")
