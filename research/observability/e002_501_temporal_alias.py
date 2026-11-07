#!/usr/bin/env python3
"""E002-501: authentic S01 frame-sampling optical alias test; never anatomical labels."""
import argparse
import json
from pathlib import Path
import sys
import tempfile
import zipfile
import shutil

import numpy as np

from e002_491_calibration_motion import read_frames, MAX_FRAMES
from e002_492_anatomical_review import EXPECTED_MD5, md5_file, safe_member

N = 64
STARTS = np.arange(0, MAX_FRAMES - 5, 5, dtype=np.int32)
CENTER = np.zeros((N, N), dtype=bool)
CENTER[16:48, 16:48] = True
BORDER = np.ones((N, N), dtype=bool)
BORDER[8:56, 8:56] = False
CONDITIONS = ('baseline', 'brightness_plus8', 'blur_3x3', 'alternating_jitter_1px')


def transform(frames, condition):
    if condition == 'baseline':
        return frames
    if condition == 'brightness_plus8':
        return np.minimum(frames.astype(np.uint16) + 8, 255).astype(np.uint8)
    if condition == 'blur_3x3':
        a = np.pad(frames.astype(np.uint16), ((0, 0), (1, 1), (1, 1)), mode='edge')
        s = sum(a[:, dy:dy+N, dx:dx+N] for dy in range(3) for dx in range(3))
        return ((s + 4) // 9).astype(np.uint8)
    if condition == 'alternating_jitter_1px':
        # Shift alternate frames left/right one pixel; replicated edge.
        cols = np.arange(N)
        shifted = np.empty_like(frames)
        for parity, shift in ((0, -1), (1, 1)):
            shifted[parity::2] = frames[parity::2][:, :, np.clip(cols-shift, 0, N-1)]
        return shifted
    raise ValueError('UNKNOWN_CONDITION')


def classify_window(window):
    """Classify 6 native grayscale frames; no timing or anatomy inference."""
    if window.shape != (6, N, N) or window.dtype != np.uint8:
        raise ValueError('INVALID_WINDOW')
    if any(np.array_equal(window[i], window[i+1]) for i in range(5)):
        return 'ABSTAIN_DUPLICATE'
    f = window.astype(np.float32)
    means = f.mean(axis=(1, 2))
    stdev = f.std(axis=(1, 2))
    if (stdev.min() < 10 or np.max(np.abs(means-means[0])) > 15 or
        np.any(stdev > 1.2 * stdev[0]) or np.any(stdev < 0.8 * stdev[0])):
        return 'ABSTAIN_PHOTOMETRIC'
    # A central excursion must not bias the global photometric offset.
    border_means = f[:, BORDER].mean(axis=1)
    residual = np.abs(f - f[0:1] - (border_means-border_means[0])[:, None, None]) / 255
    border = residual[:, BORDER].mean(axis=1)
    center = residual[:, CENTER].mean(axis=1)
    if np.max(border) > 0.020:
        return 'ABSTAIN_BORDER'
    if center[5] > 0.015:
        return 'ENDPOINT_DIFFERENT'
    if any(center[j] >= 0.035 and center[j] / (border[j]+0.01) >= 1.7
           for j in range(1, 5)):
        return 'IMAGE_ALIAS_CANDIDATE'
    return 'NO_IMAGE_ALIAS_EVIDENCE'


def screen(frames, starts=None):
    if (not isinstance(frames, np.ndarray) or frames.ndim != 3 or
        frames.shape[1:] != (N, N) or frames.dtype != np.uint8):
        raise ValueError('INVALID_FRAMES')
    if starts is None:
        starts = np.arange(0, len(frames)-5, 5)
    if any(int(s) < 0 or int(s)+6 > len(frames) for s in starts):
        raise ValueError('INVALID_WINDOW_START')
    counts = {k: 0 for k in ('ABSTAIN_DUPLICATE','ABSTAIN_PHOTOMETRIC',
                            'ABSTAIN_BORDER','ENDPOINT_DIFFERENT',
                            'IMAGE_ALIAS_CANDIDATE','NO_IMAGE_ALIAS_EVIDENCE')}
    candidate_starts = set()
    for start in starts:
        verdict = classify_window(frames[int(start):int(start)+6])
        counts[verdict] += 1
        if verdict == 'IMAGE_ALIAS_CANDIDATE':
            candidate_starts.add(int(start))
    return counts, candidate_starts


def analyze(frames):
    if frames.shape != (MAX_FRAMES, N, N) or frames.dtype != np.uint8:
        raise ValueError('EXPECTED_12000_NATIVE_FRAMES')
    results, candidates = {}, {}
    for condition in CONDITIONS:
        counts, starts = screen(transform(frames, condition), STARTS)
        results[condition] = counts
        candidates[condition] = starts
    baseline = candidates['baseline']
    differences = {}
    for condition in CONDITIONS[1:]:
        differences[condition] = {
            'baseline_candidates_lost': len(baseline-candidates[condition]),
            'new_candidates_gained': len(candidates[condition]-baseline),
        }
    survivors = set.intersection(*candidates.values())
    return {
        'experiment': 'E002-501',
        'subject': 'S01_CALIBRATION_ONLY',
        'evidence_tier': 'AUTHENTIC_HUMAN_IMAGE_SAMPLING_SURROGATE_ONLY',
        'native_frames': int(len(frames)),
        'native_window_step_intervals': 5,
        'surrogate_windows': len(STARTS),
        'condition_counts': results,
        'nuisance_candidate_differences': differences,
        'image_proxy_nuisance_survivors': len(survivors),
        'anatomical_closure_labels': 0,
        'camera_clock_authenticated': False,
        'physical_shutter_calibrated': False,
        'physical_hidden_closure_certified': False,
        'product': 'ABSTAIN_UNCALIBRATED',
        'release': 'BLOCKED',
    }


def inspect(archive):
    archive = Path(archive)
    if archive.stat().st_size > 600_000_000 or md5_file(archive) != EXPECTED_MD5:
        raise ValueError('ARCHIVE_SIZE_OR_CHECKSUM_MISMATCH')
    with zipfile.ZipFile(archive) as z:
        infos = z.infolist()
        if not all(safe_member(i) for i in infos):
            raise ValueError('UNSAFE_ARCHIVE')
        videos = sorted((i for i in infos if i.filename.lower().endswith('_phantom.avi')),
                        key=lambda i: i.filename)
        if not videos or videos[0].file_size > 1_000_000_000:
            raise ValueError('MISSING_OR_OVERSIZE_VIDEO')
        with tempfile.TemporaryDirectory(prefix='lucent501_') as td:
            video = Path(td) / 'source.avi'
            with z.open(videos[0]) as src, video.open('wb') as dst:
                shutil.copyfileobj(src, dst, 1024*1024)
            if video.stat().st_size != videos[0].file_size:
                raise ValueError('TRUNCATED_VIDEO')
            frames = np.stack([np.frombuffer(f, dtype=np.uint8).reshape(N,N)
                               for f in read_frames(video)])
            return analyze(frames)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--archive', required=True)
    p.add_argument('--output', required=True)
    args = p.parse_args()
    try:
        result = inspect(args.archive)
        rc = 0
    except Exception as e:
        result = {'experiment':'E002-501', 'status':'FAILED_OR_ABSTAINED',
                  'error_class':type(e).__name__,
                  'anatomical_closure_labels':0, 'physical_hidden_closure_certified':False,
                  'product':'ABSTAIN_UNCALIBRATED','release':'BLOCKED'}
        rc = 2
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, sort_keys=True))
    return rc


if __name__ == '__main__':
    sys.exit(main())
