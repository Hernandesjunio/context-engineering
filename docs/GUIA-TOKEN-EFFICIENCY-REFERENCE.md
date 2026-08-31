# Referência detalhada de eficiência de tokens no Cursor

> 💡 **Escopo:** use este documento para comparar modelos, contexto e práticas de trabalho dentro dos agentes do Cursor. As recomendações são hipóteses condicionadas à tarefa, não garantias de qualidade ou de economia.

Este documento contém os detalhes por trás do [guia rápido](GUIA-TOKEN-EFFICIENCY.md).

> ⚠️ **Atualidade dos dados:** preços de referência em USD por 1 milhão de tokens. `in` é entrada e `out` é saída. Valores, nomes, limites, pools e disponibilidade podem mudar; confirme no Cursor antes de uma decisão de longo prazo.

## Termos de consulta

- **Context ring:** indicador do Cursor que mostra o uso do contexto e sua divisão por categoria.
- **Tool loop:** ciclo em que o agente usa uma ferramenta, avalia o resultado e decide a próxima ação.
- **Cache hit/read:** reutilização de entrada já processada; pode reduzir o custo, conforme modelo e provedor.
- **Pool:** grupo de uso e cobrança do Cursor, como Cursor Models ou Other Models.
- **Long context:** uso de uma janela de contexto estendida, que pode ter preço ou limites próprios.
- **Front matter:** metadados YAML no início de um arquivo `.mdc`.
- **`globs`:** padrões curinga que vinculam uma Rule aos arquivos correspondentes.
- **Amostra controlada:** comparação de pelo menos três tarefas com mesmo aceite, escopo e evidências necessárias; veja [Amostra controlada mínima](#amostra-controlada-mínima).
- **Contexto equivalente:** o mesmo recorte de evidências necessárias em cada rota comparada.
- **Fluxo validado:** rota que preservou os critérios de aceite na amostra controlada mínima.

## 1. Como interpretar as recomendações

Separe as dimensões antes de escolher:

- **Fase:** discovery, requisitos, arquitetura, desenvolvimento, documentação ou debugging.
- **Atividade:** o que será produzido, por exemplo, edição local, refactor, teste, síntese ou investigação.
- **Modo:** `Ask`, `Plan`, `Agent`, `Debug` ou `Multitask`.
- **Modelo:** compromisso entre raciocínio, execução, contexto, velocidade e custo.
- **Effort:** deve subir por evidência de insuficiência, não automaticamente pela duração da tarefa.

Use esta taxonomia:

- **Início:** hipótese atual de custo-benefício para o perfil; não é o melhor modelo universal.
- **Menor custo:** alternativa mais barata que ainda atende aos critérios de qualidade; preço isolado não basta.
- **Promoção:** modelo de maior capacidade ou melhor adequação quando o gatilho objetivo aparecer.

Se uma opção mais barata superar o início em qualidade e custo total numa [amostra controlada](#amostra-controlada-mínima), ela pode se tornar o novo início. Sem evidência comparativa, descreva a escolha como hipótese de roteamento.

“BMAD” não foi avaliado como categoria independente. Requisitos, Understanding Doc, specs, ADR, RFC e arquitetura devem ser tratados como análise, planejamento e documentação, com validação em tarefas representativas.

## 2. Rotas por fase

Use esta seção apenas para localizar a categoria correspondente à fase. A escolha do modelo, do nível de dificuldade e do gatilho de promoção está na [seção 3](#3-candidatos-por-atividade-modo-e-dificuldade).

> 🧭 **Como navegar:** identifique a fase e o modo abaixo e consulte a atividade correspondente na seção 3.

| Fase | Modo | Categoria detalhada na seção 3 |
| --- | --- | --- |
| Extração e Q&A simples | `Ask` | [Seção 3](#3-candidatos-por-atividade-modo-e-dificuldade) — Documentação e Q&A |
| Análise e discovery | `Ask`/`Plan` | [Seção 3](#3-candidatos-por-atividade-modo-e-dificuldade) — Planejamento e análise |
| Requisitos e documentação | `Ask`/`Plan` | [Seção 3](#3-candidatos-por-atividade-modo-e-dificuldade) — Documentação e Q&A ou Planejamento e análise |
| Arquitetura, ADR e RFC | `Plan` | [Seção 3](#3-candidatos-por-atividade-modo-e-dificuldade) — Planejamento e análise, dificuldade avançada |
| Desenvolvimento local | `Agent` | [Seção 3](#3-candidatos-por-atividade-modo-e-dificuldade) — Desenvolvimento |
| Desenvolvimento em volume | `Agent`/`Multitask` | [Seção 3](#3-candidatos-por-atividade-modo-e-dificuldade) — Desenvolvimento em volume |
| Debugging difícil | `Debug` | [Seção 3](#3-candidatos-por-atividade-modo-e-dificuldade) — Debugging |

> 📌 **Regra de precedência:** a seção 3 é a referência operacional para candidatos, preços e promoções. Esta seção não repete recomendações de modelos.

## 3. Candidatos por atividade, modo e dificuldade

> 💡 **Referência canônica:** responda primeiro **qual atividade será executada**, classifique sua dificuldade e só depois escolha o modelo. As tabelas desta seção são a fonte operacional para candidatos, preços e gatilhos de promoção.

> 💲 **Preços:** toda menção operacional a um modelo mantém seu preço Cursor `in/out` visível. `$0.20 in / $1.25 out` significa USD por 1M de tokens de entrada/saída.

A ordem é uma hipótese operacional, não um ranking universal.

### Desenvolvimento — `Agent`

| Dificuldade | Início | Menor custo | Promova quando | Atividades típicas |
| --- | --- | --- | --- | --- |
| Básica | `kimi-k2.7-code` ($0.95 in / $4 out) | `gpt-5.4-nano-medium` ($0.20 in / $1.25 out) para transformação simples | a edição exigir tool loop ou entendimento de repositório | arquivo único, boilerplate, teste local e correção direta |
| Média | `cursor-grok-4.6-medium` ($2 in / $6 out) | `glm-5.2-high` ($1.40 in / $4.40 out) se a tarefa couber no fluxo validado | houver integração multi-arquivo, contrato implícito ou testes difíceis; use `gpt-5.4-high` ($2.50 in / $15 out) como promoção | feature pequena, refactor coordenado e integração |
| Avançada | `gpt-5.6-sol-medium` ($4 in / $20 out) | `kimi-k3-max` ($3 in / $15 out) quando contexto e risco permitirem | a persistência, o raciocínio ou o custo de falha justificarem `claude-opus-5-thinking-high` ($5 in / $25 out) | migração, arquitetura aplicada e mudança crítica |

### Desenvolvimento em volume — `Agent`/`Multitask`

| Dificuldade | Início | Menor custo | Promova quando | Atividades típicas |
| --- | --- | --- | --- | --- |
| Básica | `gpt-5.4-nano-medium` ($0.20 in / $1.25 out) | `gpt-5.4-nano-medium` ($0.20 in / $1.25 out) | a coordenação superar a economia | tarefas repetitivas e independentes |
| Média | `kimi-k2.7-code` ($0.95 in / $4 out) | `composer-2.5` ($0.50 in / $2.50 out) para subtarefas curtas | a síntese exigir mais contexto; teste `glm-5.2-high` ($1.40 in / $4.40 out) | geração de testes, transformações e arquivos paralelos |
| Avançada | `glm-5.2-high` ($1.40 in / $4.40 out) | `kimi-k2.7-code` ($0.95 in / $4 out) se 256k bastar | a integração exigir `cursor-grok-4.6-medium` ($2 in / $6 out) ou raciocínio mais forte | lotes com dependências explícitas e revisão posterior |

### Planejamento e análise — `Ask`/`Plan`

| Dificuldade | Início | Menor custo | Promova quando | Atividades típicas |
| --- | --- | --- | --- | --- |
| Básica | `glm-5.2-high` ($1.40 in / $4.40 out) | `kimi-k2.7-code` ($0.95 in / $4 out) | houver dependências ou alternativas não resolvidas | decomposição, localização e plano curto |
| Média | `cursor-grok-4.6-medium` ($2 in / $6 out) | `glm-5.2-high` ($1.40 in / $4.40 out) | a síntese ou o contexto exigirem `claude-sonnet-5` ($2 in / $10 out) | plano multi-arquivo, trade-offs e requisitos |
| Avançada | `kimi-k3-max` ($3 in / $15 out) | `glm-5.2-high` ($1.40 in / $4.40 out) | o custo de reversão justificar `claude-opus-5-thinking-high` ($5 in / $25 out) | arquitetura, ADR, RFC e migração |

### Documentação e Q&A — `Ask`

| Dificuldade | Início | Menor custo | Promova quando | Atividades típicas |
| --- | --- | --- | --- | --- |
| Básica | `gpt-5.4-nano-medium` ($0.20 in / $1.25 out) | já é o baseline | houver erro factual ou necessidade de ferramenta; use `composer-2.5` ($0.50 in / $2.50 out) como promoção | extração, classificação, formatação e perguntas simples |
| Média | `claude-sonnet-5` ($2 in / $10 out) | `glm-5.2-high` ($1.40 in / $4.40 out) | a síntese exigir mais contexto ou raciocínio | documentação técnica e síntese comparativa |
| Avançada | `claude-opus-5-thinking-high` ($5 in / $25 out) | `kimi-k3-max` ($3 in / $15 out) | a amostra mostrar necessidade de raciocínio máximo | decisão crítica e documentação de alto risco |

### Debugging — `Debug`

| Dificuldade | Início | Menor custo | Promova quando | Atividades típicas |
| --- | --- | --- | --- | --- |
| Básica | `kimi-k2.7-code` ($0.95 in / $4 out) | `gpt-5.4-nano-medium` ($0.20 in / $1.25 out) para erro localizado | o problema não puder ser reproduzido localmente | falha determinística e teste quebrado |
| Média | `glm-5.2-high` ($1.40 in / $4.40 out) | `kimi-k2.7-code` ($0.95 in / $4 out) | tool use e iteração exigirem `cursor-grok-4.6-medium` ($2 in / $6 out) | logs, dependências e regressão multi-arquivo |
| Avançada | `gpt-5.6-sol-medium` ($4 in / $20 out) | `glm-5.2-high` ($1.40 in / $4.40 out) | hipóteses concorrentes e alto custo de falha justificarem `claude-opus-5-thinking-high` ($5 in / $25 out) | falha intermitente e investigação multi-sistema |

## 4. Escolha de modo e effort

| Modo | Use quando | Evite quando | Razão técnica |
| --- | --- | --- | --- |
| `Ask` | explicar, comparar, localizar ou diagnosticar sem editar | a entrega exige alteração e verificação | reduz ações de implementação |
| `Plan` | há decisões, dependências ou trade-offs antes de editar | a mudança é pequena e óbvia | antecipa síntese e reduz retrabalho |
| `Agent` | o objetivo é implementar e testar | você quer somente uma resposta | usa ferramentas, edições e testes |
| `Debug` | existe falha reproduzível ou evidência de runtime | ainda não há sintoma concreto | organiza hipóteses em torno de evidência |
| `Multitask` | subtarefas são independentes | agentes editam a mesma área ou dependem do mesmo estado | isola contextos, mas multiplica coordenação |

| Tarefa | Effort inicial | Aumente quando |
| --- | --- | --- |
| Formatação, extração e boilerplate | `low`/default | a saída viola regra objetiva |
| CRUD, testes locais e arquivo único | default/`medium` | existe comportamento implícito ou debugging não local |
| Refactor multi-arquivo e SPEC simples | `medium`/`high` | há contratos, migração ou alternativas válidas |
| Arquitetura, ADR/RFC e falha multi-sistema | `high`/`max` | o custo da decisão errada supera o raciocínio adicional |

Não existe multiplicador universal de effort. Observe reasoning tokens, latência, qualidade e retrabalho no modelo e na tarefa concretos.

## 5. Redução de contexto

### Atalhos macOS confirmados; Windows a validar localmente

Os atalhos macOS abaixo foram conferidos em [Keyboard Shortcuts](https://cursor.com/docs/reference/keyboard-shortcuts). As equivalências Windows seguem a base de keybindings do VS Code, mas devem ser verificadas nos keybindings locais antes de serem usadas como instrução. O mesmo atalho pode ter uma ação geral e outra contextual: por exemplo, `Cmd+L` alterna o painel em **General**, mas adiciona a seleção a um novo chat em **Code Selection & Context**.

| Ação no Cursor | Windows | macOS |
| --- | --- | --- |
| Alternar painel | `Ctrl+I` ou `Ctrl+L` | `Cmd+I` ou `Cmd+L` |
| Seleção → novo chat | `Ctrl+L` com código selecionado | `Cmd+L` com código selecionado |
| Seleção → chat atual | `Ctrl+Shift+L` | `Cmd+Shift+L` |
| Abrir o Inline Edit | `Ctrl+K` | `Cmd+K` |
| Focar entrada do Inline Edit | `Ctrl+Shift+K` | `Cmd+Shift+K` |
| Alternar estratégia de leitura | `Ctrl+M` | `Cmd+M` |
| Novo chat | `Ctrl+N` ou `Ctrl+R` | `Cmd+N` ou `Cmd+R` |
| Nova aba de chat | `Ctrl+T` | `Cmd+T` |
| Alternar modos do Agent | `Shift+Tab` | `Shift+Tab` |
| Configurações do Cursor | `Ctrl+Shift+J` | `Cmd+Shift+J` |
| Adicionar arquivo, pasta ou outro contexto | `@` no chat | `@` no chat |

Todos os keybindings podem ser remapeados. A documentação consultada não confirma os atalhos específicos do CLI listados anteriormente; por isso, este guia não prescreve comandos de CLI sem fonte própria.

### Abas abertas, anexos e context ring

A documentação de [Prompting agents](https://cursor.com/docs/agent/prompting) descreve contexto anexado por seleção, `@arquivo`, `@pasta`, terminal, chat, diff, browser, ferramentas e histórico. Ela não afirma que todas as abas abertas do editor sejam automaticamente enviadas ao Agent.

Portanto:

- uma aba aberta pode facilitar a seleção, mas não deve ser contada como contexto enviado por si só;
- conte o que aparece no context ring e o que foi explicitamente anexado ou lido;
- use seleção ou `@arquivo` quando o objetivo for restrito;
- use `@pasta`, `@Branch` ou `@Terminals` somente quando a tarefa exigir esse escopo;
- mantenha logs longos fora do prompt e anexe apenas o recorte necessário.

O context ring mostra categorias como System prompt, Tools, Rules, Skills, MCP, Subagents, Conversation e Summarized conversation. Use-o para medir, não para presumir, o que está no contexto.

## 6. Chats e handoffs

Abra outro chat quando o objetivo mudar, o histórico deixar de ajudar ou a compressão do contexto ameaçar a clareza. Um novo chat não elimina a necessidade de anexar os arquivos relevantes.

### Handoff como skill invocável

Um workflow de handoff pode ser empacotado como uma skill invocável pelo menu `/`, conforme [Prompting agents](https://cursor.com/docs/agent/prompting). A skill deve produzir somente o resumo necessário para retomar o trabalho. Enquanto ela não existir no projeto, use o template manual abaixo.

Contrato mínimo da skill ou do template:

1. decisão tomada;
2. arquivos-chave, preferencialmente como `@arquivo`;
3. restrições e invariantes;
4. evidência curta ou erro reproduzível;
5. próxima ação ou pergunta;
6. pendências, somente se alterarem a retomada.

```markdown
# Contexto: <tema>

## Decisão
<1-3 linhas>

## Arquivos-chave
- @src/Foo.cs — <papel>

## Restrições
- <invariante>

## Evidências ou erros
<recorte curto ou @arquivo>

## Próxima ação ou pergunta
<objetivo atual>

## Pendências
- <item>
```

Um handoff substitui histórico irrelevante por resumo controlado. Conteúdo repetido pode favorecer cache, mas não há garantia de cache entre chats.

## 7. Execução da otimização

Siga uma sequência que mede antes de remover:

1. Abra o context ring e identifique a maior categoria controlável.
2. Remova apenas MCP, plugins, skills ou subagents ociosos que contribuam para essa categoria.
3. Reduza Rules universais quando elas não forem invariantes universais; escolha aplicação inteligente, globs ou manual conforme o caso.
4. Troque anexos amplos por seleção, `@arquivo` ou um recorte de log.
5. Se o objetivo ou o histórico estiverem misturados, abra novo chat e use um handoff curto.
6. Escolha o modo, modelo e effort compatíveis com a atividade e o risco.
7. Confira novamente o context ring e valide se a evidência necessária permaneceu.

Não desative tudo por padrão: contexto útil pode ser mais barato que uma correção posterior.

## 8. Controles avançados

`Customize`, `Max Mode`, `Privacy Mode` e `Approvals` têm efeitos diferentes. Nenhum deles deve ser tratado como redução automática de contexto.

- **Customize:** permite revisar fontes ativas de contexto e desativar somente o que estiver ocioso.
- **Max Mode:** pode ampliar o contexto e alterar o consumo conforme o plano e o modelo; verifique o comportamento atual no Cursor.
- **Privacy Mode:** controla tratamento de dados; não reduz por si só o tamanho do prompt.
- **Approvals:** controlam autorização, execução e segurança; não removem o contexto já enviado.

### Rules e front matter

Uma Rule do projeto é um arquivo `.mdc`. A documentação oficial usa os campos `description`, `globs` e `alwaysApply`; não existe necessidade de um campo `rules`.

| Tipo na interface | Front matter | Quando entra | Uso recomendado |
| --- | --- | --- | --- |
| `Always Apply` | `alwaysApply: true` | em todos os chats | invariantes curtas e universais |
| `Apply Intelligently` (`Intelligent`) | `alwaysApply: false` + `description` | o Agent decide pela descrição | orientação temática |
| `Apply to Specific Files` | `alwaysApply: false` + `globs` | quando arquivo correspondente está no contexto | convenções por tipo de arquivo |
| `Apply Manually` | `alwaysApply: false`, sem `description` e sem `globs` | quando mencionada com `@` | workflow ocasional |

Quando `alwaysApply` é `true`, `description` e `globs` não alteram a aplicação. `Intelligent` é um rótulo da interface para seleção baseada na descrição; não é um valor para escrever no front matter.

Exemplo de Rule estrita e universal:

```markdown
---
description: Exige autorização antes de expandir contexto
alwaysApply: true
---

# Token Efficiency (strict)

- Use a mensagem atual, seleções explícitas e itens `@` anexados.
- Se faltar contexto, peça autorização antes de ler outro path.
- Não faça discovery amplo nem siga referências cruzadas sem autorização.
```

Se a mesma Rule for opcional, use `alwaysApply: false` sem `description` nem `globs` e mencione-a manualmente. Uma Rule strict adiciona tokens fixos e pode criar turnos de autorização; use-a quando a previsibilidade compensar esse custo.

### Rules, Skills, MCP e subagents

| Recurso | O que é | Como entra | Impacto provável no contexto | Uso eficiente |
| --- | --- | --- | --- | --- |
| Rule `Always Apply` | instrução persistente do projeto | automaticamente em todo chat | conteúdo completo em todo chat | invariantes curtas e universais |
| Rule `Intelligent` | Rule selecionada por relevância | descrição avaliada pelo Agent | conteúdo entra quando selecionada | orientação temática |
| Rule com `Globs` | Rule vinculada a padrões de arquivo | autoanexada quando o padrão corresponde | conteúdo entra em tarefas correspondentes | convenções de código |
| Rule `Manual` | Rule sob demanda | `@nome-da-rule` | somente quando chamada | workflows ocasionais |
| Skill | instruções especializadas para um workflow | descoberta por descrição ou invocação pelo `/` | descrição ajuda discovery; instruções entram quando ativadas | manter escopo estreito e acionável |
| MCP | servidores e ferramentas externas conectadas | catálogo/instruções e chamadas disponíveis | catálogo e instruções podem ocupar contexto | conectar somente servidores necessários |
| Subagent | Agent delegado em janela própria | o Agent pai o invoca | o pai recebe o resultado, não todo o processo intermediário | delegar pesquisa ou logs volumosos com escopo definido |

Desativar um recurso só é otimização quando ele está contribuindo com contexto ou coordenação sem benefício para a tarefa atual.

## 9. Perfis exemplificativos de seleção

Estes perfis exemplificam a aplicação da rota canônica da [seção 3](#3-candidatos-por-atividade-modo-e-dificuldade); não a substituem. Compare o contexto equivalente definido na [amostra controlada mínima](#amostra-controlada-mínima) e o custo por entrega, não apenas preço por token.

| Perfil | Início | Menor custo, quando validado | Promoção por capacidade | Critério |
| --- | --- | --- | --- | --- |
| Q&A, extração e formatação | `gpt-5.4-nano-medium` ($0.20 in / $1.25 out) | já é o baseline | `composer-2.5` ($0.50 in / $2.50 out) | saída correta e curta |
| Edição e código repetitivo | `kimi-k2.7-code` ($0.95 in / $4 out) | `gpt-5.4-nano-medium` ($0.20 in / $1.25 out) para transformações simples | `glm-5.2-high` ($1.40 in / $4.40 out) | testes e taxa de retrabalho |
| Repositório grande e terminal | `glm-5.2-high` ($1.40 in / $4.40 out) | `kimi-k2.7-code` ($0.95 in / $4 out) quando 256k bastar | `cursor-grok-4.6-medium` ($2 in / $6 out) | contexto necessário e tool use |
| Desenvolvimento multi-arquivo | `cursor-grok-4.6-medium` ($2 in / $6 out) | `glm-5.2-high` ($1.40 in / $4.40 out) | `gpt-5.4-high` ($2.50 in / $15 out) | integração e testes aprovados |
| Discovery e arquitetura | `kimi-k3-max` ($3 in / $15 out) | `glm-5.2-high` ($1.40 in / $4.40 out) | `claude-opus-5-thinking-high` ($5 in / $25 out) | qualidade da decisão e reversibilidade |
| Debugging intermitente ou multi-sistema | `gpt-5.6-sol-medium` ($4 in / $20 out) | `glm-5.2-high` ($1.40 in / $4.40 out) | `claude-opus-5-thinking-high` ($5 in / $25 out) | hipóteses testadas e correções posteriores |

## 10. Catálogo seletivo por preço e responsabilidade

Esta seção lista somente os modelos usados pelas rotas recomendadas neste guia; não é um catálogo completo dos modelos disponíveis no Cursor. A ordenação prioriza preço `in` e, em seguida, preço `out`, para localizar rapidamente as opções mais baratas.

> 💲 **Leitura dos preços:** `$0.20 in / $1.25 out` significa USD por 1M de tokens de entrada/saída. São referências de uso/contabilização no Cursor, não instruções para configurar uma API própria. A disponibilidade e o pool dependem do plano.

| Modelo | Preço Cursor in/out | Contexto e notas | Responsabilidade apropriada | Evite como padrão para |
| --- | --- | --- | --- | --- |
| `gpt-5.4-nano-medium` | $0.20 in / $1.25 out | menor GPT-5.4 | extração, classificação, formatação e Q&A simples | debugging sistêmico ou arquitetura |
| `gpt-5-mini` | $0.25 in / $2 out | pode estar oculto por padrão | Q&A e pequenas transformações | execução agentic complexa |
| `composer-2.5` | $0.50 in / $2.50 out | Cursor Models; Fast: $3 in / $15 out | loop curto de edição no Cursor | raciocínio arquitetural ou contexto amplo |
| `kimi-k2.7-code` | $0.95 in / $4 out | contexto declarado de 256k; cache read $0.19 | código repetitivo, edição, testes locais e volume | contexto acima de 256k ou arquitetura de alto risco |
| `claude-haiku-4.5` | $1 in / $5 out | contexto declarado de 200K; cache read $0.10 | subtarefas rápidas, volume e agentes auxiliares | decisão crítica isolada |
| `glm-5.2-high` | $1.40 in / $4.40 out | contexto declarado de até 1M; cache read $0.26 | repository work, tool use, refactor e tarefas longas | anexar 1M sem necessidade demonstrada |
| Gemini 3.6 Flash | $1.50 in / $7.50 out | contexto declarado de até 1M; disponibilidade pode variar | agentic e multimodal, quando disponível | assumir disponibilidade ou qualidade universal |
| `cursor-grok-4.6-medium` | $2 in / $6 out | pool Cursor; limites podem variar | desenvolvimento geral, integração e tool loops | toda tarefa simples |
| `claude-sonnet-5` | $2 in / $10 out | contexto declarado de até 1M; tokenizer próprio | síntese, documentação e código complexo | extração trivial ou volume máximo |
| `gpt-5.4-high` | $2.50 in / $15 out | long context pode elevar o input | código avançado e contexto amplo justificado | tarefas simples |
| `kimi-k3-max` | $3 in / $15 out | contexto declarado de até 1M | discovery, raciocínio amplo e arquitetura | edição curta de baixo risco |
| `composer-2.5-fast` | $3 in / $15 out | variante para latência; valide o ganho | edição quando latência comprovadamente domina | presumir que Fast reduz custo |
| `gpt-5.6-sol-medium` | $4 in / $20 out | contexto declarado de até 1M; limites long context podem aplicar sobretaxa | Agent/debug avançado e hipóteses concorrentes | tarefas rotineiras |
| `claude-opus-5-thinking-high` | $5 in / $25 out | contexto declarado de até 1M | ADR/RFC e decisões críticas | documentação comum |

Nenhuma linha significa superioridade universal. Aceite a responsabilidade como hipótese somente quando uma amostra mostrar menos falhas e retrabalho por custo total.

## 11. Comparações exemplificativas orientadas à decisão

Esta seção aplica a rota canônica da [seção 3](#3-candidatos-por-atividade-modo-e-dificuldade) a cenários comuns; ela não define rotas adicionais. As capacidades são declarações dos fornecedores ou do catálogo do Cursor; elas não demonstram desempenho superior no repositório atual.

### GLM 5.2 ($1.40 in / $4.40 out) × Kimi K2.7 ($0.95 in / $4 out)

- **Preço:** `glm-5.2-high` ($1.40 in / $4.40 out); `kimi-k2.7-code` ($0.95 in / $4 out).
- **Use `glm-5.2-high` ($1.40 in / $4.40 out) quando:** o repositório, o terminal ou o horizonte da tarefa exigirem o contexto declarado maior.
- **Use `kimi-k2.7-code` ($0.95 in / $4 out) quando:** a edição, os testes e o volume couberem em 256k.
- **Validação:** compare testes aprovados, tokens, tool calls e retrabalho com o mesmo contexto.

### GLM 5.2 ($1.40 in / $4.40 out) × Grok 4.6 ($2 in / $6 out)

- **Preço:** `glm-5.2-high` ($1.40 in / $4.40 out); `cursor-grok-4.6-medium` ($2 in / $6 out).
- **Use `glm-5.2-high` ($1.40 in / $4.40 out) quando:** custo de token e tarefa longa dominarem.
- **Use `cursor-grok-4.6-medium` ($2 in / $6 out) quando:** integração, execução e tool loop forem o principal risco.
- **Validação:** meça intervenções humanas, latência e correções posteriores; preço menor não prova execução melhor.

### GLM 5.2 ($1.40 in / $4.40 out) × GPT-5.4 High ($2.50 in / $15 out)

- **Preço:** `glm-5.2-high` ($1.40 in / $4.40 out); `gpt-5.4-high` ($2.50 in / $15 out).
- **Use `gpt-5.4-high` ($2.50 in / $15 out) quando:** a amostra demonstrar necessidade de raciocínio ou execução superior.
- **Use `glm-5.2-high` ($1.40 in / $4.40 out) quando:** a capacidade declarada e o custo menor forem suficientes.
- **Cautela:** long context pode alterar o custo do GPT; não anexe contexto máximo sem necessidade.

### Kimi K3 ($3 in / $15 out) × Claude Sonnet ($2 in / $10 out) / Opus ($5 in / $25 out)

- **Preço:** `kimi-k3-max` ($3 in / $15 out); `claude-sonnet-5` ($2 in / $10 out); `claude-opus-5-thinking-high` ($5 in / $25 out).
- **Use `kimi-k3-max` ($3 in / $15 out) quando:** contexto, raciocínio e agent loop forem a necessidade demonstrada.
- **Use `claude-sonnet-5` ($2 in / $10 out) quando:** síntese, documentação ou código complexo exigirem custo intermediário.
- **Use `claude-opus-5-thinking-high` ($5 in / $25 out) quando:** o custo de uma decisão errada justificar o prêmio.
- **Cautela:** a origem do modelo não é critério suficiente para promoção.

O custo-benefício deve ser calculado por entrega:

`custo efetivo = tokens + cache + tool calls + coordenação + retrabalho + latência operacional`

Para mudar uma rota padrão, execute a [amostra controlada mínima](#amostra-controlada-mínima) com contexto equivalente e registre sucesso por critério objetivo, testes, tokens in/out, cache hit, ferramentas, tempo, intervenções e correções posteriores.

## 12. Checklist

- [ ] Identifique a maior categoria no context ring.
- [ ] Remova somente MCP, plugins, skills, subagents ou Rules sem uso que contribuam para essa categoria.
- [ ] Reduza `Always Apply` ao mínimo ou altere o tipo de ativação quando apropriado.
- [ ] Use seleção ou `@arquivo` antes de anexar pasta, branch ou terminal.
- [ ] Defina a atividade antes de escolher modo, modelo e effort.
- [ ] Comece com o menor modelo compatível com o risco e os testes necessários.
- [ ] Abra novo chat ao mudar de objetivo e gere um handoff curto, manual ou pela skill de handoff.
- [ ] Confira novamente o context ring sem remover evidência necessária.
- [ ] Registre custo efetivo, qualidade e retrabalho antes de promover uma rota.

## 13. Fontes oficiais

> 🔎 **Rastreabilidade:** revalide preços, modelos, capacidades, limites e atalhos antes de decisões de longo prazo.

- Cursor: [Models & Pricing](https://cursor.com/docs/models-and-pricing), [Prompting agents](https://cursor.com/docs/agent/prompting), [Rules](https://cursor.com/docs/rules), [Subagents](https://cursor.com/docs/subagents), [Keyboard shortcuts](https://cursor.com/docs/reference/keyboard-shortcuts).
- Capacidades dos fornecedores: [xAI models](https://docs.x.ai/developers/models), [Kimi Code models](https://www.kimi.com/code/docs/en/kimi-code/models), [Z.ai GLM 5.2](https://docs.z.ai/guides/llm/glm-5.2).

Os modelos são selecionados no model picker dos agentes do Cursor. O usuário não precisa fornecer uma chave de API própria para usar os modelos disponibilizados pelo Cursor. A documentação de preços do Cursor, entretanto, distingue o pool Cursor Models do pool Other Models e pode descrever o uso de modelos de terceiros por taxas equivalentes às da API dentro da contabilização do Cursor; isso não deve ser confundido com consumo direto de uma API externa.

> ⚠️ **Limite metodológico:** eficiência vem de limitar contexto sem retirar a evidência necessária para produzir uma resposta correta. Preço, contexto declarado e disponibilidade não constituem promessa de acerto.
