#!/usr/bin/env python3
"""E002-492: local-only blinded S01 image review and conservative aggregate adjudication.

No raw human imagery is uploaded by this script. No frame-index-to-time conversion.
"""
import argparse
import hashlib
import json
import math
import os
import re
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess
import tempfile
import zipfile

EXPECTED_MD5 = 'fb56109542a13aa7879778833fe4cbaa'
CANDIDATE = 5356
HALF_WIDTH = 6
N_CLIPS = 20
MAX_FRAME = 11999
FLAGS = {'GAZE', 'GLASSES', 'BLUR', 'LIGHTING', 'OCCLUSION', 'MISSING_ANATOMY',
         'POOR_GEOMETRY', 'UNREVIEWED'}


def digest(s):
    return hashlib.sha256(s.encode('ascii')).hexdigest()


def frozen_centers():
    candidates = sorted(range(HALF_WIDTH, MAX_FRAME-HALF_WIDTH+1),
                        key=lambda i: digest(f'E002-492-control-{i}'))
    controls = []
    for i in candidates:
        if abs(i-CANDIDATE) <= 20 or any(abs(i-j) < 20 for j in controls):
            continue
        controls.append(i)
        if len(controls) == 19:
            break
    if len(controls) != 19:
        raise AssertionError('CONTROL_SELECTION_FAILED')
    centers = [CANDIDATE] + controls
    return sorted(centers, key=lambda i: digest(f'E002-492-blind-{i}'))


def build_manifest():
    centers = frozen_centers()
    return {'experiment': 'E002-492', 'subject': 'S01_CALIBRATION_ONLY',
            'camera_timing_authenticated': False, 'review_clips': [
                {'clip': f'clip_{j:02d}', 'center_native_frame': i,
                 'native_frames': list(range(i-HALF_WIDTH, i+HALF_WIDTH+1)),
                 'candidate': i == CANDIDATE}
                for j, i in enumerate(centers)]}


def template(manifest, rater):
    return {'experiment': 'E002-492', 'rater': rater,
            'clips': {c['clip']: [
                {'frame': j, 'upper_y': None, 'lower_y': None,
                 'iris_diameter': None, 'uncertainty_px': None,
                 'flags': ['UNREVIEWED']}
                for j in range(13)] for c in manifest['review_clips']}}


def md5_file(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()


def safe_member(info):
    p = PurePosixPath(info.filename)
    mode = info.external_attr >> 16
    return (not p.is_absolute() and '..' not in p.parts
            and not re.match(r'^[A-Za-z]:', info.filename)
            and '\\' not in info.filename and '\x00' not in info.filename
            and not stat.S_ISLNK(mode))


def extract_frames_local_only(archive, outdir, manifest):
    if not shutil.which('ffmpeg'):
        raise RuntimeError('FFMPEG_MISSING')
    if Path(archive).stat().st_size > 600_000_000 or md5_file(archive) != EXPECTED_MD5:
        raise ValueError('ARCHIVE_SIZE_OR_CHECKSUM_MISMATCH')
    with zipfile.ZipFile(archive) as z:
        infos = z.infolist()
        if not all(safe_member(i) for i in infos):
            raise ValueError('UNSAFE_ARCHIVE')
        vids = sorted((i for i in infos if i.filename.lower().endswith('_phantom.avi')),
                      key=lambda i: i.filename)
        if not vids or vids[0].file_size > 1_000_000_000:
            raise ValueError('MISSING_OR_OVERSIZE_VIDEO')
        with tempfile.TemporaryDirectory(prefix='lucent492_') as td:
            video = Path(td) / 'source.avi'
            with z.open(vids[0]) as src, video.open('wb') as dst:
                shutil.copyfileobj(src, dst, 1024*1024)
            if video.stat().st_size != vids[0].file_size:
                raise ValueError('TRUNCATED_VIDEO')
            # Native frame order, no resampling, no camera-clock inference.
            ranges = sorted((c['native_frames'][0], c['native_frames'][-1])
                            for c in manifest['review_clips'])
            select = '+'.join(f'between(n\\,{a}\\,{b})' for a, b in ranges)
            image_dir = Path(outdir) / 'PRIVATE_FRAMES_DO_NOT_UPLOAD'
            image_dir.mkdir(mode=0o700)
            cmd = ['ffmpeg', '-nostdin', '-hide_banner', '-loglevel', 'error',
                   '-i', str(video), '-vf', f'select={select}', '-fps_mode', 'passthrough',
                   str(image_dir / 'frame_%04d.png')]
            subprocess.run(cmd, check=True, timeout=900, stdout=subprocess.DEVNULL)
            files = sorted(image_dir.glob('frame_*.png'))
            if len(files) != 260:
                raise ValueError(f'EXPECTED_260_FRAMES_GOT_{len(files)}')
            for image in files:
                with image.open('rb') as f:
                    header = f.read(24)
                if (header[:8] != b'\x89PNG\r\n\x1a\n' or
                    int.from_bytes(header[16:20], 'big') != 320 or
                    int.from_bytes(header[20:24], 'big') != 288):
                    raise ValueError('UNEXPECTED_NATIVE_FRAME_GEOMETRY')
            ordered = sorted((frame, clip['clip'], j)
                             for clip in manifest['review_clips']
                             for j, frame in enumerate(clip['native_frames']))
            for image, (_, clip, j) in zip(files, ordered):
                dest = image_dir / f'{clip}_frame_{j:02d}.png'
                image.rename(dest)
            # No source indices or candidate status in image filenames.


def make_packet(outdir, archive=None):
    outdir = Path(outdir)
    if outdir.exists() and any(outdir.iterdir()):
        raise ValueError('OUTPUT_DIRECTORY_MUST_BE_EMPTY')
    outdir.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(outdir, 0o700)
    manifest = build_manifest()
    (outdir / 'OWNER_ONLY_MAPPING.json').write_text(json.dumps(manifest, indent=2)+'\n')
    for r in ('A', 'B'):
        (outdir / f'RATER_{r}_TEMPLATE.json').write_text(json.dumps(template(manifest,r),indent=2)+'\n')
    (outdir / 'READ_ME_PRIVATE.txt').write_text(
        'S01 calibration only. Do not upload frames or annotations to GitHub.\n'
        'Keep OWNER_ONLY_MAPPING.json hidden from raters. Share only clip_XX frames\n'
        'and one rater template per independent rater. Annotate frame positions 0..12.\n'
        'upper_y/lower_y at fixed native x=160 (E002-499), iris_diameter from an open\n'
        'reference frame, and conservative uncertainty_px per landmark. Use flags\n'
        'or UNREVIEWED when anatomy is not reliably visible. No fps assumptions.\n')
    if archive is not None:
        extract_frames_local_only(archive, outdir, manifest)
    return manifest


def validate_frame(f, frame_index):
    if not isinstance(f, dict) or f.get('frame') != frame_index:
        raise ValueError('INVALID_FRAME_INDEX')
    flags = f.get('flags')
    if not isinstance(flags, list) or any(x not in FLAGS for x in flags) or len(flags) != len(set(flags)):
        raise ValueError('INVALID_FLAGS')
    if flags:
        return None, 'UNREVIEWED' if 'UNREVIEWED' in flags else 'NUISANCE'
    fields = ('upper_y','lower_y','iris_diameter','uncertainty_px')
    vals = [f.get(k) for k in fields]
    if any(isinstance(v, bool) or not isinstance(v, (int,float)) or not math.isfinite(v) for v in vals):
        return None, 'MISSING_GEOMETRY'
    u, l, d, e = vals
    if not (0 <= u <= l <= 288 and 0 < d <= 288 and 0 <= e <= 30):
        return None, 'INVALID_GEOMETRY'
    return (max(0., (l-u-2*e)/d), (l-u+2*e)/d, (l-u)/d), None


def quantile(values, q):
    if not values:
        return None
    a = sorted(values)
    return round(a[int((len(a)-1)*q)], 6)


def adjudicate(manifest, a, b):
    expected = {c['clip'] for c in manifest['review_clips']}
    if a.get('rater') == b.get('rater') or {a.get('rater'),b.get('rater')} != {'A','B'}:
        raise ValueError('RATERS_NOT_INDEPENDENT_IDENTITIES')
    if a.get('experiment') != 'E002-492' or b.get('experiment') != 'E002-492':
        raise ValueError('WRONG_EXPERIMENT')
    if set(a.get('clips',{})) != expected or set(b.get('clips',{})) != expected:
        raise ValueError('CLIP_SET_MISMATCH')
    count = {'total_review_positions': 260, 'dual_measurable': 0,
             'dual_reviewed': 0, 'interval_disagreement': 0,
             'unreviewed': 0, 'nuisance_abstention': 0, 'geometry_abstention': 0,
             'agreement_intervals': 0}
    diffs, widths = [], []
    for clip in sorted(expected):
        fa, fb = a['clips'][clip], b['clips'][clip]
        if not isinstance(fa, list) or not isinstance(fb, list) or len(fa) != 13 or len(fb) != 13:
            raise ValueError('FRAME_SET_MISMATCH')
        for j, (x, y) in enumerate(zip(fa, fb)):
            ia, ra = validate_frame(x, j)
            ib, rb = validate_frame(y, j)
            if ra == 'UNREVIEWED' or rb == 'UNREVIEWED':
                count['unreviewed'] += 1
                continue
            count['dual_reviewed'] += 1
            if ra == 'NUISANCE' or rb == 'NUISANCE':
                count['nuisance_abstention'] += 1
            elif ra or rb:
                count['geometry_abstention'] += 1
            else:
                count['dual_measurable'] += 1
                diffs.append(abs(ia[2]-ib[2]))
                lo, hi = max(ia[0],ib[0]), min(ia[1],ib[1])
                if lo > hi:
                    count['interval_disagreement'] += 1
                else:
                    count['agreement_intervals'] += 1
                    widths.append(hi-lo)
    fraction = count['interval_disagreement']/max(1,count['dual_measurable'])
    return {'experiment':'E002-492', 'evidence_tier':'HUMAN_ANNOTATION_AGREEMENT_ONLY_IF_RATINGS_REAL',
            **count, 'disagreement_fraction_among_dual_measurable':round(fraction,6),
            'absolute_normalized_aperture_difference_median':quantile(diffs,.5),
            'absolute_normalized_aperture_difference_p90':quantile(diffs,.9),
            'agreement_interval_width_median':quantile(widths,.5),
            'falsification_disagreement_gt_20pct':fraction>.20,
            'human_reference_validated':False, 'acquisition_fps_authenticated':False,
            'physical_hidden_closure_certified':False,
            'product':'ABSTAIN_UNCALIBRATED','release':'BLOCKED'}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    sub=ap.add_subparsers(dest='mode',required=True)
    make=sub.add_parser('packet');make.add_argument('--outdir',required=True)
    make.add_argument('--archive',help='Local verified S01.zip; images never uploaded')
    review=sub.add_parser('adjudicate');review.add_argument('--manifest',required=True)
    review.add_argument('--rater-a',required=True);review.add_argument('--rater-b',required=True)
    review.add_argument('--aggregate',required=True)
    args=ap.parse_args()
    if args.mode=='packet':
        manifest=make_packet(args.outdir,args.archive)
        print(json.dumps({'experiment':'E002-492','clips':len(manifest['review_clips']),
                          'frames':260,'private_local_only':True,'anatomical_labels':0}))
    else:
        read=lambda p:json.loads(Path(p).read_text())
        result=adjudicate(read(args.manifest),read(args.rater_a),read(args.rater_b))
        Path(args.aggregate).write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
        print(json.dumps(result,sort_keys=True))

if __name__=='__main__':
    main()
