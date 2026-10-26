#!/usr/bin/env python3
"""E002-469: one-shot independent clock discovery. Never certifies shutter/anatomy."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
import re
import statistics
import tempfile
import xml.etree.ElementTree as ET
import zipfile

MD5 = '022dc7770d62b258ce2dd5a9a7b3df6c'
NEEDED = ('ME191_phantom.xml', 'ME191_sync.csv')
KEY = re.compile(r'frame|fps|rate|clock|time|timestamp|tick|trigger|sample|frequency|interval|duration', re.I)
FRAME = re.compile(r'(frame|image)[_\\s-]*(index|number|num|id|counter)|^(frame|frame_idx|frameindex|framenumber)$', re.I)
TIME = re.compile(r'time|timestamp|clock', re.I)
UNIT = re.compile(r'(?:^|[_\\s(\\[])(ns|us|ms|s|nanoseconds?|microseconds?|milliseconds?|seconds?)(?:$|[_\\s)\\]])', re.I)
UNIT_SCALE = {'s':1, 'second':1, 'seconds':1, 'ms':.001, 'millisecond':.001, 'milliseconds':.001, 'us':1e-6, 'microsecond':1e-6, 'microseconds':1e-6, 'ns':1e-9, 'nanosecond':1e-9, 'nanoseconds':1e-9}

def digest(path, kind='md5'):
    h = hashlib.new(kind)
    with open(path, 'rb') as f:
        for chunk in iter(lambda:f.read(1<<20), b''):
            h.update(chunk)
    return h.hexdigest()

def safe_components(archive, directory):
    paths = {}
    with zipfile.ZipFile(archive) as z:
        for name in NEEDED:
            candidates = []
            for item in z.infolist():
                p = PurePosixPath(item.filename)
                if (p.name == name and not item.is_dir() and not p.is_absolute()
                    and '..' not in p.parts and item.file_size <= 30_000_000):
                    candidates.append(item)
            if len(candidates) != 1:
                raise ValueError('unsafe, missing, or ambiguous expected component: '+name)
            item = candidates[0]
            target = Path(directory) / name
            with z.open(item) as src, target.open('wb') as dst:
                while True:
                    chunk = src.read(1<<20)
                    if not chunk: break
                    dst.write(chunk)
            if target.stat().st_size != item.file_size:
                raise ValueError('size mismatch')
            paths[name] = target
    return paths

def safe_key(s):
    s = str(s).strip()
    return s if len(s) <= 64 and re.fullmatch(r'[\\w .()/\\[\\]-]+', s) else '[REDACTED]'

def xml_summary(path):
    n = 0; keys = {}; numeric_rate = []
    for _, elem in ET.iterparse(path, events=('end',)):
        n += 1
        tag = elem.tag.rsplit('}',1)[-1]
        pairs = [(tag, elem.text or '')] + list(elem.attrib.items())
        for k, v in pairs:
            if KEY.search(k):
                sk = safe_key(k)
                keys[sk] = keys.get(sk, 0) + 1
                if re.search(r'fps|frame[_\\s-]?rate', k, re.I):
                    try:
                        f = float(v.strip())
                        if math.isfinite(f) and 0 < f <= 10000:
                            numeric_rate.append(f)
                    except (ValueError, AttributeError):
                        pass
        elem.clear()
    return {'elements':n, 'time_related_keys':dict(sorted(keys.items())[:50]),
            'nominal_rate_values':sorted(set(numeric_rate))[:15],
            'nominal_rate_is_not_hardware_clock':True}

def frame_clock_candidate(headers, rows):
    fidx = [i for i, h in enumerate(headers) if FRAME.search(h)]
    tidx = [i for i, h in enumerate(headers) if TIME.search(h) and UNIT.search(h)]
    if len(fidx) != 1 or len(tidx) != 1:
        return {'status':'NO_EXPLICIT_FRAME_CLOCK', 'frame_fields':len(fidx), 'unit_bearing_time_fields':len(tidx)}
    fi, ti = fidx[0], tidx[0]
    unit = UNIT.search(headers[ti]).group(1).lower()
    scale = UNIT_SCALE[unit]
    points = []; bad = 0
    for row in rows:
        try:
            x = float(row[fi]); y = float(row[ti]) * scale
            if not (math.isfinite(x) and math.isfinite(y) and x >= 0 and abs(x-round(x))<1e-6):
                raise ValueError()
            points.append((int(round(x)),y))
        except (IndexError, ValueError, TypeError):
            bad += 1
    if len(points) < 1000:
        return {'status':'INSUFFICIENT_EXPLICIT_PAIRS','valid_pairs':len(points),'invalid_rows':bad}
    diffs = [(b[0]-a[0], b[1]-a[1]) for a,b in zip(points,points[1:])]
    if any(dx <= 0 or dt <= 0 for dx,dt in diffs):
        return {'status':'NONMONOTONIC_CLOCK','valid_pairs':len(points),'invalid_rows':bad}
    slopes = [dt/dx for dx,dt in diffs]
    median_slope = statistics.median(slopes)
    if median_slope <= 0:
        return {'status':'INVALID_SLOPE'}
    deviation = statistics.median(abs(s/median_slope-1) for s in slopes)
    intercept = statistics.median(y - x*median_slope for x,y in points)
    max_residual_frames = max(abs(y-(intercept+x*median_slope))/median_slope for x,y in points)
    eligible = deviation < .01 and max_residual_frames < .5
    return {'status':'CANDIDATE_FRAME_CLOCK' if eligible else 'CLOCK_UNSTABLE',
            'valid_pairs':len(points),'invalid_rows':bad,
            'frame_column':safe_key(headers[fi]),'time_column':safe_key(headers[ti]),
            'candidate_fps':round(1/median_slope,6),
            'median_relative_interval_deviation':round(deviation,8),
            'max_affine_residual_frames':round(max_residual_frames,6),
            'clock_identity_documented':False,'hardware_shutter_authenticated':False}

def csv_summary(path):
    with path.open('r',encoding='utf-8-sig',errors='replace',newline='') as f:
        sample = f.read(4096); f.seek(0)
        try: dialect = csv.Sniffer().sniff(sample, delimiters=',;\\t|')
        except csv.Error: dialect = csv.excel
        reader = csv.reader(f, dialect)
        headers = next(reader, [])
        if not headers: return {'status':'EMPTY_CSV'}
        rows = []; count = 0
        for row in reader:
            count += 1
            if count <= 200000: rows.append(row)
        matches = [safe_key(h) for h in headers if KEY.search(h)]
        return {'columns':len(headers),'rows':count,'sampled_rows':len(rows),
                'time_related_headers':matches[:50],
                'clock_test':frame_clock_candidate(headers,rows)}

def analyze(archive, expected_md5=MD5):
    if digest(archive) != expected_md5: raise ValueError('archive MD5 mismatch')
    with tempfile.TemporaryDirectory() as td:
        paths = safe_components(archive,td)
        return {'protocol':'E002-469-frozen-v1','source_archive_sha256':digest(archive,'sha256'),
                'xml':xml_summary(paths[NEEDED[0]]), 'sync_csv':csv_summary(paths[NEEDED[1]]),
                'anatomical_reference_authenticated':False,
                'hardware_exposure_timing_authenticated':False,
                'physical_hidden_closure_exclusion':'ABSTAIN_UNCALIBRATED',
                'product_release_authorized':False,
                'note':'A candidate frame clock requires independent unit/clock identity verification.'}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--archive',required=True); ap.add_argument('--output',required=True)
    args=ap.parse_args(); result=analyze(args.archive)
    Path(args.output).write_text(json.dumps(result,sort_keys=True,indent=2)+'\\n')
    print(json.dumps({'status':result['sync_csv']['clock_test']['status'],
                      'csv_rows':result['sync_csv']['rows'],
                      'xml_elements':result['xml']['elements'],
                      'physical_release_authorized':False}))

if __name__=='__main__': main()
