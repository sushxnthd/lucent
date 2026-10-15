import csv, json, math, pathlib
p=pathlib.Path(__file__).resolve().parent
rows=list(csv.DictReader(open(p/"RAW_SYNTHETIC.csv")))
result=json.load(open(p/"RESULTS.json"))
assert len(rows)==12
for row in rows:
    f=lambda k:float(row[k])
    d=f("image_l2");s=f("noise_sd")
    assert abs(f("moment2_0")-f("moment2_1"))<1e-5
    Phi=lambda x:.5*(1+math.erf(x/math.sqrt(2)))
    assert abs(f("accuracy_one_frame")-Phi(d/(2*s)))<1e-11
    for rho,key in [(0,"accuracy_150_iid"),(.2,"accuracy_150_rho_0p2"),(.8,"accuracy_150_rho_0p8")]:
        neff=150/(1+149*rho)
        assert abs(f(key)-Phi(math.sqrt(neff)*d/(2*s)))<1e-11
assert result["dataset"]=="SYNTHETIC_ONLY"
assert result["gates"]["human_rgb_reference"] is False
assert abs(result["monte_carlo_one_frame_accuracy"]-result["exact_one_frame_accuracy"])<5*result["monte_carlo_standard_error"]
print("PASS: 12 synthetic cases; zero human observations")
