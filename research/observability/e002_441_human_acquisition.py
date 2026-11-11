#!/usr/bin/env python3
"""E002-441: acquire high-speed human AVI with integrity checks, no raw-frame export.
NOT physical eyelid validation. Only nonidentifying acquisition metadata is emitted.
"""
import argparse, csv, hashlib, io, json, subprocess, tempfile, urllib.request, zipfile
from pathlib import Path
import xml.etree.ElementTree as ET

SOURCES = {
 "S19": ("8a16cf12526f7558b4e49926c4bc5e8e", 373146176),
 "S21": ("d897548665718c4d5b16846a82e6a95a", None),
 "S22": ("4aabb674dea7b945b1d67cee229a4c96", None),
}
URL = "https://zenodo.org/records/18978288/files/{}.zip?download=1"

def digest(path):
 h=hashlib.md5()
 with open(path,"rb") as f:
  for b in iter(lambda:f.read(1048576),b""): h.update(b)
 return h.hexdigest()

def download(subject,path):
 req=urllib.request.Request(URL.format(subject),headers={"User-Agent":"Lucent-research-validation/1.0"})
 with urllib.request.urlopen(req,timeout=120) as src,open(path,"wb") as dst:
  while True:
   b=src.read(1048576)
   if not b: break
   dst.write(b)

def probe(path):
 p=subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-show_entries",
  "stream=codec_name,width,height,r_frame_rate,avg_frame_rate,nb_frames,duration,time_base",
  "-of","json",str(path)],capture_output=True,text=True,check=True,timeout=120)
 streams=json.loads(p.stdout).get("streams",[])
 if not streams: raise ValueError("No decodable video stream")
 cmd=["ffmpeg","-hide_banner","-loglevel","error","-i",str(path),"-map","0:v:0",
      "-frames:v","2","-f","framemd5","-"]
 p=subprocess.run(cmd,capture_output=True,text=True,check=True,timeout=90)
 rows=[x.strip().split(",") for x in p.stdout.splitlines() if x and not x.startswith("#")]
 if len(rows)!=2: raise ValueError("Two-frame decoder probe failed")
 return {**streams[0],"decoded_probe_frames":2,
         "distinct_first_two_frames":rows[0][-1]!=rows[1][-1]}

def inspect(path,subject,verify=True):
 if subject not in SOURCES: raise ValueError("Unknown frozen subject")
 expected,size=SOURCES[subject]; actual=digest(path)
 if verify and actual.lower()!=expected: raise ValueError("Published archive MD5 mismatch")
 if verify and size and path.stat().st_size!=size: raise ValueError("Published archive size mismatch")
 with zipfile.ZipFile(path) as z:
  files=[i for i in z.infolist() if not i.is_dir()]
  for i in files:
   q=Path(i.filename)
   if q.is_absolute() or ".." in q.parts: raise ValueError("Unsafe ZIP path")
  videos=[i for i in files if i.filename.lower().endswith("_phantom.avi")]
  csvs=[i for i in files if i.filename.lower().endswith("_sync.csv")]
  xmls=[i for i in files if i.filename.lower().endswith("_phantom.xml")]
  if not videos: raise ValueError("No high-speed Phantom AVI")
  schemas=[]
  for i in csvs[:3]:
   with z.open(i) as f:
    row=next(csv.reader(io.TextIOWrapper(f,encoding="utf-8-sig",errors="replace")),[])
   schemas.append({"column_count":len(row),
    "blink_named_columns":[x for x in row if "blink" in x.lower()],
    "timing_named_columns":[x for x in row if "time" in x.lower() or "sync" in x.lower()][:20]})
  roots=[]
  for i in xmls[:3]:
   with z.open(i) as f:
    _,root=next(ET.iterparse(f,events=("start",)))
   roots.append(root.tag.split("}")[-1])
  meta=[]
  with tempfile.TemporaryDirectory() as td:
   for i in videos[:2]:
    dest=Path(td)/Path(i.filename).name
    with z.open(i) as src,open(dest,"wb") as out:
     while True:
      b=src.read(1048576)
      if not b: break
      out.write(b)
    meta.append(probe(dest));dest.unlink()
 return {"subject":subject,"archive_bytes":path.stat().st_size,
  "archive_md5":actual,"published_md5_verified":actual.lower()==expected,
  "archive_member_count":len(files),"human_video_count":len(videos),
  "sync_csv_count":len(csvs),"xml_count":len(xmls),
  "video_probe":meta,"sync_column_schema":schemas,"xml_root_tags":roots,
  "evidence_tier":"HUMAN_HIGH_RATE_VIDEO_PROBE_ONLY",
  "independent_physical_shutter_calibration":False,
  "independent_anatomical_aperture_reference":False,
  "validated_physiological_speed_cap":False,
  "e002_371_physical_validation":"FAIL",
  "physical_release_authorized":False,
  "product_claim":"ABSTAIN_UNCALIBRATED"}

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--subject",choices=sorted(SOURCES),default="S19")
 p.add_argument("--zip",type=Path)
 p.add_argument("--output",required=True,type=Path)
 p.add_argument("--fixture",action="store_true",help="Synthetic test ZIP, bypass published hash")
 a=p.parse_args()
 with tempfile.TemporaryDirectory() as td:
  path=a.zip or Path(td)/(a.subject+".zip")
  if a.zip is None: download(a.subject,path)
  result=inspect(path,a.subject,verify=not a.fixture)
 a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
 print(json.dumps({"subject":a.subject,"video_count":result["human_video_count"],
  "physical_validation":result["e002_371_physical_validation"]}))

if __name__=="__main__":main()
