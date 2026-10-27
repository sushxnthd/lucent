#!/usr/bin/env python3
"""E002-485: participant-disjoint, reference-only falsification of gap exclusions.

Input is independently annotated 150-fps high-speed eyelid *aperture fractions*,
NOT raw video or proof of physical camera exposure. This program never authorizes
anatomical or medical claims. Standard library only.
"""
import argparse
import csv
import json
import math
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

SOURCE_DOI = '10.1038/s41597-025-04861-9'
MIN_DT_MS = 1000.0 / 150.0 * 0.8
MAX_DT_MS = 1000.0 / 150.0 * 1.2
CAL_SUBJECTS = {f'S{i:02d}' for i in range(1, 21)}
TEST_SUBJECTS = {f'S{i:02d}' for i in range(21, 32)}


@dataclass(frozen=True)
class Frame:
    subject: str
    session: str
    idx: int
    t: float
    a: float
    u: float
    quality: str

    @property
    def lo(self):
        return max(0.0, self.a - self.u)

    @property
    def hi(self):
        return min(1.0, self.a + self.u)


def load_csv(path):
    groups = defaultdict(list)
    required = {'participant', 'session', 'frame_idx', 't_ms',
                'aperture_fraction', 'uncertainty_fraction', 'quality_flags'}
    with open(path, newline='', encoding='utf-8') as handle:
        reader = csv.DictReader(handle)
        if not required.issubset(set(reader.fieldnames or [])):
            raise ValueError('Missing required columns: ' + ','.join(sorted(required - set(reader.fieldnames or []))))
        for line, row in enumerate(reader, 2):
            try:
                subject = row['participant'].strip()
                if subject not in CAL_SUBJECTS | TEST_SUBJECTS:
                    raise ValueError('unrecognized participant')
                frame = Frame(subject, row['session'].strip(), int(row['frame_idx']),
                              float(row['t_ms']), float(row['aperture_fraction']),
                              float(row['uncertainty_fraction']), row['quality_flags'].strip().lower())
                if not frame.session or not all(math.isfinite(x) for x in (frame.t, frame.a, frame.u)):
                    raise ValueError('missing session or nonfinite measurement')
                if not (0 <= frame.a <= 1 and 0 <= frame.u <= 1):
                    raise ValueError('aperture/uncertainty outside [0,1]')
            except (TypeError, ValueError) as exc:
                raise ValueError(f'CSV line {line}: {exc}') from exc
            groups[(subject, frame.session)].append(frame)
    for key, frames in groups.items():
        frames.sort(key=lambda f: f.idx)
        if any(b.idx <= a.idx or b.t <= a.t for a, b in zip(frames, frames[1:])):
            raise ValueError(f'duplicate/nonmonotonic frame or timestamp in {key}')
    return groups


def clean_pair(a, b):
    return (a.quality == 'ok' and b.quality == 'ok' and b.idx == a.idx + 1
            and MIN_DT_MS <= b.t - a.t <= MAX_DT_MS)


def analyze(groups, threshold=0.1, clock_ms=0.5, synthetic=False):
    if not (0 <= threshold < 1 and 0 <= clock_ms < MIN_DT_MS / 2):
        raise ValueError('invalid threshold or clock error')
    cal = set()
    test = set()
    speeds = []
    for (subject, _), frames in groups.items():
        if subject in CAL_SUBJECTS:
            for a, b in zip(frames, frames[1:]):
                if clean_pair(a, b):
                    dt_min = (b.t - a.t) - 2 * clock_ms
                    speeds.append((abs(b.a - a.a) + a.u + b.u) / dt_min)
                    cal.add(subject)
        elif subject in TEST_SUBJECTS and len(frames) >= 6:
            test.add(subject)
    if not speeds:
        raise ValueError('no usable calibration slopes')
    if not synthetic and (len(cal) != 20 or len(test) != 11):
        raise ValueError(f'prespecified 20/11 subject coverage unmet: {len(cal)}/{len(test)}')
    v_proxy = max(speeds)  # observed secant proxy, NEVER a physiological hard cap
    counts = defaultdict(int)
    examples = []
    test_speed_exceedances = 0
    test_speed_pairs = 0
    for (subject, session), frames in sorted(groups.items()):
        if subject not in TEST_SUBJECTS:
            continue
        for a, b in zip(frames, frames[1:]):
            if clean_pair(a, b):
                test_speed_pairs += 1
                speed = (abs(b.a - a.a) + a.u + b.u) / ((b.t - a.t) - 2 * clock_ms)
                if speed > v_proxy + 1e-12:
                    test_speed_exceedances += 1
        # Nonoverlapping 5-interval windows, aligned to recorded frame indices.
        for start in range(0, len(frames) - 5, 5):
            window = frames[start:start + 6]
            if not all(clean_pair(a, b) for a, b in zip(window, window[1:])):
                counts['abstain_nuisance_or_missing'] += 1
                continue
            a, b = window[0], window[-1]
            if a.lo <= threshold or b.lo <= threshold:
                counts['abstain_endpoint_uncertain'] += 1
                continue
            gap_max = b.t - a.t + 2 * clock_ms
            z = ((a.lo - threshold) + (b.lo - threshold)) / (v_proxy * gap_max) if v_proxy > 0 else math.inf
            excluded = z > 1 + 1e-12
            witnessed = any(f.hi <= threshold for f in window[1:-1])
            counts['windows_eligible'] += 1
            counts['conditional_excluded' if excluded else 'conditional_possible'] += 1
            if witnessed:
                counts['reference_observed_closure'] += 1
            else:
                counts['reference_unresolved_not_negative'] += 1
            if excluded and witnessed:
                counts['falsified_joint_assumptions'] += 1
                examples.append({'participant': subject, 'session': session,
                                 'frame_start': a.idx, 'frame_end': b.idx,
                                 'z': round(z, 8), 'reason': 'observed high-rate closure contradicts proxy-cap exclusion'})
    if counts['windows_eligible'] == 0:
        raise ValueError('no eligible held-out windows; cannot report success')
    return {
        'protocol': 'E002-485', 'source_doi': SOURCE_DOI,
        'evidence_tier': 'SYNTHETIC_FIXTURE' if synthetic else 'UNVERIFIED_HUMAN_ANNOTATIONS',
        'reference_frame_rate_hz': 150, 'simulated_low_rate_hz': 30,
        'aperture_threshold_fraction': threshold, 'endpoint_clock_uncertainty_ms': clock_ms,
        'calibration_subjects': len(cal), 'heldout_subjects': len(test),
        'calibration_proxy_speed_fraction_per_ms': round(v_proxy, 10),
        'proxy_is_hard_velocity_bound': False,
        'heldout_secant_proxy_exceedances': test_speed_exceedances,
        'heldout_secant_pairs': test_speed_pairs,
        'counts': dict(sorted(counts.items())), 'falsification_examples': examples[:20],
        'interpretation': 'A conditional exclusion contradicted by observed reference closure falsifies the joint proxy-speed/measurement assumptions; no nonclosure ground truth is inferred from missed high-rate frames.',
        'physical_claims': 'ABSTAIN_UNCALIBRATED', 'product_release': 'BLOCKED',
    }


def synthetic_fixture(path):
    """A deliberately false speed-proxy exclusion, plus missingness and blur controls."""
    subjects = {
        'S01': ([0.80, 0.75, 0.70, 0.65, 0.60, 0.55], 'ok', None),
        'S21': ([0.80, 0.60, 0.30, 0.05, 0.30, 0.80], 'ok', None),
        'S22': ([0.80] * 6, 'ok', None),
        'S23': ([0.80] * 6, 'blur', None),
        'S24': ([0.80] * 6, 'ok', 3),
    }
    with open(path, 'w', newline='', encoding='utf-8') as handle:
        writer = csv.writer(handle)
        writer.writerow(['participant', 'session', 'frame_idx', 't_ms',
                         'aperture_fraction', 'uncertainty_fraction', 'quality_flags'])
        for subject, (values, quality, skip) in subjects.items():
            for idx, val in enumerate(values):
                actual_idx = idx + (1 if skip is not None and idx >= skip else 0)
                writer.writerow([subject, 'Sess01', actual_idx, f'{actual_idx * 1000 / 150:.9f}',
                                 val, '0.005', quality])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--annotations', type=Path)
    parser.add_argument('--synthetic-fixture', action='store_true')
    parser.add_argument('--threshold', type=float, default=0.1)
    parser.add_argument('--clock-ms', type=float, default=0.5)
    args = parser.parse_args()
    if args.synthetic_fixture:
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            fixture = Path(d) / 'synthetic.csv'
            synthetic_fixture(fixture)
            result = analyze(load_csv(fixture), args.threshold, args.clock_ms, synthetic=True)
        assert result['counts']['falsified_joint_assumptions'] >= 1
        assert result['counts']['abstain_nuisance_or_missing'] == 2
        assert result['heldout_secant_proxy_exceedances'] >= 1
    else:
        if not args.annotations:
            parser.error('--annotations required unless --synthetic-fixture')
        result = analyze(load_csv(args.annotations), args.threshold, args.clock_ms)
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
