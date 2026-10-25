#!/usr/bin/env python3
"""E002-439 virtual optical clock: instrument test, NOT sensor authentication.

All images and ticks are synthetically authored. A real camera requires an
independently driven oscillator/LED, calibrated exposure and row timing.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

WIDTH, HEIGHT, CELL = 64, 32, 8
TICKS = (0, 33, 67, 100, 200, 233, 267, 300, 400, 433, 467, 500)
VIRTUAL_TICK_HZ = 1000
PRODUCT = 'ABSTAIN_UNCALIBRATED'

class OpticalClockError(ValueError):
    pass

def crc8(payload):
    """CRC-8/SMBUS: poly 0x07, init 0x00, no reflection/xorout."""
    state = 0
    for byte in payload:
        state ^= byte
        for _ in range(8):
            state = ((state << 1) ^ (0x07 if state & 0x80 else 0)) & 255
    return state

def payload_bits(tick):
    if type(tick) is not int or not 0 <= tick < 65536:
        raise OpticalClockError('invalid virtual tick')
    gray = tick ^ (tick >> 1)
    crc = crc8(tick.to_bytes(2, 'big'))
    value = (gray << 8) | crc
    return [(value >> (23 - k)) & 1 for k in range(24)]

def render_frame(tick):
    bits = payload_bits(tick) + [k % 2 for k in range(8)]
    pixels = bytearray(WIDTH * HEIGHT * 3)
    for k, bit in enumerate(bits):
        col, row = k % 8, k // 8
        level = 224 if bit else 24
        for y in range(row*CELL, (row+1)*CELL):
            for x in range(col*CELL, (col+1)*CELL):
                j = (y*WIDTH+x)*3
                pixels[j:j+3] = bytes((level,level,level))
    return bytes(pixels)

def decode_frame(frame):
    if len(frame) != WIDTH*HEIGHT*3:
        raise OpticalClockError('invalid image dimensions')
    # Decode only central 4x4 of each 8x8 cell; reference cells set threshold.
    levels = []
    for k in range(32):
        col, row = k % 8, k // 8
        samples = [frame[(y*WIDTH+x)*3] for y in range(row*8+2,row*8+6)
                   for x in range(col*8+2,col*8+6)]
        levels.append(sum(samples)/len(samples))
    black = [levels[24+k] for k in range(0,8,2)]
    white = [levels[24+k] for k in range(1,8,2)]
    low, high = sum(black)/4, sum(white)/4
    if high-low < 80 or low > 120 or high < 135:
        raise OpticalClockError('reference contrast/saturation failure')
    threshold = (low+high)/2
    bits = [int(v>threshold) for v in levels]
    if bits[24:] != [k%2 for k in range(8)]:
        raise OpticalClockError('optical fiducial mismatch')
    value = 0
    for b in bits[:24]:
        value = (value<<1) | b
    gray, checksum = value>>8, value & 255
    binary = gray
    mask = binary >> 1
    while mask:
        binary ^= mask
        mask >>= 1
    if crc8(binary.to_bytes(2,'big')) != checksum:
        raise OpticalClockError('CRC mismatch')
    return binary

def adjudicate_frames(frames):
    ticks = [decode_frame(frame) for frame in frames]
    if not ticks:
        raise OpticalClockError('empty sequence')
    if any(b <= a for a,b in zip(ticks,ticks[1:])):
        raise OpticalClockError('duplicate or nonmonotonic optical clock')
    gaps = [b-a for a,b in zip(ticks,ticks[1:])]
    return {'evidence_tier':'VIRTUAL_OPTICAL_INSTRUMENT_NOT_PHYSICAL',
            'tick_hz':'1000_STIPULATED_NOT_MEASURED',
            'ticks':ticks, 'gaps_virtual_ms':gaps,
            'max_gap_virtual_ms':max(gaps,default=0),
            'physical_exposure_authenticated':False,
            'physical_hidden_closure_certified':False,
            'product':PRODUCT}

def run(command):
    p=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if p.returncode:
        raise RuntimeError('command failed: '+repr(command)+'\n'+p.stderr.decode(errors='replace')[-1500:])
    return p.stdout

def encode_frames(directory, ticks, output):
    if not ticks or any(type(t) is not int for t in ticks):
        raise OpticalClockError('invalid tick sequence')
    directory = Path(directory)
    directory.mkdir(parents=True,exist_ok=True)
    for i,tick in enumerate(ticks):
        (directory/f'f{i:03d}.ppm').write_bytes(
            f'P6\n{WIDTH} {HEIGHT}\n255\n'.encode()+render_frame(tick))
    # Set a 1-ms filter timebase to avoid image2's 25-fps quantization.
    expr = str(ticks[-1])
    for i in range(len(ticks)-2,-1,-1):
        expr = f'if(eq(N,{i}),{ticks[i]},{expr})'
    filt = 'settb=1/1000,setpts='+expr.replace(',','\\,')
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-framerate','25',
         '-i',str(directory/'f%03d.ppm'),'-vf',filt,'-fps_mode','vfr',
         '-c:v','ffv1',str(output)])

def video_frames(path):
    raw = run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(path),
               '-f','rawvideo','-pix_fmt','rgb24','-vsync','0','pipe:1'])
    size=WIDTH*HEIGHT*3
    if len(raw)%size:
        raise OpticalClockError('decoded frame size mismatch')
    return [raw[i:i+size] for i in range(0,len(raw),size)]

def pts_ms(path):
    raw=run(['ffprobe','-v','error','-select_streams','v:0',
             '-show_entries','frame=best_effort_timestamp_time','-of','json',str(path)])
    obj=json.loads(raw)
    return [round(float(f['best_effort_timestamp_time'])*1000,3) for f in obj['frames']]

def experiment(workdir):
    if not shutil.which('ffmpeg') or not shutil.which('ffprobe'):
        raise RuntimeError('ffmpeg and ffprobe required')
    workdir=Path(workdir)
    workdir.mkdir(parents=True,exist_ok=True)
    original=workdir/'original.mkv'
    retimed=workdir/'retimed.mkv'
    encode_frames(workdir/'frames',TICKS,original)
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(original),
         '-vf','settb=1/1000,setpts=2*PTS','-fps_mode','vfr',
         '-c:v','ffv1',str(retimed)])
    a,b=video_frames(original),video_frames(retimed)
    original_report=adjudicate_frames(a)
    retimed_report=adjudicate_frames(b)
    source_pts,retimed_pts=pts_ms(original),pts_ms(retimed)
    image_hashes=[hashlib.sha256(frame).hexdigest() for frame in a]
    if original_report['ticks']!=list(TICKS) or retimed_report['ticks']!=list(TICKS):
        raise AssertionError('optical tick recovery failed')
    if a!=b or any(hashlib.sha256(f).hexdigest()!=h for f,h in zip(b,image_hashes)):
        raise AssertionError('decoded frames changed')
    if len(source_pts)!=len(TICKS) or len(retimed_pts)!=len(TICKS):
        raise AssertionError('PTS/frame count mismatch')
    if any(abs(x-t)>1 for x,t in zip(source_pts,TICKS)):
        raise AssertionError('source PTS mismatch')
    if any(abs(x-2*t)>1 for x,t in zip(retimed_pts,TICKS)):
        raise AssertionError('retimed PTS mismatch')
    dropped=a[:5]+a[6:]
    loss_report=adjudicate_frames(dropped)
    if loss_report['ticks']!=list(TICKS[:5]+TICKS[6:]):
        raise AssertionError('frame loss clock mismatch')
    for corrupt in (a[:5]+a[4:5]+a[5:], a[:5]+a[6:5:-1]+a[5:]):
        try:adjudicate_frames(corrupt)
        except OpticalClockError:pass
        else:raise AssertionError('duplicate/reorder not rejected')
    # Exact negative control: CRC-8 collision permits a rolling-row splice.
    collision_a,collision_b=1322,14003
    ca,cb=render_frame(collision_a),render_frame(collision_b)
    hybrid=ca[:16*WIDTH*3]+cb[16*WIDTH*3:]
    if ca==cb or hybrid!=ca or decode_frame(hybrid)!=collision_a:
        raise AssertionError('rolling-shutter negative control changed')
    return {'experiment':'E002-439','virtual_tick_hz':VIRTUAL_TICK_HZ,
            'frame_count':len(a),'authored_ticks':list(TICKS),
            'source_pts_ms':source_pts,'retimed_pts_ms':retimed_pts,
            'optical_ticks_after_retiming':retimed_report['ticks'],
            'identical_decoded_image_sha256':True,
            'sha256_first_frame':image_hashes[0],
            'original_max_gap_virtual_ms':original_report['max_gap_virtual_ms'],
            'after_one_drop_max_gap_virtual_ms':loss_report['max_gap_virtual_ms'],
            'naive_30fps_gap_ms':round(1000/30,6),
            'duplicate_reorder_rejected':True,
            'rolling_shutter_crc_collision_ticks':[collision_a,collision_b],
            'rolling_shutter_splice_indistinguishable':True,
            'all_24_single_cell_bit_errors_rejected_in_unit_tests':True,
            'physical_exposure_authenticated':False,
            'product':PRODUCT}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output')
    args=parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='e002439-') as temp:
        result=experiment(temp)
    rendered=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.output:Path(args.output).write_text(rendered)
    else:print(rendered,end='')

if __name__=='__main__':
    main()
