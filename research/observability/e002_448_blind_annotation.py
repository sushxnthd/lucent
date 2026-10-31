#!/usr/bin/env python3
"""E002-448: offline, blinded, two-rater S19 anatomical annotation instrument.

This is a data collection/adjudication tool, NOT a physical aperture estimator.
No images, per-frame mappings or individual labels may enter public artifacts.
"""
import argparse
import hashlib
import hmac
import json
import math
import secrets
import struct
import tempfile
import zlib
from pathlib import Path

from e002_441_human_acquisition import download
from e002_444_human_optical_motion import WIDTH, HEIGHT, FIXED_WINDOW, grayscale_frames, verify_and_extract

SEED = 'lucent-e002-448-v1-frozen-20261026'
MAX_MEDIUM = 24
REPEATS = 12
FLAGS = {'occlusion_glasses', 'glare_brightness', 'motion_blur', 'off_axis_gaze',
         'ambiguous_margin', 'not_anatomical', 'other'}
POINTS = ('L', 'R', 'U', 'D')


def token(tag, value):
    return hashlib.sha256(f'{SEED}:{tag}:{value}'.encode()).hexdigest()[:24]


def select_indices(times, blind_key=None):
    blind_key = blind_key or secrets.token_hex(24)
    if len(blind_key) < 32:
        raise ValueError('blinding key too short')
    def blind(tag, value):
        return hmac.new(bytes.fromhex(blind_key), f'{tag}:{value}'.encode(), hashlib.sha256).hexdigest()[:24]
    if len(times) < FIXED_WINDOW:
        raise ValueError('insufficient candidate events')
    if any(not math.isfinite(float(x)) for x in times[:FIXED_WINDOW]):
        raise ValueError('nonfinite candidate event')
    if any(times[i] <= times[i-1] for i in range(1, FIXED_WINDOW)):
        raise ValueError('nonmonotone candidate event')
    medium = [i for i in range(2, FIXED_WINDOW-1)
              if .01000001 < times[i]-times[i-1] <= .10000001][:MAX_MEDIUM]
    if not medium:
        raise ValueError('no candidate 10-100ms gaps; no positive stratum')
    short = [i for i in range(2, FIXED_WINDOW-1)
             if times[i]-times[i-1] <= .01000001 and i not in medium]
    if len(short) < len(medium):
        raise ValueError('insufficient short-gap controls')
    controls = sorted(short, key=lambda i: token('control', i))[:len(medium)]
    chosen = sorted(set(k for i in medium + controls for k in (i-2, i-1, i)))
    repeats = sorted(chosen, key=lambda i: token('repeat', i))[:min(REPEATS, len(chosen))]
    views = []
    for i in chosen:
        views.append({'view_id': blind('view', f'{i}:0'), 'frame_index': i, 'repeat': False})
    for i in repeats:
        views.append({'view_id': blind('view', f'{i}:1'), 'frame_index': i, 'repeat': True})
    views.sort(key=lambda v: blind('shuffle', v['view_id']))
    if len({v['view_id'] for v in views}) != len(views):
        raise ValueError('blind ID collision')
    return {'medium_intervals': medium, 'control_intervals': controls,
            'views': views, 'unique_frame_indices': chosen, 'private_blind_key': blind_key}


def _chunk(kind, payload):
    c = kind + payload
    return struct.pack('>I', len(payload)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)


def grayscale_png(raw, width=WIDTH, height=HEIGHT):
    if len(raw) != width * height or not (1 <= width <= 8192 and 1 <= height <= 8192):
        raise ValueError('invalid grayscale image')
    scanlines = b''.join(b'\x00' + raw[y*width:(y+1)*width] for y in range(height))
    return (b'\x89PNG\r\n\x1a\n' + _chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 0, 0, 0, 0))
            + _chunk(b'IDAT', zlib.compress(scanlines, 6)) + _chunk(b'IEND', b''))


def build_pack(frames, selected, output_root):
    """Materialize offline rater pack and private key; never publish either."""
    output_root = Path(output_root)
    if output_root.exists():
        raise FileExistsError('refuse overwrite of existing private annotation pack')
    pack = output_root / 'rater_pack'
    image_dir = pack / 'frames'
    image_dir.mkdir(parents=True)
    by_index = {}
    for view in selected['views']:
        by_index.setdefault(view['frame_index'], []).append(view['view_id'])
    seen = set()
    count = 0
    for count, frame in enumerate(frames, 1):
        idx = count-1
        if idx in by_index:
            raw = frame.tobytes() if hasattr(frame, 'tobytes') else bytes(frame)
            png = grayscale_png(raw)
            for view_id in by_index[idx]:
                (image_dir / (view_id + '.png')).write_bytes(png)
            seen.add(idx)
        if count >= FIXED_WINDOW:
            break
    if count != FIXED_WINDOW or seen != set(by_index):
        raise ValueError('video truncation or selected frame not decoded')
    manifest = {'experiment': 'E002-448', 'version': 1,
                'instructions': 'Mark canthi L/R and upper/lower eyelid margin U/D or abstain. No physical interpretation.',
                'views': [{'view_id': v['view_id'], 'image': 'frames/' + v['view_id'] + '.png'}
                          for v in selected['views']]}
    (pack / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    html = Path(__file__).with_name('e002_448_rater.html')
    if not html.exists():
        raise FileNotFoundError('missing offline rater interface')
    (pack / 'rater.html').write_bytes(html.read_bytes())
    master = {'experiment': 'E002-448', 'pilot': 'S19', 'seed': SEED,
              'medium_intervals': selected['medium_intervals'],
              'control_intervals': selected['control_intervals'],
              'private_blind_key': selected['private_blind_key'],
              'views': selected['views'], 'physical_release_authorized': False}
    (output_root / 'PRIVATE_MASTER_DO_NOT_SHARE.json').write_text(json.dumps(master, indent=2) + '\n')
    return {'experiment': 'E002-448', 'pilot': 'S19',
            'candidate_medium_intervals': len(selected['medium_intervals']),
            'candidate_short_controls': len(selected['control_intervals']),
            'unique_frames': len(selected['unique_frame_indices']),
            'blinded_views': len(selected['views']),
            'hidden_repeat_views': sum(v['repeat'] for v in selected['views']),
            'human_labels_collected': 0,
            'annotation_status': 'ZERO_HUMAN_LABELS',
            'physical_timing_authenticated': False,
            'anatomical_scale_authenticated': False,
            'e002_371_physical_validation': 'NOT_ESTABLISHED',
            'physical_release_authorized': False,
            'product_claim': 'ABSTAIN_UNCALIBRATED'}


def aperture(record):
    if not isinstance(record, dict) or record.get('status') != 'valid':
        return None
    flags = record.get('flags', [])
    if not isinstance(flags, list) or any(f not in FLAGS for f in flags) or flags:
        return None
    p = record.get('points')
    if not isinstance(p, dict) or set(p) != set(POINTS):
        return None
    try:
        coords = {k: (float(p[k][0]), float(p[k][1])) for k in POINTS}
    except (TypeError, ValueError, IndexError, KeyError):
        return None
    if any(not (math.isfinite(x) and math.isfinite(y) and 0 <= x < WIDTH and 0 <= y < HEIGHT)
           for x,y in coords.values()):
        return None
    (lx,ly),(rx,ry),(ux,uy),(dx,dy) = (coords[k] for k in POINTS)
    vx,vy = rx-lx,ry-ly
    length = math.hypot(vx,vy)
    if length < 20 or vx <= 0:
        return None
    proj_u = ((ux-lx)*vx+(uy-ly)*vy)/(length*length)
    proj_d = ((dx-lx)*vx+(dy-ly)*vy)/(length*length)
    if not (.2 <= proj_u <= .8 and .2 <= proj_d <= .8 and abs(proj_u-proj_d) <= .15):
        return None
    # Normal is clockwise in pixel coordinates (positive y is down).
    a = ((dx-ux)*(-vy)+(dy-uy)*vx)/(length*length)
    if not (0 <= a <= 1.5):
        return None
    return a


def _records(document, ids):
    if not isinstance(document, dict) or not isinstance(document.get('rater_id'), str):
        raise ValueError('missing rater identity')
    if not isinstance(document.get('annotations'), list):
        raise ValueError('missing annotation array')
    out = {}
    for row in document['annotations']:
        if not isinstance(row, dict) or row.get('view_id') not in ids:
            raise ValueError('unknown view ID')
        if row['view_id'] in out:
            raise ValueError('duplicate annotation ID')
        if row.get('status') not in ('valid', 'abstain'):
            raise ValueError('unknown annotation status')
        if row['status'] == 'abstain' and not row.get('flags'):
            raise ValueError('abstention requires a reason flag')
        out[row['view_id']] = row
    return out


def adjudicate(master, r1=None, r2=None):
    if master.get('pilot') != 'S19' or master.get('experiment') != 'E002-448':
        raise ValueError('not frozen S19 master')
    views = master['views']
    ids = {v['view_id'] for v in views}
    if len(ids) != len(views):
        raise ValueError('duplicate master IDs')
    base = {'experiment': 'E002-448', 'pilot': 'S19', 'blinded_views': len(views),
            'complete_two_rater_views': 0, 'eligible_consensus_frames': 0,
            'repeat_disagreements': 0, 'between_rater_disagreements': 0,
            'eligible_candidate_pairs': 0, 'consensus_aperture_p50': None,
            'anatomical_scale_authenticated': False, 'physical_timing_authenticated': False,
            'physiological_velocity_cap_established': False,
            'e002_371_physical_validation': 'NOT_ESTABLISHED',
            'product_claim': 'ABSTAIN_UNCALIBRATED', 'physical_release_authorized': False}
    if r1 is None or r2 is None:
        return {**base, 'annotation_status': 'ZERO_HUMAN_LABELS'}
    if r1.get('rater_id') == r2.get('rater_id'):
        raise ValueError('independent rater identities required')
    a1,a2 = _records(r1,ids),_records(r2,ids)
    base['complete_two_rater_views'] = len(set(a1) & set(a2))
    values = {}
    for view in views:
        vid = view['view_id']
        if vid not in a1 or vid not in a2:
            continue
        p1,p2 = aperture(a1[vid]), aperture(a2[vid])
        if p1 is None or p2 is None:
            continue
        if abs(p1-p2) > .03:
            base['between_rater_disagreements'] += 1
            continue
        values[vid] = (p1+p2)/2
    by_index = {}
    for view in views:
        by_index.setdefault(view['frame_index'], []).append(view['view_id'])
    accepted = {}
    for idx, view_ids in by_index.items():
        val = [values[v] for v in view_ids if v in values]
        if len(val) != len(view_ids):
            continue
        if max(val)-min(val) > .03:
            base['repeat_disagreements'] += 1
            continue
        accepted[idx] = sum(val)/len(val)
    base['eligible_consensus_frames'] = len(accepted)
    # Candidate event intervals are not authenticated exposure times.
    pairs = master['medium_intervals'] + master['control_intervals']
    base['eligible_candidate_pairs'] = sum(i-1 in accepted and i in accepted for i in pairs)
    if accepted:
        sorted_values = sorted(accepted.values())
        n = len(sorted_values)
        base['consensus_aperture_p50'] = (sorted_values[(n-1)//2] + sorted_values[n//2])/2
    base['annotation_status'] = 'PILOT_2D_CONSENSUS_ONLY' if accepted else 'ABSTAIN_REFERENCE_UNRESOLVED'
    return base


def main():
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers(dest='mode', required=True)
    p = subs.add_parser('prepare')
    p.add_argument('--zip', type=Path)
    p.add_argument('--output-root', type=Path, required=True)
    p.add_argument('--summary', type=Path, required=True)
    q = subs.add_parser('score')
    q.add_argument('--master', type=Path, required=True)
    q.add_argument('--rater1', type=Path)
    q.add_argument('--rater2', type=Path)
    q.add_argument('--summary', type=Path, required=True)
    args = parser.parse_args()
    if args.mode == 'prepare':
        with tempfile.TemporaryDirectory() as td:
            archive = args.zip or Path(td)/'S19.zip'
            if args.zip is None:
                download('S19',archive)
            video = Path(td)/'S19.avi'
            times = verify_and_extract(archive,video)
            selected = select_indices(times)
            result = build_pack(grayscale_frames(video), selected, args.output_root)
    else:
        master = json.loads(args.master.read_text())
        if bool(args.rater1) != bool(args.rater2):
            raise ValueError('both independent rater files required')
        r1 = json.loads(args.rater1.read_text()) if args.rater1 else None
        r2 = json.loads(args.rater2.read_text()) if args.rater2 else None
        result = adjudicate(master,r1,r2)
    args.summary.parent.mkdir(parents=True,exist_ok=True)
    args.summary.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,sort_keys=True))


if __name__ == '__main__':
    main()
