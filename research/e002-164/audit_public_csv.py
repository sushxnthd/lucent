"""Check whether public EyeDentify session labels have a unique tracker timestamp."""
import csv,hashlib,io,json,pathlib,requests
URL="https://www.kaggle.com/api/v1/datasets/download/vijuls/pupildiameterdatasets/eyedentify/eyedentify/left_eyes/1/1/session_data.csv"
result={"source":URL,"status":"NOT_EVALUABLE"}
try:
    r=requests.get(URL,timeout=30)
    result["http_status"]=r.status_code
    if r.status_code==200:
        rows=list(csv.DictReader(io.StringIO(r.content.decode("utf-8-sig"))))
        result.update(status="READ",sha256=hashlib.sha256(r.content).hexdigest(),
                      rows=len(rows),unique_timestamps=len({x["#timestamp"] for x in rows}))
except Exception as e:
    result["error"]=type(e).__name__
pathlib.Path(__file__).with_name("KAGGLE_PROBE.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
