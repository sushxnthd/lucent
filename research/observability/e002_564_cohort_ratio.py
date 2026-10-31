#!/usr/bin/env python3
"""E002-564: exact literature-cohort ratio challenge, not a human speed ceiling."""
from fractions import Fraction
import json

# Source values are reported decimal point estimates, not certified error intervals.
COHORTS = (
    ('kwon2013_25', '10.1098/rsif.2013.0227', 'primary_table', 25, '243', '9.83'),
    ('sun1997_40_49_8', 'PMID:9008634', 'secondary_table_transcription', 8, '427', '11.7'),
    ('sun1997_50_59_8', 'PMID:9008634', 'secondary_table_transcription', 8, '329', '10.2'),
    ('sun1997_60_69_8', 'PMID:9008634', 'secondary_table_transcription', 8, '349', '10.6'),
)

def ratio_bound(mean_peak_speed, mean_aperture):
    v, a = Fraction(str(mean_peak_speed)), Fraction(str(mean_aperture))
    if v < 0 or a <= 0:
        raise ValueError('nonnegative speed and strictly positive aperture required')
    return v / a

def verify_pairwise_witness(speeds, apertures):
    if not speeds or len(speeds) != len(apertures):
        raise ValueError('paired, nonempty cohort required')
    vs = [Fraction(str(x)) for x in speeds]
    aa = [Fraction(str(x)) for x in apertures]
    if any(v < 0 for v in vs) or any(a <= 0 for a in aa):
        raise ValueError('invalid cohort measurement')
    bound = sum(vs) / sum(aa)
    witnesses = [i for i, (v, a) in enumerate(zip(vs, aa)) if v/a >= bound]
    if not witnesses:
        raise AssertionError('ratio lemma violated')
    return bound, witnesses

def serialize(f):
    return {'numerator': f.numerator, 'denominator': f.denominator,
            'per_second': round(float(f), 9)}

def report():
    rows = []
    for name, source, evidence, n, speed, aperture in COHORTS:
        r = ratio_bound(speed, aperture)
        conservative = r * Fraction(9, 11)  # Hypothetical systematic bias, NOT a CI.
        rows.append({'cohort': name, 'source': source, 'evidence': evidence,
                     'n': n, 'mean_peak_speed_mm_per_s': speed,
                     'mean_aperture_mm': aperture,
                     'denominator_definition': ('initial_palpebral_aperture' if evidence == 'primary_table' else 'closing_excursion_amplitude'),
                     'supports_initial_aperture_normalized_E002_371': evidence == 'primary_table',
                     'necessary_observed_speed': serialize(r),
                     'illustrative_10pct_adverse_systematic_bias': serialize(conservative)})
    prior = Fraction(243, 1) / Fraction('12.8')
    improvement = ratio_bound('243', '9.83') / prior
    return {'experiment': 'E002-564', 'evidence_tier': 'published_group_means_only',
            'lemma': 'max(v_i/a_i) >= sum(v_i)/sum(a_i), for paired nonnegative v_i and positive a_i',
            'cohorts': rows, 'prior_E002_558_bound': serialize(prior),
            'kwon2013_strengthening_factor': serialize(improvement),
            'systematic_bias_scenario_is_certified': False,
            'sun1997_primary_numeric_table_verified': False,
            'sun1997_excursion_normalization_is_not_initial_aperture': True,
            'hard_continuous_time_human_upper_bound_certified': False,
            'human_video_annotations_obtained': 0,
            'physical_shutter_captures_obtained': 0,
            'product': 'ABSTAIN_UNCALIBRATED', 'release': 'BLOCKED'}

if __name__ == '__main__':
    print(json.dumps(report(), indent=2, sort_keys=True))
