#!/usr/bin/env python3
"""Bounded public Kaggle inventory: metadata pages and ZIP central directory only.
Never downloads images, videos, or an entire dataset archive.
"""
import collections, datetime, hashlib, json, pathlib, re, struct, urllib.parse, urllib.request

BASE = 'https://www.kaggle.com/api/v1/datasets'
REF = 'vijuls/PupilDiameterDatasets'
OUT = pathlib.Path('research/e002-218')
OUT.mkdir(parents=True, exist_ok=True)
HEADERS = {'User-Agent': 'Lucent-E002-218-Archive-Provenance/1.0', 'Accept-Encoding': 'identity'}
MAX_CD = 80_000_000
MAX_RESPONSE = 80_000_100

def fetch(url, method='GET', headers=None, limit=1_000_000):
    req = urllib.request.Request(url, method=method, headers={**HEADERS, **(headers or {})})
    with urllib.request.urlopen(req, timeout=65) as response:
        code = response.status
        h = {k.lower(): v for k, v in response.headers.items()}
        data = b'' if method == 'HEAD' else response.read(limit + 1)
    if len(data) > limit:
        raise ValueError('bounded request exceeded limit')
    return code, h, data

def failure(e):
    return {'type': type(e).__name__, 'status': getattr(e, 'code', None), 'message': str(e)[:250]}

def parse_directory(data):
    counts, hits, examples = collections.Counter(), collections.Counter(), []
    pos = 0
    while pos < len(data):
        if len(data) - pos < 46 or data[pos:pos+4] != b'PK\x01\x02':
            raise ValueError('invalid central directory signature or length')
        flags = struct.unpack_from('<H', data, pos + 8)[0]
        n, extra, comment = struct.unpack_from('<HHH', data, pos + 28)
        end = pos + 46 + n + extra + comment
        if end > len(data):
            raise ValueError('central directory truncated')
        raw = data[pos+46:pos+46+n]
        name = raw.decode('utf-8' if flags & 2048 else 'cp437', errors='replace')
        ext = pathlib.PurePosixPath(name).suffix.lower() or '[no-extension]'
        counts[ext] += 1
        if ext in ('.csv','.json','.tsv','.h5','.hdf5','.parquet','.mp4','.avi','.mov','.mkv','.webm','.npy','.npz','.zip','.tar','.gz') or re.search('tobii|timestamp|raw|session|recording|pupil|reference|metadata', name, re.I):
            hits[ext] += 1
            if len(examples) < 35: examples.append(name[:230])
        pos = end
    return {'entry_count': sum(counts.values()), 'extension_counts': dict(counts), 'candidate_counts': dict(hits), 'candidate_examples': examples}

def range_bytes(url, start, end, maxlen):
    status, headers, data = fetch(url, headers={'Range': f'bytes={start}-{end}'}, limit=maxlen)
    if status != 206 or not headers.get('content-range', '').lower().startswith(f'bytes {start}-'):
        raise ValueError('server did not honor exact byte range')
    if len(data) != end - start + 1:
        raise ValueError('byte-range length mismatch')
    return data

def archive_probe():
    url = BASE + '/download/' + REF
    out = {'url': url, 'status': 'blocked', 'central_directory_complete': False, 'native_paired_reference_certified': False}
    try:
        try:
            code, head, _ = fetch(url, method='HEAD')
            out['head'] = {'status': code, 'length': head.get('content-length'), 'accept_ranges': head.get('accept-ranges'), 'content_type': head.get('content-type')}
        except Exception as exc:
            out['head_error'] = failure(exc)
        code, hdr, tail = fetch(url, headers={'Range': 'bytes=-65557'}, limit=65557)
        out['tail_status'] = code
        out['tail_sha256'] = hashlib.sha256(tail).hexdigest()
        cr = hdr.get('content-range', '')
        out['content_range'] = cr
        m = re.fullmatch(r'bytes (\d+)-(\d+)/(\d+)', cr)
        if code != 206 or not m:
            out['status'] = 'range_unsupported'
            return out
        a, b, total = map(int, m.groups())
        if b != total - 1 or len(tail) != b-a+1:
            raise ValueError('tail range inconsistent')
        e = tail.rfind(b'PK\x05\x06')
        if e < 0 or e + 22 > len(tail):
            out['status'] = 'eocd_not_found'
            return out
        sig, disk, disk_cd, n_disk, n_all, cd_size, cd_start, comment = struct.unpack_from('<4s4H2IH', tail, e)
        if disk != 0 or disk_cd != 0:
            out['status'] = 'multidisk_zip_unsupported'
            return out
        if n_all == 65535 or cd_size == 0xffffffff or cd_start == 0xffffffff:
            loc = tail.rfind(b'PK\x06\x07', 0, e)
            if loc < 0 or loc + 20 > len(tail):
                out['status'] = 'zip64_locator_unavailable'
                return out
            _, disk_start, z64_offset, n_disks = struct.unpack_from('<4sIQI', tail, loc)
            z64 = range_bytes(url, z64_offset, z64_offset+55, 56)
            if z64[:4] != b'PK\x06\x06':
                raise ValueError('invalid ZIP64 EOCD')
            n_all, cd_size, cd_start = struct.unpack_from('<QQQ', z64, 32)
            out['zip64'] = True
        else:
            out['zip64'] = False
        out['declared_entries'] = n_all
        out['central_directory_bytes'] = cd_size
        out['central_directory_offset'] = cd_start
        if cd_size <= 0 or cd_size > MAX_CD:
            out['status'] = 'central_directory_over_budget'
            return out
        cd = range_bytes(url, cd_start, cd_start + cd_size - 1, MAX_RESPONSE)
        out['central_directory_sha256'] = hashlib.sha256(cd).hexdigest()
        result = parse_directory(cd)
        out.update(result)
        if result['entry_count'] != n_all:
            raise ValueError('declared entries differ from parsed entries')
        out['central_directory_complete'] = True
        out['status'] = 'complete'
    except Exception as exc:
        out['error'] = failure(exc)
    return out

def listing_probe():
    url = BASE + '/list/' + REF
    out = {'url': url, 'status': 'blocked', 'pages': [], 'complete': False}
    token = None
    try:
        for page in range(4):
            query = {'pageSize': '200'}
            if token: query['pageToken'] = token
            code, headers, b = fetch(url + '?' + urllib.parse.urlencode(query), limit=1_500_000)
            obj = json.loads(b)
            files = obj.get('datasetFiles', obj.get('files', []))
            if not isinstance(files, list): raise ValueError('invalid listing structure')
            out['pages'].append({'page': page+1, 'count': len(files), 'sha256': hashlib.sha256(b).hexdigest(),
                'extension_counts': dict(collections.Counter(pathlib.PurePosixPath(x.get('name','')).suffix.lower() for x in files)),
                'candidate_examples': [x.get('name') for x in files if pathlib.PurePosixPath(x.get('name','')).suffix.lower() not in ('.png','.jpg','.jpeg','.bmp')][:15]})
            new_token = obj.get('nextPageToken')
            if not new_token:
                out['complete'] = True
                break
            if new_token == token: raise ValueError('pagination token did not advance')
            token = new_token
        out['status'] = 'complete' if out['complete'] else 'partial'
    except Exception as exc:
        out['error'] = failure(exc)
    return out

def main():
    report = {'run': 'E002-218', 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'source': REF, 'signal_reference_pair': 'ordinary RGB pupil/iris waveform vs native-time same-eye tracker pupil diameter',
        'human_waveform_evaluated': False, 'frozen_gates_changed': False,
        'archive': archive_probe(), 'listing': listing_probe()}
    report['native_paired_reference_certified'] = False
    path = OUT / 'PROVENANCE.json'
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'archive': report['archive']['status'], 'archive_entries': report['archive'].get('entry_count'),
        'listing': report['listing']['status'], 'listing_pages': len(report['listing']['pages']),
        'native_pair_certified': False}))

if __name__ == '__main__': main()
