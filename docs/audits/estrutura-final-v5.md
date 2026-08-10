# Estrutura final — Context Engineering V5

## Identidade do produto

O material passa a ser um **sistema editorial em dois volumes complementares**:

1. **Livro principal — Context Engineering para Times de Desenvolvimento:** compreensão, decisões, modelo mental, microexemplos e governança.
2. **Workbook de Context Engineering:** prompts, YAML, JSON, templates, execuções, Evals, Evidence Records e laboratórios reproduzíveis.

A pasta `lab/` é a fonte canônica dos artefatos completos executáveis. A baseline Beta 3 permanece congelada em `sources/`.

## Livro principal — macroestrutura

1. Como ler: três rotas e funções dos marcadores.
2. Introdução: por que documentação abundante não equivale a contexto utilizável.
3. Parte I — oficina desorganizada:
   - manual monolítico;
   - cartão operacional, ordem de serviço, capacidade e manual consultivo;
   - teste e laudo;
   - anti-pattern e jornada guiada;
   - limites da metáfora.
4. Parte II — ponte para engenharia de contexto:
   - contexto além do prompt;
   - HOT/WARM/COLD;
   - autoridade separada de temperatura;
   - progressive disclosure e seus limites;
   - árvore Cursor-first.
5. Parte III — contexto executável:
   - mecanismos nativos versus ontologia do livro;
   - host, runtime, participação e evidência;
   - fluxo essencial em quatro movimentos;
   - catálogo dos nove artefatos;
   - anti-pattern backend caótico;
   - frontmatter e contrato do consumidor;
   - microfluxo Contract → Assertion → Eval → Evidence;
   - recuperação, aplicação e resultado;
   - aprofundamento sobre verificadores.
6. Parte IV — estudo assíncrono resumido:
   - requisito;
   - aceitação e conclusão;
   - estados, transições e edge cases;
   - massa progressiva;
   - captura, Eval e Evidence do caso.
7. Parte V — governança e operação:
   - classificação híbrida;
   - autoridade e conflitos;
   - metadados e convenções;
   - orçamento de contexto;
   - ciclo de vida e refatoração;
   - loops controlados;
   - adoção por gates;
   - antipadrões e critérios de sucesso.
8. Workbook e laboratórios: orientação para o companion.
9. Checklist do curador, glossário, conclusão e referências.

## Workbook — macroestrutura

1. Como usar, pré-requisitos e ordem recomendada.
2. Laboratório 1 — contexto mínimo executável.
3. Artefatos e testes focados:
   - Agent, Playbook, Skill, Knowledge e Rule;
   - frontmatter e anatomia de pacotes;
   - Contracts, Assertions, Evals e Evidence Records.
4. Laboratório 2 — estudo assíncrono completo.
5. Laboratório 3 — kits e templates:
   - contexto sob avaliação;
   - harness;
   - templates mínimos e ampliados;
   - laboratório Agent HOT.
6. Checklist do curador e referências.

## Política de navegação

| Rota | Deve permitir | Não deve exigir |
|---|---|---|
| ESSENCIAL | explicar os papéis, classificar temperatura e acompanhar expectativa → evidência | copiar schemas extensos ou executar o Cursor |
| APROFUNDAMENTO | avaliar conflitos, verificadores, orçamento e governança | conhecimento necessário para compreender o capítulo seguinte |
| HANDS-ON | reproduzir artefatos e registrar resultados | manter o livro principal aberto na mesma página |

## Linha de raciocínio preservada

```text
problema observável
→ modelo mental
→ tradução técnica
→ mecanismo de execução
→ restrições verificáveis
→ avaliação
→ evidência
→ governança
```

