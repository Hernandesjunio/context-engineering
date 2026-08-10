# Guia de Contrato HTTP Assíncrono

## Aceitação

- `202 Accepted` confirma aceitação e criação de um job recuperável.
- A resposta deve fornecer `jobId` e `statusUrl`.

## Conclusão

- A conclusão deve permanecer consultável por API.
- Notificação em tempo real reduz latência percebida, mas não substitui estado durável.

## Compatibilidade

- Mudanças de schema devem declarar consumidores afetados.
- Campos novos obrigatórios exigem estratégia de versão ou migração.
