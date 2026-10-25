"""E002-435: stream-copy PTS intervention on bitstream-identical video.

Evidence: real FFmpeg/FFprobe container operation, synthetic image source only.
No physical camera, sensor clock, human subject or eyelid claim is validated.

Run: python research/observability/e002_435_media_clock.py --output /tmp/e002_435.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'instrument'))
from verify_frame_timing import probe_video  # noqa: E402


class ExperimentFailure(RuntimeError):
    """A preregistered identity or timing prediction failed."""


def run(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=45).stdout
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError) as exc:
        raise ExperimentFailure(f'command failed: {cmd!r}') from exc


def packet_hashes(path):
    """SHA256 over encoded packet payload, not container bytes or timestamps."""
    raw = run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
               '-show_packets', '-show_data_hash', 'sha256',
               '-show_entries', 'packet=pts_time,size,data_hash', '-of', 'json', str(path)])
    try:
        packets = json.loads(raw)['packets']
        digests = [p['data_hash'] for p in packets]
        times = [float(p['pts_time']) for p in packets]
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise ExperimentFailure('malformed packet hashes or packet PTS') from exc
    if not packets or any(not d.startswith('SHA256:') for d in digests):
        raise ExperimentFailure('missing packet hashes')
    return digests, times


def decoded_frame_hashes(path, width=64, height=64):
    """Independent raw RGB frame hashes, avoiding container/codec metadata."""
    cmd = ['ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:v:0',
           '-fps_mode', 'passthrough', '-pix_fmt', 'rgb24', '-f', 'rawvideo', '-']
    try:
        raw = subprocess.run(cmd, capture_output=True, check=True, timeout=45).stdout
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError) as exc:
        raise ExperimentFailure('raw decode failed') from exc
    frame_bytes = width * height * 3
    if not raw or len(raw) % frame_bytes:
        raise ExperimentFailure('unexpected raw frame shape')
    return [hashlib.sha256(raw[i:i+frame_bytes]).hexdigest()
            for i in range(0, len(raw), frame_bytes)]


def close_vectors(observed, expected, tol=0.001):
    return len(observed) == len(expected) and all(abs(a-b) <= tol for a, b in zip(observed, expected))


def evaluate_variants(baseline, variants):
    """Pure oracle: strict bitstream/pixel identity plus frozen clock transformations."""
    base_pts = baseline['pts']
    base_gaps = [b-a for a,b in zip(base_pts, base_pts[1:])]
    if len(base_pts) != 13 or not close_vectors(base_gaps, [0.04]*12):
        raise ExperimentFailure('baseline does not contain 13 frames at 25 Hz')
    if len(set(baseline['pixel_hashes'])) != 13:
        raise ExperimentFailure('source frames not distinguishable')
    out = {}
    for name, item in variants.items():
        if len(item['pts']) != len(base_pts):
            raise ExperimentFailure(f'{name}: frame count changed')
        if item['packet_hashes'] != baseline['packet_hashes']:
            raise ExperimentFailure(f'{name}: encoded packet content changed')
        if item['pixel_hashes'] != baseline['pixel_hashes']:
            raise ExperimentFailure(f'{name}: decoded pixels changed')
        if len(item['packet_pts']) != len(item['pts']):
            raise ExperimentFailure(f'{name}: packet count mismatch')
        if not close_vectors(item['packet_pts'], item['pts']):
            raise ExperimentFailure(f'{name}: packet/frame PTS disagreement')
        gaps = [b-a for a,b in zip(item['pts'], item['pts'][1:])]
        if name == 'scaled':
            passed = close_vectors(gaps, [2*x for x in base_gaps]) and item['pts'][-1]-base_pts[-1] > 0.40
        elif name == 'offset':
            passed = close_vectors(item['pts'], [x+0.8 for x in base_pts]) and close_vectors(gaps, base_gaps)
        elif name == 'identity':
            passed = close_vectors(item['pts'], base_pts)
        else:
            raise ExperimentFailure(f'unknown variant {name}')
        if not passed:
            raise ExperimentFailure(f'{name}: frozen timing prediction failed')
        if item['physical_certificate_authorized'] or item['product'] != 'ABSTAIN_UNCALIBRATED':
            raise ExperimentFailure(f'{name}: unsafe physical product authorization')
        out[name] = {
            'frame_count': len(item['pts']),
            'packet_payload_sha256_sequence_identical': True,
            'decoded_frame_sha256_sequence_identical': True,
            'pts_s': item['pts'],
            'max_abs_pts_difference_from_base_s': max(abs(a-b) for a,b in zip(item['pts'],base_pts)),
            'max_gap_s': max(gaps),
            'reported_average_fps_hz': item['reported_fps'],
            'frozen_prediction_passed': True,
        }
    return out


def experiment():
    if not shutil.which('ffmpeg') or not shutil.which('ffprobe'):
        raise ExperimentFailure('ffmpeg/ffprobe required')
    with tempfile.TemporaryDirectory(prefix='lucent-e002-435-') as td:
        folder = Path(td)
        source = folder/'base.mkv'
        source_cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
                      '-f', 'lavfi', '-i', 'testsrc2=size=64x64:rate=25:duration=0.52',
                      '-c:v', 'ffv1', str(source)]
        run(source_cmd)
        commands = {'base': source_cmd}
        paths = {}
        for name, opts in (('identity', []), ('scaled', ['-itsscale','2']), ('offset', ['-itsoffset','0.8'])):
            dest = folder/f'{name}.mkv'
            cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
                   *opts, '-i', str(source), '-map', '0:v:0', '-c:v', 'copy', str(dest)]
            run(cmd)
            commands[name] = cmd
            paths[name] = dest

        def inspect(path):
            parsed = probe_video(path)
            packets, packet_pts = packet_hashes(path)
            return {'pts': parsed['container_pts_s'], 'packet_hashes': packets,
                    'packet_pts': packet_pts, 'pixel_hashes': decoded_frame_hashes(path),
                    'reported_fps': parsed['reported_avg_frame_rate_hz'],
                    'physical_certificate_authorized': parsed['physical_certificate_authorized'],
                    'product': parsed['product']}

        baseline = inspect(source)
        variants = {k: inspect(v) for k,v in paths.items()}
        outcomes = evaluate_variants(baseline, variants)
        if baseline['physical_certificate_authorized'] or baseline['product'] != 'ABSTAIN_UNCALIBRATED':
            raise ExperimentFailure('unsafe baseline authorization')
        return {
            'experiment': 'E002-435',
            'evidence_tier': 'REAL_FFMPEG_STREAM_COPY_SYNTHETIC_VIDEO_NO_SENSOR_VALIDATION',
            'ffmpeg_version': run(['ffmpeg','-version']).splitlines()[0],
            'ffprobe_version': run(['ffprobe','-version']).splitlines()[0],
            'baseline': {'frame_count': len(baseline['pts']), 'pts_s': baseline['pts'],
                         'max_gap_s': max(b-a for a,b in zip(baseline['pts'],baseline['pts'][1:])),
                         'reported_average_fps_hz': baseline['reported_fps'],
                         'packet_sha256_sequence': baseline['packet_hashes'],
                         'pixel_sha256_sequence': baseline['pixel_hashes']},
            'variants': outcomes,
            'commands': {k:' '.join(v) for k,v in commands.items()},
            'human_sequences': 0,
            'authenticated_hardware_exposure_timing': False,
            'physical_certificate_authorized': False,
            'product': 'ABSTAIN_UNCALIBRATED',
            'frozen_predictions_passed': True,
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = experiment()
    data = json.dumps(result, sort_keys=True, indent=2, allow_nan=False)+'\n'
    if args.output:
        args.output.write_text(data, encoding='utf-8')
    else:
        print(data, end='')


if __name__ == '__main__':
    main()
