---
id: PLAYBOOK-ASYNC-001
name: Operação Assíncrona de Relatório
type: playbook
description: Coordena aceitação, processamento, persistência, notificação e reconciliação de relatórios longos.
temperature: warm
authority: normative
owner: backend-platform
status: approved
version: 1.0.0
---

# Operação Assíncrona de Relatório

## Quando usar

- Quando a geração não puder concluir no tempo síncrono esperado.
- Quando o front-end precisar de progresso ou conclusão em tempo real.

## Pré-condições

- Contract de entrada aprovado.
- Política de idempotência definida.
- Estados e autorização conhecidos.

## Fluxo

1. Validar a solicitação.
2. Criar o job durável.
3. Retornar `202`, `jobId` e `statusUrl`.
4. Processar com correlação.
5. Persistir o resultado final.
6. Confirmar o commit.
7. Publicar notificação SignalR.
8. Reconciliar por API em reconexão ou dúvida.

## Stop conditions

- Pare se o job não puder ser consultado depois da aceitação.
- Pare se não houver evidência de commit antes da notificação.

## Evidence

- Capture transições, commit, publicação, consulta de status e testes.
