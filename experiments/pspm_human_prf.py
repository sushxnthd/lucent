"""APST5-HUMAN-PRF-001.

Human-calibrated equal-exposure probe observability using the public
PsPM-AOB_UW controlled-luminance EyeLink dataset.

Preregistration:
experiments/registrations/APST5_HUMAN_PRF_001.md

Data are downloaded by the reproduction workflow and are not redistributed.
"""

from __future__ import annotations

import argparse
import itertools
import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy.io import loadmat
from scipy.signal import butter, sosfiltfilt


FS_RAW = 500.0
FS_ANALYSIS = 50.0
DOWNSAMPLE = int(round(FS_RAW / FS_ANALYSIS))
MAX_GAP_S = 0.250
MAX_GAP_RAW = int(round(MAX_GAP_S * FS_RAW))
LOWPASS_HZ = 4.0

BACKGROUND_CODE = 9.0
CODE_TO_LUMINANCE = {
    0.00: 33.50,
    0.25: 36.70,
    0.75: 60.70,
    1.00: 84.10,
    9.00: 46.10,
}

CONTIGUOUS = (4, 5, 6)
E002 = (1, 2, 8)
SIM005 = (1, 2, 9)
EVEN = (2, 5, 8)
DESIGN_SEED = 20260930
THRESHOLD = 1.25


@dataclass
class ParticipantPRF:
    subject: str
    step_time: np.ndarray
    step_response: np.ndarray
    sigma: float
    validation_rmse: float
    validation_r2: float
    n_fit: int
    n_validation: int


def interpolate_short_gaps(x: np.ndarray, max_gap: int) -> np.ndarray:
    x = np.asarray(x, dtype=float).copy()
    finite = np.isfinite(x) & (x > 0)
    x[~finite] = np.nan

    n = len(x)
    i = 0
    while i < n:
        if np.isfinite(x[i]):
            i += 1
            continue
        start = i
        while i < n and not np.isfinite(x[i]):
            i += 1
        end = i
        gap = end - start

        if (
            gap <= max_gap
            and start > 0
            and end < n
            and np.isfinite(x[start - 1])
            and np.isfinite(x[end])
        ):
            x[start:end] = np.linspace(
                x[start - 1],
                x[end],
                gap + 2,
            )[1:-1]

    return x


def filter_finite_segments(x: np.ndarray) -> np.ndarray:
    out = np.full_like(x, np.nan, dtype=float)
    sos = butter(
        4,
        LOWPASS_HZ,
        btype="lowpass",
        fs=FS_RAW,
        output="sos",
    )

    finite = np.isfinite(x)
    n = len(x)
    i = 0

    while i < n:
        if not finite[i]:
            i += 1
            continue
        start = i
        while i < n and finite[i]:
            i += 1
        end = i

        segment = x[start:end]
        if len(segment) >= int(FS_RAW):
            try:
                out[start:end] = sosfiltfilt(sos, segment)
            except ValueError:
                out[start:end] = segment
        else:
            out[start:end] = segment

    return out


def preprocess_eye(x: np.ndarray) -> np.ndarray:
    x = interpolate_short_gaps(x, MAX_GAP_RAW)
    x = filter_finite_segments(x)
    return x


def combine_eyes(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    left = preprocess_eye(left)
    right = preprocess_eye(right)

    stacked = np.stack([left, right], axis=0)
    count = np.sum(np.isfinite(stacked), axis=0)
    total = np.nansum(stacked, axis=0)

    out = np.full(left.shape, np.nan, dtype=float)
    ok = count > 0
    out[ok] = total[ok] / count[ok]
    return out


def mat_channels(path: Path):
    d = loadmat(path, squeeze_me=True, struct_as_record=False)
    channels = np.asarray(d["data"], dtype=object).reshape(-1)

    left = np.asarray(channels[0].data, dtype=float).reshape(-1)
    right = np.asarray(channels[1].data, dtype=float).reshape(-1)

    markers = channels[6]
    times = np.asarray(markers.data, dtype=float).reshape(-1)
    names = np.asarray(markers.markerinfo.name, dtype=object).reshape(-1)

    return left, right, times, [str(x) for x in names]


def cogent_stimulus(path: Path) -> np.ndarray:
    d = loadmat(path, squeeze_me=True, struct_as_record=False)
    arr = np.asarray(d["data"], dtype=float)

    if arr.ndim != 2 or arr.shape[1] < 2:
        raise RuntimeError(f"Unexpected Cogent matrix: {path} {arr.shape}")

    trial_index = arr[:, 0]
    expected = np.arange(1, len(arr) + 1, dtype=float)
    if not np.array_equal(trial_index, expected):
        raise RuntimeError(f"Unexpected Cogent trial indices in {path}")

    return arr[:, 1].astype(float)


def canonical_code(value: float) -> float:
    keys = np.asarray(list(CODE_TO_LUMINANCE), dtype=float)
    index = int(np.argmin(np.abs(keys - value)))
    nearest = float(keys[index])
    if abs(nearest - value) > 1e-6:
        raise RuntimeError(f"Unknown luminance stimulus code {value!r}")
    return nearest


def downsample_combined(x: np.ndarray) -> np.ndarray:
    return x[::DOWNSAMPLE].copy()


def extract_response(
    pupil50: np.ndarray,
    event_time_s: float,
    amplitude: float,
):
    if abs(amplitude) <= 1e-12:
        return None

    start_s = event_time_s - 0.5
    stop_s = event_time_s + 4.5

    start = int(round(start_s * FS_ANALYSIS))
    stop = int(round(stop_s * FS_ANALYSIS))

    if start < 0 or stop > len(pupil50):
        return None

    window = pupil50[start:stop]
    expected = int(round(5.0 * FS_ANALYSIS))
    if len(window) != expected:
        return None

    finite_fraction = float(np.mean(np.isfinite(window)))
    if finite_fraction < 0.80:
        return None

    time = np.arange(expected, dtype=float) / FS_ANALYSIS - 0.5
    baseline_mask = (time >= -0.4) & (time < 0.0)
    baseline_values = window[baseline_mask]
    baseline_values = baseline_values[np.isfinite(baseline_values)]

    if len(baseline_values) < 0.8 * np.sum(baseline_mask):
        return None

    baseline = float(np.median(baseline_values))
    response = (window - baseline) / amplitude

    # Primary PRF lives from transition onset through +4.5 s.
    post = time >= 0.0
    return time[post], response[post]


def trial_partition(stimulus: np.ndarray):
    disc_rows = [
        i
        for i, code in enumerate(stimulus)
        if canonical_code(float(code)) != BACKGROUND_CODE
    ]

    by_code: dict[float, list[int]] = {}
    for row in disc_rows:
        code = canonical_code(float(stimulus[row]))
        by_code.setdefault(code, []).append(row)

    expected_disc_codes = sorted(
        code for code in CODE_TO_LUMINANCE if code != BACKGROUND_CODE
    )

    if sorted(by_code) != expected_disc_codes:
        raise RuntimeError(
            f"Unexpected disc-code set {sorted(by_code)}; "
            f"expected {expected_disc_codes}"
        )

    fit_rows = []
    validation_rows = []

    for code in expected_disc_codes:
        rows = sorted(by_code[code])
        if len(rows) != 6:
            raise RuntimeError(
                f"Stimulus code {code} has {len(rows)} presentations, expected 6"
            )
        fit_rows.extend(rows[:3])
        validation_rows.extend(rows[3:])

    return sorted(fit_rows), sorted(validation_rows)


def transitions_for_rows(
    rows: list[int],
    stimulus: np.ndarray,
    marker_times: np.ndarray,
):
    events = []

    for row in rows:
        if row <= 0:
            raise RuntimeError("Disc row has no preceding luminance marker")
        if row + 1 >= len(stimulus):
            raise RuntimeError("Disc row has no return-to-background marker")

        disc_code = canonical_code(float(stimulus[row]))
        before_code = canonical_code(float(stimulus[row - 1]))
        after_code = canonical_code(float(stimulus[row + 1]))

        if before_code != BACKGROUND_CODE or after_code != BACKGROUND_CODE:
            raise RuntimeError(
                f"Expected background-disc-background around row {row}"
            )

        l_bg = CODE_TO_LUMINANCE[BACKGROUND_CODE]
        l_disc = CODE_TO_LUMINANCE[disc_code]

        events.append(
            (
                float(marker_times[row]),
                float(np.log(l_disc / l_bg)),
                f"{disc_code:g}_on",
            )
        )
        events.append(
            (
                float(marker_times[row + 1]),
                float(np.log(l_bg / l_disc)),
                f"{disc_code:g}_off",
            )
        )

    return events


def rmse(a: np.ndarray, b: np.ndarray) -> float:
    ok = np.isfinite(a) & np.isfinite(b)
    if np.sum(ok) < 20:
        return np.nan
    return float(np.sqrt(np.mean((a[ok] - b[ok]) ** 2)))


def r2_score(obs: np.ndarray, pred: np.ndarray) -> float:
    ok = np.isfinite(obs) & np.isfinite(pred)
    if np.sum(ok) < 20:
        return np.nan

    y = obs[ok]
    p = pred[ok]
    denom = float(np.sum((y - np.mean(y)) ** 2))
    if denom <= 1e-12:
        return np.nan

    return float(1.0 - np.sum((y - p) ** 2) / denom)


def estimate_participant(
    subject: str,
    pupil_path: Path,
    cogent_path: Path,
) -> ParticipantPRF:
    left, right, marker_times, marker_names = mat_channels(pupil_path)
    stimulus = cogent_stimulus(cogent_path)

    if len(marker_times) != len(stimulus):
        raise RuntimeError(
            f"subject {subject}: marker/stimulus length mismatch "
            f"{len(marker_times)} vs {len(stimulus)}"
        )

    if len(marker_names) != len(stimulus):
        raise RuntimeError(
            f"subject {subject}: marker-name/stimulus length mismatch"
        )

    # Mapping is mechanical: published Cogent stimulus rows align one-to-one
    # with the pupil event channel.
    codes = [canonical_code(float(x)) for x in stimulus]
    if codes[0] != BACKGROUND_CODE:
        raise RuntimeError(f"subject {subject}: first event is not background")

    combined = combine_eyes(left, right)
    pupil50 = downsample_combined(combined)

    fit_rows, validation_rows = trial_partition(stimulus)
    fit_events = transitions_for_rows(
        fit_rows,
        stimulus,
        marker_times,
    )
    validation_events = transitions_for_rows(
        validation_rows,
        stimulus,
        marker_times,
    )

    fit_responses = []
    step_time = None

    for event_time, amplitude, _ in fit_events:
        extracted = extract_response(
            pupil50,
            event_time,
            amplitude,
        )
        if extracted is None:
            continue
        time, response = extracted
        step_time = time
        fit_responses.append(response)

    if not fit_responses or step_time is None:
        raise RuntimeError(f"subject {subject}: no usable fit responses")

    fit_stack = np.stack(fit_responses, axis=0)
    step_response = np.nanmedian(fit_stack, axis=0)

    validation_responses = []
    errors = []
    observed_all = []
    predicted_all = []

    for event_time, amplitude, _ in validation_events:
        extracted = extract_response(
            pupil50,
            event_time,
            amplitude,
        )
        if extracted is None:
            continue

        time, normalized = extracted
        if len(time) != len(step_time):
            continue

        validation_responses.append(normalized)
        error = rmse(normalized, step_response)
        if np.isfinite(error):
            errors.append(error)

        observed_all.append(normalized)
        predicted_all.append(step_response)

    if not errors:
        raise RuntimeError(f"subject {subject}: no usable validation responses")

    observed = np.concatenate(observed_all)
    predicted = np.concatenate(predicted_all)

    return ParticipantPRF(
        subject=subject,
        step_time=step_time,
        step_response=step_response,
        sigma=float(np.median(errors)),
        validation_rmse=float(rmse(observed, predicted)),
        validation_r2=float(r2_score(observed, predicted)),
        n_fit=len(fit_responses),
        n_validation=len(validation_responses),
    )


def candidate_positions():
    yield from itertools.combinations(range(1, 10), 3)


def binary_probe(positions: tuple[int, ...]) -> np.ndarray:
    probe = np.zeros(10, dtype=float)
    probe[list(positions)] = 1.0
    return probe


def predicted_probe_waveform(
    participant: ParticipantPRF,
    positions: tuple[int, ...],
):
    probe = binary_probe(positions)
    grid = np.arange(0.0, 5.0, 0.05)
    response = np.zeros_like(grid)

    previous = 0.0
    for segment, level in enumerate(probe):
        if segment == 0:
            previous = level
            continue

        delta = float(level - previous)
        if abs(delta) > 0:
            transition_time = segment * 0.5
            shifted = grid - transition_time
            active = shifted >= 0.0
            if np.any(active):
                response[active] += delta * np.interp(
                    shifted[active],
                    participant.step_time,
                    participant.step_response,
                    left=0.0,
                    right=participant.step_response[-1],
                )
        previous = level

    baseline = response[grid < 0.4]
    response = response - float(np.median(baseline))
    return grid, response


def separation(
    participant: ParticipantPRF,
    positions: tuple[int, ...],
):
    _, candidate = predicted_probe_waveform(participant, positions)
    _, control = predicted_probe_waveform(participant, CONTIGUOUS)

    between = rmse(candidate, control)
    if not np.isfinite(between):
        return np.nan

    if not np.isfinite(participant.sigma) or participant.sigma <= 1e-12:
        return np.nan

    return float(between / participant.sigma)


def summarize(values: list[float]):
    x = np.asarray([v for v in values if np.isfinite(v)], dtype=float)
    if len(x) == 0:
        return {
            "n": 0,
            "mean": np.nan,
            "p10": np.nan,
            "median": np.nan,
            "p90": np.nan,
            "pass_fraction": np.nan,
        }

    return {
        "n": int(len(x)),
        "mean": float(np.mean(x)),
        "p10": float(np.quantile(x, 0.10)),
        "median": float(np.median(x)),
        "p90": float(np.quantile(x, 0.90)),
        "pass_fraction": float(np.mean(x > THRESHOLD)),
    }


def split_participants(participants: list[ParticipantPRF]):
    ordered = sorted(participants, key=lambda p: p.subject)
    rng = np.random.default_rng(DESIGN_SEED)
    index = np.arange(len(ordered))
    rng.shuffle(index)

    n_design = len(ordered) // 2
    design = [ordered[i] for i in index[:n_design]]
    heldout = [ordered[i] for i in index[n_design:]]
    return design, heldout


def design_probe(design: list[ParticipantPRF]):
    rows = []

    for positions in candidate_positions():
        values = [separation(p, positions) for p in design]
        report = summarize(values)
        rows.append(
            (
                report["p10"],
                report["median"],
                report["mean"],
                positions,
                report,
            )
        )

    rows.sort(reverse=True, key=lambda row: (row[0], row[1], row[2]))
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    participants = []
    failures = []

    for sid in range(1, 24):
        subject = f"{sid:02d}"
        pupil = args.data_root / f"AOB_UW_pupil_{subject}_sn2.mat"
        cogent = args.data_root / f"AOB_UW_cogent_{subject}_sn2.mat"

        if not pupil.exists():
            failures.append((subject, "missing luminance pupil file"))
            continue
        if not cogent.exists():
            failures.append((subject, "missing luminance Cogent file"))
            continue

        try:
            participants.append(
                estimate_participant(subject, pupil, cogent)
            )
        except Exception as exc:
            failures.append((subject, f"{type(exc).__name__}: {exc}"))

    if len(participants) < 15:
        raise RuntimeError(
            f"Only {len(participants)} participants usable; failures={failures}"
        )

    design, heldout = split_participants(participants)
    ranking = design_probe(design)
    selected = ranking[0][3]

    named = {
        "human_selected": selected,
        "frozen_e002": E002,
        "sim005": SIM005,
        "evenly_spaced": EVEN,
    }

    design_reports = {}
    heldout_reports = {}

    for name, positions in named.items():
        design_reports[name] = summarize(
            [separation(p, positions) for p in design]
        )
        heldout_reports[name] = summarize(
            [separation(p, positions) for p in heldout]
        )

    h1 = (
        heldout_reports["human_selected"]["p10"] > THRESHOLD
        and heldout_reports["human_selected"]["pass_fraction"] >= 0.90
    )
    h2 = (
        heldout_reports["frozen_e002"]["p10"] > THRESHOLD
        and heldout_reports["frozen_e002"]["pass_fraction"] >= 0.90
    )

    all_positions = [row[3] for row in ranking]
    design_rank = {
        positions: i + 1
        for i, positions in enumerate(all_positions)
    }

    lines = []
    lines.append(
        "# APST5-HUMAN-PRF-001: Human-Calibrated Active-Probe Observability"
    )
    lines.append("")
    lines.append(
        "**Status:** completed preregistered public-human controlled-luminance analysis."
    )
    lines.append("")
    lines.append(
        f"**H1 human-optimized held-out criterion:** "
        f"**{'SUPPORTED' if h1 else 'NOT SUPPORTED'}**."
    )
    lines.append("")
    lines.append(
        f"**H2 frozen E002 held-out criterion:** "
        f"**{'SUPPORTED' if h2 else 'NOT SUPPORTED'}**."
    )
    lines.append("")
    lines.append("## Dataset")
    lines.append("")
    lines.append(
        "PsPM-AOB_UW public EyeLink controlled-luminance data "
        "(Zenodo 10.5281/zenodo.8239465)."
    )
    lines.append("")
    lines.append(
        f"- usable participants: **{len(participants)}**"
    )
    lines.append(
        f"- design participants: **{len(design)}**"
    )
    lines.append(
        f"- held-out participants: **{len(heldout)}**"
    )
    lines.append(
        "- subject 06 luminance pupil recording is absent in the source archive."
    )
    lines.append("")
    lines.append("## Empirical step-response adequacy")
    lines.append("")
    lines.append(
        "| subject | fit transitions | validation transitions | "
        "validation RMSE | validation R2 | noise scale sigma | split |"
    )
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | --- |")

    design_ids = {p.subject for p in design}
    for p in sorted(participants, key=lambda x: x.subject):
        lines.append(
            f"| {p.subject} | {p.n_fit} | {p.n_validation} | "
            f"{p.validation_rmse:.4f} | {p.validation_r2:.4f} | "
            f"{p.sigma:.4f} | "
            f"{'design' if p.subject in design_ids else 'held-out'} |"
        )

    lines.append("")
    lines.append("## Equal-exposure sequence result")
    lines.append("")
    lines.append(
        f"Human-design-set P10 search selected **{selected}**."
    )
    lines.append("")
    lines.append(
        "| Probe | positions | design P10 S | held-out P10 S | "
        "held-out median S | held-out S>1.25 | design rank |"
    )
    lines.append("| --- | --- | ---: | ---: | ---: | ---: | ---: |")

    for name, positions in named.items():
        dr = design_reports[name]
        hr = heldout_reports[name]
        lines.append(
            f"| {name} | {positions} | "
            f"{dr['p10']:.3f} | **{hr['p10']:.3f}** | "
            f"{hr['median']:.3f} | "
            f"{100*hr['pass_fraction']:.1f}% | "
            f"{design_rank.get(positions, 'NA')} |"
        )

    lines.append("")
    lines.append("## Interpretation")
    lines.append("")

    if h2:
        lines.append(
            "The frozen E002 split timing exceeds the preregistered "
            "human-calibrated observability threshold on held-out participants "
            "under the empirical linear step-response approximation."
        )
    else:
        lines.append(
            "The frozen E002 split timing does not satisfy the preregistered "
            "human-calibrated held-out observability criterion."
        )

    lines.append("")
    lines.append(
        "This analysis does not use the hand-specified Lucent pupil-parameter "
        "population for the primary waveform. Each participant's response "
        "function and noise scale are estimated from real controlled-luminance "
        "EyeLink transitions, with separate held-out transitions used to "
        "quantify response error."
    )

    poor_r2 = [
        p.subject
        for p in participants
        if not np.isfinite(p.validation_r2) or p.validation_r2 <= 0.0
    ]

    lines.append("")
    lines.append("## Model-adequacy warning")
    lines.append("")
    lines.append(
        f"Participants with non-positive held-out step-response R2: "
        f"**{len(poor_r2)}/{len(participants)}**"
        + (f" ({', '.join(poor_r2)})" if poor_r2 else "")
        + "."
    )

    if len(poor_r2) > len(participants) / 2:
        lines.append("")
        lines.append(
            "**The empirical LTI bridge predicts held-out transition waveforms "
            "poorly for most participants; probe-separation results must be "
            "treated as exploratory regardless of H1/H2.**"
        )

    lines.append("")
    lines.append("## Source-data failures")
    lines.append("")
    for subject, reason in failures:
        lines.append(f"- {subject}: {reason}")

    lines.append("")
    lines.append("## Claim boundary")
    lines.append("")
    lines.append(
        "A positive result predicts biological waveform observability under a "
        "human-calibrated LTI approximation. It does not show that an RGB "
        "phone camera resolves that waveform and does not validate fatigue or "
        "vigilance inference."
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    print("\n".join(lines[:160]))


if __name__ == "__main__":
    main()
