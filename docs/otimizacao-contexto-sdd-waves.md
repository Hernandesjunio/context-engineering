# Otimização de contexto em um fluxo SDD por Waves

> **Objetivo:** reduzir custo total e tempo de execução por Wave aceita, preservando correção, testes, revisão independente e governança.
>
> **Limitação fundamental:** o fluxo descrito é uma aproximação fornecida pelo usuário. O repositório, as instruções reais e os registros de execução não foram examinados. Este documento orienta diagnóstico e um piloto; não confirma a causa do consumo nem autoriza refatoração automática.

## 1. Instruções para a IA que receber este documento

1. Leia as seções 1 a 4 antes de propor alterações.
2. No ambiente corporativo autorizado, confronte a proposta com os artefatos reais. Reutilize estruturas existentes antes de criar novos documentos.
3. Identifique o que já está implementado, o que diverge deste relato e o que continua desconhecido.
4. Apresente diagnóstico com evidências e um ajuste mínimo. Só implemente mediante autorização aplicável ao fluxo real.
5. Não solicite exportação de código, logs sensíveis ou documentos confidenciais para fora do ambiente autorizado.
6. Use as seções 5 a 9 como proposta adaptável, não como configuração nativa do Cursor ou política já aprovada.
7. Use o checklist final para validar a adaptação e o piloto. Não marque itens sem evidência.

**Precedência:** políticas corporativas e instruções vigentes do projeto prevalecem sobre esta proposta. Conflitos não resolvidos devem ser explicitados e escalados.

### Termos usados

- **DEVE / NÃO DEVE:** requisito para adotar esta proposta com segurança; não substitui normas corporativas.
- **RECOMENDA-SE:** orientação que pode ser adaptada mediante justificativa.
- **HIPÓTESE:** explicação ainda dependente de evidência do fluxo real.
- **Wave:** unidade de trabalho delimitada, desenvolvível, testável e revisável. Não significa necessariamente deploy independente ou transação de banco.
- **Pacote de contexto:** informações mínimas e referências selecionadas para executar uma responsabilidade na Wave.
- **Handoff:** registro objetivo do resultado de uma etapa para a seguinte.
- **Delta:** mudanças, findings e evidências novas em relação a uma base identificada.

## 2. Contexto conhecido e desconhecido

### 2.1 Relato do usuário — não auditado no repositório

- Fluxo SDD para aplicações .NET, usado no Cursor Enterprise.
- Artefatos incluem contratos, ADRs, BMAD, Waves, dependências, memória persistente e README; a lista não é exaustiva.
- Cada Wave possui documentos e referências para arquivos do projeto.
- Há três papéis por Wave: desenvolvimento, testes e revisão, coordenados por um orquestrador.
- Há correções limitadas, descritas como no máximo duas vezes, seguidas de gate humano quando necessário.
- Uma execução apresentou aproximadamente 58 milhões de tokens de entrada e 260 mil de saída, com muitos cache reads relatados.
- A qualidade observada pelo usuário é alta; custo e duração são os problemas principais.

### 2.2 Dados que precisam ser confirmados localmente

- Quais artefatos cada agente efetivamente recebe e lê; quais regras entram automaticamente.
- Se agentes novos são criados em toda etapa ou correção, e se existe retomada de sessão no mecanismo utilizado.
- Ordem real de desenvolvimento, testes e review. Três agentes por Wave não implica execução simultânea.
- Se o modo TDD está ativo e quais etapas ele altera.
- Se as referências da Wave já constituem um pacote suficiente, mas as instruções induzem exploração adicional.
- Semântica dos contadores de tokens e do cache; modelo, preço e cobrança efetiva.
- Tempo gasto em inferência, chamadas de ferramentas, testes, filas e coordenação.
- Se o limite de duas vezes significa duas correções após a execução inicial ou duas tentativas totais.
- Tamanho das Waves e proporção entre trabalho útil e custo fixo de inicialização.

**Não inferir arquitetura real a partir dos nomes exemplificativos deste documento.**

## 3. Self-check das recomendações anteriores

| Recomendação ou afirmação anterior | Correção adotada |
| --- | --- |
| A descoberta repetida é o vilão do consumo | É hipótese plausível, não causa comprovada. Investigar também histórico reenviado, regras automáticas, logs extensos, número de chamadas e granularidade das Waves. |
| A proporção de 223:1 demonstra desperdício | 58 milhões / 260 mil é aproximadamente 223:1, mas não existe limiar universal de eficiência nessa proporção. Ela não mede custo por entrega nem qualidade. |
| Muitos cache reads indicam releitura de arquivos | Cache de prompt e leitura por ferramentas são eventos distintos. Um arquivo lido uma vez pode permanecer no histórico enviado em muitas chamadas. |
| Contexto persistido evita pagar novamente pela leitura | Persistência evita reconstrução do conhecimento; o conteúdo ainda precisa entrar no contexto de um agente novo. Economia vem da seleção e da redução de chamadas, não da existência do arquivo. |
| A exploração deve ocorrer exatamente uma vez | Reutilizar a descoberta inicial enquanto válida. Permitir recuperação adicional diante de lacunas, mudanças ou contradições. |
| Fatos verificados dispensam validação | Evidências precisam de origem e revisão. Conclusões críticas, contestadas ou desatualizadas exigem revalidação proporcional ao risco. |
| Reviewer deve revisar exclusivamente o diff | O diff é ponto inicial. Revisão pode exigir métodos completos, consumidores, configuração, contratos e dependências não alteradas. |
| Segunda tentativa deve receber apenas o delta | Um agente novo precisa de base mínima suficiente mais delta. Apenas delta funciona quando a base permanece disponível e atual no contexto. |
| Arquivos sem findings não devem ser modificados | Evitar alterações alheias à correção, mas permitir investigar impactos conexos. Expansão de escrita segue a autorização vigente. |
| Tester e reviewer devem trabalhar em paralelo | Paralelismo depende de ausência de conflito e de uma revisão identificável. Testes em edição podem invalidar a revisão; sincronizar ou separar etapas. |
| Fontes citadas / fontes lidas mede utilização real | Citação não comprova uso cognitivo; ausência de citação não comprova inutilidade. Essa razão é, no máximo, sinal auxiliar, nunca gate de qualidade. |
| Poucas Waves permitem afirmar equivalência estatística | Um piloto pequeno fornece evidência preliminar. Não prova ausência de regressões nem equivalência estatística. |

**Conclusão do self-check:** preservar os três papéis no primeiro experimento; reduzir redescoberta e carregamento indiscriminado sem bloquear investigação necessária.

## 4. Objetivo e ganho esperado

### 4.1 Resultado principal

Reduzir **custo total por Wave aceita** e **tempo até aceitação**, mantendo os critérios de qualidade acordados.

O custo total inclui planejamento, preparação do contexto, agentes, ferramentas pertinentes, correções e retrabalho humano. Não considerar economia uma redução no developer que apenas transfere custo para o planner ou reviewer.

### 4.2 Ganhos esperados — a confirmar

| Ajuste | Mecanismo esperado | Evidência de benefício |
| --- | --- | --- |
| Reutilizar mapeamento já existente na Wave | Menos buscas para localizar as mesmas fontes | Menos buscas repetidas e menor tempo de descoberta |
| Selecionar contexto por papel | Menos material irrelevante carregado | Menor entrada acumulada por papel, sem omissão relevante |
| Referenciar skills aplicáveis | Menos seleção redundante e menos referências indevidas | Menos carregamentos desnecessários, mantendo conformidade |
| Handoff compacto com evidências | Menos reconstrução do que foi feito | Menos consultas de estado e menor coordenação |
| Base mínima mais delta na correção | Menos reinício da análise | Menor custo das correções, sem regressão |
| Saídas de ferramentas resumidas | Menos logs repetidos no contexto | Menor volume retornado, com falhas ainda diagnosticáveis |

Não há percentual de economia prometido. Se a maior parte do consumo for histórico cacheado e a latência estiver nos testes, restringir busca pode gerar pouco ganho. Medir antes de expandir a solução.

## 5. Mudança mínima: tornar o contexto existente executável

**Não criar um quarto agente nem uma nova família de documentos como pré-requisito.**

Se a Wave já contém objetivo, critérios, referências e estado, acrescente apenas os campos ausentes. O pacote pode ser uma seção da Wave ou uma projeção gerada dos artefatos existentes.

O orquestrador DEVE fornecer ao agente:

| Informação | Conteúdo mínimo |
| --- | --- |
| Identidade | Wave, tarefa, papel, tentativa e revisão atual |
| Missão | Resultado esperado para aquele papel e critérios de aceite aplicáveis |
| Restrições | Invariantes, limites de autonomia e condições de parada |
| Pontos de entrada | Arquivos e símbolos prioritários; fonte e seção das decisões relevantes |
| Leitura inicial | Fontes obrigatórias e motivo de aplicabilidade |
| Recuperação adicional | Fontes condicionais, gatilhos e fronteira de busca permitida |
| Escrita | Arquivos ou diretórios autorizados, separados do escopo de leitura |
| Skills | Skills requeridas, condicionais e respectivos gatilhos |
| Evidência anterior | Resultado, origem e revisão a que cada evidência se refere |
| Verificação | Checks a executar e resultado esperado; falhas preexistentes conhecidas |
| Saída | Formato compacto de handoff ou findings |

Um caminho para um arquivo não significa que seu conteúdo já foi fornecido. A delegação DEVE distinguir **conteúdo incluído**, **leitura necessária** e **consulta condicional**.

### 5.1 Evitar duplicação e desatualização

- Manter contratos, ADRs e requisitos em suas fontes canônicas.
- Usar resumos para orientação, não para substituir cláusulas normativas necessárias.
- Referenciar seção ou símbolo e revisão; números de linha isolados são frágeis.
- Associar evidências ao estado relevante: commit, revisão da Wave ou identificação equivalente do estado de trabalho.
- Se houver mudanças não commitadas, o commit-base sozinho NÃO identifica o código testado.
- Quando a fonte mudar, revalidar os fatos afetados; não reconstruir automaticamente todo o mapa.
- Mudanças em arquivos compartilhados de build, configuração ou dependências também podem invalidar evidências.
- Evidência sobre versão anterior não deve aparecer como validação da versão atual.

## 6. Contrato por papel

### 6.1 Desenvolvimento

**Missão:** implementar os critérios atribuídos à Wave dentro do escopo autorizado.

- Começar pelas fontes indicadas e pela implementação atual dos componentes afetados.
- Evitar descoberta geral quando os pontos de entrada já respondem às necessidades da tarefa.
- Consultar dependências quando necessárias para correção, segurança ou compatibilidade.
- Executar os checks atribuídos e registrar resultados reais, inclusive falhas.
- Entregar arquivos alterados, critérios atendidos, decisões aplicadas, pendências e evidências.
- Não declarar sucesso apenas porque o código foi produzido.

### 6.2 Testes

**Missão:** obter evidência comportamental independente a partir dos requisitos e riscos.

- Derivar cenários de critérios de aceite e contratos, não apenas do relato do developer.
- Usar diff e handoff para localizar alterações; consultar código e dependências quando necessário.
- Cobrir cenários negativos e regressões proporcionais ao risco.
- Registrar comando, resultado, revisão testada e limitações do ambiente.
- Distinguir teste não executado, falha preexistente, falha de ambiente e falha introduzida.
- No modo TDD, preservar a ordem RED/GREEN aprovada no fluxo real.

### 6.3 Review

**Missão:** julgar de forma independente a solução e seus impactos.

- Começar pelo diff, requisitos aplicáveis e evidências, sem tratar o handoff como prova de correção.
- Examinar contexto adjacente e dependências quando necessário; não limitar a análise às linhas alteradas.
- Procurar omissões de requisitos, incompatibilidades, regressões e riscos relevantes.
- Poder contestar o pacote, inclusive suas conclusões previamente classificadas como verificadas.
- Informar finding com severidade, evidência, impacto e critério violado quando houver.
- Distinguir defeito bloqueante de sugestão opcional; não inventar exigências normativas.

### 6.4 Orquestrador

**Missão:** manter estado, dependências, autorização e critérios de conclusão.

- Entregar contexto suficiente por papel sem reenviar todos os artefatos por padrão.
- Não refazer automaticamente implementação, testes e review apenas para consolidar resultados.
- Conferir completude e atualidade das evidências; escalar inconsistências.
- Preservar o limite real de correções e o gate humano.
- Registrar a semântica do contador de tentativas antes do piloto.
- Não transformar lacuna de contexto em licença para ampliar escopo de escrita.

## 7. Política de recuperação de contexto

**Delimitar a descoberta não significa impedir a investigação.**

1. **Leitura inicial:** consumir o núcleo obrigatório e os arquivos prioritários.
2. **Expansão local:** consultar dependências e fontes pertinentes dentro da fronteira de leitura aprovada.
3. **Expansão excepcional:** solicitar decisão do orquestrador quando a fronteira autorizada for insuficiente.
4. **Mudança de escopo:** cumprir o gate humano previsto no fluxo real antes de alterar requisitos, contratos ou áreas não autorizadas.

Para expansões significativas, registrar de forma breve: pergunta não respondida, fonte consultada, motivo e conclusão. Não gerar relatório extenso para cada leitura trivial.

O agente NÃO DEVE:

- Fazer buscas amplas apenas por hábito ou para “entender tudo”.
- Adivinhar comportamento para evitar ultrapassar uma meta de tokens.
- Ignorar uma contradição porque a informação estava marcada como verificada.
- Tratar uma lista de leitura inicial como uma proibição absoluta de consultar dependências.

Limites de tokens, leituras e buscas devem começar como alertas. Ao atingir um limite sem evidência suficiente, registrar bloqueio ou pedir extensão; nunca aprovar silenciosamente.

## 8. Handoff, correções e skills

### 8.1 Handoff mínimo

O resultado de cada etapa DEVE informar:

- Wave, papel, tentativa e revisão analisada.
- Arquivos alterados ou examinados relevantes.
- Critérios comprovados, não comprovados e não aplicáveis, com justificativa.
- Checks executados, resultados e ponteiros para evidências completas.
- Findings, hipóteses ainda abertas e impactos conhecidos.
- Expansões relevantes de contexto e divergências do plano.

Logs completos ficam disponíveis para diagnóstico. O contexto inicial recebe resumo de execução, falhas relevantes e localização dos logs, sem ocultar erros.

### 8.2 Correção: base mínima suficiente mais delta

Se um agente novo for criado, enviar:

1. Missão, restrições e critérios ainda vigentes.
2. Identificação do estado atual e referências essenciais.
3. Findings e falhas reproduzíveis a corrigir.
4. Mudanças desde a tentativa anterior.
5. Partes aprovadas a preservar quando não impactadas.
6. Checks de correção e regressão necessários.

Não reabrir decisões sem motivo; também não impedir correções conexas necessárias. Após editar código, reavaliar quais aprovações e resultados de testes foram invalidados.

Retomada de sessão, se disponível e autorizada, pode ser comparada com um agente novo. Não pressupor que manter uma sessão sempre custa menos: o histórico também pode crescer.

### 8.3 Seleção antecipada de skills

O plano pode indicar skills requeridas e condicionais, com motivo e gatilho. Isso é uma boa hipótese de otimização, mas não garante carregamento correto por si só.

- Usar metadados para seleção quando suficientes; abrir detalhes quando necessários para verificar aplicabilidade.
- O executor carrega as instruções da skill selecionada e suas referências obrigatórias aplicáveis.
- Não copiar o conteúdo de todas as skills para o pacote.
- Seleção planejada não substitui regras corporativas obrigatórias.
- Skill inicialmente não aplicável pode tornar-se necessária; revisar a seleção diante de evidência nova.
- Antes de alterar configuração do Cursor, confirmar campos suportados e comportamento na versão efetivamente instalada. Este documento não prescreve campos de configuração não testados.

## 9. Sequenciamento e preservação da qualidade

Não há evidência de que os três agentes atualmente rodem juntos. Verificar antes de mudar a ordem.

- No fluxo sem TDD, testes podem ser planejados antes da implementação; execução e revisão da solução dependem de um estado identificável.
- No fluxo com TDD, manter testes RED antes da implementação quando isso fizer parte do plano aprovado.
- Se tester altera arquivos enquanto reviewer analisa a mesma árvore, coordenar snapshots ou sequenciar as etapas.
- Paralelismo pode reduzir tempo de parede, mas não necessariamente tokens ou custo total.
- Manter os três papéis e o modelo atual no primeiro piloto ajuda a isolar o efeito da mudança de contexto.
- Não reduzir testes, retirar review nem trocar simultaneamente para um modelo mais barato para demonstrar economia.

Se, após a otimização de contexto, o custo fixo continuar dominante, avaliar a granularidade das Waves. Agrupamento só faz sentido quando preserva critérios próprios, dependências, governança e capacidade de localizar falhas; não é a primeira alteração proposta.

## 10. Medição e piloto

### 10.1 Medir mecanismos diferentes separadamente

| Métrica | Uso e cuidado |
| --- | --- |
| Custo total por Wave aceita | Indicador principal; incluir preparação, correções e execuções abandonadas no conjunto avaliado |
| Tempo até aceitação | Separar tempo ativo, testes, espera de ferramentas e gate humano |
| Entrada e cache | Confirmar se cache é subconjunto da entrada ou categoria separada; não somar duas vezes |
| Chamadas ao modelo | Muitas chamadas podem reprocessar histórico mesmo sem novas leituras |
| Leituras e buscas por papel | Distinguir descoberta repetida de verificação independente necessária |
| Saída de ferramentas | Medir volume de logs, buscas e arquivos retornados |
| Aprovação e retrabalho | Acompanhar correções, defeitos escapados e intervenção humana |
| Custo do próprio pacote | Incluir criação, atualização e validação do contexto na comparação |

Não pedir ao modelo para declarar quantos tokens realmente utilizou. Preferir telemetria disponível; rotular estimativas quando contadores exatos não existirem.

Cache alto pode significar reaproveitamento eficiente, e não desperdício. Avaliar custo efetivo e chamadas junto aos contadores. Não definir uma meta de proporção entrada/saída.

### 10.2 Experimento mínimo

1. Selecionar uma Wave representativa e registrar o fluxo atual, sem código confidencial fora do ambiente.
2. Levantar quais informações já existem e observar leituras, chamadas e tempos por papel.
3. Acrescentar somente seleção por papel, leitura inicial explícita e handoff compacto onde faltarem.
4. Manter critérios de qualidade, modelo e estratégia de testes comparáveis.
5. Nas correções, usar base mínima mais delta.
6. Comparar com execuções de tarefas equivalentes ou replays controlados, sem entregar ao segundo método a solução do primeiro.
7. Registrar variáveis que impedem comparação direta: complexidade, cache aquecido, modelo, ambiente e duração de testes.
8. Ampliar gradualmente a amostra; um resultado isolado não comprova generalização.

Fórmula descritiva para um conjunto comparável:

`redução de custo (%) = 100 × (custo_base − custo_piloto) / custo_base`

Aplicar apenas quando custo_base for maior que zero. Para tempo, usar a mesma lógica e declarar o intervalo medido. Exibir valores absolutos além dos percentuais.

### 10.3 Critérios de adoção e rollback

Antes do piloto, o responsável deve definir metas de custo/tempo e tolerâncias de qualidade. Não inventar limiares universais.

Adotar quando houver ganho líquido e evidência suficiente de preservação dos requisitos, da revisão e dos testes acordados. Se surgirem omissões associadas ao contexto reduzido, restaurar as fontes necessárias e revisar a seleção.

Zero defeitos críticos observados é condição desejável, não prova de ausência de defeitos. Declarar o tamanho da amostra e as limitações.

## 11. Resultado esperado da IA no ambiente real

A IA que aplicar este documento deve entregar, antes de uma alteração ampla:

1. **Diagnóstico:** comportamento observado, evidências e hipóteses ainda abertas.
2. **Mapa de reaproveitamento:** quais artefatos atuais já cobrem o pacote proposto.
3. **Mudança mínima:** instruções e campos a ajustar, sem duplicar fontes.
4. **Riscos:** informações que não podem ser removidas e situações de expansão.
5. **Plano de piloto:** baseline, métricas, qualidade, autorização e rollback.
6. **Após execução autorizada:** resultados reais, ganhos líquidos, perdas e limitações.

**Síntese:** o ganho procurado é evitar redescoberta desnecessária e excesso de contexto, não eliminar leitura, independência ou validação.

## 12. Registro de revisão deste documento

- Origem: duas respostas anteriores e relatos do usuário nesta conversa; sem acesso ao fluxo real.
- Método: self-check de causalidade, suficiência do contexto, independência de revisão, invalidação de evidências e mensuração.
- Correções rastreáveis: registradas na seção 3 e incorporadas às seções operacionais.
- Natureza: proposta consultiva para diagnóstico e piloto, não política corporativa nem especificação executável.
- Organização: objetivo e limitações primeiro; instruções operacionais no meio; medição e checklist ao final.
- Revisão independente por outro modelo: não realizada.
- Execução no Cursor e ganho real: não verificados.
- Validação formal pelo validador da skill de curadoria: não executada; referências obrigatórias da skill indisponíveis.
- Roteamento automático por frontmatter: não utilizado nem verificado; este arquivo é um documento de orientação.

## 13. Checklist de validação no ambiente real

### Diagnóstico e escopo

- [ ] O fluxo real foi inspecionado sem presumir que o relato aproximado é completo.
- [ ] A ordem dos agentes, o modo TDD e o contador de tentativas foram confirmados.
- [ ] As políticas corporativas e a autorização para mudanças foram respeitadas.
- [ ] Cache reads foram distinguidos de leituras de arquivos por ferramentas.
- [ ] A semântica dos contadores foi confirmada, evitando dupla contagem.
- [ ] O custo e o tempo foram decompostos antes de atribuir a causa aos três agentes.

### Contexto e recuperação

- [ ] Os artefatos existentes foram reaproveitados antes de criar novos documentos.
- [ ] Cada papel recebe missão, critérios, restrições e contexto inicial suficientes.
- [ ] Conteúdo incluído, leitura obrigatória e consulta condicional estão separados.
- [ ] O escopo de leitura é distinto do escopo de escrita.
- [ ] As fontes possuem referências e identificação de revisão suficientes.
- [ ] Alterações não commitadas são consideradas na identificação do estado.
- [ ] Skills requeridas e condicionais possuem motivo e gatilhos claros.
- [ ] O agente pode expandir contexto diante de lacuna, risco ou contradição.
- [ ] Limites de consumo não induzem adivinhação ou aprovação sem evidência.

### Qualidade e correções

- [ ] Testes derivam dos requisitos, não apenas do relato de implementação.
- [ ] O reviewer pode contestar o pacote e examinar código não alterado relevante.
- [ ] Resultados de testes e review apontam para o estado efetivamente analisado.
- [ ] Paralelismo não causa conflito de arquivos ou evidências desatualizadas.
- [ ] Agentes novos de correção recebem base mínima suficiente mais delta.
- [ ] Aprovações impactadas por correções são reavaliadas.
- [ ] Limites de correção e gate humano foram preservados.

### Ganho e decisão

- [ ] A baseline inclui planejamento, contexto, agentes, correções e retrabalho.
- [ ] Modelo, critérios e estratégia de testes foram mantidos comparáveis no piloto.
- [ ] Metas e tolerâncias foram definidas antes de avaliar o resultado.
- [ ] Custo e tempo por entrega aceita foram comparados com valores absolutos.
- [ ] O ganho não foi obtido pela retirada de validações necessárias.
- [ ] O tamanho da amostra e as limitações foram declarados.
- [ ] Existe rollback caso o contexto reduzido provoque omissões.
- [ ] A adoção foi baseada em ganho líquido observado, não em economia presumida.
