# Context Engineering

Repositório de conhecimento para times de desenvolvimento que projetam, operam e avaliam o contexto fornecido a sistemas baseados em LLMs e agentes.

O acervo separa **fontes editáveis**, **artefatos de distribuição**, **apresentações** e **evidências de qualidade**. Essa separação mantém o material fácil de encontrar, reduz alterações acidentais em arquivos binários e permite que o repositório cresça sem transformar a raiz em um catálogo sem organização.

## Conteúdo em destaque

| Material | Formato | Finalidade |
|---|---|---|
| [Context Engineering para Times de Desenvolvimento](docs/ebooks/context-engineering-para-times-de-desenvolvimento-v3.md) | Markdown | Fonte canônica e editável do e-book. |
| [E-book — PDF](downloads/ebooks/context-engineering-para-times-de-desenvolvimento-v3.pdf) | PDF | Leitura e compartilhamento offline. |
| [Apresentação V3](presentations/context-engineering-para-times-de-desenvolvimento-v3-apresentacao.pptx) | PPTX | Apresentação do conteúdo para workshops e reuniões. |
| [Auditoria editorial e técnica V3](docs/audits/auditoria-editorial-e-tecnica-v3.md) | Markdown | Registro de critérios, riscos, decisões e evidências de revisão. |

## Estrutura do repositório

```text
.
├── docs/
│   ├── audits/              # Auditorias, checklists e evidências de qualidade
│   └── ebooks/              # Fontes Markdown canônicas dos e-books
├── downloads/
│   └── ebooks/              # PDFs prontos para leitura e distribuição
├── presentations/           # Materiais de apresentação editáveis (PPTX)
├── LICENSE                  # Termos de licenciamento do acervo
└── README.md                # Ponto de entrada e índice do repositório
```

## Fundamentos técnicos da organização

### Fonte canônica separada do artefato publicado

Os arquivos Markdown em `docs/` são revisáveis por diff, pesquisáveis e adequados à colaboração via Git. PDFs em `downloads/` são resultados de publicação: preservam layout e são práticos para consumo, mas não devem ser tratados como fonte de edição. A separação evita divergência de propósito e deixa claro onde uma mudança deve começar.

### Organização por tipo de artefato e ciclo de vida

- `docs/ebooks/` concentra conhecimento em evolução e sua fonte canônica.
- `downloads/` contém pacotes prontos para distribuição, cujo ciclo de atualização é vinculado à respectiva fonte.
- `presentations/` isola materiais orientados a comunicação síncrona, que possuem formato e ritmo de revisão diferentes dos e-books.
- `docs/audits/` mantém as evidências de avaliação próximas da documentação, mas sem misturá-las ao conteúdo didático.

Essa taxonomia reduz a ambiguidade de descoberta: o caminho do arquivo comunica seu propósito sem depender de convenções implícitas no nome.

### Raiz mínima e descoberta previsível

A raiz contém apenas os arquivos de orientação e licenciamento. Materiais novos devem entrar no diretório que representa sua função, não diretamente na raiz. Isso escala melhor para busca humana, automação de publicação e agentes que recuperam conteúdo por caminho, tipo e metadados.

### Versionamento explícito

Utilize nomes em minúsculas, com hífens e versão no sufixo:

```text
<assunto>-v<versão>.<extensão>
```

Exemplo: `context-engineering-para-times-de-desenvolvimento-v3.md`.

O mesmo identificador de versão deve aparecer na fonte e nos artefatos derivados correspondentes. Quando uma versão deixar de ser a recomendada, mantenha-a somente se houver necessidade de rastreabilidade; nesse caso, mova-a para uma futura área `archive/` em vez de deixá-la nos diretórios de conteúdo atual.

## Política de manutenção

1. Edite primeiro a fonte Markdown em `docs/ebooks/`.
2. Gere ou atualize o PDF correspondente em `downloads/ebooks/`.
3. Atualize a apresentação quando houver mudança relevante para comunicação ao vivo.
4. Registre revisões, limitações e critérios em `docs/audits/`.
5. Atualize a tabela **Conteúdo em destaque** deste README ao adicionar material de referência.

Arquivos binários, como PDF e PPTX, não oferecem diffs textuais úteis. Para artefatos grandes ou com histórico frequente, recomenda-se Git LFS, mantendo no Git convencional apenas fontes e metadados textuais.

## Licença

Consulte [LICENSE](LICENSE) para os termos aplicáveis ao conteúdo deste repositório.