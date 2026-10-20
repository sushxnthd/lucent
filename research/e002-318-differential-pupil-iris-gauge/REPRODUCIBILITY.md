# Reproduction and integrity

Install public packages NumPy and SymPy in a clean Python 3 environment. In this directory run:

    python experiments.py
    python independent_checker.py

Both scripts overwrite their respective JSON result files. The random seeds are fixed (318 and 118). Full RGB frames are generated deterministically and compared bitwise, not stored as large image binaries. The exact rational witness is in RAW_WITNESS.json. Source scripts are the authoritative raw-data generator. The separate complete downloadable package has SHA256SUMS.txt.

Gates: synthetic and symbolic tests passed locally on 2026-10-20; **no human evidence**, no independent corneal/glasses calibration, and no field-level novelty. GitHub remote CI should be reported only after an actual check exists.