#!/usr/bin/env python3
from pathlib import Path
import sys
import yaml

root = Path(__file__).resolve().parents[3]
path = root / "contracts" / "report-request.contract.yaml"
data = yaml.safe_load(path.read_text(encoding="utf-8"))
required = ["schemaVersion", "id", "name", "operation", "input", "output", "preconditions", "postconditions", "forbidden", "observability"]
missing = [key for key in required if key not in data]
accepted = data.get("output", {}).get("accepted", {})
if accepted.get("status") != 202:
    missing.append("output.accepted.status=202")
for field in ("jobId", "statusUrl"):
    if field not in accepted.get("required", []):
        missing.append(f"output.accepted.required:{field}")
if missing:
    print("FAIL", ", ".join(missing))
    sys.exit(1)
print("PASS", path)
