# Guia rápido de eficiência de tokens no Cursor

> 💡 **Objetivo:** escolha a menor combinação de contexto, modo, modelo e effort que atenda ao risco da tarefa. Promova somente quando uma evidência observável mostrar um gargalo.

O custo por entrega inclui tokens de entrada e saída, cache, chamadas de ferramentas, coordenação entre agentes, latência e retrabalho. Por isso, o menor preço por token não garante o menor custo total.

> 📚 **Dados variáveis:** consulte a [referência detalhada](GUIA-TOKEN-EFFICIENCY-REFERENCE.md) para modelos, preços, limites e fontes oficiais. Revalide-os antes de decisões de longo prazo.

## Termos mínimos

- **Contexto efetivo:** somente a evidência realmente enviada ou lida pelo agente para concluir a tarefa.
- **Effort:** nível de raciocínio alocado pelo modelo. Mais effort pode melhorar a análise, mas não garante uma resposta correta.
- **Baseline:** opção inicial usada como comparação de custo e qualidade.
- **Tool use:** uso de ferramentas, como leitura de arquivos, terminal, testes ou busca.
- **Promoção:** trocar modelo, effort ou contexto porque o baseline não atende a um critério observável.
- **Q&A:** perguntas e respostas sem alteração de arquivos.

## Ordem de decisão

1. Defina a atividade e a dificuldade: básica, média ou avançada.
2. Escolha o modo e o effort inicial.
3. Use a matriz como hipótese de baseline.
4. Meça o resultado contra o critério de aceite.
5. Promova apenas para remover o gargalo identificado.

> 🧭 **Decisão operacional:** primeiro fixe a necessidade; depois pague pela capacidade necessária. Isso reduz escolhas pelo nome do modelo.

## Modo e effort

| Modo | Use para | Effort inicial | Aumente quando |
| --- | --- | --- | --- |
| `Ask` | explicar, comparar, localizar ou diagnosticar sem editar | `low`/default | houver erro factual, ambiguidade ou análise insuficiente |
| `Plan` | decisões, dependências e trade-offs antes de editar | `medium` | houver alternativas válidas, migração ou alto custo de reversão |
| `Agent` | implementar e testar | default/`medium` | falhar uma regra, teste, contrato ou integração |
| `Debug` | investigar falha com sintoma e evidência | `medium` | existirem hipóteses concorrentes ou falha multi-sistema |
| `Multitask` | subtarefas independentes | default/`medium` | a coordenação exigir síntese adicional |

Use `high`/`max` apenas quando o custo esperado de uma decisão errada superar o custo adicional de raciocínio. Para o significado operacional e as restrições de cada modo, veja a seção 4 da [referência detalhada](GUIA-TOKEN-EFFICIENCY-REFERENCE.md#4-escolha-de-modo-e-effort).

## Escolha rápida

> 🔎 **Leitura da matriz:** as rotas são hipóteses por atividade e dificuldade; não são um ranking universal de qualidade.

As rotas desta matriz seguem a [seção 3 da referência detalhada](GUIA-TOKEN-EFFICIENCY-REFERENCE.md#3-candidatos-por-atividade-modo-e-dificuldade), que é a fonte canônica para candidatos, preços e promoções.

| Tarefa e dificuldade | Baseline | Alternativa de menor custo | Promoção por capacidade | Promova quando |
| --- | --- | --- | --- | --- |
| Q&A, extração ou formatação básica (`Ask`) | `gpt-5.4-nano-medium` | —; o baseline já é a opção de menor custo | `composer-2.5` | uma regra objetiva falhar ou a tarefa exigir ferramentas |
| Análise ou discovery básico (`Ask`/`Plan`) | `glm-5.2-high` | `kimi-k2.7-code` | consulte o nível médio ou avançado | faltarem dependências ou alternativas necessárias à decisão |
| Requisitos e documentação média (`Ask`/`Plan`) | `claude-sonnet-5` | `glm-5.2-high` | `claude-opus-5-thinking-high` para decisão crítica | a síntese exigir mais contexto ou raciocínio |
| Arquitetura, ADR ou RFC avançada (`Plan`) | `kimi-k3-max` | `glm-5.2-high` | `claude-opus-5-thinking-high` | o custo de reversão justificar a decisão mais cara |
| Desenvolvimento local médio (`Agent`) | `cursor-grok-4.6-medium` | `glm-5.2-high` | `gpt-5.4-high` | houver integração multi-arquivo, contrato implícito ou testes difíceis |
| Código em volume médio (`Agent`/`Multitask`) | `kimi-k2.7-code` | `composer-2.5` para subtarefas curtas | `glm-5.2-high` | a síntese exigir mais contexto ou a coordenação eliminar a economia |
| Debugging avançado (`Debug`) | `gpt-5.6-sol-medium` | `glm-5.2-high` | `claude-opus-5-thinking-high` | hipóteses concorrentes e custo de falha justificarem a promoção |

As tarefas básicas e avançadas de desenvolvimento em volume, e as demais combinações de atividade e dificuldade, estão na [seção 3 da referência detalhada](GUIA-TOKEN-EFFICIENCY-REFERENCE.md#3-candidatos-por-atividade-modo-e-dificuldade). Não extrapole uma rota média para outro nível de dificuldade.

## Gatilhos observáveis de promoção

Promova somente depois de identificar o gargalo:

| Evidência observada | Gargalo | Ajuste |
| --- | --- | --- |
| teste, requisito ou regra objetiva falha | raciocínio ou execução | aumente effort ou use o próximo modelo da rota |
| falta um arquivo, contrato ou dependência indispensável | contexto | anexe somente a evidência ausente |
| a tarefa requer mais integrações do que o baseline suporta | capacidade de execução | use o próximo modelo indicado |
| há hipóteses concorrentes sem evidência suficiente | investigação | aumente effort ou use a rota avançada |
| retrabalho medido supera o custo adicional estimado | custo total | promova e registre o resultado |

Não promova quando o problema for instrução vaga ou escopo excessivo: nesses casos, reduza o contexto e explicite o critério de aceite.

### Amostra controlada mínima

Para mudar uma rota padrão, compare pelo menos três tarefas representativas com:

1. mesmo critério de aceite e mesmo escopo;
2. contexto equivalente e evidência necessária preservada;
3. registro de testes aprovados, tokens, cache, tool use, tempo, intervenções e correções posteriores.

Adote a alternativa apenas se ela mantiver os critérios de aceite e reduzir o custo efetivo. Essa comparação isola o efeito da rota de variações de escopo e evita concluir que um preço menor é automaticamente melhor.

## Regra de contexto

> ⚠️ **Controle de escopo:** contexto maior é capacidade, não objetivo.

- prefira seleção ou `@arquivo` a anexar uma pasta;
- peça um path adicional por vez quando faltar evidência;
- anexe recortes de logs, não logs inteiros;
- abra novo chat ao mudar de objetivo;
- use `@Branch` e `@Terminals` somente quando a tarefa exigir esse escopo.

Um contexto de 1M não é meta de anexação. Arquivos irrelevantes competem com evidências importantes, elevam o custo e podem reduzir a precisão.

## Verificação antes de publicar ou decidir

> ✅ **Checklist de decisão:** confirme os dados variáveis e preserve a evidência que fundamenta a rota escolhida.

- confirme no Cursor o nome exibido, o modelo selecionado, o plano, o preço e a disponibilidade;
- confira limites de contexto e regras de cache nas fontes oficiais da [referência detalhada](GUIA-TOKEN-EFFICIENCY-REFERENCE.md#13-fontes-oficiais);
- valide a rota em tarefas representativas antes de torná-la padrão;
- preserve a evidência que permite revisar a decisão.

> ⚠️ **Limite metodológico:** recomendações de rota são hipóteses operacionais. Elas apoiam comparação e execução; não são garantia de qualidade, economia ou resultado.
