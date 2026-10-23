#!/usr/bin/env python3
"""E002-392B: correct false AVI 1-fps time base; do not certify aperture."""
import argparse,csv,json,pathlib,zipfile
import cv2,numpy as np

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--archive",required=True)
    p.add_argument("--output",required=True)
    p.add_argument("--published-fps",type=float,default=150.0)
    a=p.parse_args();out=pathlib.Path(a.output)
    base=json.loads((out/"result.json").read_text())
    video=out/"human_reference.avi";cap=cv2.VideoCapture(str(video))
    if not cap.isOpened():raise RuntimeError("Cannot decode human source")
    n=int(cap.get(cv2.CAP_PROP_FRAME_COUNT));fps=a.published_fps
    if fps<=0:raise ValueError("Invalid published fps")
    rows=[];summaries=[];thumbnails=[]
    for frac in (.15,.5,.8):
        start=int(max(0,min(n-int(8*fps),round(n*frac))))
        cap.set(cv2.CAP_PROP_POS_FRAMES,start)
        prev=None;motions=[]
        for k in range(min(n-start,int(8*fps))):
            ok,frame=cap.read()
            if not ok:break
            h,w=frame.shape[:2]
            roi=cv2.cvtColor(frame[h//5:4*h//5,w//5:4*w//5],cv2.COLOR_BGR2GRAY)
            roi=cv2.resize(roi,(64,64),interpolation=cv2.INTER_AREA)
            motion=float(np.mean(np.abs(roi.astype(np.float32)-prev.astype(np.float32)))) if prev is not None else None
            prev=roi
            if motion is not None:motions.append(motion)
            rows.append((frac,start+k,(start+k)/fps,float(roi.mean()),float(roi.std()),motion))
            if k in (0,int(1.5*fps),int(4*fps)):
                t=cv2.resize(frame,(320,240))
                cv2.putText(t,f"frame {start+k}",(8,22),cv2.FONT_HERSHEY_SIMPLEX,.55,(255,255,255),2)
                thumbnails.append(t)
        if not motions:raise RuntimeError("No frames decoded for segment")
        med=float(np.median(motions));mad=float(np.median(np.abs(np.asarray(motions)-med)))
        summaries.append({"fraction":frac,"start_frame":start,"start_nominal_seconds":start/fps,
          "decoded_frames":len(motions)+1,"motion_median":med,"motion_mad":mad,
          "unlabeled_motion_spikes":sum(x>med+4*max(.01,mad) for x in motions)})
    cap.release()
    with open(out/"roi_motion_repaired.csv","w",newline="") as f:
        w=csv.writer(f)
        w.writerow(["segment","frame_index","published_rate_nominal_time_s","brightness","contrast","motion_proxy"])
        w.writerows(rows)
    if thumbnails:
        cv2.imwrite(str(out/"human_contact_sheet_repaired.jpg"),
          cv2.vconcat([cv2.hconcat(thumbnails[i:i+3]) for i in range(0,len(thumbnails),3)]))
    sidecars=[]
    with zipfile.ZipFile(a.archive) as z:
        for name in z.namelist():
            if name.endswith("_sync.csv") or name.endswith("_phantom.xml"):
                with z.open(name) as f: head=f.read(2048).decode("utf-8","replace")
                sidecars.append({"path":name,"bytes":z.getinfo(name).file_size,"first_120_chars":head[:120]})
    repaired={"source_verified":base["archive_verified"],"frame_count":n,
      "container_avg_fps":base["observed_fps"],"primary_paper_acquisition_fps":fps,
      "container_vs_paper_rate_factor":fps/base["observed_fps"],
      "nominal_duration_from_published_rate_s":n/fps,
      "video_container_duration_s":float(base["video"]["duration"]),
      "source_rate_is_independently_clock_verified":False,
      "sidecar_inspection":sidecars,"segments":summaries,
      "human_eye_imagery":"real; motion is exploratory and NOT aperture or blink ground truth",
      "product_certificate":"ABSTAIN_UNCALIBRATED",
      "evidence_tier":"human video timing-metadata falsification, not shutter-gap human validation"}
    (out/"result_repaired.json").write_text(json.dumps(repaired,indent=2))
    print(json.dumps({k:repaired[k] for k in ("frame_count","container_avg_fps",
       "primary_paper_acquisition_fps","container_vs_paper_rate_factor",
       "nominal_duration_from_published_rate_s","segments","product_certificate")},indent=2))
if __name__=="__main__":main()
