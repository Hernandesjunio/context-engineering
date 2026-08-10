---
name: audit-context-execution
description: Audit an observed agent execution against an approved Eval Spec, checking retrieved artifacts, applied and forbidden assertions, tool facts, tests, and final state. Use after an Eval Runner has captured evidence; do not use to invent missing traces or rerun the agent silently.
---

# Auditar Execução de Contexto

## Entradas

- `.cursor/evals/eval-async-report.yaml`.
- `.cursor/evals/fixtures/async-report-observed.json`.
- Schema canônico em `.cursor/contracts/schemas/evidence-record.schema.json`.

## Procedimento

1. Valide os arquivos por código.
2. Compare `expected` e `observed` por ID.
3. Julgue semanticamente apenas o significado não coberto por checks exatos.
4. Use `PASS`, `FAIL` ou `INCONCLUSIVE`.
5. Registre evidência ausente e próxima camada a corrigir.

## Guardrails

- Não invente arquivo, tool, trace, teste ou resultado.
- Não use cadeia de pensamento como evidência.
- Não registre payload sensível desnecessário.

## Recursos empacotados

- `references/semantic-criteria.md`: fronteira entre avaliação determinística e semântica.
- `scripts/validate_evidence.py`: validação do schema.
- O schema não é duplicado na skill; a fonte canônica fica em `.cursor/contracts/schemas/`.
