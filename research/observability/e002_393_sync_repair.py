#!/usr/bin/env python3
"""E002-393B: gap-aware Phantom cadence and in-coverage EEG marker alignment."""
import argparse,bisect,csv,io,json,pathlib,zipfile
import cv2

def val(s):
    try:return float(s)
    except (ValueError,TypeError):return None

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--archive",required=True)
    p.add_argument("--output",required=True)
    a=p.parse_args();out=pathlib.Path(a.output)
    prev=json.loads((out/"e002_393_sync_result.json").read_text())
    if not prev["source_verified"]:raise RuntimeError("Unverified archive")
    with zipfile.ZipFile(a.archive) as z:
        name=next(n for n in z.namelist() if n.endswith("_sync.csv"))
        with z.open(name) as f:
            rows=csv.DictReader(io.TextIOWrapper(f,encoding="utf-8-sig"))
            frames=[];markers=[]
            for row in rows:
                t=val(row.get("Time"));fr=val(row.get("PhanFrame"));b=val(row.get("Blinks"))
                if t is None:continue
                if fr is not None:frames.append((int(fr),t))
                if b is not None and b>0:markers.append(t)
    if len(frames)<2:raise RuntimeError("Insufficient camera sync")
    active_n=0;active_time=0.;gaps=[];bad_steps=[];step_counts={}
    for (f0,t0),(f1,t1) in zip(frames,frames[1:]):
        df=f1-f0;dt=t1-t0
        if df<=0 or dt<=0:
            bad_steps.append((f0,f1,t0,t1));continue
        if dt>.02:gaps.append({"after_frame":f0,"before_frame":f1,
           "duration_s":dt,"start_s":t0,"end_s":t1})
        else:
            active_n+=df;active_time+=dt
            k=round(dt*1000);step_counts[k]=step_counts.get(k,0)+1
    rate=active_n/active_time if active_time>0 else None
    start_frame,start_time=frames[0];end_frame,end_time=frames[-1]
    clock=[t for f,t in frames];ids=[f for f,t in frames]
    valid=[];rejected_outside=0;rejected_gap=0
    for t in markers:
        if t<start_time or t>end_time:
            rejected_outside+=1;continue
        i=bisect.bisect_left(clock,t);i=min(max(0,i),len(frames)-1)
        near=[i]
        if i>0:near.append(i-1)
        best=min(near,key=lambda j:abs(clock[j]-t))
        if abs(clock[best]-t)>.01:
            rejected_gap+=1;continue
        valid.append((t,ids[best],clock[best]))
    chosen=[]
    for v in valid:
        if not chosen or v[0]-chosen[-1][0]>=1.:chosen.append(v)
        if len(chosen)>=6:break
    cap=cv2.VideoCapture(str(out/"human_reference.avi"))
    if not cap.isOpened():raise RuntimeError("Video not decoded")
    n=int(cap.get(cv2.CAP_PROP_FRAME_COUNT));sheets=[];events=[]
    for t,frame_id,nearest_time in chosen:
        video_idx=frame_id-start_frame
        if not (0<=video_idx<n):raise RuntimeError("Camera frame mapping out of bounds")
        thumbs=[]
        for shift in (-15,0,15):
            idx=max(0,min(n-1,video_idx+shift))
            cap.set(cv2.CAP_PROP_POS_FRAMES,idx)
            ok,im=cap.read()
            if not ok:break
            im=cv2.resize(im,(320,240))
            cv2.putText(im,f"AVI {idx} Phan {idx+start_frame}",(5,20),
                        cv2.FONT_HERSHEY_SIMPLEX,.48,(255,255,255),2)
            thumbs.append(im)
        if len(thumbs)==3:sheets.append(cv2.hconcat(thumbs))
        events.append({"eeg_marker_s":t,"phantom_frame_id":frame_id,
           "avi_frame_index":video_idx,"sync_time_s":nearest_time,
           "alignment_error_s":nearest_time-t})
    cap.release()
    if sheets:cv2.imwrite(str(out/"eeg_marker_contact_sheet_corrected.jpg"),
                            cv2.vconcat(sheets),[cv2.IMWRITE_JPEG_QUALITY,80])
    result={"source_verified":True,"first_phantom_frame_id":start_frame,
      "first_sync_time_s":start_time,"last_phantom_frame_id":end_frame,
      "last_sync_time_s":end_time,"active_frame_steps":active_n,
      "active_elapsed_s":active_time,"active_rate_fps":rate,
      "global_rate_fps":prev["independent_sync_inferred_fps"],
      "active_rate_within_1fps_of_paper_150":rate is not None and abs(rate-150)<1,
      "interframe_step_histogram_ms":step_counts,"recording_gap_count":len(gaps),
      "recording_gap_total_s":sum(g["duration_s"] for g in gaps),
      "largest_gaps":sorted(gaps,key=lambda g:-g["duration_s"])[:8],
      "nonmonotonic_steps":len(bad_steps),"blink_markers_total":len(markers),
      "blink_markers_before_or_after_camera":rejected_outside,
      "blink_markers_inside_camera_gaps":rejected_gap,
      "blink_markers_aligned_within_10ms":len(valid),
      "first_six_separated_in_coverage_events":events,
      "blink_marker_is_not_physical_closure":True,
      "product_decision":"ABSTAIN_UNCALIBRATED"}
    (out/"e002_393_sync_repaired.json").write_text(json.dumps(result,indent=2))
    print(json.dumps({k:result[k] for k in ("active_rate_fps","global_rate_fps",
      "recording_gap_count","recording_gap_total_s","blink_markers_total",
      "blink_markers_aligned_within_10ms","first_six_separated_in_coverage_events",
      "product_decision")},indent=2))
if __name__=="__main__":main()
