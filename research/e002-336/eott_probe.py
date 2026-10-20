"""Bounded EOTT HTTP range probe; never downloads archive or human data."""
import json,sys,urllib.request
URL="https://webgazer.cs.brown.edu/data/WebGazerETRA2018Dataset_Release20180420.zip"
def probe():
    d={"dataset":"EOTT","url":URL,"status":"blocked"}
    try:
        with urllib.request.urlopen(urllib.request.Request(URL,method="HEAD"),timeout=15) as r:
            d["head_status"]=r.status
            d["content_length"]=r.headers.get("Content-Length")
            d["accept_ranges"]=r.headers.get("Accept-Ranges")
        with urllib.request.urlopen(urllib.request.Request(URL,headers={"Range":"bytes=0-0"}),timeout=15) as r:
            d["range_status"]=r.status
            d["content_range"]=r.headers.get("Content-Range")
            d["first_byte_len"]=len(r.read(1))
        d["status"]="range_supported" if d["range_status"]==206 else "range_unsupported"
    except Exception as e:
        d["error"]=type(e).__name__+": "+str(e)[:180]
    print(json.dumps(d,sort_keys=True))
    return d["status"]=="range_supported"
if __name__=="__main__":
    sys.exit(0 if probe() else 2)
