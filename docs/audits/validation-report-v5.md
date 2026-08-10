# Relatório de validação — V5

## Veredito

`PASS_FOR_V5_RELEASE`

A V5 foi aprovada pelo autor e encerrada como release `5.0.0`. Teste formal com leitores representativos e PDF tagged permanecem limitações conhecidas e registradas; não foram tratados como evidência já executada.

## Baseline

- Fonte: `sources/context-engineering-v5-beta3-frozen.md`.
- SHA-256: `578e37d6ff7aabc49dae4f20d34e9f5b83c6672df5a5de77227a40a4f5f765ba`.
- Estado original: 6.482 linhas, cerca de 37.949 palavras Markdown e 136 páginas A4.

## Saídas

| Volume | Linhas | Palavras | Páginas | SHA-256 PDF |
|---|---:|---:|---:|---|
| Livro principal | 2.685 | 17.179 | 66 | `18e134f0cf9133eaa66b8abad6461fe2f03e40e9e8a305769b21027106e0ad75` |
| Workbook | 4.646 | 25.231 | 96 | `540d3429503a3af510053de902c60ed65f7b5ea7dbcaca8c9731bc3ebac30629` |

As palavras não devem ser somadas como conteúdo totalmente único: definições e referências mínimas reaparecem quando necessárias para tornar o workbook utilizável.

## Checks determinísticos

| Check | Resultado |
|---|---|
| Hash da baseline | PASS |
| 171 títulos inventariados | PASS |
| Hierarquia de headings | PASS nos dois volumes |
| Cercas de código | PASS |
| Fenced divs | PASS |
| Imagens referenciadas | PASS |
| Python compile | PASS |
| Laboratório Cursor-first | PASS |
| Markdown → LaTeX → PDF em duas passagens | PASS |
| PDF A4 | PASS |
| Overfull hbox | 0 nos dois volumes |
| Painéis de código medidos | 271 |
| Caracteres de painel medidos | 66.210 |
| Menor folga direita observada | 7,97 pt |
| Páginas renderizadas | 162/162 |
| Páginas inválidas | 0 |

## Revisão visual

Foram inspecionadas as duas contact sheets integrais e, em alta resolução:

- capa e sumário;
- abertura da Parte III;
- catálogo de artefatos;
- microfluxo Contract → Assertion → Eval → Evidence;
- tabelas do estudo assíncrono;
- blocos YAML/JSON multipágina;
- callouts corrigidos de Playbook, rota essencial e auditabilidade;
- Figura 7.1 e sua curva de retorno;
- bloco “Contexto mínimo executável — expectativa” e outros blocos com linhas longas;
- bloco “Crie a Skill” indicado pelo autor;
- painéis com a menor folga direita de cada volume;
- páginas associadas aos avisos verticais do LaTeX.

Resultado observado:

- fundo cinza de código presente;
- padding presente;
- syntax highlighting legível;
- zebra striping sutil presente;
- cabeçalhos e regras horizontais preservados;
- nenhum texto cortado ou sobreposto;
- linhas longas de blocos cercados quebradas dentro das margens;
- curva de retorno da Figura 7.1 afastada do rótulo central;
- nenhum callout órfão após a correção final;
- nenhum marcador estrutural vazando como texto fora de exemplos literais.

## Achados corrigidos durante a validação

1. Salto de H1 para H3 na seção de frontmatter.
2. Fundo `Shaded` configurado, mas não aplicado efetivamente.
3. Ausência de zebra striping.
4. Overflows horizontais em prosa densa.
5. Callout da rota essencial dividido com uma linha órfã.
6. Fenced div “Regra prática” sem fechamento na baseline.
7. Outros três callouts sem fechamento e um exemplo literal incompleto.
8. Curva de retorno da Figura 7.1 muito próxima do rótulo central.
9. Cobertura parcial da primeira regra de quebra e validação baseada apenas em exemplos/logs.
10. Quebra global ampliada para `FancyVerb`, grupos do highlighter e tokens não espaçados, seguida de medição geométrica integral.

## Validação semântica dos resumos

Cada trecho condensado foi checado contra os invariantes canônicos:

- HOT/WARM/COLD continua sendo política de carregamento, não autoridade;
- progressive disclosure não garante recuperação, custo ou qualidade;
- frontmatter não garante cache nem roteamento;
- `202 Accepted` não comprova conclusão nem durabilidade;
- SignalR permanece uma otimização de notificação no estudo;
- resultado funcional correto não prova lineage;
- LLM-as-a-Judge permanece probabilístico e versionado;
- Evidence Record separa expected, observed, checks, verdict e limitações.

Nenhuma ideia principal foi removida dos conceitos essenciais; a execução detalhada foi preservada no workbook e na baseline congelada.

## Limitações aceitas e evolução futura

1. Testar três tarefas com leitores representativos em uma futura avaliação editorial.
2. Definir previamente os critérios de sucesso do teste, sem percentual universal.
3. Avaliar PDF tagged em uma futura revisão de acessibilidade.
4. Revalidar documentação do Cursor na data de publicação.
5. Incorporar feedback do autor sem alterar silenciosamente Assertions e critérios já preservados.
