"""E002-479: adversarial sub-grid shutter island with real E002-477 intake.

SYNTHETIC ONLY. An intake PASS never authorizes physical shutter or human claims.
The original freeze was amended before implementation; see E002_479_AMENDMENT_A.md.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import tempfile
from pathlib import Path

from e002_477_optical_intake import evaluate

T = 1000.0 / 240.0
STEP = 0.05
WIDTH = 0.006
U = 0.004
ISLAND = (2.015, 2.025)
BASE = (0.4, 1.4)
AMPLITUDE = 0.20
ROWS = ("top", "bottom")
REPEATS = 20
PHASE_COUNT = math.ceil(T * 2 / STEP - 1e-10) + 1
BLOCKED = "ABSTAIN_UNCALIBRATED"


def overlap(a: float, b: float, c: float, d: float) -> float:
    return max(0.0, min(b, d) - max(a, c))


def pulse_contrast(start: float, amplitude: float = 0.0) -> float:
    """Normalized integral of stationary periodic optical sensitivity."""
    end = start + WIDTH
    area = 0.0
    for k in range(-1, 4):
        area += overlap(start, end, k * T + BASE[0], k * T + BASE[1])
        area += amplitude * overlap(start, end, k * T + ISLAND[0], k * T + ISLAND[1])
    return area / WIDTH


def robust_island_unseen() -> bool:
    """Check full possible pulse support, not just nominal pulse starts."""
    for phase in range(PHASE_COUNT):
        t = phase * STEP
        for k in range(-1, 4):
            if overlap(t - U, t + WIDTH + U, k * T + ISLAND[0], k * T + ISLAND[1]) > 1e-12:
                return False
    return True


def write_fixture(root: Path, amplitude: float) -> tuple[Path, Path, Path, Path]:
    """Write synthetic CSVs. Amplitude is hidden ground truth, not metadata."""
    root.mkdir(parents=True, exist_ok=True)
    camera = root / "camera.csv"
    clock = root / "clock.csv"
    raw = root / "raw_video_bundle"
    raw.write_bytes(b"SYNTHETIC optical acquisition placeholder; not real frames.\n")
    with camera.open("w", newline="", encoding="utf-8") as c, clock.open("w", newline="", encoding="utf-8") as d:
        cw = csv.writer(c, lineterminator="\n")
        dw = csv.writer(d, lineterminator="\n")
        cw.writerow(("row_stratum", "phase_index", "repeat_index", "response", "dark_reference", "gain", "saturated", "dropped"))
        dw.writerow(("row_stratum", "phase_index", "repeat_index", "pulse_start_ms", "pulse_end_ms"))
        for row in ROWS:
            for phase in range(PHASE_COUNT):
                start = phase * STEP
                contrast = pulse_contrast(start, amplitude)
                for rep in range(REPEATS):
                    cw.writerow((row, phase, rep, f"{contrast:.9f}", "0", "1", "0", "0"))
                    dw.writerow((row, phase, rep, f"{start:.9f}", f"{start + WIDTH:.9f}"))
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    manifest = {
        "schema": "lucent-e002-477-optical-intake-v1",
        "frame_period_ms": T,
        "phase_step_ms": STEP,
        "scan_periods": 2,
        "repeats_per_phase": REPEATS,
        "row_strata": list(ROWS),
        "pulse_width_ms": WIDTH,
        "pulse_width_tolerance_ms": 0.00001,
        "clock_error_bound_ms": U,
        "expected_gain": 1,
        "camera_gain_locked": True,
        "clock_source_type": "independent_photodiode_logic_analyzer",
        "camera_device_id": "SYNTHETIC-CAMERA",
        "clock_device_id": "SYNTHETIC-CLOCK",
        "camera_csv_sha256": sha(camera),
        "clock_csv_sha256": sha(clock),
        "raw_video_sha256": sha(raw),
    }
    manifest_path = root / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return manifest_path, camera, clock, raw


def heldout_readings(amplitude: float) -> list[float]:
    """Two authenticated periods, 20 deterministic repeats each, two rows.

    Frozen jitter and additive contrast errors are constructed instrument noise,
    not empirically measured physical tolerances.
    """
    values = []
    for row in ROWS:
        for period in range(2):
            for rep in range(REPEATS):
                jitter = (-2, -1, 0, 1, 2)[rep % 5] * 0.001
                noise = (-2, -1, 0, 1, 2)[(rep + period + (row == "bottom")) % 5] * 0.001
                start = period * T + 2.017 + jitter
                values.append(pulse_contrast(start, amplitude) + noise)
    return values


def detect(readings: list[float], threshold: float = 0.04) -> bool:
    """Detection, never proof of absent optical sensitivity."""
    return min(readings) > threshold


def run_experiment() -> dict:
    with tempfile.TemporaryDirectory(prefix="lucent-e002-479-") as tmp:
        a = write_fixture(Path(tmp) / "no_island", 0.0)
        b = write_fixture(Path(tmp) / "island", AMPLITUDE)
        qa_a = evaluate(*a)
        qa_b = evaluate(*b)
        hashes_match = all(x.read_bytes() == y.read_bytes() for x, y in zip(a, b))
        hi = heldout_readings(AMPLITUDE)
        null = heldout_readings(0.0)
        low = heldout_readings(0.004)
        return {
            "experiment": "E002-479",
            "evidence_tier": "SYNTHETIC_INSTRUMENT_MODEL_ONLY",
            "phase_count": PHASE_COUNT,
            "paired_rows": PHASE_COUNT * REPEATS * len(ROWS),
            "two_period_grid_observations": PHASE_COUNT * REPEATS * len(ROWS),
            "nominal_phase_step_ms": STEP,
            "pulse_width_ms": WIDTH,
            "phase_error_bound_ms": U,
            "guaranteed_single_cell_unprobed_width_ms": round(STEP - WIDTH - 2 * U, 9),
            "two_period_robust_island_unseen": robust_island_unseen(),
            "all_source_files_identical": hashes_match,
            "null_intake": qa_a["qa_status"],
            "island_intake": qa_b["qa_status"],
            "intake_output_identical": qa_a == qa_b,
            "heldout_observations_per_model": len(hi),
            "heldout_null_detected": detect(null),
            "heldout_high_island_detected": detect(hi),
            "heldout_low_island_detected": detect(low),
            "heldout_high_min_contrast": round(min(hi), 6),
            "heldout_null_max_contrast": round(max(null), 6),
            "physical_acquisitions": 0,
            "new_human_reference_sequences": 0,
            "product_claim": BLOCKED,
        }


def main() -> None:
    print(json.dumps(run_experiment(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
