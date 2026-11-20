#!/usr/bin/env python3
"""E002-489: conservative provenance guard for real AVI header metadata.

No AVI header, even one agreeing with a paper, authenticates capture timing.
This module intentionally cannot issue a physical certificate.
"""
import argparse
import json
import math
from pathlib import Path


def evaluate(header):
    main = header.get('main_header_nominal_fps')
    stream = header.get('stream_header_nominal_fps')
    frames = header.get('avi_main_header', {}).get('declared_frames')
    if not all(isinstance(x, (int, float)) and not isinstance(x, bool)
               and math.isfinite(x) and 0 < x < 1_000_000 for x in (main, stream)):
        raise ValueError('INVALID_NOMINAL_RATE')
    if not isinstance(frames, int) or isinstance(frames, bool) or frames <= 0:
        raise ValueError('INVALID_FRAME_COUNT')
    if abs(main / stream - 1) > .02:
        raise ValueError('INCONSISTENT_AVI_HEADERS')
    # Hypothetical zero-exposure gap with V=40 mm/s, b=0.3 mm, c=0.1 mm.
    # This is a dimensional illustration, NOT a human-validated speed bound.
    k_per_second = 40.0 / (2 * (0.3 - 0.1))
    scenarios = []
    for label, fps in [('avi_header_only', float(stream)),
                       ('source_paper_hypothesis', 150.0),
                       ('rehost_description_hypothesis', 500.0)]:
        ratio = k_per_second / fps
        scenarios.append({'label': label, 'hypothetical_fps': fps,
                          'hypothetical_zero_exposure_gap_ms': round(1000 / fps, 6),
                          'hypothetical_R': round(ratio, 9),
                          'hypothetical_hidden_closure_kinematically_possible': ratio >= 1})
    return {
        'protocol': 'E002-489',
        'evidence_tier': 'AUTHENTIC_ARCHIVE_HEADER_ONLY_NO_CAPTURE_CLOCK',
        'declared_frames': frames,
        'avi_header_fps': stream,
        'avi_implied_duration_seconds': round(frames / stream, 6),
        'paper_150fps_implied_duration_seconds': round(frames / 150, 6),
        'rehost_500fps_implied_duration_seconds': round(frames / 500, 6),
        'hypothetical_scenarios_not_anatomical_predictions': scenarios,
        'timing_certificate': 'ABSTAIN_UNAUTHENTICATED_CLOCK',
        'eyelid_velocity_certificate': 'ABSTAIN_UNCALIBRATED',
        'hidden_closure_exclusion': 'ABSTAIN_UNCALIBRATED',
        'blink_duration': 'ABSTAIN_UNCALIBRATED',
        'perclos': 'ABSTAIN_UNCALIBRATED',
        'fatigue': 'ABSTAIN_UNCALIBRATED',
        'medical': 'ABSTAIN_UNCALIBRATED',
        'product_release': 'BLOCKED',
        'required_independent_evidence': [
            'camera acquisition timestamps or independently calibrated clock',
            'measured shutter/exposure windows and jitter',
            'independent eyelid geometry and velocity bounds',
            'human reference annotation and nuisance calibration'],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--header-json', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    report = evaluate(json.loads(args.header_json.read_text()))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(report, sort_keys=True))


if __name__ == '__main__':
    main()
