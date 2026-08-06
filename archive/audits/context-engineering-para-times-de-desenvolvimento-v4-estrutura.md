---
title: Estrutura editorial da V4
author: Hernandes Junio de Assis
version: 4.0.0
---

# Estrutura Editorial da V4

## Objetivo

Levar um desenvolvedor iniciante de um modelo mental simples até a execução auditável de contexto no Cursor, sem confundir organização de arquivos com comportamento do runtime.

## Progressão

1. **Orientação:** público, rotas de leitura, limites e vocabulário mínimo.
2. **Oficina desorganizada:** responsabilidades misturadas e separação lúdica.
3. **Ponte técnica:** contexto, progressive disclosure, temperatura e custo como hipótese.
4. **Cursor executável:** mecanismos nativos, convenções curadas e primeiro checkpoint.
5. **Artefatos verificáveis:** agent, playbook, skill, knowledge, rule e contract.
6. **Avaliação:** origem das assertions, Eval Spec, captura e Evidence Record.
7. **Caso assíncrono:** API, job, persistência, SignalR, reconciliação e evidência.
8. **Governança:** classificação híbrida, autoridade, escrita, orçamento e adoção.
9. **Laboratórios:** Kit A, Kit B, templates, checklist e generalização.

## Linha narrativa

```mermaid
flowchart TD
    A[Manual caótico] --> B[Papéis explícitos]
    B --> C[Árvore .cursor]
    C --> D[Contexto carregado]
    D --> E[Execução observada]
    E --> F[Eval Spec]
    F --> G[Evidence Record]
```

## Decisões estruturais

| Decisão | Aplicação na V4 |
|---|---|
| Fonte única | Artefatos específicos ficam sob `.cursor/`; não existe `ai-context/`. |
| Playbook fora de knowledge | `.cursor/playbooks/` permanece no primeiro nível do contexto. |
| Host explícito | O Cursor é a implementação de referência. |
| Fronteira semântica | `CURSOR NATIVE`, `OPEN SPEC` e `BOOK ONTOLOGY`. |
| Schema canônico | Campos próprios do livro usam lowerCamelCase e `schemaVersion`. |
| Avaliação rastreável | Assertions ligam fonte original, artefato atual, método e verificador. |
| Caso semi-completo | Segurança e infraestrutura detalhadas permanecem fora do recorte. |
| Hands-on real | Kit A e Kit B existem como arquivos executáveis no pacote. |

## Recursos visuais

- Capa: oficina mecânica transformada em arquitetura modular de contexto.
- Diagrama 1: caos versus separação por responsabilidade.
- Diagrama 2: montagem de contexto no Cursor.
- Diagrama 3: árvore `.cursor/` e fronteira nativo/curado.
- Diagrama 4: origem dos campos de Eval.
- Diagrama 5: sequência persistir → confirmar → notificar → reconciliar.
- Diagrama 6: adoção POC → piloto → padrão controlado.

## Critério de conclusão editorial

- Um iniciante consegue nomear o consumidor de cada artefato.
- O livro não apresenta frontmatter como garantia de cache ou roteamento.
- O caso assíncrono termina em Evidence Record comparável.
- Os exemplos próprios usam um schema consistente.
- O laboratório executa sem dependências externas além de Python e PyYAML.
