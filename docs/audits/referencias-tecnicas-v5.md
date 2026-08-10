# Referências técnicas das decisões — V5

As referências abaixo sustentam afirmações materiais. Decisões editoriais próprias são identificadas como convenções e não apresentadas como leis universais.

| Decisão ou afirmação | Classe | Fundamento | Limite aplicado na edição |
|---|---|---|---|
| Separar ergonomia do leitor de custo e memória do runtime | política técnica | Sweller (carga cognitiva) e Kwon et al. (PagedAttention/KV cache) tratam superfícies diferentes | nenhuma dificuldade de leitura é convertida em consumo de KV cache sem telemetria |
| Dividir livro e workbook | decisão editorial informada | Mayer & Moreno discutem segmentação e redução de processamento extrínseco; literatura de worked examples apoia exemplos guiados | não se afirma que a divisão mediu ou reduziu carga cognitiva deste público; isso exige teste com leitores |
| Evitar que informação crítica dependa apenas de posição intermediária | comportamento de LLM | Liu et al., TACL 2024 | resultado limitado aos modelos, tarefas e protocolos avaliados; sem percentual universal |
| Progressive disclosure em Agent Skills | especificação aberta | Agent Skills Specification e guia de descrições | não se confunde com cache físico nem se estende automaticamente a todo host |
| `name` e `description` como metadados mínimos de Skill | especificação aberta | Agent Skills Specification | campos de governança adicionais só produzem efeito se algum consumidor os interpretar |
| Rules, Skills, subagents e hooks no Cursor | produto | documentação oficial do Cursor consultada em 9 ago. 2026 | `playbooks`, `contracts`, `evals`, `evidence` e a árvore proposta permanecem convenções do livro |
| `202 Accepted` não comprova conclusão | padrão HTTP | RFC 9110, seção 15.3.3 | durabilidade e consulta do job vêm do Contract da arquitetura de referência |
| SignalR como notificação, não fonte canônica neste estudo | exemplo arquitetural | documentação ASP.NET Core SignalR + Contract do estudo | não universalizado para toda arquitetura em tempo real |
| Verificadores determinísticos para schema, estado e igualdade | política de avaliação | propriedades calculáveis não precisam de interpretação probabilística | LLM-as-a-Judge permanece permitido para critérios semânticos, com versão, rubrica e revisão proporcional ao risco |
| Fundo de código e tabelas striped | decisão visual validada | revisão visual da skill editorial; contraste e rastreamento de linha verificados na renderização | striping não substitui cabeçalho, regras horizontais ou rótulo textual; não se atribui ganho cognitivo universal |

## Fontes primárias e autoritativas

- Liu, N. F. et al. **Lost in the Middle: How Language Models Use Long Contexts**. TACL 12, 2024. <https://aclanthology.org/2024.tacl-1.9/>.
- Sweller, J. **Cognitive Load During Problem Solving: Effects on Learning**. Cognitive Science, 1988. <https://doi.org/10.1207/s15516709cog1202_4>.
- Mayer, R. E.; Moreno, R. **Nine Ways to Reduce Cognitive Load in Multimedia Learning**. Educational Psychologist, 2003. <https://doi.org/10.1207/S15326985EP3801_6>.
- Kwon, W. et al. **Efficient Memory Management for Large Language Model Serving with PagedAttention**. 2023. <https://arxiv.org/abs/2309.06180>.
- Agent Skills. **Specification**. <https://agentskills.io/specification>.
- Cursor. **Rules**. <https://cursor.com/docs/rules>.
- Cursor. **Subagents**. <https://cursor.com/docs/subagents>.
- Cursor. **Agent Skills**. <https://cursor.com/docs/skills>.
- Cursor. **Hooks**. <https://cursor.com/docs/hooks>.
- IETF. **RFC 9110 — HTTP Semantics**, seção 15.3.3. <https://www.rfc-editor.org/rfc/rfc9110.html#name-202-accepted>.
- Microsoft. **ASP.NET Core SignalR overview**. <https://learn.microsoft.com/aspnet/core/signalr/introduction>.

