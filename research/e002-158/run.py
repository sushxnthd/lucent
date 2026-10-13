import csv,hashlib,json,pathlib,zipfile
from download import get
from pairs import matched
from score import score
from report import summarize
from auc import check
OUT=pathlib.Path("research/e002-158")
def main():
 OUT.mkdir(parents=True,exist_ok=True);check()
 result={"status":"NOT_EVALUABLE","claim":"Oracle-label-localized RGB photometric separability only; no tracker or fatigue"}
 try:
  td,path,manifest=get()
  with zipfile.ZipFile(path) as z:
   pairs,inventory=matched(z);rows=[];excluded={}
   for n,m in pairs[960:]:
    try:r,err=score(z.read(n),z.read(m),n,len(rows)+sum(excluded.values()))
    except Exception as e:r,err=None,"decode_"+type(e).__name__
    if err:excluded[err]=excluded.get(err,0)+1
    else:rows.append(r)
    if len(rows)>=480:break
  td.cleanup()
  result.update(status="ORIGINAL_HUMAN_RGB_LOCAL_CONTRAST_SCORED",manifest=manifest,
   inventory=inventory,excluded=excluded,summary=summarize(rows))
  with (OUT/"RAW_RESULTS.csv").open("w",newline="") as f:
   w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 except Exception as e:result["error"]=type(e).__name__+": "+str(e)
 (OUT/"RESULTS.json").write_text(json.dumps(result,indent=2)+"\n")
 (OUT/"SHA256SUMS").write_text("\n".join(hashlib.sha256(p.read_bytes()).hexdigest()+"  "+p.name for p in [OUT/"RAW_RESULTS.csv",OUT/"RESULTS.json"] if p.exists())+"\n")
 print(json.dumps(result,indent=2))
 if result["status"]!="ORIGINAL_HUMAN_RGB_LOCAL_CONTRAST_SCORED":raise SystemExit(2)
if __name__=="__main__":main()
