#!/usr/bin/env python3
"""Reproduce the E002-400 synthetic optical falsification as a vector SVG."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,
                     'svg.fonttype':'none','axes.spines.top':False,
                     'axes.spines.right':False,'axes.linewidth':.8})
t=np.linspace(-.05,.25,1201)
x=.199+np.abs(t-.1)
fig,ax=plt.subplots(figsize=(8.4,4.7))
ax.plot(t*1000,x,color='#1D3557',lw=2.2,label='Physical aperture x(t)')
ax.axhline(.2,color='#B74141',lw=1.3,ls='--',label='Closure threshold')
for i,c in enumerate([0,.2]):
    ax.axvspan((c-.05)*1000,(c+.05)*1000,color='#B8C4D1',alpha=.24,
               label='Shutter exposure window' if i==0 else None)
ax.scatter([0,200],[.299,.299],s=55,facecolor='white',edgecolor='#1D3557',
           zorder=4,label='True exposure mean')
ax.scatter([0,200],[.3282923933831731]*2,s=65,marker='^',color='#C18A35',
           zorder=5,label='Inverse of averaged optical signal')
ax.scatter([100],[.199],s=70,color='#B74141',zorder=5)
ax.annotate('Hidden crossing (0.199)',xy=(100,.199),xytext=(123,.235),
            arrowprops={'arrowstyle':'->','color':'#B74141','lw':1},color='#B74141')
ax.annotate('0.0293 aperture-unit bias',xy=(200,.3282923933831731),
            xytext=(95,.38),arrowprops={'arrowstyle':'->','color':'#C18A35','lw':1},
            color='#86601C')
ax.set(xlabel='Time (ms)',ylabel='Normalized aperture',xlim=(-55,255),ylim=(.15,.42))
ax.legend(loc='upper left',fontsize=8.5,frameon=False,ncol=2)
ax.grid(axis='y',alpha=.2)
fig.tight_layout()
fig.savefig(Path(__file__).with_name('E002_400_optical_noncommutation.svg'),format='svg')
print('wrote vector figure')
