# Ledger de ajustes, autocrítica e validação adversarial — V5

## Lote 0 — congelamento e inventário

- **Esperado:** preservar a baseline e mapear toda seção antes de mover conteúdo.
- **Observado:** SHA-256 da baseline confirmado; 171 títulos identificados; 171 classificados no inventário.
- **Autocrítica:** títulos dentro de blocos poderiam contaminar a hierarquia.
- **Validação adversarial:** o parser ignora cercas; os dois manuscritos foram inspecionados novamente depois da geração.
- **Veredito:** `PASS`.

## Lote 1 — arquitetura em dois volumes

- **Esperado:** tornar real a promessa das rotas sem apagar profundidade.
- **Observado:** livro reduzido de 136 para 66 páginas; a primeira geração do workbook teve 94 páginas e preservou o conteúdo operacional; baseline permanece disponível. Os refinamentos tipográficos dos Lotes 6 e 7 redistribuíram esse conteúdo para 96 páginas.
- **Autocrítica:** a redução poderia transformar o livro em resumo superficial.
- **Validação adversarial:** nove artefatos continuam definidos; o microfluxo Contract → Assertion → Eval → Evidence permanece completo; estudo assíncrono e governança continuam no livro.
- **Veredito:** `PASS`, condicionado a teste futuro com leitores representativos.

## Lote 2 — reordenação e microcoesão

- **Esperado:** conceito antes de decisão; problema → modelo → técnica → execução → evidência.
- **Observado:** Parte III agora introduz mecanismo/ontologia, quatro movimentos, catálogo e microfluxo antes do estudo integrado.
- **Autocrítica:** uma ponte curta poderia ocultar dependências que antes apareciam em exemplos longos.
- **Validação adversarial:** checkpoint técnico exige identificar fonte da Assertion, executor da Eval e limite de lineage sem abrir o workbook.
- **Veredito:** `PASS` editorial; validação empírica permanece pendente.

## Lote 3 — resumo e preservação semântica

- **Esperado:** condensar a execução sem alterar definições materiais.
- **Observado:** HOT/WARM/COLD continua separado de autoridade; progressive disclosure permanece não garantístico; `202` continua separado de durabilidade; SignalR continua restrito ao estudo.
- **Self-check:** cada resumo foi comparado com as definições canônicas e com o Claim Ledger.
- **Validação adversarial:** procuradas universalizações (`sempre`, `garante`, cache físico, porcentagem fixa) e inferências de lineage; nenhuma nova universalização foi aceita.
- **Veredito:** `PASS`.

## Lote 4 — estilos de código e tabelas

- **Esperado:** fundo cinza real nos ambientes `Shaded`, padding, contraste e zebra striping sutil.
- **Observado:** `Shaded` foi redefinido para `snugshade`; `CodePanel` e `TableStripe` estão na fonte canônica; renderização confirma faixas e fundo.
- **Autocrítica:** configurar uma cor não prova que o Pandoc a aplicou; striping forte poderia competir com syntax highlighting.
- **Validação adversarial:** páginas com código e tabelas foram abertas em alta resolução; faixas permanecem discretas, headers e regras horizontais continuam presentes.
- **Veredito:** `PASS`.

## Lote 5 — build e paginação

- **Esperado:** dois PDFs A4, sem overflow horizontal, clipping ou callout órfão.
- **Observado:** build duplo XeLaTeX passou; 160 páginas renderizadas; overflows horizontais eliminados.
- **Autocrítica:** o primeiro PDF compilado deixou uma linha de callout isolada no topo da página seguinte.
- **Validação adversarial:** defeito localizado na inspeção visual e callout condensado sem perda da ideia principal; nova renderização exigida antes do pacote final.
- **Veredito:** `PASS` após a nova renderização registrada no Evidence Record.

## Lote 6 — refinamentos visuais finais

- **Esperado:** afastar a curva de retorno da Figura 7.1 do rótulo central e manter todo texto de blocos cercados dentro das margens.
- **Observado:** os controles da curva foram rebaixados em 35 px, equivalentes a aproximadamente 5,1% da altura do diagrama; `fvextra` passou a quebrar linhas e tokens longos em todos os ambientes `Highlighting`.
- **Autocrítica:** corrigir somente o exemplo relatado poderia deixar outros blocos vulneráveis; a nova quebra também poderia alterar paginação ou criar linhas órfãs.
- **Validação adversarial:** os dois PDFs foram recompilados; os logs registram zero `Overfull \hbox`; 161 de 161 páginas foram renderizadas; as duas contact sheets, a Figura 7.1, o bloco “Contexto mínimo executável — expectativa” e páginas vizinhas foram inspecionados. O workbook passou de 94 para 95 páginas sem clipping observado.
- **Self-check semântico:** os Markdown permaneceram byte a byte inalterados; somente SVG, PNG e estilos tipográficos mudaram, portanto nenhuma ideia principal foi resumida ou reescrita.
- **Veredito:** `PASS`.

### Reabertura do Lote 6

- **Contraprova do autor:** uma captura do bloco “Crie a Skill” mostrou a linha `description` sem quebra na saída consultada.
- **Falha de validação:** a checagem anterior demonstrou casos específicos e zero `Overfull \hbox`, mas não mediu geometricamente todos os painéis; o veredito abrangente foi prematuro.
- **Veredito revisado:** `FAIL_PARTIAL`, substituído pelo Lote 7.

## Lote 7 — quebra automática global e prova geométrica

- **Esperado:** qualquer bloco cercado deve quebrar dentro do painel, inclusive texto agrupado pelo syntax highlighting, URLs e identificadores sem espaços.
- **Observado:** `\fvset` aplica `breaklines`, `breakanywhere`, `breaknonspaceingroup` e margem interna direita a toda a família `FancyVerb`; `Highlighting` mantém configuração explícita para preservar `commandchars`.
- **Fundamento técnico:** `fvextra` mantém `breaknonspaceingroup=false` por padrão; a opção foi ativada para permitir quebra de conteúdo não espaçado dentro dos grupos criados pelo highlighter.
- **Autocrítica:** aviso LaTeX ausente não prova que texto não foi cortado; visualização pontual também não cobre o corpus.
- **Validação adversarial:** 271 painéis cinza e 66.210 caracteres monoespaçados foram medidos nas coordenadas dos PDFs; nenhum caractere ultrapassou a borda e a menor folga direita foi 7,97 pt. O bloco enviado, o painel mais estreito de cada volume, as contact sheets e 162 de 162 páginas foram inspecionados; zero páginas inválidas e zero `Overfull \hbox`.
- **Self-check semântico:** os hashes dos dois Markdown permaneceram inalterados; a correção ocorreu apenas na camada TeX.
- **Veredito:** `PASS`.

## Limites não mascarados

- O PDF ainda não é tagged; acessibilidade estrutural permanece decisão de publicação.
- Não foi realizado teste com leitores nesta execução.
- Alegações do Cursor devem ser revalidadas quando a versão/documentação mudar.
- O comportamento de descoberta/lineage precisa ser medido no host; presença de arquivo e resposta correta não bastam.

## Lote 8 — fechamento da release V5

- **Esperado:** promover a RC1 aprovada para `5.0.0` sem deixar artefatos canônicos com nomes, metadados ou instruções divergentes.
- **Observado:** livro, workbook, estilos, scripts, estrutura, validações e handoff usam V5; a baseline Beta 3 permanece isolada em `sources/`.
- **Autocrítica:** trocar somente o nome dos PDFs deixaria scripts, capas e evidências inconsistentes; “pacote completo” também exige continuidade e manifesto, não apenas os dois volumes.
- **Validação adversarial:** build realizado a partir dos scripts finais; 162 páginas renderizadas; nove diagramas inspecionados; 271 painéis medidos; Markdown, JSON, YAML e laboratório passaram; busca por rótulos RC1 fora da história não encontrou artefato canônico remanescente.
- **Veredito:** `PASS_FOR_V5_RELEASE`.
