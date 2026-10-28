#!/usr/bin/env python3
"""E002-502: prepare private, blinded human-rater handoff on an authorized local machine.

Never uploads human frames, individual annotations, archive bytes or source-index map.
This is an operational human-validation instrument, not physiological evidence.
"""
import argparse
import json
import os
from pathlib import Path
import shutil

FRAME_NAMES = frozenset(f'clip_{i:02d}_frame_{j:02d}.png'
                        for i in range(20) for j in range(13))


def stage_raters(owner, target, viewer):
    """Copy only whitelisted blinded frames/templates/viewer into separate rater folders.

    The caller MUST validate the source packet and independently replay its
    checksum-pinned archive before invoking this staging function.
    """
    owner, target, viewer = Path(owner), Path(target), Path(viewer)
    if target.exists() or target.is_symlink():
        raise ValueError('REVIEWER_TARGET_MUST_NOT_EXIST')
    if viewer.is_symlink() or not viewer.is_file():
        raise ValueError('VIEWER_MISSING_OR_SYMLINK')
    images = owner / 'PRIVATE_FRAMES_DO_NOT_UPLOAD'
    if images.is_symlink() or not images.is_dir():
        raise ValueError('SOURCE_IMAGE_DIR_INVALID')
    actual = {p.name for p in images.iterdir()}
    if actual != FRAME_NAMES or any(not p.is_file() or p.is_symlink() for p in images.iterdir()):
        raise ValueError('SOURCE_FRAME_SET_INVALID')
    templates = {}
    for r in ('A', 'B'):
        t = owner / f'RATER_{r}_TEMPLATE.json'
        if t.is_symlink() or not t.is_file():
            raise ValueError('SOURCE_TEMPLATE_INVALID')
        obj = json.loads(t.read_text())
        if set(obj) != {'experiment', 'rater', 'clips'} or obj['experiment'] != 'E002-492' or obj['rater'] != r:
            raise ValueError('SOURCE_TEMPLATE_IDENTITY_INVALID')
        if set(obj['clips']) != {f'clip_{i:02d}' for i in range(20)}:
            raise ValueError('SOURCE_TEMPLATE_CLIPS_INVALID')
        for frames in obj['clips'].values():
            if not isinstance(frames, list) or len(frames) != 13:
                raise ValueError('SOURCE_TEMPLATE_FRAMES_INVALID')
            for j, f in enumerate(frames):
                if set(f) != {'frame', 'upper_y', 'lower_y', 'iris_diameter', 'uncertainty_px', 'flags'} or type(f['frame']) is not int or f['frame'] != j or f['flags'] != ['UNREVIEWED'] or any(f[k] is not None for k in ('upper_y', 'lower_y', 'iris_diameter', 'uncertainty_px')):
                    raise ValueError('SOURCE_TEMPLATE_NOT_BLANK')
        templates[r] = t
    target.mkdir(parents=True, mode=0o700)
    os.chmod(target, 0o700)
    try:
        for r in ('A', 'B'):
            folder = target / f'RATER_{r}_PRIVATE'
            folder.mkdir(mode=0o700)
            frames_dir = folder / 'PRIVATE_FRAMES_DO_NOT_UPLOAD'
            frames_dir.mkdir(mode=0o700)
            for name in sorted(FRAME_NAMES):
                dest = frames_dir / name
                shutil.copyfile(images / name, dest)
                os.chmod(dest, 0o600)
            for src, name in ((templates[r], f'RATER_{r}_TEMPLATE.json'),
                              (viewer, 'e002_497_offline_rater.html')):
                dest = folder / name
                shutil.copyfile(src, dest)
                os.chmod(dest, 0o600)
            (folder / 'READ_ME_PRIVATE.txt').write_text(
                'Private, blinded S01 calibration images. Never upload or publish.\n'
                'Open e002_497_offline_rater.html locally; select this folder\'s own\n'
                'RATER template and PRIVATE_FRAMES_DO_NOT_UPLOAD image directory.\n'
                'Review independently, export private JSON and return only to the study owner.\n'
                'Do not request the owner-only source-index/candidate mapping.\n'
                'Do not infer camera fps, blink duration, fatigue or health status.\n')
            os.chmod(folder / 'READ_ME_PRIVATE.txt', 0o600)
        # Explicit allowlist: no owner mapping, native frame indices, candidate labels,
        # archive, source paths or other files in either rater bundle.
        for r in ('A', 'B'):
            folder = target / f'RATER_{r}_PRIVATE'
            if {p.name for p in folder.iterdir()} != {
                'PRIVATE_FRAMES_DO_NOT_UPLOAD', f'RATER_{r}_TEMPLATE.json',
                'e002_497_offline_rater.html', 'READ_ME_PRIVATE.txt'}:
                raise ValueError('REVIEWER_BUNDLE_LEAK')
        return {'experiment': 'E002-502', 'status': 'PRIVATE_HANDOFF_STAGED',
                'reviewer_bundles': 2, 'blinded_frames_per_reviewer': 260,
                'human_ratings': 0, 'camera_timing_authenticated': False,
                'physical_hidden_closure_certified': False,
                'product': 'ABSTAIN_UNCALIBRATED', 'release': 'BLOCKED'}
    except BaseException:
        shutil.rmtree(target)
        raise


def prepare(archive, outdir):
    """Source-verified local packet -> independent private rater bundles."""
    from e002_492_anatomical_review import make_packet
    from e002_496_packet_integrity import validate
    from e002_500_source_replay import verify_against_source
    archive_input = Path(archive)
    if archive_input.is_symlink():
        raise ValueError('LOCAL_ARCHIVE_SYMLINK_REJECTED')
    archive, outdir = archive_input.resolve(), Path(outdir).resolve()
    if not archive.is_file():
        raise ValueError('LOCAL_ARCHIVE_REQUIRED')
    if outdir.exists():
        raise ValueError('OUTPUT_MUST_NOT_EXIST')
    if outdir == archive.parent or outdir in archive.parents:
        raise ValueError('UNSAFE_OUTPUT_LOCATION')
    if any((p / '.git').exists() for p in (outdir, *outdir.parents)):
        raise ValueError('OUTPUT_INSIDE_GIT_REPOSITORY')
    outdir.mkdir(parents=True, mode=0o700)
    os.chmod(outdir, 0o700)
    owner = outdir / 'OWNER_PRIVATE_DO_NOT_SHARE'
    make_packet(owner, archive)
    validate(owner)
    verify_against_source(owner, archive)
    return stage_raters(owner, outdir / 'REVIEWER_PACKETS',
                        Path(__file__).with_name('e002_497_offline_rater.html'))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--archive', required=True, help='Already downloaded, checksum-pinned S01.zip')
    ap.add_argument('--outdir', required=True, help='New private local directory; must not exist')
    args = ap.parse_args()
    os.umask(0o077)
    try:
        print(json.dumps(prepare(args.archive, args.outdir), sort_keys=True))
    except Exception as exc:
        # Never print private paths, source indices, archive metadata or image content.
        print(json.dumps({'experiment': 'E002-502', 'status': 'FAILED_OR_ABSTAINED',
                          'error_type': type(exc).__name__, 'human_ratings': 0,
                          'product': 'ABSTAIN_UNCALIBRATED', 'release': 'BLOCKED'}))
        raise SystemExit(2)


if __name__ == '__main__':
    main()
