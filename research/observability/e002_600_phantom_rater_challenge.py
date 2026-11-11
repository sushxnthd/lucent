#!/usr/bin/env python3
"""E002-600: owner-local synthetic reviewer qualification, not human evidence.

Requires Pillow only for build. Generated PNGs, private manifest and reviewer
exports must remain off public GitHub. Does not validate a shutter law.
"""
import argparse
import hashlib
import io
import json
import math
import random
import secrets
from pathlib import Path

N_CLIPS = 10
N_FRAMES = 19
W, H = 640, 480
IRIS_PX = 100
THRESHOLD = 0.20
NUISANCE = {6: 'BRIGHTNESS', 7: 'BLUR', 8: 'OCCLUSION', 9: 'GAZE_GEOMETRY'}
PULSES = {0: (), 1: (1,), 2: (7, 8), 3: (10, 11, 12),
          4: (13, 14, 15, 16), 5: (3,), 6: (6, 7),
          7: (4,), 8: (10, 11), 9: (14, 15, 16)}

def json_write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + '\n', encoding='utf-8')

def blank_template(rater):
    return {'experiment': 'E002-574', 'rater': rater,
            'clips': {f'clip_{c:04d}': [
                {'frame': i, 'upper_y': None, 'lower_y': None,
                 'iris_diameter': None, 'uncertainty_px': None,
                 'flags': ['UNREVIEWED']} for i in range(N_FRAMES)]
                for c in range(N_CLIPS)}}

def frame_png(upper, gap, slope, kind, index, seed_rng):
    from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageChops
    im = Image.new('RGB', (W, H), (185, 146, 126))
    draw = ImageDraw.Draw(im)
    xs = list(range(W))
    top = [(x, round(upper + slope * (x - 320))) for x in xs]
    bottom = [(x, round(upper + gap + slope * (x - 320))) for x in xs]
    draw.polygon(top + list(reversed(bottom)), fill=(240, 239, 230))
    iris = Image.new('RGB', (W, H), (44, 100, 119))
    mask = Image.new('L', (W, H), 0)
    gaze_x = 320 + (20 if kind == 'GAZE_GEOMETRY' else 0)
    ImageDraw.Draw(mask).ellipse((gaze_x - 50, upper + gap/2 - 50,
                                  gaze_x + 50, upper + gap/2 + 50), fill=255)
    ap = Image.new('L', (W, H), 0)
    ImageDraw.Draw(ap).polygon(top + list(reversed(bottom)), fill=255)
    im.paste(iris, (0, 0), ImageChops.multiply(mask, ap))
    draw = ImageDraw.Draw(im)
    draw.line(top, fill=(65, 45, 42), width=2)
    draw.line(bottom, fill=(65, 45, 42), width=2)
    if kind == 'BRIGHTNESS':
        im = ImageEnhance.Brightness(im).enhance(0.65 if index % 2 else 1.30)
    elif kind == 'BLUR':
        im = im.filter(ImageFilter.GaussianBlur(radius=3.2))
    elif kind == 'OCCLUSION':
        ImageDraw.Draw(im).rectangle((260, int(upper)-10, 390, int(upper)+gap+10),
                                      fill=(38, 36, 37))
    elif kind == 'GAZE_GEOMETRY':
        ImageDraw.Draw(im).line([(50, round(upper + slope*(50-320))-8),
                                 (590, round(upper + slope*(590-320))-8)],
                                fill=(50, 49, 50), width=4)
    draw = ImageDraw.Draw(im)
    for _ in range(12):
        x, y = seed_rng.randrange(W), seed_rng.randrange(H)
        draw.point((x, y), fill=(160, 131, 117))
    out = io.BytesIO()
    im.save(out, format='PNG', optimize=False)
    return out.getvalue()

def build(output, seed):
    if output.exists() and any(output.iterdir()):
        raise ValueError('OUTPUT_DIRECTORY_NOT_EMPTY')
    rng = random.Random(int.from_bytes(hashlib.sha256(seed.encode()).digest(), 'big'))
    frames = {}
    for c in range(N_CLIPS):
        clip = f'clip_{c:04d}'
        rows = []
        for i in range(N_FRAMES):
            gap = 4 if i in PULSES[c] else 34
            upper = 190 + rng.randrange(-2, 3)
            slope = (0.0, 0.05, -0.05, 0.12, -0.12)[c % 5]
            kind = NUISANCE.get(c, 'CLEAN')
            raw = frame_png(upper, gap, slope, kind, i, rng)
            path = output / 'reviewer' / 'clips' / clip / f'frame_{i:02d}.png'
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
            rows.append({'frame': i, 'upper_at_x320': upper,
                         'lower_at_x320': upper + gap, 'slope': slope,
                         'gap_px': gap, 'clean': c not in NUISANCE,
                         'nuisance': kind, 'sha256': hashlib.sha256(raw).hexdigest()})
        frames[clip] = rows
    for r in ('A', 'B'):
        json_write(output / 'reviewer' / f'template_{r}.json', blank_template(r))
    json_write(output / 'private' / 'truth.json',
               {'experiment': 'E002-600', 'evidence_tier': 'SYNTHETIC_ONLY',
                'iris_diameter_px': IRIS_PX, 'threshold': THRESHOLD,
                'seed_sha256': hashlib.sha256(seed.encode()).hexdigest(),
                'clips': frames})
    return {'experiment': 'E002-600', 'frames': N_CLIPS*N_FRAMES,
            'native_templates': 2, 'owner_only_truth': True,
            'evidence_tier': 'SYNTHETIC_REVIEWER_INSTRUMENT_ONLY',
            'human_ratings': 0, 'physical_shutter_validation': False,
            'product': 'ABSTAIN_UNCALIBRATED', 'release': 'BLOCKED'}

def valid_row(row, i):
    if not isinstance(row, dict) or row.get('frame') != i:
        raise ValueError('INVALID_REVIEW_FRAME')
    flags = row.get('flags')
    if not isinstance(flags, list) or len(flags) > 1 or any(
        x not in ('UNREVIEWED', 'OCCLUSION', 'BLUR', 'GAZE', 'GLASSES',
                  'GEOMETRY', 'BRIGHTNESS', 'MISSING', 'OTHER') for x in flags):
        raise ValueError('INVALID_REVIEW_FLAGS')
    if flags:
        if set(row) != {'frame', 'upper_y', 'lower_y', 'iris_diameter', 'uncertainty_px', 'flags'} or any(
            row[k] is not None for k in ('upper_y','lower_y','iris_diameter','uncertainty_px')):
            raise ValueError('INVALID_ABSTENTION')
        return False
    if set(row) != {'frame', 'upper_y', 'lower_y', 'iris_diameter',
                    'uncertainty_px', 'measurement_x', 'flags'} or row['iris_diameter'] is not None:
        raise ValueError('INVALID_MEASURED_ROW')
    u,l,e,x = (row[k] for k in ('upper_y','lower_y','uncertainty_px','measurement_x'))
    if not all(type(v) in (float,int) and math.isfinite(v) for v in (u,l,e,x)) or not (
        0 <= u < l <= 480 and .5 <= e <= 50 and 0 <= x <= 639):
        raise ValueError('INVALID_REVIEW_COORDINATES')
    return True

def grade(truth, export):
    if truth.get('experiment') != 'E002-600' or truth.get('iris_diameter_px') != IRIS_PX or not isinstance(truth.get('clips'), dict):
        raise ValueError('INVALID_TRUTH')
    if (not isinstance(export, dict) or export.get('experiment') != 'E002-574'
        or export.get('rater') not in ('A', 'B') or 'arm' in export
        or not isinstance(export.get('clips'), dict)
        or set(export['clips']) != set(truth['clips'])
        or len(export['clips']) != N_CLIPS):
        raise ValueError('INVALID_REVIEW_EXPORT')
    clean = measured = covered = false_closed = false_open = 0
    clean_open = clean_closed = correct_open = correct_closed = ambiguous_measured = 0
    nuisance = abstained_nuisance = 0
    for clip, ground_rows in truth['clips'].items():
        rows = export['clips'][clip]
        if not isinstance(rows, list) or len(rows) != N_FRAMES or len(ground_rows) != N_FRAMES:
            raise ValueError('INVALID_FRAME_COUNT')
        for i, (r, g) in enumerate(zip(rows, ground_rows)):
            is_measured = valid_row(r, i)
            if not g['clean']:
                nuisance += 1
                abstained_nuisance += int(not is_measured)
                continue
            clean += 1
            truth_closed = g['gap_px'] <= THRESHOLD * IRIS_PX
            clean_closed += int(truth_closed)
            clean_open += int(not truth_closed)
            if not is_measured:
                continue
            measured += 1
            x = r['measurement_x']
            u_true = g['upper_at_x320'] + g['slope']*(x-320)
            l_true = g['lower_at_x320'] + g['slope']*(x-320)
            true_gap = l_true-u_true
            observed = r['lower_y']-r['upper_y']
            e = r['uncertainty_px']
            lo, hi = max(0, observed-2*e), observed+2*e
            covered += int(lo-1e-9 <= true_gap <= hi+1e-9)
            pred = 'CLOSED' if hi/IRIS_PX <= THRESHOLD else (
                'OPEN' if lo/IRIS_PX > THRESHOLD else 'ABSTAIN')
            if true_gap > THRESHOLD*IRIS_PX and pred == 'CLOSED': false_closed += 1
            if true_gap <= THRESHOLD*IRIS_PX and pred == 'OPEN': false_open += 1
            if pred == 'ABSTAIN':
                ambiguous_measured += 1
            elif pred == 'OPEN' and not truth_closed:
                correct_open += 1
            elif pred == 'CLOSED' and truth_closed:
                correct_closed += 1
    qualified = (measured*100 >= 80*clean and covered*100 >= 95*measured
                 and false_closed <= 1 and false_open <= 1
                 and clean_open > 0 and clean_closed > 0 and nuisance > 0
                 and correct_open*100 >= 80*clean_open
                 and correct_closed*100 >= 80*clean_closed
                 and abstained_nuisance*100 >= 75*nuisance)
    return {'experiment': 'E002-600', 'rater': export['rater'],
            'clean_frames': clean, 'clean_measured': measured,
            'clean_interval_covered': covered,
            'clean_open_frames': clean_open, 'clean_closed_frames': clean_closed,
            'correct_decisive_open': correct_open, 'correct_decisive_closed': correct_closed,
            'ambiguous_measured': ambiguous_measured,
            'clean_false_closed': false_closed, 'clean_false_open': false_open,
            'nuisance_frames': nuisance, 'nuisance_abstentions': abstained_nuisance,
            'qualified_on_synthetic_challenge': qualified,
            'human_validation_of_E002_371': False,
            'evidence_tier': 'SYNTHETIC_REVIEWER_QUALIFICATION_ONLY',
            'product': 'ABSTAIN_UNCALIBRATED', 'release': 'BLOCKED'}

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest='cmd', required=True)
    b = sub.add_parser('build'); b.add_argument('--output', type=Path, required=True)
    b.add_argument('--seed', help='Owner-only seed. If omitted, fresh random seed is used.')
    g = sub.add_parser('grade'); g.add_argument('--truth', type=Path, required=True)
    g.add_argument('--review', type=Path, required=True)
    args = ap.parse_args()
    try:
        if args.cmd == 'build':
            result = build(args.output, args.seed or secrets.token_hex(24))
        else:
            result = grade(json.loads(args.truth.read_text()), json.loads(args.review.read_text()))
        print(json.dumps(result, sort_keys=True))
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as e:
        print(json.dumps({'experiment':'E002-600','status':'ABSTAIN',
                          'error_type':type(e).__name__, 'release':'BLOCKED'}))
        raise SystemExit(2)

if __name__ == '__main__':
    main()
