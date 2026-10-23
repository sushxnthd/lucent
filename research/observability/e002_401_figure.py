#!/usr/bin/env python3
"""Reproducible vector figure for E002-401. Standard library only."""
from __future__ import annotations
import argparse
from pathlib import Path
from xml.etree import ElementTree as ET
from e002_401_rolling_shutter import experiment

def make_svg():
    r=experiment()
    naive=r['naive_wrong_certificates']
    corrected=r['corrected_wrong_certificates']
    unresolved=r['corrected_decisions']['UNRESOLVED']
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1060" height="440" viewBox="0 0 1060 440" role="img" aria-label="E002-401 synthetic rolling-shutter falsification">
<rect width="1060" height="440" fill="#ffffff"/>
<text x="48" y="48" font-family="Arial,sans-serif" font-size="25" font-weight="700" fill="#152534">Rolling shutter can invert an eyelid-aperture certificate</text>
<text x="48" y="73" font-family="Arial,sans-serif" font-size="13" fill="#596b78">E002-401 | calibrated synthetic two-landmark instrument, not human-camera error rates</text>
<line x1="528" y1="100" x2="528" y2="370" stroke="#d5dde3" stroke-width="1"/>
<text x="48" y="116" font-family="Arial,sans-serif" font-size="16" font-weight="700" fill="#152534">A. Constant physical closure, asynchronous rows</text>
<text x="48" y="144" font-family="Arial,sans-serif" font-size="12" fill="#596b78">Upper/lower row centers differ by 8 ms; both lids move at 20/s.</text>
<line x1="78" y1="317" x2="474" y2="317" stroke="#8c9aa6" stroke-width="1"/>
<line x1="78" y1="171" x2="78" y2="317" stroke="#8c9aa6" stroke-width="1"/>
<line x1="78" y1="261" x2="474" y2="261" stroke="#b66a62" stroke-width="2" stroke-dasharray="6,5"/>
<text x="85" y="254" font-family="Arial,sans-serif" font-size="12" fill="#a24e48">closure threshold 0.20</text>
<line x1="105" y1="267" x2="451" y2="267" stroke="#147d8b" stroke-width="3"/>
<circle cx="105" cy="267" r="4" fill="#147d8b"/><circle cx="451" cy="267" r="4" fill="#147d8b"/>
<text x="114" y="286" font-family="Arial,sans-serif" font-size="12" fill="#147d8b">true physical aperture = 0.19</text>
<line x1="105" y1="206" x2="451" y2="206" stroke="#cc7535" stroke-width="3"/>
<circle cx="105" cy="206" r="4" fill="#cc7535"/><circle cx="451" cy="206" r="4" fill="#cc7535"/>
<text x="114" y="197" font-family="Arial,sans-serif" font-size="12" fill="#9d551f">asynchronous apparent aperture = 0.35</text>
<text x="80" y="343" font-family="Arial,sans-serif" font-size="12" fill="#152534">Naive: FALSE no-closure certificate</text>
<text x="80" y="362" font-family="Arial,sans-serif" font-size="12" fill="#147d8b">With row error bound ±0.16: UNRESOLVED</text>
<text x="561" y="116" font-family="Arial,sans-serif" font-size="16" font-weight="700" fill="#152534">B. Frozen adversarial trials (n=1,000)</text>
<text x="561" y="144" font-family="Arial,sans-serif" font-size="12" fill="#596b78">Random common motion, acquisition phase, and row-time jitter.</text>
<text x="561" y="194" font-family="Arial,sans-serif" font-size="13" fill="#152534">Incorrect certificates</text>
<rect x="561" y="210" width="400" height="20" rx="3" fill="#edf1f4"/>
<rect x="561" y="210" width="{400*naive/1000:.1f}" height="20" rx="3" fill="#cc7535"/>
<text x="570" y="225" font-family="Arial,sans-serif" font-size="12" fill="#ffffff">naive {naive}/1000</text>
<rect x="561" y="244" width="400" height="20" rx="3" fill="#edf1f4"/>
<text x="570" y="259" font-family="Arial,sans-serif" font-size="12" fill="#152534">row-calibrated {corrected}/1000</text>
<text x="561" y="298" font-family="Arial,sans-serif" font-size="13" fill="#152534">Calibrated abstentions</text>
<rect x="561" y="314" width="400" height="20" rx="3" fill="#edf1f4"/>
<rect x="561" y="314" width="{400*unresolved/1000:.1f}" height="20" rx="3" fill="#147d8b"/>
<text x="570" y="329" font-family="Arial,sans-serif" font-size="12" fill="#ffffff">{unresolved}/1000 unresolved</text>
<text x="561" y="362" font-family="Arial,sans-serif" font-size="12" fill="#596b78">The bound trades unsupported certainty for explicit abstention.</text>
<line x1="48" y1="393" x2="1012" y2="393" stroke="#d5dde3"/>
<text x="48" y="415" font-family="Arial,sans-serif" font-size="12" fill="#596b78">Synthetic only. Physical camera shutter, optical transfer, and human velocity calibration remain unvalidated.</text>
</svg>'''
    ET.fromstring(svg)
    return svg

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--output',default='/tmp/e002_401_figure.svg')
    args=p.parse_args()
    path=Path(args.output)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(make_svg(),encoding='utf-8')
    print(f'Wrote {path}')
