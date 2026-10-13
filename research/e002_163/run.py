"""E002-163 exploratory reanalysis. Input: E002-159 PAIRS.csv, see PROTOCOL.md."""
import csv,hashlib,json,math,pathlib
P=pathlib.Path(__file__).parent
src=P/"PAIRS.csv"
EXPECTED="ec150e35dc84e120f1a0418a003989f4948595a8034ecbc68088954cfe0ce730"
assert hashlib.sha256(src.read_bytes()).hexdigest()==EXPECTED
T=math.log(1.05)
def label(x):return int(x>=T)-int(x<=-T)
rows=list(csv.DictReader(src.open()))
assert len(rows)==17903
result={}
for gap in (1,5,15,30):
 subset=[r for r in rows if int(r["lag"])==gap]
 n_cons=n_dis=n_active=n_act_dis=n_opposite=n_neutral=n_hidden=0
 for r in subset:
  a=float(r["dPn"])/2
  b=float(r["dq"])
  c=(float(r["dPn"])+float(r["dE"])-float(r["dD"]))/2
  la,lb,lc=label(a),label(b),label(c)
  if la!=lb:continue
  n_cons+=1
  n_dis+=int(lc!=la)
  if la:
   n_active+=1;n_act_dis+=int(lc!=la);n_opposite+=int(lc==-la)
  else:
   n_neutral+=1;n_hidden+=int(lc!=0)
 result[str(gap)]={"pairs":len(subset),"consensus":n_cons,"discordant_with_raw":n_dis,
   "active_consensus":n_active,"active_discordant":n_act_dis,"active_opposite":n_opposite,
   "neutral_consensus":n_neutral,"neutral_hidden":n_hidden}
assert abs((0.0+math.log(1.1))-(0.0+math.log(1.1)))<1e-14
print(json.dumps(result,indent=2))
