"""Complete the preregistered secondary diagnostics for APST5-HUMAN-PRF-001.

This is explicitly secondary. It does not replace the failed primary H1/H2.

Plan:
experiments/registrations/APST5_HUMAN_PRF_001_SECONDARY_ADEQUACY.md
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import numpy as np

import pspm_human_prf as base
import pspm_human_prf_directional as directional


RATES = (50.0, 30.0, 24.0)


@dataclass
class TrialDiagnostic:
    subject: str
    disc_code: float
    rmse_mm: float
    r2: float
    return_offset_s: float


@dataclass
class ParticipantDiagnostic:
    subject: str
    pooled_r2: float
    median_trial_r2: float
    median_trial_rmse_mm: float
    n_trials: int
    return_offset_median_s: float
    trials: list[TrialDiagnostic]


def extract_full_trial(
    pupil50: np.ndarray,
    onset_s: float,
):
    """Observed baseline-centered waveform from -0.4 to +9.5 s."""
    start = int(round((onset_s - 0.4) * base.FS_ANALYSIS))
    stop = int(round((onset_s + 9.5) * base.FS_ANALYSIS))
    if start < 0 or stop > len(pupil50):
        return None

    window = pupil50[start:stop]
    expected = int(round(9.9 * base.FS_ANALYSIS))
    if len(window) != expected:
        return None

    finite_fraction = float(np.mean(np.isfinite(window)))
    if finite_fraction < 0.80:
        return None

    time = np.arange(expected, dtype=float) / base.FS_ANALYSIS - 0.4
    baseline_mask = (time >= -0.4) & (time < 0.0)
    baseline_values = window[baseline_mask]
    baseline_values = baseline_values[np.isfinite(baseline_values)]
    if len(baseline_values) < 0.8 * np.sum(baseline_mask):
        return None

    baseline = float(np.median(baseline_values))
    observed = window - baseline

    eval_mask = time >= 0.0
    return time[eval_mask], observed[eval_mask]


def predict_two_transition(
    participant: directional.DirectionalPRF,
    amplitude: float,
    time: np.ndarray,
):
    """Predict disc-on then return-to-background at +5 s."""
    prediction = np.zeros_like(time, dtype=float)

    # Disc-on transition.
    active = time >= 0.0
    kernel_on = participant.bright if amplitude > 0 else participant.dark
    prediction[active] += amplitude * np.interp(
        time[active],
        participant.step_time,
        kernel_on,
        left=0.0,
        right=kernel_on[-1],
    )

    # Return to background at 5 s has the opposite signed amplitude.
    return_amplitude = -amplitude
    shifted = time - 5.0
    active_return = shifted >= 0.0
    kernel_return = (
        participant.bright if return_amplitude > 0 else participant.dark
    )
    prediction[active_return] += return_amplitude * np.interp(
        shifted[active_return],
        participant.step_time,
        kernel_return,
        left=0.0,
        right=kernel_return[-1],
    )

    return prediction


def participant_superposition(
    subject: str,
    data_root: Path,
):
    pupil_path = data_root / f"AOB_UW_pupil_{subject}_sn2.mat"
    cogent_path = data_root / f"AOB_UW_cogent_{subject}_sn2.mat"

    model = directional.estimate_directional(
        subject,
        pupil_path,
        cogent_path,
    )

    left, right, marker_times, marker_names = base.mat_channels(pupil_path)
    stimulus = base.cogent_stimulus(cogent_path)

    if len(marker_times) != len(stimulus):
        raise RuntimeError("marker/stimulus mismatch")

    combined = base.combine_eyes(left, right)
    pupil50 = base.downsample_combined(combined)

    _, validation_rows = base.trial_partition(stimulus)

    observed_all = []
    predicted_all = []
    trials = []

    for row in validation_rows:
        disc_code = base.canonical_code(float(stimulus[row]))
        if disc_code == base.BACKGROUND_CODE:
            continue

        onset_s = float(marker_times[row])
        return_s = float(marker_times[row + 1])
        return_offset = return_s - onset_s

        # The released protocol is a 5 s disc followed by background.
        # Retain small clock deviations, but reject structurally wrong trials.
        if not (4.8 <= return_offset <= 5.2):
            continue

        extracted = extract_full_trial(pupil50, onset_s)
        if extracted is None:
            continue
        time, observed = extracted

        l_bg = base.CODE_TO_LUMINANCE[base.BACKGROUND_CODE]
        l_disc = base.CODE_TO_LUMINANCE[disc_code]
        amplitude = float(np.log(l_disc / l_bg))

        prediction = predict_two_transition(
            model,
            amplitude,
            time,
        )

        ok = np.isfinite(observed) & np.isfinite(prediction)
        if np.sum(ok) < 0.80 * len(time):
            continue

        obs = observed[ok]
        pred = prediction[ok]

        trial_rmse = base.rmse(obs, pred)
        trial_r2 = base.r2_score(obs, pred)

        trials.append(
            TrialDiagnostic(
                subject=subject,
                disc_code=disc_code,
                rmse_mm=float(trial_rmse),
                r2=float(trial_r2),
                return_offset_s=float(return_offset),
            )
        )
        observed_all.append(obs)
        predicted_all.append(pred)

    if not trials:
        raise RuntimeError("no usable validation full trials")

    pooled_observed = np.concatenate(observed_all)
    pooled_predicted = np.concatenate(predicted_all)

    return model, ParticipantDiagnostic(
        subject=subject,
        pooled_r2=float(base.r2_score(pooled_observed, pooled_predicted)),
        median_trial_r2=float(np.median([x.r2 for x in trials])),
        median_trial_rmse_mm=float(np.median([x.rmse_mm for x in trials])),
        n_trials=len(trials),
        return_offset_median_s=float(
            np.median([x.return_offset_s for x in trials])
        ),
        trials=trials,
    )


def sampled_separation(
    participant: directional.DirectionalPRF,
    positions: tuple[int, ...],
    rate_hz: float,
):
    grid50, candidate50 = directional.predicted_waveform(
        participant,
        positions,
    )
    _, control50 = directional.predicted_waveform(
        participant,
        base.CONTIGUOUS,
    )

    grid = np.arange(0.0, 5.0, 1.0 / rate_hz)
    candidate = np.interp(grid, grid50, candidate50)
    control = np.interp(grid, grid50, control50)

    between = base.rmse(candidate, control)
    if not np.isfinite(participant.sigma) or participant.sigma <= 1e-12:
        return np.nan
    return float(between / participant.sigma)


def rate_summary(participants, rate_hz):
    values = np.asarray(
        [
            sampled_separation(p, base.E002, rate_hz)
            for p in participants
        ],
        dtype=float,
    )
    values = values[np.isfinite(values)]
    return {
        "n": int(len(values)),
        "p10": float(np.quantile(values, 0.10)),
        "median": float(np.median(values)),
        "pass_fraction": float(np.mean(values > base.THRESHOLD)),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    models = []
    diagnostics = []
    failures = []

    for sid in range(1, 24):
        subject = f"{sid:02d}"
        pupil = args.data_root / f"AOB_UW_pupil_{subject}_sn2.mat"
        cogent = args.data_root / f"AOB_UW_cogent_{subject}_sn2.mat"
        if not pupil.exists() or not cogent.exists():
            failures.append((subject, "missing source file"))
            continue

        try:
            model, diagnostic = participant_superposition(
                subject,
                args.data_root,
            )
            models.append(model)
            diagnostics.append(diagnostic)
        except Exception as exc:
            failures.append(
                (subject, f"{type(exc).__name__}: {exc}")
            )

    if len(models) < 15:
        raise RuntimeError(
            f"Only {len(models)} participants usable: {failures}"
        )

    design, heldout = directional.split_participants(models)

    rate_reports = {
        rate: rate_summary(heldout, rate)
        for rate in RATES
    }

    pooled_r2 = np.asarray(
        [d.pooled_r2 for d in diagnostics],
        dtype=float,
    )
    median_trial_r2 = np.asarray(
        [d.median_trial_r2 for d in diagnostics],
        dtype=float,
    )

    lines = []
    lines.append(
        "# APST5-HUMAN-PRF-001 Secondary Adequacy and Camera-Rate Diagnostics"
    )
    lines.append("")
    lines.append(
        "**Status:** completed secondary diagnostics predeclared after the "
        "failed primary. These results do not replace H1/H2."
    )
    lines.append("")
    lines.append("## Two-transition superposition adequacy")
    lines.append("")
    lines.append(
        "Directional kernels estimated from fit transitions were used, "
        "without refitting, to predict complete held-out five-second "
        "disc-on plus five-second return-to-background pupil trials."
    )
    lines.append("")
    lines.append(
        "| subject | validation trials | pooled R2 | median trial R2 | "
        "median trial RMSE (mm) | median return offset (s) |"
    )
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: |")

    for d in sorted(diagnostics, key=lambda x: x.subject):
        lines.append(
            f"| {d.subject} | {d.n_trials} | {d.pooled_r2:.4f} | "
            f"{d.median_trial_r2:.4f} | {d.median_trial_rmse_mm:.4f} | "
            f"{d.return_offset_median_s:.4f} |"
        )

    lines.append("")
    lines.append(
        f"- participants with pooled R2 > 0: "
        f"**{100*np.mean(pooled_r2 > 0):.1f}% "
        f"({int(np.sum(pooled_r2 > 0))}/{len(pooled_r2)})**"
    )
    lines.append(
        f"- median participant pooled R2: "
        f"**{np.median(pooled_r2):.4f}**"
    )
    lines.append(
        f"- median participant median-trial R2: "
        f"**{np.median(median_trial_r2):.4f}**"
    )
    lines.append("")
    lines.append("## Frozen E002 camera-rate sensitivity")
    lines.append("")
    lines.append(
        "No sequence was re-optimized. The already frozen E002 (1,2,8) "
        "was sampled from the directional human-calibrated waveform model."
    )
    lines.append("")
    lines.append(
        "| sampling rate | held-out P10 S | held-out median S | "
        "held-out S>1.25 |"
    )
    lines.append("| ---: | ---: | ---: | ---: |")

    for rate in RATES:
        report = rate_reports[rate]
        lines.append(
            f"| {rate:.0f} Hz | **{report['p10']:.3f}** | "
            f"{report['median']:.3f} | "
            f"{100*report['pass_fraction']:.1f}% |"
        )

    lines.append("")
    lines.append("## Interpretation")
    lines.append("")

    positive_fraction = float(np.mean(pooled_r2 > 0))
    median_pooled = float(np.median(pooled_r2))

    if positive_fraction >= 0.75 and median_pooled > 0:
        lines.append(
            "The directional superposition bridge predicts complete held-out "
            "two-transition luminance trials above a zero-R2 baseline for most "
            "participants. This strengthens, but does not confirm, the "
            "secondary human-calibrated E002 waveform result."
        )
    else:
        lines.append(
            "The directional superposition bridge does not predict complete "
            "held-out two-transition trials reliably enough to treat the "
            "secondary E002 separation result as strong biological evidence. "
            "Real phone capture remains decisive."
        )

    lines.append("")
    lines.append(
        "Camera-rate sensitivity only tests temporal sampling of the "
        "EyeLink-derived model. It does not model RGB pupil segmentation, "
        "phone auto-exposure, or state prediction."
    )
    lines.append("")
    lines.append("## Failures")
    lines.append("")
    for subject, reason in failures:
        lines.append(f"- {subject}: {reason}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )
    print("\n".join(lines[:220]))


if __name__ == "__main__":
    main()
