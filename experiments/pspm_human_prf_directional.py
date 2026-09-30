"""Directional secondary analysis for APST5-HUMAN-PRF-001.

This is explicitly secondary/exploratory. It cannot replace the failed
preregistered H1/H2 primary result.

Plan:
experiments/registrations/APST5_HUMAN_PRF_001_SECONDARY_PLAN.md
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import numpy as np

import pspm_human_prf as base


@dataclass
class DirectionalPRF:
    subject: str
    step_time: np.ndarray
    bright: np.ndarray
    dark: np.ndarray
    sigma: float
    validation_rmse: float
    validation_r2: float
    n_fit_bright: int
    n_fit_dark: int
    n_validation_bright: int
    n_validation_dark: int


def estimate_directional(
    subject: str,
    pupil_path: Path,
    cogent_path: Path,
) -> DirectionalPRF:
    left, right, marker_times, marker_names = base.mat_channels(pupil_path)
    stimulus = base.cogent_stimulus(cogent_path)

    if len(marker_times) != len(stimulus):
        raise RuntimeError(
            f"subject {subject}: marker/stimulus length mismatch"
        )

    combined = base.combine_eyes(left, right)
    pupil50 = base.downsample_combined(combined)

    fit_rows, validation_rows = base.trial_partition(stimulus)
    fit_events = base.transitions_for_rows(
        fit_rows,
        stimulus,
        marker_times,
    )
    validation_events = base.transitions_for_rows(
        validation_rows,
        stimulus,
        marker_times,
    )

    fit = {"bright": [], "dark": []}
    step_time = None

    for event_time, amplitude, _ in fit_events:
        extracted = base.extract_response(
            pupil50,
            event_time,
            amplitude,
        )
        if extracted is None:
            continue
        time, response = extracted
        step_time = time
        key = "bright" if amplitude > 0 else "dark"
        fit[key].append(response)

    if step_time is None or not fit["bright"] or not fit["dark"]:
        raise RuntimeError(
            f"subject {subject}: missing directional fit responses"
        )

    bright = np.nanmedian(np.stack(fit["bright"], axis=0), axis=0)
    dark = np.nanmedian(np.stack(fit["dark"], axis=0), axis=0)

    errors = []
    obs_all = []
    pred_all = []
    n_val = {"bright": 0, "dark": 0}

    for event_time, amplitude, _ in validation_events:
        extracted = base.extract_response(
            pupil50,
            event_time,
            amplitude,
        )
        if extracted is None:
            continue

        time, response = extracted
        if len(time) != len(step_time):
            continue

        key = "bright" if amplitude > 0 else "dark"
        prediction = bright if key == "bright" else dark

        err = base.rmse(response, prediction)
        if np.isfinite(err):
            errors.append(err)
            n_val[key] += 1
            obs_all.append(response)
            pred_all.append(prediction)

    if not errors:
        raise RuntimeError(f"subject {subject}: no directional validation")

    observed = np.concatenate(obs_all)
    predicted = np.concatenate(pred_all)

    return DirectionalPRF(
        subject=subject,
        step_time=step_time,
        bright=bright,
        dark=dark,
        sigma=float(np.median(errors)),
        validation_rmse=float(base.rmse(observed, predicted)),
        validation_r2=float(base.r2_score(observed, predicted)),
        n_fit_bright=len(fit["bright"]),
        n_fit_dark=len(fit["dark"]),
        n_validation_bright=n_val["bright"],
        n_validation_dark=n_val["dark"],
    )


def predicted_waveform(
    participant: DirectionalPRF,
    positions: tuple[int, ...],
):
    probe = base.binary_probe(positions)
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
            kernel = participant.bright if delta > 0 else participant.dark

            if np.any(active):
                response[active] += delta * np.interp(
                    shifted[active],
                    participant.step_time,
                    kernel,
                    left=0.0,
                    right=kernel[-1],
                )

        previous = level

    response -= float(np.median(response[grid < 0.4]))
    return grid, response


def separation(
    participant: DirectionalPRF,
    positions: tuple[int, ...],
):
    _, candidate = predicted_waveform(participant, positions)
    _, control = predicted_waveform(participant, base.CONTIGUOUS)

    between = base.rmse(candidate, control)
    if (
        not np.isfinite(between)
        or not np.isfinite(participant.sigma)
        or participant.sigma <= 1e-12
    ):
        return np.nan

    return float(between / participant.sigma)


def split_participants(participants):
    ordered = sorted(participants, key=lambda p: p.subject)
    rng = np.random.default_rng(base.DESIGN_SEED)
    idx = np.arange(len(ordered))
    rng.shuffle(idx)
    n = len(ordered) // 2
    return [ordered[i] for i in idx[:n]], [ordered[i] for i in idx[n:]]


def summary(participants, positions):
    values = np.asarray(
        [separation(p, positions) for p in participants],
        dtype=float,
    )
    values = values[np.isfinite(values)]
    return {
        "n": int(len(values)),
        "mean": float(np.mean(values)),
        "p10": float(np.quantile(values, 0.10)),
        "median": float(np.median(values)),
        "p90": float(np.quantile(values, 0.90)),
        "pass_fraction": float(np.mean(values > base.THRESHOLD)),
        "values": values,
    }


def design_probe(design):
    rows = []
    for positions in base.candidate_positions():
        report = summary(design, positions)
        rows.append(
            (
                report["p10"],
                report["median"],
                report["mean"],
                positions,
                report,
            )
        )
    rows.sort(reverse=True, key=lambda x: (x[0], x[1], x[2]))
    return rows


def required_contrast(report):
    """Log-luminance step required for P10 S to hit frozen threshold."""
    p10 = report["p10"]
    if not np.isfinite(p10) or p10 <= 0:
        return np.nan, np.nan
    log_ratio = base.THRESHOLD / p10
    return float(log_ratio), float(np.exp(log_ratio))


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

        try:
            participants.append(
                estimate_directional(subject, pupil, cogent)
            )
        except Exception as exc:
            failures.append((subject, f"{type(exc).__name__}: {exc}"))

    if len(participants) < 15:
        raise RuntimeError(
            f"Only {len(participants)} participants usable: {failures}"
        )

    design, heldout = split_participants(participants)
    ranking = design_probe(design)
    selected = ranking[0][3]

    named = {
        "directional_selected": selected,
        "frozen_e002": base.E002,
        "sim005": base.SIM005,
        "evenly_spaced": base.EVEN,
    }

    design_reports = {
        name: summary(design, pos)
        for name, pos in named.items()
    }
    heldout_reports = {
        name: summary(heldout, pos)
        for name, pos in named.items()
    }

    ranks = {
        row[3]: i + 1
        for i, row in enumerate(ranking)
    }

    lines = []
    lines.append(
        "# APST5-HUMAN-PRF-001 Secondary: Directional Human Response Kernels"
    )
    lines.append("")
    lines.append(
        "**Status:** completed post-primary secondary/exploratory analysis."
    )
    lines.append("")
    lines.append(
        "**This result does not replace the failed preregistered primary H1/H2.**"
    )
    lines.append("")
    lines.append("## Directional held-out response adequacy")
    lines.append("")
    lines.append(
        "| subject | bright fit/val | dark fit/val | held-out RMSE | "
        "held-out R2 | sigma | split |"
    )
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | --- |")

    design_ids = {p.subject for p in design}
    for p in sorted(participants, key=lambda x: x.subject):
        lines.append(
            f"| {p.subject} | {p.n_fit_bright}/{p.n_validation_bright} | "
            f"{p.n_fit_dark}/{p.n_validation_dark} | "
            f"{p.validation_rmse:.4f} | {p.validation_r2:.4f} | "
            f"{p.sigma:.4f} | "
            f"{'design' if p.subject in design_ids else 'held-out'} |"
        )

    poor = [
        p.subject
        for p in participants
        if not np.isfinite(p.validation_r2) or p.validation_r2 <= 0
    ]

    lines.append("")
    lines.append(
        f"Non-positive directional held-out R2: **{len(poor)}/{len(participants)}**"
        + (f" ({', '.join(poor)})" if poor else "")
        + "."
    )

    lines.append("")
    lines.append("## Equal-exposure secondary result")
    lines.append("")
    lines.append(
        f"Directional design-set P10 search selected **{selected}**."
    )
    lines.append("")
    lines.append(
        "| Probe | positions | design P10 S | held-out P10 S | "
        "held-out median S | held-out S>1.25 | design rank | "
        "required log-contrast | required luminance ratio |"
    )
    lines.append(
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"
    )

    for name, positions in named.items():
        dr = design_reports[name]
        hr = heldout_reports[name]
        req_log, req_ratio = required_contrast(hr)
        lines.append(
            f"| {name} | {positions} | {dr['p10']:.3f} | "
            f"**{hr['p10']:.3f}** | {hr['median']:.3f} | "
            f"{100*hr['pass_fraction']:.1f}% | {ranks.get(positions, 'NA')} | "
            f"{req_log:.3f} | {req_ratio:.2f}x |"
        )

    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append(
        "Separating brightening and darkening response kernels tests whether "
        "the primary single-kernel model was too restrictive. Any improvement "
        "here is secondary evidence about response asymmetry, not a "
        "confirmatory rescue of the primary test."
    )
    lines.append("")
    lines.append(
        "The required-contrast columns use the LTI model's linear amplitude "
        "scaling to report the minimum high/low luminance ratio whose P10 "
        "separation would reach S=1.25. They are design requirements, not "
        "measurements of the current phone screen."
    )
    lines.append("")
    lines.append("## Failures")
    lines.append("")
    for subject, reason in failures:
        lines.append(f"- {subject}: {reason}")

    lines.append("")
    lines.append("## Claim boundary")
    lines.append("")
    lines.append(
        "This secondary analysis remains an EyeLink-based response-model "
        "bridge. It does not establish RGB-phone observability or state "
        "prediction."
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    print("\n".join(lines[:180]))


if __name__ == "__main__":
    main()
