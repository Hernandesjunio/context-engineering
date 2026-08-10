---
name: validate-api-contract
description: Validate HTTP and OpenAPI contract changes, including status codes, headers, request and response schemas, idempotency, asynchronous 202 responses, and client compatibility. Use for API contract creation or modification; do not use for worker-only retry logic without an HTTP boundary.
---

# Validar Contrato de API

## Entradas

- Operação e consumidores.
- Contract canônico.
- Payloads válidos e inválidos.

## Procedimento

1. Leia `.cursor/contracts/report-request.contract.yaml`.
2. Compare entrada, saída, pré-condições, pós-condições e estados proibidos.
3. Execute `scripts/validate_contract.py`.
4. Registre comando, código de saída e divergências.

## Recursos empacotados

- `references/http-contract-guidance.md`: explicação sob demanda.
- `scripts/validate_contract.py`: validação determinística do exemplo.

## Definition of Done

- Contract válido.
- `202` não confundido com conclusão.
- `jobId` e `statusUrl` presentes.
- Evidência do validador registrada.
