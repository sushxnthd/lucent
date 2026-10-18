#!/usr/bin/env python3
"""Wildcard negative evidence: no blink, local eye-patch offset only."""
q=.75;gain=.20;bias=.10
base=[gain*q+bias,bias,gain+bias]
spoof=[base[0]-.09,base[1],base[2]]
def norm(x):return (x[0]-x[1])/(x[2]-x[1])
assert abs((norm(base)-norm(spoof))-.45)<1e-12
print("NO BLINK; false normalized closure",norm(base)-norm(spoof))
