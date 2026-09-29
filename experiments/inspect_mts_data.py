"""Inspect one public Massoz et al. eyelid-distance sequence.

The public repository accompanying Massoz et al. (Sensors, 2018) includes
Torch7-serialized eyelid-distance sequences and reaction-time logs. This
script verifies that the data can be loaded without copying the dataset into
Lucent.

Citation:
Q. Massoz, J. G. Verly, M. Van Droogenbroeck,
"Multi-Timescale Drowsiness Characterization Based on a Video of a Driver's Face,"
Sensors 18(9):2801, 2018.
"""

from __future__ import annotations

import tempfile
import urllib.request
from pathlib import Path

import numpy as np
import torchfile


BASE = "https://raw.githubusercontent.com/QMassoz/mts-drowsiness/master/data/raw"


def download(url: str, target: Path) -> None:
    with urllib.request.urlopen(url, timeout=60) as response:
        target.write_bytes(response.read())


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        sequence_path = root / "1-1.t7"
        rt_path = root / "1-1.txt"

        download(f"{BASE}/eld-seq/1-1.t7", sequence_path)
        download(f"{BASE}/rt/1-1.txt", rt_path)

        sequence = torchfile.load(str(sequence_path))
        array = np.asarray(sequence)

        print("MTS public-data inspection")
        print("=" * 60)
        print(f"sequence type: {type(sequence)!r}")
        print(f"shape: {array.shape}")
        print(f"dtype: {array.dtype}")
        print(f"finite: {np.isfinite(array).all()}")
        print(f"min: {np.nanmin(array):.6f}")
        print(f"max: {np.nanmax(array):.6f}")
        print(f"mean: {np.nanmean(array):.6f}")

        lines = rt_path.read_text(encoding="utf-8").splitlines()
        print(f"reaction-time lines: {len(lines)}")
        print("first reaction-time line:")
        print(lines[0] if lines else "<empty>")


if __name__ == "__main__":
    main()
