#!/usr/bin/env python3
"""E002-614 private offline packet binding. Never uploads images or ratings."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import struct
from pathlib import Path

SHA = re.compile(r'^[0-9a-f]{64}$')
CLIP = re.compile(r'^[A-Za-z0-9_-]{1,100}$')

def expected(template):
    if not isinstance(template, dict) or template.get('rater') not in ('A', 'B'):
        raise ValueError('INVALID_RATER')
    native = template.get('experiment') == 'E002-574' and 'arm' not in template
    arm = template.get('experiment') == 'E002-595' and template.get('arm') in ('ARM_0','ARM_1','ARM_2')
    if not (native or arm):
        raise ValueError('INVALID_TEMPLATE_TYPE')
    clips = template.get('clips')
    if not isinstance(clips, dict) or len(clips) != 10:
        raise ValueError('INVALID_CLIPS')
    keys = []
    for clip, rows in sorted(clips.items()):
        if not CLIP.fullmatch(clip) or clip in ('__proto__', 'constructor', 'prototype'):
            raise ValueError('INVALID_CLIP_ID')
        if not isinstance(rows, list) or len(rows) != (19 if native else 6):
            raise ValueError('INVALID_FRAME_COUNT')
        for i, row in enumerate(rows):
            if not isinstance(row, dict) or row.get('frame') != i or any(row.get(x) is not None for x in ('upper_y','lower_y','iris_diameter','uncertainty_px')) or row.get('flags') != ['UNREVIEWED']:
                raise ValueError('NOT_BLANK_TEMPLATE')
            keys.append(f'{clip}::{i}')
    return keys

def packet_hash(frame_hashes):
    payload = ''.join(f'{key}\t{frame_hashes[key]}\n' for key in sorted(frame_hashes))
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()

def file_path(root, key):
    clip, frame = key.split('::')
    return root / 'clips' / clip / f'frame_{int(frame):02d}.png'

def png_digest(path):
    data = path.read_bytes()
    if not 0 < len(data) < 3_000_000 or data[:8] != b'\x89PNG\r\n\x1a\n' or data[12:16] != b'IHDR' or len(data) < 24:
        raise ValueError('INVALID_PNG_BYTES')
    if struct.unpack('>II', data[16:24]) != (640, 480):
        raise ValueError('INVALID_PNG_DIMENSIONS')
    return hashlib.sha256(data).hexdigest()

def actual_hashes(root, keys):
    if not root.is_dir():
        raise ValueError('NO_IMAGE_ROOT')
    expected_paths = {file_path(root, key).resolve() for key in keys}
    actual_paths = {p.resolve() for p in root.rglob('*.png')}
    if actual_paths != expected_paths:
        raise ValueError('MISSING_OR_EXTRA_PNG')
    return {key: png_digest(file_path(root, key)) for key in keys}

def verify(template, root):
    keys = expected(template)
    hashes = template.get('frame_sha256')
    digest = template.get('packet_sha256')
    if not isinstance(hashes, dict) or set(hashes) != set(keys) or not all(isinstance(x, str) and SHA.fullmatch(x) for x in hashes.values()):
        raise ValueError('INVALID_FRAME_HASH_MANIFEST')
    if not isinstance(digest, str) or not SHA.fullmatch(digest) or packet_hash(hashes) != digest:
        raise ValueError('INVALID_PACKET_DIGEST')
    if actual_hashes(root, keys) != hashes:
        raise ValueError('SOURCE_FRAME_SUBSTITUTION')
    return digest, keys

def bind(template, root):
    if 'frame_sha256' in template or 'packet_sha256' in template:
        raise ValueError('ALREADY_BOUND')
    keys = expected(template)
    hashes = actual_hashes(root, keys)
    out = dict(template)
    out['frame_sha256'] = hashes
    out['packet_sha256'] = packet_hash(hashes)
    return out

def audit(template, root, ratings):
    digest, keys = verify(template, root)
    if not isinstance(ratings, dict) or ratings.get('experiment') != template['experiment'] or ratings.get('rater') != template['rater'] or ratings.get('arm') != template.get('arm'):
        raise ValueError('RATER_TEMPLATE_MISMATCH')
    if ratings.get('source_integrity') != {'status':'SHA256_PACKET_MATCH', 'packet_sha256':digest}:
        raise ValueError('UNBOUND_OR_WRONG_RATER_EXPORT')
    clips = ratings.get('clips')
    if not isinstance(clips, dict) or set(clips) != set(template['clips']):
        raise ValueError('RATER_CLIPS_MISMATCH')
    for clip, rows in clips.items():
        if not isinstance(rows, list) or len(rows) != len(template['clips'][clip]) or any(not isinstance(row, dict) or row.get('frame') != i for i, row in enumerate(rows)):
            raise ValueError('RATER_FRAME_MISMATCH')
    return {'status':'SOURCE_PACKET_MATCH_ONLY', 'frames':len(keys), 'packet_sha256':digest, 'human_validation':False, 'product':'ABSTAIN_UNCALIBRATED', 'release':'BLOCKED'}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('mode', choices=('bind','verify','audit'))
    p.add_argument('--template', required=True, type=Path)
    p.add_argument('--images', required=True, type=Path)
    p.add_argument('--output', type=Path)
    p.add_argument('--ratings', type=Path)
    args = p.parse_args()
    template = json.loads(args.template.read_text(encoding='utf-8'))
    if args.mode == 'bind':
        if args.output is None:
            p.error('bind requires --output')
        result = bind(template, args.images)
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n', encoding='utf-8')
        summary = {'status':'BOUND_TEMPLATE_CREATED', 'frames':len(result['frame_sha256']), 'packet_sha256':result['packet_sha256']}
    elif args.mode == 'verify':
        digest, keys = verify(template, args.images)
        summary = {'status':'SOURCE_PACKET_MATCH_ONLY', 'frames':len(keys), 'packet_sha256':digest}
    else:
        if args.ratings is None:
            p.error('audit requires --ratings')
        summary = audit(template, args.images, json.loads(args.ratings.read_text(encoding='utf-8')))
    print(json.dumps(summary, sort_keys=True))

if __name__ == '__main__':
    main()
