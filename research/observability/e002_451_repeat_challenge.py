#!/usr/bin/env python3
"""E002-451: private offline mirror-perturbed hidden-repeat challenge.

NOT a blind guarantee, human annotation, or physical eyelid measurement.
No participant images or identifiers are written to stdout.
"""
import argparse
import json
import shutil
import struct
import zlib
from pathlib import Path

from e002_448_blind_annotation import WIDTH, HEIGHT, grayscale_png

PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'


def _decode_frozen_png(data):
    """Decode only grayscale, filter-0, 8-bit PNGs from E002-448."""
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError('unsupported PNG signature')
    pos, chunks, ended = len(PNG_SIGNATURE), [], False
    while pos + 12 <= len(data):
        n = struct.unpack('>I', data[pos:pos+4])[0]
        if n > 20_000_000 or pos + 12 + n > len(data):
            raise ValueError('malformed PNG chunk')
        kind = data[pos+4:pos+8]
        payload = data[pos+8:pos+8+n]
        crc = struct.unpack('>I', data[pos+8+n:pos+12+n])[0]
        if zlib.crc32(kind + payload) & 0xffffffff != crc:
            raise ValueError('invalid PNG CRC')
        chunks.append((kind, payload))
        pos += n + 12
        if kind == b'IEND':
            ended = True
            break
    if not ended or pos != len(data) or [k for k,_ in chunks].count(b'IHDR') != 1:
        raise ValueError('invalid PNG structure')
    if chunks[0][0] != b'IHDR' or chunks[-1][0] != b'IEND':
        raise ValueError('invalid PNG chunk ordering')
    w,h,depth,color,compression,filter_method,interlace = struct.unpack('>IIBBBBB',chunks[0][1])
    if (w,h,depth,color,compression,filter_method,interlace) != (WIDTH,HEIGHT,8,0,0,0,0):
        raise ValueError('unexpected PNG geometry or format')
    if any(k not in (b'IHDR',b'IDAT',b'IEND') for k,_ in chunks):
        raise ValueError('unexpected PNG chunk')
    compressed = b''.join(p for k,p in chunks if k == b'IDAT')
    decompressor = zlib.decompressobj()
    expected = HEIGHT*(WIDTH+1)
    raw = decompressor.decompress(compressed, expected+1)
    if (len(raw) != expected or not decompressor.eof or decompressor.unused_data
            or decompressor.unconsumed_tail or decompressor.flush()):
        raise ValueError('unexpected PNG decompression length')
    rows = []
    for y in range(HEIGHT):
        row = raw[y*(WIDTH+1):(y+1)*(WIDTH+1)]
        if row[0] != 0:
            raise ValueError('unsupported PNG filter')
        rows.append(row[1:])
    return rows


def mirrored_png(data):
    rows = _decode_frozen_png(data)
    return grayscale_png(b''.join(row[::-1] for row in rows))


def _validated(source):
    master = json.loads((source/'PRIVATE_MASTER_DO_NOT_SHARE.json').read_text())
    manifest = json.loads((source/'rater_pack'/'manifest.json').read_text())
    if master.get('experiment') != 'E002-448' or master.get('pilot') != 'S19':
        raise ValueError('not frozen S19 master')
    views = master.get('views')
    if not isinstance(views,list) or not views:
        raise ValueError('missing master views')
    by_frame, ids = {}, set()
    for v in views:
        if not isinstance(v,dict):
            raise ValueError('invalid view')
        vid, idx, repeat = v.get('view_id'),v.get('frame_index'),v.get('repeat')
        if (not isinstance(vid,str) or not vid or '/' in vid or '\\' in vid or vid in ids
                or type(idx) is not int or idx < 0 or type(repeat) is not bool):
            raise ValueError('invalid or duplicate master view')
        ids.add(vid)
        by_frame.setdefault(idx,[]).append(v)
    if not any(len(vs)==2 for vs in by_frame.values()):
        raise ValueError('no hidden repeats')
    if any(sorted(v['repeat'] for v in vs) not in ([False],[False,True]) for vs in by_frame.values()):
        raise ValueError('invalid repeat mapping')
    mviews = manifest.get('views')
    if (not isinstance(mviews,list) or len(mviews)!=len(views)
            or {v.get('view_id') for v in mviews if isinstance(v,dict)}!=ids
            or any(v.get('image')!='frames/'+v['view_id']+'.png' for v in mviews)):
        raise ValueError('manifest/master mismatch')
    frames = source/'rater_pack'/'frames'
    if {p.name for p in frames.iterdir()} != {vid+'.png' for vid in ids}:
        raise ValueError('unexpected or missing PNG')
    original = {vid:(frames/(vid+'.png')).read_bytes() for vid in ids}
    transformed = dict(original)
    repeats = 0
    for vs in by_frame.values():
        if len(vs)==2:
            base = next(v for v in vs if not v['repeat'])['view_id']
            rep = next(v for v in vs if v['repeat'])['view_id']
            if original[base]!=original[rep]:
                raise ValueError('frozen pack no longer has exact repeated images')
            mirrored = mirrored_png(original[rep])
            if mirrored==original[base]:
                raise ValueError('mirror-symmetric repeat: cannot remove exact duplicate')
            transformed[rep]=mirrored
            repeats+=1
    if not (source/'rater_pack'/'rater.html').is_file():
        raise ValueError('missing rater UI')
    return master,manifest,transformed,repeats


def create_challenge(source_root,destination_root):
    source,dest = Path(source_root),Path(destination_root)
    if dest.exists():
        raise FileExistsError('refuse overwrite')
    master,manifest,images,repeats = _validated(source)
    # Preflight complete before any output; preserve original source untouched.
    pack = dest/'rater_pack'
    try:
        (pack/'frames').mkdir(parents=True,exist_ok=False)
        for vid,raw in images.items():
            (pack/'frames'/(vid+'.png')).write_bytes(raw)
        (pack/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
        shutil.copyfile(source/'rater_pack'/'rater.html',pack/'rater.html')
        master = {**master, 'e002_451_challenge': {
            'type':'mirror_repeat_only', 'interpretation':'exploratory perturbation, not cryptographic blinding',
            'human_annotations_collected':False, 'physical_release_authorized':False}}
        (dest/'PRIVATE_MASTER_DO_NOT_SHARE.json').write_text(json.dumps(master,indent=2)+'\n')
    except Exception:
        shutil.rmtree(dest,ignore_errors=True)
        raise
    return {'experiment':'E002-451','source':'E002-448',
            'repeat_pairs':repeats,'original_hash_linkable_pairs':repeats,
            'challenge_byte_identical_repeat_pairs':0,
            'interpretation':'SYNTHETIC_OR_PRIVATE_PACK_INSTRUMENT_ONLY',
            'human_labels_collected':0,'physical_release_authorized':False,
            'e002_371_physical_validation':'NOT_ESTABLISHED',
            'product_claim':'ABSTAIN_UNCALIBRATED'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source-root',type=Path,required=True)
    p.add_argument('--dest-root',type=Path,required=True)
    p.add_argument('--summary',type=Path,required=True)
    a=p.parse_args()
    result=create_challenge(a.source_root,a.dest_root)
    a.summary.parent.mkdir(parents=True,exist_ok=True)
    a.summary.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':
    main()
