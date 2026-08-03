# Auditoria editorial e técnica - Edição V3

**Autor do E-book:** Hernandes Junio de Assis  
**Data da auditoria:** 2026-08-03  
**Escopo:** progressão editorial, frontmatter, anatomia opcional de skills, consistência do PDF e da apresentação.

## Veredito

**PASS com ressalva operacional.** A V3 está coerente para orientar a curadoria da POC e satisfaz as invariantes editoriais definidas. A estrutura ampliada de `SKILL.md` é tecnicamente viável como convenção interna, mas não deve ser apresentada como requisito oficial nem como garantia de recuperação perfeita. Sua eficácia precisa ser comprovada no cliente utilizado por meio de evals de ativação, recuperação, aplicação e custo.

## Análise incremental dos ajustes

| Ponto | Avaliação | Fundamento técnico | Decisão aplicada |
|---|---|---|---|
| Fundir o manual caótico ao texto anterior | Procede. | Problema e artefato ficam no mesmo ciclo de atenção; o leitor não precisa manter a descrição na memória até outro subtítulo. | O título intermediário foi removido; o hook conduz diretamente ao bloco `markdown`. |
| Adicionar `name` aos artefatos | Procede, com distinção. | `id` oferece identidade técnica estável; `name` melhora catálogo e leitura. Alterar um título não deve quebrar relações por ID. | Agent, playbook, knowledge, rule, contract e eval passaram a usar `id` + `name`. |
| Usar `name` em Agent Skills | Obrigatório, mas não em Pascal Case. | A especificação exige `name` e `description`; o `name` deve ser kebab-case, coincidir com o diretório e respeitar os limites publicados. | `name` interoperável permanece no YAML; o título humano fica no H1 ou em `metadata.display-name`. |
| Anatomia ampliada da skill | Viável como aprofundamento opcional. | O corpo do `SKILL.md` é livre e pode reunir escopo, fluxo, guardrails e verificação; carregar tudo sem critério recriaria um arquivo monolítico. | Foi adicionada uma seção “Para curiosos”, explicitamente classificada como convenção interna. |
| Catálogo HOT/WARM/COLD + outros eixos | Coerente após correção de nomenclatura. | Temperatura, acesso e autoridade respondem a perguntas independentes. `NORMATIVE` não é um valor de “semantic”; é autoridade. | O catálogo usa `Tier`, `Access`, `Authority`, `Abrir quando` e `Path`. |
| Frontmatter para roteamento MCP | Parcialmente correto. | YAML próprio só produz efeito se o harness o interpretar. MCP expõe tools e resources por contratos do protocolo; não consome automaticamente frontmatter arbitrário. | O E-book inclui um aviso explícito e orienta alinhar catálogo, schemas e descrições. |
| Convenção de Markdown e delimitadores | A ausência era uma lacuna prática para iniciantes. | Nomear uma construção sem mostrar sua sintaxe literal não garante transferência para uso real. Delimitadores consistentes reduzem ambiguidade, mas não criam autoridade nem segurança. | A seção 7.4.1 foi restaurada e ampliada com crases, asteriscos, checklists, chaves, comentários e tags XML-like. |

## Avaliação da anatomia ampliada de Skill

### Componentes aprovados

- **Quando usar / quando não usar:** reduz colisão entre capacidades vizinhas.
- **Sinais de ativação:** melhora descoberta quando descreve situações e exemplos, não apenas palavras-chave.
- **Guardrails NORMATIVE:** concentra limites da capacidade, desde que referencie a fonte canônica.
- **Recursos empacotados:** evita que o agente presuma `scripts/`, `references/` ou `assets/` inexistentes.
- **Catálogo progressivo:** torna explícita a política de abertura sob demanda.
- **Receitas compactas:** oferecem atalhos operacionais quando apontam para regra vigente.
- **Avisos de saída:** protegem comunicação obrigatória quando aplicados condicionalmente.
- **Perguntas e stop conditions:** impedem execução baseada em hipóteses materiais.
- **Checklist final:** reduz omissões e torna a conclusão revisável.

### Correções necessárias para não criar um novo monólito

1. **Acrescentar entradas, fluxo principal, saída e Definition of Done.** A proposta original descrevia ativação e revisão, mas não fechava integralmente o contrato de operação.
2. **Aplicar “descobrir -> verificar -> perguntar”.** Perguntas não devem consumir interação quando a resposta existe no repositório ou em uma tool autorizada.
3. **Referenciar rules compartilhadas.** Duplicar portas, métricas, políticas de secrets e padrões de HPA em todas as skills cria drift.
4. **Diferenciar aviso obrigatório de aviso condicional.** Repetir disclaimers irrelevantes em toda saída aumenta ruído e reduz atenção.
5. **Vincular checklist a evidência.** Sempre que possível, cada item deve apontar comando, arquivo, ID de rule ou resultado observável.

## Contrato recomendado de metadados

| Artefato | Identidade técnica | Nome legível | Descrição | Observação |
|---|---|---|---|---|
| Agent Skills `SKILL.md` | `name` da especificação | H1 ou `metadata.display-name` | `description` obrigatória | Campos próprios ficam em `metadata` para maior portabilidade. |
| Agent, playbook, knowledge, rule | `id` | `name` | Recomendada | Convenção interna; deve ser validada pelo catálogo da equipe. |
| Contract e eval | `id` | `name` | Recomendada no catálogo | O corpo continua orientado a condições e resultados observáveis. |
| Evidence Record de execução | `evidenceId` | Não obrigatório | Não aplicável por registro | É instância auditável, não capacidade descoberta por nome. |

## Riscos residuais da POC

- **Portabilidade:** clientes podem interpretar extensões de metadados de maneiras diferentes.
- **Superativação:** descrição e sinais amplos podem ativar skills em tarefas vizinhas.
- **Subativação:** descrições estreitas podem ocultar uma skill válida.
- **Drift:** receita HOT copiada de uma rule pode ficar desatualizada.
- **Custo:** mais arquivos podem economizar contexto ou gerar leituras adicionais; medir custo por tarefa válida.
- **Confiança:** conteúdo de repositório deve passar por política de trust antes de ser injetado como instrução.

## Definition of Done para adoção na POC

- [ ] O validador oficial aceita o frontmatter das skills.
- [ ] `name` coincide com o diretório e `description` explica o que faz e quando usar.
- [ ] O catálogo interno distingue `id`, `name`, `type`, autoridade e temperatura.
- [ ] Todos os caminhos listados no pacote existem.
- [ ] Evals positivos, negativos e por sinônimo exercitam ativação e recuperação.
- [ ] Evals de aplicação comprovam respeito a guardrails e stop conditions.
- [ ] Evidence Records registram artefatos recuperados, tools, testes e resultado.
- [ ] O mesmo corpus é testado no cliente realmente usado pelo time.
- [ ] Latência, tokens, leituras e taxa de conclusão são comparados com a baseline.
- [ ] Existe rollback para a versão anterior do contexto.

## Evidence Record Editorial

```json
{
  "editorialAudit": {
    "antiPatternFormat": "Validado - manual mecânico no bloco markdown com alerta na linha 112; backend no bloco markdown com alerta na linha 607",
    "playbooksRootLevel": "Validado - playbooks/ permanece no nível raiz da árvore mínima, linha 591",
    "noExcessiveSubsections": "Validado - references/, scripts/ e assets/ permanecem em bullets na seção Anatomia dos pacotes, iniciada na linha 814",
    "frontmatterExplained": "Validado - seção YAML frontmatter na linha 837; distinção id/name na linha 854; exemplos para skill, playbook e rule nas linhas 870-924",
    "evidenceRecordPromptFound": "Validado - ATUE COMO UM AUDITOR DE; prompt prático iniciado na linha 1196"
  }
}
```

## Evidências de entrega

- Manuscrito: 11.803 palavras e 2.122 linhas na versão final.
- PDF: 62 páginas; todas renderizadas e inspecionadas visualmente.
- PPTX: 18 slides; sem overflow; fidelidade ao deck-base aprovada sem desvios estruturais.
- Frontmatters reutilizáveis: todos os exemplos com `id` passaram a possuir `name` na linha imediatamente seguinte.

## Referências técnicas principais

- [Agent Skills - Specification](https://agentskills.io/specification)
- [Agent Skills - How to add skills support to your agent](https://agentskills.io/client-implementation/adding-skills-support)
- [Model Context Protocol - Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
- [Model Context Protocol - Resources](https://modelcontextprotocol.io/specification/2026-07-28/server/resources)
- [Anthropic - Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
