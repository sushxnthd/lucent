#!/usr/bin/env python3
"""E002-575: private, source-bound native-geometry LPW reviewer packets.

No download, face recognition, physiological inference, or network transfer.
Never publish generated packets: they contain human eye-region images.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import tempfile
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path

CLIP = re.compile(r'^clip_[0-9]{4}$')
HEX = re.compile(r'^[0-9a-f]{64}$')
PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'
WINDOW = 19


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def private_json(path):
    p = Path(path)
    if p.is_symlink() or not p.is_file():
        raise ValueError('UNSAFE_INPUT_FILE')
    return json.loads(p.read_text(encoding='utf-8'))


def run(command, timeout=1200):
    p = subprocess.run(command, capture_output=True, text=True, timeout=timeout,
                       check=False)
    if p.returncode:
        raise ValueError('DECODER_OR_PROBE_FAILED')
    return p.stdout


def validate_timestamps(frames):
    if not isinstance(frames, list) or not frames:
        raise ValueError('EMPTY_FRAME_STREAM')
    last = None
    dims = None
    for f in frames:
        if not isinstance(f, dict) or 'best_effort_timestamp_time' not in f:
            raise ValueError('MISSING_FRAME_TIMESTAMP')
        try:
            t = Decimal(str(f['best_effort_timestamp_time']))
        except (InvalidOperation, ValueError):
            raise ValueError('INVALID_FRAME_TIMESTAMP') from None
        if not t.is_finite() or (last is not None and t <= last):
            raise ValueError('NONMONOTONIC_FRAME_TIMESTAMP')
        last = t
        wh = (f.get('width'), f.get('height'))
        if any(type(x) is not int or x <= 0 for x in wh):
            raise ValueError('INVALID_NATIVE_DIMENSIONS')
        if dims is not None and wh != dims:
            raise ValueError('VARIABLE_NATIVE_DIMENSIONS')
        dims = wh
    return dims


def probe_video(path):
    data = json.loads(run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                           '-show_frames', '-show_entries',
                           'frame=best_effort_timestamp_time,width,height',
                           '-of', 'json', str(path)]))
    frames = data.get('frames')
    dims = validate_timestamps(frames)
    return len(frames), dims


def png_dimensions(path):
    with open(path, 'rb') as f:
        header = f.read(24)
    if len(header) != 24 or header[:8] != PNG_SIGNATURE or header[12:16] != b'IHDR':
        raise ValueError('INVALID_EXTRACTED_PNG')
    return struct.unpack('>II', header[16:24])


def validate_plan(owner, template_a, template_b):
    if not isinstance(owner, dict) or owner.get('experiment') != 'E002-574' or owner.get('evidence_tier') != 'SELECTION_PLAN_ONLY':
        raise ValueError('WRONG_SELECTION_PLAN')
    mapping = owner.get('owner_mapping')
    if not isinstance(mapping, list) or not mapping or owner.get('window_count') != len(mapping):
        raise ValueError('INVALID_OWNER_MAPPING')
    clips, windows = set(), set()
    for w in mapping:
        if not isinstance(w, dict) or not CLIP.fullmatch(str(w.get('blind_clip', ''))):
            raise ValueError('INVALID_CLIP_ID')
        clip = w['blind_clip']
        if clip in clips:
            raise ValueError('DUPLICATE_CLIP')
        clips.add(clip)
        start, frames = w.get('start_native_frame'), w.get('native_frames')
        if type(start) is not int or start < 0 or frames != list(range(start, start + WINDOW)):
            raise ValueError('INVALID_NATIVE_WINDOW')
        p, vid, digest = (w.get(k) for k in ('participant_id', 'video_id', 'video_sha256'))
        if not all(isinstance(x, str) and re.fullmatch(r'[A-Za-z0-9_-]{1,80}', x) for x in (p, vid)):
            raise ValueError('INVALID_SOURCE_ID')
        if not isinstance(digest, str) or not HEX.fullmatch(digest):
            raise ValueError('INVALID_SOURCE_HASH')
        if (p, vid, start) in windows:
            raise ValueError('DUPLICATE_WINDOW')
        windows.add((p, vid, start))
    for r, t in [('A', template_a), ('B', template_b)]:
        if not isinstance(t, dict) or set(t) != {'experiment', 'rater', 'clips'} or t['experiment'] != 'E002-574' or t['rater'] != r:
            raise ValueError('INVALID_RATER_TEMPLATE')
        if not isinstance(t['clips'], dict) or set(t['clips']) != clips:
            raise ValueError('RATER_CLIP_MISMATCH')
        for positions in t['clips'].values():
            if not isinstance(positions, list) or len(positions) != WINDOW:
                raise ValueError('INVALID_RATER_FRAME_COUNT')
            for j, pos in enumerate(positions):
                if pos != {'frame': j, 'upper_y': None, 'lower_y': None,
                           'iris_diameter': None, 'uncertainty_px': None,
                           'flags': ['UNREVIEWED']}:
                    raise ValueError('NONBLIND_OR_PREFILLED_RATER_TEMPLATE')
    return mapping


def validate_sources(sources, mapping):
    if not isinstance(sources, dict) or set(sources) != {'videos'} or not isinstance(sources['videos'], list):
        raise ValueError('INVALID_SOURCE_MANIFEST')
    needed = {(w['participant_id'], w['video_id']): w['video_sha256'] for w in mapping}
    found = {}
    for s in sources['videos']:
        if not isinstance(s, dict) or set(s) != {'participant_id', 'video_id', 'video_sha256', 'native_frame_count', 'absolute_path'}:
            raise ValueError('INVALID_SOURCE_ENTRY')
        key = (s['participant_id'], s['video_id'])
        if key in found or key not in needed or s['video_sha256'] != needed[key]:
            raise ValueError('SOURCE_NOT_BOUND_TO_PLAN')
        path = Path(s['absolute_path'])
        if (not path.is_absolute() or not path.is_file() or
                any(a.is_symlink() for a in (path, *path.parents))):
            raise ValueError('UNSAFE_SOURCE_PATH')
        if type(s['native_frame_count']) is not int or s['native_frame_count'] < WINDOW:
            raise ValueError('INVALID_DECLARED_FRAME_COUNT')
        found[key] = s
    if set(found) != set(needed):
        raise ValueError('MISSING_OR_EXTRA_SOURCE')
    return found


def check_destination(outdir):
    out = Path(outdir)
    if out.exists() or out.is_symlink() or not out.parent.is_dir():
        raise ValueError('DESTINATION_MUST_BE_NEW')
    for ancestor in (out.parent, *out.parent.parents):
        if ancestor.is_symlink() or (ancestor / '.git').exists():
            raise ValueError('REFUSE_REPOSITORY_OR_SYMLINK_OUTPUT')
    return out


def extract_selected(video, indices, dest, dimensions):
    # All selected positions are native decoded-frame indices; no scaling or cropping.
    # select(n) uses the same decoder-order index as ffprobe -show_frames.
    expr = '+'.join(f'between(n\,{lo}\,{hi})' for lo, hi in indices)
    dest.mkdir(mode=0o700)
    run(['ffmpeg', '-nostdin', '-hide_banner', '-loglevel', 'error', '-y',
         '-noautorotate', '-i', str(video), '-map', '0:v:0', '-an', '-sn', '-dn',
         '-map_metadata', '-1', '-vf', f'select={expr}', '-fps_mode', 'passthrough',
         '-start_number', '0', str(dest / 'selected_%06d.png')])
    files = sorted(dest.glob('selected_*.png'))
    expected = sum(hi - lo + 1 for lo, hi in indices)
    if len(files) != expected:
        raise ValueError('EXTRACTED_FRAME_COUNT_MISMATCH')
    for f in files:
        if png_dimensions(f) != dimensions:
            raise ValueError('EXTRACTED_GEOMETRY_MISMATCH')
        f.chmod(0o600)
    return files


def build_packet(owner, sources, template_a, template_b, outdir):
    mapping = validate_plan(owner, template_a, template_b)
    found = validate_sources(sources, mapping)
    out = check_destination(outdir)
    tmp = Path(tempfile.mkdtemp(prefix='.e002_575_staging_', dir=str(out.parent)))
    os.chmod(tmp, 0o700)
    try:
        raters = {}
        for r, template in [('A', template_a), ('B', template_b)]:
            root = tmp / f'RATER_{r}'
            root.mkdir(mode=0o700)
            (root / 'clips').mkdir(mode=0o700)
            tpath = root / 'BLANK_ANATOMICAL_RATINGS.json'
            tpath.write_text(json.dumps(template, indent=2, sort_keys=True) + '\n', encoding='utf-8')
            tpath.chmod(0o600)
            raters[r] = root
        by_video = defaultdict(list)
        for w in mapping:
            by_video[(w['participant_id'], w['video_id'])].append(w)
        owner_audit = {'experiment': 'E002-575', 'evidence_tier': 'SOURCE_BOUND_NATIVE_FRAME_PACKET_ONLY',
                       'timing_authenticated': False, 'physiological_labels': 0,
                       'human_rater_pairs': 0, 'videos': [], 'frames': []}
        work = tmp / '_STAGING_ONLY'
        work.mkdir(mode=0o700)
        for key in sorted(by_video):
            s = found[key]
            path = Path(s['absolute_path'])
            if sha256(path) != s['video_sha256']:
                raise ValueError('SOURCE_SHA256_MISMATCH')
            n, dims = probe_video(path)
            if n != s['native_frame_count']:
                raise ValueError('NATIVE_FRAME_COUNT_MISMATCH')
            ws = sorted(by_video[key], key=lambda w: w['start_native_frame'])
            ranges = [(w['start_native_frame'], w['start_native_frame'] + WINDOW - 1) for w in ws]
            if any(hi >= n for lo, hi in ranges) or any(ranges[i][0] <= ranges[i-1][1] for i in range(1, len(ranges))):
                raise ValueError('OVERLAPPING_OR_OUT_OF_RANGE_WINDOWS')
            extracted = extract_selected(path, ranges, work / f'video_{len(owner_audit["videos"]):04d}', dims)
            if sha256(path) != s['video_sha256']:
                raise ValueError('SOURCE_CHANGED_DURING_DECODE')
            owner_audit['videos'].append({'participant_id': key[0], 'video_id': key[1],
                                          'video_sha256': s['video_sha256'],
                                          'decoded_frames': n, 'native_width': dims[0], 'native_height': dims[1],
                                          'timestamp_check': 'STRICTLY_MONOTONIC_CONTAINER_PTS_ONLY'})
            k = 0
            for w in ws:
                for r in ('A', 'B'):
                    (raters[r] / 'clips' / w['blind_clip']).mkdir(mode=0o700)
                for j in range(WINDOW):
                    src = extracted[k]; k += 1
                    frame_name = f'frame_{j:02d}.png'
                    digest = sha256(src)
                    for r in ('A', 'B'):
                        dst = raters[r] / 'clips' / w['blind_clip'] / frame_name
                        shutil.copyfile(src, dst)
                        dst.chmod(0o600)
                    owner_audit['frames'].append({'blind_clip': w['blind_clip'],
                                                  'participant_id': key[0], 'video_id': key[1],
                                                  'native_frame_index': w['start_native_frame'] + j,
                                                  'frame_in_clip': j, 'decoded_png_sha256': digest})
        shutil.rmtree(work)
        for r in ('A', 'B'):
            manifest = {'experiment': 'E002-575', 'rater': r,
                        'evidence_tier': 'NATIVE_DECODED_FRAME_IMAGES_NOT_PHYSICAL_SHUTTER_REFERENCE',
                        'clip_count': len(mapping), 'frames_per_clip': WINDOW,
                        'human_annotations': 0, 'camera_clock_authenticated': False}
            p = raters[r] / 'PACKET_MANIFEST.json'
            p.write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n', encoding='utf-8')
            p.chmod(0o600)
        audit = tmp / 'OWNER_ONLY_SOURCE_AUDIT.json'
        audit.write_text(json.dumps(owner_audit, indent=2, sort_keys=True) + '\n', encoding='utf-8')
        audit.chmod(0o600)
        tmp.rename(out)
        return {'experiment': 'E002-575', 'status': 'PRIVATE_PACKETS_READY_NOT_HUMAN_VALIDATED',
                'clips': len(mapping), 'frames_per_reviewer': WINDOW * len(mapping),
                'independent_human_rater_pairs': 0, 'physical_camera_certified': False,
                'product': 'ABSTAIN_UNCALIBRATED', 'release': 'BLOCKED'}
    except BaseException:
        shutil.rmtree(tmp, ignore_errors=True)
        raise


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for flag in ('owner', 'sources', 'rater-a', 'rater-b', 'outdir'):
        ap.add_argument('--' + flag, required=True)
    a = ap.parse_args()
    try:
        print(json.dumps(build_packet(private_json(a.owner), private_json(a.sources),
                                      private_json(a.rater_a), private_json(a.rater_b), a.outdir), sort_keys=True))
    except Exception as e:
        print(json.dumps({'experiment': 'E002-575', 'status': 'FAILED_OR_ABSTAINED',
                          'error_type': type(e).__name__, 'product': 'ABSTAIN_UNCALIBRATED',
                          'release': 'BLOCKED'}))
        raise SystemExit(2)


if __name__ == '__main__':
    main()
