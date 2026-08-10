#!/usr/bin/env python3
"""Generate the V5 reader book, workbook, and route inventory.

The frozen Beta 3 manuscript remains the only input.  Line ranges below are
recorded in docs/audits/route-inventory-v5.md so every movement can be
audited and reversed. Only useful for re-deriving the manuscripts from the
archived Beta 3 baseline; regular recompilation uses build.sh/build.ps1.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SOURCE = REPO_ROOT / "archive" / "ebooks" / "v5-sources" / "context-engineering-v5-beta3-frozen.md"
BOOK = REPO_ROOT / "docs" / "ebooks" / "ebook" / "context-engineering-para-times-de-desenvolvimento-v5.md"
WORKBOOK = REPO_ROOT / "docs" / "ebooks" / "workbook" / "workbook-context-engineering-v5.md"
INVENTORY = REPO_ROOT / "docs" / "audits" / "route-inventory-v5.md"


def lines(start: int, end: int) -> str:
    """Return an inclusive 1-based source range."""
    return "".join(SOURCE.read_text(encoding="utf-8").splitlines(keepends=True)[start - 1 : end])


def replace_frontmatter(text: str, *, workbook: bool = False) -> str:
    title = "Workbook de Context Engineering" if workbook else "Context Engineering para Times de Desenvolvimento"
    subtitle = (
        "Laboratórios, templates e evidências — V5"
        if workbook
        else "Rota essencial e aprofundamentos — V5"
    )
    text = re.sub(r'^title:.*$', f'title: "{title}"', text, count=1, flags=re.MULTILINE)
    text = re.sub(r'^subtitle:.*$', f'subtitle: "{subtitle}"', text, count=1, flags=re.MULTILINE)
    return text


BOOK_BRIDGE = r'''
## Da tarefa à evidência em quatro movimentos

O catálogo completo de artefatos é útil, mas não precisa ser aprendido de uma vez. Na rota essencial, acompanhe quatro movimentos que preservam a relação entre intenção, execução e prova:

1. **Decidir:** o Agent identifica a missão, as invariantes e a condição de parada.
2. **Recuperar:** o Playbook coordena o fluxo e a Skill traz a capacidade aplicável; Knowledge oferece fundamentação quando necessário.
3. **Restringir:** Rule e Contract tornam obrigações e condições observáveis; Assertions registram expectativas derivadas dessas fontes.
4. **Verificar:** a Eval executa um cenário previamente definido e o Evidence Record preserva o esperado, o observado, os verificadores, o veredito e as limitações.

```text
pedido
→ decisão e roteamento
→ contexto aplicável
→ execução sob restrições
→ comparação com expectativas
→ evidência e decisão
```

\Needspace{8\baselineskip}

::: {.tip title="Rota essencial"}
Este capítulo explica os papéis e acompanha um microfluxo completo. Arquivos copiáveis, prompts, schemas e execuções ficam no workbook.
:::

## O catálogo essencial de artefatos

| Artefato | Pergunta que responde | Conteúdo mínimo | Erro que evita |
|---|---|---|---|
| Agent | Quem decide e quando deve parar? | Missão, invariantes, roteamento, stop conditions e evidência mínima. | Um agente genérico tentando executar qualquer responsabilidade. |
| Playbook | Como coordenar uma jornada recorrente? | Pré-condições, passos, decisões, fallbacks e saídas. | Procedimento longo misturado à identidade do Agent. |
| Skill | Qual capacidade especializada deve ser ativada? | Gatilhos, entradas, fluxo, guardrails, recursos e Definition of Done. | Copiar instruções especializadas para todo contexto. |
| Knowledge | Qual fundamento apoia a decisão? | Conceitos, limites, fontes e exemplos consultivos. | Tratar explicação como obrigação operacional. |
| Rule | O que é obrigatório, proibido ou exige fallback? | Escopo, obrigação, proibição, fallback e evidência. | Regra crítica escondida em prosa ou exemplo. |
| Contract | Que condições observáveis conectam componentes? | Entradas, saídas, pré-condições, pós-condições e efeitos proibidos. | Interfaces aparentemente compatíveis, mas semanticamente divergentes. |
| Assertion | Qual expectativa estável será verificada? | Fonte, escopo, expected e mecanismo de prova. | Inventar o critério depois de observar o resultado. |
| Eval | Em qual cenário e com quais verificadores comparar? | Massa, execução, checks e regra de veredito. | Confundir uma demonstração convincente com avaliação reproduzível. |
| Evidence Record | O que ocorreu e o que ainda não foi provado? | Expected, observed, checks, verdict, lineage e limitações. | Transformar evidência em narrativa persuasiva. |

Temperatura, autoridade e tipo continuam separados. Um Contract pode ser COLD e NORMATIVE; uma explicação HOT pode ser apenas ADVISORY. **HOT/WARM/COLD responde quando carregar, não quanto o conteúdo obriga.**

### Do backend caótico à separação

O anti-pattern abaixo mistura identidade, procedimento, política, explicação e teste. O problema não é apenas o tamanho: nenhuma parte possui ownership, ativação ou mecanismo de prova claro.

```markdown
<!-- ANTI-PATTERN -->
# Backend Agent

Sempre implemente APIs, mensageria, persistência e SignalR.
Use 202, salve o job, publique eventos, aplique retry e gere testes.
SignalR funciona assim: [... explicação longa ...]
Se o teste passar, considere concluído.
```

A separação mínima transforma esse bloco em relações verificáveis:

```text
Agent → roteia a tarefa e preserva invariantes
Playbook → coordena a operação assíncrona
Skill → valida o contrato de API
Knowledge → explica limites do SignalR
Rule → exige a política aprovada no estudo
Contract → descreve estados e transições observáveis
Eval → executa cenários definidos antes da resposta
Evidence → registra resultado e limitações
```

## Frontmatter: contrato do consumidor antes da ontologia do livro

Frontmatter melhora identidade, catálogo e interoperabilidade quando um consumidor reconhece seus campos. Ele **não garante**, isoladamente, descoberta, roteamento ou cache.

Uma Agent Skill interoperável começa pelo contrato da especificação aberta:

```markdown
---
name: validate-api-contract
description: Valida contratos HTTP assíncronos quando a tarefa altera aceitação, consulta de status ou transições de job.
---

# Validar contrato de API

## Quando usar

Use quando uma alteração puder mudar status, headers, estados ou efeitos observáveis.
```

Campos adicionais só devem ser usados quando o host, um catálogo ou outro componente do projeto realmente os interpretar. A mesma cautela vale para Rules e Playbooks: metadados de governança podem ser úteis sem possuir efeito nativo no Cursor.

::: {.warning title="Existência não prova participação"}
Um arquivo presente no repositório pode não ter entrado no contexto. Mesmo quando participou, isso não demonstra aplicação correta. Quando o host não expuser lineage suficiente, registre `INCONCLUSIVE` em vez de deduzir o caminho a partir de uma resposta correta.
:::

## Microfluxo: Contract → Assertion → Eval → Evidence

Considere o recorte didático de uma API que aceita um relatório assíncrono. O status HTTP `202 Accepted` informa que a requisição foi aceita para processamento; ele não comprova conclusão e, isoladamente, não prova a durabilidade do job.[^rfc-202]

O Contract adiciona as condições específicas da arquitetura de referência:

```yaml
operation: POST /reports
preconditions:
  - request_is_authorized
postconditions:
  - response_status_is_202
  - job_is_queryable_by_returned_location
forbiddenEffects:
  - report_marked_completed_before_processing
```

A Assertion é derivada antes da execução:

```yaml
assertionId: ASYNC-ACCEPT-001
source: report-request.contract.yaml
expected:
  status: 202
  locationHeader: required
  initialState: accepted
```

A Eval fornece a entrada, executa o cenário e combina verificadores compatíveis com cada critério. Igualdade, schema, status e transições devem preferir verificadores determinísticos. Critérios semânticos podem exigir rubrica e julgamento probabilístico versionado.

O Evidence Record não repete a intenção; ele registra o que foi observado:

```json
{
  "evidenceId": "EV-ASYNC-001",
  "assertionId": "ASYNC-ACCEPT-001",
  "expected": {"status": 202, "locationHeader": "required"},
  "observed": {"status": 202, "locationHeader": "/reports/jobs/42"},
  "checks": [
    {"id": "status", "mechanism": "exact", "result": "PASS"},
    {"id": "location", "mechanism": "schema", "result": "PASS"}
  ],
  "verdict": "PASS",
  "limitations": ["O lineage de arquivos consultados não foi exposto pelo host."]
}
```

O `PASS` demonstra somente o escopo verificado. Ele não prova que todos os artefatos foram recuperados, que outros modelos agirão do mesmo modo ou que a arquitetura é adequada para qualquer domínio.

::: {.example title="Checkpoint técnico"}
Sem abrir o workbook, tente responder: de qual fonte nasceu a Assertion, quem executou a Eval e qual limitação impede transformar o resultado funcional em prova de lineage? Se uma dessas relações não estiver clara, releia o microfluxo antes de continuar.
:::

## Recuperação, aplicação e resultado são camadas diferentes

Uma avaliação útil separa ao menos três perguntas:

1. **Recuperação ou roteamento:** o conteúdo aplicável foi disponibilizado?
2. **Aplicação:** as obrigações e restrições recuperadas influenciaram corretamente a execução?
3. **Resultado:** a saída satisfaz as condições observáveis do Contract e das Assertions?

```text
resultado correto + lineage ausente
→ resultado funcional PASS
→ recuperação INCONCLUSIVE

artefato recuperado + regra violada
→ recuperação PASS
→ aplicação FAIL
```

Essa separação evita dois falsos positivos comuns: considerar uma resposta correta como prova de recuperação e considerar a simples presença de palavras como prova de aplicação.

::: {.curious title="APROFUNDAMENTO — verificadores determinísticos e semânticos"}
Use verificadores determinísticos para propriedades que podem ser calculadas sem interpretação: schema, igualdade, presença obrigatória, ordem, estado e status. Reserve LLM-as-a-Judge para critérios realmente semânticos; versione modelo, prompt e rubrica, preserve amostras e mantenha revisão humana compatível com o risco. O avaliador probabilístico não se torna verdade objetiva por receber o nome de judge.
:::

## Da compreensão para a execução

O workbook contém o experimento completo no Cursor, os testes mínimos de cada artefato, o Eval Spec integral, o prompt do Auditor de Contexto, o estudo assíncrono, templates e Evidence Records preenchidos. O laboratório `lab/` permanece como corpus executável e fonte canônica dos arquivos completos.

Antes de ir ao workbook, preserve esta cadeia:

```text
fonte aprovada
→ expectativa derivada
→ cenário definido
→ execução observada
→ verificadores
→ veredito com limitações
```

'''


BOOK_WORKBOOK_LINK = r'''
# Workbook e laboratórios

Os templates extensos, prompts, YAML, JSON, execuções guiadas e checkpoints foram separados do fluxo de leitura e estão no **Workbook de Context Engineering V5**, incluído neste pacote.

Essa divisão não reduz o método. Ela cria duas rotas complementares:

- o livro principal ensina o modelo mental, os papéis, as decisões e os limites;
- o workbook conduz a implementação, a avaliação e o registro de evidências.

Use o workbook quando precisar copiar um artefato, executar um laboratório ou reproduzir uma Eval. Use a pasta `lab/` como fonte canônica dos arquivos completos; os blocos do workbook explicam como consumi-los.

'''


WORKBOOK_INTRO = r'''---
title: "Workbook de Context Engineering"
subtitle: "Laboratórios, templates e evidências — V5"
author: "Hernandes Junio de Assis"
date: "2026"
lang: pt-BR
toc: true
toc-depth: 3
numbersections: true
linkcolor: blue
urlcolor: blue
geometry: margin=2.0cm
papersize: a4
fontsize: 10pt
documentclass: book
classoption:
  - oneside
---

::: {.info title="Como usar este workbook"}
Este material é o companion hands-on do livro **Context Engineering para Times de Desenvolvimento**. Ele preserva os prompts, schemas, templates, massas e execuções que interrompiam a rota conceitual. Para cada laboratório, registre a expectativa antes de executar, diferencie resultado funcional de lineage e use `INCONCLUSIVE` quando a evidência não permitir uma conclusão.
:::

## Pré-requisitos

- ter lido ao menos a rota essencial do livro principal;
- usar uma cópia de trabalho do diretório `lab/`;
- registrar host, versão, modelo e data da execução;
- não utilizar respostas anteriores como massa visível ao agente sob avaliação;
- interromper quando faltar fonte aprovada, observabilidade ou autoridade para a próxima ação.

## Ordem recomendada

1. Experimento mínimo executável.
2. Artefatos e testes focados.
3. Contract, Assertion, Eval e Evidence Record.
4. Estudo assíncrono integrado.
5. Kits, templates e laboratório Agent HOT.
6. Checklist do curador.

Cada `PASS` vale apenas para o cenário, a versão e os verificadores registrados. O workbook ensina um processo de produção de evidência; não promete comportamento determinístico de uma LLM.

# Laboratório 1 — contexto mínimo executável

'''


def build_book() -> str:
    front_and_core = replace_frontmatter(lines(1, 957))
    # Beta 3 omitted the closing fenced-div marker of the "Regra prática"
    # callout immediately before line 958. Close it explicitly before the
    # generated bridge so the marker does not leak into the rendered PDF.
    front_and_core = front_and_core.rstrip() + "\n\n:::\n\n"
    front_and_core = front_and_core.replace(
        "Edição integral Beta 3 — da oficina ao harness auditável",
        "Rota essencial e aprofundamentos — V5",
    )
    front_and_core = re.sub(
        r'::: \{\.info title="Propósito da edição Beta 3"\}.*?:::\n',
        '::: {.info title="Propósito da edição"}\n'
        'Esta edição separa compreensão e execução em dois artefatos complementares. '
        'O livro principal preserva a progressão conceitual e as decisões; o workbook reúne '
        'prompts, schemas, templates, laboratórios e evidências reproduzíveis.\n:::\n',
        front_and_core,
        count=1,
        flags=re.DOTALL,
    )
    front_and_core = front_and_core.replace(
        "**Rota hands-on.** Ao chegar aos exercícios de eval e evidência, use a referência para a Parte VI. Lá estão os artefatos completos e copiáveis; no fluxo principal permanecem apenas os conceitos e o exemplo mínimo necessário.",
        "**Rota hands-on.** Use o workbook que acompanha esta edição. Nele estão os artefatos completos, prompts, schemas, execuções e laboratórios; no livro principal permanecem conceitos, decisões e microexemplos.",
    )
    front_and_core = front_and_core.replace(
        "A partir deste ponto, o foco passa a ser **como esse contexto participa de uma execução real**.\n\n## O que é nativo e o que é convenção",
        "A partir deste ponto, o foco passa a ser **como esse contexto participa de uma execução real**.\n\n:::\n\n## O que é nativo e o que é convenção",
    )
    tail = lines(3711, 5079) + BOOK_WORKBOOK_LINK + lines(6329, 6482)
    tail = tail.replace("A próxima parte transforma esses princípios em **templates e laboratórios reutilizáveis**, para que o leitor possa criar, executar e avaliar os artefatos apresentados ao longo do livro.", "O workbook transforma esses princípios em **templates e laboratórios reutilizáveis**, permitindo criar, executar e avaliar os artefatos sem interromper a rota conceitual deste livro.")
    tail = tail.replace("A Parte V termina nesse ponto", "A parte de governança termina nesse ponto")
    tail = tail.replace("A próxima parte", "O workbook")
    tail = tail.replace("# Glossário", "# Glossário essencial")
    tail = re.sub(r"\n\[\^mcp-routing\]:.*?\n", "\n", tail)
    tail = tail.replace(
        "- Liu, N. F. et al. **Lost in the Middle: How Language Models Use Long Contexts**. 2023. <https://arxiv.org/abs/2307.03172>.",
        "- Liu, N. F. et al. **Lost in the Middle: How Language Models Use Long Contexts**. TACL, 2024. <https://aclanthology.org/2024.tacl-1.9/>.\n"
        "- Sweller, J. **Cognitive Load During Problem Solving: Effects on Learning**. Cognitive Science, 1988. <https://doi.org/10.1207/s15516709cog1202_4>.\n"
        "- Mayer, R. E.; Moreno, R. **Nine Ways to Reduce Cognitive Load in Multimedia Learning**. Educational Psychologist, 2003. <https://doi.org/10.1207/S15326985EP3801_6>."
    )
    tail = tail.replace(
        "## Tecnologias do estudo de caso\n",
        "## Tecnologias do estudo de caso\n\n- IETF. **RFC 9110 — HTTP Semantics**, seção 15.3.3 (`202 Accepted`). <https://www.rfc-editor.org/rfc/rfc9110.html#name-202-accepted>.\n"
    )
    tail += "\n[^rfc-202]: RFC 9110, seção 15.3.3, define `202 Accepted` como aceitação para processamento ainda não concluído e recomenda indicar um monitor de status quando aplicável.\n"
    return front_and_core + BOOK_BRIDGE + tail


def build_workbook() -> str:
    detailed = lines(958, 4230)
    detailed = re.sub(r"\s*:contentReference\[oaicite:\d+\]\{index=\d+\}", "", detailed)
    detailed = detailed.replace("## Contexto mínimo executável", "## Montagem do experimento")
    detailed = detailed.replace("### Frontmatter de uma Skill", "## Frontmatter de uma Skill")
    detailed = detailed.replace("# Parte IV - Estudo de caso: operação assíncrona", "# Laboratório 2 — estudo de caso: operação assíncrona")
    detailed = detailed.replace(
        "desde que exista um mecanismo capaz de referenciá-los ou recuperá-los quando aplicáveis.\n\n## Skill: capacidade especializada sob demanda",
        "desde que exista um mecanismo capaz de referenciá-los ou recuperá-los quando aplicáveis.\n\n:::\n\n## Skill: capacidade especializada sob demanda",
    )
    detailed = detailed.replace(
        "Use `kebab-case` no frontmatter e mantenha o título humano separado.\n\n````",
        "Use `kebab-case` no frontmatter e mantenha o título humano separado.\n\n:::\n````",
    )
    detailed = detailed.replace(
        "o Evidence Record ainda está incompleto.\n\n\n## Reduzindo omissão e alucinação operacional",
        "o Evidence Record ainda está incompleto.\n\n:::\n\n## Reduzindo omissão e alucinação operacional",
    )
    detailed = detailed.replace(
        "O bloco abaixo exemplifica os dados fornecidos ao avaliador depois da execução. `artefatosEsperados`, `assertionsEsperadas` e `criteriosSemanticos` vêm da Eval Spec. `artefatosObservados`, `respostaDoAgente`, `toolsExecutadas`, `testesExecutados` e `resultadoObservado` vêm da execução. `resultadosDeterministicos` são produzidos pelos verificadores executados antes do julgamento semântico.",
        "O bloco abaixo exemplifica os dados fornecidos ao avaliador depois da execução.\n\n- `artefatosEsperados`, `assertionsEsperadas` e `criteriosSemanticos` vêm da Eval Spec;\n- `artefatosObservados`, `respostaDoAgente`, `toolsExecutadas`, `testesExecutados` e `resultadoObservado` vêm da execução;\n- `resultadosDeterministicos` são produzidos pelos verificadores executados antes do julgamento semântico.",
    )
    detailed = detailed.replace(
        "A anatomia ampliada e o exemplo completo de Kubernetes foram movidos para a Parte VI.",
        "A anatomia ampliada e o exemplo completo de Kubernetes estão no Laboratório 3 deste workbook.",
    )
    detailed = detailed.replace(
        "A Parte VI concentra os templates completos utilizados neste fluxo",
        "O Laboratório 3 deste workbook concentra os templates completos utilizados neste fluxo",
    )
    templates = lines(5080, 6364)
    templates = templates.replace("# Parte VI - Templates práticos", "# Laboratório 3 — kits e templates práticos")
    templates = templates.replace(
        "Este laboratório complementa a seção **Agent: o conteúdo HOT** e verifica duas responsabilidades específicas:",
        "Este laboratório complementa a definição de **Agent HOT** e verifica duas responsabilidades:",
    )
    refs = lines(6435, 6482)
    refs = refs.replace("# Referências e leituras recomendadas", "# Referências técnicas")
    refs = re.sub(r"\n\[\^[^\]]+\]:.*?(?=\n\[\^|\Z)", "", refs, flags=re.DOTALL)
    return WORKBOOK_INTRO + detailed + templates + refs


def classify(line_no: int, title: str) -> tuple[str, str, str]:
    if 958 <= line_no <= 3709 or 5080 <= line_no <= 6364:
        return "HANDS-ON", "mover", "Workbook"
    if 3710 <= line_no <= 4230:
        return "ESSENCIAL + HANDS-ON", "condensar no livro e preservar integral no workbook", "Livro + Workbook"
    if 4231 <= line_no <= 5079:
        route = "APROFUNDAMENTO" if any(k in title.lower() for k in ("classificação", "conflito", "orçamento", "ciclo de vida", "refatoração", "loop", "gate")) else "ESSENCIAL"
        return route, "manter", "Livro"
    if 6329 <= line_no <= 6364:
        return "HANDS-ON", "mover", "Workbook"
    return "ESSENCIAL", "manter", "Livro"


def build_inventory(source_text: str) -> str:
    rows = []
    in_fence = False
    for no, raw in enumerate(source_text.splitlines(), 1):
        if re.match(r"^\s*`{3,}", raw):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.match(r"^(#{1,3})\s+(.+)$", raw)
        if not m:
            continue
        level, title = len(m.group(1)), re.sub(r"\s+\{.*\}$", "", m.group(2)).strip()
        route, action, destination = classify(no, title)
        risk = "perda de fundamento ou vínculo" if action != "manter" else "baixo; validar pontes e referências"
        rows.append((no, level, title, route, action, destination, risk))
    header = """# Inventário de rotas — V5

Baseline: `sources/context-engineering-v5-beta3-frozen.md`  
SHA-256: `{sha}`

Este inventário classifica títulos reais fora de blocos cercados. As faixas movidas continuam preservadas integralmente no workbook; a baseline congelada permite reconstrução e comparação.

| Linha | Nível | Seção atual | Rota | Ação | Destino | Risco controlado |
|---:|---:|---|---|---|---|---|
""".format(sha=hashlib.sha256(source_text.encode()).hexdigest())
    body = "\n".join(
        f"| {no} | H{level} | {title.replace('|', '/')} | {route} | {action} | {destination} | {risk} |"
        for no, level, title, route, action, destination, risk in rows
    )
    return header + body + "\n"


def main() -> None:
    source_text = SOURCE.read_text(encoding="utf-8")
    BOOK.write_text(build_book(), encoding="utf-8")
    WORKBOOK.write_text(build_workbook(), encoding="utf-8")
    INVENTORY.write_text(build_inventory(source_text), encoding="utf-8")
    print(f"book={BOOK} sha256={hashlib.sha256(BOOK.read_bytes()).hexdigest()}")
    print(f"workbook={WORKBOOK} sha256={hashlib.sha256(WORKBOOK.read_bytes()).hexdigest()}")
    print(f"inventory={INVENTORY}")


if __name__ == "__main__":
    main()
