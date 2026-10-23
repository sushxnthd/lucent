"""Generate vector figures from E002-386 frozen JSON results."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
p=Path(__file__).parent
r=json.loads((p/'e002_386_results.json').read_text())
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,
    'axes.spines.top':False,'axes.spines.right':False,
    'svg.fonttype':'none','pdf.fonttype':42})
labels=['IID / naive','IID / calibrated','Shift / bypassed gate']
rows=[r['iid']['naive'],r['iid']['selected'],
      r['unseen_device_if_gate_bypassed']['selected']]
for metric,filename,ylabel,ymax in [
    ('risk','e002_386_selective_risk.svg','False / issued decisions',.23),
    ('issue_fraction','e002_386_coverage.svg','Fraction receiving a decision',.56)]:
    fig,ax=plt.subplots(figsize=(7.5,3.5))
    bars=ax.bar(labels,[z[metric] for z in rows],width=.54)
    ax.set_ylim(0,ymax)
    ax.set_ylabel(ylabel)
    ax.yaxis.set_major_formatter(PercentFormatter(1))
    if metric=='risk':
        ax.axhline(.02,ls='--',lw=1.2,c='black',label='2% conditional risk target')
        ax.legend(loc='upper left',frameon=False)
    for bar,z in zip(bars,rows):
        label=(f"{z['false']:,}/{z['issued']:,}" if metric=='risk'
               else f"{z['issue_fraction']:.1%}")
        ax.text(bar.get_x()+bar.get_width()/2,bar.get_height()+.007,
                label,ha='center',va='bottom',fontsize=9)
    fig.tight_layout()
    fig.savefig(p/filename)
    plt.close(fig)
