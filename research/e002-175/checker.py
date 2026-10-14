import csv
import json
from pathlib import Path
p = Path(__file__).parent
result = json.loads((p / "RESULTS.json").read_text())
for filename, field in [("data_loss_per_trial.csv", "prop_missing_data"), ("data_quality_validation.csv", "Prop_data_loss_left_eye")]:
    with (p / filename).open() as stream:
        rows = list(csv.DictReader(stream))
    observed = sum(float(row[field]) < 0 or float(row[field]) > 1 for row in rows if row.get(field, "").strip())
    assert observed == result["fraction_checks"][field]["violations"]
print("PASS")
