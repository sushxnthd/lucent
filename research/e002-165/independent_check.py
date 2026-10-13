import csv,json,pathlib,statistics
p=pathlib.Path(__file__).resolve().parent
r=list(csv.DictReader((p/"RAW_CHROMA.csv").open()))
assert len(r)==480
for x in r:
    for k in ("all_exact_gray","eye_exact_gray","all_gt2","eye_gt2"):
        assert 0<=float(x[k])<=1
    assert len(x["image_sha256"])==64
v=json.loads((p/"RESULTS.json").read_text())
assert v["n"]==480 and v["groups"]==len(set(x["group"] for x in r))
assert v["all_gray99"]==sum(float(x["all_exact_gray"])>=.99 for x in r)
assert v["eye_gray99"]==sum(float(x["eye_exact_gray"])>=.99 for x in r)
assert abs(v["all_pixel_exact_gray_mean"]-statistics.mean(float(x["all_exact_gray"]) for x in r))<1e-12
assert v["G1_effectively_monochrome"]==(v["all_gray99"]/480>=.95)
print("Independent arithmetic checker PASS: 480 original human images")
