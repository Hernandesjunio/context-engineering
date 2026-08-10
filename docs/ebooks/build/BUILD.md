# Recompilação da V5

## Pré-requisitos

- Pandoc;
- XeLaTeX/TeX Live ou MiKTeX;
- fontes DejaVu Sans e DejaVu Sans Mono;
- Inkscape apenas se algum SVG for alterado.

## Fontes canônicas

Caminhos relativos a `docs/ebooks/`, exceto onde indicado:

| Alteração | Arquivo |
|---|---|
| Texto do livro | `ebook/context-engineering-para-times-de-desenvolvimento-v5.md` |
| Texto do workbook | `workbook/workbook-context-engineering-v5.md` |
| Estilo do livro | `ebook/ebook-style.tex` |
| Estilo do workbook | `workbook/workbook-style.tex` |
| Diagramas | `ebook/assets/diagrams/*.svg` |
| Corpus executável | `lab/` (raiz do repositório) |

O script `restructure.py` reconstrói os dois manuscritos a partir da baseline Beta 3 arquivada em `archive/ebooks/v5-sources/context-engineering-v5-beta3-frozen.md` e grava o inventário em `docs/audits/route-inventory-v5.md`. Execute-o somente quando quiser reaplicar a movimentação auditável a partir da baseline histórica; edições feitas diretamente nos manuscritos gerados serão substituídas.

## Build

Linux/macOS:

```bash
./build/build.sh all
./build/build.sh book
./build/build.sh workbook
```

Windows:

```powershell
.\build\build.ps1 -Mode all
.\build\build.ps1 -Mode book
.\build\build.ps1 -Mode workbook
```

Cada build executa Pandoc e duas passagens de XeLaTeX. Execute os comandos acima a partir de `docs/ebooks/`.

## Validação mínima

A partir de `docs/ebooks/`:

```bash
python3 build/restructure.py
python3 /caminho/inspect_manuscript.py ebook/context-engineering-para-times-de-desenvolvimento-v5.md
python3 /caminho/inspect_manuscript.py workbook/workbook-context-engineering-v5.md
```

A partir da raiz do repositório:

```bash
python3 lab/.cursor/hooks/validate_lab.py
```

Depois do build, renderize todas as páginas e inspecione:

- capa, sumário e aberturas;
- fundo e padding de blocos cercados;
- tabelas striped e cabeçalhos repetidos;
- blocos multipágina;
- páginas anteriores e posteriores a qualquer alteração;
- ausência de clipping, sobreposição ou callout órfão.

Não considere um log sem erro fatal como validação visual.

