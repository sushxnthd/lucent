"""Deterministic synthetic validation of E002-436; not a human study."""
import argparse
import json
import random
from collections import Counter
from pathlib import Path

from e002_436_dual_rater import adjudicate


def run(n=1200, seed=436):
    rng = random.Random(seed)
    counts = Counter()
    failures = []
    examples = {}
    dt = 0.00025
    rate = 200  # synthetic reference frame rate; 5-ms steps
    velocity = 120.0
    for trial_index in range(n):
        x = rng.uniform(1.5, 3.3)
        trace = [x]
        for _ in range(160):
            # True continuous piecewise-linear speed is <= 120 mm/s.
            x = max(0., x + rng.uniform(-velocity,velocity)*dt)
            trace.append(x)
        frames = []
        for k in range(9):
            truth = trace[k*20]
            a_minus,a_plus,b_minus,b_plus = (rng.uniform(.01,.06) for _ in range(4))
            frames.append({'frame_id':k,'time_s':k/rate,'nuisance_ok':True,
                           'rater_a':[max(0,truth-a_minus),truth+a_plus],
                           'rater_b':[max(0,truth-b_minus),truth+b_plus]})
        trial = {'trial_id':f'synthetic_{trial_index:04}',
                 'interval_start_s':0., 'interval_end_s':.04,
                 'threshold_mm':2., 'clock_error_s':.0001,
                 'max_reference_step_s':.00501,
                 'velocity_upper_mm_s':velocity,
                 'velocity_bound_attested':True,
                 'sensor_timing_attested':True,
                 'physical_scale_attested':True,
                 'rater_blinding_attested':True,
                 'frames':frames}
        out = adjudicate(trial)
        label = out['reference_label']
        actual_min = min(trace)
        counts[label] += 1
        if actual_min <= 2.:
            counts['actual_crossing'] += 1
            if label == 'UNRESOLVED':
                counts['actual_crossing_unresolved'] += 1
        elif label == 'UNRESOLVED':
            counts['actual_non_crossing_unresolved'] += 1
        if label == 'NEGATIVE_CONDITIONAL' and actual_min <= 2.:
            failures.append(trial_index)
        if label == 'WITNESSED_CROSSING' and actual_min > 2.:
            failures.append(trial_index)
        if label not in examples:
            examples[label] = {'trial_index':trial_index,'minimum_true_aperture_mm':actual_min,
                               'reference_lower_envelope_mm':out['lower_envelope_mm'],
                               'reference_reason':out['reason']}
    if failures:
        raise AssertionError(f'conditional reference adjudication contradicted truth: {failures[:20]}')
    return {'experiment':'E002-436','evidence_tier':'SYNTHETIC_INDEPENDENT_PIECEWISE_LINEAR_TRUTH',
            'participants':0,'human_sequences':0,'seed':seed,'synthetic_trials':n,
            'reference_sampling_hz':rate,'truth_time_step_s':dt,
            'stipulated_velocity_mm_s':velocity,'clock_uncertainty_s':.0001,
            'threshold_mm':2.,'counts':dict(sorted(counts.items())),
            'false_conditional_negative_against_synthetic_truth':0,
            'examples':examples,
            'product':'ABSTAIN_UNCALIBRATED','product_claim_authorized':False,
            'external_physical_provenance_authenticated':False}


def figure(report):
    """Self-contained SVG: a hidden intersample valley and adjudication totals."""
    counts=report['counts']
    n=report['synthetic_trials']
    bars=[('NEGATIVE_CONDITIONAL','#176d75'),('UNRESOLVED','#d29b35'),('WITNESSED_CROSSING','#6a7fa8')]
    def y(mm): return 330-(mm-1.7)*250
    pts=' '.join(f'{120+50*k},{y(2.1-100*min(k*.0005, .005-k*.0005)):.2f}' for k in range(11))
    parts=['<svg xmlns="http://www.w3.org/2000/svg" width="980" height="570" viewBox="0 0 980 570">',
      '<rect width="980" height="570" fill="#fff"/>',
      '<text x="50" y="45" font-family="Arial" font-size="23" font-weight="bold">E002-436 | Reference evidence is not binary</text>',
      '<text x="50" y="70" font-family="Arial" font-size="13" fill="#555">Synthetic 200-Hz reference, 1200 stipulated Lipschitz traces. No human evidence.</text>',
      '<text x="65" y="112" font-family="Arial" font-size="17">A. Hidden closure between open reference frames</text>',
      '<line x1="120" y1="350" x2="650" y2="350" stroke="#333"/>',
      '<line x1="120" y1="140" x2="120" y2="350" stroke="#333"/>',
      f'<line x1="120" y1="{y(2):.2f}" x2="650" y2="{y(2):.2f}" stroke="#bf3d44" stroke-dasharray="6 4"/>',
      f'<text x="658" y="{y(2)+5:.2f}" font-family="Arial" font-size="12" fill="#bf3d44">2.0 mm threshold</text>',
      f'<polyline points="{pts}" fill="none" stroke="#176d75" stroke-width="3"/>',
      f'<circle cx="120" cy="{y(2.1):.2f}" r="6" fill="#6a7fa8"/>',
      f'<circle cx="620" cy="{y(2.1):.2f}" r="6" fill="#6a7fa8"/>',
      '<text x="245" y="375" font-family="Arial" font-size="13">Time (0 to 5 ms)</text>',
      '<text x="73" y="135" font-family="Arial" font-size="12">Aperture (mm)</text>',
      '<text x="140" y="410" font-family="Arial" font-size="13" fill="#444">Open sampled points cannot certify no intersample crossing.</text>',
      '<text x="65" y="460" font-family="Arial" font-size="17">B. Dual-rater conditional reference labels</text>']
    x=65
    for label,color in bars:
        width=850*counts[label]/n
        parts.append(f'<rect x="{x:.2f}" y="478" width="{width:.2f}" height="35" fill="{color}"/>')
        x+=width
    x=65
    for label,color in bars:
        parts.append(f'<rect x="{x}" y="530" width="12" height="12" fill="{color}"/>')
        parts.append(f'<text x="{x+18}" y="541" font-family="Arial" font-size="12">{label}: {counts[label]}</text>')
        x+=282
    parts.append('</svg>')
    return '\n'.join(parts)+'\n'


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--trials',type=int,default=1200)
    p.add_argument('--seed',type=int,default=436)
    p.add_argument('--output')
    p.add_argument('--figure')
    args=p.parse_args()
    if args.trials<1 or args.trials>100000:
        raise ValueError('invalid trial count')
    report=run(args.trials,args.seed)
    text=json.dumps(report,sort_keys=True,indent=2)+'\n'
    if args.figure:Path(args.figure).write_text(figure(report))
    if args.output:Path(args.output).write_text(text)
    else:print(text,end='')


if __name__=='__main__':main()
