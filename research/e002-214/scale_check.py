#!/usr/bin/env python3
"""Independent pinned-source checker for third-party human-frame rescale stress test."""
import csv,hashlib,io,json,pathlib,urllib.request
ROOT=pathlib.Path(__file__).resolve().parent
PIN="aa9bddf498a3b6e4104c2c000d2cc0c06a816aae"
SHA={"All_Smiles_Ahead":"a23fa7a4202a74094e8f74795ca3ba709e477595","And_it_was_all_Yellow":"3fd586507655c40fe7e2b98041f5069424ac1e50","Blink_It_Like_Brian":"d1f997b264d5e1b22c598043ee5b63137a231fd1","Funny_Talks":"4aa693bc51f36da6be09764baa26da92c1a81310","I_like_to_move_it_move_it":"ef3736f0b0f91935385df92778e79ae01e1bc3f2","Infinite_Blue":"d89f21cb23eb53292e506c34383ed4bf9490c429","Red_Ross":"7dd76649df705ad59533fdfba3600e5d775eeae8","focus_pocus":"99852be62b4bd315b9ed9a15db40db37150dd078"}
def source(name):
    url=f"https://raw.githubusercontent.com/CondadosAI/pupil-diameter-webcam/{PIN}/output/scale_{name}.csv"
    raw=urllib.request.urlopen(url,timeout=45).read()
    digest=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\x00"+raw).hexdigest()
    if digest!=SHA[name]:raise ValueError("SOURCE_BLOB_MISMATCH "+name)
    return list(csv.DictReader(io.StringIO(raw.decode())))
def verify(d,files):
    assert d["source_clips"]==len(files)==8
    nrows=0; frames=[]; seen=[]
    for name,rows in files.items():
        nrows+=len(rows); g={}
        for row in rows:
            f=int(row["frame"]);g.setdefault(f,[]).append(row)
        for f,rs in g.items():
            assert len({float(x["scale"]) for x in rs})==9
            left=[float(x["left_mm"]) for x in rs]
            right=[float(x["right_mm"]) for x in rs]
            frames.append((max(left)-min(left),max(right)-min(right),len(rs)))
    assert d["source_rows"]==nrows
    assert d["unique_frames"]==len(frames)
    assert d["scales_per_frame_min"]==min(x[2] for x in frames)
    assert d["scales_per_frame_max"]==max(x[2] for x in frames)
    t=d["descriptive_threshold_mm"]
    assert d["frames_left_swing_gt_025"]==sum(x[0]>t for x in frames)
    assert d["frames_right_swing_gt_025"]==sum(x[1]>t for x in frames)
    assert d["frames_either_eye_swing_gt_025"]==sum(x[0]>t or x[1]>t for x in frames)
    assert d["frames_both_eyes_swing_gt_025"]==sum(x[0]>t and x[1]>t for x in frames)
    assert abs(d["global_max_left_mm"]-max(x[0] for x in frames))<1e-9
    assert abs(d["global_max_right_mm"]-max(x[1] for x in frames))<1e-9
if __name__=="__main__":
    files={n:source(n) for n in SHA}
    d=json.loads((ROOT/"SCALE_RESULTS.json").read_text())
    verify(d,files)
    mutant=json.loads(json.dumps(d));mutant["frames_either_eye_swing_gt_025"]+=1
    try:verify(mutant,files)
    except AssertionError:pass
    else:raise RuntimeError("MUTATION_NOT_DETECTED")
    print("PASS_E002_214_WILDCARD",d["frames_either_eye_swing_gt_025"],"/",d["unique_frames"])
