#!/usr/bin/env python3
"""Frozen E002-468 acquisition audit: real video diagnostics, NEVER anatomical labels."""
import argparse
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
import shutil
import statistics
import subprocess
import tempfile
import zipfile

EXPECTED_MD5 = '022dc7770d62b258ce2dd5a9a7b3df6c'
EXPECTED_NAMES = ('ME191_phantom.avi', 'ME191_phantom.xml', 'ME191_sync.csv')
MAX_UNCOMPRESSED = 700_000_000

def checksum(path, algorithm):
    digest = hashlib.new(algorithm)
    with open(path, 'rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()

def run_command(argv, timeout=150):
    return subprocess.run(argv, capture_output=True, check=True, timeout=timeout)

def extract_selected(archive, directory):
    paths = {}
    with zipfile.ZipFile(archive) as z:
        for name in EXPECTED_NAMES:
            candidates = []
            for item in z.infolist():
                path = PurePosixPath(item.filename)
                if (not item.is_dir() and path.name == name and
                    not path.is_absolute() and '..' not in path.parts and
                    item.file_size <= MAX_UNCOMPRESSED):
                    candidates.append(item)
            if len(candidates) != 1:
                raise ValueError(f'expected one safe {name}; found {len(candidates)}')
            item = candidates[0]
            target = Path(directory) / name
            with z.open(item) as source, open(target, 'wb') as sink:
                shutil.copyfileobj(source, sink, 1024 * 1024)
            if target.stat().st_size != item.file_size:
                raise ValueError('extracted size mismatch')
            paths[name] = target
    return paths

def fraction(value):
    try:
        a, b = str(value).split('/')
        result = int(a) / int(b)
        return result if math.isfinite(result) and result > 0 else None
    except (ValueError, ZeroDivisionError, AttributeError):
        return None

def pct(values, p):
    s = sorted(values)
    if not s:
        return None
    return round(s[min(len(s)-1, math.ceil(p * len(s))-1)], 6)

def inspect_video(video):
    stream_data = json.loads(run_command(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
        '-show_entries', 'stream=codec_name,width,height,r_frame_rate,avg_frame_rate,nb_frames,duration',
        '-of', 'json', str(video)]).stdout)
    streams = stream_data.get('streams', [])
    if len(streams) != 1:
        raise ValueError('expected one video stream')
    stream = streams[0]
    fps = fraction(stream.get('avg_frame_rate'))
    if fps is None:
        raise ValueError('invalid declared video frame rate')
    pts_data = json.loads(run_command(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
        '-read_intervals', '%+#120', '-show_entries', 'frame=best_effort_timestamp_time',
        '-of', 'json', str(video)]).stdout)
    timestamps = []
    missing_pts = 0
    for frame in pts_data.get('frames', []):
        try:
            t = float(frame['best_effort_timestamp_time'])
            if not math.isfinite(t):
                raise ValueError()
            timestamps.append(t)
        except (KeyError, TypeError, ValueError):
            missing_pts += 1
    deltas = [b-a for a, b in zip(timestamps, timestamps[1:])]
    invalid_steps = sum(d <= 0 for d in deltas)
    decoded = run_command(['ffmpeg', '-v', 'error', '-nostdin', '-i', str(video),
        '-frames:v', '512', '-vf', 'scale=64:48,format=gray',
        '-f', 'rawvideo', 'pipe:1'], timeout=200).stdout
    pixels = 64 * 48
    if len(decoded) % pixels:
        raise ValueError('incomplete grayscale frame')
    frames = len(decoded) // pixels
    if frames < 2:
        raise ValueError('insufficient decodable frames')
    brightness = sum(decoded) / len(decoded)
    diffs = []
    for i in range(1, frames):
        left, right = decoded[(i-1)*pixels:i*pixels], decoded[i*pixels:(i+1)*pixels]
        diffs.append(sum(abs(x-y) for x, y in zip(left, right)) / pixels)
    return {
        'container_stream': {key: stream.get(key) for key in ('codec_name','width','height','r_frame_rate','avg_frame_rate','nb_frames','duration')},
        'container_avg_fps': round(fps, 6),
        'nominal_150fps_conflict': abs(fps - 150.0) / 150.0 > 0.01,
        'rehost_approximately_500fps_conflict': abs(fps - 500.0) / 500.0 > 0.01,
        'pts_first_120': {'available': len(timestamps), 'missing': missing_pts,
                          'nonpositive_steps': invalid_steps,
                          'median_step_ms': round(statistics.median(deltas)*1000, 6) if deltas else None,
                          'min_step_ms': round(min(deltas)*1000, 6) if deltas else None,
                          'max_step_ms': round(max(deltas)*1000, 6) if deltas else None},
        'decoded_signal_first_512': {'frames': frames,
                                     'mean_brightness_0_255': round(brightness, 6),
                                     'adjacent_mad_median_0_255': round(statistics.median(diffs), 6),
                                     'adjacent_mad_p95_0_255': pct(diffs, 0.95),
                                     'adjacent_mad_max_0_255': round(max(diffs), 6)}
    }

def analyze(archive, expected_md5=EXPECTED_MD5):
    if checksum(archive, 'md5') != expected_md5:
        raise ValueError('archive MD5 mismatch; acquisition not accepted')
    with tempfile.TemporaryDirectory(prefix='lucent_e002_468_') as directory:
        files = extract_selected(archive, directory)
        result = inspect_video(files['ME191_phantom.avi'])
        result.update({
            'protocol': 'E002-468-frozen-v1',
            'evidence_tier': 'independent public human video, container-level signal only',
            'source_archive_sha256': checksum(archive, 'sha256'),
            'source_component_sha256': {name.split('.')[-1]: checksum(path, 'sha256')
                                        for name, path in files.items()},
            'hardware_exposure_timing_authenticated': False,
            'anatomical_reference_authenticated': False,
            'anatomical_closure_labels': 0,
            'physical_hidden_closure_exclusion': 'ABSTAIN_UNCALIBRATED',
            'product_release_authorized': False,
            'note': 'AVI timestamps may be synthetic; image differences are not eyelid measurements.'
        })
        return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--archive', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    result = analyze(args.archive)
    Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'status':'ACQUIRED_SIGNAL_ONLY',
        'container_avg_fps':result['container_avg_fps'],
        'nominal_150fps_conflict':result['nominal_150fps_conflict'],
        'decoded_frames':result['decoded_signal_first_512']['frames'],
        'physical_release_authorized':False}, sort_keys=True))

if __name__ == '__main__':
    main()
