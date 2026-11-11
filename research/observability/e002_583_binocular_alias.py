#!/usr/bin/env python3
"""E002-583: prospectively frozen simultaneous binocular human FC-label alias test.

Source is pinned by E002-582; results are index-only, not physical shutter claims.
Only aggregate counts are emitted. No raw frames, labels, names or source members.
"""
import collections
import hashlib
import json
import sys

from e002_582_silesian5_fc import parse_archive, retained_indices
from e002_582_source_probe import retrieve


def candidate_runs(rows, kind):
    if kind not in ('both', 'either'):
        raise ValueError('UNKNOWN_EVENT_DEFINITION')
    def positive(row):
        l, r = row[2] == 'C', row[4] == 'C'
        return l and r if kind == 'both' else l or r
    runs = []
    start = None
    for i, row in enumerate(rows):
        if positive(row):
            if start is None:
                start = i
            elif row[0] != rows[i-1][0] + 1:
                runs.append((start, i-1))
                start = i
        elif start is not None:
            runs.append((start, i-1))
            start = None
    if start is not None:
        runs.append((start, len(rows)-1))
    return runs


def analyze_sequence(rows, kind):
    if not rows or any(rows[i+1][0] <= rows[i][0] for i in range(len(rows)-1)):
        raise ValueError('BAD_SOURCE_INDICES')
    first, last = rows[0][0], rows[-1][0]
    retained = [retained_indices(first, last, p) for p in range(10)]
    totals = collections.Counter()
    lens = collections.Counter()
    missed_by_phase = [0] * 10
    for a, b in candidate_runs(rows, kind):
        totals['candidate_runs'] += 1
        if a == 0 or b == len(rows)-1 or rows[a][0] < first+10 or rows[b][0] > last-10:
            totals['boundary_abstain'] += 1
            continue
        seg = rows[a-1:b+2]
        if any(seg[i+1][0] != seg[i][0]+1 for i in range(len(seg)-1)):
            totals['missing_index_abstain'] += 1
            continue
        if any(row[1] == 'N' or row[3] == 'N' or row[5] == 'N' for row in seg):
            totals['nuisance_abstain'] += 1
            continue
        length = b-a+1
        lens[str(length) if length < 4 else '4+'] += 1
        totals['eligible_runs'] += 1
        missed = [not any(frame in keep for frame in range(rows[a][0], rows[b][0]+1)) for keep in retained]
        nmiss = sum(missed)
        if nmiss != {1:7,2:4,3:1}.get(length,0):
            raise ValueError('EXACT_PHASE_LAW_FALSIFIED')
        totals['phase_law_checked'] += 1
        totals['runs_omitted_any_phase'] += int(nmiss>0)
        totals['runs_omitted_all_phases'] += int(nmiss==10)
        for p, flag in enumerate(missed):
            missed_by_phase[p] += int(flag)
    return totals, lens, missed_by_phase


def analyze(sequences, sha):
    result = {'experiment':'E002-583', 'evidence_tier':'HUMAN_INVESTIGATOR_FC_INDEX_ALIAS_ONLY',
              'source_archive_sha256':sha, 'nominal_source_fps':100,'nominal_target_fps':30,
              'independent_anatomical_raters':False,'physical_shutter_verified':False,
              'continuous_velocity_bound_verified':False,'product':'ABSTAIN_UNCALIBRATED','release':'BLOCKED',
              'source_sequences':len(sequences),'source_rows':sum(map(len,sequences))}
    for kind in ('both','either'):
        totals, lengths, phases = collections.Counter(), collections.Counter(), [0]*10
        per_sequence = []
        for seq in sequences:
            t, lens, missed = analyze_sequence(seq, kind)
            totals.update(t)
            lengths.update(lens)
            phases = [a+b for a,b in zip(phases, missed)]
            per_sequence.append({'rows':len(seq), 'eligible':t['eligible_runs'],
                                 'omitted_any':t['runs_omitted_any_phase']})
        if sum(phases) != sum(lengths[str(i)]*{1:7,2:4,3:1}[i] for i in (1,2,3)):
            raise AssertionError('AGGREGATE_INCONSISTENT')
        if totals['candidate_runs'] != totals['eligible_runs'] + totals['boundary_abstain'] + totals['missing_index_abstain'] + totals['nuisance_abstain']:
            raise AssertionError('UNACCOUNTED_ABSTENTION')
        result[kind] = {'counts':dict(sorted(totals.items())),
                        'length_histogram':{k:lengths[k] for k in ('1','2','3','4+')},
                        'omitted_by_phase':phases,
                        'anonymized_sequence_counts':sorted(per_sequence,key=lambda x:(x['rows'],x['eligible'],x['omitted_any']))}
    return result


def fixtures():
    def make(n=60, l=None, r=None, missing=None, nuisance=None):
        l=set(l or []); r=set(r or [])
        rows=[]
        for i in range(n):
            if i == missing: continue
            rows.append((i,'N' if i==nuisance else 'X',
                         'C' if i in l else 'X','X','C' if i in r else 'X','X'))
        return rows
    rows=make(l=[20,21,22],r=[22,23,24])
    t,l,p=analyze_sequence(rows,'both')
    assert t['eligible_runs']==1 and l['1']==1 and sum(p)==7
    t,l,p=analyze_sequence(rows,'either')
    assert t['eligible_runs']==1 and l['4+']==1 and sum(p)==0
    t,_,_=analyze_sequence(make(l=[20],r=[25]),'both')
    assert t['candidate_runs']==0
    t,_,p=analyze_sequence(make(l=range(20,30),r=range(20,30)),'both')
    assert t['eligible_runs']==1 and sum(p)==0
    t,_,_=analyze_sequence(make(l=[20],r=[20],nuisance=20),'both')
    assert t['nuisance_abstain']==1 and t['eligible_runs']==0
    t,_,_=analyze_sequence(make(l=[20],r=[20],missing=19),'both')
    assert t['missing_index_abstain']==1
    t,_,_=analyze_sequence(make(l=[1],r=[1]),'both')
    assert t['boundary_abstain']==1
    a=make(l=[20],r=[20]); b=make(l=[30,31],r=[30,31])
    assert analyze([a,b],'0'*64)==analyze([b,a],'0'*64)
    try:
        analyze_sequence(make(l=[20],r=[20])+[(20,'X','X','X','X','X')],'both')
    except ValueError:
        pass
    else:
        raise AssertionError('DUPLICATE_NOT_REJECTED')
    print(json.dumps({'experiment':'E002-583','self_test':'PASS','fixture_count':9},sort_keys=True))


if __name__ == '__main__':
    fixtures()
    if '--source' in sys.argv:
        raw=retrieve()
        print(json.dumps(analyze(parse_archive(raw),hashlib.sha256(raw).hexdigest()),sort_keys=True))
