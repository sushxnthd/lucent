#!/usr/bin/env python3
"""Deterministic, standard-library SVG for E002-437's sampling-rate tradeoff."""
import argparse
import math
from pathlib import Path
from e002_437_velocity_bridge import penalty, optimal_spacing


def figure():
    w, h = 950, 550
    left, right, top, bottom = 120, 865, 65, 450
    fmin, fmax = 100, 1200
    ymin, ymax = 0, 24
    x = lambda f: left + (f-fmin)/(fmax-fmin)*(right-left)
    y = lambda z: bottom - (z-ymin)/(ymax-ymin)*(bottom-top)
    curve = ' '.join(('M' if i == 0 else 'L') + f'{x(f):.2f},{y(penalty(1/f,.005,3600)):.2f}'
                     for i, f in enumerate(range(fmin, fmax+1, 4)))
    opt = optimal_spacing(.005,3600)
    best_f = opt['optimal_reference_rate_hz']
    best_y = opt['minimum_penalty_mm_s']
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
             '<rect width="100%" height="100%" fill="#fff"/>',
             '<text x="120" y="33" font-family="Arial" font-size="23" font-weight="bold" fill="#202a34">Reference rate is not monotonically better under fixed localization error</text>',
             '<text x="120" y="55" font-family="Arial" font-size="14" fill="#536170">Conditional bound penalty 2ε/h + Ah/2, ε = 0.005 mm, A = 3600 mm/s², exact sensor time</text>']
    for yy in (0, 4, 8, 12, 16, 20, 24):
        parts += [f'<line x1="{left}" y1="{y(yy):.2f}" x2="{right}" y2="{y(yy):.2f}" stroke="#e5e9ed"/>',
                  f'<text x="{left-13}" y="{y(yy)+5:.2f}" text-anchor="end" font-family="Arial" font-size="13" fill="#45525d">{yy}</text>']
    for f in (100, 200, 400, 600, 800, 1000, 1200):
        parts += [f'<line x1="{x(f):.2f}" y1="{bottom}" x2="{x(f):.2f}" y2="{bottom+6}" stroke="#4d5965"/>',
                  f'<text x="{x(f):.2f}" y="{bottom+25}" text-anchor="middle" font-family="Arial" font-size="13" fill="#45525d">{f}</text>']
    parts += [f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" stroke="#253645" stroke-width="2"/>',
              f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" stroke="#253645" stroke-width="2"/>',
              f'<path d="{curve}" fill="none" stroke="#245c84" stroke-width="3"/>',
              f'<line x1="{x(best_f):.2f}" y1="{y(best_y):.2f}" x2="{x(best_f):.2f}" y2="{bottom}" stroke="#bd4a34" stroke-dasharray="5,5"/>',
              f'<circle cx="{x(best_f):.2f}" cy="{y(best_y):.2f}" r="6" fill="#bd4a34"/>',
              f'<text x="{x(best_f)+15:.2f}" y="{y(best_y)-15:.2f}" font-family="Arial" font-size="14" fill="#a43e2c">optimum ~424 Hz, 8.485 mm/s</text>']
    for f in (200,400,1000):
        z=penalty(1/f,.005,3600)
        parts += [f'<circle cx="{x(f):.2f}" cy="{y(z):.2f}" r="5" fill="#245c84"/>',
                  f'<text x="{x(f)+9:.2f}" y="{y(z)-9:.2f}" font-family="Arial" font-size="13" fill="#245c84">{f} Hz: {z:.1f}</text>']
    parts += [f'<text x="{(left+right)/2:.2f}" y="{bottom+58}" text-anchor="middle" font-family="Arial" font-size="17" fill="#263745">Reference sampling frequency (Hz)</text>',
              f'<text transform="translate(37,{(top+bottom)/2:.2f}) rotate(-90)" text-anchor="middle" font-family="Arial" font-size="17" fill="#263745">Conservative velocity penalty (mm/s)</text>',
              '<text x="120" y="529" font-family="Arial" font-size="12" fill="#586570">Illustrative stipulated parameters only. Not a measured human error floor or certified physiological bound.</text>',
              '</svg>']
    return '\n'.join(parts)+'\n'


if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--output',required=True)
    a=p.parse_args()
    Path(a.output).write_text(figure(),encoding='utf-8')
