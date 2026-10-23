#!/usr/bin/env python3
"""E002-393: independent human sync-clock audit; EEG blink pulses != closure."""
import argparse,bisect,collections,csv,io,json,pathlib,statistics,zipfile
import cv2

def num(s):
    try:return float(s)
    except (TypeError,ValueError):return None

def quant(v):
    if not v:return None
    s=sorted(v)
    return {"n":len(s),"min":s[0],"p05":s[int(.05*(len(s)-1))],
       "median":statistics.median(s),"p95":s[int(.95*(len(s)-1))],"max":s[-1]}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--archive",required=True)
    p.add_argument("--output",required=True)
    a=p.parse_args();out=pathlib.Path(a.output)
    base=json.loads((out/"result_repaired.json").read_text())
    if not base["source_verified"]:raise RuntimeError("Archive hash not verified")
    with zipfile.ZipFile(a.archive) as z:
        matches=sorted(n for n in z.namelist() if n.endswith("_sync.csv"))
        if not matches:raise RuntimeError("No sync CSV in source archive")
        with z.open(matches[0]) as f:
            reader=csv.DictReader(io.TextIOWrapper(f,encoding="utf-8-sig",errors="replace"))
            fields=reader.fieldnames
            time_prev=None;time_dt=[];frame_samples=[];blink_counts=collections.Counter()
            prev_blink=False;blink_starts=[];blink_run_lengths=[];blink_run=0;total=0
            for row in reader:
                total+=1
                t=num(row.get("Time"));frame=num(row.get("PhanFrame"))
                if t is not None and time_prev is not None and t>time_prev:time_dt.append(t-time_prev)
                if t is not None:time_prev=t
                if frame is not None and t is not None:frame_samples.append((int(frame),t,row.get("PhanTime","")))
                raw=(row.get("Blinks") or "").strip();blink_counts[raw]+=1
                b=num(raw);on=b is not None and b>0
                if on:
                    blink_run+=1
                    if not prev_blink and t is not None:blink_starts.append(t)
                elif prev_blink:
                    blink_run_lengths.append(blink_run);blink_run=0
                prev_blink=on
            if blink_run:blink_run_lengths.append(blink_run)
    by_frame={}
    for frame,t,pt in frame_samples:
        if frame not in by_frame:by_frame[frame]=(t,pt)
    pairs=sorted((frame,*v) for frame,v in by_frame.items())
    frame_diffs=[];clock_diffs=[];time_per_frame=[]
    for (f1,t1,_),(f2,t2,_) in zip(pairs,pairs[1:]):
        if f2>f1 and t2>t1:
            frame_diffs.append(f2-f1);clock_diffs.append(t2-t1)
            time_per_frame.append((t2-t1)/(f2-f1))
    # 1-ms EEG clock quantizes 150-Hz intervals to alternating 6/7 ms.
    # Median single-interval estimator is biased. Use long-baseline slope.
    inferred_rate=(pairs[-1][0]-pairs[0][0])/(pairs[-1][1]-pairs[0][1]) if len(pairs)>2 and pairs[-1][1]>pairs[0][1] else None
    selected=[]
    for t in blink_starts:
        if not selected or t-selected[-1]>=1.0:selected.append(t)
        if len(selected)==6:break
    imgs=[];events=[]
    if pairs and selected:
        clock=[p[1] for p in pairs]
        cap=cv2.VideoCapture(str(out/"human_reference.avi"))
        for t in selected:
            idx=bisect.bisect_left(clock,t);idx=min(max(0,idx),len(pairs)-1)
            center=pairs[idx][0]
            events.append({"eeg_marker_time":t,"nearest_frame":center,"nearest_frame_time":pairs[idx][1],
                           "alignment_error_seconds":pairs[idx][1]-t})
            frames=[]
            for shift in (-15,0,15):
                cap.set(cv2.CAP_PROP_POS_FRAMES,max(0,center+shift))
                ok,im=cap.read()
                if not ok:break
                thumb=cv2.resize(im,(320,240))
                cv2.putText(thumb,f"frame {center+shift}",(8,22),cv2.FONT_HERSHEY_SIMPLEX,.55,(255,255,255),2)
                frames.append(thumb)
            if len(frames)==3:imgs.append(cv2.hconcat(frames))
        cap.release()
    if imgs:cv2.imwrite(str(out/"eeg_marker_contact_sheet.jpg"),cv2.vconcat(imgs),[cv2.IMWRITE_JPEG_QUALITY,80])
    report={"source_verified":True,"sync_file":matches[0],"csv_fields":fields,"sync_rows":total,
      "time_step_seconds":quant(time_dt),"phantom_frame_observations":len(frame_samples),
      "distinct_phantom_frames":len(pairs),"frame_index_step":quant(frame_diffs),
      "time_between_distinct_frame_records_seconds":quant(clock_diffs),
      "seconds_per_phantom_frame_from_eeg_time":quant(time_per_frame),
      "independent_sync_inferred_fps":inferred_rate,
      "matches_primary_paper_150fps":inferred_rate is not None and abs(inferred_rate-150)<5,
      "matches_container_1fps":inferred_rate is not None and abs(inferred_rate-1)<.1,
      "blink_marker_values":blink_counts.most_common(12),"blink_rising_edges":len(blink_starts),
      "blink_positive_run_length_rows":quant(blink_run_lengths),
      "first_six_separated_marker_windows":events,
      "blink_marker_semantics":"EEG-derived annotation/pulse; NOT physical closure duration",
      "exposure_start_end_verified":False,"physical_aperture_verified":False,
      "product_decision":"ABSTAIN_UNCALIBRATED"}
    (out/"e002_393_sync_result.json").write_text(json.dumps(report,indent=2))
    print(json.dumps({k:report[k] for k in ("sync_rows","distinct_phantom_frames",
      "independent_sync_inferred_fps","matches_primary_paper_150fps",
      "blink_rising_edges","blink_positive_run_length_rows","product_decision")},indent=2))
if __name__=="__main__":main()
