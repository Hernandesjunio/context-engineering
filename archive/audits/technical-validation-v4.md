# Validação Técnica da V4

## Escopo

- Manuscrito e PDF.
- Apresentação PowerPoint.
- Laboratório Cursor-first.
- Schemas, skills, fixtures e Evidence Record.

## Checks determinísticos

| Check | Resultado |
|---|---|
| Skill `validate-api-contract` | PASS |
| Skill `audit-context-execution` | PASS |
| Contract do relatório | PASS |
| Evidence Record do laboratório | PASS |
| Vínculo Project Rule → Domain Rule | PASS |
| Assertions da Eval Spec resolvem por ID | PASS |
| Ausência de `ai-context/` no laboratório | PASS |
| PDF renderizado e inspecionado visualmente (75 páginas) | PASS |
| PowerPoint renderizado sem overflow (18 slides) | PASS |
| Fidelidade ao template da apresentação | PASS |
| Busca por referências residuais à V3.1 e `ai-context/` | PASS |

## Integridade dos entregáveis

| Artefato | SHA-256 |
|---|---|
| Markdown V4 | `b8a9f8ce9bbabf0ab3673aa0ffde488f98122495539d206aa174c5da2a87dbcb` |
| PDF V4 | `5effcd78e54b7298e7ba23d881cd9f6e9cfad51fcdfd75d58599965765cfd19b` |
| PowerPoint V4 | `96352c87ba093fd9c7526dc4a7d337e94d922345501ee3ac16baa170a9c271c9` |

## Evidência visual

- O PDF completo foi renderizado em imagens e revisado por montagem geral e amostras de páginas críticas.
- Os 18 slides foram renderizados, inspecionados em contact sheet e submetidos ao teste automatizado de overflow.
- O arquivo `presentation-inspection-v4.ndjson` preserva a inspeção estrutural da apresentação.
- O parecer técnico progressivo que fundamentou as decisões da V4 acompanha este pacote.

## Validação editorial

- O manual caótico e o arquivo backend caótico estão cercados e marcados como anti-pattern.
- O playbook não está aninhado em knowledge.
- `id` e `name` têm papéis distintos; Agent Skills mantêm apenas `name` e `description` no frontmatter.
- `mustRetrieve`, `mustApply`, `mustNotClaim`, `evaluationMethod` e `verifyWith` possuem produtor e uso explicados.
- A captura operacional não é chamada de Evidence Record antes da comparação.
- O estudo de caso declara explicitamente o que omite.

## Limitações

- A ativação real das Rules, Agents e Skills deve ser testada na versão do Cursor usada pelo time.
- `hooks.json` e `mcp.json` são exemplos sem integração produtiva ou credenciais.
- Critérios semânticos ainda exigem o modelo, prompt, política de judge e amostragem definidos pelo ambiente real.
- O laboratório valida o schema essencial por script leve; pipelines de produção devem usar um validador JSON Schema completo.
