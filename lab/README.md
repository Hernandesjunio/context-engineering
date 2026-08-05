# Laboratório V4 — Context Engineering no Cursor

## Objetivo

Executar o caso assíncrono do e-book com uma única fonte de contexto em `.cursor/` e produzir um Evidence Record validado.

## Componentes

- **Kit A:** `backend-development`, rule, skill, playbook, knowledge, contract e Eval Spec.
- **Kit B:** `context-evaluation`, skill de auditoria, schemas e validadores.

## Execução

1. Abra esta pasta como repositório no Cursor.
2. Use a query de `.cursor/evals/eval-async-report.yaml` com o agente backend.
3. Substitua a fixture pelos fatos capturados da execução.
4. Execute `python .cursor/hooks/validate_lab.py`.
5. Use o agente de avaliação para comparar esperado e observado.
6. Grave o resultado em `.cursor/evidence/` e execute o validador novamente.

## Limite

O laboratório é didático e não inclui autenticação completa, infraestrutura, deploy ou política corporativa de retenção.
