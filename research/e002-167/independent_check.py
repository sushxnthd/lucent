import xml.etree.ElementTree as ET
import re
import audit
s=audit.s
def truth(parts):
    return [x.attrib for x in ET.fromstring("<root>"+"".join(parts).replace("\r","").replace("\n","")+"</root>")]
reference=truth([s])
assert len(reference)==1
assert reference[0]["LPMMV"]=="0" and reference[0]["RPMMV"]=="0"
assert len(reference[0])==48
bad=0
for i in range(1,len(s)):
    p=[s[:i],s[i:]]
    assert truth(p)==reference
    lines="".join(x+"\n" for x in p).splitlines()
    rows=[[m.group(1) for m in re.finditer(r'"([^"]*)"(?= )',x)] for x in lines if "LPOGX" in x and "RPOGY" in x]
    if rows!=[list(reference[0].values())]: bad+=1
assert bad==683,bad
assert len(truth([s+"\r\n"+s]))==2
assert len(audit.source([s+"\r\n"+s]))==2
assert len(audit.source([s+s]))==1
print("Independent XML check PASS: 683 mismatches / 695 splits; all repaired; no valid pupil-mm fixture")
