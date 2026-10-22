# Plano incremental de curadoria e pesquisa em fontes autorizadas

**Versão 2.0 — 21/10/2026**  
**Estado:** proposta para refinamento com o time; implementação não iniciada.  
**Objetivo:** entregar valor utilizável e mensurável desde o primeiro incremento, com itens candidatos a até 8 pontos, evoluindo até uma operação enterprise.

> Organizar entregas pelo benefício disponível ao investidor ou à operação de curadoria. Cada incremento contém o mínimo de catálogo, implementação, segurança, avaliação e operação necessário ao seu próprio escopo.
>
> Começar a curadoria com um fluxo assistido por IA: propostas fundamentadas, validação e publicação controlada. Introduzir manutenção recorrente acionada por mudança, lacuna e risco, sem executar um agente completo sobre todos os sites a cada pergunta.

## Leitura rápida

- **Primeira atividade sugerida:** I01 — catálogo pequeno, usado pela curadoria real, com classificação assistida por IA e medição de tempo/correções.
- **Primeiro benefício direto ao investidor:** I02 — indicação de fontes adequadas no chat.
- **Primeira explicação fundamentada:** I03 — respostas sobre um tema, usando conteúdo aprovado e versionado.
- **Primeira consulta web automática:** I04 — uma fonte HTML consultada com controles de saída.
- **Manutenção recorrente:** I05 — detectar mudanças e reclassificar/revisar os perfis afetados.
- **Expansão:** lotes pequenos e capacidades escolhidas por demanda e métricas.
- **8 pontos:** limite pretendido a validar com o time; não significa dias nem garantia de cabimento em uma sprint.

## Sumário

1. [Mudança de planejamento](#1-mudança-de-planejamento)
2. [Curadoria com IA](#2-curadoria-com-ia)
3. [Recorte em atividades de até 8 pontos](#3-recorte-em-atividades-de-até-8-pontos)
4. [Roadmap incremental](#4-roadmap-incremental)
5. [Fichas dos incrementos](#5-fichas-dos-incrementos)
6. [Metadados e arquitetura evolutiva](#6-metadados-e-arquitetura-evolutiva)
7. [Tarefas atômicas e estados](#7-tarefas-atômicas-e-estados)
8. [Métricas e DoD](#8-métricas-e-dod)
9. [Migração do backlog anterior](#9-migração-do-backlog-anterior)
10. [Self-check e limites](#10-self-check-e-limites)
11. [Fundamentação auditável](#11-fundamentação-auditável)
12. [Checklist do próximo refinamento](#12-checklist-do-próximo-refinamento)

## 1. Mudança de planejamento

### 1.1 O que esta versão substitui

A versão anterior descrevia uma arquitetura-alvo abrangente e um grafo técnico T01–T41, com gates G0–G4. A sequência concentrava descoberta, contratos, persistência, coleta e roteamento antes da disponibilização de respostas.

Esta versão substitui aquele grafo e aqueles gates como **autoridade de execução**. Os conceitos de catálogo, política, evidência, temporalidade e auditoria continuam válidos. A seção 9 mapeia os temas anteriores para as entregas atuais.

A unidade de planejamento passa a ser um resultado utilizável em um escopo pequeno: tema, fonte/seção, modalidade de conteúdo, classe de pergunta ou cenário operacional.

Não será necessário classificar os 313 sites, construir todos os conectores ou escolher um banco vetorial antes do primeiro valor.

### 1.2 Valor de negócio desde o primeiro incremento

| Beneficiário | Valor observável | Primeiro incremento |
|---|---|---|
| Operação de curadoria | Menos esforço para transformar nome/URL em perfil revisável e reutilizável | I01 |
| Investidor | Encontrar fontes específicas adequadas ao assunto | I02 |
| Investidor | Receber explicação apoiada em conteúdo aprovado | I03 |
| Investidor | Consultar conteúdo web revalidado no atendimento | I04 |

I01 tem valor operacional. Não é uma resposta web ao investidor. Para cumprir a regra de valor, o Product Owner precisa aceitar esse beneficiário e o catálogo deve ser usado no processo real. Um protótipo descartável ou documento sem uso não satisfaz o incremento.

Se a primeira entrega tiver de responder ao investidor pela web, o time precisa demonstrar que as capacidades necessárias já existem e recortar uma pergunta/fonte sobre elas. Sem essa reutilização, não há justificativa para prometer todo o caminho em 8 pontos.

### 1.3 Qualidade enterprise com escopo pequeno

A cobertura pode ser limitada. Os controles correspondentes à exposição não são opcionais:

- Antes de coletar automaticamente, controlar a saída de rede.
- Antes de afirmar fatos, ter evidência e validade adequadas.
- Antes de usar uma fonte, conferir aprovação e suspensão.
- Antes de transmitir fatos no NDJSON, validar o resultado.
- Antes de manter conteúdo, definir direitos e retenção.

A evolução amplia cobertura, eficiência, disponibilidade e automação. Não depende de entregar uma primeira versão insegura para “endurecer” no final.

### 1.4 Insumos ainda ausentes

Não foram disponibilizados a lista dos 313 sites, a análise da outra IA, contratos do chat, volume, orçamento ou capacidades de rede/armazenamento efetivamente existentes.

O plano não classifica os sites nem certifica conformidade com padrões internos da B3. Define entregas e evidências para demonstrar adequação no escopo liberado.

A análise externa será reconciliada quando disponível. Sua ausência não impede um primeiro lote que já tenha material e autorização suficientes.

## 2. Curadoria com IA

### 2.1 Justificativa técnica

É razoável experimentar LLM para propor resumos, temas, exclusões e diferenças semânticas em textos heterogêneos. A tarefa tem partes de interpretação de linguagem, mas também partes determinísticas e decisões de autoridade.

R03 distingue workflows de agentes que escolhem suas ações dinamicamente. A escolha proposta é começar com um fluxo previsível. R04 fundamenta supervisão e monitoramento; não prova que uma LLM específica classificará corretamente estes sites.

O número 313 não demonstra, isoladamente, a necessidade de um agente autônomo. O esforço depende de seções por site, diversidade de templates, taxa de mudança e criticidade.

A justificativa auditável será:

1. Medir esforço e erros do processo manual.
2. Automatizar uma parte delimitada.
3. Medir preparação, revisão, correção, publicação e custo.
4. Manter IA onde há ganho líquido com qualidade aceitável.
5. Ampliar autonomia somente mediante evidências adicionais.

### 2.2 Responsabilidades

| Trabalho | Mecanismo inicial | Autoridade da IA |
|---|---|---|
| Validar URL, duplicidade e campos obrigatórios | Código | Nenhuma |
| Obter amostra autorizada | Processo existente ou coletor limitado | Não amplia destinos |
| Identificar temas/tarefas cobertos | LLM com taxonomia e evidências | Propõe |
| Resumir seção e apontar exclusões | LLM | Propõe com suporte |
| Detectar mudança de bytes | Hash/HTTP condicional | Nenhuma |
| Avaliar impacto semântico da mudança | Regras e LLM quando necessário | Propõe impacto |
| Validar contrato e referências | Schema e regras do backend | Não sobrepõe a validação |
| Aprovar domínio, identidade, direitos e autoridade | Responsável habilitado | Não aprova |
| Publicar classificação | Fluxo autenticado e auditado | Sem publicação autônoma inicial |
| Suspender ou bloquear por vencimento | Política determinística | Não remove bloqueio |
| Priorizar revisão | Regras por risco; modelo opcional | Recomenda prioridade |

Não é necessário iniciar vários agentes para cada fonte. Um job pode coletar, chamar o modelo, validar a proposta e encaminhar revisão, com estado observável.

### 2.3 Fluxo proposto

~~~mermaid
flowchart TD
  A["Fonte, mudança ou revisão vencida"] --> B["Verificar política e obter amostra"]
  B --> C{"Há mudança relevante ou lacuna?"}
  C -->|Não| D["Registrar verificação e prazo de revisão"]
  C -->|Sim| E["IA propõe metadados e diferenças"]
  E --> F["Validar contrato e evidências"]
  F --> G["Revisor aceita ou rejeita"]
  G --> H["Publicar versão aprovada"]
~~~

Inicialmente, só metadados operacionais autorizados, como instante de verificação bem-sucedida, podem ser atualizados automaticamente. Temas, exclusões, identidade, autoridade e permissões permanecem sob aprovação.

Conteúdo externo é dado não confiável: uma página não pode instruir o curador a aprovar um domínio, alterar política ou executar comandos.

### 2.4 Quando executar

Combinar periodicidade e eventos:

- Verificação técnica das fontes ativas.
- Reclassificação quando mudar conteúdo relevante da amostra.
- Revisão por erro de roteamento, reclamação ou lacuna.
- Revisão humana ao vencer o prazo, mesmo sem mudança detectada.
- Avaliação imediata de domínio, publicador, direitos ou identidade alterados.
- Auditoria amostral de itens considerados inalterados.

Não executar a LLM sobre todos os sites a cada pergunta ou disparo do agendador.

ETag, Last-Modified e hash ajudam a detectar mudança da representação. Não comprovam cobertura completa, vigência regulatória ou licença. Um HTTP 304 não estende automaticamente a validade de uma conclusão.

A amostra precisa de descoberta periódica de novas seções dentro do escopo permitido: verificar apenas as mesmas páginas pode deixar de perceber uma seção nova.

### 2.5 Como medir a utilidade

**Tempo assistido = preparar amostra + executar/importar IA + revisar + corrigir + publicar.**

**Economia de tempo = 1 − tempo assistido / tempo manual comparável.**

**Custo líquido = revisão + inferência + coleta + operação + retrabalho.**

Medir também:

- Campos aceitos sem correção e correções materiais.
- Cobertura proposta sem evidência.
- Erros que passaram pela revisão.
- Tempo para tratar mudança relevante.
- Tamanho/idade da fila de revisão.
- Percentual de fontes ativas com revisão válida.

Comparar amostras equivalentes em complexidade, alternar a ordem e reduzir o efeito de memorização pelo revisor. Lote pequeno gera sinal inicial; não prova estatística definitiva.

**Hipótese para I01:** testar redução de pelo menos 20% no tempo total mediano sem aumento observado de erro material. Não é ganho prometido nem benchmark externo.

Se a hipótese falhar, registrar o resultado, manter o fluxo seguro e decidir se ajusta ou interrompe a expansão da automação. Não declarar ganho com base apenas na velocidade de geração da LLM.

### 2.6 Contrato da proposta curatorial

~~~json
{
  "schema_version": "1.0",
  "source_id": "src-001",
  "section_id": "sec-001",
  "base_profile_version": 1,
  "run_id": "curation-run-001",
  "proposed_changes": [
    {
      "field": "topic_ids",
      "operation": "add",
      "value": "investimentos.renda_fixa",
      "evidence_ids": ["ev-perfil-001"],
      "reason_code": "EXPLICIT_COVERAGE"
    }
  ],
  "unknowns": ["historical_coverage"],
  "risk_flags": [],
  "model_version": "modelo-configurado-pelo-backend",
  "prompt_version": "curador-v1",
  "status": "pending_review"
}
~~~

Exemplo ilustrativo. A evidência deve existir na amostra versionada. Campo desconhecido permanece unknown. Score autodeclarado pelo modelo não equivale a probabilidade calibrada.

A versão base evita sobrescrever uma revisão humana com proposta calculada sobre perfil antigo.

## 3. Recorte em atividades de até 8 pontos

### 3.1 Estimativa

Pontos são relativos ao time e consideram esforço, complexidade e risco [R02]. Não equivalem a duração universal.

Cada incremento deste plano é **candidato a até 8 pontos**, sujeito a refinamento. A estimativa inclui implementação, testes, revisão, implantação e dependências.

Não atribuir 8 a todos automaticamente, converter pontos em dias ou somar os itens para prometer uma data. A sprint pode conter mais de um incremento, conforme capacidade.

### 3.2 Premissas de reutilização

| Capacidade | Situação | Consequência |
|---|---|---|
| Chat A2UI/NDJSON | Informado pelo usuário | Reutilizar contrato e interface atuais |
| Acesso à LLM para esta demanda | Confirmar | I01 não fica ready sem acesso autorizado |
| Persistência/revisão/autenticação existentes | Não demonstradas | Reutilizar recursos corporativos; não presumir uma plataforma nova em 8 pontos |
| Coletor com saída restrita | Não demonstrado | I04 exige refinamento dessa capacidade |
| Aprovador de conteúdo/fontes | Confirmar | Necessário antes de publicar o lote |
| Implantação e observabilidade | Confirmar | Incorporar o mínimo ao escopo e à estimativa |

Se for necessária habilitação extensa de infraestrutura, registrá-la como trabalho habilitador e dependência. Não disfarçar “criar infraestrutura” como benefício já disponível ao investidor.

O item de produto fica bloqueado, ou usa um caminho que reutilize recursos demonstrados. Segurança não é retirada para preservar a pontuação.

### 3.3 Cortes válidos

- Um tema ou subtema.
- Uma fonte/seção e um template.
- Uma classe de pergunta.
- Um tipo temporal: conceito estável, regra ou notícia.
- Uma modalidade: HTML, PDF textual ou OCR.
- Um pequeno lote homogêneo.
- Um gargalo ou incidente específico.

“SÓ banco”, “SÓ embeddings” e “toda a curadoria enterprise” são componentes ou épicos. O incremento precisa permitir uso e aceite.

Se o time estimar 13 pontos, aplicar o corte descrito na ficha e reestimar. Se o corte não preservar valor e DoD, o item exige novo refinamento.

### 3.4 Atividade atual de pavimentação

A atividade de planejamento pode encerrar com:

- Roadmap priorizado.
- I01 com tema, lote, responsáveis, aceite e medição.
- Dependências verificadas.
- Estimativa do time e cortes alternativos.

Isso entrega prontidão e redução de incerteza. O primeiro incremento de produto continua sendo I01: documento aprovado não significa catálogo implementado.

## 4. Roadmap incremental

Todos os itens começam em **proposed**. Quantidades são recortes iniciais; tamanho precisa ser estimado pelo time.

| ID | Entrega utilizável | Valor principal | Dependências |
|---|---|---|---|
| I01 | Catálogo pequeno com curadoria assistida por IA | Menos esforço e retrabalho na classificação | DoR e acessos resolvidos |
| I02 | Indicação de fontes no chat | Encontrar fonte adequada | I01 |
| I03 | Resposta fundamentada sobre um tema | Perguntas atendidas com evidência | I02 |
| I04 | Consulta web a uma fonte HTML | Conteúdo revalidado no atendimento | I03 e cliente seguro |
| I05 | Revalidação recorrente de um lote | Menor esforço de manutenção | I04 |
| I06 | Novo tema/lote de fontes habilitado | Mais perguntas prioritárias atendidas | I03; I04/I05 conforme modalidade/validade |
| I07 | Melhoria lexical de uma classe de falhas | Menos erros com termos/aliases | I02 e erros rotulados |
| I08 | Melhoria semântica quando comprovada | Menos erros em paráfrases | I07 e lacuna demonstrada |
| I09 | Uma família de regras com vigência | Acerto temporal | I04 e fonte oficial habilitada |
| I10 | Eventos recentes de um tema | Recência e atraso conhecidos | I04 e canal autorizado |
| I11 | Uma classe de pergunta com múltiplas facetas | Cobrir todas as partes necessárias | I03 e fontes/capacidades necessárias |
| I12 | Uma modalidade adicional | Atender perguntas antes indisponíveis | I04 e autorização específica |
| I13 | Custo ou latência melhorados em uma rota | Sustentabilidade/experiência | I03 e gargalo medido |
| I14 | Continuidade em um cenário de incidente | Menor interrupção/recuperação | I04 e recursos do cenário |

I06, I12, I13 e I14 são modelos repetíveis. Cada instância tem ID, escopo e dependências concretos, como I06-renda-variavel-01 ou I14-origem-indisponivel-01.

Não há uma atividade única “expandir para 313 fontes”. I08 é opcional; vetor não é requisito de maturidade enterprise.

**Ordem sugerida:** I01 → I02 → I03 → I04. Depois priorizar I05, lotes I06 e continuidade I14 segundo risco/demanda. I07/I08 entram por erros observados; I09–I12 por novos casos de uso; I13 por gargalos.

São tipos de entrega, não 14 sprints contratadas.

## 5. Fichas dos incrementos

### I01 — Curadoria assistida utilizável

**História:** como curador, quero propostas fundamentadas de classificação para aprovar perfis mais rapidamente e disponibilizar um catálogo reutilizável.

**Requisito R-I01:** transformar um lote de nomes/URLs e materiais aprovados em perfis revisados e versionados.

**Escopo candidato:** até 5 fontes de um tema; até 2 documentos/seções representativos por fonte. Perfil parcial não representa cobertura completa do domínio.

**Implementação mínima:** usar extratos/snapshots obtidos pelo processo autorizado e fornecidos ao fluxo. A IA propõe temas, resumo, exclusões e unknown. Revisor publica usando mecanismo existente. CLI/exportação estruturada basta se for utilizável pela operação. Não construir scraping, nova UI, agendador ou vetor.

**Valor:** a operação usa o catálogo para classificar o lote real e o disponibiliza ao incremento seguinte.

**DoR:** amostra/retencão autorizadas, LLM acessível, revisor, taxonomia mínima e mecanismo corporativo de registro/revisão.

**Aceite:**

- Origem, IDs e contagem reconciliados.
- Propostas têm evidência ou unknown.
- IA não aprova domínio, direitos ou autoridade.
- Perfil pendente não aparece como ativo.
- Revisão e versão são registradas.
- Catálogo pode ser exportado/importado sem perder identidade.
- Instrução maliciosa em extrato não altera a autoridade do processo.
- Tempo, custo e correções medidos; uso operacional demonstrado.

**Métrica:** tempo total mediano por perfil, correção material e custo. Testar a hipótese de economia da seção 2.5.

**Dependência:** nenhuma de produto; DoR obrigatório.

**Corte se exceder 8:** duas fontes ou um tipo de seção, mantendo evidência, revisão, uso e medição.

### I02 — Indicação de fontes no chat

**História:** como investidor, quero descobrir quais fontes aprovadas tratam da minha pergunta.

**Requisito R-I02:** selecionar perfis ativos de um tema e apresentar links com descrição correta de cobertura.

**Escopo candidato:** um tema; regras, termos e aliases; interface atual. Sem navegação ou resposta factual baseada em documento não lido.

**Valor:** localizar fontes específicas sem pesquisa genérica.

**Aceite:**

- Até 3 fontes/seções elegíveis, com descrição derivada do perfil.
- Declara que se trata de indicação; não afirma consulta ao vivo.
- Ausência de cobertura e ambiguidade têm retorno definido.
- Suspensão manual impede seleção; backend confere política.
- Links são sanitizados/validados.
- Meta local: ao menos 18 de 20 perguntas respondíveis rotuladas têm fonte aceitável no top-3.
- Casos negativos/ambíguos avaliados separadamente.
- Mecanismo de feedback de utilidade disponível.

**Métrica:** Hit@3, recusa indevida, latência e utilidade. A amostra pequena não representa taxa global.

**Dependência:** I01.

**Corte:** uma classe de pergunta e apresentação simples de links.

### I03 — Resposta fundamentada sobre um tema

**História:** como investidor, quero explicação direta com as evidências usadas.

**Requisito R-I03:** responder a partir de pequena base autorizada, versionada e com validade definida.

**Escopo candidato:** uma fonte/seção, até 10 documentos e 20 perguntas conceituais. Usar snapshots aprovados; busca simples em documentos conhecidos. Sem web ao vivo.

**Valor:** primeira resposta explicativa completa para um caso real.

**Aceite:**

- Afirmações factuais materiais apontam para trecho da versão usada.
- Fonte, documento, localizador, coleta e validade registrados.
- Base vencida não sustenta afirmação de atualidade.
- Resposta distingue sucesso, parcial, esclarecimento e insuficiência.
- Números preservam unidade/período.
- Citação existe e seu suporte semântico foi revisado.
- Nenhum erro material aceito no conjunto pequeno de liberação.
- NDJSON transmite fatos após validação; usar buffer se necessário.
- Um caso pode ser reconstruído por IDs/versões.
- Suspensão é reconferida antes da liberação.

**Métrica:** respostas aceitas por especialista, precisão de citação, tempo e custo.

**Dependência:** I02.

**Corte:** subtema, 3–5 documentos e formato único de resposta; manter cobertura do conjunto de perguntas acordado.

### I04 — Consulta web a uma fonte HTML

**História:** como investidor, quero resposta baseada na página atual de uma fonte aprovada.

**Requisito R-I04:** recuperar/revalidar HTML sem sair da política autorizada.

**Escopo candidato:** caminhos e páginas pré-selecionados; HTML estático; sem crawl aberto, JavaScript, PDF ou busca global.

**Valor:** substituir a dependência de importação manual pela consulta revalidada no caso escolhido.

**Aceite:**

- Controlar esquema, host, porta, path, IP e cada redirect.
- Impedir redes internas/indevidas e troca de destino entre validação e conexão.
- Conferir TLS, robots e uso permitido.
- Timeout, cancelamento, orçamento e bytes limitados.
- Extração preserva o trecho necessário; falha não produz afirmação inventada.
- Versão e coleta registradas.
- Mudança na fonte de teste aparece conforme política.
- Suspensão impede consulta e uso por cache.
- Falha de origem retorna limitação controlada.
- Testes de destinos maliciosos e injeção indireta executados para o recorte.

**Métrica:** evidência útil obtida no prazo, sucesso de extração, latência e custo.

**Dependência:** I03 e controle de saída disponível.

**Corte:** uma URL fixa e uma classe de pergunta. Se construir o cliente seguro do zero ultrapassar o tamanho, refinar a dependência explicitamente; não usar cliente irrestrito temporário.

### I05 — Curadoria recorrente por mudança

**História:** como curador, quero revisar mudanças relevantes sem reler manualmente todas as fontes.

**Requisito R-I05:** verificar um lote, comparar versões e propor alterações fundamentadas quando o perfil puder mudar.

**Escopo candidato:** lote já consultável; uma periodicidade; fila de revisão existente; publicação humana.

**Valor:** menos manutenção manual e menor tempo de catálogo desatualizado.

**Aceite:**

- Agendamento, chave idempotente e histórico.
- Distinguir alteração técnica/editorial/possível cobertura.
- Não chamar reclassificação por IA sem motivo registrado.
- Inalterado não elimina revisão humana vencida.
- Proposta mostra diferença, evidência e versão base.
- Revisão concorrente não é sobrescrita.
- Risco/vencimento limita ou bloqueia conforme política.
- Testar mudança material, cosmética e falha de origem.
- Ciclo termina publicado, rejeitado ou pendente com responsável.

**Métrica:** minutos de revisão por ciclo, custo/chamadas por mudança útil, atraso e erros de detecção.

**Dependência:** I04.

**Corte:** uma fonte e uma classe de mudança. Publicação autônoma de semântica fica fora.

### I06 — Novo tema ou lote habilitado

**História:** como investidor, quero respostas para outro grupo de perguntas relevantes.

**Requisito R-I06:** ampliar cobertura sem reduzir autorização, evidência e validade.

**Escopo por instância:** um tema ou 2–5 fontes de capacidade já suportada, ajustado à heterogeneidade.

**Valor:** novas perguntas efetivamente atendidas; quantidade de URLs não é o benefício.

**Aceite:**

- Perfis fundamentados e aprovados.
- Endpoints/direitos habilitados.
- Perguntas novas rotuladas, com alternativas aceitáveis.
- Respostas no chat atendem aos controles existentes.
- Regressão dos casos essenciais anteriores.
- Fontes pendentes permanecem desativadas.
- Validade sustentada por atualização manual ou automática demonstrável.

**Métrica:** perguntas prioritárias adicionais atendidas e taxa de aceite.

**Dependências:** I03; I04 se ao vivo; I05 se a validade exigir manutenção automática. Sem I05, comprovar processo manual e prazo.

**Corte:** uma fonte/subtema. Fonte com conector novo precisa da instância aplicável de I12.

### I07 — Melhoria lexical nos erros observados

**História:** como investidor, quero que termos usuais e aliases levem à fonte certa.

**Requisito R-I07:** corrigir uma classe demonstrada de falhas com lexical/aliases governados.

**Escopo candidato:** uma classe de erro, um idioma, fontes já ativas.

**Aceite:**

- Baseline e erros registrados.
- Comparação com versão anterior em validação separada dos ajustes.
- Autorização mantida.
- Ganho no grupo-alvo sem regressão material acordada.
- Comportamento melhorado disponível ao usuário.

**Métrica:** Hit@k, recusa indevida, latência e custo.

**Dependência:** I02 e casos suficientes para avaliar o problema.

**Corte:** aliases de um produto ou uma classe de pergunta. Não embutir motor de busca de documentos inteiro.

### I08 — Melhoria semântica quando justificada

**História:** como investidor, quero encontrar a fonte correta usando paráfrases.

**Requisito R-I08:** adicionar similaridade semântica somente com ganho e custo aceitáveis.

**Escopo candidato:** embeddings de perfis de um tema e fusão lexical/vetorial. Catálogo pequeno pode usar comparação exata de vetores.

**Aceite:**

- Lacuna em paráfrases demonstrada.
- Texto, modelo/dimensão e índice versionados.
- Política e revalidação no backend mantidas.
- Não somar scores incompatíveis.
- Comparar qualidade, custo, latência e manutenção.
- Feature flag e retorno ao baseline.
- Sem ganho, não promover a variante e registrar decisão.

**Métrica:** acerto adicional em paráfrases e custo por acerto adicional.

**Dependência:** I07 e lacuna demonstrada.

**Corte:** um tema e uma fusão, sem reranker adicional.

**Valor condicionado:** experimento sem ganho entrega redução de incerteza, não melhoria ao investidor. Se toda atividade precisar obrigatoriamente de ganho direto já entregue, fazer avaliação pequena no refinamento e criar I08 apenas quando houver evidência para implementação.

### I09 — Uma família de regras com vigência

**História:** como investidor, quero saber qual regra vale para meu produto/período.

**Requisito R-I09:** vincular resposta a documento oficial aplicável.

**Escopo candidato:** uma família de regras e fonte responsável; sem recomendação personalizada.

**Aceite:**

- Publicação, vigência, coleta e referência separadas.
- Documento substituído e pergunta histórica tratados.
- Vigência desconhecida impede conclusão crítica afirmativa.
- Divergências/limites expostos.
- Especialista revisa casos atuais, históricos e ambíguos.
- Mudança documental pode suspender respostas afetadas.

**Métrica:** acerto temporal e erros materiais no conjunto crítico.

**Dependências:** I04, fonte habilitada e modalidade necessária; incluir I06/I12 aplicáveis.

**Corte:** um procedimento ou pequeno conjunto documental; não toda a regulamentação.

### I10 — Eventos recentes de um tema

**História:** como investidor, quero acompanhar eventos recentes com fontes e datas claras.

**Requisito R-I10:** usar canal autorizado e expor recência/atraso.

**Escopo candidato:** um tema, um feed/API/seção acessível e uma classe de pergunta.

**Aceite:**

- Distinguir publicação, atualização, evento e coleta.
- Definir atraso tolerado.
- Não apresentar notícia antiga como evento novo.
- Correções/republicações tratadas.
- Falta de atualização gera limitação.
- Uso/redistribuição autorizados.
- Resposta citada e recência medida.

**Métrica:** atraso, adequação temporal e custo.

**Dependências:** I04 e canal habilitado; novo conector pode exigir I12.

**Corte:** um tipo de notícia/fonte. Cotação em tempo real e séries licenciadas exigem escopo e contrato próprios.

### I11 — Perguntas com múltiplas facetas

**História:** como investidor, quero que uma comparação cubra todas as partes necessárias.

**Requisito R-I11:** decompor uma classe de pergunta, recuperar evidência por faceta e declarar lacunas.

**Escopo candidato:** uma comparação, até 3 facetas, fontes habilitadas e prazo global.

**Aceite:**

- Cada necessidade tem evidência ou lacuna.
- Orçamento global não reinicia por subtarefa.
- Não exigir vários agentes para decompor.
- Conflito não é resolvido por quantidade de sites.
- Resposta parcial identifica a parte faltante.
- Datas, unidades e critérios preservados.

**Métrica:** cobertura de facetas, suporte e custo por resposta completa.

**Dependências:** I03 e fontes/capacidades requeridas; I09/I10 se temporalidade exigir.

**Corte:** duas facetas e duas fontes.

### I12 — Uma modalidade adicional

**História:** como investidor, quero respostas que dependem de formato/acesso ainda indisponível.

**Requisito R-I12:** disponibilizar uma capacidade e demonstrar uma pergunta antes não atendida.

**Escopo por instância:** escolher apenas PDF textual, OCR, navegador para uma seção dinâmica ou uma API/feed.

**Aceite:**

- Fonte/modalidade autorizadas.
- Classe real de perguntas passa a ser atendida.
- Limites de rede, bytes, tempo e cancelamento específicos.
- PDF preserva páginas, tabelas/ressalvas; OCR recebe revisão compatível.
- Navegador controla subrequisições e destinos auxiliares.
- Falha de extração não vira resposta inventada.
- Conector observável e desativável.

**Métrica:** perguntas antes indisponíveis agora aceitas, extração e custo.

**Dependências:** I04 e autorização. Cadastro segue I01/I06.

**Corte:** um template/seção. PDF, OCR e JavaScript são instâncias diferentes.

### I13 — Custo ou latência de uma rota

**História:** como usuário ou responsável pelo produto, quero uma rota mais rápida ou sustentável sem perda de qualidade.

**Requisito R-I13:** resolver um gargalo medido.

**Escopo por instância:** um objetivo principal e uma intervenção, como cache, reduzir coleta repetida ou diminuir contexto.

**Aceite:**

- Baseline, carga e objetivo registrados.
- p50/p95 quando latência for alvo; custo integral comparável quando custo for alvo.
- Qualidade/política sem regressão.
- Cache não mistura usuários nem ignora vencimento/suspensão.
- Resultado demonstrado e implantado na rota.

**Métrica:** objetivo escolhido, com qualidade como limite.

**Dependências:** I03 e telemetria; I04 quando envolver rede.

**Corte:** uma rota e uma alteração. “Escalar tudo” é épico.

### I14 — Continuidade em uma classe de incidente

**História:** como investidor, quero resposta adequada ou limitação clara diante de falha.

**Requisito R-I14:** reduzir impacto ou recuperação de um cenário.

**Escopo por instância:** origem indisponível, restauração de catálogo, perda de worker ou outro cenário priorizado.

**Aceite:**

- Impacto, objetivo e responsáveis definidos.
- Implementar/exercitar o mecanismo escolhido.
- Fallback nunca usa fonte não aprovada ou conteúdo vencido silenciosamente.
- Medir por falha controlada.
- Runbook exercitado; operador diferente do autor quando viável.
- Estado/auditoria permitem entender o ocorrido.

**Métrica:** utilidade preservada, interrupção ou recuperação, conforme o cenário.

**Dependências:** I04 e recursos necessários. Fonte alternativa precisa estar habilitada.

**Corte:** uma origem ou procedimento. Timeout e falha segura básica já entram em I04; aqui se acrescenta continuidade.

## 6. Metadados e arquitetura evolutiva

### 6.1 Dados entram quando há uso e validação

| Dados | Primeiro incremento | Evolução |
|---|---|---|
| ID, nome, URL, seção, publicador | I01 | Mais seções/hosts e relações editoriais |
| Temas, tarefas, resumo, exclusões, unknown | I01 | Taxonomia conforme demanda |
| Evidência de perfil, revisor, estado, prazo | I01 | Mudanças e revisão por risco |
| Aliases/exemplos | I02 | Lexical/vetor em I07/I08 |
| Documento, versão, localizador, validade | I03 | Modalidades/retenções |
| URL efetiva, HTTP, extração | I04 | Novos conectores em I12 |
| Hash, verificação, mudança, próxima revisão | I05 | Priorização de manutenção |
| Vigência/substituição/evento | I09/I10 | Histórico aplicável |
| Origem editorial/independência | Quando várias fontes exigirem | Evitar falsas confirmações |
| Features de ranking e custo | I07/I08/I13 | Apenas as utilizadas |

Usar IDs estáveis e schema_version desde o início. Não construir o modelo físico final completo em I01.

### 6.2 Perfil inicial

~~~json
{
  "schema_version": "1.0",
  "source_id": "src-001",
  "section_id": "sec-001",
  "name": "Fonte de exemplo",
  "url": "https://fonte.example.org/educacao/",
  "topic_ids": ["investimentos.renda_fixa"],
  "task_ids": ["explicar_conceito"],
  "summary": "Resumo fundamentado nos extratos fornecidos.",
  "exclusions": ["cotacao_tempo_real"],
  "unknowns": ["cobertura_historica"],
  "classification_evidence_ids": ["ev-perfil-001"],
  "status": "pending_review",
  "profile_version": 1,
  "reviewed_by": null,
  "review_due_at": null,
  "access_policy_id": "pol-001"
}
~~~

A política de acesso é do backend; a IA não pode aprová-la. Pendência não é elegibilidade.

### 6.3 Contratos mínimos

**Rota:** request_id, query_sanitized, intent, selected_section_ids, catalog_version, policy_version, reason_codes e budget.

**Evidência:** evidence_id, document_version_id, source_id, section_id, URL validada, trecho/dado, localizador, datas aplicáveis, qualidade e restrição de uso.

**Resposta:** status, blocos, claim_ids, evidence_ids, limitações e referência temporal.

Estados: answered, partially_answered, needs_clarification, no_approved_source, temporarily_unavailable e insufficient_evidence; acrescentar conflicting_evidence quando aplicável.

Saída de LLM é proposta. Backend valida contrato, referências e política. A2UI/NDJSON apresentam o resultado.

### 6.4 Controles por exposição

| A partir de | Obrigatório |
|---|---|
| I01 — extratos externos | Dados não confiáveis, proposta estruturada, aprovação autenticada |
| I02 — links no chat | Perfis ativos, links sanitizados, suspensão aplicada |
| I03 — fatos | Evidência, validade, suporte semântico, privacidade e auditoria |
| I04 — saída web | Allowlist host/path/porta, DNS/IP/redirect/TLS, robots/direitos, limites e cancelamento |
| I05 — recorrência | Idempotência, concorrência, histórico e revisão/vencimento |
| I12 — modalidade nova | Controles específicos antes da habilitação |
| Todos | Sem segredos/dados pessoais desnecessários em pesquisa/logs |

O filtro site: de um buscador não comprova que toda a consulta/processamento ficou nos domínios permitidos. A exigência estrita requer canais/índice/coleta com fronteira demonstrável, não um buscador irrestrito temporário.

### 6.5 Três mudanças diferentes

- **Conteúdo:** a página mudou e pode alterar uma resposta.
- **Perfil:** mudou a cobertura usada para rotear.
- **Política:** mudou o que pode ser acessado, mantido ou exibido.

Notícia nova não exige reclassificar o site inteiro. Domínio novo não é mera alteração de título. Mudança regulatória pode suspender respostas sem alterar o tema do perfil.

Separar catálogo, política, roteamento, recuperação e evidência logicamente. Não exigir microserviço por módulo, plataforma de agentes ou banco vetorial desde o início.

## 7. Tarefas atômicas e estados

### 7.1 Incremento versus tarefa

Incremento é resultado utilizável. Tarefa é unidade técnica verificável dentro dele. “Criar schema” pode ser tarefa necessária sem ser valor independente ao investidor.

A pontuação pertence ao item estimado pelo time. Não contar pontos do pai e das subtarefas em duplicidade.

### 7.2 Decomposição de I01

| Tarefa | Requisito próprio | Dependência | Resultado verificável | Estado |
|---|---|---|---|---|
| I01-A | Fixar lote/tema, revisor e comparação | — | Amostra autorizada, recorte e método de medição aceitos | proposed |
| I01-B | Representar perfil/proposta/evidência | I01-A | Contrato com exemplos válidos/inválidos | proposed |
| I01-C | Gerar proposta sem publicar | I01-B | Saída estruturada, evidências resolvidas e autoridade preservada | proposed |
| I01-D | Revisar/publicar no processo existente | I01-C | Decisões registradas e versões concorrentes protegidas | proposed |
| I01-E | Liberar uso e medir | I01-D | Lote usado, custo/tempo/correções registrados e handoff aceito | proposed |

Ausência de acesso/material bloqueia a entrada da tarefa dependente; não fica oculta na execução.

### 7.3 Decomposição dos demais itens

No refinamento de cada item priorizado, instanciar:

1. **A — caso e baseline:** recorte, risco, amostra e métrica.
2. **B — comportamento mínimo:** implementação dentro dos contratos.
3. **C — validação:** riscos específicos, regressão e limitações.
4. **D — disponibilização:** uso, retorno/rollback e medição.

Se B tiver entregas independentes, decompor B1/B2 com requisito/aceite próprios. Não detalhar centenas de tarefas antes de escolher lotes, nem considerar essa lista genérica como backlog ready.

Se o conjunto exceder o limite, dividir por valor, não apenas multiplicar subtarefas.

### 7.4 Estados

~~~mermaid
stateDiagram-v2
  [*] --> proposed
  proposed --> ready
  ready --> in_progress
  in_progress --> in_review
  in_review --> done
  in_review --> in_progress
  ready --> blocked
  in_progress --> blocked
  blocked --> ready
  proposed --> cancelled
~~~

- **proposed:** ideia de entrega; sem compromisso de tamanho.
- **ready:** DoR satisfeito, dependências concluídas, responsáveis e estimativa definidos.
- **in_progress:** reserva, versão base e tentativa registradas.
- **in_review:** artefato e evidências disponíveis.
- **done:** DoD verificado, entrega utilizável.
- **blocked:** motivo, responsável e próxima ação registrados.
- **cancelled:** decisão e impacto nos dependentes revisados.

Uma tarefa done não comprova incremento done. Alteração posterior gera trabalho vinculado; não apaga o histórico.

### 7.5 Registro e handoff

~~~json
{
  "increment_id": "I01",
  "task_id": "I01-C",
  "requirement_id": "R-I01-C",
  "status": "proposed",
  "depends_on": ["I01-B"],
  "scope_ref": "escopo-I01-v1",
  "owner": null,
  "reviewer": null,
  "base_version": 1,
  "attempt": 0,
  "artifact_refs": [],
  "acceptance_evidence_refs": [],
  "blocker": null,
  "state_version": 1
}
~~~

Transição registra ator, instante, motivo e versão esperada. Handoff contém contrato, artefato, evidência, limite conhecido e decisões que afetam o próximo executor. Não exigir releitura de todo o projeto a cada tarefa.

## 8. Métricas e DoD

### 8.1 Métricas que demonstram valor

| Estágio | Medir | Não usar isoladamente |
|---|---|---|
| Curadoria | Tempo total e qualidade de aprovação | Perfis gerados pela IA |
| Indicação | Fonte adequada e utilidade | Links mostrados |
| Resposta | Perguntas atendidas com suporte/validade | Fluência |
| Coleta | Evidência útil no prazo | Páginas baixadas |
| Expansão | Novos casos de uso cobertos | URLs cadastradas |
| Manutenção | Mudanças tratadas e fila saudável | Jobs executados |
| Otimização | Custo/latência com qualidade | Tokens reduzidos |
| Continuidade | Impacto/recuperação exercitados | Runbook apenas escrito |

Cada métrica precisa de baseline, amostra, janela, responsável e critério. Avaliar por tema/risco; média global não compensa erro grave.

### 8.2 DoR comum

- [ ] Beneficiário e problema definidos.
- [ ] Recorte com valor utilizável.
- [ ] Dependências técnicas/de conteúdo verificadas.
- [ ] Responsável, revisor e ambiente disponíveis.
- [ ] Aceite e métrica definidos.
- [ ] Material/uso autorizados.
- [ ] Time estimou até 8 ou escolheu corte alternativo.
- [ ] Limites e fora de escopo explícitos.

### 8.3 DoD comum

- [ ] Comportamento utilizável entregue ao beneficiário.
- [ ] Aceite específico demonstrado.
- [ ] Controles necessários ao risco ativos.
- [ ] Contratos/estado versionados.
- [ ] Testes relevantes e regressão passaram.
- [ ] Revisão, evidência e limitações registradas.
- [ ] Baseline/métrica coletados.
- [ ] Monitoramento contínuo quando necessário.
- [ ] Falha segura e retorno compatíveis com o risco.
- [ ] Nenhuma falha crítica aberta.
- [ ] Handoff aceito.

Distinguir **entrega concluída** de **benefício confirmado**. Um efeito que depende de uso posterior tem janela e responsável para acompanhamento. Não afirmar redução de esforço antes da medição; não exigir semanas de tráfego para marcar uma implantação controlada como entregue.

### 8.4 DoD de lote de fontes

- [ ] Identidade/endpoints/operações autorizados.
- [ ] Perfil por seção fundamentado.
- [ ] Exclusões/unknown explícitos.
- [ ] Revisor e validade definidos.
- [ ] Método de obtenção/extração validado.
- [ ] Perguntas positivas, negativas e ambíguas exercitadas.
- [ ] Evidência/temporalidade verificadas quando há resposta.
- [ ] Suspensão impede seleção, consulta e uso.
- [ ] Manutenção sustenta a validade prometida.
- [ ] Cobertura nova contada por perguntas suportadas.

### 8.5 Maturidade enterprise

Não depende de concluir todos os itens opcionais. Depende de evidências aplicáveis ao escopo/carga reais.

| Dimensão | Evidência necessária |
|---|---|
| Cobertura | Inventário reconciliado e fontes ativas com casos suportados |
| Governança | Identidade, direitos, donos, revisões e suspensão |
| Qualidade | Dataset versionado, revisão por risco, suporte e temporalidade |
| Segurança | Fronteira de rede, privacidade, ferramentas limitadas e testes adversariais |
| Atualidade | Revisões/validações no prazo e tratamento de remoção/mudança |
| Operação | Monitoramento, orçamento, runbooks, capacidade e recuperação demonstrados |
| Evolução | Contratos, regressão e rollout/rollback por escopo |
| Auditoria | Reconstituição por versões/evidências dentro da retenção permitida |
| Sustentabilidade | Custo integral e capacidade da fila humana |

Construir essas evidências nas entregas e ampliá-las conforme exposição. Não concentrar segurança/operação em uma última sprint.

### 8.6 Avaliação proporcional

Começar com amostra pequena curada, declarar limitações e ampliar estratos com cobertura. Separar configuração, validação e teste; manter paráfrases semelhantes no mesmo grupo.

Zero falhas observadas não prova risco zero. Avaliação por outra LLM pode ajudar na triagem, mas não substitui revisão especializada em temas críticos. Não exigir um segundo agente para cada documento quando regras e revisão focada bastam.

## 9. Migração do backlog anterior

Não herdar integralmente as dependências anteriores: isso recriaria a longa sequência antes do primeiro valor.

| Tema anterior | Novo destino |
|---|---|
| T01–T10: descoberta, política, modelos e dataset | Recorte necessário a I01–I03; aprofundamento por necessidade |
| T11,T14,T18: catálogo/persistência/importação | I01 mínimo; lotes I06 |
| T12,T13,T15–T17,T19: acesso/coleta/conteúdo | Materiais aprovados em I01/I03; rede segura I04; modalidades I12 |
| T20–T22: interpretação/baseline/lexical | I02 e I07 |
| T23–T25: vetores e comparação | I08 condicionado; comparação simples desde I02/I07 |
| T26–T30: recuperação/validação/chat | I03/I04; facetas I11 |
| T31: atualização | I05; temporalidade específica I09/I10 |
| T32: suspensão/revogação | Básico I02; evidência/cache/rede desde I03/I04 |
| T33: observabilidade/auditoria | Mínimo em cada entrega; aprofundamento pelo risco |
| T34–T37: segurança/carga/qualidade/operação | Dentro de cada item; objetivos adicionais I13/I14 |
| T38,T39: extensões | I12 por capacidade |
| T40,T41: expansão/rollout | I06 por lote e liberação por escopo |

## 10. Self-check e limites

Esta é revisão do próprio documento, não avaliação independente por outro modelo nem teste do sistema.

Verificação documental realizada: três exemplos JSON válidos; 14 fichas de incremento com requisito, aceite, métrica e corte de escopo; blocos de código balanceados. Dependências condicionais precisam ser substituídas por IDs concretos no refinamento de cada instância; o roadmap não é um backlog já estimado ou pronto para execução integral.

| Verificação | Resultado |
|---|---|
| Primeiro incremento tem valor? | Sim, condicionado ao uso real e aceite pela curadoria |
| Esse valor foi confundido com resposta web? | Não; I01 operacional, I02 indicação, I03 resposta, I04 web |
| Há necessidade de classificar todos os sites antes? | Não; lotes aprovados funcionam e pendentes ficam desativados |
| Agente autônomo foi considerado obrigatório? | Não; workflow assistido primeiro |
| IA garante consistência? | Não; evidência, revisão e monitoramento continuam necessários |
| Há reanálise completa em todo ciclo? | Não; mudança/lacuna/risco e revisão periódica |
| Todos os itens foram declarados 8 pontos? | Não; estimativa depende do time e da reutilização |
| Infraestrutura isolada foi vendida como valor ao investidor? | Não; dependência habilitadora é explícita |
| Vetor é obrigatório? | Não |
| Segurança ficou para o fim? | Não; precede a exposição correspondente |
| Enterprise é uma lista fixa de tecnologias? | Não; critérios são evidências por escopo/carga |
| Há estados/requisitos/dependências? | Sim; I01 decomposto e demais itens refinados conforme prioridade |
| Há falsa promessa de ganho experimental? | Não; I08 distingue redução de incerteza de benefício direto |

### 10.1 Resolver no refinamento de I01

1. Tema e beneficiário prioritários.
2. Duas a cinco fontes com amostras autorizadas.
3. Acesso à LLM e mecanismo de registro/revisão.
4. Donos de classificação e de autoridade/permissão.
5. Baseline comparável e erro material.
6. Hipótese de economia.
7. Estimativa usando uma atividade de referência do time.

Não é necessário escolher agora banco vetorial, conectores futuros ou taxonomia completa dos 313 sites.

### 10.2 Riscos de execução

- Dependência descoberta tarde: verificar acesso no DoR.
- Cobertura artificial: contar perguntas suportadas e lacunas.
- Fila humana virar gargalo: medir entrada/saída, idade e criticidade.
- IA aumentar retrabalho: medir tempo total e erro.
- Autonomia prematura: separar sugestão de aprovação.
- Forçar 8 pontos: cortar escopo e reestimar, preservando controles.
- Voltar a camadas técnicas: exigir uso/benefício no aceite.
- Excesso documental inicial: registrar decisões do recorte e aprofundar por necessidade.

## 11. Fundamentação auditável

Referências primárias consultadas em 21/10/2026. Mecanismos são fundamentados; tamanhos de lote, pontuação e metas são propostas locais.

| ID | Referência | Fundamento |
|---|---|---|
| R01 | [Scrum Guide](https://scrumguides.org/scrum-guide.html) | Incremento utilizável, aditivo, verificado e sujeito ao DoD |
| R02 | [Atlassian — Story points and estimation](https://www.atlassian.com/agile/project-management/estimation) | Estimativa relativa por esforço, complexidade e risco |
| R03 | [Anthropic — Building effective agents](https://www.anthropic.com/research/building-effective-agents) | Workflow versus agente e complexidade justificada |
| R04 | [NIST — AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) | Supervisão, medição e monitoramento contínuos |
| R05 | [IETF RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html) | Validação HTTP condicional |
| R06 | [IETF RFC 9309](https://www.rfc-editor.org/rfc/rfc9309.html) | Protocolo robots e suas condições |
| R07 | [OWASP — Prompt Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html) | Risco de instruções em dados externos e defesas em camadas |
| R08 | [OWASP — SSRF Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html) | Validação de destinos e redirects |
| R09 | [Microsoft Learn — Hybrid search](https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview) | Combinação lexical/vetorial e ranking |
| R10 | [W3C — PROV-O](https://www.w3.org/TR/prov-o/) | Proveniência |
| R11 | [JSON Schema 2020-12](https://json-schema.org/draft/2020-12) | Contratos estruturais |
| R12 | [OpenTelemetry — Traces](https://opentelemetry.io/docs/concepts/signals/traces/) | Correlação operacional |

R03 é usado como referência de padrões, não indicação de ferramenta ou modelo. O artigo reconhece evolução do ferramental desde sua publicação; o uso aqui é conceitual.

### 11.1 Decisão versus evidência

| Decisão | Natureza | Base | Comprovação local |
|---|---|---|---|
| Incrementos por benefício | Entrega | R01 | Uso/aceite por incremento |
| Limite pretendido de 8 | Planejamento | R02 | Estimativa/histórico do time |
| Workflow curador primeiro | Arquitetura | R03 | Tempo/erro/custo em I01 |
| Aprovação humana de campos críticos | Governança | R04,R07 | Revisão e testes de autoridade |
| IA principalmente por mudança | Hipótese de eficiência | R05 + desenho proposto | Chamadas/custo/perdas em I05 |
| Pequenos lotes | Hipótese de recorte | Requisito incremental | Estimativa e DoD do lote |
| Meta de 20% de economia | Hipótese local | Sem benchmark externo | Comparação manual/assistida |
| Separar indicação/resposta/web | Recorte de produto | Exposições e reutilização distintas | I02–I04 |
| Controles antes da rede | Segurança | R06–R08 | Suíte e revisão de acesso |
| Vetor só com ganho | Complexidade | R03,R09 | Comparação em I08 |
| Versionar proposta/evidência | Auditoria | R10,R11 | Reconstrução de um caso |
| Capacidade por gargalos | Operação | R04,R12 | I13/I14 |

Nenhuma referência prova que 5 fontes cabem em 8 pontos ou que IA reduzirá 20% do esforço.

### 11.2 Registro de aceite

~~~yaml
acceptance_record:
  increment_id: I01
  instance_id: I01-lote-01
  scope_version: 1
  estimated_points: null
  estimation_status: pending_team_estimate
  beneficiary: curadoria
  baseline_ref: null
  metric_results_ref: null
  artifacts: []
  reviewer: null
  accepted_at: null
  delivery_status: proposed
  business_outcome_status: not_measured
  limitations: []
~~~

Null e not_measured são intencionais. Entrega não comprova automaticamente o resultado de negócio.

## 12. Checklist do próximo refinamento

- [ ] Aceitar I01 como valor operacional; caso contrário, selecionar caso direto com capacidades demonstradas.
- [ ] Escolher tema e lote de fontes.
- [ ] Confirmar amostras, permissões e revisor.
- [ ] Confirmar LLM, registro e revisão.
- [ ] Definir baseline e erro material.
- [ ] Estimar I01 e aplicar corte se ultrapassar 8.
- [ ] Atribuir tarefas I01-A a I01-E.
- [ ] Demonstrar uso operacional no aceite.
- [ ] Refinar I02 sobre o catálogo realmente produzido.
- [ ] Priorizar os itens seguintes por demanda, métricas e risco.
- [ ] Expandir em lotes sem aprovação em massa.
- [ ] Demonstrar maturidade enterprise no escopo efetivamente liberado.

