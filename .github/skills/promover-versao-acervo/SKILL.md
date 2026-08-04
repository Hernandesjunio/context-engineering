---
name: promover-versao-acervo
description: "Promove uma nova versão de e-book, PDF, apresentação e evidências de revisão a partir de uma pasta temporária; arquiva a versão atual e atualiza o índice. Use quando publicar, distribuir, substituir, arquivar ou promover uma nova versão do acervo."
argument-hint: "Informe a pasta de origem e a versão a publicar, por exemplo: temp, v3.2"
user-invocable: true
---

# Promover versão do acervo

## Objetivo

Publicar uma nova versão sem perder a rastreabilidade da versão anterior. A fonte Markdown, o PDF, a apresentação e as evidências devem permanecer coerentes pelo mesmo sufixo de versão.

## Entradas esperadas

- Uma pasta temporária com os artefatos da nova versão.
- Ao menos a fonte Markdown e o PDF com o mesmo identificador de versão.
- Quando existirem, apresentação e arquivos de auditoria ou validação.

## Procedimento

1. Inspecione o estado do Git e liste os arquivos da pasta de origem. Não descarte alterações não relacionadas.
2. Confirme que os nomes dos artefatos novos usam a mesma versão e que o PDF corresponde ao Markdown publicado. Se houver um Evidence Record com hash, valide o hash da fonte antes de mover os arquivos.
3. Mova os artefatos atualmente publicados para `archive/`, mantendo o tipo: Markdown em `archive/ebooks/`, PDFs em `archive/ebooks/`, apresentações em `archive/presentations/` e auditorias em `archive/audits/`.
4. Promova o Markdown para `docs/ebooks/`, o PDF para `downloads/ebooks/`, a apresentação para `presentations/` e auditorias, Evidence Records e validações para `docs/audits/`.
5. Atualize a tabela **Conteúdo em destaque**, a árvore de diretórios e qualquer referência de versão no README.
6. Verifique que os links do README apontam para arquivos existentes, que não há artefatos da versão promovida na pasta temporária e que o Git mostra apenas as mudanças esperadas.
7. Faça commit somente se o usuário solicitar. Nunca faça push sem solicitação explícita.

## Regras de segurança

- Nunca sobrescreva ou exclua uma versão atual: arquive-a primeiro.
- Preserve nomes versionados; não renomeie uma versão antiga para parecer atual.
- Não trate PDF ou PPTX como fonte editável.
- Mantenha auditorias e evidências junto da versão que elas descrevem.