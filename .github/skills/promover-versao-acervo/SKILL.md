---
name: promover-versao-acervo
description: "Promove uma nova versão de e-book, PDF, apresentação, laboratório executável e evidências de revisão a partir de uma pasta temporária; arquiva a versão atual e atualiza o índice. Use quando publicar, distribuir, substituir, arquivar ou promover uma nova versão do acervo."
argument-hint: "Informe a pasta de origem e a versão a publicar, por exemplo: temp, v3.2"
user-invocable: true
---

# Promover versão do acervo

## Objetivo

Publicar uma nova versão sem perder a rastreabilidade da versão anterior. A fonte Markdown, o PDF, a apresentação, o laboratório executável e as evidências devem permanecer coerentes pelo mesmo sufixo de versão.

## Entradas esperadas

- Uma pasta temporária com os artefatos da nova versão.
- Ao menos a fonte Markdown e o PDF com o mesmo identificador de versão.
- Quando existirem: apresentação, arquivos de auditoria ou validação, documento de estrutura/decisões editoriais, assets de build do e-book (capa, diagramas, header LaTeX, filtros Pandoc) e um laboratório executável (`lab/`).

## Categorias de artefato

| Categoria | Onde fica quando publicada | Como arquivar |
|---|---|---|
| Fonte Markdown do e-book | `docs/ebooks/` | `archive/ebooks/` |
| PDF do e-book | `downloads/ebooks/` | `archive/ebooks/` |
| Assets de build do e-book (capa, diagramas, header LaTeX, filtros Pandoc) | `docs/ebooks/` (mesmo nível do Markdown, ex.: `docs/ebooks/assets/`), pois são referenciados por caminho relativo dentro da fonte | `archive/ebooks/` junto do Markdown e do PDF da mesma versão, como um pacote único |
| Apresentação | `presentations/` | `archive/presentations/` |
| Auditorias, Evidence Records, validações e documentos de estrutura/decisões editoriais | `docs/audits/` | `archive/audits/` |
| Laboratório executável (`lab/`, árvore `.cursor/` completa) | `lab/` na raiz do repositório | `archive/lab/v<versão>/` — a árvore inteira, pois arquivos internos têm nomes fixos exigidos pelo host (`SKILL.md`, `hooks.json`, `mcp.json`) e não carregam sufixo de versão individualmente |

## Procedimento

1. Inspecione o estado do Git e liste os arquivos da pasta de origem. Não descarte alterações não relacionadas.
2. Confirme que os nomes dos artefatos novos usam a mesma versão e que o PDF corresponde ao Markdown publicado. Se houver um Evidence Record com hash, recalcule o hash SHA-256 da fonte (markdown, PDF, apresentação) e compare com o valor registrado antes de mover os arquivos.
3. Busque referências residuais ao caminho temporário de origem ou a artefatos de versões anteriores dentro dos arquivos novos (ex.: `grep` por `ai-context/`, o nome da pasta temporária ou caminhos absolutos locais).
4. Mova os artefatos atualmente publicados para `archive/`, seguindo a tabela de categorias acima. Para o laboratório, mova a árvore inteira para `archive/lab/v<versão>/`.
5. Promova cada categoria da pasta temporária para o destino correspondente na tabela acima.
6. Atualize a tabela **Conteúdo em destaque**, a árvore de diretórios e qualquer referência de versão no README. Se uma categoria nova de artefato for introduzida pela primeira vez (como `lab/`), adicione também uma justificativa na seção de fundamentos técnicos do README.
7. Verifique que os links do README apontam para arquivos existentes, que não há artefatos da versão promovida na pasta temporária e que o Git mostra apenas as mudanças esperadas.
8. Remova a pasta temporária de origem somente depois de confirmar que todos os artefatos foram movidos (não copiados) com sucesso.
9. Faça commit somente se o usuário solicitar. Nunca faça push sem solicitação explícita.

## Regras de segurança

- Nunca sobrescreva ou exclua uma versão atual: arquive-a primeiro.
- Preserve nomes versionados; não renomeie uma versão antiga para parecer atual.
- Não trate PDF ou PPTX como fonte editável.
- Mantenha auditorias e evidências junto da versão que elas descrevem.
- Não renomeie arquivos de auditoria/validação para uniformizar convenções de nomenclatura entre versões (ex.: português vs. inglês) sem confirmação explícita do autor — isso pode invalidar hashes já registrados em Evidence Records.
- Não divida a árvore do laboratório entre múltiplos diretórios de topo; ela deve permanecer um projeto único e coeso em `lab/`.