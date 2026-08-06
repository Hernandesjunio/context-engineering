---
id: KNOWLEDGE-SIGNALR-001
name: SignalR em Operações Assíncronas
type: knowledge
description: Fundamenta o uso de SignalR como canal de atualização com reconciliação por estado durável.
temperature: warm
authority: advisory
owner: backend-platform
status: approved
version: 1.0.0
---

# SignalR em Operações Assíncronas

## Papel

SignalR reduz a latência percebida ao enviar progresso e conclusão para clientes conectados.

## Limite

Uma conexão pode cair e um evento pode não chegar. O estado persistido e consultável pela API continua sendo a fonte de verdade.

## Reconciliação

- O evento carrega `jobId` e versão monotônica.
- O cliente ignora evento antigo ou duplicado.
- Ao reconectar, o cliente consulta `statusUrl`.
