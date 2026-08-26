# Auditoria técnica do Protocolo de Exploração e das 20 Lentes de Portfólio

**Data da revisão:** 25 de agosto de 2026  
**Escopo:** capacidade de produzir insights decisórios a partir da posição atual do investidor, com enriquecimentos determinísticos e fontes externas.  
**Natureza:** desenho de produto e arquitetura analítica; não constitui recomendação individual de investimento, tributária ou jurídica.

---

## 1. Parecer executivo

O protocolo tem uma fundação correta — separar cálculo determinístico de síntese em linguagem natural —, mas o catálogo ainda não é “definitivo”. Das 20 lentes:

- **6 têm alto valor e podem integrar o núcleo do MVP**, desde que sejam corrigidas: look-through, sensibilidade a juros, risco por emissor/garantia, assimetria de derivativos, integridade de hedge e alavancagem econômica;
- **8 são valiosas, porém dependem de dados que a posição atual não contém**, como perfil, necessidades futuras, lotes de aquisição, contratos completos, histórico de ordens ou séries de mercado;
- **4 são alertas operacionais ou itens de higiene**, úteis no produto, mas fracos para disputar o top 5 de “insights intelectuais”;
- **2, na forma proposta, são epistemicamente inválidas**: inferir a estratégia barbell pela fotografia da carteira e reconstruir a taxa original de um título apenas por valor atual, quantidade e vencimento.

As falhas mais graves são anteriores às lentes:

1. **`nulo → R$ 0` é uma normalização economicamente destrutiva.** Zero é um valor observado; nulo é ausência ou inaplicabilidade. A conversão cria patrimônio ficticiamente nulo, distorce pesos e pode fabricar concentração, perda e risco de crédito.
2. **O fluxo obriga a LLM a produzir uma hipótese para toda lente.** Isso induz confirmação e transforma ausência de evidência em narrativa. Uma saída legítima precisa ser `NOT_APPLICABLE`, `INSUFFICIENT_DATA` ou `NO_MATERIAL_FINDING`.
3. **A carteira atual não revela intenção.** Não permite concluir se o investidor é previdenciário, se a proteção foi deliberada, se há patrimônio fora da B3, qual perda tolera ou quando precisará do dinheiro.
4. **Fato, inferência, cenário e recomendação estão misturados.** Cada um exige um nível diferente de prova e de responsabilidade regulatória.
5. **“Validação adversarial interna” não é evidência auditável.** O produto precisa guardar premissas, evidências, cálculos, contrahipóteses e razão de aprovação/rejeição; não depender de raciocínio oculto do modelo.

O ponto central é este: **um Power BI pode exibir qualquer cálculo determinístico que seja programado**. O que diferencia um insight não é ser “impossível em um relatório”, e sim conectar evidências dispersas a uma decisão relevante, testar explicações alternativas e explicitar em quais condições a conclusão muda.

> **Definição operacional:** um insight é uma síntese decisória sustentada por evidências, que revela uma relação material não evidente na visualização da posição, muda a compreensão de um risco ou trade-off e continua válida após contrafactuais razoáveis.

---

## 2. O teto informacional da carteira atual

### 2.1 O que a fotografia da posição pode sustentar

Com posição, contratos completos e metadados versionados, o motor consegue sustentar:

- exposição direta e indireta por ativo, emissor, conglomerado, indexador e fator previamente mapeado;
- fluxos contratuais, vencimentos, duration, DV01 e cenários de curva, se os termos do instrumento estiverem disponíveis;
- nocional, payoff, delta equivalente e perdas em cenários de derivativos, se todas as pernas e especificações estiverem presentes;
- elegibilidade e eficiência de garantias, considerando regras, limites e deságios vigentes;
- prazos contratuais de liquidez, carência, vencimento, empréstimo e eventos societários conhecidos;
- cobertura estimada do FGC, separando instrumentos elegíveis dos não elegíveis;
- qualidade, atualidade e cobertura dos dados de preço.

### 2.2 O que a fotografia não pode provar

A fotografia, isoladamente, não prova:

- objetivo, estratégia, perfil de risco ou horizonte do investidor;
- se uma sobreposição é erro, hedge, arbitragem, transição ou posição intencional;
- desempenho histórico, habilidade, comportamento ou qualidade de execução;
- custo de aquisição e lote fiscal, salvo se enviados separadamente;
- taxa original de um título quando faltam preço de compra e fluxos contratuais;
- necessidade de liquidez, passivos futuros, renda, reserva externa ou outros patrimônios;
- causalidade macroeconômica ou o que acontecerá com o preço;
- se um ativo sem preço sofreu deterioração de crédito.

### 2.3 Escada de personalização

| Nível | Contexto disponível | Linguagem permitida |
|---|---|---|
| P0 — desconhecido | Apenas posição | “A carteira apresenta...”; “se houver necessidade de caixa...” |
| P1 — declarado | Horizonte, objetivo, necessidade de caixa, tolerância a perda | “Isso conflita com o objetivo declarado...” |
| P2 — perfil verificado | Informações atualizadas de suitability e escopo regulatório definido | Recomendação personalizada, apenas se a instituição e o fluxo estiverem autorizados |

A Resolução CVM 30 vincula adequação a objetivos, situação financeira e conhecimento do cliente; também menciona horizonte, preferência de risco, finalidade e necessidade futura de recursos. Portanto, **se o produto emitir recomendações individualizadas**, não basta inferir perfil pela carteira ([Resolução CVM 30 consolidada](https://conteudo.cvm.gov.br/export/sites/cvm/legislacao/resolucoes/anexos/001/resol030consolid.pdf)).

---

## 3. Nova taxonomia: não chamar tudo de insight

| Tipo de saída | Exemplo | Pode entrar no top 5? |
|---|---|---|
| Qualidade de dados | “18% do valor nominal não tem preço confiável” | Sim, se material e se bloquear decisões |
| Fato de carteira | “35% está no setor financeiro” | Não, salvo se for evidência de uma conclusão maior |
| Diagnóstico | “O look-through eleva a exposição bancária de 18% para 31%” | Sim |
| Cenário | “Em choque de +200 bps, a perda estimada é X” | Sim, identificado como cenário, não previsão |
| Hipótese contextual | “Isso pode ser incompatível com caixa em 12 meses” | Sim, mas condicionada ou após confirmação do objetivo |
| Evento/alerta | “OPA com prazo de habilitação em 9 dias” | Sim, pela urgência, mesmo não sendo ‘criação intelectual’ |
| Recomendação | “Venda/troque/role” | Só após controles de adequação, autorização e explicação de trade-offs |

Essa separação evita que um alerta de cadastro seja vendido como inteligência e impede que uma hipótese da LLM seja apresentada como fato.

---

## 4. Classificação resumida das 20 lentes

**Legenda:** P1 = núcleo do MVP; P2 = fase seguinte ou dependência adicional; P3 = utilidade operacional/baixa prioridade; R = reconstruir antes de usar.

| # | Lente original | Valor potencial | Viável com posição atual? | Parecer |
|---:|---|---|---|---|
| 1 | Falsa diversificação | Alto | Sim, com look-through externo | **P1 — manter e fortalecer** |
| 2 | Exposição cambial invisível | Alto | Não de forma robusta | **P2 — reconstruir o método** |
| 3 | Ativos sem preço | Alto como incerteza | Parcialmente | **P1 — renomear; não inferir crédito** |
| 4 | Imunização/ALM | Alto | Sensibilidade sim; ALM não | **P1/P2 — separar em duas lentes** |
| 5 | Eficiência de colateral | Alto, nichado | Só com dados de margem | **P2 — manter condicional** |
| 6 | Liquidação de aluguel | Médio/alto | Só com contrato completo | **P2 — trocar previsão de squeeze por custo de opcionalidade** |
| 7 | Assimetria de derivativos | Muito alto | Sim, com todas as pernas | **P1 — prioritária** |
| 8 | Cachoeira de liquidez | Alto | Só descritiva sem objetivos | **P2; vira P1 com necessidade de caixa** |
| 9 | Armadilhas tributárias | Alto | Não sem lotes e regime | **P2 — corrigir cálculo e exemplo** |
| 10 | Risco por emissor/FGC | Muito alto | Sim, com grafo jurídico | **P1 — prioritária** |
| 11 | Passivos ocultos/bleed | Muito alto em alavancados | Só com taxas e contratos | **P1 condicional** |
| 12 | Delisting/eventos | Alto pela urgência | Exige feed de eventos | **P2 — evento, não previsão** |
| 13 | Zombie assets | Baixo/médio | Sim | **P3 — higiene, não top insight** |
| 14 | Barbell | Baixo na forma atual | Não permite inferir intenção | **R — converter em pergunta de confirmação** |
| 15 | Ticket erosion | Médio | Não sem execuções/quotes | **P3/P2 — análise de execução** |
| 16 | YTM presumido | Alto se correto | Não com os campos citados | **R — método matematicamente subdeterminado** |
| 17 | Hedge overlap | Muito alto | Sim, com instrumento completo | **P1 — renomear integridade do hedge** |
| 18 | Concentração de custódia | Médio | Parcialmente | **P3 — risco operacional, não de crédito** |
| 19 | Alavancagem sintética | Muito alto | Sim, com especificações | **P1 — separar margem, nocional e delta** |
| 20 | ESG/contágio macro | Alto, mas amplo | Não com robustez | **P2 — separar ESG de fatores macro** |

---

## 5. Auditoria lente a lente

### 1. Falsa Diversificação — manter, com look-through verificável

**O que há de intelectualmente útil:** revelar que nomes diferentes não significam riscos diferentes. A relação entre ação direta, ETF, fundo e índice raramente é visível na tela consolidada. A base CVM CDA descreve a composição de carteiras de fundos e é atualizada periodicamente; índices B3 também publicam composição, mas datas e defasagens precisam acompanhar o dado ([CVM — CDA](https://dados.cvm.gov.br/dataset/fi-doc-cda), [B3 — ETF de renda variável](https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/etf-de-renda-variavel.htm)).

**Problema atual:** somar ações por setor ainda é uma agregação. “BOVA11 + ITUB4” só vira insight quando o motor mostra a contribuição indireta de Itaú/setor financeiro, mede quanto a diversificação efetiva caiu e explica por que isso é material. Fundos podem ter divulgação defasada, “outros” ou ativos não identificados; ETF internacional não deve ser expandido pelo XML CVM como se fosse fundo local.

**Redesenho determinístico:**

\[
E_i = w_i^{direto} + \sum_f w_f \times h_{f,i}
\]

Calcular também HHI, número efetivo de exposições \(N_{efetivo}=1/\sum_i E_i^2\), concentração por controlador e diferença `antes × depois do look-through`. O payload deve carregar `source_as_of`, cobertura de decomposição e parcela desconhecida.

**Insight aprovado:** “Embora existam 12 linhas, 38% do risco econômico está ligado a bancos; 11 p.p. estavam ocultos em ETFs/fundos. O número efetivo de exposições cai de 8,2 para 5,4 após o look-through.”

**Teste adversarial:** trocar o ETF por seus componentes equivalentes não pode alterar a exposição econômica; apenas a forma de custódia.

### 2. Exposição Cambial Invisível — potencial alto, causalidade frágil

**O que há de útil:** mostrar que moeda de negociação e motor econômico são coisas diferentes. Uma carteira toda em BRL pode responder a USD/BRL.

**Problema atual:** origem da receita é apenas um indício. VALE3 tem receita em dólar, mas também custos, dívida, preço de minério e hedge; um “beta cambial” é variável no tempo. IVVB11 geralmente combina exposição ao índice externo e ao câmbio, mas isso depende do produto e de eventual hedge. Classificação manual `Long Dólar` não quantifica sensibilidade e pode atribuir ao câmbio um movimento causado por commodity ou bolsa americana.

**Redesenho:** usar metadados fundamentais como prior e estimar sensibilidade empírica em janelas múltiplas:

\[
\beta_{FX} = \frac{Cov(r_{ativo}, r_{USD/BRL})}{Var(r_{USD/BRL})}
\]

Aplicar regressão multivariada com fatores relevantes, estabilidade entre janelas e intervalo de confiança. Separar: exposição contratual em moeda, exposição econômica, hedge explícito e sensibilidade histórica.

**Insight aprovado:** “A parcela explicitamente dolarizada é 12%, mas a sensibilidade histórica estimada ao USD/BRL equivale a 27% do patrimônio; o resultado é instável entre janelas e tem confiança média.”

**Dados faltantes:** séries de preço/retorno, composição dos veículos, receita/custo por moeda, derivativos cambiais e data de referência. Sem isso, a lente deve retornar insuficiência, não uma narrativa.

### 3. Ativos “Sem Preço” — transformar em incerteza de avaliação

**O que há de útil:** quantificar quanto do patrimônio não pode ser avaliado ou liquidado com confiança. Isso pode alterar todas as outras conclusões.

**Erro conceitual:** ausência de preço **não se transforma automaticamente em risco de crédito**. Pode ser erro de integração, preço defasado, instrumento sem mercado secundário, valor não aplicável ou contrato cujo MTM está em outra fonte. O próprio plano contábil do Banco Central prevê registro de valor de mercado de COE, considerando seus componentes, o que mostra que `COE = sem preço` também é uma generalização inválida ([BCB — função contábil de valor de mercado do COE](https://www.bcb.gov.br/content/estabilidadefinanceira/supervisao/Fun%C3%A7%C3%B5es%20de%20Contas%20Novo%20Padr%C3%A3o.pdf)).

**Redesenho dos estados:** `OBSERVED_ZERO`, `MISSING`, `STALE`, `NOT_APPLICABLE`, `MODEL_VALUED`, `INDICATIVE`, `RESTRICTED`. Preservar valor nominal, custo, última observação, fonte e método de avaliação.

**Insight aprovado:** “22% do valor nominal está em instrumentos cuja avaliação tem mais de 30 dias ou depende de modelo. O peso real das demais classes pode variar entre X e Y; por isso os rankings de concentração 2 e 3 estão suspensos.”

**Não aprovar:** “Seu capital virou caixa-preta e o emissor pode quebrar.” Essa frase confunde avaliação, liquidez e crédito.

### 4. Imunização e descasamento de indexadores — separar risco de juros de ALM

**O que há de útil:** traduzir prazo contratual em sensibilidade econômica. Uma lista de vencimentos não mostra quanto o patrimônio reage a mudanças de curva.

**Problema atual:** ALM exige o lado do passivo — metas, despesas ou obrigações. Sem isso, existe apenas análise de ativos. Também é inadequado assumir “cenário de alta de juros” como verdade; o motor deve executar cenários simétricos e identificá-los como choques, não previsões.

**Redesenho P1 — sensibilidade de renda fixa:** duration, convexidade, DV01, exposição por vértice e indexador. Aproximação:

\[
DV01 \approx Valor \times Duration_{modificada} \times 0{,}0001
\]

Para IPCA+, separar choque de juro real, inflação e spread de crédito. Para pós-fixado, modelar reinvestimento e defasagem do indexador.

**Redesenho P2 — ALM verdadeiro:** comparar fluxos líquidos de ativos com necessidades declaradas por horizonte; medir gap, cobertura e sensibilidade conjunta.

**Insight aprovado:** “Apenas 24% do valor está em prefixados longos, mas eles explicam 71% da perda estimada num choque paralelo de +200 bps. Se o dinheiro for necessário antes do vencimento, a marcação a mercado passa a ser decisiva.”

### 5. Eficiência de Colateral — valiosa, mas altamente condicionada

**O que há de útil:** margem bloqueada é pequena na tela, mas a escolha do ativo dado em garantia pode criar custo de oportunidade, risco de liquidação ou concentração de liquidez.

**Problema atual:** `temBloqueio=true` não informa a causa nem autoriza a troca. Bloqueio por garantia, empréstimo, ordem, evento ou restrição judicial são estados distintos. CDB, LCI e LCA podem ser aceitos pela Câmara B3 apenas sob critérios de emissor, limites e disponibilidade; ações, Tesouro, ETFs e outros ativos também têm regras próprias. Portanto, a frase “troque por CDB/Tesouro e melhore a margem” não pode ser genérica ([B3 — garantias aceitas](https://www.b3.com.br/pt_br/produtos-e-servicos/compensacao-e-liquidacao/clearing/administracao-de-riscos/garantias/garantias-aceitas/)).

**Redesenho:** calcular, por ativo elegível, valor de mercado, crédito efetivo de garantia, deságio, limite, liquidez, custo de oportunidade, concentração e wrong-way risk. Separar `margem requerida`, `garantia depositada`, `crédito reconhecido` e `excesso de garantia`.

**Insight aprovado:** “R$ 42 mil em ações voláteis geram apenas R$ 19 mil de crédito de garantia. Há R$ 30 mil em ativo elegível com maior razão crédito/valor, mas a substituição reduziria liquidez imediata; compare as duas configurações antes de agir.”

**Validação obrigatória:** regras B3 e regras do participante na data da análise; simulação pós-substituição; nunca inferir motivo de bloqueio.

### 6. Risco de Liquidação de Aluguel — reformular como valor da liquidez cedida

**O que há de útil:** o doador recebe uma taxa, mas entrega temporariamente a capacidade de dispor instantaneamente do ativo. A B3 informa que, em contrato reversível pelo doador, a devolução pode levar dois pregões — ou três conforme o horário da solicitação ([B3 — perguntas frequentes de empréstimo](https://www.b3.com.br/pt_br/produtos-e-servicos/emprestimo-de-ativos/renda-variavel/s_pergfre/)).

**Problema atual:** volatilidade ou beta não predizem short squeeze. “Penny stock + aluguel” não basta. O risco verdadeiro é o custo de opcionalidade/recall, condicionado à reversibilidade, prazo, liquidez do papel, eventos e intenção de venda. O ciclo à vista segue D+2 em 2026; a B3 anunciou D+1 para fevereiro de 2028, logo os prazos devem ser versionados, não fixados no prompt ([B3 — projeto D+1](https://www.b3.com.br/pt_br/noticias/liquidacao-d-1.htm)).

**Redesenho:** comparar remuneração líquida do empréstimo com cenários de custo de indisponibilidade durante `Ds+2/Ds+3`, sem atribuir probabilidades inventadas. Incluir taxa, tributo, comissão, reversibilidade, carência, utilização do mercado, evento conhecido e liquidez.

**Insight aprovado:** “O contrato rende R$ 18 líquidos estimados até o vencimento; uma venda durante o prazo de recall pode ficar indisponível por dois ou três pregões. O trade-off é assimétrico se a intenção for negociar o evento societário em 6 dias.”

### 7. Assimetria de Derivativos — uma das melhores lentes do MVP

**O que há de útil:** traduzir várias pernas, strikes e vencimentos em distribuição de payoff. Isso dificilmente é percebido numa lista de posições e pode revelar risco de ruína ou falsa proteção.

**Problema atual:** não se pode classificar uma opção vendida como naked antes de consolidar ativo-objeto, todas as opções, futuros e coberturas por quantidade e vencimento. “Risco ilimitado” aplica-se, por exemplo, à call vendida descoberta; put vendida tem perda máxima grande, mas limitada. Prêmio recebido não equivale ao ganho final.

**Redesenho:** montar grupos por ativo/vencimento; calcular payoff líquido em grade de preços, máximo ganho/perda, breakevens, delta, gamma, theta, vega, cobertura e cenários de gap/volatilidade. Custos e liquidação física/financeira entram no contrato.

**Insight aprovado:** “A estrutura parece uma trava pela proximidade dos strikes, mas 40% da call vendida não está coberta pela call comprada. Acima de R$ X, a perda volta a crescer linearmente; um movimento de +15% produz perda de R$ Y, 6,4 vezes o prêmio recebido.”

**Testes metamórficos:** adicionar exatamente a quantidade de cobertura deve eliminar o trecho descoberto; duplicar todas as pernas deve duplicar valores, sem mudar breakevens.

### 8. Cachoeira de Liquidez — só vira insight quando encontra uma necessidade

**O que há de útil:** transformar produtos heterogêneos numa linha do tempo de caixa realmente disponível.

**Problema atual:** D+0/D+30/vencimento é uma tabela. “Não terá capital se ocorrer um passivo” é hipótese sem passivo conhecido. Liquidez também não é apenas prazo contratual: exige haircut de venda, imposto, carência, gates, horário de corte, liquidação e estresse de mercado.

**Redesenho:** calcular caixa líquido disponível por horizonte e cenário:

\[
Cobertura(h) = \frac{Caixa\ líquido\ realizável\ até\ h}{Necessidade\ declarada\ até\ h}
\]

Sem necessidade declarada, mostrar o mapa como diagnóstico e perguntar apenas o contexto que muda a conclusão: “Existe uso previsto de R$ X nos próximos 12 meses?”.

**Insight aprovado:** “Você declarou necessidade de R$ 80 mil em 90 dias. Em condições normais há R$ 96 mil realizáveis; num estresse com deságio e tributação, caem para R$ 63 mil. O risco é a dependência de vender ativos voláteis, não a quantidade nominal de produtos D+0.”

### 9. Armadilhas Tributárias — alto valor, exemplo original incorreto

**O que há de útil:** considerar que pequenas diferenças de data podem alterar a alíquota sobre o rendimento e mudar a melhor sequência de liquidação.

**Erro factual/matemático:** esperar 14 dias não reduz, de modo geral, a alíquota de 22,5% para 17,5%. A tabela regressiva atual passa de 22,5% até 180 dias para 20% entre 181–360, 17,5% entre 361–720 e 15% acima de 720; o benefício ocorre apenas ao cruzar o limite aplicável e incide sobre o rendimento tributável, não sobre o principal ([Receita Federal — Perguntas e Respostas IRPF 2026, questões 734 e 736](https://www.gov.br/receitafederal/pt-br/centrais-de-conteudo/publicacoes/perguntas-e-respostas/dirpf/p-r-irpf-2026-v1-00-2026-04-23.pdf)).

**Redesenho:** por lote de aquisição, calcular economia fiscal marginal e comparar com custo de oportunidade, risco de crédito, necessidade de caixa e custos:

\[
Benefício\ líquido = Ganho\ tributável \times \Delta alíquota - Custos - Custo\ de\ esperar
\]

Regras devem ser versionadas por produto, residência fiscal e data. Come-cotas, isenções, IOF e compensações não podem ser tratados por uma única fórmula.

**Insight aprovado:** “Este lote cruza de 20% para 17,5% em 14 dias. A economia máxima estimada é R$ 86, não R$ 2,5 mil sobre o saldo. Se o caixa for necessário agora, o ganho fiscal é imaterial.”

### 10. Risco Sistêmico de Emissor — excelente, mas o grafo jurídico precisa ser correto

**O que há de útil:** consolidar risco pelo obrigado econômico e pelo conglomerado, atravessando classes de produto. Essa relação é pouco visível na posição consolidada.

**Correção crítica do exemplo:** R$ 200 mil em CDB + R$ 100 mil em COE do mesmo banco não formam R$ 300 mil de saldo coberto. COE não conta com proteção do FGC; o CDB elegível entra no cálculo do limite e o COE permanece exposição ao emissor ([FGC — limites de cobertura](https://www.fgc.org.br/sobre-garantia-fgc), [B3 — COE sem proteção do FGC](https://borainvestir.b3.com.br/tipos-de-investimentos/o-que-sao-titulos-privados/)). O limite ordinário é de até R$ 250 mil por CPF/CNPJ e instituição ou conglomerado, com teto global de R$ 1 milhão em quatro anos para garantias pagas, observadas as regras de elegibilidade.

**Problema de modelagem:** “controlador final” não basta. Para CDB/COE importa o emissor; para debênture, a companhia emissora e garantias; para CRI/CRA, patrimônio separado, devedores/lastro e estrutura; para fundo, ativos subjacentes. Custodiante e distribuidor não devem virar devedores por associação.

**Redesenho:** grafo com `issued_by`, `obligor`, `guaranteed_by`, `belongs_to_conglomerate`, `backed_by`, `administered_by` e `custodied_at`. Calcular separadamente: exposição bruta, elegível ao FGC, estimativa coberta, não coberta, subordinada e look-through.

**Insight aprovado:** “O conglomerado X concentra 31% do patrimônio. Apenas R$ Y está em instrumentos potencialmente elegíveis ao FGC; o COE de R$ Z e a debênture de R$ W permanecem exposição não coberta. O risco econômico não está no número de produtos, mas no mesmo obrigado final.”

### 11. Passivos Ocultos / Negative Carry — manter, mas decompor o sangramento

**O que há de útil:** mostrar que uma posição aparentemente pequena pode consumir caixa continuamente e produzir chamada de margem. É especialmente relevante para tomadores de ativos, futuros, termo e saldos financiados.

**Problema atual:** `naturezaEmprestimo=Tomador` não fornece o custo. Faltam taxa, prazo, comissão, tributo, custo de funding, ajuste diário, proventos a reembolsar e variação da margem. Saldo negativo também não deve ser somado a aluguel como se fosse o mesmo passivo.

**Redesenho:** decompor carry observado/contratual:

\[
Carry = Juros + Aluguel + Comissões + Reembolsos + Custo\ de\ margem - Receitas\ da\ posição
\]

Exibir taxa diária/mensal, valor até o vencimento, sensibilidade a taxa e condições de aceleração. Para futuros, separar carry de ajuste a mercado; para short, separar custo do aluguel da perda por alta do ativo.

**Insight aprovado:** “A posição vendida equivale a 4% do patrimônio, mas consome R$ X/mês em aluguel e funding. Se a taxa de aluguel dobrar, o custo anual passa de Y% do capital comprometido; a remuneração esperada da tese precisa superar esse patamar apenas para empatar.”

**Teste adversarial:** zerar a taxa de empréstimo deve eliminar essa parcela do carry, sem eliminar o risco de mercado da posição.

### 12. Delisting e Eventos Societários — alto valor como inteligência de evento

**O que há de útil:** combinar posição, evento oficial, prazos operacionais e contratos de empréstimo. Uma OPA, subscrição ou grupamento pode exigir ação dentro de uma janela que não aparece na visão patrimonial. A OPA oferece aos acionistas a possibilidade de alienação em condições definidas e deve ser tratada com dados oficiais do evento ([B3 — OPAs](https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/leiloes/opas/)).

**Problema atual:** `preço cronicamente abaixo de R$ 1` não antecipa delisting. Pode haver determinação para grupamento ou outras medidas, mas preço isolado não prova fechamento de capital. `recuperacaoJudicial` também não é sinônimo de evento iminente de saída da bolsa.

**Redesenho:** feed oficial versionado de OPA, incorporação, cisão, grupamento, subscrição, conversão, vencimento de direito, recuperação judicial e cancelamento de registro. O insight cruza quantidade elegível, custo/valor, empréstimo, bloqueio e prazo operacional.

**Insight aprovado:** “Há OPA anunciada para o ativo X. Metade da posição está emprestada e o recall pode consumir dois ou três pregões; a janela operacional restante é de N dias. O risco principal é perder a capacidade de habilitação, não prever o preço da ação.”

### 13. Ativos Desidratados / Zombie Assets — útil como higiene, fraco como insight

**O que há de útil:** detectar direitos a expirar, frações, posições residuais e ativos sem negociação que geram obrigação operacional.

**Problema atual:** valor inferior a R$ 50 não significa que vender é racional. Pode haver spread, ausência de comprador, custo superior ao valor, direito futuro, amortização pendente ou necessidade de manter memória fiscal. “Reduzir dor de cabeça no IR” é genérico; a liquidação pode criar nova apuração.

**Redesenho:** classificar o motivo do residual: fração, direito, evento, amortização, inatividade, suspensão ou pó econômico. Estimar valor realizável líquido, prazo e consequência de não agir.

**Saída adequada:** alerta operacional: “Direito de subscrição no valor indicativo de R$ X expira em 5 dias; após a data pode perder valor.” Posição residual sem prazo ou impacto não deve ocupar o top 5.

### 14. Barbell Extreme — não inferir estratégia pela forma da carteira

**O que há de útil:** medir a distribuição entre ativos defensivos e exposições de cauda pode revelar uma geometria incomum.

**Erro epistemológico:** a fotografia não mostra se a barra foi desenhada deliberadamente, se é carteira incompleta ou se resultou de compras aleatórias. “DNA estratégico” é antropomorfização. Além disso, classificar “blue chip” como risco intermediário e toda posição extrema como Talebiana é uma simplificação inadequada.

**Redesenho:** produzir um diagnóstico neutro e uma pergunta de confirmação. Exemplo: “82% está em ativos de baixa sensibilidade nos cenários definidos e 18% responde por 93% da perda de cauda; essa assimetria é intencional?”. Se o investidor confirmar objetivo barbell, avaliar se a construção cumpre o objetivo; se negar, gerar hipótese de desalinhamento.

**Parecer:** remover do gerador autônomo de insights no MVP. Pode voltar como **lente de estrutura de risco confirmada pelo usuário**.

### 15. Fricção de Corretagem / Ticket Erosion — exige histórico de execução

**O que há de útil:** custos pequenos e repetidos podem destruir retorno, especialmente quando spread e impacto são grandes em relação ao ticket.

**Problema atual:** uma posição fracionária pequena não prova que houve execução ruim nem corretagem relevante. A posição pode ser fração de evento corporativo, compra recorrente eficiente ou resultado de venda parcial. Algumas corretoras cobram corretagem zero; spread e emolumentos continuam existindo, mas precisam de ordens, execuções e quotes.

**Redesenho:** usar histórico de ordens e mercado para medir custo realizado, como implementation shortfall:

\[
Custo = sinal \times (Preço_{execução}-Midpoint_{chegada}) \times quantidade + tarifas
\]

Agrupar por estratégia e periodicidade; comparar execução real com alternativa contrafactual, sem assumir que tickets maiores seriam sempre melhores.

**Insight aprovado:** “Em 34 compras recorrentes, 1,7% do capital foi consumido por spread, emolumentos e desvio de execução; 78% do custo veio de seis ordens em horários de baixa liquidez.” Sem histórico, retornar `INSUFFICIENT_DATA`.

### 16. YTM Presumido — método original é matematicamente impossível

**O que há de útil:** traduzir preço e fluxos futuros em taxa de retorno até o vencimento é valioso para planejamento.

**Erro determinante:** `valorAtualizado + quantidade + vencimento` não identifica taxa original. Infinitas combinações de cupom, indexador, preço de aquisição, amortizações e spreads podem produzir o mesmo valor atual. Mesmo o YTM atual exige todos os fluxos contratuais e um preço válido; a taxa contratada original exige preço/data de aquisição ou registro equivalente.

**Redesenho:**

- **retorno contratado/original:** preço de compra, data, fluxo completo, taxas e eventos;
- **YTM atual:** preço de mercado, settlement, fluxo remanescente e convenção;
- **fluxo futuro contratual:** projeções por cenário de indexador, explicitando que pós-fixado não tem retorno nominal conhecido.

Resolver numericamente:

\[
Preço = \sum_{t=1}^{T}\frac{Fluxo_t}{(1+y)^{\tau_t}}
\]

**Parecer:** proibir a palavra “presumido” para preencher dados ausentes. O motor deve declarar qual taxa calculou, quais fluxos usou e se existe solução única.

### 17. Contradição Operacional / Hedge Overlap — renomear para Integridade do Hedge

**O que há de útil:** duas posições podem se anular economicamente enquanto mantêm custos, margem e risco de base. Esse é um insight genuinamente relacional.

**Problema atual:** estar comprado em ETF e vendido em futuro não é contradição; frequentemente é um hedge intencional, temporário ou incompleto. Desmontar as duas pontas pode aumentar muito o risco.

**Redesenho:** calcular exposição bruta, exposição líquida por fator, beta/ratio do hedge, basis, vencimento, rolagem, custos e cenários. Pedir ou recuperar o objetivo declarado: proteção total, parcial, arbitragem, transição ou desconhecido.

**Insight aprovado:** “O futuro reduz 86% do beta de bolsa, mas vence 18 meses antes do horizonte declarado e deixa concentração em bancos fora do hedge. A proteção funciona para o índice, não para o risco específico dominante.”

**Insight de custo:** “As pontas mantêm exposição líquida próxima de zero há 90 dias, mas acumulam R$ X em rolagem e taxas; confirme se a neutralidade ainda é necessária.”

### 18. Concentração de Custódia — não confundir acesso operacional com perda dos ativos

**O que há de útil:** uma única instituição pode ser ponto de falha para envio de ordens, saque, autenticação ou atendimento num momento crítico.

**Problema atual:** “se o app cair, a liquidez total cai junto” é exagero. A central depositária e os agentes de custódia têm papéis distintos; a B3 oferece consolidação e portabilidade entre instituições. Ativos custodiados, saldo de caixa e exposição creditícia à instituição também são riscos diferentes ([B3 — Área do Investidor](https://www.b3.com.br/pt_br/produtos-e-servicos/central-depositaria/canal-com-investidores/area-do-investidor/), [B3 — Portabilidade](https://www.b3.com.br/pt_br/produtos-e-servicos/central-depositaria/canal-com-investidores/portabilidade-de-investimentos/)).

**Redesenho:** separar:

- acesso operacional para negociação;
- dependência de canal/autenticação;
- caixa ou crédito exposto à instituição;
- custódia escritural/centralizada;
- prazo e elegibilidade de portabilidade.

**Parecer:** alerta de resiliência P3. Só ganha prioridade se houver derivativos, chamadas de margem, evento com prazo curto ou histórico de indisponibilidade verificável.

### 19. Alavancagem Sintética — prioritária, mas margem não é exposição

**O que há de útil:** mostrar que capital bloqueado é apenas garantia; a variação econômica incide sobre nocional muito maior.

**Problema atual:** “expandir a margem para o valor nocional” sugere uma transformação que não existe. Margem é calculada por risco e portfólio; não determina o nocional. Nocional, delta equivalente, perda em cenário e margem requerida são quatro medidas diferentes.

**Redesenho:**

- futuros: \(Nocional = contratos \times multiplicador \times preço\);
- opções: nocional de referência e \(Delta\ equivalente = Nocional \times delta\);
- estruturas não lineares: gamma/vega e payoff por cenário;
- risco de liquidez: variação de margem e capacidade de atender ajustes.

**Insight aprovado:** “R$ 5 mil de margem suportam R$ 150 mil de nocional, mas a exposição delta atual é R$ 92 mil. Um choque de -8% combinado com alta de volatilidade produz perda estimada de R$ X e margem adicional de R$ Y; o segundo valor é o risco de caixa.”

**Teste adversarial:** aumentar margem depositada sem mudar contratos não pode alterar o nocional ou delta; apenas a folga de liquidez.

### 20. ESG e Contágio Macro — são duas lentes incompatíveis no mesmo item

**O que há de útil:** ativos de setores diferentes podem compartilhar drivers econômicos e cair juntos num cenário. Também pode haver desalinhamento com restrições de sustentabilidade declaradas.

**Problema atual:** ESG não é um fator macro único. Taxa de juros, seca, petróleo e câmbio exigem modelos diferentes; “aviação, varejo e construtora vão cair em bloco se a Selic subir” é previsão categórica e ignora repasses, hedge, balanço e regime. Clusterizar setores por narrativa cria correlação imaginária.

**Redesenho A — crowding de fatores macro:** mapear sensibilidades históricas e estruturais, testar cenários e estabilidade; produzir contribuição por fator, não previsão. Exemplo: “Três setores diferentes explicam 64% da perda no cenário de juro real +200 bps.”

**Redesenho B — alinhamento de mandato ESG:** exigir preferência/mandato do investidor, taxonomia, controvérsias e qualidade da fonte; mostrar exposição e incerteza. Sem preferência declarada, isso é informação, não inadequação.

**Parecer:** P2. Começar por cenários macro específicos e auditáveis; ESG entra como módulo separado.

---

## 6. Protocolo revisado de exploração de insights

### Etapa 0 — Contrato epistêmico

Antes de calcular, registrar:

- `as_of` da posição e de cada fonte;
- universo coberto e patrimônio possivelmente externo;
- perguntas que os dados podem responder;
- perguntas proibidas por insuficiência de dados;
- modo de saída: informativo, educacional, cenário ou recomendação autorizada.

### Etapa 1 — Ingestão sem perda semântica

Nunca preencher ausência econômica com zero. Para cada campo: valor, estado, fonte, data, método, unidade e confiança. Validar reconciliação de quantidade, valor, duplicidade, moeda, conta, ativo e natureza de posição.

### Etapa 2 — Modelo canônico e reconciliação

Construir lotes/posições/contratos separados. Não somar posição própria, doadora, tomadora, bloqueada e garantia como se fossem estoques independentes; identificar direitos, obrigações e disponibilidade.

### Etapa 3 — Enriquecimento e teia financeira

Resolver instrumento, emissor, obrigado, conglomerado, garantidor, subjacente, índice, fundo, fator, fluxo, regime tributário, evento e custodiante. Toda aresta carrega fonte, validade e confiança.

### Etapa 4 — Roteador de lentes por elegibilidade

Em vez de executar as 20 lentes sempre, cada lente declara:

- pré-condições de dados;
- universo de produtos;
- cálculo mínimo;
- condições de rejeição;
- evidência obrigatória;
- data máxima aceitável das fontes.

O motor cria candidatos apenas quando as pré-condições passam. A LLM não inventa o candidato.

### Etapa 5 — Cálculo de fatos, cenários e contrafactuais

O motor calcula fatos e cenários. Para cada candidato, gera pelo menos um contrafactual: sem look-through, com cobertura integral, sem choque, com outro horizonte ou com perfil desconhecido. A LLM recebe os resultados, não refaz contas.

### Etapa 6 — Contexto mínimo sob demanda

Se uma única informação puder alterar materialmente a conclusão, perguntar de modo progressivo. Exemplos: necessidade de caixa, horizonte do hedge, intenção de manter até vencimento. Não aplicar um questionário completo para toda análise, mas também não inferir perfil pela posição.

### Etapa 7 — Síntese da LLM

A LLM conecta evidências e produz linguagem. Ela pode sugerir explicações alternativas, mas cada frase deve apontar para evidência ou premissa. Não deve calcular valores críticos nem alterar severidade determinística.

### Etapa 8 — Crítica estruturada

Executar uma segunda passagem com um contrato observável:

1. Qual é a explicação alternativa mais forte?
2. Qual dado faltante pode inverter a conclusão?
3. O fato continua correto para outro perfil?
4. A severidade muda ou o insight deixa de existir?
5. Há recomendação disfarçada?
6. Alguma frase prevê mercado sem modelo?

Guardar respostas resumidas e códigos de decisão; não exigir exposição de cadeia de pensamento.

### Etapa 9 — Gates e ranking

Aplicar gates antes do score:

- integridade de dados;
- suficiência causal;
- materialidade mínima;
- confiança mínima;
- não redundância;
- conformidade de linguagem.

Só depois ranquear. Não colapsar tudo num score opaco: manter eixos separados de **impacto**, **urgência**, **confiança**, **personalização**, **não-obviedade** e **acionabilidade**. Um score composto pode ordenar, mas não deve permitir que grande impacto compense confiança muito baixa.

Uma fórmula inicial, calibrável por evidência, pode ser:

\[
Prioridade = (0{,}30M + 0{,}20U + 0{,}20A + 0{,}15N + 0{,}15R)
             \times C \times Q - P_{premissas} - P_{redundância}
\]

onde \(M\)=materialidade, \(U\)=urgência, \(A\)=acionabilidade, \(N\)=não-obviedade, \(R\)=relevância ao objetivo, \(C\)=confiança e \(Q\)=qualidade dos dados. Antes da fórmula, exigir `C` e `Q` acima do piso da lente. Os pesos são hipótese de produto a ser validada; não fundamento financeiro universal.

### Etapa 10 — Entrega e aprendizado

Exibir no máximo cinco itens, porém preservar também `no finding` e rejeições para auditoria. Coletar feedback do investidor e revisão de especialista sem transformar clique em verdade financeira.

---

## 7. Contrato de saída auditável

```json
{
  "insight_id": "INS-20260825-001",
  "as_of": "2026-08-25T00:00:00-03:00",
  "lens_id": "issuer_protection_graph_v2",
  "status": "approved",
  "output_mode": "educational_scenario",
  "decision_question": "Quanto do patrimônio depende do mesmo obrigado econômico?",
  "facts": [
    {
      "statement": "31% do patrimônio está ligado ao conglomerado X",
      "evidence_ids": ["CALC-81", "SRC-FGC-20260825"],
      "confidence": "high"
    }
  ],
  "inference": "A diversidade nominal de produtos não reduz essa concentração econômica.",
  "scenarios": [],
  "assumptions": ["A carteira fornecida representa todo o patrimônio financeiro analisado"],
  "counter_hypotheses": [
    "Parte da exposição pode possuir garantia específica ainda não integrada"
  ],
  "missing_data": [],
  "impact": "high",
  "urgency": "low",
  "confidence": "high",
  "profile_sensitivity": "medium",
  "action_options": [
    {
      "option": "Revisar a documentação de garantias e o limite por conglomerado",
      "tradeoffs": "Não implica vender; pode confirmar ou reduzir o gap identificado"
    }
  ],
  "limitations": "Não estima probabilidade de default.",
  "source_versions": ["FGC@2026-08-25", "position@2026-08-25"]
}
```

**Correção do modelo original:** “ação mapeada” não deve ser uma ordem curta como “role opções” ou “troque o colateral”. Deve apresentar opções, pré-condições, custos e o que muda em cada alternativa.

---

## 8. Novas lentes com maior potencial de criação intelectual

As lentes abaixo não são apenas novos agrupamentos. Cada uma conecta pelo menos duas dimensões e responde a uma pergunta decisória.

### 8.1 Contribuição marginal de risco

**Pergunta:** qual posição pequena altera desproporcionalmente o risco total?  
**Mecanismo:** covariância/fatores e `Marginal Contribution to Risk`, com janelas e cenários.  
**Valor:** mostra por que uma posição de 5% pode responder por 20% do risco, algo que peso nominal não revela.  
**Dados:** séries de retorno/fatores; não viável apenas com snapshot.

### 8.2 Concentração de motores de caixa

**Pergunta:** quantas posições dependem do mesmo fluxo econômico, mesmo com emissores diferentes?  
**Mecanismo:** grafo de receita/custo/commodity/juro/crédito e cenários.  
**Valor:** vai além de setor. Bancos, varejo e construção podem responder ao mesmo ciclo de crédito por canais diferentes.  
**Cuidado:** apresentar como sensibilidade de cenário, nunca como “todos vão cair”.

### 8.3 Abismo de reinvestimento

**Pergunta:** uma parcela relevante vence na mesma janela e terá de ser reinvestida sob uma taxa desconhecida?  
**Mecanismo:** ladder de principal/cupons, concentração por janela, cenários de reinvestimento.  
**Valor:** a carteira pode ter baixa duration hoje, mas risco alto de renovar 60% do capital no mesmo mês.  
**Dados:** fluxos contratuais; viável no MVP enriquecido.

### 8.4 Gap de inflação pessoal

**Pergunta:** os fluxos que financiam uma meta preservam poder de compra compatível com ela?  
**Mecanismo:** separar fluxos nominais, CDI, IPCA e exposição real; comparar com meta indexada.  
**Valor:** “ter IPCA+” não significa que a parcela e o prazo cobrem a necessidade.  
**Dados:** objetivo/horizonte e fluxos; requer contexto mínimo.

### 8.5 Fragilidade de sequência de retornos

**Pergunta:** retiradas no início de um drawdown podem comprometer uma carteira de acumulação/aposentadoria?  
**Mecanismo:** simulação determinística de trajetórias e saques, sem prometer probabilidades quando o modelo não as suporta.  
**Valor:** duas carteiras com retorno médio igual podem sustentar resultados muito diferentes sob retiradas.  
**Dados:** plano de retiradas, horizonte e cenários; fase posterior.

### 8.6 Mapa de optionalidade embutida

**Pergunta:** quem possui o direito de alterar o fluxo — investidor, emissor ou contraparte?  
**Mecanismo:** calls, puts, barreiras, caps, floors, pré-pagamento, resgate antecipado e conversão.  
**Valor:** revela que “capital protegido” ou “taxa alta” pode ter upside limitado, call do emissor ou liquidez inexistente.  
**Dados:** DIE/termos completos do produto; muito relevante para COE e crédito estruturado.

### 8.7 Compensação insuficiente pelo risco assumido

**Pergunta:** o prêmio recebido compensa concentração, liquidez, subordinação e garantia?  
**Mecanismo:** spread/taxa contra comparáveis, curva, custos, garantia e cenários de perda; não estimar default sem modelo.  
**Valor:** transforma “CDB a 115% do CDI” em comparação econômica, não em ranking de taxa.  
**Dados:** preço/taxa de aquisição, comparáveis de mercado e estrutura de crédito.

### 8.8 Wrong-way risk de colateral

**Pergunta:** a garantia perde valor justamente no cenário em que a obrigação cresce?  
**Mecanismo:** cenários conjuntos entre posição e colateral.  
**Valor:** uma garantia formalmente elegível pode ser economicamente frágil se correlacionada ao risco coberto.  
**Dados:** composição de margem, fatores e cenários; extensão natural da lente 5.

### 8.9 Fronteira de liquidação pós-imposto

**Pergunta:** qual combinação atende uma necessidade de caixa minimizando imposto, perda de proteção e risco residual?  
**Mecanismo:** otimizador determinístico com lotes fiscais, custos, liquidez, restrições e cenários.  
**Valor:** não recomenda “vender o ativo mais líquido” de forma míope; compara consequências no portfólio restante.  
**Dados:** lotes, custos, regras fiscais, necessidade e autorização de uso.

### 8.10 Orçamento de incerteza dos dados

**Pergunta:** quanto da decisão depende de dados estimados, defasados ou desconhecidos?  
**Mecanismo:** propagar intervalos e confiança pelos cálculos; identificar conclusões que mudam de sinal.  
**Valor:** evita top 5 preciso na aparência e frágil na origem.  
**Dados:** lineage e estados de qualidade; viável desde o MVP.

### 8.11 Simplificação econômica da carteira

**Pergunta:** existem várias posições que replicam quase a mesma exposição, elevando custo e complexidade sem benefício mensurável?  
**Mecanismo:** similaridade de payoff/fatores, custos totais, tributação e restrições.  
**Valor:** diferente de “falsa diversificação”: busca configurações economicamente equivalentes e explicita o custo de manter complexidade.  
**Cuidado:** simplificar pode realizar imposto ou remover optionalidade; não sugerir desmonte sem simulação.

### 8.12 Proteção que falha fora do cenário central

**Pergunta:** o hedge continua funcionando com gap, mudança de correlação, base, vencimento ou volatilidade?  
**Mecanismo:** cenários multidimensionais e degradação de hedge.  
**Valor:** uma proteção pode parecer perfeita no delta atual e falhar numa mudança grande.  
**Dados:** contratos completos e superfície/cenários; evolução da lente 17.

---

## 9. Teia de conhecimento financeiro

Uma taxonomia plana por produto não é suficiente. O motor precisa de um grafo temporal e versionado.

### 9.1 Nós principais

| Domínio | Nós |
|---|---|
| Investidor | Investidor, perfil, objetivo, necessidade de caixa, passivo, restrição |
| Posição | Conta, lote, posição, contrato, saldo, garantia, bloqueio |
| Instrumento | Instrumento, classe, série, fluxo, indexador, moeda, vencimento, optionalidade |
| Risco jurídico | Emissor, obrigado, conglomerado, garantidor, devedor, patrimônio separado |
| Look-through | Fundo, classe de fundo, ETF, índice, subjacente, participação |
| Mercado | Preço, curva, volatilidade, liquidez, fator, cenário, correlação |
| Operacional | Custodiante, participante, canal, settlement, empréstimo, recall |
| Fiscal | Regime, lote fiscal, alíquota, evento tributável, isenção |
| Eventos | OPA, subscrição, grupamento, amortização, conversão, recuperação, vencimento |
| Evidência | Fonte, versão, validade, observação, cálculo, confiança |

### 9.2 Arestas que evitam conclusões erradas

- `INVESTOR holds POSITION`
- `POSITION represents INSTRUMENT`
- `INSTRUMENT issued_by ISSUER`
- `ISSUER belongs_to CONGLOMERATE`
- `INSTRUMENT obligor OBLIGOR`
- `INSTRUMENT guaranteed_by GUARANTOR`
- `INSTRUMENT backed_by COLLATERAL_POOL`
- `FUND holds UNDERLYING`
- `ETF tracks INDEX`
- `POSITION pledged_for OBLIGATION`
- `LOAN_CONTRACT lends_or_borrows POSITION`
- `INSTRUMENT sensitive_to FACTOR`
- `CASH_FLOW due_before NEED`
- `LOT taxed_by TAX_RULE`
- `EVENT affects INSTRUMENT`
- `OBSERVATION supports CALCULATION`

**Por que isso importa:** sem tipos de aresta, o sistema pode tratar custodiante como emissor, administrador como devedor, controlador como garantidor ou patrimônio separado como dívida da securitizadora. O grafo não é luxo arquitetural; é uma defesa contra falsos vínculos financeiros.

### 9.3 Requisitos temporais

Cada nó e aresta externa deve conter `valid_from`, `valid_to`, `observed_at`, `source_id` e `confidence`. Composição de fundo, grupo econômico, regra tributária, haircut, série de derivativo e evento mudam. Um grafo sem tempo cria look-through e garantias historicamente incorretos.

---

## 10. Harness recomendado: inteligência como processo, não como prompt

O bom resultado observado em outro harness provavelmente não decorreu apenas do modelo. A criação de scripts, seleção dos dados e iteração indicam que houve **decomposição adaptativa do problema**. O equivalente controlável para o produto é uma máquina de estados com ferramentas, não um único prompt enorme.

### 10.1 Fluxo lógico do MVP

1. **Profiler de dados:** inventaria produtos, contratos, lacunas e cobertura.
2. **Roteador de lentes:** escolhe somente lentes elegíveis e potencialmente materiais.
3. **Planejador de evidências:** define os cálculos e enriquecimentos necessários por candidato.
4. **Ferramentas determinísticas:** executam look-through, cash-flow, FGC, payoff, DV01, liquidez e grafo.
5. **Gerador de candidatos:** formula a relação decisória com IDs de evidência.
6. **Crítico financeiro:** busca explicação alternativa, perfil sensível e dado inversor.
7. **Verificador:** reprova conta refeita pela LLM, fonte vencida, causalidade indevida e linguagem de recomendação.
8. **Ranker:** aplica gates, deduplica por mecanismo de risco e seleciona até cinco.
9. **Narrador:** ajusta a linguagem ao conhecimento do investidor sem mudar os fatos.

Isso pode ser implementado com um único modelo em chamadas separadas e estado explícito. Não é necessário criar muitos “agentes autônomos” no MVP; as responsabilidades devem ser separadas no código e no contrato.

### 10.2 Tools mínimas

| Tool | Responsabilidade |
|---|---|
| `resolve_instrument` | Identidade, classe, série, termos e fonte |
| `portfolio_lookthrough` | Exposição direta/indireta e cobertura |
| `issuer_protection_graph` | Emissor, obrigado, conglomerado e garantias |
| `fixed_income_cashflows` | Fluxos, duration, DV01 e cenários |
| `derivative_payoff` | Pernas, payoff, Greeks, nocional e cenários |
| `liquidity_timeline` | Caixa líquido por horizonte e cenário |
| `collateral_efficiency` | Crédito reconhecido, haircut, limite e folga |
| `data_uncertainty` | Frescor, método, cobertura e propagação de incerteza |
| `tax_lot_simulator` | Apenas quando lotes e regime estiverem completos |
| `event_impact` | Evento oficial, prazos e posição afetada |

### 10.3 Regra de parada

O loop termina quando:

- não há candidato novo material;
- todos os candidatos passaram ou falharam nos gates;
- o orçamento de tool calls foi atingido;
- um dado essencial exige pergunta ao investidor;
- a confiança caiu abaixo do mínimo.

Não continuar “pensando” até inventar cinco itens. Uma carteira simples pode ter zero ou dois insights válidos.

---

## 11. Avaliação e evidências

### 11.1 Baselines necessários

Comparar a solução contra:

1. dashboard de posição e agregações;
2. regras determinísticas sem LLM;
3. LLM em chamada única;
4. pipeline completo com ferramentas e crítico.

Sem baseline, um texto elegante pode parecer inteligente mesmo quando apenas verbaliza a tabela.

### 11.2 Rubrica de especialista

Cada item deve ser avaliado, de 0 a 4, em:

- correção factual e matemática;
- rastreabilidade da evidência;
- não-obviedade em relação ao dashboard baseline;
- materialidade;
- relevância para uma decisão;
- robustez a explicações alternativas;
- calibração da confiança;
- clareza e adequação da linguagem;
- ausência de recomendação indevida.

**Gate:** qualquer nota 0 em correção, evidência ou conformidade reprova o insight, independentemente da média.

### 11.3 Testes adversariais e metamórficos

| Teste | Resultado esperado |
|---|---|
| Converter preço nulo em zero | Pipeline deve falhar/rejeitar, nunca aceitar silenciosamente |
| Dobrar todas as posições | Valores absolutos dobram; pesos e mecanismos relativos permanecem |
| Dividir o mesmo emissor em duas corretoras | Risco por emissor não diminui; risco operacional pode mudar |
| Substituir ETF pelos mesmos componentes | Exposição look-through permanece equivalente |
| Adicionar cobertura exata a call vendida | Classificação naked desaparece |
| Depositar mais margem sem mudar contratos | Nocional/delta não mudam; folga de caixa muda |
| Mesma carteira, dois objetivos | Fatos iguais; relevância/severidade contextual pode mudar |
| Retirar lotes fiscais | Lente tributária retorna insuficiência, sem presumir data |
| Fonte externa vencida | Confiança cai ou candidato é suspenso |
| Carteira simples e bem distribuída | É válido retornar nenhum insight material |

### 11.4 Métricas de produto

- `supported_claim_rate`: frases com evidência rastreável;
- `calculation_error_rate`;
- `false_critical_alert_rate`;
- `abstention_precision`: qualidade das recusas por insuficiência;
- `dashboard_novelty_rate`: itens que superam o baseline de agregação;
- `expert_decision_relevance`;
- `profile_flip_consistency`: fatos estáveis e severidade coerente entre perfis;
- `duplicate_mechanism_rate` no top 5;
- latência, custo e chamadas por insight aprovado.

Feedback “gostei/não gostei” não mede verdade financeira. Deve complementar, não substituir, revisão de domínio e casos dourados.

---

## 12. Priorização recomendada para o MVP

### 12.1 Núcleo sem histórico de movimentação

Implementar primeiro:

1. **qualidade e incerteza de avaliação** — bloqueia conclusões inválidas;
2. **look-through e concentração econômica**;
3. **emissor, obrigado, conglomerado e cobertura/garantia**;
4. **sensibilidade de renda fixa: fluxos, duration, DV01 e cenários**;
5. **derivativos: payoff, cobertura, nocional, delta e risco de margem**;
6. **integridade de hedge**;
7. **vencimentos e abismo de reinvestimento**.

Essas lentes podem produzir valor real com fotografia da posição **desde que** termos e metadados estejam disponíveis.

### 12.2 Um pequeno acréscimo que aumenta muito o valor

Adicionar contexto progressivo, não um perfil inferido:

- horizonte principal;
- necessidade de caixa por janela;
- finalidade da carteira;
- perda temporária tolerável declarada;
- intenção de manter títulos até vencimento;
- objetivo de hedges/derivativos quando existir.

Com isso, cachoeira de liquidez e ALM deixam de ser tabelas e passam a responder a decisões.

### 12.3 Adiar até haver os dados corretos

- tributação: lotes, custos e regime;
- execução/fricção: ordens, negócios e quotes;
- comportamento/performance: histórico de movimentação;
- beta cambial e macro: séries e modelos validados;
- ESG: preferência e taxonomia;
- estratégia barbell: confirmação explícita;
- YTM original: preço/data de aquisição e fluxo completo.

### 12.4 Ordem de implementação técnica

**Sprint 1 — verdade dos dados:** estados de ausência, modelo canônico, lineage e reconciliação.  
**Sprint 2 — grafo de instrumento/emissor:** look-through, obrigado e garantia.  
**Sprint 3 — motores financeiros:** renda fixa e derivativos com testes dourados.  
**Sprint 4 — candidatos e gates:** contratos de lentes, abstention e ranking.  
**Sprint 5 — síntese/critique:** linguagem, contrahipóteses e perfil progressivo.  
**Sprint 6 — avaliação:** baseline, especialistas, adversarial e métricas.

---

## 13. Critério final para aprovar um insight

Um candidato só deve chegar ao investidor se todas as respostas forem “sim”:

1. Há um fato material calculado ou um evento verificável?
2. A relação não é apenas uma reformulação de peso, saldo ou contagem?
3. A inferência está sustentada pelos dados disponíveis?
4. A explicação alternativa mais forte foi considerada?
5. As premissas que mudam a conclusão estão explícitas?
6. A confiança é compatível com a força da linguagem?
7. O item responde a uma pergunta decisória?
8. A ação, se houver, apresenta opções e trade-offs?
9. A recomendação está dentro do modo e do escopo regulatório?
10. Um especialista consegue reproduzir o caminho até as evidências?

Se a resposta 1, 3, 6, 9 ou 10 for “não”, o candidato deve ser rejeitado, não reescrito.

---

## 14. Conclusão

A maior oportunidade não é ampliar de 20 para 40 lentes. É transformar lentes em **testes de hipóteses com contratos de evidência**. O protocolo revisado deve aceitar que:

- uma fotografia suporta diagnósticos fortes de estrutura, exposição, contratos e cenários;
- não suporta intenção, comportamento, causalidade ou recomendação personalizada sem contexto adicional;
- o motor determinístico fornece verdade calculável;
- a teia financeira fornece relações;
- a LLM formula síntese e contrahipóteses;
- o crítico e os gates impedem que eloquência vire falsa inteligência.

O melhor insight do MVP não será o mais sofisticado linguisticamente. Será aquele que um especialista consegue reproduzir, que o investidor não percebe numa lista de posições e que muda uma decisão sem esconder a incerteza.

---

## 15. Fontes oficiais e normativas consultadas

- [CVM — Resolução CVM 30 consolidada (suitability)](https://conteudo.cvm.gov.br/export/sites/cvm/legislacao/resolucoes/anexos/001/resol030consolid.pdf)
- [CVM — Dados Abertos: Composição e Diversificação das Aplicações (CDA)](https://dados.cvm.gov.br/dataset/fi-doc-cda)
- [FGC — limites e condições gerais de cobertura](https://www.fgc.org.br/sobre-garantia-fgc)
- [B3 — garantias aceitas pela Câmara](https://www.b3.com.br/pt_br/produtos-e-servicos/compensacao-e-liquidacao/clearing/administracao-de-riscos/garantias/garantias-aceitas/)
- [B3 — empréstimo de ativos: prazos de devolução](https://www.b3.com.br/pt_br/produtos-e-servicos/emprestimo-de-ativos/renda-variavel/s_pergfre/)
- [B3 — transição anunciada de D+2 para D+1](https://www.b3.com.br/pt_br/noticias/liquidacao-d-1.htm)
- [B3 — OPAs](https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/leiloes/opas/)
- [B3 — Área do Investidor](https://www.b3.com.br/pt_br/produtos-e-servicos/central-depositaria/canal-com-investidores/area-do-investidor/)
- [B3 — Portabilidade de Investimentos](https://www.b3.com.br/pt_br/produtos-e-servicos/central-depositaria/canal-com-investidores/portabilidade-de-investimentos/)
- [Receita Federal — Perguntas e Respostas IRPF 2026](https://www.gov.br/receitafederal/pt-br/centrais-de-conteudo/publicacoes/perguntas-e-respostas/dirpf/p-r-irpf-2026-v1-00-2026-04-23.pdf)
- [Banco Central — plano contábil com valor de mercado de COE](https://www.bcb.gov.br/content/estabilidadefinanceira/supervisao/Fun%C3%A7%C3%B5es%20de%20Contas%20Novo%20Padr%C3%A3o.pdf)
