#!/usr/bin/env python3
"""E002-563: privacy-preserving original Phantom AVI rate/provenance probe.

Never outputs frames, filenames, participant IDs, or anatomical inferences.
"""
import argparse
import hashlib
import json
import math
import shutil
import subprocess
import tempfile
import urllib.request
import zipfile
from fractions import Fraction
from pathlib import Path

URL = 'https://zenodo.org/records/18971758/files/S01.zip?download=1'
MD5 = 'bce89dd9fbb67e27a656623aa27927e0'
MAX_ARCHIVE = 600 * 1024 * 1024
MAX_VIDEO = 900 * 1024 * 1024


def download(url, dest, limit=MAX_ARCHIVE):
    h = hashlib.md5()
    total = 0
    req = urllib.request.Request(url, headers={'User-Agent': 'Lucent-E002-563-research-probe/1.0'})
    with urllib.request.urlopen(req, timeout=90) as response, open(dest, 'wb') as f:
        while True:
            block = response.read(1024 * 1024)
            if not block:
                break
            total += len(block)
            if total > limit:
                raise ValueError('archive size cap exceeded')
            h.update(block)
            f.write(block)
    return h.hexdigest(), total


def safe_video(archive, destination):
    with zipfile.ZipFile(archive) as z:
        matches = []
        for info in z.infolist():
            name = info.filename.replace('\\', '/')
            if (name.startswith('/') or '..' in name.split('/') or info.flag_bits & 1 or
                    (info.external_attr >> 16) & 0o170000 == 0o120000):
                raise ValueError('unsafe ZIP member')
            if name.lower().endswith('_phantom.avi') and not info.is_dir():
                if info.file_size > MAX_VIDEO or info.file_size > max(info.compress_size, 1) * 2000:
                    raise ValueError('video member size/ratio cap exceeded')
                matches.append(info)
        if not matches:
            raise ValueError('no original Phantom AVI member')
        chosen = sorted(matches, key=lambda i: i.filename)[0]
        with z.open(chosen) as src, open(destination, 'wb') as dst:
            copied = 0
            while True:
                chunk = src.read(1024 * 1024)
                if not chunk:
                    break
                copied += len(chunk)
                if copied > MAX_VIDEO:
                    raise ValueError('extracted member too large')
                dst.write(chunk)
    return copied, len(matches)


def rate(raw):
    try:
        r = Fraction(raw)
        return float(r) if r > 0 and math.isfinite(float(r)) else None
    except (TypeError, ValueError, ZeroDivisionError):
        return None


def verdict(avg, nominal):
    if avg is None or nominal is None:
        return 'UNRESOLVED_RATE'
    if abs(avg - 150) <= 1.5 and abs(nominal - 150) <= 1.5:
        return 'PAPER_RATE_COMPATIBLE_METADATA_ONLY'
    if abs(avg - 500) <= 5 and abs(nominal - 500) <= 5:
        return 'REHOST_RATE_COMPATIBLE_PAPER_CONFLICT'
    return 'UNRESOLVED_RATE'


def probe(video):
    p = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                        '-show_entries', 'stream=codec_name,avg_frame_rate,r_frame_rate,nb_frames,width,height',
                        '-of', 'json', str(video)], capture_output=True, text=True, timeout=100, check=True)
    streams = json.loads(p.stdout).get('streams', [])
    if len(streams) != 1:
        raise ValueError('missing or multiple first video streams')
    s = streams[0]
    avg, nominal = rate(s.get('avg_frame_rate')), rate(s.get('r_frame_rate'))
    d = subprocess.run(['ffmpeg', '-hide_banner', '-nostdin', '-v', 'error', '-i', str(video),
                        '-frames:v', '90', '-f', 'framemd5', '-'], capture_output=True,
                       text=True, timeout=180, check=True)
    hashes = [line.rsplit(',', 1)[-1].strip() for line in d.stdout.splitlines()
              if line and not line.startswith('#')]
    if not hashes:
        raise ValueError('decoded zero prefix frames')
    dup = sum(a == b for a, b in zip(hashes, hashes[1:]))
    return {'codec': str(s.get('codec_name', 'unknown'))[:50],
            'width': int(s.get('width', 0)), 'height': int(s.get('height', 0)),
            'avg_fps': avg, 'nominal_fps': nominal,
            'reported_frames': int(s['nb_frames']) if str(s.get('nb_frames', '')).isdigit() else None,
            'prefix_decoded_frames': len(hashes), 'prefix_exact_adjacent_duplicates': dup,
            'rate_verdict': verdict(avg, nominal)}


def analyze(archive, expected_md5=MD5):
    with open(archive, 'rb') as f:
        h = hashlib.md5()
        n = 0
        for block in iter(lambda: f.read(1024 * 1024), b''):
            n += len(block)
            if n > MAX_ARCHIVE:
                raise ValueError('archive size cap exceeded')
            h.update(block)
    if h.hexdigest() != expected_md5:
        raise ValueError('archive MD5 mismatch')
    with tempfile.TemporaryDirectory(prefix='lucent563-') as t:
        video = Path(t) / 'private.avi'
        video_size, count = safe_video(archive, video)
        report = probe(video)
    return {'experiment': 'E002-563', 'source_doi': '10.5281/zenodo.18971758',
            'archive_md5_verified': True, 'archive_bytes': n,
            'video_bytes': video_size, 'phantom_avi_members': count,
            **report, 'sensor_clock_verified': False,
            'anatomical_closure_verified': False, 'independent_raters': 0,
            'reference_negative_evidence': 'CENSORED',
            'product': 'ABSTAIN_UNCALIBRATED', 'release': 'BLOCKED'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    parser.add_argument('--local-zip', help='offline synthetic fixture only')
    parser.add_argument('--local-md5', help='MD5 for offline synthetic fixture only')
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='lucent563-archive-') as t:
        archive = Path(args.local_zip) if args.local_zip else Path(t) / 'S01.zip'
        if not args.local_zip:
            md5, size = download(URL, archive)
            if md5 != MD5:
                raise ValueError(f'archive MD5 mismatch (bytes={size})')
        elif not args.local_md5:
            raise ValueError('local fixture requires explicit MD5')
        result = analyze(archive, args.local_md5 if args.local_zip else MD5)
    Path(args.output).write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
