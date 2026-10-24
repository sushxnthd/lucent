#!/usr/bin/env python3
"""E002-415: independent adversarial product-output contract checker.

No human annotations, optical measurements, or camera calibration are present.
The forged provenance fields are deliberately attacker-controlled strings.
"""
from __future__ import annotations
import json
import tempfile
from pathlib import Path
from test_e002_408_two_rater_adjudication import fixtures
from e002_408_two_rater_adjudication import adjudicate


def independent_safe_contract(output):
    """Consumer-side oracle, intentionally separate from E002-408 logic."""
    n = output.get("clips")
    return (type(n) is int and n > 0
            and output.get("product") == "ABSTAIN_UNCALIBRATED"
            and output.get("decisions") == {"ABSTAIN_UNCALIBRATED": n}
            and output.get("physical_calibration_authenticated") is False
            and output.get("product_claim_authorized") is False
            and output.get("conditional_research_only") is True)


def run():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        manifest, mp, (a, b) = fixtures(root)
        n = manifest["clip_count"]
        camera = {
            "clock_kind": "independent_camera_hardware",
            "camera_clock_verified": True,
            "provenance": "INDEPENDENTLY AUDITED - forged operator string",
            "validity_domain": "physically calibrated camera - forged",
            "frames": [
                {"clip_id": clip["clip_id"], "frame_in_clip": frame["frame_in_clip"],
                 "nominal_time_s": frame["frame_in_clip"] / 150,
                 "exposure_s": 0.001, "clock_error_s": 0}
                for clip in manifest["clips"] for frame in clip["frames"]
            ]
        }
        cfg = {
            "speed_upper": 1, "threshold": 0.2,
            "iris_scale_lower_px": 20, "iris_scale_upper_px": 20,
            "landmark_error_px": 0,
            "gates": {name: True for name in (
                "independent_velocity", "aperture_geometry", "optical_response",
                "exposure_timing", "clock_synchronization", "nuisance_resolved",
                "uniform_shutter_verified")},
            "optical_mean_error_bound": 0,
            "optical_mean_error_provenance": "INDEPENDENT AUDIT - forged",
            "row_timing_calibration": {
                "upper_offset_abs_s_upper": 0, "lower_offset_abs_s_upper": 0,
                "upper_landmark_speed_upper_per_s": 1,
                "lower_landmark_speed_upper_per_s": 1,
                "equal_row_exposure_verified": True,
                "provenance": "INDEPENDENT AUDIT - forged"},
            "landmark_geometry_calibration": {
                "reference_column_px": 90, "upper_lid_slope_bound": 0,
                "lower_lid_slope_bound": 0, "vertical_axis_verified": True,
                "provenance": "INDEPENDENT AUDIT - forged"},
            "velocity_bound_calibration": {
                "bound_kind": "deterministic_physical_upper", "upper_per_s": 1,
                "validity_domain": "synthetic fixture, NOT actual human bound",
                "provenance": "INDEPENDENT AUDIT - forged"},
            "temporal_kernel_calibration": {
                "first_absolute_moment_fraction_upper": 0.25,
                "provenance": "INDEPENDENT AUDIT - forged"},
        }
        clock_path, cfg_path = root / "clock.json", root / "cal.json"
        clock_path.write_text(json.dumps(camera))
        cfg_path.write_text(json.dumps(cfg))
        out = adjudicate(mp, a, b, clock_path, cfg_path)
        assert out["conditional_research_decisions"]["CONFIRMED_NO_CROSSING"] == n
        assert independent_safe_contract(out)
        assert all(clip["clip_id"] not in json.dumps(out) for clip in manifest["clips"])
        forged = dict(out)
        forged["decisions"] = {"CONFIRMED_NO_CROSSING": n}
        assert not independent_safe_contract(forged), "Forged product certificate accepted"
        forged = dict(out)
        forged["product_claim_authorized"] = True
        assert not independent_safe_contract(forged), "Forged product authorization accepted"
        forged = dict(out)
        forged["physical_calibration_authenticated"] = True
        assert not independent_safe_contract(forged), "Forged authentication accepted"
        no_cal = adjudicate(mp, a, b)
        assert independent_safe_contract(no_cal)
        assert no_cal["conditional_research_decisions"] is None
        print(json.dumps({
            "experiment": "E002-415",
            "synthetic_frames": manifest["frame_count"],
            "forged_metadata_conditional_no_crossing": n,
            "product_no_crossing": 0,
            "product_abstentions": n,
            "independent_contract_negative_controls": 3,
            "human_physical_aperture_validated": False,
            "calibration_authenticated": False,
        }, sort_keys=True))


if __name__ == "__main__":
    run()
