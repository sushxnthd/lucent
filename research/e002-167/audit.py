import ast,re,urllib.request,hashlib
url="https://raw.githubusercontent.com/GuangrongZhao/RGBE-Gaze/153979be846fd8a2f483e9af53a9ef52a623533f/data_acquisition_scripts/python/extracker-txt2.py"
raw=urllib.request.urlopen(url,timeout=30).read()
sha=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
assert sha=="c033cac83edd6de0ed226c36436bf5af75fd665f",sha
line=next(x for x in raw.decode().splitlines() if x.startswith("# text = "))
s=ast.literal_eval(line.split("=",1)[1].strip())
def source(chunks):
    rows=[]
    for x in "".join(y+"\n" for y in chunks).splitlines():
        if "LPOGX" in x and "RPOGY" in x:
            rows.append([m.group(1) for m in re.finditer(r'"([^"]*)"(?= )',x)])
    return rows
ref=source([s]); assert len(ref)==1 and len(ref[0])==48
count={"exact":0,"missing_row":0,"wrong_width":0,"other":0}
for i in range(1,len(s)):
    got=source([s[:i],s[i:]])
    if got==ref:count["exact"]+=1
    elif not got:count["missing_row"]+=1
    elif len(got)==1 and len(got[0])!=48:count["wrong_width"]+=1
    else:count["other"]+=1
assert len(s)==696 and count=={"exact":12,"missing_row":62,"wrong_width":621,"other":0},count
print("E002-167 PASS",count)
