#!/usr/bin/env python3
"""Generate E002-391 vector figure from reproducible JSON (matplotlib optional)."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

base=Path(__file__).parent
r=json.loads((base/"e002_391_results.json").read_text())
u=json.loads((base/"e002_391_unseen_results.json").read_text())
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,
                     "svg.fonttype":"none","pdf.fonttype":42,
                     "axes.spines.top":False,"axes.spines.right":False})
fig,ax=plt.subplots(figsize=(8.6,4.6))
labels=["30 Hz\nLocked","30 Hz\n±1 ms jitter","30 Hz\nIndependent phase",
        "60 Hz\nLocked (unseen)","60 Hz\nIndependent (unseen)"]
values=[r["locked_any_fraction"],r["jitter_1ms_any_fraction"],
        r["randomized_any_fraction"],u["unseen_60hz_locked_fraction"],
        u["unseen_60hz_randomized_fraction"]]
colors=["#68798A","#A0AEBB","#217A7A","#68798A","#217A7A"]
bars=ax.bar(range(len(labels)),values,width=.63,color=colors,edgecolor="none")
ax.set_xticks(range(len(labels)),labels)
ax.set_ylim(0,1.12)
ax.yaxis.set_major_formatter(PercentFormatter(1))
ax.set_ylabel("At least one event detected across 12 repeats")
ax.set_title("Controlled phase sweeps expose fixed aliases only under event-phase independence",
             loc="left",pad=20,fontsize=12,fontweight="bold")
for bar,value in zip(bars,values):
    ax.text(bar.get_x()+bar.get_width()/2,value+.024,f"{value*100:.2f}%",
            ha="center",va="bottom",fontsize=10,fontweight="bold")
ax.axhline(1,ls=":",lw=.8,color="#8E9AA5")
fig.text(.11,.01,"Synthetic shutter/aperture instrument; 12,000 trial sets per acquisition condition. Not human evidence.",
         fontsize=8.7,color="#4F5C68")
fig.tight_layout(rect=(0,.05,1,.95))
for ext in ("svg","pdf","png"):
    fig.savefig(base/f"e002_391_phase_detection.{ext}",dpi=200,bbox_inches="tight")
print("Saved SVG/PDF/PNG figures")
