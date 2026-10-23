#!/usr/bin/env python3
"""Reproducible E002-399 vector SVG figure from frozen synthetic results."""
import argparse
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--results',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    data=json.loads(args.results.read_text())
    keys=['open_240','crossing_960','crossing_30','marginal_240_full','marginal_240_missing']
    labels=['Open / 240 Hz','Crossing / 960 Hz','Crossing / 30 Hz',
            'Marginal open / 240 Hz','Marginal + dropped frames']
    outcomes=['CONFIRMED_NO_CROSSING','CONFIRMED_CROSSING','UNRESOLVED']
    colors=['#2E6262','#B96B4F','#A9AAB0']
    with plt.rc_context({'font.family':'DejaVu Sans','font.size':9,
                         'svg.fonttype':'none','axes.spines.top':False,
                         'axes.spines.right':False}):
        fig,ax=plt.subplots(figsize=(8.6,3.3))
        y=np.arange(len(keys))
        left=np.zeros(len(keys))
        for outcome,color in zip(outcomes,colors):
            vals=np.array([data['cohorts'][k][outcome]/data['trials_per_cohort'] for k in keys])
            ax.barh(y,vals,left=left,color=color,label=outcome.replace('_',' ').title(),height=.58)
            for i,v in enumerate(vals):
                if v>.07:
                    ax.text(left[i]+v/2,y[i],f'{v:.0%}',ha='center',va='center',
                            color='white' if outcome!='UNRESOLVED' else '#222',fontsize=8)
            left+=vals
        ax.set_yticks(y,labels)
        ax.invert_yaxis()
        ax.set_xlim(0,1)
        ax.set_xlabel('Share of 200 synthetic trials')
        ax.set_title('Reference-label adequacy depends on sampling and calibration',
                     loc='left',fontweight='bold',pad=13)
        ax.legend(loc='lower center',bbox_to_anchor=(.5,-.42),ncol=3,frameon=False,fontsize=8)
        fig.text(.02,.005,'Synthetic normalized-aperture trajectories; no human or physical-camera validation.',
                 fontsize=7,color='#666')
        fig.tight_layout(rect=(0,.07,1,1))
        args.output.parent.mkdir(parents=True,exist_ok=True)
        fig.savefig(args.output,format='svg',bbox_inches='tight')
        plt.close(fig)


if __name__=='__main__':main()
