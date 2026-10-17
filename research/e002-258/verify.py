#!/usr/bin/env python3
"""Exact integer proof witness; no external dependencies."""
import csv
from pathlib import Path
from fractions import Fraction
P=Path(__file__).parent
with (P/"WITNESS.csv").open() as f: rows=list(csv.DictReader(f))
def world(name):
    a=[r for r in rows if r["world"]==name]
    assert len(a)==4
    x=[int(r["rgb"]) for r in a]
    y=[int(r["reference"]) for r in a]
    return x,y
def moments(x,y):
    assert sum(x)==sum(y)==0
    return (sum(z*z for z in x),sum(z*z for z in y),
            sum(a*b for a,b in zip(x,y)),
            Fraction(sum((a-b)**2 for a,b in zip(x,y)),4))
x,ya=world("same_direction")
xp,yb=world("opposite_direction")
assert x==xp==[-11,-9,9,11]
assert moments(x,ya)==moments(x,yb)==(404,10100,1616,1818)
assert 1616*5==4*2020 and 2020**2==404*10100
def signs(x,y):
    return [1 if (x[j+1]-x[j])*(y[j+1]-y[j])>0 else -1 for j in (0,2)]
assert signs(x,ya)==[1,1] and signs(x,yb)==[-1,-1]
print("EXACT_PASS: same global moments, opposite session correlations")
