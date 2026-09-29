from pathlib import Path
import sys

import numpy as np

EXPERIMENTS_DIR = Path(__file__).resolve().parents[1] / "experiments"
sys.path.insert(0, str(EXPERIMENTS_DIR))

from martin_pvt_target_alignment import (  # noqa: E402
    parse_events,
    pupil_features,
)


def test_parse_martin_events(tmp_path: Path):
    text = """MSG 1000 TRIALID 0
START 1010 LEFT EVENTS
MSG 7010 -14 DISPLAY_target
MSG 7420 0 KEYBOARD_response
MSG 8000 !V TRIAL_VAR RT 410
MSG 8001 !V TRIAL_VAR blockn 1
MSG 8002 !V TRIAL_VAR trialn 1
MSG 9000 TRIALID 1
START 9010 LEFT EVENTS
MSG 15010 -14 DISPLAY_target
MSG 15520 0 KEYBOARD_response
MSG 16000 !V TRIAL_VAR RT 510
MSG 16001 !V TRIAL_VAR blockn 1
MSG 16002 !V TRIAL_VAR trialn 2
"""
    path = tmp_path / "sub001_events.asc"
    path.write_text(text, encoding="utf-8")

    trials = parse_events(path, "1")

    assert len(trials) == 2
    assert trials[0].subject == "1"
    assert trials[0].block == 1
    assert trials[0].trialn == 1
    assert trials[0].rt_ms == 410
    assert trials[0].foreperiod_s == 6.0
    assert trials[0].progress == 0.0

    assert trials[1].trialn == 2
    assert trials[1].progress == 1.0


def test_pupil_feature_map_is_scale_invariant():
    times = np.arange(0, 6000, 4, dtype=np.int64)
    pupil = 2000.0 + 120.0 * np.sin(times / 350.0)

    a = pupil_features(times, pupil, target_ms=6000, duration_s=5)
    b = pupil_features(times, pupil * 3.7, target_ms=6000, duration_s=5)

    assert a is not None
    assert b is not None
    assert len(a) == 11
    np.testing.assert_allclose(a, b, rtol=1e-10, atol=1e-10)
    assert a[-1] == 1.0


def test_pupil_feature_map_enforces_frozen_missingness_gate():
    times = np.arange(0, 6000, 4, dtype=np.int64)
    pupil = np.full(len(times), 2000.0)
    pupil[times >= 2500] = np.nan

    features = pupil_features(
        times,
        pupil,
        target_ms=6000,
        duration_s=5,
    )

    assert features is None
