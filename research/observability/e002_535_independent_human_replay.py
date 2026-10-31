#!/usr/bin/env python3
"""Independent FFmpeg-CLI replay of frozen E002-534 human-image null.

No anatomical claims; no private frames or per-window linkage in output.
"""
from __future__ import annotations
import argparse
from collections import deque
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile

import numpy as np

EXPECTED_MD5 = {"S01": "fef02cb7ebf62e4f3efb6303284fd6cb",
                "S19": "8a16cf12526f7558b4e49926c4bc5e8e"}
HEIGHT, WIDTH, LIMIT = 288, 320, 12006
EYE = (slice(118,190), slice(100,230))
BACKGROUND = (slice(20,100), slice(30,290))
EXPECTED = {
    "S01": {"0": (2379,22,0,0,0), "2": (2378,22,0,0,0)},
    "S19": {"0": (2380,21,0,0,0), "2": (2379,21,0,0,0)},
}


def source_md5(path):
    h = hashlib.md5()
    with open(path,"rb") as f:
        for block in iter(lambda: f.read(1<<20), b""):
            h.update(block)
    return h.hexdigest()


def quality(ids, times):
    if len(ids)!=6 or len(times)!=6:
        return False
    try:
        if any(not isinstance(v,(int,float)) or not math.isfinite(v) for v in times):
            return False
        if any(int(ids[j+1])!=int(ids[j])+1 for j in range(5)):
            return False
        deltas=[times[j+1]-times[j] for j in range(5)]
    except (TypeError,ValueError,OverflowError):
        return False
    return all(0.002<=v<=0.020 for v in deltas) and 0.020<=sum(deltas)<=0.050


def scores(six):
    if len(six)!=6 or any(x.shape!=(HEIGHT,WIDTH) or x.dtype!=np.uint8 for x in six):
        raise ValueError("invalid six-frame native grayscale geometry")
    reference_median=float(np.median(six[0][BACKGROUND]))
    corrected=[np.maximum(0.,np.minimum(255.,x.astype(np.float64)
                 +reference_median-float(np.median(x[BACKGROUND])))) for x in six]
    result={}
    for key,roi in (("eye",EYE),("background",BACKGROUND)):
        left,right=corrected[0][roi],corrected[5][roi]
        endpoint=float(np.abs(right-left).mean())
        interior=max(float(np.abs(corrected[j][roi] -
                     (left+(right-left)*(j/5.))).mean()) for j in range(1,5))
        result[key]=(endpoint,interior)
    return result


def empty():
    return {"eligible":0,"rejected_time_or_id":0,"eye_return":0,
            "eye_specific":0,"background_return":0}


def scan(images, ids, times, limit=LIMIT):
    if len(ids)<limit or len(times)<limit:
        raise ValueError("too few synchronization records")
    result={"0":empty(),"2":empty()}
    window=deque(maxlen=6)
    count=0
    for frame in images:
        if frame.shape!=(HEIGHT,WIDTH) or frame.dtype!=np.uint8:
            raise ValueError("invalid decoded native frame")
        if count<limit:
            window.append(frame)
            start=count-5
            if start>=0 and start%5 in (0,2):
                bucket=result[str(start%5)]
                if not quality(ids[start:start+6],times[start:start+6]):
                    bucket["rejected_time_or_id"]+=1
                else:
                    m=scores(list(window))
                    bucket["eligible"]+=1
                    er=m["eye"][0]<=8 and m["eye"][1]>=18
                    br=m["background"][0]<=8 and m["background"][1]>=18
                    bucket["eye_return"]+=int(er)
                    bucket["background_return"]+=int(br)
                    bucket["eye_specific"]+=int(er and m["background"][1]<=8)
        count+=1
    if count!=len(ids) or count<limit:
        raise ValueError("native video frame count differs from sync records")
    return result


def ffmpeg_frames(path):
    args=["ffmpeg","-hide_banner","-loglevel","error","-nostdin","-i",str(path),
          "-map","0:v:0","-an","-sn","-dn","-f","rawvideo","-pix_fmt","gray","pipe:1"]
    with tempfile.TemporaryFile() as errors:
        process=subprocess.Popen(args,stdout=subprocess.PIPE,stderr=errors)
        try:
            while True:
                raw=process.stdout.read(HEIGHT*WIDTH)
                if not raw:
                    break
                if len(raw)!=HEIGHT*WIDTH:
                    raise ValueError("truncated native frame")
                yield np.frombuffer(raw,dtype=np.uint8).reshape(HEIGHT,WIDTH).copy()
            if process.wait()!=0:
                raise RuntimeError("FFmpeg native decoding failed")
        finally:
            if process.poll() is None:
                process.kill()
                process.wait()
            if process.stdout:
                process.stdout.close()


def evaluate(archive, participant):
    if participant not in EXPECTED_MD5 or source_md5(archive)!=EXPECTED_MD5[participant]:
        raise ValueError("checksum/participant mismatch")
    # Shared metadata parser only; no OpenCV decoding or original E002-534 scoring.
    import e002_397_human_motion as source
    with zipfile.ZipFile(archive) as z:
        video, records, _ = source.load_archive(z,participant)
        if len(records)<LIMIT:
            raise ValueError("source too short")
        with tempfile.TemporaryDirectory(prefix="lucent535_") as temp:
            avi=Path(temp)/"native.avi"
            with z.open(video) as stream, avi.open("wb") as out:
                shutil.copyfileobj(stream,out,1<<20)
            probe=subprocess.run(["ffprobe","-v","error","-select_streams","v:0",
                  "-show_entries","stream=width,height","-of","json",str(avi)],
                  capture_output=True,text=True,check=True)
            tracks=json.loads(probe.stdout).get("streams",[])
            if len(tracks)!=1 or (tracks[0].get("width"),tracks[0].get("height"))!=(WIDTH,HEIGHT):
                raise ValueError("source video geometry mismatch")
            counts=scan(ffmpeg_frames(avi),[x for x,_ in records],[t for _,t in records])
    match=all(tuple(counts[p][key] for key in
        ("eligible","rejected_time_or_id","eye_return","eye_specific","background_return"))
        == EXPECTED[participant][p] for p in ("0","2"))
    return {"experiment":"E002-535","participant":participant,
            "evidence_tier":"REAL_HUMAN_VIDEO_SOFTWARE_REPLAY_NOT_ANATOMY",
            "decoder":"ffmpeg_cli_gray_not_opencv_videocapture",
            "shared_metadata_parser":True,"source_checksum_verified":True,
            "counts":counts,"original_frozen_counts_reproduced":match,
            "decision":"REPLAY_AGREEMENT" if match else "REPLAY_DISAGREEMENT",
            "physical_shutter_authenticated":False,"independent_anatomical_ratings":0,
            "product":"ABSTAIN_UNCALIBRATED","release":"BLOCKED"}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--archive",type=Path,required=True)
    p.add_argument("--participant",choices=tuple(EXPECTED_MD5),required=True)
    args=p.parse_args()
    result=evaluate(args.archive,args.participant)
    print(json.dumps(result,indent=2,sort_keys=True))
    if result["decision"]!="REPLAY_AGREEMENT":
        raise SystemExit(2)

if __name__=="__main__":
    main()
