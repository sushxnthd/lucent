#!/usr/bin/env python3
"""Deterministic stratified samples of huge ZIP central directory (metadata only)."""
import collections, datetime, hashlib, json, pathlib, struct
from probe import fetch

OUT = pathlib.Path('research/e002-218')
provenance = json.loads((OUT/'PROVENANCE.json').read_text())
a = provenance['archive']
report = {'run':'E002-218b','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'source':provenance['source'],'status':'blocked','full_inventory':False,
          'human_waveform_evaluated':False,'native_paired_reference_certified':False,
          'sampling_method':'deterministic 16-stratum 512-KiB byte-window ZIP central directory samples',
          'samples':[]}

def parse_chunk(b):
    pos = b.find(b'PK\x01\x02')
    counts = collections.Counter(); dirs = collections.Counter(); candidates=[]; parsed=0
    while pos >= 0 and pos+46 <= len(b) and b[pos:pos+4] == b'PK\x01\x02':
        flags = struct.unpack_from('<H',b,pos+8)[0]
        n, ex, co = struct.unpack_from('<HHH',b,pos+28)
        end=pos+46+n+ex+co
        if end>len(b) or n>1024: break
        raw=b[pos+46:pos+46+n]
        name=raw.decode('utf-8' if flags&2048 else 'cp437',errors='replace')
        ext=pathlib.PurePosixPath(name).suffix.lower() or '[none]'
        counts[ext]+=1
        dirs['/'.join(name.split('/')[:3])]+=1
        if ext not in ('.png','.jpg','.jpeg','.bmp') and len(candidates)<20:
            candidates.append(name[:180])
        parsed+=1
        pos=end
    return {'parsed_entries':parsed,'extension_counts':dict(counts),
            'prefix_counts_top':dirs.most_common(6),'nonimage_examples':candidates}

if a.get('status')=='central_directory_over_budget' and a.get('central_directory_offset') and a.get('central_directory_bytes'):
    start=a['central_directory_offset']; size=a['central_directory_bytes']
    fractions=[0,.01,.05,.10,.20,.30,.40,.50,.60,.70,.80,.90,.95,.98,.99,.999]
    length=524288
    for f in fractions:
        offset=start+min(int(f*size),max(0,size-length))
        end=min(offset+length-1,start+size-1)
        sample={'fraction':f,'byte_start':offset,'byte_end':end}
        try:
            code,headers,data=fetch(a['url'],headers={'Range':f'bytes={offset}-{end}'},limit=length)
            if code!=206 or len(data)!=end-offset+1 or not headers.get('content-range','').startswith(f'bytes {offset}-'):
                raise ValueError('range not honored')
            sample.update(status='ok',sha256=hashlib.sha256(data).hexdigest(),**parse_chunk(data))
        except Exception as e:
            sample.update(status='blocked',error={'type':type(e).__name__,'message':str(e)[:180]})
        report['samples'].append(sample)
    report['status']='complete' if all(x['status']=='ok' for x in report['samples']) else 'partial'
else:
    report['reason']='archive directory not available for stratified sampling'
(OUT/'SAMPLES.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':report['status'],'windows':len(report['samples']),
                  'sampled_entries':sum(x.get('parsed_entries',0) for x in report['samples']),
                  'nonimage_entries':sum(sum(v for k,v in x.get('extension_counts',{}).items() if k not in ('.png','.jpg','.jpeg','.bmp')) for x in report['samples'])}))

# Independent, bounded public CSV schema check after directory sampling.
import csv_probe
