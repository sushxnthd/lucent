"""CI gate for the preregistered E002-380 synthetic measurement kernel."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_e002_380_exact_oracle():
    subprocess.run([sys.executable, str(ROOT/"research/observability/e002_380_exact.py")],check=True,timeout=120)

def test_e002_380_instrument():
    subprocess.run([sys.executable, str(ROOT/"research/observability/e002_380_instrument.py")],check=True,timeout=120)

def test_e002_380_camera_abstention():
    subprocess.run([sys.executable, str(ROOT/"research/observability/e002_380_certificate.py")],check=True,timeout=120)
