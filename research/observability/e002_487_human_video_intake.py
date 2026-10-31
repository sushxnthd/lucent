#!/usr/bin/env python3
"""E002-487 authentic human-eye-video metadata-only intake (no anatomical labels).

Never writes raw frames or participant videos to output. Python standard library.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile
from statistics import median

EXPECTED_MD5 = '3e8eb615d4a3415115f61dad5265ef12'
MAX_ARCHIVE_BYTES = 600_000_000
MAX_VIDEO_BYTES = 1_500_000_000
MAX_PTS = 10000


def safe_member(info):
    path = PurePosixPath(info.filename)
    mode = (info.external_attr >> 16) & 0xffff
    return (not path.is_absolute() and '..' not in path.parts
            and not re.match(r'^[A-Za-z]:', info.filename)
            and '\\' not in info.filename and '\x00' not in info.filename
            and not stat.S_ISLNK(mode))


def md5_file(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(2 ** 20), b''):
            h.update(chunk)
    return h.hexdigest()


def run_ffprobe(video, timestamps=None):
    args = ['ffprobe', '-v', 'error', '-select_streams', 'v:0']
    if timestamps == 'packet':
        args += ['-read_intervals', '%+#10000', '-show_packets',
                 '-show_entries', 'packet=pts_time', '-of', 'csv=p=0']
    elif timestamps == 'frame':
        args += ['-read_intervals', '%+#10000', '-show_frames',
                 '-show_entries', 'frame=best_effort_timestamp_time', '-of', 'csv=p=0']
    else:
        args += ['-show_entries',
                 'stream=codec_name,width,height,r_frame_rate,avg_frame_rate,time_base,nb_frames,duration',
                 '-show_streams', '-of', 'json']
    args.append(str(video))
    return subprocess.run(args, text=True, capture_output=True, timeout=180, check=True).stdout


def rate(s):
    if not s or s == '0/0':
        return None
    parts = s.split('/')
    try:
        v = float(parts[0]) / float(parts[1]) if len(parts) == 2 else float(s)
        return v if math.isfinite(v) and v > 0 else None
    except (ValueError, ZeroDivisionError):
        return None


def pts_audit(raw):
    pts = []
    invalid = 0
    for line in raw.splitlines():
        if len(pts) >= MAX_PTS:
            break
        field = line.strip().split(',')[0]
        try:
            value = float(field)
            if math.isfinite(value):
                pts.append(value)
            else:
                invalid += 1
        except ValueError:
            invalid += 1
    deltas = [b - a for a, b in zip(pts, pts[1:])]
    pos = [d for d in deltas if d > 0]
    med = median(pos) if pos else None
    return {
        'pts_observations': len(pts), 'invalid_pts_fields': invalid,
        'nonpositive_steps': sum(d <= 0 for d in deltas),
        'median_positive_delta_ms': round(1000 * med, 6) if med else None,
        'empirical_positive_pts_rate_hz': round(1 / med, 6) if med else None,
        'large_positive_gaps_gt_1_5x_median': sum(d > 1.5 * med for d in pos) if med else None,
        'pts_temporally_usable': len(pts) >= 3 and len(pos) == len(deltas) and invalid == 0,
        'pts_truncated_to_first': MAX_PTS,
        'pts_are_container_timestamps_not_external_clock': True,
    }


def inspect(path, expected_md5=EXPECTED_MD5):
    path = Path(path)
    result = {
        'protocol': 'E002-487', 'subject': 'S24',
        'evidence_tier': 'HUMAN_VIDEO_METADATA_ONLY',
        'source_url': 'https://zenodo.org/records/18970793',
        'source_paper_doi': '10.1038/s41597-025-04861-9',
        'source_rehost_date': '2026-03-12',
        'paper_claimed_fps': 150, 'rehost_claimed_approx_fps': 500,
        'anatomical_reference_sequences_annotated': 0,
        'physical_shutter_calibrations': 0,
        'physical_claims': 'ABSTAIN_UNCALIBRATED', 'product_release': 'BLOCKED',
    }
    size = path.stat().st_size
    result['archive_bytes'] = size
    if size > MAX_ARCHIVE_BYTES:
        raise ValueError('ARCHIVE_SIZE_LIMIT')
    digest = md5_file(path)
    result['archive_md5'] = digest
    if digest != expected_md5:
        raise ValueError('CHECKSUM_MISMATCH')
    with zipfile.ZipFile(path) as z:
        infos = z.infolist()
        if not all(safe_member(info) for info in infos):
            raise ValueError('UNSAFE_ZIP_MEMBER')
        videos = sorted((i for i in infos if i.filename.lower().endswith('_phantom.avi')),
                        key=lambda i: i.filename)
        result['video_members_found'] = len(videos)
        result['sync_csv_members_found'] = sum(i.filename.lower().endswith('_sync.csv') for i in infos)
        result['phantom_xml_members_found'] = sum(i.filename.lower().endswith('_phantom.xml') for i in infos)
        if not videos:
            raise ValueError('NO_PHANTOM_VIDEO')
        selected = videos[0]
        result['selected_video_member'] = selected.filename
        result['selected_video_uncompressed_bytes'] = selected.file_size
        if selected.file_size > MAX_VIDEO_BYTES:
            raise ValueError('VIDEO_SIZE_LIMIT')
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / 'selected.avi'
            with z.open(selected) as src, open(dest, 'wb') as dst:
                shutil.copyfileobj(src, dst, 2 ** 20)
            if dest.stat().st_size != selected.file_size:
                raise ValueError('VIDEO_EXTRACTION_LENGTH_MISMATCH')
            streams = json.loads(run_ffprobe(dest))['streams']
            if not streams:
                raise ValueError('FFPROBE_NO_VIDEO_STREAM')
            stream = streams[0]
            result['video_stream'] = {k: stream.get(k) for k in
                                      ('codec_name', 'width', 'height', 'r_frame_rate',
                                       'avg_frame_rate', 'time_base', 'nb_frames', 'duration')}
            header_rate = rate(stream.get('avg_frame_rate')) or rate(stream.get('r_frame_rate'))
            result['nominal_rate_hz'] = header_rate
            result['header_matches_paper_150fps_2pct'] = (abs(header_rate / 150 - 1) <= 0.02) if header_rate else False
            result['source_rate_conflict'] = not result['header_matches_paper_150fps_2pct']
            packet = pts_audit(run_ffprobe(dest, 'packet'))
            result['packet_timing'] = packet
            if packet['pts_temporally_usable']:
                timing = packet
                origin = 'container_packet_pts'
            else:
                frame = pts_audit(run_ffprobe(dest, 'frame'))
                result['decoded_frame_timing'] = frame
                timing = frame
                origin = 'decoder_best_effort_from_container'
            result['timing_source'] = origin if timing['pts_temporally_usable'] else 'none_usable'
            result['pilot_acquisition_status'] = ('PASS_ARCHIVE_VIDEO_METADATA_ONLY'
                                                   if timing['pts_temporally_usable']
                                                   else 'ABSTAIN_NO_USABLE_CONTAINER_TIMESTAMPS')
            result['independent_hardware_clock_authenticated'] = False
            result['timing_is_not_physical_exposure_calibration'] = True
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--archive', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--expected-md5', default=EXPECTED_MD5,
                   help='For local unit tests only; production CI uses the frozen S24 checksum')
    a = p.parse_args()
    try:
        out = inspect(a.archive, a.expected_md5)
        code = 0 if out['pilot_acquisition_status'] == 'PASS_ARCHIVE_VIDEO_METADATA_ONLY' else 2
    except Exception as exc:
        out = {'protocol': 'E002-487', 'pilot_acquisition_status': 'FAILED_INTAKE',
               'failure_reason': str(exc)[:200], 'evidence_tier': 'NO_AUTHENTICATED_HUMAN_VIDEO',
               'physical_claims': 'ABSTAIN_UNCALIBRATED', 'product_release': 'BLOCKED'}
        code = 2
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(out, sort_keys=True, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(out, sort_keys=True, indent=2))
    return code


if __name__ == '__main__':
    sys.exit(main())
