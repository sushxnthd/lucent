#!/usr/bin/env python3
"""Independent real-FFV1 optical clock / PTS replay; synthetic images only.

No imports from E002-439. No authenticated physical camera or eyelid evidence.
"""
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

TICKS = (0, 33, 67, 100, 200, 233, 267, 300, 400, 433, 467, 500)
W, H, CELL = 64, 32, 8


def command(*args):
    return subprocess.run(args, capture_output=True, check=True, timeout=120).stdout


def frame(tick):
    # Binary payload intentionally independent of E002-439's Gray/CRC encoding.
    bits = [(tick >> (15 - i)) & 1 for i in range(16)] + [0, 1] * 8
    out = bytearray(W * H * 3)
    for i, bit in enumerate(bits):
        x0, y0 = (i % 8) * CELL, (i // 8) * CELL
        v = 224 if bit else 24
        for y in range(y0, y0 + CELL):
            for x in range(x0, x0 + CELL):
                j = (y * W + x) * 3
                out[j:j + 3] = bytes((v, v, v))
    return bytes(out)


def decode(raw):
    if len(raw) != W * H * 3:
        raise ValueError('wrong frame length')
    bits = []
    for i in range(32):
        x0, y0 = (i % 8) * CELL, (i // 8) * CELL
        values = [raw[(y * W + x) * 3] for y in range(y0 + 2, y0 + 6)
                  for x in range(x0 + 2, x0 + 6)]
        bits.append(int(sum(values) > len(values) * 124))
    if bits[16:] != [0, 1] * 8:
        raise ValueError('optical reference lost')
    return sum(b << (15 - i) for i, b in enumerate(bits[:16]))


def read_frames(path):
    raw = command('ffmpeg', '-v', 'error', '-i', str(path), '-vsync', '0',
                  '-f', 'rawvideo', '-pix_fmt', 'rgb24', 'pipe:1')
    n = W * H * 3
    if len(raw) % n:
        raise ValueError('partial decoded frame')
    return [raw[i:i + n] for i in range(0, len(raw), n)]


def pts(path):
    raw = command('ffprobe', '-v', 'error', '-select_streams', 'v:0',
                  '-show_entries', 'frame=best_effort_timestamp_time',
                  '-of', 'json', str(path))
    return [float(f['best_effort_timestamp_time']) * 1000
            for f in json.loads(raw)['frames']]


def run():
    if not shutil.which('ffmpeg') or not shutil.which('ffprobe'):
        raise RuntimeError('FFmpeg and FFprobe must be independently installed')
    with tempfile.TemporaryDirectory(prefix='e002490_') as td:
        root = Path(td)
        for i, tick in enumerate(TICKS):
            (root / f'f{i:03}.ppm').write_bytes(
                f'P6\n{W} {H}\n255\n'.encode() + frame(tick))
        expression = str(TICKS[-1])
        for i in range(len(TICKS) - 2, -1, -1):
            expression = f'if(eq(N,{i}),{TICKS[i]},{expression})'
        filt = 'settb=1/1000,setpts=' + expression.replace(',', chr(92) + ',')
        original, retimed = root / 'original.mkv', root / 'retimed.mkv'
        command('ffmpeg', '-v', 'error', '-y', '-framerate', '25', '-i',
                str(root / 'f%03d.ppm'), '-vf', filt, '-fps_mode', 'vfr', '-enc_time_base:v', '1:1000',
                '-c:v', 'ffv1', str(original))
        command('ffmpeg', '-v', 'error', '-y', '-i', str(original),
                '-vf', 'settb=1/1000,setpts=2*PTS', '-fps_mode', 'vfr', '-enc_time_base:v', '1:1000',
                '-c:v', 'ffv1', str(retimed))
        a, b = read_frames(original), read_frames(retimed)
        if len(a) != len(TICKS) or a != b:
            raise AssertionError('retime changed decoded image pixels')
        decoded = [decode(x) for x in b]
        if decoded != list(TICKS):
            raise AssertionError('independent optical ticks changed')
        pa, pb = pts(original), pts(retimed)
        if len(pa) != len(TICKS) or len(pb) != len(TICKS):
            raise AssertionError('PTS/frame count mismatch')
        if max(abs(x - t) for x, t in zip(pa, TICKS)) > 1:
            raise AssertionError('source PTS mismatch')
        if max(abs(x - 2 * t) for x, t in zip(pb, TICKS)) > 1:
            raise AssertionError('retimed PTS mismatch')
        return {
            'experiment': 'E002-490',
            'evidence_tier': 'INDEPENDENT_REAL_CODEC_SYNTHETIC_FRAMES',
            'authored_frame_count': len(TICKS),
            'decoded_optical_ticks_match_authored': True,
            'decoded_frames_identical_after_retime': True,
            'original_final_container_pts_ms': pa[-1],
            'retimed_final_container_pts_ms': pb[-1],
            'max_container_pts_shift_ms': max(abs(x - y) for x, y in zip(pa, pb)),
            'image_sha256_first': hashlib.sha256(a[0]).hexdigest(),
            'human_sequences': 0,
            'physical_shutter_calibrations': 0,
            'physical_exposure_authenticated': False,
            'product': 'ABSTAIN_UNCALIBRATED',
        }


if __name__ == '__main__':
    print(json.dumps(run(), sort_keys=True, indent=2))
