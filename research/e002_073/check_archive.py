"""Public archive metadata preflight, no user data."""
import hashlib
import json
import urllib.request
from pathlib import Path

URL = "https://zenodo.org/records/20492528/files/human_eyeregion_pupil_segmentation_dataset.zip?download=1"
EXPECTED_BYTES = 137446558
EXPECTED_MD5 = "a30eafe5e71cef9de1e08b91988f88b6"

def main():
    out = Path("e002_073_results")
    out.mkdir(exist_ok=True)
    target = out / "source.zip"
    if not target.exists():
        urllib.request.urlretrieve(URL, target)
    h = hashlib.md5()
    with target.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    result = {"bytes": target.stat().st_size, "md5": h.hexdigest()}
    result["pass"] = result["bytes"] == EXPECTED_BYTES and result["md5"] == EXPECTED_MD5
    (out / "results.json").write_text(json.dumps(result, indent=2))
    print(json.dumps(result))
    if not result["pass"]:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
