"""E002-434: audit encoded frame PTS, never infer physical sensor exposure times.

Run:
    python instrument/verify_frame_timing.py video.mkv --output timing.json
    python instrument/verify_frame_timing.py --experiment --output E002_434_INSTRUMENT_AGGREGATE.json

FFprobe reports *container presentation times*. Neither FFprobe nor a video's
reported frame rate can authenticate hardware capture, shutter or clock timing.
"""
from __future__ import annotations

import argparse
import json
import math
import shutil
import statistics
import subprocess
import tempfile
from fractions import Fraction
from pathlib import Path


class TimingError(ValueError):
    """Unusable or ambiguous container frame timing."""


def _number(value, label):
    if isinstance(value, bool) or value is None:
        raise TimingError(f"missing {label}")
    try:
        v = float(value)
    except (TypeError, ValueError, OverflowError) as e:
        raise TimingError(f"invalid {label}") from e
    if not math.isfinite(v):
        raise TimingError(f"nonfinite {label}")
    return v


def _fps(value):
    try:
        fps = float(Fraction(value)) if isinstance(value, str) else _number(value, 'reported fps')
    except (ValueError, TypeError, ZeroDivisionError, OverflowError) as e:
        raise TimingError('invalid reported fps') from e
    if not math.isfinite(fps) or fps <= 0:
        raise TimingError('invalid reported fps')
    return fps


def analyze_probe(probe):
    """Pure independent parser for FFprobe -show_frames JSON."""
    if not isinstance(probe, dict):
        raise TimingError('invalid probe JSON')
    streams = probe.get('streams')
    frames = probe.get('frames')
    if not isinstance(streams, list) or len(streams) != 1 or not isinstance(frames, list) or len(frames) < 2:
        raise TimingError('expected one selected video stream and at least two frames')
    stream = streams[0]
    if not isinstance(stream, dict) or stream.get('codec_type') not in (None, 'video'):
        raise TimingError('non-video stream')
    fps = _fps(stream.get('avg_frame_rate'))
    pts = []
    for i, frame in enumerate(frames):
        if not isinstance(frame, dict):
            raise TimingError('malformed frame')
        t = _number(frame.get('best_effort_timestamp_time'), f'frame {i} PTS')
        if t < 0 or (pts and t <= pts[-1]):
            raise TimingError('negative, duplicate or nonmonotone PTS')
        pts.append(t)
    gaps = [b-a for a,b in zip(pts,pts[1:])]
    naive = [pts[0]+i/fps for i in range(len(pts))]
    errors = [t-n for t,n in zip(pts,naive)]
    return {
        'schema': 'lucent-e002-434-container-pts-v1',
        'evidence_tier': 'ENCODED_MEDIA_INSTRUMENT_ONLY',
        'time_basis': 'CONTAINER_PRESENTATION_TIME_NOT_SENSOR_EXPOSURE_TIME',
        'reported_avg_frame_rate_hz': fps,
        'frame_count': len(pts),
        'container_pts_s': pts,
        'presentation_gaps_s': gaps,
        'max_presentation_gap_s': max(gaps),
        'median_presentation_gap_s': statistics.median(gaps),
        'max_abs_nominal_clock_error_s': max(map(abs, errors)),
        'large_presentation_intervals': [
            {'after_frame': i, 'gap_s': dt}
            for i,dt in enumerate(gaps) if dt > 1.5/fps
        ],
        'sensor_exposure_start_end_authenticated': False,
        'physical_certificate_authorized': False,
        'product': 'ABSTAIN_UNCALIBRATED',
        'limitations': (
            'Container PTS can be rewritten, shifted, duplicated, or synthesized during '
            'capture/transcoding. Long PTS gaps are not proof of sensor frame loss. '
            'No eyelid, blink, PERCLOS, fatigue or no-hidden-closure measurement is authorized.'
        ),
    }


def probe_video(path):
    if not Path(path).is_file():
        raise TimingError('video not found')
    cmd = ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
           '-show_entries', 'stream=codec_type,avg_frame_rate,r_frame_rate,time_base:frame=best_effort_timestamp_time',
           '-show_streams', '-show_frames', '-of', 'json', str(path)]
    try:
        completed = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=30)
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        raise TimingError('ffprobe unavailable or video undecodable') from e
    try:
        data = json.loads(completed.stdout)
    except json.JSONDecodeError as e:
        raise TimingError('ffprobe returned malformed JSON') from e
    return analyze_probe(data)


def _ppm(path, i):
    pixel = bytes(((i*17)%256, (i*43)%256, (i*71)%256))
    path.write_bytes(b'P6\n16 16\n255\n' + pixel*256)


def encode_fixture(folder, durations, label):
    if not shutil.which('ffmpeg') or not shutil.which('ffprobe'):
        raise TimingError('ffmpeg and ffprobe required')
    folder.mkdir(parents=True, exist_ok=True)
    frames = []
    for i in range(len(durations)):
        f = folder/f'{label}_{i:02d}.ppm'
        _ppm(f, i)
        frames.append(f)
    lines = ['ffconcat version 1.0']
    for f,d in zip(frames,durations):
        lines += [f"file '{f.as_posix()}'", f'duration {d:.6f}']
    lines.append(f"file '{frames[-1].as_posix()}'")
    manifest = folder/f'{label}.ffconcat'
    manifest.write_text('\n'.join(lines)+'\n', encoding='utf-8')
    video = folder/f'{label}.mkv'
    cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
           '-safe', '0', '-f', 'concat', '-i', str(manifest),
           '-fps_mode', 'vfr', '-enc_time_base', '1/1000', '-c:v', 'ffv1', str(video)]
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=30)
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        raise TimingError('FFmpeg fixture encoding failed') from e
    authored_pts = [0.0]
    for d in durations:
        authored_pts.append(authored_pts[-1]+d)
    return video, authored_pts, cmd


def experiment():
    vfr = [.04,.04,.04,.20,.04,.04,.12,.04,.04,.04,.04,.04]
    cfr = [.04]*len(vfr)
    with tempfile.TemporaryDirectory(prefix='lucent-e002-434-') as tmp:
        root = Path(tmp)
        results = {}
        for label, durations in (('vfr',vfr),('cfr',cfr)):
            video, authored, cmd = encode_fixture(root, durations, label)
            result = probe_video(video)
            if result['frame_count'] != len(authored):
                raise AssertionError('unexpected number of decoded frames')
            pts_error = max(abs(a-b) for a,b in zip(authored, result['container_pts_s']))
            results[label] = {
                'frame_count': result['frame_count'],
                'reported_fps_hz': result['reported_avg_frame_rate_hz'],
                'max_abs_naive_time_error_s': result['max_abs_nominal_clock_error_s'],
                'max_gap_s': result['max_presentation_gap_s'],
                'large_presentation_intervals': result['large_presentation_intervals'],
                'max_authored_vs_pts_error_s': pts_error,
                'pts_s': result['container_pts_s'],
                'authored_pts_s': authored,
                'ffmpeg_command': ' '.join(cmd),
            }
            if pts_error > .015:
                raise AssertionError(f'{label}: encoded PTS failed authored-time control')
            if result['product'] != 'ABSTAIN_UNCALIBRATED' or result['physical_certificate_authorized']:
                raise AssertionError('physical authorization safety failure')
        if results['vfr']['max_abs_naive_time_error_s'] <= .05:
            raise AssertionError('VFR primary prediction falsified')
        if results['vfr']['max_gap_s'] < .10:
            raise AssertionError('VFR long-gap control falsified')
        if results['cfr']['max_abs_naive_time_error_s'] > .01:
            raise AssertionError('CFR negative control falsified')
        return {
            'experiment':'E002-434',
            'evidence_tier':'REAL_FFMPEG_FFV1_CONTAINER_TEST_SYNTHETIC_FRAMES',
            'ffmpeg_version': subprocess.run(['ffmpeg','-version'],capture_output=True,text=True,check=True).stdout.splitlines()[0],
            'ffprobe_version': subprocess.run(['ffprobe','-version'],capture_output=True,text=True,check=True).stdout.splitlines()[0],
            'vfr':results['vfr'], 'cfr':results['cfr'],
            'primary_prediction_passed': True,
            'human_sequences':0,
            'hardware_sensor_exposure_authenticated':False,
            'physical_certificate_authorized':False,
            'product':'ABSTAIN_UNCALIBRATED',
        }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('video', nargs='?', type=Path)
    p.add_argument('--experiment', action='store_true')
    p.add_argument('--output', type=Path)
    args = p.parse_args()
    if args.experiment == bool(args.video):
        p.error('provide exactly one of VIDEO or --experiment')
    report = experiment() if args.experiment else probe_video(args.video)
    content = json.dumps(report, sort_keys=True, indent=2, allow_nan=False)+'\n'
    if args.output:
        args.output.write_text(content, encoding='utf-8')
    else:
        print(content, end='')


if __name__ == '__main__':
    main()
