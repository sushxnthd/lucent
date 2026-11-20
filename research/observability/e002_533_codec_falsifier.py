"""E002-533: encoded synthetic optical patch instrument stress, not physical calibration.

Uses actual ffmpeg encoders and OpenCV decoder. All data are rendered synthetic.
Fail-closed outputs are delegated to the E002-532 evaluator.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import tempfile
from fractions import Fraction as Q
from pathlib import Path

import cv2
import numpy as np

from e002_532_optical_calibration import evaluate, synthetic_input

HEIGHT = WIDTH = 96
PATCH_X = slice(24, 72)
PATCH_YS = (slice(8, 20), slice(40, 52), slice(72, 84))
SAMPLE_X = slice(36, 60)
SAMPLE_YS = (slice(10, 18), slice(42, 50), slice(74, 82))
DARK_X = slice(3, 9)
WHITE_X = slice(87, 93)


def render(data, *, gamma=False, glare=False):
    frames = []
    for i in range(20):
        arr = np.full((HEIGHT, WIDTH, 3), 60, dtype=np.uint8)
        arr[:, :12] = 0
        arr[:, 84:] = 255
        for j, roi in enumerate(PATCH_YS):
            duty = float(Q(data['frames'][3*i+j]['brightness']))
            value = duty ** (1 / 2.2) if gamma else duty
            arr[roi, PATCH_X] = round(255 * value)
        if glare and i == 15:
            arr[PATCH_YS[1], PATCH_X] = 255
        frames.append(arr)
    return frames


def encode(frames, path, codec):
    args = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
            '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{WIDTH}x{HEIGHT}',
            '-r', '100', '-i', 'pipe:0', '-an']
    if codec == 'ffv1':
        args += ['-c:v', 'ffv1', '-pix_fmt', 'bgr0']
    elif codec == 'h264':
        args += ['-c:v', 'libx264', '-crf', '23', '-preset', 'medium',
                 '-pix_fmt', 'yuv420p', '-movflags', '+faststart']
    else:
        raise ValueError('unsupported codec')
    args += [str(path)]
    run = subprocess.run(args, input=b''.join(f.tobytes() for f in frames),
                         capture_output=True, check=False)
    if run.returncode:
        raise RuntimeError(run.stderr.decode(errors='replace'))


def decode(path):
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise RuntimeError('OpenCV cannot decode video')
    frames = []
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if frame.shape != (HEIGHT, WIDTH, 3):
            raise ValueError('unexpected decoded dimensions')
        frames.append(frame)
    cap.release()
    if len(frames) != 20:
        raise ValueError(f'expected 20 native frames; got {len(frames)}')
    return frames


def decode_independent_ffmpeg(path):
    """Separate ffmpeg raw RGB decoder, not OpenCV VideoCapture."""
    run = subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error',
                          '-i', str(path), '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                          'pipe:1'], capture_output=True, check=False)
    if run.returncode:
        raise RuntimeError(run.stderr.decode(errors='replace'))
    expected = 20 * HEIGHT * WIDTH * 3
    if len(run.stdout) != expected:
        raise ValueError('independent decoded byte count mismatch')
    return list(np.frombuffer(run.stdout, dtype=np.uint8)
                .reshape((20, HEIGHT, WIDTH, 3)))


def extract(frames, *, inverse_gamma=False):
    measurements = []
    for frame in frames:
        gray = frame.astype(np.float64).mean(axis=2)
        dark = float(np.mean(gray[20:76, DARK_X]))
        bright = float(np.mean(gray[20:76, WHITE_X]))
        if bright - dark < 150:
            raise ValueError('reference dynamic range collapsed')
        for roi in SAMPLE_YS:
            level = float(np.mean(gray[roi, SAMPLE_X]))
            normalized = min(1.0, max(0.0, (level-dark)/(bright-dark)))
            if inverse_gamma:
                normalized = normalized ** 2.2
            measurements.append(normalized)
    return measurements


def measure_case(data, codec, *, gamma=False, inverse_gamma=False, glare=False,
                 missing=False, output_dir):
    frames = render(data, gamma=gamma, glare=glare)
    suffix = '.avi' if codec == 'ffv1' else '.mp4'
    name = ('gamma' if gamma else 'linear') + ('_glare' if glare else '') + '_' + codec
    path = output_dir / (name + suffix)
    encode(frames, path, codec)
    decoded = decode(path)
    values = extract(decoded, inverse_gamma=inverse_gamma)
    independent = extract(decode_independent_ffmpeg(path), inverse_gamma=inverse_gamma)
    independent_max_delta = max(abs(a-b) for a,b in zip(values, independent))
    if independent_max_delta > Q(1, 50):
        raise ValueError('independent decoder disagrees beyond preregistered tolerance')
    candidate = copy.deepcopy(data)
    for k, (f, value) in enumerate(zip(candidate['frames'], values)):
        if missing and k == 3*15+1:
            f['valid'] = False
            del f['brightness']
        else:
            f['brightness'] = str(Q(str(value)).limit_denominator(10**9))
    result = evaluate(candidate)
    residuals = [abs(float(Q(f['brightness'])) - float(Q(original['brightness'])))
                 for f, original in zip(candidate['frames'], data['frames']) if f.get('valid',True)]
    result.update(codec=codec, gamma_rendered=gamma, inverse_gamma=inverse_gamma,
                  glare=glare, missing=missing, file_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                  bytes=path.stat().st_size,
                  independent_decoder_max_abs_delta=independent_max_delta,
                  observed_max_abs_deviation_from_truth=max(residuals),
                  evidence_tier='SYNTHETIC_OPTICAL_SCENE_REAL_CODEC_NOT_CAMERA')
    return result


def run_suite(output_dir):
    data = synthetic_input()
    cases = {
        'lossless_linear': ('ffv1', dict()),
        'h264_linear': ('h264', dict()),
        'h264_gamma_uncorrected': ('h264', dict(gamma=True)),
        'h264_gamma_corrected': ('h264', dict(gamma=True, inverse_gamma=True)),
        'h264_heldout_glare': ('h264', dict(glare=True)),
        'h264_missing_native': ('h264', dict(missing=True)),
    }
    out = {}
    for name, (codec, kwargs) in cases.items():
        out[name] = measure_case(data, codec, output_dir=output_dir, **kwargs)
    out['_environment'] = {
        'ffmpeg': subprocess.check_output(['ffmpeg','-version'], text=True).splitlines()[0],
        'opencv': cv2.__version__, 'numpy': np.__version__,
        'source': 'E002-532 frozen synthetic duty fractions',
        'physical_measurements': 0, 'human_measurements': 0,
    }
    return out


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,help='write aggregate JSON')
    p.add_argument('--retain-videos',type=Path,help='keep generated synthetic videos locally')
    args=p.parse_args()
    if args.retain_videos:
        args.retain_videos.mkdir(parents=True,exist_ok=True)
        out=run_suite(args.retain_videos)
    else:
        with tempfile.TemporaryDirectory(prefix='lucent533_') as temp:
            out=run_suite(Path(temp))
    text=json.dumps(out,sort_keys=True,indent=2)
    if args.output:
        args.output.write_text(text+'\n',encoding='utf-8')
    print(text)


if __name__=='__main__':
    main()
