#!/usr/bin/env python3
from pathlib import Path
import json
import sys

root = Path(__file__).resolve().parents[3]
schema_path = root / "contracts" / "schemas" / "evidence-record.schema.json"
evidence_path = root / "evidence" / "EV-ASYNC-REPORT-001.json"
schema = json.loads(schema_path.read_text(encoding="utf-8"))
evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
missing = [field for field in schema["required"] if field not in evidence]
if missing:
    print("FAIL campos ausentes", ", ".join(missing))
    sys.exit(1)
if evidence["schemaVersion"] != "1.0.0" or evidence["verdict"] not in {"PASS", "FAIL", "INCONCLUSIVE"}:
    print("FAIL versão ou veredito inválido")
    sys.exit(1)
for section in ("expected", "observed"):
    if not isinstance(evidence.get(section), dict):
        print("FAIL", section, "deve ser objeto")
        sys.exit(1)
print("PASS", evidence_path)
