# Como recompilar o E-book

## Pré-requisitos

- XeLaTeX, normalmente instalado pelo MiKTeX ou TeX Live.
- Pandoc para reconstruir o LaTeX a partir do Markdown.
- Inkscape somente quando algum SVG for alterado.

## Qual fonte editar

Os comandos abaixo devem ser executados a partir de `docs/ebooks/` (a pasta que contém o Markdown, o `.tex` gerado e este diretório `build/`).

| Alteração | Arquivo recomendado | Comando |
|---|---|---|
| Texto, títulos, tabelas e exemplos | `*.md` | `build.ps1 -Mode markdown` |
| Quebra de página ou ajuste LaTeX localizado | `*.tex` | `build.ps1 -Mode latex` |
| Cores, caixas, margens e tipografia | `ebook-style.tex` | `build.ps1 -Mode markdown` |
| Caixas e setas de um diagrama | `assets/diagrams/*.svg` | `render-diagrams.ps1`, depois build Markdown |

O modo Markdown recria o arquivo `.tex`. Portanto, uma correção feita somente no LaTeX será substituída se o Markdown for recompilado posteriormente. Para uma correção permanente, prefira ajustar Markdown, estilo ou SVG e então regenerar o LaTeX.

## Windows PowerShell

Execute a partir de `docs/ebooks/`:

```powershell
# Compilar alterações feitas diretamente no LaTeX.
.\build\build.ps1 -Mode latex

# Recriar LaTeX a partir do Markdown e compilar.
.\build\build.ps1 -Mode markdown

# Recriar PNGs depois de editar SVGs.
.\build\render-diagrams.ps1
.\build\build.ps1 -Mode markdown
```

## Linux ou macOS

Execute a partir de `docs/ebooks/`:

```bash
./build/build.sh latex
./build/build.sh markdown
./build/render-diagrams.sh
./build/build.sh markdown
```

## Ajustes de paginação

- Use `\Needspace{N\baselineskip}` antes de uma seção ou caixa que não deve ser dividida.
- Use `\newpage` apenas quando a nova página fizer parte da estrutura editorial.
- Não altere margens ou fonte para esconder uma quebra local; isso muda todas as páginas.
- Depois da compilação, confira a página modificada e também a página anterior e a seguinte.

## Ajustes dos diagramas

Os SVGs são as fontes editáveis. Os PNGs são consumidos pelo Markdown e pelo LaTeX gerado.

1. Edite o SVG no Inkscape.
2. Garanta que textos permanecem dentro das caixas.
3. Use pontas de seta proporcionais e mantenha espaço entre texto e conectores.
4. Execute o script de renderização dos diagramas.
5. Recompile no modo Markdown.

## Diagnóstico de erros

- `*.log`: log completo do XeLaTeX.
- `*.aux`, `*.toc`, `*.out`: arquivos temporários de referências e sumário.
- Texto cortado normalmente aparece como `Overfull \\hbox` no log.
- Referência ou sumário desatualizado normalmente exige uma segunda compilação.
