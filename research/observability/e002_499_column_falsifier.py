#!/usr/bin/env python3
"""E002-499: static-geometry falsifier for E002-492. Synthetic, not human data."""
import json
from fractions import Fraction as F
from e002_492_anatomical_review import build_manifest, template, adjudicate

def aperture(x):
    return F(12)+F(3,100)*(x-160)**2

def interval(x):
    h=aperture(x)
    return ((h-F(1))/F(40),(h+F(1))/F(40))

def frame(x):
    return {"frame":0,"upper_y":90.0,"lower_y":float(90+aperture(x)),
            "iris_diameter":40.0,"uncertainty_px":0.5,"flags":[]}

def run():
    manifest=build_manifest()
    clip=sorted(c["clip"] for c in manifest["review_clips"])[0]
    a,b=template(manifest,"A"),template(manifest,"B")
    a["clips"][clip][0]=frame(160)
    b["clips"][clip][0]=frame(170)
    different=adjudicate(manifest,a,b)
    b["clips"][clip][0]=frame(160)
    same=adjudicate(manifest,a,b)
    assert interval(160)==(F(11,40),F(13,40))
    assert interval(170)==(F(14,40),F(16,40))
    assert different["dual_measurable"]==1 and different["interval_disagreement"]==1
    assert same["dual_measurable"]==1 and same["interval_disagreement"]==0
    assert (aperture(170)-aperture(160))/40==F(3,40)
    return {"experiment":"E002-499","evidence_tier":"SYNTHETIC_STATIC_GEOMETRY_FALSIFICATION",
            "source":"mathematically specified unmoving lid; no human image",
            "same_image_different_column_disagreements":1,
            "same_image_fixed_column_disagreements":0,
            "native_x_columns":[160,170],
            "normalized_intervals":[[float(v) for v in interval(x)] for x in (160,170)],
            "spurious_temporal_normalized_aperture_change":0.075,
            "physical_motion_present":False,"anatomical_human_ratings":0,
            "camera_clock_authenticated":False,"physical_hidden_closure_certified":False,
            "product":"ABSTAIN_UNCALIBRATED","release":"BLOCKED"}

if __name__=="__main__":
    print(json.dumps(run(),indent=2,sort_keys=True))
