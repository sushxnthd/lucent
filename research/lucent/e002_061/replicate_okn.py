"""E002-061 independent stdlib-only raw-source verification (no user hardware).
Source: Kanari & Kikuchi OKN_Pupil_Data, commit 5e94ca5e0235e668653f44835b25a89b48cd0116.
This is a replication of the E002-060 anomaly, not a novel physiology result.
"""
import csv, hashlib, io, json, math, struct, urllib.request, zipfile
from collections import defaultdict
from pathlib import Path

COMMIT = "5e94ca5e0235e668653f44835b25a89b48cd0116"
URL = f"https://raw.githubusercontent.com/kei-kanari-hub/OKN_Pupil_Data/{COMMIT}/dataset.zip"
CONDS = ("att", "gaze")
STIMS = ("BB", "BW", "WB", "WW")
EXPECTED = {"gaze_C": (13, 13, -1.8205), "att_C": (12, 14, -0.7095),
            "gaze_D": (12, 13, 0.7298), "att_D": (11, 14, 0.4148)}

def parse_number(s):
    try: return float(s)
    except (ValueError, TypeError): return float("nan")

def read_csv_member(archive, condition, stimulus):
    path = f"dataset/Pupil/{condition}/{condition}_{stimulus}.csv"
    with archive.open(path) as fp:
        rows = list(csv.reader(io.TextIOWrapper(fp, encoding="utf-8-sig")))
    header, raw = rows[0], rows[1:]
    assert len(raw) == 2701 and len(header) == 28, (path, len(raw), len(header))
    assert all(len(row) == 28 for row in raw), path
    return [tuple(parse_number(row[j]) for row in raw) for j in range(28)]

def mean_window(trace, lo, hi):
    a = round((lo + 2.7)/0.002)
    b = round((hi + 2.7)/0.002) + 1
    samples = trace[a:b]
    good = [v for v in samples if math.isfinite(v)]
    return sum(good)/len(good) if len(good) >= 0.8*len(samples) else float("nan")

def delta(trace):
    return mean_window(trace, 0.8, 2.5) - mean_window(trace, -0.8, -0.2)

def fingerprint(trace):
    # Canonical binary representation; all-missing series excluded from evidence.
    return hashlib.sha256(b"".join(struct.pack("<d", x) for x in trace)).hexdigest()

def sign_test(k, n):
    from math import comb
    return sum(comb(n, j) for j in range(k, n+1)) / 2**n

def main():
    with urllib.request.urlopen(URL, timeout=120) as resp:
        payload = resp.read()
    assert len(payload) > 1000000, "Unexpectedly short source download"
    source_sha = hashlib.sha256(payload).hexdigest()
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        data = {(c, s): read_csv_member(archive, c, s) for c in CONDS for s in STIMS}

    groups = defaultdict(list)
    missing = []
    for (c, s), traces in data.items():
        for j, trace in enumerate(traces, 1):
            n_valid = sum(math.isfinite(v) for v in trace)
            if not n_valid:
                missing.append((c, s, j))
            elif n_valid == len(trace):
                groups[fingerprint(trace)].append((c, s, j))
    dupes = [members for members in groups.values() if len(members)>1]
    dupes.sort(key=str)
    expected_pairs = [
        sorted([("att", s, 15), ("gaze", s, 14)]) for s in STIMS
    ]
    assert sorted([sorted(x) for x in dupes]) == sorted(expected_pairs), dupes

    result = {}
    for c in CONDS:
        for contrast in ("C", "D"):
            values = []
            for j in range(14, 28):
                if contrast == "C":
                    val = delta(data[(c, "BW")][j]) - delta(data[(c, "BB")][j])
                else:
                    val = delta(data[(c, "WB")][j]) - delta(data[(c, "WW")][j])
                if math.isfinite(val): values.append((j+1, val))
            n = len(values)
            k = sum(v<0 if contrast=="C" else v>0 for _,v in values)
            mean = sum(v for _,v in values)/n
            expk, expn, expmean = EXPECTED[f"{c}_{contrast}"]
            assert (k,n)==(expk,expn), (c,contrast,k,n)
            assert abs(mean-expmean)<0.002, (c,contrast,mean,expmean)
            result[f"{c}_{contrast}"] = {
                "k":k,"n":n,"mean":mean,"one_sided_sign_p":sign_test(k,n),
                "bonferroni_4_p":min(1.,4*sign_test(k,n))
            }

    assert len(missing)==4 and all(c=="gaze" and j==28 for c,s,j in missing), missing
    out = {
        "classification":"independent Python raw-archive replication; not RGB validation",
        "source_url":URL,"source_sha256":source_sha,"source_bytes":len(payload),
        "trace_count":sum(len(x) for x in data.values()),
        "missing_series":missing,"nonmissing_exact_duplicate_groups":dupes,
        "heldout":result,
        "caveat":"Data already z-scored and trial-averaged; duplicate cause unknown. Same dataset as E002-060."
    }
    path=Path("research/lucent/e002_061/replication_result.json")
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
    print(json.dumps(out, indent=2, sort_keys=True))
    print("E002-061 INDEPENDENT RAW-SOURCE REPLICATION PASSED")

if __name__=="__main__": main()
