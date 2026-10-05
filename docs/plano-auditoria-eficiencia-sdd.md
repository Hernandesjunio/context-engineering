# Plano de instruções para auditar eficiência de SDD

> **Uso:** entregue este documento à IA que tem acesso ao repositório, às instruções do fluxo e aos registros de execução. Ela deve identificar os problemas, preparar e aplicar correções dentro da autorização vigente, validar o resultado e entregar o fluxo corrigido com evidências. Não encerrar o trabalho apenas com recomendações quando a correção estiver autorizada. Este documento não contém uma auditoria já realizada.
>
> **Objetivo:** reduzir custo total e consumo de contexto por feature aceita, preservando contratos, testes, revisão e rastreabilidade. Validar e otimizar contexto persistente durante waves atômicas pequenas, usando o relatório da execução anterior como referência histórica de consumo.

## 1. Missão, dados corrigidos e fatos disponíveis

Você é responsável por auditar um fluxo de **SDD — desenvolvimento orientado por especificações**. Primeiro observe o comportamento real; depois proponha e teste a menor alteração capaz de resolver os principais custos encontrados.

Informações fornecidas pelo usuário e evidência disponível no ambiente de origem:

- O fluxo implementa uma feature do início ao fim corretamente na avaliação do usuário.
- Já existem context packs, contracts e waves. Não propor esses mecanismos como se estivessem ausentes.
- Developer, Reviewer e Test Engineering são coordenados pelo Orchestrator.
- Antes, cada invocação começava em uma janela de contexto vazia, inclusive nas alternâncias de TDD RED/GREEN.
- A alteração recente mantém a janela de contexto durante a wave, mas ainda não foi testada.
- Dados corretos extraídos do relatório após a execução: custo aproximado de **US$ 5,16**, **14 execuções**, **17,5 milhões de cache read**, **674 mil de entrada nova** e **85 mil de saída**. Total informado: aproximadamente **18 milhões**. Estes dados substituem o número anterior de 18 milhões para esta análise.
- Entrega produzida: classe de testes de aproximadamente 60 linhas; classe de MemoryStore de aproximadamente 20 linhas; Program com Minimal API e dois GETs em aproximadamente 15 linhas. Não havia integração externa nem complexidade de negócio.
- Distribuição informada: 95,8% cache read, 3,7% entrada nova e 0,5% saída. A soma das categorias aproximadas é 18,259 milhões, coerente com o total arredondado de 18 milhões.
- Waves já são operações atômicas pequenas. O objetivo é equilibrar seu tamanho com a retenção de contexto, evitando reinícios e nova exploração dentro da mesma wave.

**Distinção de evidências:** o consumo anterior foi registrado em relatório. Os valores extraídos foram fornecidos à IA autora deste plano; o relatório completo e a sequência de chamadas continuam no ambiente de origem. A IA executora deve consultá-los para atribuir causas, sem reabrir a existência dos números como hipótese. A origem documental do volume não comprova isoladamente a causa, e a eficácia da alteração recente ainda precisa ser medida. Não confundir esta execução com registros históricos de outras tarefas.

**Direção adotada:** preservar contexto dentro da wave como estratégia principal. A janela limpa por invocação já apresentou resultado operacional inadequado de consumo para o usuário. Não exigir novas execuções caras dessa estratégia como pré-requisito; aproveitar seus registros históricos e concentrar o piloto na estratégia atual.

**Resultado principal:** custo total por feature aceita. **Resultados complementares:** entrada acumulada, chamadas ao modelo, tempo até aceitação e retrabalho. Uma redução de tokens sem preservação da qualidade não atende à missão.

## 2. Regras de execução da auditoria

1. Leia primeiro as regras obrigatórias do projeto e localize o ponto de entrada do fluxo. Use busca direcionada; não carregue o repositório inteiro para iniciar a auditoria.
2. Registre a autorização existente. Execute leituras, diagnóstico e verificações locais reversíveis dentro dela; não introduza um novo gate apenas por este documento. Alterações no fluxo e pilotos seguem a autorização vigente do projeto.
3. Reutilize os documentos e instrumentos existentes. Este plano é uma lista de verificações, não uma exigência de criar um arquivo para cada seção.
4. Separe **observado**, **calculado**, **hipótese** e **não mensurável**. Toda conclusão causal precisa de evidência local ou experimento comparável.
5. Não declare economia, conformidade com SDD ou aprovação de qualidade apenas porque a configuração mudou.
6. Não remova testes, revisão ou regras obrigatórias para produzir um ganho artificial.
7. Não invente APIs de retomada de agentes, campos de configuração, telemetria ou preços. Verifique o suporte da ferramenta e versão instaladas.
8. Mantenha o custo da própria auditoria separado do custo do benchmark. Se a otimização exigir preparação recorrente, inclua essa preparação no custo operacional.
9. Antes de executar um piloto potencialmente caro, configure orçamento e limites finitos no mecanismo disponível. Limite atingido significa execução interrompida/inconclusiva, nunca aceitação automática.

## 3. Fase A — reconstruir o fluxo real

Produza um mapa curto com referências verificáveis para os seguintes itens:

| Item | O que localizar e confirmar |
| --- | --- |
| Entrada | Comando ou instrução que inicia uma feature; requisitos fornecidos; contexto automático |
| Planejamento | Como especificações geram contratos, tarefas e waves; gates e critérios de aceite |
| Papéis | Instruções efetivamente carregadas por cada papel, não apenas arquivos cadastrados |
| Invocação | Criação, retomada ou troca de papel; identificadores de sessão; contexto herdado |
| TDD | Ordem real de autoria de testes, RED, implementação, GREEN e refatoração |
| Correções | Quem recebe findings; se é retomado; limites de tentativas; condições de parada |
| Estado | Fonte de verdade; transições; artefatos e evidências usados para concluir |
| Contexto | Conteúdo incluído, leitura obrigatória e consulta condicional de cada pack |
| Ferramentas | Buscas, leituras, comandos, logs e resultados devolvidos ao modelo |
| Medição | Contadores por chamada, execução, papel e wave; cobrança e cache disponíveis |

Para cada arquivo relevante, cite caminho e seção/símbolo. Para execução, cite run, chamada, sessão e estado de código. Commit-base sozinho não identifica alterações ainda não commitadas: registre também um identificador do snapshot ou hash do diff e dos arquivos relevantes não rastreados.

### 3.1 Esclarecer o significado de “mesma janela”

Determine qual implementação existe:

| Política | Comportamento | Questão a verificar |
| --- | --- | --- |
| Nova sessão a cada invocação | Cada papel/tentativa recebe uma base nova | Quanto custa reconstruir o contexto? |
| Sessão persistente por papel e wave | Developer retoma sua sessão; Reviewer e Tester têm sessões próprias | Evita reconstrução sem acumular todas as etapas em cada papel? |
| Uma sessão compartilhada por wave | A mesma conversa alterna instruções de Developer, Tester e Reviewer | Quanto histórico cruza os papéis? A revisão fica influenciada pela implementação? |
| Herança de conversa do orquestrador | Agentes recebem parte ou todo o histórico do coordenador | O pack é pequeno, mas o contexto efetivo é grande? |

Uma interface mostrar a mesma janela não comprova a mesma sessão no backend. Na retomada, o histórico estável pode ser reutilizado por cache; isso pode reduzir processamento repetido e custo. O cache não elimina os tokens da janela nem garante acerto em toda chamada. Confirme a reutilização real pela telemetria e pela documentação aplicável.

Se uma conversa compartilhada alterna papéis, verifique como instruções, critérios de review e julgamento são aplicados. Compartilhar contexto não elimina a necessidade de confrontar o contrato e procurar defeitos, nem comprova perda de qualidade. A separação de histórico é diferente da separação de responsabilidades: meça a eficácia da revisão e preserve exigências explícitas de independência do projeto. Não exigir nova janela apenas por preferência arquitetural.

### 3.2 Política prioritária: contexto persistente e wave pequena

1. Carregar o núcleo da wave e as instruções aplicáveis na entrada; preservar o contexto ao longo de RED, GREEN, review e correções.
2. Reutilizar informações disponíveis e atuais. Não repetir exploração para apenas reconstruir o conhecimento; consultar novamente quando houver mudança, lacuna ou contradição.
3. Enviar mudanças e resultados novos sem reescrever o histórico estável. Conferir se a troca de papel modifica instruções ou ferramentas no início do prompt e reduz o cache.
4. Para cache de prefixo, texto inalterado isoladamente não basta: o prefixo elegível e as configurações relevantes precisam continuar compatíveis [S3]. Não adicionar timestamp ou estado variável antes do conteúdo estável sem necessidade. Não inventar controles que o harness não expõe.
5. Manter escopo, logs e correções proporcionais à wave. Não compactar por rotina uma sessão pequena e eficaz: compactação também tem custo e pode alterar o prefixo reutilizável.
6. Encerrar a sessão no limite definido da wave, mantendo handoff suficiente para dependências futuras. Persistência dentro da wave não significa carregar todo o projeto entre waves.
7. Medir tamanho inicial/final/pico, crescimento por chamada, cache, novas leituras e custo. Investigar inflação apenas se observada; uma wave pequena é uma condição favorável, não motivo para presumir crescimento problemático.

O equilíbrio procurado é menos descoberta repetida, alto reaproveitamento do contexto estável e crescimento limitado durante uma unidade pequena de trabalho. O consumo acumulado pode continuar alto por leituras de cache enquanto o custo cai; avaliar ambos separadamente.

## 4. Fase B — validar SDD e governança proporcional

Use esta matriz como critérios operacionais desta auditoria. GitHub Spec Kit é uma referência de implementação, não uma certificação universal de SDD [S1]. SDD não deve ser reduzido à quantidade de agentes ou de arquivos.

| Critério | Evidência exigida | Desvio a procurar |
| --- | --- | --- |
| Especificação clara | Comportamento observável, entradas/saídas e limites | Agentes inventam requisitos para preencher lacunas |
| Fonte de verdade | Contrato canônico identificado e vigente | Packs e documentos contêm versões contraditórias |
| Rastreabilidade | Requisito → tarefa/wave → alteração → teste/evidência | Feature encerrada sem demonstrar requisitos |
| Plano proporcional | Etapas justificadas por risco e complexidade | Cerimônia de feature complexa aplicada a mocks triviais |
| Waves delimitadas | Resultado testável, dependências e condição de saída | Muitas waves repetem descoberta para uma mesma mudança pequena |
| TDD verificável | RED relevante antes da implementação; GREEN no estado posterior | RED causado por ambiente; teste alterado para acomodar defeito |
| Review eficaz | Findings baseados no contrato e código pertinente | Reviewer apenas confirma o handoff do developer |
| Estado consistente | Transições e evidências vinculadas ao snapshot | GREEN ou aprovação de versão anterior reutilizados após mudança |
| Correções finitas | Limites claros; nova tentativa explica o que mudou | Loop repetido sem progresso ou saída objetiva |
| Encerramento | Requisitos atendidos, checks finais e limitações | Orchestrator reexecuta todas as etapas sem motivo ou aceita sem prova |

Classifique cada critério como atende, parcial, não atende, não aplicável ou sem evidência. Justifique “não aplicável”. Não exija TDD onde ele não foi selecionado, mas valide sua ordem onde foi.

### 4.1 Auditoria de suficiência dos pacotes SDD

Um pacote é suficiente para iniciar e conduzir a responsabilidade quando oferece a decisão e os pontos de entrada necessários, sem obrigar o agente a redescobrir a estrutura já identificada. **Suficiente não significa copiar todo o repositório ou proibir investigação adicional.** Reutilize o formato já existente.

| Elemento do pacote | Teste de suficiência | Correção quando ausente/ineficaz |
| --- | --- | --- |
| Missão e aceite | Agente sabe o que entregar e como demonstrar? | Remover ambiguidade na especificação canônica |
| Contrato e restrições | Pode implementar sem adivinhar rota, payload ou padrão? | Incluir cláusulas pertinentes ou apontar seção exata |
| Entradas de código | Sabe por onde começar e o que reutilizar? | Indicar arquivos/símbolos relevantes já mapeados |
| Padrões/skills | Sabe quais são aplicáveis e em que condição expandir? | Seleção explícita; evitar carregar toda a biblioteca |
| Contexto disponível | Distingue conteúdo já presente de referência a ler? | Marcar incluído, obrigatório e condicional |
| Estado e versão | Sabe o que mudou e quais evidências continuam válidas? | Atualizar estado/delta e vincular ao snapshot |
| Papel e saída | Sabe a responsabilidade atual e quando devolvê-la? | Critério de término e handoff conciso |
| Comandos de validação | Sabe quais checks executar, sem redescobrir setup? | Reutilizar comandos conhecidos e explicar exceções |

Teste o pacote observando a execução: registre cada expansão significativa com pergunta não respondida e motivo. Classifique como lacuna do pacote, referência desatualizada, investigação legítima por mudança ou exploração redundante apesar de informação suficiente. Corrija a categoria responsável; não aumente o pack indiscriminadamente.

Dois defeitos podem coexistir: o pacote contém tudo, mas a instrução manda explorar novamente; ou a instrução manda usar o pacote, mas ele não contém os pontos de entrada. A correção deve atingir a origem, não apenas pedir “gaste menos tokens”.

## 5. Fase C — explicar o consumo documentado de aproximadamente 18 milhões

### 5.1 Decompor o relatório existente antes de explicar a causa

Comece pelo relatório extraído após a implementação. Use-o como evidência do volume registrado; identifique categorias, intervalo e chamadas associadas. A reconciliação esclarece a composição, não exige que o usuário prove novamente que observou o consumo.

- Identifique o intervalo medido e quais runs estão incluídos: planejamento, implementação, retries, execuções abortadas e agentes auxiliares.
- Determine se o painel mostra total acumulado, consumo faturável, estimativa ou unidades de créditos. Registre a definição oficial da métrica.
- Confirme se entrada inclui cache ou se as categorias são separadas. Não some um subtotal novamente ao total.
- Identifique retries do proxy/provedor e chamadas invisíveis à UI, se observáveis. Reconcilie por request ID e attempt ID; tentativas reais não são duplicatas de telemetria.
- Distinga contadores acumulativos de sessão de deltas por chamada. Somar snapshots acumulativos infla o total.
- Compare a soma normalizada com o painel e explique qualquer diferença. Se faltam registros, declare a cobertura e a impossibilidade de reconciliar integralmente.

### 5.1.1 Leitura correta dos números

| Categoria | Volume aproximado | Participação no total das categorias |
| --- | --- | --- |
| Cache read | 17.500.000 | 95,84% |
| Entrada nova | 674.000 | 3,69% |
| Saída | 85.000 | 0,47% |
| Soma | 18.259.000 | 100% |

Os percentuais informados são consistentes com arredondamento. Sobre a entrada, excluindo saída, a participação de cache é aproximadamente **96,29%**. Não confundir essa taxa com 95,8% do total de tokens.

**Conclusões sustentadas pelos dados:**

- Houve alto reaproveitamento por cache no fluxo anterior, apesar de novas janelas. Não caracterizar o problema como falta generalizada de cache.
- O trabalho teve volume acumulado grande em relação à tarefa descrita. Cache alto não demonstra que o fluxo foi enxuto; pode haver contexto grande repetido, muitas chamadas ou ambos.
- Os 674 mil tokens de entrada nova e 85 mil de saída também merecem decomposição. Entrada nova não significa conteúdo semanticamente inédito: inclui material que não obteve cache. Saída inclui mais do que o código final, conforme o relatório: planejamento, coordenação e outras respostas podem contribuir.
- US$ 5,16 é o custo observado. Percentual de tokens por categoria não é percentual de custo: tarifas distintas impedem essa inferência sem modelo e cobrança por categoria.
- As aproximadamente 95 linhas finais descrevem a simplicidade da entrega, mas não servem como denominador universal de eficiência. Avaliar trabalho realizado, requisitos atendidos e validações necessárias.

**As 14 execuções precisam ser identificadas.** Podem ser invocações de agentes, sessões, operações agregadas ou outra unidade do relatório. Não presumir 14 chamadas ao modelo nem 14 features completas. Se forem unidades do mesmo conjunto, os quocientes descritivos são aproximadamente 1,304 milhão de tokens, 48,1 mil de entrada nova, 6,1 mil de saída e US$ 0,37 por unidade. Esses valores não medem tamanho de uma janela.

A pergunta causal é: **quais etapas, chamadas e conteúdos produziram esse volume, e quais deixaram de ser necessários com continuidade na mesma wave?**

### 5.2 Hipóteses e testes de evidência

| Hipótese | Evidência local necessária | Intervenção isolável |
| --- | --- | --- |
| Reinícios reconstroem conhecimento | Sessões novas repetem buscas/leituras do mesmo conteúdo | Retomar sessão por papel/wave |
| Histórico cresce excessivamente | Entrada por chamada aumenta mesmo com poucas leituras novas | Handoff compacto ou compactação controlada |
| Pack não controla o contexto efetivo | Regras, herança ou anexos adicionam conteúdo além do pack | Corrigir seleção/injeção na origem |
| Dependências de skills expandem leitura | Grafo de referências carrega material não aplicável | Carregamento condicional com gatilhos |
| Logs dominam o histórico | Grande volume de saída de build, teste, busca e arquivos | Resumo fiel com logs completos recuperáveis |
| TDD multiplica delegações | Reinício de papéis por teste/comando ou transição RED/GREEN | Retomar papéis no ciclo existente |
| Orchestrator duplica trabalho | Reanalisa implementação e reroda checks já válidos | Consolidar evidências atuais sem reexecução automática |
| Loops não convergem | Repetição de falha/finding sem mudança relevante | Condição de parada baseada em progresso |
| Granularidade excessiva | Custo de preparação domina pequenas waves | Avaliar agrupamento após o primeiro experimento |
| Categorias precisam de normalização | Definições ou agregações do relatório diferem da telemetria por chamada | Harmonizar métricas sem descartar o volume documentado |

Ordene causas por contribuição mensurada e confiança. Se componentes de prompt não forem visíveis, use estimativas identificadas como estimativas; bytes ou palavras não são contagem exata de tokens. Não atribua todo o consumo aos agentes novos por plausibilidade.

## 6. Fase D — instrumentação mínima

Prefira logs já disponíveis. Se necessário e autorizado, acrescente um evento por chamada ao modelo em formato estruturado, mantendo payloads sensíveis fora do relatório. Não registre prompts completos apenas para medir tokens.

Campos mínimos; ausências ficam `null` com motivo, nunca zero presumido:

```json
{
  "run_id": "identificador-real",
  "variant": "A",
  "feature_id": "identificador-real",
  "wave_id": "identificador-real",
  "role": "developer",
  "phase": "green",
  "session_id": "identificador-real-ou-null",
  "request_id": "identificador-real-ou-null",
  "attempt_id": "identificador-real-ou-null",
  "code_state_id": "snapshot-real",
  "model": "modelo-e-versao-observados",
  "started_at": "timestamp-real",
  "duration_ms": null,
  "input_total_tokens": null,
  "input_uncached_tokens": null,
  "cache_read_tokens": null,
  "cache_write_tokens": null,
  "output_total_tokens": null,
  "reasoning_tokens": null,
  "billed_cost": null,
  "cost_currency": null,
  "usage_schema": "definicao-do-provedor-e-versao",
  "measurement_status": "partial"
}
```

Esse é um **modelo conceitual de registro**, não uma API pronta. Adapte-o ao schema real. Preserve os contadores originais para auditar a normalização. Reasoning pode estar incluído na saída: não o some novamente. Escrita de cache pode ter categorias e tarifas próprias; não aplique a semântica de um provedor a outro.

Registre também, quando disponíveis: bytes/tokens de ferramentas, arquivos distintos lidos, releituras da mesma versão, compactações, chamadas de coordenação, testes executados e intervenções humanas. Conte leituras repetidas como sinal investigativo; algumas são necessárias após mudanças.

### 6.1 Cálculos e indicadores

- **Entrada acumulada:** soma da entrada normalizada das chamadas reais, incluindo tentativas. Não é o pico da janela nem o volume de conteúdo único.
- **Pico de contexto:** maior entrada observada por chamada. Separar da entrada acumulada.
- **Taxa de cache:** soma das leituras de cache / soma da entrada total, somente quando cache é subconjunto da entrada. Se não for, use o denominador definido pelo provedor.
- **Custo por feature aceita:** custo de todas as execuções do conjunto avaliado / quantidade aceita. Incluir falhas e abortos; sem aceites, indicador indefinido.
- **Custo operacional:** planejamento + preparação recorrente + agentes + correções + ferramentas cobradas. Custos humanos e de infraestrutura podem ficar separados, com escopo explícito.
- **Custo estimado:** soma de tokens em categorias de cobrança mutuamente exclusivas × tarifa aplicável / 1 milhão. Incluir escrita de cache quando cobrada. Na presença de créditos ou preço opaco, apresentar créditos reais e não inventar valor em dinheiro.
- **Tempo:** medir parede até aceitação; discriminar inferência, ferramentas e espera quando possível. Em paralelo, somar durações mede trabalho agregado, não tempo de parede.
- **Qualidade:** aceites, falhas de contrato, correções, requisitos omitidos e defeitos encontrados pela validação final.
- **Economia:** `100 × (valor_A − valor_B) / valor_A`, com base positiva e escopo equivalente. Mostrar valores absolutos.

As docs de cache fornecem contadores de reutilização [S3], mas a medição precisa corresponder ao provedor, modelo e proxy efetivamente usados. Não existe limite universal de tokens para dois endpoints.

## 7. Fase E — benchmark simples e reproduzível

### 7.1 Especificação fixa da tarefa

No stack e convenções existentes, implementar **uma wave** com dois endpoints mockados:

| Requisito | Contrato e aceite |
| --- | --- |
| R1 | `GET /sdd-benchmark/items` retorna 200 e JSON `[{"id":1,"name":"Mock A"},{"id":2,"name":"Mock B"}]` |
| R2 | `GET /sdd-benchmark/items/{id}` retorna 200 e objeto correspondente para IDs 1 e 2 |
| R3 | ID numérico inexistente retorna 404, sem retornar item padrão |
| R4 | Content-Type JSON nas respostas 200; campos e tipos iguais ao contrato; ordem da coleção conforme R1 |
| R5 | Build e testes pertinentes passam; nenhuma integração externa ou persistência é necessária |
| R6 | Seguir estrutura e políticas obrigatórias existentes; evitar camadas, pacotes e infraestrutura sem necessidade para esta tarefa |

Se padrões do projeto exigirem envelope ou rota diferente, faça uma adaptação documentada **antes** de fixar a especificação. Use o mesmo contrato adaptado em todas as variantes. Não adicione autenticação, paginação, regra financeira ou novos requisitos só para aumentar complexidade; cumpra o que já é obrigatório no projeto.

### 7.2 Evidência de qualidade

Verifique o comportamento HTTP pelo mecanismo de integração já usado no projeto. Cobrir lista, detalhes 1 e 2, inexistente, campos/tipos e códigos de status. Testes não podem apenas chamar um mock que não atravessa o endpoint real.

No modo TDD:

1. Test Engineering deriva testes do contrato antes da implementação.
2. Registra RED por comportamento ausente/incorreto, com comando e snapshot. Falha de compilação só vale como RED se a API/símbolo esperado ausente for deliberadamente parte do ciclo e isso estiver explicado; falha de setup não vale.
3. Developer implementa o mínimo necessário.
4. Registra GREEN e refatora apenas quando há necessidade, repetindo checks afetados.
5. Reviewer confronta solução, contrato e evidências finais; correções invalidam checks impactados.

Como controle do benchmark, introduza temporariamente, em cópia isolada e após registrar o resultado da implementação, um defeito: devolver 200 para ID inexistente. O teste de R3 deve falhar. Restaure o estado e confirme GREEN. Essa verificação mede a capacidade de detecção do teste; seu custo deve ficar separado do custo de implementação e igual entre variantes. Não é exigência de suíte de mutation testing para o projeto todo.

### 7.3 Piloto prioritário da estratégia atual

| Referência/variante | Uso |
| --- | --- |
| A — histórica | Relatório e registros do fluxo anterior com sessão nova por invocação; referência de consumo já observado |
| B — atual | Executar contexto persistente por wave exatamente como implementado hoje |
| B2 — ajuste opcional | Corrigir um mecanismo observado em B: prefixo instável, releitura redundante, logs ou coordenação |

Comece por B. Mantenha modelos por papel, raciocínio quando configurável, contratos, skills, ferramentas, número de waves, gates, ordem TDD e checks. Faça uma calibração curta para confirmar telemetria e orçamento, depois busque até três execuções válidas de B dentro do orçamento. É evidência preliminar, sem garantia estatística.

Use A para localizar o custo anterior e avaliar a melhoria com as limitações de comparabilidade explícitas. Se o contrato, modelo, ambiente ou escopo forem diferentes, apresente evolução observada e mecanismos medidos, sem chamar a comparação de A/B controlado ou atribuir um percentual causal preciso.

**Não exigir três novas execuções da estratégia que já teve consumo inadequado.** Uma repetição de A só se justifica se existir pergunta essencial não respondida pelos registros e orçamento suficiente. A falta dessa repetição não impede diagnosticar B ou otimizar sua eficiência.

Se B mostrar um custo evitável, compare B/B2 alterando apenas um mecanismo. Cada run começa do mesmo snapshot sem endpoints implementados, em cópia/worktree isolada. Nunca apague mudanças do usuário. Não inclua soluções ou sessões de runs anteriores no contexto inicial; **preserve integralmente a continuidade planejada dentro de cada wave**. Alterne ordem B/B2 quando viável.

Registre versões, modelo/configuração, falhas de ambiente e cache observado. Separe resultados com cache predominantemente frio/aquecido quando possível; não alegue limpeza sem controle. Para qualidade, acrescente após o benchmark pequeno uma wave real representativa, se houver orçamento. Não infira inflação de contexto apenas pelo fato de existir persistência.

### 7.4 Controle de proporcionalidade: execução direta

Dentro do orçamento e da autorização local, executar uma referência simples: um agente, na mesma sessão, recebe o contrato e as regras obrigatórias, implementa a tarefa e executa os checks pertinentes sem a orquestração SDD completa. Registrar prompt/preparação e validar o resultado com o mesmo aceite externo usado nas variantes SDD.

Essa referência mede o custo da tarefa e o acréscimo da estrutura SDD. Não serve para declarar equivalência de governança se algum gate obrigatório foi removido; separar custo do agente direto e custo da validação externa. TDD deve ser igual nas comparações de contexto; se a execução direta não usar TDD, explicitar o contraste como controle de proporcionalidade, não experimento de sessão isolado.

Apresentar diferença absoluta e razão `custo_SDD / custo_direto` com custos positivos e escopo explicitado. A razão é descritiva; não há limite universal aceitável. Se o acréscimo vier de preparo e coordenação sem efeito observável no caso simples, preparar um caminho SDD proporcional que preserve especificação, rastreabilidade, testes e gates requeridos. Usar uma sessão com papéis sequenciais pode manter esses elementos sem recriar agentes a cada etapa. Confirmar o benefício também em uma tarefa real antes de generalizar.

## 8. Fase F — identificar, corrigir e validar o fluxo

**Obrigação de conclusão:** diagnóstico → patch concreto → aplicação autorizada → piloto → decisão. Quando mudanças locais estiverem autorizadas, não terminar com uma lista de sugestões. Se houver impedimento real, entregar o patch preparado e identificar exatamente o bloqueio.

### 8.1 Prioridades de investigação e correção

| Prioridade | Problema a demonstrar | Correção dirigida | Evidência de resolução |
| --- | --- | --- | --- |
| 1 | Agentes reconstroem conhecimento dentro da mesma wave | Preservar sessão compartilhada da wave e retirar instruções de redescoberta incondicional | Menos sessões/leituras/chamadas de descoberta, mantendo aceites |
| 2 | Packs insuficientes ou ignorados | Corrigir campos/referências ou instruções na origem | Menos expansões por lacuna e nenhuma omissão relevante |
| 3 | Coordenação repete decisões ou validação atual | Handoff curto; consolidar evidências do estado vigente | Menos chamadas/saída de coordenação e mesmos gates |
| 4 | Conteúdo demais é reenviado por hábito | Selecionar contexto aplicável; preservar prefixo estável quando suportado | Menor entrada por chamada e menor custo absoluto de cache |
| 5 | Logs e documentos duplicados aumentam histórico | Retornar resumo fiel e manter log recuperável | Menor entrada nova/saída de ferramentas sem perder diagnóstico |
| 6 | TDD reinicia papéis ou passa por ciclos vazios | Continuar RED/GREEN na sessão da wave; corrigir transições redundantes | RED/GREEN verificáveis com menos coordenação |
| 7 | Mesma falha retorna sem progresso | Atualizar hipótese, delta e check; respeitar limite finito | Menos tentativas repetidas e bloqueios explícitos |

As prioridades orientam a busca, não afirmam causas já demonstradas. Como cache já foi alto, **não priorizar elevar a taxa de cache isoladamente**. Reduzir o volume desnecessário lido do cache e o número de chamadas pode ser mais relevante.

### 8.2 Instrução operacional a adaptar ao orquestrador

> Durante a wave, preserve a sessão compartilhada e o conhecimento já carregado. Em cada transição, informe apenas papel atual, objetivo, estado/delta, checks necessários e condição de saída. Não repita exploração geral, contratos ou regras já disponíveis e atuais. Expanda contexto quando faltar informação concreta, houver mudança pertinente ou contradição. Tester e Reviewer devem validar contra os requisitos e o código efetivo, podendo contestar decisões anteriores. Registre evidências no estado analisado; finalize quando os aceites forem comprovados. Use os contratos e artefatos existentes como fonte canônica.

Aplicar apenas o mecanismo suportado pelo harness. Se a troca de papel muda o início do prompt, verificar perda de cache e corrigir a organização quando possível. Não substituir instruções de sistema por texto de menor precedência nem omitir regras obrigatórias para manter cache.

### 8.3 Ciclo de correção verificável

1. Para cada problema, apontar instrução/configuração responsável e evidência da execução.
2. Preparar alteração mínima com antes/depois. Não criar novo agente, família de arquivos ou camada sem necessidade.
3. Versionar e aplicar dentro da autorização vigente; registrar como reverter.
4. Executar B/B2 com o mesmo contrato, modelo, checks e estado inicial para isolar o ajuste.
5. Comparar custo real, entrada nova, cache absoluto, saída, chamadas, tempo e qualidade. Cache percentual pode subir ou cair sem determinar sozinho o sucesso.
6. Manter a correção se houver ganho observado e aceites preservados. Se insuficiente, investigar o próximo mecanismo, com orçamento e limite finitos. Não iterar indefinidamente esperando atingir percentual arbitrário.

Compactação é condicional ao crescimento observado, não rotina obrigatória para uma wave pequena. Independência de contexto adicional só quando exigida pela política ou justificada por defeito de revisão demonstrado; não reinstalar janelas novas como solução automática.

## 9. Orçamento, decisão e reversão

Antes do piloto, registre orçamento total, alerta por run, teto por run, limite de chamadas/tentativas e como interromper efetivamente. Reutilize limites existentes quando adequados. Se faltarem, proponha valores com base na calibração e nas restrições reais; não inicie repetidamente uma execução com potencial de consumir outros 18 milhões sem teto.

Defina previamente meta de economia e tolerância de tempo. Compare B com A histórica apenas no grau de comparabilidade disponível; use B/B2 para medir causalmente um ajuste isolado quando necessário. Na ausência de meta empresarial, reportar ganho absoluto e percentual observado, preservação de qualidade e variabilidade; não impor um percentual arbitrário como obrigação de continuar rodando. No novo piloto, registrar custo monetário como na referência de US$ 5,16. Se essa medição ficar indisponível, comparar entrada nova, cache e chamadas separadamente como proxies, sem declarar ganho financeiro comprovado.

Apresente resultados por run, não só mediana; custos do conjunto incluem falhas e abortos. Não exclua execuções ruins depois de ver os resultados. Runs com defeito de medição ou ambiente podem ser separados com justificativa, mantendo seu consumo visível.

- **Adotar provisoriamente:** ganho observado, qualidade preservada e mecanismo consistente com as evidências.
- **Continuar investigando:** resultados variáveis, amostra insuficiente ou medição parcial.
- **Reverter:** omissões, piora de revisão, contexto desatualizado ou custo maior associado à mudança.

Reversão restaura instruções/configuração anteriores, preserva código válido e registros e reexecuta somente checks impactados. Versione a alteração para tornar a reversão concreta.

## 10. Entregáveis obrigatórios da IA executora

Entregue um relatório conciso com evidências anexáveis, sem reproduzir todo o contexto:

1. **Fluxo real:** sequência, sessões, packs e limites; diferenças em relação ao relato.
2. **Validação SDD:** matriz da seção 4 preenchida e critérios sem evidência.
3. **Diagnóstico de consumo:** decomposição dos US$ 5,16 e aproximadamente 18 milhões de tokens; significado das 14 execuções; distribuição por papel/fase e causas ordenadas por impacto/confiança; auditoria de suficiência dos packs.
4. **Correções concretas:** patches de instruções/configuração/pacotes, motivo, antes/depois, aplicação realizada, fontes preservadas e reversão. Evitar recomendações genéricas já implementadas.
5. **Resultado do piloto:** comandos, snapshots, checks, métricas por run, qualidade e custos de falhas/abortos.
6. **Decisão:** adotar, investigar ou reverter; limites da conclusão e próximo teste necessário.

Tabela mínima de resultados:

| Run | Variante | Sessões/chamadas | Entrada total/cache | Saída | Custo ou créditos | Tempo | Aceita? | Correções/omissões |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Preencher com medições reais | | | | | | | | |

Para cada finding: identificador, observado, evidência, impacto, hipótese causal, intervenção proposta e teste para validá-la. Se não executou o piloto, entregue diagnóstico e plano com status pendente; não preencha resultados previstos como medidos.

## 11. Fontes e limites desta orientação

Consultadas em 05/10/2026. Validar novamente compatibilidade específica no ambiente executor.

- **[S1] GitHub Spec Kit:** [documentação oficial](https://github.github.com/spec-kit/) e [conceitos de SDD](https://github.com/github/spec-kit/blob/main/docs/concepts/sdd.md). Referência para especificação, planejamento, tarefas e consistência; não estabelece custo universal nem exige esta topologia de agentes.
- **[S2] Anthropic:** [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents). Referência para gestão de contexto e compactação; aplicação ao fluxo concreto exige medição.
- **[S4] Anthropic:** [Building effective agents](https://www.anthropic.com/research/building-effective-agents). Referência para começar pela solução mais simples e justificar custo/latência adicionais pela melhoria de desempenho.
- **[S3] OpenAI:** [Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching) e [diagnóstico de cache](https://developers.openai.com/api/docs/guides/prompt-caching/diagnostics). Referência para observar reutilização de cache; semântica e cobrança dependem da configuração real.

O benchmark, critérios, orçamento, matriz e desenho de comparação deste documento são propostas operacionais para o caso relatado, não prescrições dos fornecedores. As fontes públicas não comprovam a causa dos 18 milhões de tokens.

Continuidade: o documento anterior “Otimização de contexto em um fluxo SDD por Waves” foi consultado. Este plano detalha a nova alteração de sessões e torna o experimento de dois endpoints executável; não substitui uma inspeção do repositório real.

Revisão após dados corrigidos: valores anteriores substituídos pelo detalhamento de aproximadamente 18 milhões de tokens e US$ 5,16; cache alto reconhecido; auditoria de suficiência dos packs, controle direto e ciclo de correção incorporados.

Validação deste material: revisão de coerência das definições, contagem, comparação histórica/controlada, TDD, autorização e condições de parada. Não houve execução do fluxo real nem avaliação independente por outro modelo.

## 12. Checklist final

- [ ] O fluxo foi inspecionado; caminhos e registros sustentam o mapa.
- [ ] O significado real de “mesma janela” foi confirmado.
- [ ] Contexto incluído, leituras e herança automática foram distinguidos.
- [ ] Os dados corrigidos substituíram o valor anterior: US$ 5,16; 14 execuções; 17,5 milhões cache; 674 mil entrada nova; 85 mil saída.
- [ ] As 14 execuções foram distinguidas de chamadas, sessões, waves e features.
- [ ] Os pacotes foram avaliados por suficiência operacional, atualidade e uso efetivo.
- [ ] O cache alto foi reconhecido; não se tratou taxa de cache como prova de eficiência.
- [ ] Cache, entrada, saída/reasoning e contadores acumulativos não foram somados duas vezes.
- [ ] Custos e preços foram observados ou explicitamente classificados como indisponíveis/estimados.
- [ ] SDD foi avaliado por critérios verificáveis, sem contar documentos como prova de qualidade.
- [ ] Um contrato único e snapshots equivalentes foram usados no benchmark.
- [ ] B foi medido com continuidade dentro da wave; não houve reinício involuntário nas trocas de papel.
- [ ] A histórica foi usada com suas limitações; não se exigiu repetição cara sem necessidade.
- [ ] B/B2, quando executado, alterou apenas um mecanismo.
- [ ] Prefixo estável, cache real, exploração evitada e crescimento da janela foram medidos separadamente.
- [ ] RED foi relevante e anterior; GREEN corresponde ao estado final.
- [ ] O teste de ID inexistente detectou o defeito controlado.
- [ ] A revisão verificou requisitos/código sem depender apenas do relato do developer.
- [ ] Falhas, abortos, preparação e correções aparecem no custo do conjunto.
- [ ] Orçamento e condições de parada estavam ativos antes das execuções.
- [ ] Resultados apresentam valores absolutos, amostra, variabilidade e limitações.
- [ ] As correções possuem patches concretos, status de aplicação e reversão definida.
- [ ] O trabalho autorizado não terminou apenas com diagnóstico ou sugestões.
- [ ] O controle direto foi executado ou sua ausência foi justificada; diferenças de governança ficaram explícitas.
- [ ] Nenhuma economia foi declarada sem medição; nenhuma execução interrompida foi aceita como concluída.
