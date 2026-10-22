"""Regenerate E002-377 synthetic shutter/contrast certificate figure.
Requires numpy, scipy and matplotlib. Never label as human evidence."""
import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import subprocess
root=Path(__file__).parent
subprocess.run(["python",str(root/"e002_377_optical_stress.py")],check=True)
rows=json.loads((root/"e002_377_optical_results.json").read_text())["conditions"]
conds=["clean","blur_1px","blur_2px","blur_4px","blur_8px","missing_eye","global_gain","local_drift"]
fig,ax=plt.subplots(figsize=(8.2,4.6))
for fps,mark in [(20,"o"),(30,"s")]:
    yy=[next(v["Xi_8bit"] for v in rows if v["condition"]==c and v["fps"]==fps) for c in conds]
    ax.plot(np.arange(len(conds)),yy,marker=mark,label=f"{fps} fps",linewidth=1.8)
ax.axhline(1,color="black",ls="--",lw=1,label="Certificate threshold")
ax.set_yscale("symlog",linthresh=.4)
ax.set_xticks(np.arange(len(conds)),conds,rotation=25,ha="right")
ax.set_ylabel("Dimensionless contrast-overlap margin Xi")
ax.set_title("Synthetic shutter/contrast observability boundary")
ax.grid(alpha=.2)
ax.legend(frameon=False)
fig.text(.1,.01,"Synthetic model only. No human RGB/reference validation.",fontsize=8)
fig.tight_layout(rect=[0,.035,1,1])
fig.savefig(root/"e002_377_boundary.svg")
