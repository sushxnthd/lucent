import csv,io
import human_edge_coverage as h
def sample(bad):
 s=io.StringIO();w=csv.writer(s,delimiter="\t",lineterminator="\n")
 w.writerow(["system_timestamp","left_pupil_valid","left_pupil_diameter",
             "right_pupil_valid","right_pupil_diameter"])
 for i in range(600):
  valid=i not in bad
  w.writerow([f"{i*1e6/120:.6f}",int(valid),3.2 if valid else -1,
              int(valid),3.2 if valid else -1])
 n=600-len(bad)
 meta={("participant_001","image_01_1",eye):
       {"n_trial_samples":"600","n_valid_trial_samples":str(n)}
       for eye in ("left","right")}
 return h.one_trial(s.getvalue().encode(),"participant_001",meta)
def main():
 for bad,expected in [(set(),(True,True)),(set(range(30)),(True,False)),
                       (set(range(570,600)),(True,False)),
                       (set(range(4)),(True,False)),
                       (set(range(285,315)),(False,False))]:
  out=sample(bad)
  for eye in ("left","right"):
   e=out["eyes"][eye]
   assert (e["old_pass"],e["complete_pass"])==expected
 print("PASS five synthetic edge and interior censoring controls")
if __name__=="__main__":main()
