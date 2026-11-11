#!/usr/bin/env python3
"""E002-565: provenance-first wrapper around the E002-562 one-sided replay.

A source match is necessary, never sufficient for human physical validation.
"""
from e002_565_provenance_guard import adjudicate_source


def guarded_replay(prediction, witness, prediction_source, witness_source, replay_fn=None):
    """Fail closed before E002-562 candidate adjudication on cross-source inputs."""
    guard = adjudicate_source({'source': prediction_source}, {'source': witness_source})
    if not guard['source_match_only']:
        return {**guard, 'positive_witness_candidates': 0,
                'adjudication_attempted': False}
    if (not isinstance(prediction, dict) or not isinstance(witness, dict) or
        prediction.get('source_sha256') != prediction_source['video_sha256'] or
        witness.get('source_sha256') != witness_source['video_sha256']):
        return {**guard, 'status': 'REJECT_VIDEO_IDENTITY',
                'source_match_only': False, 'positive_witness_candidates': 0,
                'adjudication_attempted': False}
    # One native video digest cannot authenticate an eight-participant replay.
    # Every row and positive must refer to the same participant as the video.
    rows = prediction.get('rows')
    positives = witness.get('positives')
    if (not isinstance(rows, list) or not rows or
        not isinstance(positives, list) or
        any(not isinstance(row, dict) or row.get('participant_id') != prediction_source['participant_id'] for row in rows) or
        any(not isinstance(x, dict) or x.get('participant_id') != witness_source['participant_id'] for x in positives)):
        return {**guard, 'status': 'REJECT_SAMPLE_NAMESPACE',
                'source_match_only': False, 'positive_witness_candidates': 0,
                'adjudication_attempted': False}
    if replay_fn is None:
        from e002_562_replay import adjudicate as replay_fn
    result = replay_fn(prediction, witness)
    return {**guard, 'adjudication_attempted': True,
            'positive_witness_candidates': result['positive_witness_candidates'],
            'heldout_participants': result['heldout_participants'],
            'reference_negative_evidence': 'CENSORED',
            'physical_validation': False, 'product': 'ABSTAIN_UNCALIBRATED',
            'release': 'BLOCKED'}
