#!/usr/bin/env python3
"""E002-574: preregistered LPW participant-disjoint blinded window plan.

Runs on a private local inventory; never reads or publishes human imagery.
The inventory is NOT evidence of authentic footage or acquisition timing.
"""
import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

WINDOW = 19
WINDOWS_PER_VIDEO = 10
SPLIT_SALT = 'E002-573-LPW-v1|'
WINDOW_SALT = 'E002-573-window-v1|'
ID = re.compile(r'^[A-Za-z0-9_-]{1,80}$')
HEX = re.compile(r'^[a-f0-9]{64}$')


def digest(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()


def plan(inventory):
    if not isinstance(inventory, dict) or set(inventory) != {'videos'}:
        raise ValueError('INVENTORY_SCHEMA')
    videos = inventory['videos']
    if not isinstance(videos, list) or len(videos) != 66:
        raise ValueError('EXPECTED_66_VIDEOS')
    participants, seen_videos, seen_sha = Counter(), set(), set()
    for v in videos:
        if not isinstance(v, dict) or set(v) != {'participant_id', 'video_id', 'video_sha256', 'native_frame_count'}:
            raise ValueError('VIDEO_SCHEMA')
        p, vid, sha, count = (v[k] for k in ('participant_id','video_id','video_sha256','native_frame_count'))
        if not all(isinstance(x, str) and ID.fullmatch(x) for x in (p, vid)):
            raise ValueError('UNSAFE_IDENTIFIER')
        if not isinstance(sha, str) or not HEX.fullmatch(sha):
            raise ValueError('INVALID_VIDEO_DIGEST')
        if type(count) is not int or count < WINDOW:
            raise ValueError('INVALID_FRAME_COUNT')
        if (p, vid) in seen_videos or sha in seen_sha:
            raise ValueError('DUPLICATE_VIDEO_OR_DIGEST')
        seen_videos.add((p, vid)); seen_sha.add(sha); participants[p] += 1
    if len(participants) != 22 or set(participants.values()) != {3}:
        raise ValueError('EXPECTED_22_PARTICIPANTS_THREE_VIDEOS_EACH')
    ordered = sorted(participants, key=lambda p: (digest(SPLIT_SALT + p), p))
    development, heldout = set(ordered[:11]), set(ordered[11:])
    owner = []
    for v in sorted(videos, key=lambda v: (v['participant_id'],v['video_id'])):
        p, vid, sha, n = (v[k] for k in ('participant_id','video_id','video_sha256','native_frame_count'))
        if p not in heldout:
            continue
        candidates = list(range(0, n - WINDOW + 1, WINDOW))
        chosen = sorted(candidates, key=lambda start: (digest(f'{WINDOW_SALT}{sha}|{start}'),start))[:WINDOWS_PER_VIDEO]
        for start in chosen:
            owner.append({'participant_id':p,'video_id':vid,'video_sha256':sha,
                          'start_native_frame':start,'native_frames':list(range(start,start+WINDOW)),
                          'candidate_windows':len(candidates)})
    owner.sort(key=lambda w: digest('E002-574-blind-v1|' + w['video_sha256'] + '|' + str(w['start_native_frame'])))
    mapping, templates = [], {}
    for i,w in enumerate(owner):
        clip=f'clip_{i:04d}'
        mapping.append({'blind_clip':clip, **w})
    for r in ('A','B'):
        templates[r]={'experiment':'E002-574','rater':r,
                      'clips':{m['blind_clip']:[{'frame':j,'upper_y':None,'lower_y':None,
                                               'iris_diameter':None,'uncertainty_px':None,
                                               'flags':['UNREVIEWED']} for j in range(WINDOW)]
                               for m in mapping}}
    return {'experiment':'E002-574','evidence_tier':'SELECTION_PLAN_ONLY',
            'development_participants':sorted(development),'heldout_participants':sorted(heldout),
            'owner_mapping':mapping,'rater_templates':templates,
            'window_count':len(mapping),'total_heldout_video_count':33,
            'anatomical_human_rater_pairs':0,'physical_camera_certified':False,
            'product':'ABSTAIN_UNCALIBRATED','release':'BLOCKED'}


def write_private(inventory_path, outdir):
    src, out = Path(inventory_path), Path(outdir)
    if src.is_symlink() or not src.is_file() or out.exists() or out.is_symlink():
        raise ValueError('INVALID_INPUT_OR_OUTPUT')
    if any((parent/'.git').exists() for parent in (out,*out.parents)):
        raise ValueError('REFUSE_REPOSITORY_OUTPUT')
    obj = plan(json.loads(src.read_text(encoding='utf-8')))
    out.mkdir(mode=0o700)
    for name, content in [('OWNER_PRIVATE_MAPPING.json', {k:v for k,v in obj.items() if k!='rater_templates'}),
                          ('RATER_A_BLANK.json',obj['rater_templates']['A']),
                          ('RATER_B_BLANK.json',obj['rater_templates']['B'])]:
        path=out/name
        path.write_text(json.dumps(content,indent=2,sort_keys=True)+'\n',encoding='utf-8')
        path.chmod(0o600)
    return {'experiment':'E002-574','status':'PRIVATE_SELECTION_PLAN_WRITTEN',
            'blind_windows':obj['window_count'],'human_rater_pairs':0,
            'product':'ABSTAIN_UNCALIBRATED','release':'BLOCKED'}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--inventory',required=True)
    ap.add_argument('--outdir',required=True)
    args=ap.parse_args()
    try:
        print(json.dumps(write_private(args.inventory,args.outdir),sort_keys=True))
    except Exception as exc:
        print(json.dumps({'experiment':'E002-574','status':'FAILED_OR_ABSTAINED',
                          'error_type':type(exc).__name__, 'product':'ABSTAIN_UNCALIBRATED',
                          'release':'BLOCKED'}))
        raise SystemExit(2)


if __name__=='__main__':
    main()
