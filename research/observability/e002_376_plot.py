"""Regenerate E002-376 synthetic boundary figure (requires matplotlib)."""
import numpy as np
import matplotlib.pyplot as plt
fps=np.linspace(5,60,600)
D=.058;w=.010
fig,ax=plt.subplots(figsize=(7.2,4.3))
for m,label in [(.010,'10 ms overlap (full exposure)'),(.005,'5 ms overlap')]:
    p=np.minimum(1,np.maximum(0,(D+w-2*m)*fps))
    ax.plot(fps,p,label=label,linewidth=2)
ax.axvline(25,linestyle=':',linewidth=1)
ax.scatter([10,20,25,30],[.48,.96,1,1],s=24,zorder=4)
ax.set(xlabel='Native acquisition frame rate (frames/s)',
       ylabel='Capture fraction under uniform shutter phase',
       ylim=(-.03,1.06),xlim=(5,60),
       title='Synthetic shutter-phase coverage, 58 ms closure plateau')
ax.grid(alpha=.22)
ax.legend(frameon=False,loc='lower right')
fig.text(.12,.01,'Geometric shutter overlap only; not validated RGB detection or a human duration guarantee.',fontsize=8)
fig.tight_layout(rect=[0,.04,1,1])
fig.savefig('phase_boundary.svg')
