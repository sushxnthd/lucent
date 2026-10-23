#!/usr/bin/env python3
"""E002-392: exploratory human high-speed video timing audit, NOT blink labels."""
import argparse, csv, hashlib, json, pathlib, subprocess, zipfile
from fractions import Fraction

MD5="fef02cb7ebf62e4f3efb6303284fd6cb"

def digest(path):
    h=hashlib.md5()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1<<20),b""): h.update(chunk)
    return h.hexdigest()

def ffprobe(path,entries,interval=None):
    cmd=["ffprobe","-v","error","-select_streams","v:0"]
    if interval: cmd+=["-read_intervals",interval]
    cmd+=["-show_entries",entries,"-of","json",str(path)]
    return json.loads(subprocess.run(cmd,check=True,capture_output=True,text=True).stdout)

def extract(zpath,out):
    with zipfile.ZipFile(zpath) as z:
        videos=sorted(n for n in z.namelist() if n.lower().endswith("_phantom.avi"))
        if not videos: raise RuntimeError("No *_phantom.avi in source archive")
        name=videos[0]; dest=out/"human_reference.avi"
        with z.open(name) as src,open(dest,"wb") as dst:
            while True:
                block=src.read(1<<20)
                if not block: break
                dst.write(block)
        siblings=[n for n in z.namelist() if n.startswith(name.rsplit("/",1)[0]+"/") and (n.endswith("_sync.csv") or n.endswith("_phantom.xml"))]
        return dest,{"video_path_in_zip":name,"video_count":len(videos),"sidecars_present":siblings}

def image_audit(video,fps,duration,out):
    import cv2,numpy as np
    cap=cv2.VideoCapture(str(video))
    if not cap.isOpened():raise RuntimeError("Video decode unavailable")
    n=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    dur=duration if duration>0 else n/fps
    rows=[]; segments=[];thumbs=[]
    for fraction in (0.15,0.5,0.8):
        start=max(0,min(max(0,dur-8),dur*fraction))
        cap.set(cv2.CAP_PROP_POS_FRAMES,int(start*fps))
        prev=None;motion=[]
        for i in range(min(1200,int(8*fps))):
            ok,frame=cap.read()
            if not ok:break
            h,w=frame.shape[:2]
            roi=frame[h//5:4*h//5,w//5:4*w//5]
            gray=cv2.resize(cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY),(64,64))
            delta=float(np.mean(np.abs(gray.astype("float32")-prev.astype("float32")))) if prev is not None else None
            rows.append((fraction,i,start+i/fps,float(gray.mean()),float(gray.std()),delta))
            if delta is not None:motion.append(delta)
            prev=gray
            if i in (0,min(200,int(1.5*fps)),min(600,int(4*fps))):
                t=cv2.resize(frame,(320,240))
                cv2.putText(t,f"{start+i/fps:.2f}s",(8,22),cv2.FONT_HERSHEY_SIMPLEX,.6,(255,255,255),2)
                thumbs.append(t)
        if not motion:raise RuntimeError("No decoded frames")
        med=float(np.median(motion));mad=float(np.median(np.abs(np.array(motion)-med)))
        segments.append({"fraction":fraction,"start_s":start,"decoded_frames":len(motion)+1,
          "motion_median":med,"motion_mad":mad,
          "unlabeled_motion_spikes":sum(m>med+4*max(mad,.01) for m in motion)})
    cap.release()
    with open(out/"roi_motion.csv","w",newline="") as f:
        writer=csv.writer(f)
        writer.writerow(["segment","frame","nominal_time_s","brightness","contrast","motion_proxy"])
        writer.writerows(rows)
    if thumbs:
        while len(thumbs)%3:thumbs.append(np.zeros_like(thumbs[0]))
        sheet=cv2.vconcat([cv2.hconcat(thumbs[i:i+3]) for i in range(0,len(thumbs),3)])
        cv2.imwrite(str(out/"human_contact_sheet.jpg"),sheet,[cv2.IMWRITE_JPEG_QUALITY,80])
    return segments

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--archive",required=True)
    ap.add_argument("--output",required=True)
    ap.add_argument("--fixture",action="store_true")
    args=ap.parse_args()
    out=pathlib.Path(args.output);out.mkdir(parents=True,exist_ok=True)
    actual_md5=digest(args.archive)
    if not args.fixture and actual_md5!=MD5:raise RuntimeError("Source archive MD5 mismatch: "+actual_md5)
    video,source=extract(args.archive,out)
    info=ffprobe(video,"stream=avg_frame_rate,r_frame_rate,nb_frames,duration,width,height,codec_name,time_base")["streams"][0]
    fps=float(Fraction(info["avg_frame_rate"]))
    if fps<=0:raise RuntimeError("Unknown frame rate")
    duration=float(info.get("duration") or 0)
    frames=ffprobe(video,"frame=best_effort_timestamp_time","%+2").get("frames",[])
    pts=[float(f["best_effort_timestamp_time"]) for f in frames if "best_effort_timestamp_time" in f]
    deltas=[b-a for a,b in zip(pts,pts[1:])]
    segments=image_audit(video,fps,duration,out)
    result={"source":"Guttmann-Flury et al., Scientific Data (2025), Zenodo 18978288, S01.zip",
      "archive_md5":actual_md5,"archive_verified":actual_md5==MD5,
      "source":source,"video":info,"observed_fps":fps,
      "primary_paper_reports_fps":150,"mirror_describes_approx_fps":500,
      "paper_150fps_prediction_met":abs(fps-150)<1,
      "timestamp_deltas_first_2s":{"count":len(deltas),"min":min(deltas) if deltas else None,
        "max":max(deltas) if deltas else None,
        "nonpositive":sum(d<=0 for d in deltas)},
      "segments":segments,"human_aperture_ground_truth":False,
      "blink_labels_issued":0,"certificate":"ABSTAIN_UNCALIBRATED",
      "missing":["exposure start/end","physical aperture","independent velocity bound",
                 "optical transfer calibration","paired ordinary RGB","held-out participants/devices"],
      "evidence_tier":"exploratory real human video only"}
    (out/"result.json").write_text(json.dumps(result,indent=2))
    (out/"LIMITATIONS.md").write_text(
      "Real human eye video, exploratory cadence/motion audit only. Pixel motion is not blink detection. "
      "Nominal fps is not exposure timing. No calibrated aperture or hard observability certificate. "
      "Product decision: ABSTAIN_UNCALIBRATED.\n")
    print(json.dumps({"fps":fps,"prediction_met":result["paper_150fps_prediction_met"],
       "segments":segments,"certificate":result["certificate"]},indent=2))

if __name__=="__main__":main()
