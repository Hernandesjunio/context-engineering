# Context Tiering no Cursor

> 💡 **Visão geral:** organize o contexto do projeto com HOT, WARM e COLD, recuperando cada camada conforme a necessidade da tarefa.

## O que é

Projetos acumulam regras, planos, decisões e históricos. Nem todo esse material precisa participar de toda tarefa. Context tiering organiza **quando** um conteúdo deve ser recuperado:

- **HOT:** estado atual e instruções necessárias para começar.
- **WARM:** detalhes do trabalho atual, recuperados quando a tarefa indicar que são necessários.
- **COLD:** histórico e aprofundamento, recuperados por gatilho, investigação ou referência explícita.

O objetivo é reduzir ruído sem apagar conhecimento. O modelo não é um recurso nativo que garanta um comportamento completo do Cursor; é uma convenção implementada com arquivos, Rules, Skills e verificações.

Ele também não garante economia fixa de tokens, respostas melhores, ausência de alucinações ou recuperação perfeita. Esses efeitos precisam ser avaliados no Cursor, modelo e conjunto de tarefas usados pelo time.

> ⚠️ **Limite do modelo:** context tiering é uma convenção de organização; não garante economia fixa de tokens, qualidade da resposta, ausência de alucinações ou recuperação perfeita.

## A ideia central

Mantenha o estado atual pequeno em `MEMORY.md`, os documentos em andamento em `docs/active/` e o histórico em `docs/archived/`. Registre uma rota para que o histórico continue recuperável quando voltar a ser relevante.

Em geral:

1. o contexto HOT orienta o início;
2. uma Rule orienta o Agent a consultar o estado e os ponteiros;
3. uma Skill pode criar ou atualizar os artefatos e executar o arquivamento;
4. um checker determinístico confirma o estado do filesystem;
5. o usuário ou revisor confirma decisões semânticas e obrigações vigentes.

Consulte o [template completo de `MEMORY.md`](#template-completo-de-memory) no final deste documento.

> 📌 **Regra prática:** mantenha o estado atual pequeno, aponte para o trabalho ativo e recupere o histórico somente quando um gatilho tornar essa consulta relevante.

## Componentes e grau de automação

| Componente | Responsabilidade | O que é garantido |
|---|---|---|
| `MEMORY.md` | Estado atual, ponteiros e bloqueios. | Apenas o conteúdo escrito no arquivo. |
| Rule `alwaysApply` | Colocar a orientação de bootstrap no contexto das conversas. | A Rule é incluída; a execução de cada instrução pelo Agent não é garantida. |
| Skill | Criar, atualizar, mapear e arquivar contexto quando ativada. | O procedimento definido pela Skill, sujeito à execução e aos erros reportados. |
| `navigation-map.yaml` | Rotas, gatilhos e aplicabilidade. | Um catálogo legível; não é metadado nativo do Cursor. |
| `validate_archive.ps1` | Verificar origem e destino do arquivo. | Somente as condições determinísticas implementadas no script. |
| Revisão humana | Confirmar semântica, autoridade e conflitos. | Decisões que não podem ser provadas pelo checker. |

### Sobre `alwaysApply: true`

`alwaysApply: true` faz com que o texto da Rule seja incluído nas conversas aplicáveis. Isso não significa que o Cursor, por mecanismo próprio, abriu `MEMORY.md`, atualizou o mapa ou executou uma Skill. A Rule deve instruir o Agent a fazer essas ações, e o resultado deve ser observado ou verificado quando for importante.

Portanto, a descrição transparente é:

> ⚠️ **Transparência:** a Rule orienta a leitura de `MEMORY.md`; ela não é uma garantia determinística de leitura.

## Estrutura recomendada

O mapa de navegação é conhecimento do projeto, não configuração do Cursor. Por isso, recomenda-se mantê-lo junto da documentação:

```text
repository/
├── MEMORY.md
├── .cursorindexingignore
├── .cursor/
│   ├── rules/
│   │   └── context-bootstrap.mdc
│   └── skills/
│       └── context-tiering/
│           ├── SKILL.md
│           └── scripts/
│               └── validate_archive.ps1
└── docs/
    ├── active/
    ├── archived/
    └── context/
        └── navigation-map.yaml
```

Essa localização é uma recomendação de organização. O Cursor não exige esse path; o requisito importante é que a Rule e a Skill apontem para o mesmo arquivo e que o mapa permaneça fácil de revisar.

> 📌 **Organização recomendada:** mantenha Rule, Skill e mapa apontando para o mesmo arquivo, mesmo que o projeto escolha paths diferentes dos exemplos.

## O que deve ser configurado

### `MEMORY.md`

Use o template completo no final. Em resumo, ele deve conter apenas estado corrente, artefatos ativos, próxima ação, pendências e ponteiros para histórico relevante. Não replique nele uma arquitetura ou um manual.

### Rule de bootstrap

Uma Rule curta pode orientar o Agent:

```markdown
---
description: Orienta o bootstrap e a recuperação de contexto do projeto.
alwaysApply: true
---

Antes de planejar ou editar:
1. consulte `MEMORY.md`;
2. use os artefatos ativos indicados;
3. consulte `docs/context/navigation-map.yaml` quando houver gatilho;
4. leia COLD somente quando houver aplicabilidade ou solicitação explícita.
```

O texto é uma instrução para o Agent. Se `MEMORY.md` estiver ausente ou contraditório, a orientação deve ser parar e solicitar reconciliação.

### Skill de context tiering

A operação repetitiva pode ficar em uma Skill configurada para:

1. verificar o estado e os paths;
2. criar ou atualizar `MEMORY.md`;
3. criar ou atualizar `docs/context/navigation-map.yaml`;
4. preservar obrigações que ainda são ativas;
5. mover documentos concluídos de `docs/active/` para `docs/archived/`;
6. chamar o checker;
7. testar a referência ao arquivo arquivado;
8. reportar falha, conflito ou evidência insuficiente.

A Skill precisa ser ativada ou chamada. Ela não deve ser descrita como um processo automático do Cursor que ocorre sem execução do Agent.

Exemplo compacto de contrato:

```markdown
---
name: context-tiering
description: Mantém estado, rotas e arquivamento do contexto do projeto.
---

Use quando uma feature começar, mudar de fase ou for concluída.

Faça a alteração somente após preservar obrigações vigentes.
Atualize o mapa antes do movimento.
Execute o checker depois do movimento.
Pare em caso de conflito, destino diferente já existente ou falha do checker.
```

### Mapa de navegação

O mapa deve ser gerenciado pela Skill, não preenchido manualmente como rotina. Ele continua legível para o time e pode ser revisado quando uma rota ou uma obrigação mudar.

Exemplo mínimo em `docs/context/navigation-map.yaml`:

```yaml
routes:
  - triggers: ["FEATURE-042", "feature atual"]
    path: "docs/active/feature-042.md"
    access: lookup
  - triggers: ["Retry-After", "ADR-017"]
    path: "docs/archived/adr-017.md"
    access: deepdive
    authority: normative
    applicability: "Alteração do protocolo de consulta."
```

O mapa não faz o Cursor recuperar o arquivo por si só. Ele fornece à Rule, à Skill e ao Agent uma rota explícita e revisável.

### `.cursorindexingignore`

Quando o objetivo for retirar o histórico da indexação comum, a configuração pode ser:

```gitignore
docs/archived/
```

Essa configuração é uma proposta a validar na versão do Cursor usada. Faça teste positivo e negativo antes de adotá-la. Indexação reduzida não prova, sozinha, redução de tokens.

> ⚠️ **Valide antes de adotar:** `.cursorindexingignore` pode reduzir a indexação comum, mas isso não prova, sozinho, redução do contexto enviado ou economia de tokens.

Não confunda:

- `.cursorindexingignore`: controla a indexação do codebase;
- `.cursorignore`: bloqueia formas normais de acesso do Agent, Tab e referências;
- terminal e MCP podem operar fora de `.cursorignore`; ele não é uma fronteira completa de segurança.

## Fluxo automatizado

```text
Rule
  -> orienta bootstrap e gatilhos
Skill
  -> mantém estado, mapa e arquivamento
Checker
  -> prova o estado do filesystem
Revisão
  -> confirma semântica, autoridade e aplicabilidade
```

> 🔎 **Leitura do fluxo:** a Rule orienta, a Skill executa o procedimento repetitivo, o checker verifica o filesystem e a revisão humana confirma o significado.

O time normalmente só precisa solicitar a ação adequada e revisar o resultado:

- iniciar ou retomar uma tarefa;
- recuperar um documento por gatilho;
- arquivar uma feature concluída;
- investigar uma falha ou conflito.

A Skill pode executar os passos repetitivos. A revisão continua necessária quando uma decisão altera autoridade, uma obrigação pode ser perdida ou o resultado não é observável.

## Arquivamento e verificação

Ao concluir uma feature, a Skill deve:

1. confirmar que o documento deixou de orientar o trabalho ativo;
2. preservar em HOT ou WARM toda obrigação ainda frequente;
3. registrar gatilho, path, autoridade e aplicabilidade;
4. mover o arquivo para `docs/archived/`;
5. executar o checker;
6. testar uma referência explícita ao destino;
7. atualizar `MEMORY.md` após sucesso;
8. registrar observações e limitações.

Exemplo de checker determinístico:

```powershell
param (
    [Parameter(Mandatory = $true)]
    [string]$FileName
)

if ([System.IO.Path]::GetFileName($FileName) -ne $FileName) {
    Write-Error "FAIL: informe somente o nome do arquivo."
    exit 2
}

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "../../../..")).Path
$ActivePath = Join-Path $RepoRoot "docs/active/$FileName"
$ArchivedPath = Join-Path $RepoRoot "docs/archived/$FileName"

if (Test-Path $ActivePath) {
    Write-Error "FAIL: o arquivo ainda existe em docs/active."
    exit 1
}

if (-not (Test-Path $ArchivedPath)) {
    Write-Error "FAIL: o arquivo não foi encontrado em docs/archived."
    exit 1
}

Write-Host "PASS: movimento active para archived confirmado."
exit 0
```

Esse script prova somente que a origem não existe e o destino existe. Ele não prova que o conteúdo foi classificado corretamente, que uma obrigação foi preservada, que o Cursor indexou ou deixou de indexar o arquivo, nem que houve economia de tokens.

> 📊 **O que a verificação mede:** o checker confirma apenas as condições estruturais implementadas; semântica, indexação e economia de tokens exigem evidência adicional.

## Limites e transparência

> ⚠️ **Limites importantes:** temperatura não determina autoridade, automação não substitui revisão semântica e um `PASS` estrutural não prova a correção do conteúdo.

- **Temperatura não é autoridade:** um arquivo COLD pode conter uma regra vigente.
- **COLD não é descarte:** o histórico continua recuperável por path e gatilho.
- **Automação não é garantia semântica:** a Skill pode executar o procedimento, mas decisões de conteúdo precisam de revisão adequada ao risco.
- **Checker não é juiz:** um `PASS` estrutural não prova correção do conteúdo.
- **Indexação não é contexto efetivo:** o número de arquivos indexados não informa sozinho o prompt enviado ao modelo.
- **Observabilidade limitada:** quando não for possível provar quais arquivos foram usados, registre `INCONCLUSIVE`.
- **Conflito exige parada:** divergência entre `MEMORY.md`, código e fonte normativa deve ser reconciliada antes de continuar.

## Adoção recomendada

Comece com:

1. `MEMORY.md`;
2. pastas `docs/active/`, `docs/archived/` e `docs/context/`;
3. Rule curta;
4. Skill de context tiering;
5. checker determinístico;
6. teste de tarefa sem gatilho e teste de recuperação com gatilho.

Adicione revisão humana separada para documentos COLD normativos de alto impacto. Não trate todo arquivo como contexto de alto risco: a governança deve ser proporcional ao impacto.

Amplie a adoção somente se a recuperação necessária, a qualidade e o custo total não piorarem. Mantenha em piloto quando o ganho for incerto.

> 📌 **Adoção incremental:** comece com um piloto observável e amplie somente quando recuperação, qualidade e custo total mostrarem resultado suficiente.

## Template completo de MEMORY

Este é o único lugar do guia com o modelo detalhado. O arquivo real deve conter os dados do projeto, não este texto genérico:

```markdown
# Estado atual

Atualizado em: AAAA-MM-DD
Responsável: time

## Objetivo atual

- Descrever a feature, correção ou investigação em andamento.

## Status

- Fase: em-desenvolvimento
- Arquivamento: pending

## Artefatos ativos

- `docs/active/feature.md` — plano ou decisão vigente.

## Restrições e pendências

- Registrar somente obrigações, bloqueios ou decisões que afetem a próxima ação.

## Próxima ação

- Descrever a próxima ação verificável.

## Histórico sob demanda

- Gatilho: termo ou condição observável.
  Path: `docs/archived/feature.md`
  Autoridade: informativa | normativa
  Aplicabilidade: condição em que o arquivo deve ser consultado.
```

## Referências

- Cursor, [Changelog 0.46.x](https://cursor.com/pt-BR/changelog/0-46-x): `.cursorindexingignore`.
- Cursor, [Ignore Files](https://cursor.com/docs/reference/ignore-file): `.cursorignore`, acesso e limites.
- Cursor, [Rules](https://cursor.com/docs/rules): ativação e inclusão de Rules.
- Cursor, [Agent Skills](https://cursor.com/docs/skills): descoberta e carregamento de Skills.
- Cursor, [Prompting Agents](https://cursor.com/docs/agent/prompting): contexto e prompts.
- Agent Skills, [Specification](https://agentskills.io/specification): contrato de `SKILL.md`.
- Agent Skills, [Evaluating Skills](https://agentskills.io/skill-creation/evaluating-skills): cenários e métricas.
- Liu et al., [Lost in the Middle](https://aclanthology.org/2024.tacl-1.9/): uso de informação em contextos longos.

As referências não substituem testes na versão do Cursor, no modelo e nas tarefas do time.
