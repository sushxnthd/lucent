import collections,numpy as np
def summarize(rows):
 lum=np.array([r["auc_lum"] for r in rows]);pl=np.array([r["auc_placebo"] for r in rows])
 group=collections.defaultdict(list)
 for r in rows:group[r["group"]].append(r)
 out={"n_images":len(rows),"n_groups":len(group),"median_auc":float(np.median(lum)),
 "p10_auc":float(np.quantile(lum,.1)),"fraction_ge_08":float(np.mean(lum>=.8)),
 "fraction_below_half":float(np.mean(lum<.5)),"mean_placebo_auc":float(np.mean(pl)),
 "group_median":{g:float(np.median([r["auc_lum"] for r in v])) for g,v in sorted(group.items())},
 "group_n":{g:len(v) for g,v in sorted(group.items())}}
 for k in ("red","green","blue","highpass"):
  v=np.array([r["auc_"+k] for r in rows])
  out[k]={"median_auc":float(np.median(v)),"fraction_better_by_005":float(np.mean(v>=lum+.05))}
 bright=np.array([r["brightness"] for r in rows]);qs=np.quantile(bright,[0,.25,.5,.75,1])
 out["brightness_quartiles"]=[]
 for i in range(4):
  sel=(bright>=qs[i])&(bright<(qs[i+1] if i<3 else qs[i+1]+1e-6))
  out["brightness_quartiles"].append({"n":int(sel.sum()),"median_auc":float(np.median(lum[sel]))})
 out["gates"]={"G0":len(rows)>=300 and len(group)>=10,"G1":out["median_auc"]>=.8,
 "G2":out["p10_auc"]>=.65,"G3":out["fraction_ge_08"]>=.75,
 "G4":abs(out["mean_placebo_auc"]-.5)<=.03,
 "G5":all(np.median([r["auc_lum"] for r in v])>=.55 for v in group.values() if len(v)>=10),
 "G6":"UNTESTED"}
 return out
