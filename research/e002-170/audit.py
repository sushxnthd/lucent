#!/usr/bin/env python3
"""E002-170: frozen original-human EyeBlink8 five-second window audit.

Data source is official GPL3 EyeBlink8 ZIP. Media is never committed.
A data-access failure is NOT a scientific failure.
"""
import hashlib, json, math, os, pathlib, re, time, urllib.request, zipfile
from collections import Counter
from statistics import mean

HERE = pathlib.Path(__file__).resolve().parent
URL = "https://www.blinkingmatters.com/files/upload/research/eyeblink8.zip"
ZIP = pathlib.Path(os.getenv("RUNNER_TEMP", "/tmp")) / "lucent_eyeblink8_e002170.zip"
FRAME_WINDOW = 150
MAX_ARCHIVE = 2_000_000_000
MAX_TEXT = 30_000_000

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def save(name, obj):
    (HERE / name).write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def fetch():
    err = []
    for attempt in range(2):
        try:
            req = urllib.request.Request(URL, headers={"User-Agent": "Lucent-Measurement-Research/1.0"})
            with urllib.request.urlopen(req, timeout=90) as resp, ZIP.open("wb") as f:
                h = hashlib.sha256()
                n = 0
                while True:
                    block = resp.read(1 << 20)
                    if not block: break
                    n += len(block)
                    if n > MAX_ARCHIVE: raise RuntimeError("archive exceeds 2GB safety cap")
                    h.update(block); f.write(block)
            return {"url": URL, "bytes": n, "sha256": h.hexdigest(), "attempt": attempt + 1}
        except Exception as exc:
            err.append(type(exc).__name__ + ": " + str(exc)[:300])
            if ZIP.exists(): ZIP.unlink()
            time.sleep(3)
    raise RuntimeError(" | ".join(err))

def parse_annotations(text):
    """Original annotation format: frame ID : blink ID : NF : LE_FC : ..."""
    rows = []
    considered = 0
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"): continue
        if ":" not in line: continue
        parts = [p.strip() for p in line.split(":")]
        if len(parts) < 19: continue
        considered += 1
        if not re.fullmatch(r"[+-]?\d+", parts[0]): continue
        blink = parts[1]
        if blink in ("X", "x", "-", ""): blink = "0"
        if not re.fullmatch(r"[+-]?\d+", blink): continue
        rows.append((int(parts[0]), max(0, int(blink))))
    if len(rows) < 100 or considered == 0 or len(rows) / considered < 0.95:
        return None
    if any(rows[i][0] >= rows[i+1][0] for i in range(len(rows)-1)):
        return {"error": "nonmonotone_or_duplicate_frame_id", "rows": len(rows)}
    return rows

def analyze(rows):
    first, last = rows[0][0], rows[-1][0]
    frames = {f for f, _ in rows}
    onset = []
    previous = 0
    previous_frame = None
    for frame, blink in rows:
        if blink > 0 and (blink != previous or previous_frame is None or frame != previous_frame + 1):
            onset.append(frame)
        previous, previous_frame = blink, frame
    full = (last - first + 1) // FRAME_WINDOW
    windows = []
    for k in range(full):
        start = first + k * FRAME_WINDOW
        end = start + FRAME_WINDOW
        if all(f in frames for f in range(start, end)):
            windows.append({"start": start, "end_exclusive": end,
                            "count": sum(start <= f < end for f in onset)})
    counts = [w["count"] for w in windows]
    mu = mean(counts) if counts else None
    variance = mean([(x-mu)**2 for x in counts]) if counts else None
    return {
        "first_frame": first, "last_frame": last, "annotated_frames": len(rows),
        "missing_frames": last-first+1-len(rows),
        "blink_onsets": onset, "full_candidate_windows": full, "windows": windows,
        "eligible_windows": len(windows), "mean_count": mu,
        "population_variance": variance,
        "fano": variance/mu if mu is not None and mu > 0 else None,
        "zero_fraction": counts.count(0)/len(counts) if counts else None,
        "poisson_zero": math.exp(-mu) if mu is not None else None
    }

def main():
    manifest = {"dataset": "EyeBlink8", "source_url": URL, "license": "GPL-3.0 per official research page",
                "frozen_protocol": "research/e002-170/PROTOCOL.md",
                "frame_window": FRAME_WINDOW, "assumed_fps": 30,
                "fps_certified": False, "date_utc": __import__("datetime").datetime.now(
                    __import__("datetime").timezone.utc).isoformat(),
                "archive": None, "entries": [], "errors": []}
    summary = {"status": "NOT_EVALUABLE", "scientific_gate": "NOT_RUN",
               "reason": "", "videos": {}, "pooled": {}}
    try:
        manifest["archive"] = fetch()
        with zipfile.ZipFile(ZIP) as z:
            for info in z.infolist():
                entry = {"path": info.filename, "size": info.file_size,
                         "compressed_size": info.compress_size, "crc32": format(info.CRC, "08x")}
                if info.is_dir():
                    manifest["entries"].append(entry); continue
                if info.file_size <= MAX_TEXT and pathlib.PurePosixPath(info.filename).suffix.lower() in (".txt", ".ann", ".csv"):
                    data = z.read(info)
                    entry["sha256"] = sha256(data)
                    decoded = data.decode("utf-8", errors="replace")
                    parsed = parse_annotations(decoded)
                    if isinstance(parsed, list):
                        entry["annotation_rows"] = len(parsed)
                        entry["parsed"] = True
                        summary["videos"][info.filename] = analyze(parsed)
                    elif isinstance(parsed, dict):
                        entry["parse_error"] = parsed
                        manifest["errors"].append({"entry": info.filename, **parsed})
                manifest["entries"].append(entry)
        if summary["videos"]:
            all_windows = [w for v in summary["videos"].values() for w in v["windows"]]
            observed = sum(w["count"] == 0 for w in all_windows) / len(all_windows) if all_windows else None
            predicted = sum(v["eligible_windows"] * v["poisson_zero"] for v in summary["videos"].values()
                            if v["poisson_zero"] is not None) / len(all_windows) if all_windows else None
            summary["pooled"] = {
                "videos": len(summary["videos"]),
                "annotated_frames": sum(v["annotated_frames"] for v in summary["videos"].values()),
                "blink_onsets": sum(len(v["blink_onsets"]) for v in summary["videos"].values()),
                "eligible_windows": len(all_windows),
                "observed_zero_fraction": observed,
                "poisson_predicted_zero_fraction": predicted,
                "zero_fraction_difference": observed-predicted if observed is not None else None
            }
            summary["status"] = "EVALUABLE" if len(all_windows) >= 8 else "NOT_EVALUABLE"
            summary["reason"] = "" if summary["status"] == "EVALUABLE" else "insufficient complete 150-frame windows"
            flagged = any(v["fano"] is not None and (v["fano"] < .67 or v["fano"] > 1.5)
                          for v in summary["videos"].values())
            if observed is not None and abs(observed-predicted) > .10: flagged = True
            summary["scientific_gate"] = "DESCRIPTIVE_FLAG" if flagged else "NO_DESCRIPTIVE_FLAG"
        else:
            summary["reason"] = "no qualifying 19-field original annotation text found in downloaded archive"
    except Exception as exc:
        summary["status"] = "BLOCKED_DATA_ACCESS"
        summary["scientific_gate"] = "NOT_RUN"
        summary["reason"] = type(exc).__name__ + ": " + str(exc)[:700]
        manifest["errors"].append(summary["reason"])
    finally:
        save("SOURCE_MANIFEST.json", manifest)
        save("RESULTS.json", summary)
        print(json.dumps({"status": summary["status"], "reason": summary["reason"],
                          "pooled": summary["pooled"], "scientific_gate": summary["scientific_gate"]}, indent=2))

if __name__ == "__main__": main()
