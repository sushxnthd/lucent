#!/usr/bin/env python3
"""Vector figures for the E002-390 synthetic velocity-aliasing falsification."""
import argparse
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from e002_390_velocity_aliasing import F,W,T_END,THETA,cohort,knots,ordinary_means

def main(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none'})
    x,y=knots((.010+F)/2,.19,90,90)
    t=np.linspace(0,T_END,2000)
    fig,ax=plt.subplots(figsize=(8.1,3.2))
    ax.plot(t*1000,np.interp(t,x,y),lw=2,label='Physical aperture')
    for i in range(7):
        ax.axvspan(i*F*1000,(i*F+W)*1000,alpha=.10)
    ax.axhline(THETA,ls='--',lw=1,label='Threshold = 0.20')
    ax.set(xlabel='Time (ms)',ylabel='Normalized aperture',ylim=(0,1.08),
           xlim=(0,T_END*1000),
           title='A hidden crossing with seven identical shutter means')
    ax.text(90,.47,'Shaded bands: 10-ms exposures at 30 fps\nEvery observed mean = 1.0',fontsize=9)
    ax.legend(frameon=False,loc='lower right')
    fig.tight_layout();fig.savefig(out/'e002_390_collision.svg');plt.close(fig)

    truth=[];observed=[]
    for x,y,v,_ in cohort(39002,1500):
        m=ordinary_means(x,y)
        truth.append(v);observed.append(np.max(np.abs(np.diff(m)))/F)
    fig,ax=plt.subplots(figsize=(5.7,4.5))
    ax.scatter(truth,observed,s=9,alpha=.22,rasterized=False)
    ax.plot([0,125],[0,125],ls='--',lw=1,label='Equal slopes')
    ax.set(xlabel='True maximum aperture speed (s⁻¹)',
           ylabel='Plug-in speed from 30-fps means (s⁻¹)',
           xlim=(0,125),ylim=(0,125),
           title='Velocity self-calibration aliases fast excursions')
    ax.legend(frameon=False)
    fig.tight_layout();fig.savefig(out/'e002_390_velocity_scatter.svg');plt.close(fig)

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--out',default='/tmp/e002_390/figures')
    main(p.parse_args().out)
