"""APST5-SIM-005: camera-robust equal-exposure probe search.

Preregistration:
experiments/registrations/APST5_SIMULATION_005.md

This is a surrogate observability test, not human validation.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from pathlib import Path

import numpy as np

from lucent.active_probe import (
    ProbeConfig,
    sample_parameter_population,
    simulate_pupil,
)


DESIGN_SEED = 20261001
TEST_SEED = 271828
DESIGN_CAMERA_SEED = 424242
TEST_CAMERA_SEED = 314159

CONTIGUOUS = (4, 5, 6)
CURRENT_E002 = (1, 2, 8)
EVEN = (2, 5, 8)

GRID_DT = 0.05
INTERNAL_DT = 0.01
BASELINE_SECONDS = 0.4
THRESHOLD = 1.25


@dataclass(frozen=True)
class CameraScenario:
    name: str
    fps: float
    jitter_sd_s: float
    drop_probability: float
    noise_sd: float


SCENARIOS = (
    CameraScenario("high_quality", 60.0, 0.001, 0.00, 0.005),
    CameraScenario("ordinary", 30.0, 0.004, 0.02, 0.010),
    CameraScenario("stressed", 24.0, 0.008, 0.08, 0.020),
)


def build_probe(positions: tuple[int, ...], config: ProbeConfig) -> np.ndarray:
    probe = np.full(config.n_segments, config.low_level, dtype=float)
    probe[list(positions)] = config.high_level
    return probe


def candidate_positions():
    yield from combinations(range(1, 10), 3)


def highres_trace(
    positions: tuple[int, ...],
    theta: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    config = ProbeConfig(dt=INTERNAL_DT)
    probe = build_probe(positions, config)
    pupil = simulate_pupil(probe, theta, config)
    t = np.arange(config.n_steps, dtype=float) * INTERNAL_DT

    baseline = float(np.median(pupil[t < BASELINE_SECONDS]))
    if baseline <= 1e-9:
        raise RuntimeError("degenerate pupil baseline")

    fractional = (pupil - baseline) / baseline
    return t, fractional


def observe(
    time: np.ndarray,
    trace: np.ndarray,
    scenario: CameraScenario,
    rng: np.random.Generator,
    *,
    noisy: bool,
) -> np.ndarray | None:
    period = 1.0 / scenario.fps
    phase = float(rng.uniform(0.0, period))
    sample_t = np.arange(phase, time[-1] + 1e-9, period)

    if scenario.jitter_sd_s > 0:
        sample_t = sample_t + rng.normal(
            0.0,
            scenario.jitter_sd_s,
            size=len(sample_t),
        )

    sample_t = np.clip(sample_t, time[0], time[-1])
    sample_t.sort()

    values = np.interp(sample_t, time, trace)

    if noisy and scenario.noise_sd > 0:
        values = values + rng.normal(
            0.0,
            scenario.noise_sd,
            size=len(values),
        )

    if noisy and scenario.drop_probability > 0:
        keep = rng.random(len(values)) >= scenario.drop_probability
        sample_t = sample_t[keep]
        values = values[keep]

    if len(values) < 12:
        return None

    grid = np.arange(0.0, 5.0, GRID_DT)
    if sample_t[0] > 0.15 or sample_t[-1] < 4.80:
        return None

    reconstructed = np.interp(grid, sample_t, values)
    base = reconstructed[grid < BASELINE_SECONDS]
    reconstructed = reconstructed - float(np.median(base))
    return reconstructed


def rmse(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.sqrt(np.mean((a - b) ** 2)))


def separation_ratio(
    candidate_trace: tuple[np.ndarray, np.ndarray],
    control_trace: tuple[np.ndarray, np.ndarray],
    scenario: CameraScenario,
    rng: np.random.Generator,
) -> float | None:
    tc, yc = candidate_trace
    tt, yt = control_trace

    clean_c = observe(tc, yc, scenario, rng, noisy=False)
    clean_t = observe(tt, yt, scenario, rng, noisy=False)

    if clean_c is None or clean_t is None:
        return None

    between = rmse(clean_c, clean_t)

    within = []
    for time, trace in (candidate_trace, control_trace):
        a = observe(time, trace, scenario, rng, noisy=True)
        b = observe(time, trace, scenario, rng, noisy=True)
        if a is not None and b is not None:
            within.append(rmse(a, b))

    if not within:
        return None

    denom = float(np.median(within))
    if denom <= 1e-12:
        return None

    return between / denom


def evaluate_positions(
    positions: tuple[int, ...],
    population: np.ndarray,
    *,
    camera_seed: int,
) -> np.ndarray:
    rng = np.random.default_rng(camera_seed)
    values = []

    for theta in population:
        candidate = highres_trace(positions, theta)
        control = highres_trace(CONTIGUOUS, theta)

        for scenario in SCENARIOS:
            value = separation_ratio(
                candidate,
                control,
                scenario,
                rng,
            )
            if value is not None and np.isfinite(value):
                values.append(value)

    return np.asarray(values, dtype=float)


def summary(values: np.ndarray):
    return {
        "n": int(len(values)),
        "mean": float(np.mean(values)),
        "p10": float(np.quantile(values, 0.10)),
        "median": float(np.median(values)),
        "p90": float(np.quantile(values, 0.90)),
        "pass_fraction": float(np.mean(values > THRESHOLD)),
    }


def evaluate_by_scenario(
    positions: tuple[int, ...],
    population: np.ndarray,
    *,
    camera_seed: int,
):
    rng = np.random.default_rng(camera_seed)
    out = {scenario.name: [] for scenario in SCENARIOS}

    for theta in population:
        candidate = highres_trace(positions, theta)
        control = highres_trace(CONTIGUOUS, theta)

        for scenario in SCENARIOS:
            value = separation_ratio(
                candidate,
                control,
                scenario,
                rng,
            )
            if value is not None and np.isfinite(value):
                out[scenario.name].append(value)

    return {
        name: summary(np.asarray(values, dtype=float))
        for name, values in out.items()
    }


def main():
    design_population = sample_parameter_population(
        DESIGN_SEED,
        40,
        scale=0.60,
    )

    design_rows = []
    for index, positions in enumerate(candidate_positions()):
        values = evaluate_positions(
            positions,
            design_population,
            camera_seed=DESIGN_CAMERA_SEED + index * 97,
        )
        report = summary(values)
        design_rows.append(
            (
                report["p10"],
                report["median"],
                positions,
                report,
            )
        )

    design_rows.sort(reverse=True, key=lambda row: (row[0], row[1]))
    _, _, selected, selected_design = design_rows[0]

    test_population = sample_parameter_population(
        TEST_SEED,
        500,
        scale=0.80,
    )

    named = {
        "robust_selected": selected,
        "current_e002": CURRENT_E002,
        "evenly_spaced": EVEN,
    }

    reports = {}
    scenario_reports = {}

    for offset, (name, positions) in enumerate(named.items()):
        values = evaluate_positions(
            positions,
            test_population,
            camera_seed=TEST_CAMERA_SEED + offset * 100003,
        )
        reports[name] = summary(values)
        scenario_reports[name] = evaluate_by_scenario(
            positions,
            test_population,
            camera_seed=TEST_CAMERA_SEED + 700000 + offset * 100003,
        )

    selected_ok = (
        reports["robust_selected"]["p10"] > THRESHOLD
        and reports["robust_selected"]["pass_fraction"] >= 0.90
    )
    current_ok = (
        reports["current_e002"]["p10"] > THRESHOLD
        and reports["current_e002"]["pass_fraction"] >= 0.90
    )

    print("APST5-SIM-005")
    print("=" * 78)
    print(f"selected robust probe: {selected}")
    print(f"design P10 S: {selected_design['p10']:.6f}")
    print(f"design median S: {selected_design['median']:.6f}")
    print()

    for name, positions in named.items():
        report = reports[name]
        print(
            f"{name:16s} {positions} "
            f"mean={report['mean']:.4f} "
            f"p10={report['p10']:.4f} "
            f"median={report['median']:.4f} "
            f"p90={report['p90']:.4f} "
            f"pass={100*report['pass_fraction']:.2f}%"
        )

    print()
    print(f"selected robust-success: {selected_ok}")
    print(f"current E002 robust-success: {current_ok}")
    print()
    print("BY CAMERA SCENARIO")

    for name, positions in named.items():
        print(f"{name} {positions}")
        for scenario_name, report in scenario_reports[name].items():
            print(
                f"  {scenario_name:12s} "
                f"p10={report['p10']:.4f} "
                f"median={report['median']:.4f} "
                f"pass={100*report['pass_fraction']:.2f}%"
            )

    lines = []
    lines.append("# APST5-SIM-005: Camera-Robust Equal-Exposure Observability")
    lines.append("")
    lines.append(
        "**Status:** completed preregistered surrogate/camera observability analysis."
    )
    lines.append("")
    lines.append(f"**Selected robust sequence:** {selected}")
    lines.append("")
    lines.append(
        f"**Selected sequence meets frozen model-robust criterion:** "
        f"**{'YES' if selected_ok else 'NO'}**."
    )
    lines.append("")
    lines.append(
        f"**Current E002 (1,2,8) meets frozen model-robust criterion:** "
        f"**{'YES' if current_ok else 'NO'}**."
    )
    lines.append("")
    lines.append("## Held-out 500-person result")
    lines.append("")
    lines.append(
        "| Probe | high segments | mean S | P10 S | median S | P90 S | S>1.25 |"
    )
    lines.append("| --- | --- | ---: | ---: | ---: | ---: | ---: |")

    for name, positions in named.items():
        report = reports[name]
        lines.append(
            f"| {name} | {positions} | "
            f"{report['mean']:.3f} | **{report['p10']:.3f}** | "
            f"{report['median']:.3f} | {report['p90']:.3f} | "
            f"{100*report['pass_fraction']:.1f}% |"
        )

    lines.append("")
    lines.append("## Camera-scenario stress test")
    lines.append("")
    lines.append("| Probe | camera | P10 S | median S | S>1.25 |")
    lines.append("| --- | --- | ---: | ---: | ---: |")

    for name, positions in named.items():
        for scenario_name, report in scenario_reports[name].items():
            lines.append(
                f"| {name} {positions} | {scenario_name} | "
                f"{report['p10']:.3f} | {report['median']:.3f} | "
                f"{100*report['pass_fraction']:.1f}% |"
            )

    lines.append("")
    lines.append("## Interpretation")
    lines.append("")

    if current_ok:
        lines.append(
            "Under the committed pupil surrogate and frozen phone-camera stress "
            "model, the current E002 split sequence remains distinguishable "
            "from the matched-exposure contiguous control in at least 90% of "
            "held-out person x camera cells, with a 10th-percentile separation "
            "ratio above the E002 threshold."
        )
    else:
        lines.append(
            "Under the committed pupil surrogate and frozen phone-camera stress "
            "model, the current E002 split sequence does not satisfy the "
            "predeclared robust observability criterion. This does not invalidate "
            "E002, but it raises the risk that real phone observability will fail."
        )

    if selected != CURRENT_E002:
        lines.append("")
        lines.append(
            f"The minimax/P10 design search selected {selected} rather than "
            f"the frozen E002 sequence {CURRENT_E002}. Per preregistration, "
            "this does not modify E002-v1; it is a candidate for a future "
            "protocol version."
        )

    lines.append("")
    lines.append("## Claim boundary")
    lines.append("")
    lines.append(
        "This is a model/camera observability result. The assumed fractional "
        "pupil noise, pupil dynamics, frame drops, and timing jitter are "
        "surrogates. Only real synchronized captures can clear E002."
    )
    lines.append("")
    lines.append("## Reproduction")
    lines.append("")
    lines.append("    python experiments/camera_robust_probe.py")

    Path("results/APST5_SIMULATION_005.md").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
