import json
from pathlib import Path


def load_protocol():
    path = Path(__file__).resolve().parents[1] / "instrument" / "protocol.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_active_conditions_have_equal_exposure():
    protocol = load_protocol()
    conditions = protocol["conditions"]

    assert len(conditions["contiguous"]["high_segments"]) == 3
    assert len(conditions["split"]["high_segments"]) == 3
    assert (
        len(conditions["contiguous"]["high_segments"])
        == len(conditions["split"]["high_segments"])
    )


def test_protocol_matches_committed_sim001_design():
    protocol = load_protocol()
    assert protocol["conditions"]["contiguous"]["high_segments"] == [4, 5, 6]
    assert protocol["conditions"]["split"]["high_segments"] == [1, 2, 8]


def test_protocol_has_no_rapid_flashing():
    protocol = load_protocol()
    assert protocol["segment_seconds"] >= 0.5
    assert protocol["safety"]["rapid_flashing"] is False


def test_segments_are_in_range():
    protocol = load_protocol()
    n = round(protocol["total_seconds"] / protocol["segment_seconds"])
    for condition in ("contiguous", "split"):
        for segment in protocol["conditions"][condition]["high_segments"]:
            assert 0 <= segment < n
