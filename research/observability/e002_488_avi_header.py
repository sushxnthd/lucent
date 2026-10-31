#!/usr/bin/env python3
"""E002-488: dependency-free, metadata-only AVI header audit.

This parser deliberately does NOT infer measured frame times from AVI rate fields.
No decoded images, subject frames or anatomy are read or exported.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
import re
import stat
import struct
import sys
import zipfile

EXPECTED_MD5 = '3e8eb615d4a3415115f61dad5265ef12'
MAX_ARCHIVE_BYTES = 600_000_000
MAX_VIDEO_BYTES = 1_500_000_000
MAX_HEADER_BYTES = 8 * 1024 * 1024


def safe_member(info):
    p = PurePosixPath(info.filename)
    mode = (info.external_attr >> 16) & 0xffff
    return (not p.is_absolute() and '..' not in p.parts and not re.match(r'^[A-Za-z]:', info.filename)
            and '\\' not in info.filename and '\x00' not in info.filename and not stat.S_ISLNK(mode))


def md5_file(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def chunks(buf, start, stop):
    """Yield bounded RIFF chunks, skipping payloads without scanning them."""
    at = start
    while at + 8 <= stop and at + 8 <= len(buf):
        name, n = struct.unpack_from('<4sI', buf, at)
        payload = at + 8
        end = payload + n
        if end > stop:
            raise ValueError('RIFF_CHUNK_EXCEEDS_PARENT')
        if end > len(buf):
            if name == b'LIST' and buf[payload:payload + 4] == b'movi':
                return
            raise ValueError('RIFF_HEADER_TRUNCATED')
        yield name, payload, end
        at = end + (n & 1)


def parse_avi_header(prefix):
    if len(prefix) < 12 or prefix[:4] != b'RIFF' or prefix[8:12] != b'AVI ':
        raise ValueError('NOT_RIFF_AVI')
    riff_end = struct.unpack_from('<I', prefix, 4)[0] + 8
    avih = None
    video_streams = []
    for kind, p, end in chunks(prefix, 12, riff_end):
        if kind != b'LIST' or prefix[p:p + 4] != b'hdrl':
            continue
        for subkind, sp, se in chunks(prefix, p + 4, end):
            if subkind == b'avih':
                if se - sp < 40:
                    raise ValueError('AVI_MAIN_HEADER_SHORT')
                uspf, _, _, _, frames, _, streams, _, width, height = struct.unpack_from('<10I', prefix, sp)
                avih = {'microseconds_per_frame': uspf, 'declared_frames': frames,
                        'declared_streams': streams, 'width': width, 'height': height}
            if subkind == b'LIST' and prefix[sp:sp + 4] == b'strl':
                for typ, tp, te in chunks(prefix, sp + 4, se):
                    if typ != b'strh':
                        continue
                    if te - tp < 36:
                        raise ValueError('AVI_STREAM_HEADER_SHORT')
                    fcc, handler = struct.unpack_from('<4s4s', prefix, tp)
                    if fcc != b'vids':
                        continue
                    scale, rate, start, length = struct.unpack_from('<4I', prefix, tp + 20)
                    video_streams.append({'codec_fourcc': handler.decode('latin-1'),
                                          'scale': scale, 'rate': rate, 'start': start, 'length': length})
        break
    if not avih or not video_streams:
        raise ValueError('MISSING_AVI_VIDEO_HEADERS')
    stream = video_streams[0]
    uspf = avih['microseconds_per_frame']
    if not uspf or not stream['scale'] or not stream['rate']:
        raise ValueError('INVALID_AVI_RATE_FIELDS')
    main_rate = 1_000_000 / uspf
    stream_rate = stream['rate'] / stream['scale']
    if not all(math.isfinite(x) and 0 < x < 1e6 for x in (main_rate, stream_rate)):
        raise ValueError('INVALID_AVI_RATE_FIELDS')
    return {'avi_main_header': avih, 'avi_first_video_stream': stream,
            'main_header_nominal_fps': round(main_rate, 6),
            'stream_header_nominal_fps': round(stream_rate, 6),
            'avi_rate_fields_agree_within_2pct': abs(main_rate / stream_rate - 1) <= 0.02,
            'stream_header_matches_paper_150fps_2pct': abs(stream_rate / 150 - 1) <= 0.02,
            'stream_header_matches_rehost_500fps_2pct': abs(stream_rate / 500 - 1) <= 0.02,
            'timestamp_evidence': 'AVI_DECLARED_RATE_ONLY_NOT_INDEPENDENT_FRAME_TIMESTAMPS',
            'independent_hardware_clock_authenticated': False,
            'physical_shutter_calibrations': 0}


def inspect(path, expected_md5=EXPECTED_MD5):
    path = Path(path)
    out = {'protocol': 'E002-488', 'source_url': 'https://zenodo.org/records/18970793',
           'source_paper_doi': '10.1038/s41597-025-04861-9', 'subject': 'S24',
           'anatomical_reference_sequences_annotated': 0,
           'physical_claims': 'ABSTAIN_UNCALIBRATED', 'product_release': 'BLOCKED'}
    out['archive_bytes'] = path.stat().st_size
    if out['archive_bytes'] > MAX_ARCHIVE_BYTES:
        raise ValueError('ARCHIVE_SIZE_LIMIT')
    out['archive_md5'] = md5_file(path)
    if out['archive_md5'] != expected_md5:
        raise ValueError('CHECKSUM_MISMATCH')
    with zipfile.ZipFile(path) as z:
        infos = z.infolist()
        if not all(safe_member(i) for i in infos):
            raise ValueError('UNSAFE_ZIP_MEMBER')
        videos = sorted((i for i in infos if i.filename.lower().endswith('_phantom.avi')),
                        key=lambda i: i.filename)
        out['video_members_found'] = len(videos)
        if not videos:
            raise ValueError('NO_PHANTOM_VIDEO')
        v = videos[0]
        if v.file_size > MAX_VIDEO_BYTES:
            raise ValueError('VIDEO_SIZE_LIMIT')
        out['selected_video_member'] = v.filename
        out['selected_video_uncompressed_bytes'] = v.file_size
        with z.open(v) as stream:
            prefix = stream.read(MAX_HEADER_BYTES)
        out.update(parse_avi_header(prefix))
    out['pilot_acquisition_status'] = 'PASS_AUTHENTIC_ARCHIVE_HEADER_ONLY'
    out['evidence_tier'] = 'AUTHENTIC_ARCHIVE_UNVERIFIED_CAMERA_TIMING'
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--archive', required=True, type=Path)
    p.add_argument('--output', required=True, type=Path)
    a = p.parse_args()
    try:
        result = inspect(a.archive)
        rc = 0
    except Exception as e:
        result = {'protocol': 'E002-488', 'pilot_acquisition_status': 'FAILED_INTAKE',
                  'failure_reason': str(e)[:160], 'evidence_tier': 'NO_AUTHENTICATED_HUMAN_VIDEO',
                  'physical_claims': 'ABSTAIN_UNCALIBRATED', 'product_release': 'BLOCKED'}
        rc = 2
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(result, sort_keys=True))
    return rc

if __name__ == '__main__':
    sys.exit(main())
