# Context Engineering

Repositório de conhecimento para times de desenvolvimento que projetam, operam e avaliam o contexto fornecido a sistemas baseados em LLMs e agentes.

O acervo separa **fontes editáveis**, **artefatos de distribuição**, **apresentações**, **evidências de qualidade** e um **laboratório executável**. Essa separação mantém o material fácil de encontrar, reduz alterações acidentais em arquivos binários e permite que o repositório cresça sem transformar a raiz em um catálogo sem organização.

## Conteúdo em destaque

> A V5 Beta 2 é uma edição em revisão externa (`5.0.0-beta.2`), ainda não a edição final publicada.

| Material | Formato | Finalidade |
|---|---|---|
| [Context Engineering para Times de Desenvolvimento V5 Beta 2](docs/ebooks/context-engineering-para-times-de-desenvolvimento-v5-beta2.md) | Markdown | Fonte canônica e editável do e-book. |
| [E-book V5 Beta 2 — PDF](downloads/ebooks/context-engineering-para-times-de-desenvolvimento-v5-beta2.pdf) | PDF | Leitura e compartilhamento offline. |
| [Como recompilar o e-book](docs/ebooks/build/BUILD.md) | Markdown | Instruções e scripts para reconstruir o PDF a partir do Markdown ou do LaTeX. |
| [Apresentação V4](presentations/context-engineering-para-times-de-desenvolvimento-v4-apresentacao.pptx) | PPTX | Apresentação do conteúdo para workshops e reuniões; ainda não atualizada para a V5. |
| [Estrutura e decisões editoriais da V5 Beta 2](docs/audits/context-engineering-v5-beta2-estrutura.md) | Markdown | Racional das mudanças estruturais em relação à versão anterior. |
| [Relatório de validação V5 Beta 2](docs/audits/validation-report-v5-beta2.md) | Markdown | Escopo de verificação, checks determinísticos, hashes de integridade e limitações conhecidas. |
| [Laboratório executável V5 Beta 2](lab/README.md) | Projeto Cursor | Kit A e Kit B executáveis para praticar contexto, avaliação e evidência no Cursor. |

## Estrutura do repositório

```text
.
├── docs/
│   ├── audits/              # Auditorias, checklists e evidências de qualidade
│   └── ebooks/              # Fontes Markdown canônicas dos e-books e seus assets de build
│       ├── assets/          # Capa, diagramas e demais recursos referenciados pelo Markdown
│       └── build/           # Scripts e instruções para recompilar o PDF a partir do Markdown/LaTeX
├── downloads/
│   └── ebooks/              # PDFs prontos para leitura e distribuição
├── presentations/           # Materiais de apresentação editáveis (PPTX)
├── lab/                     # Laboratório executável Cursor-first (projeto .cursor/ independente)
├── archive/                 # Versões substituídas, preservadas para rastreabilidade
├── LICENSE                  # Termos de licenciamento do acervo
└── README.md                # Ponto de entrada e índice do repositório
```

## Fundamentos técnicos da organização

### Fonte canônica separada do artefato publicado

Os arquivos Markdown em `docs/` são revisáveis por diff, pesquisáveis e adequados à colaboração via Git. PDFs em `downloads/` são resultados de publicação: preservam layout e são práticos para consumo, mas não devem ser tratados como fonte de edição. A separação evita divergência de propósito e deixa claro onde uma mudança deve começar.

### Organização por tipo de artefato e ciclo de vida

- `docs/ebooks/` concentra conhecimento em evolução, sua fonte canônica e os assets de build (capa, diagramas, estilo e filtro Pandoc) que o Markdown referencia por caminho relativo.
- `docs/ebooks/build/` reúne os scripts (`build.ps1`/`build.sh`/`render-diagrams.*`) e o guia `BUILD.md` que reproduzem o PDF a partir do Markdown ou do `.tex`. Fica dentro de `docs/ebooks/` porque os scripts resolvem caminhos relativos ao próprio diretório do e-book (o mesmo nível do Markdown, do estilo e dos assets), e não faz sentido como categoria de topo por não ter conteúdo de leitura próprio.
- `downloads/` contém pacotes prontos para distribuição, cujo ciclo de atualização é vinculado à respectiva fonte.
- `presentations/` isola materiais orientados a comunicação síncrona, que possuem formato e ritmo de revisão diferentes dos e-books.
- `docs/audits/` mantém as evidências de avaliação, validações e decisões editoriais próximas da documentação, mas sem misturá-las ao conteúdo didático.
- `lab/` isola um projeto executável (não apenas leitura): uma árvore `.cursor/` completa com agents, skills, rules, evals e evidence, pensada para ser aberta como workspace no Cursor. Fica fora de `docs/` porque seu consumidor não é um leitor, é um host de agente.

Essa taxonomia reduz a ambiguidade de descoberta: o caminho do arquivo comunica seu propósito sem depender de convenções implícitas no nome.

### Raiz mínima e descoberta previsível

A raiz contém apenas os arquivos de orientação, licenciamento e os diretórios de topo que representam uma função clara do acervo (conteúdo, distribuição, apresentação, laboratório executável e arquivo). Materiais novos devem entrar no diretório que representa sua função, não soltos na raiz; uma nova categoria só ganha diretório de topo quando seu ciclo de vida e consumidor forem genuinamente distintos dos existentes — como ocorre com `lab/`, que é executado por um host de agente, não apenas lido. Isso escala melhor para busca humana, automação de publicação e agentes que recuperam conteúdo por caminho, tipo e metadados.

### Versionamento explícito

Utilize nomes em minúsculas, com hífens e versão no sufixo:

```text
<assunto>-v<versão>.<extensão>
```

Exemplo: `context-engineering-para-times-de-desenvolvimento-v5-beta2.md`.

Versões em revisão externa usam um sufixo de pré-lançamento (`v5-beta2`) em vez de um número inteiro. O sufixo é mantido em todos os artefatos derivados da mesma revisão (Markdown, PDF, laboratório, auditorias) até a edição final ser promovida com um número de versão inteiro.

O mesmo identificador de versão deve aparecer na fonte e nos artefatos derivados correspondentes. Quando uma versão deixar de ser a recomendada, mantenha-a somente se houver necessidade de rastreabilidade; nesse caso, mova-a para uma futura área `archive/` em vez de deixá-la nos diretórios de conteúdo atual.

Para artefatos que são árvores de diretório inteiras, como `lab/`, os arquivos internos mantêm nomes fixos exigidos pelo host (`SKILL.md`, `hooks.json`, `mcp.json`) e não recebem sufixo de versão individualmente. Nesse caso, a versão vai no nome da pasta de arquivamento (`archive/lab/v4/`), preservando a árvore interna intacta.

## Política de manutenção

1. Edite primeiro a fonte Markdown em `docs/ebooks/`.
2. Gere ou atualize o PDF correspondente em `downloads/ebooks/`.
3. Atualize a apresentação quando houver mudança relevante para comunicação ao vivo.
4. Registre revisões, limitações e critérios em `docs/audits/`.
5. Ao atualizar o laboratório (`lab/`), sincronize-o com a versão do e-book correspondente; ao substituí-lo, arquive a árvore anterior inteira em `archive/lab/v<versão>/` antes de promover a nova.
6. Atualize a tabela **Conteúdo em destaque** deste README ao adicionar material de referência.

Arquivos binários, como PDF e PPTX, não oferecem diffs textuais úteis. Para artefatos grandes ou com histórico frequente, recomenda-se Git LFS, mantendo no Git convencional apenas fontes e metadados textuais.

## Licença

Consulte [LICENSE](LICENSE) para os termos aplicáveis ao conteúdo deste repositório.