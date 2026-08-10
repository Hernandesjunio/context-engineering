#!/usr/bin/env python3
from pathlib import Path
import json
import subprocess
import sys
import yaml

cursor = Path(__file__).resolve().parents[1]

def fail(message):
    print("FAIL", message)
    return 1

errors = 0
eval_spec = yaml.safe_load((cursor / "evals" / "eval-async-report.yaml").read_text(encoding="utf-8"))
required_eval = {"schemaVersion", "id", "name", "agentUnderEvaluation", "query", "assertions", "expected", "evaluationMethod", "verifyWith"}
missing_eval = required_eval - set(eval_spec)
if missing_eval:
    errors += fail(f"Eval Spec sem campos: {sorted(missing_eval)}")

assertion_ids = {item["id"] for item in eval_spec.get("assertions", [])}
expected_ids = set(eval_spec.get("expected", {}).get("mustApply", [])) | set(eval_spec.get("expected", {}).get("mustNotClaim", []))
if not expected_ids <= assertion_ids:
    errors += fail(f"Assertions sem definição: {sorted(expected_ids - assertion_ids)}")

schema = json.loads((cursor / "contracts" / "schemas" / "evidence-record.schema.json").read_text(encoding="utf-8"))
evidence = json.loads((cursor / "evidence" / "EV-ASYNC-REPORT-001.json").read_text(encoding="utf-8"))
missing_evidence = [field for field in schema["required"] if field not in evidence]
if missing_evidence:
    errors += fail(f"Evidence Record sem campos: {missing_evidence}")
if evidence.get("schemaVersion") != "1.0.0" or evidence.get("verdict") not in {"PASS", "FAIL", "INCONCLUSIVE"}:
    errors += fail("Evidence Record com versão ou veredito inválido")
observed = evidence.get("observed", {})
if observed.get("persistedCompletionSequence", 0) >= observed.get("notificationPublishedSequence", 0):
    errors += fail("Evidence Record não comprova persistência antes da notificação")

rule = (cursor / "rules" / "async-durable-state.mdc").read_text(encoding="utf-8")
if "RULE-ASYNC-001" not in rule or "antes de publicar" not in rule:
    errors += fail("Project Rule perdeu vínculo ou obrigação canônica")

contract_check = subprocess.run([sys.executable, str(cursor / "skills" / "validate-api-contract" / "scripts" / "validate_contract.py")], text=True, capture_output=True)
print(contract_check.stdout.strip())
if contract_check.returncode:
    errors += 1

if errors:
    sys.exit(1)
print("PASS laboratório V5 Beta 2")
