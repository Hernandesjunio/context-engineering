# Auditoria técnica — Segurança do MCP, Azure AD B2C e propagação de token

> Documento auditado: `seguranca-mcp-stateless-azure-b2c(1).md`  
> Escopo: coerência, segurança OAuth/MCP, Azure AD B2C, multi-JWT, HMAC e identidade do investidor.  
> Data da revisão: 14/09/2026.

## Veredito executivo

O documento possui uma base de segurança boa: diferencia access token de ID token, exige PKCE, valida `iss`/`aud`/prazo, trata BOLA, não considera Swagger um controle e reconhece expressamente que o token passthrough é temporário.

Entretanto, ele **ainda não deve ser usado como especificação normativa de produção**. Há quatro problemas prioritários:

1. o consentimento deixou de ser vinculado ao cliente OAuth (`client_id`/`azp`);
2. existem decisões contraditórias sobre exigir ou omitir `mcp.read`;
3. exemplos confundem a URI canônica do MCP com o valor real de `aud` emitido pelo B2C;
4. o texto ainda sugere que o mesmo `oid` explica a validade do token na API de Negócio, quando isso apenas explica a resolução do mesmo usuário.

> [!IMPORTANT]
> **Conclusão sobre a dúvida principal:** a propagação continua sendo má prática e não conformidade mesmo que as duas APIs encontrem o mesmo `oid` e acessem os mesmos dados. O HMAC é uma mitigação útil, mas não altera o destinatário criptograficamente declarado no token. O MCP 2026-07-28 determina que o token do upstream seja separado e proíbe repassar o token recebido do cliente.

## Matriz de findings

| ID | Severidade | Finding | Situação |
|---|---:|---|---|
| F-01 | Crítica | Consentimento não está vinculado ao cliente OAuth | Corrigir antes de conectar mais de um host/agente |
| F-02 | Crítica | Mesmo `oid` é tratado como justificativa para aceitar token com audiência errada | Corrigir conceito e arquitetura |
| F-03 | Alta | B2C não oferece OBO para a cadeia MCP → API de Negócio | Decisão arquitetural necessária |
| F-04 | Alta | Documento simultaneamente exige e omite `mcp.read` | Consolidar uma única decisão |
| F-05 | Alta | Exemplos assumem `aud` igual à URL do MCP | Substituir pelo valor real do tenant |
| F-06 | Alta | Exemplo multi-JWT é ilustrativo, mas parece produção-ready | Completar requisitos e tratamento de falhas |
| F-07 | Média | HMAC é construção própria e tem lacunas de protocolo | Padronizar ou especificar formalmente |
| F-08 | Média | Uso de `azp` foi afastado do consentimento principal | Reintroduzir vínculo do cliente |
| F-09 | Média | `oid` é usado sem namespace de emissor/tenant | Usar identidade composta |
| F-10 | Média | Token de aplicação presume `roles`, mas B2C documenta comportamento diferente | Validar token real e remover premissa |
| F-11 | Média | Fluxo inicial mostra MCP iniciando login no B2C | Corrigir diagrama |
| F-12 | Baixa | Documento com 9,7 mil palavras repete conceitos e decisões | Reestruturar por progressive disclosure |

---

## Findings detalhados

### F-01 — Consentimento sem `client_id` ou `azp`

**Onde aparece:** “O consentimento é do investidor para o MCP”, glossário de `azp`, chave proposta `oid + resource + tool(s)` e resposta “`azp` não tem nada a ver com este consentimento”.

**Problema:** OAuth delega um cliente a acessar um recurso em nome do usuário. Se Cursor, ChatGPT e Claude usarem o mesmo MCP, a autorização dada a um cliente não deve ser automaticamente reutilizada por outro. O próprio exemplo oficial de access token B2C contém `azp`, associado ao cliente que iniciou a solicitação.

**Impacto:** revogação por aplicativo fica impossível; um novo plugin pode herdar consentimento concedido a outro; auditoria não consegue responder “qual agente recebeu a autorização?”.

**Correção:** gravar e validar:

```text
issuer/tenant + oid + client_id/azp + resource + permission/tool
+ status + consent_version + granted_at + revoked_at
```

Se o token real emitir `azp`, compare-o ao cliente gravado. Se não emitir, a policy deve produzir uma claim confiável equivalente ou a arquitetura deve obter essa identidade por outro mecanismo autenticado. Não aceite um `client_id` vindo em header comum.

**Base auditável:** [Microsoft — exemplo de token B2C com `aud`, `oid`, `scp` e `azp`](https://learn.microsoft.com/en-us/azure/active-directory-b2c/access-tokens).

### F-02 — O mesmo `oid` não torna o token válido para outra API

**Onde aparece:** fluxo da API de Negócio e justificativa de que ambas usam o mesmo Graph/`oid`.

**Problema:** são verificações diferentes:

- `oid` identifica o objeto do usuário dentro do diretório;
- `aud` identifica o resource server autorizado a consumir o access token.

A API de Negócio encontra o investidor porque extrai um identificador válido de um JWT que decidiu aceitar via multi-JWT. Isso demonstra interoperabilidade do identificador, não validade de audiência. A funcionalidade “funcionar” é consequência da configuração excepcional que adicionou a audiência do MCP à API de Negócio.

Além disso, Microsoft Graph exige um token destinado ao Graph. Se a API consulta o Graph pelo `oid`, ela precisa obter separadamente um token Graph — normalmente app-only — ou usar outro serviço já autenticado. O token MCP não deve ser enviado ao Graph.

**Correção textual:** substituir “o token funciona porque usa o mesmo `oid`” por:

> A API de Negócio consegue resolver o mesmo usuário porque o `oid` pertence ao mesmo diretório B2C. Ela aceita o Bearer somente porque foi excepcionalmente configurada para confiar também na audiência MCP. Essas duas propriedades são independentes.

**Base auditável:** o B2C documenta `aud` como destinatário e `oid` como objeto do usuário; o Graph exige token próprio obtido para `https://graph.microsoft.com/.default`. [Tokens B2C](https://learn.microsoft.com/en-us/azure/active-directory-b2c/access-tokens) e [acesso app-only ao Microsoft Graph](https://learn.microsoft.com/en-us/graph/auth-v2-service).

### F-03 — Azure AD B2C não implementa OBO

**Onde aparece:** solução futura descrita genericamente como “troca/delegação aprovada”.

**Problema:** no cenário API A → API B, o mecanismo Microsoft equivalente seria On-Behalf-Of: o token A, destinado à API A, é trocado por token B, destinado à API B, mantendo o usuário delegado. A documentação oficial informa explicitamente que OBO não está implementado no Azure AD B2C.

**Consequência:** `AcquireTokenOnBehalfOf`/`requested_token_use=on_behalf_of` não é uma saída disponível para o token emitido por B2C. O B2C também não deve ser presumido como implementação de RFC 8693 Token Exchange.

**Correção:** documentar três opções reais, apresentadas mais adiante neste relatório.

**Base auditável:** [Microsoft — B2C não suporta cadeias de APIs/OBO](https://learn.microsoft.com/en-us/azure/active-directory-b2c/access-tokens) e [Microsoft Entra ID — funcionamento do OBO quando suportado](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-on-behalf-of-flow).

### F-04 — Contradição sobre `mcp.read`

**Onde aparece:** decisão, exemplos, policies e checklist exigem `mcp.read`; a descoberta e o roadmap permitem omiti-lo.

**Problema:** o documento define duas arquiteturas incompatíveis. Além disso, o B2C documenta que o cliente solicita um resource scope para obter access token e coloca apenas os scopes concedidos em `scp`.

**Correção recomendada:** como o arquivo já adotou `mcp.read` de forma predominante, mantenha o scope agregado no MVP e retire todas as frases que autorizam omiti-lo. Publique `mcp.read` em `scopes_supported` e, quando apropriado, no desafio `WWW-Authenticate`. A granularidade por tool continua no banco; não é preciso criar scopes dinâmicos.

Se a decisão real for não usar scope, remova `ScopeRequirement`, `scp`, `mcp.read` e todos os exemplos correspondentes. Não deixe fallback ambíguo.

**Base auditável:** [Microsoft — scopes e emissão de access token no B2C](https://learn.microsoft.com/en-us/azure/active-directory-b2c/access-tokens) e [MCP 2026-07-28 — seleção e desafios de scope](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization).

### F-05 — `resource` MCP não é automaticamente o `aud` JWT do B2C

**Onde aparece:** exemplos usam `aud = https://mcp.investidor.com.br/mcp` e `ValidAudience` com a mesma URL.

**Problema:** a URI canônica do Protected Resource Metadata é uma coisa; a claim `aud` concretamente emitida pelo B2C é outra configuração. A documentação B2C apresenta `aud` como o Application/Client ID da API, normalmente um GUID. Não assuma que o parâmetro `resource` do MCP fará o B2C emitir a URL como audience.

**Correção:** use marcadores separados:

```text
MCP canonical resource = https://mcp.investidor.com.br/mcp
B2C expected aud       = <Application (client) ID observado no token real>
```

Configure `ValidAudience`/`ValidAudiences` com o valor real emitido e validado pelo time de identidade. Mantenha um teste contratual específico para saber se o B2C aceita ou ignora o parâmetro `resource` obrigatório enviado pelo cliente MCP.

### F-06 — Exemplo .NET não está pronto para ser copiado em produção

**Onde aparece:** configurações `AddJwtBearer` e endpoints de exemplo.

**Problemas:**

- a policy B2C esperada é mencionada fora do código, mas não aparece como requisito;
- `AddAuthentication()` sem default só funciona de forma previsível quando toda rota informa explicitamente o esquema;
- `throw new UnauthorizedAccessException` pode resultar em `500` se não houver mapeamento global apropriado;
- a identidade é autorizada apenas por `oid`, sem `client_id`/`azp` no grant;
- o código não deixa claro que `Authority`, issuer, metadata HTTPS, clock skew e audiência foram verificados com tokens reais;
- a API de Negócio aceita deliberadamente uma audiência que não lhe pertence, o que deve estar marcado no código/configuração como feature flag não produtiva.

**Correção:** transformar os snippets em pseudocódigo ou completar uma policy composta por `issuer + policy + audience + scope + client + consent + ownership`. Trate claim ausente via challenge/forbid controlado, não exceção genérica. Exija uma flag como `AllowMcpAudiencePassthrough=false` por padrão e impeça sua ativação no ambiente produtivo durante startup/deploy policy.

### F-07 — HMAC melhora a exceção, mas o protocolo proposto é artesanal

**Onde aparece:** `X-MCP-Timestamp`, `X-MCP-Nonce`, `X-MCP-Signature` e concatenação manual.

**Acerto:** incluir método, caminho/query, digest do body e hash do access token é muito melhor do que header estático. Timestamp e nonce também reduzem replay.

**Lacunas:** não estão formalizados encoding, normalização de URI/query, parâmetros repetidos, autoridade/host, versão/chave, tolerância de relógio, armazenamento atômico do nonce entre réplicas e transformações feitas por gateway/HTTP version. Diferenças de canonicalização são fonte frequente de bypass ou indisponibilidade.

**Correção preferida:** adotar **HTTP Message Signatures (RFC 9421)** com `hmac-sha256` e **Content-Digest (RFC 9530)**, cobrindo pelo menos `@method`, `@target-uri`/`@authority`, `content-digest`, `authorization` ou seu digest, `created`, `expires`, `nonce` e `keyid`. Se mantiver o formato próprio, escreva um perfil normativo equivalente e use `SET NX`/operação atômica no Redis para consumir o nonce.

HMAC deve continuar sobre TLS, com segredo por ambiente, identificador de chave, rotação current/previous curta, algoritmo fixo e comparação em tempo constante.

**Base auditável:** [RFC 9421 — HTTP Message Signatures](https://www.rfc-editor.org/rfc/rfc9421.html) e [RFC 9530 — Digest Fields](https://www.rfc-editor.org/rfc/rfc9530.html).

### F-08 — `azp` foi indevidamente afastado do fluxo principal

**Onde aparece:** “`azp` não participa do consentimento” e Q&A final.

**Problema:** `azp` não substitui o investidor, mas pode ser justamente a claim que liga o token ao cliente OAuth. No cenário com vários hosts MCP, isso é relevante para consentimento, allowlist, auditoria e revogação por cliente.

**Correção:** redigir: “`oid` identifica o investidor; `azp` identifica o cliente autorizado, quando emitido; ambos participam da chave de autorização, com `iss`/tenant e resource.” Validar com token real, pois claims podem variar por policy.

### F-09 — `oid` precisa de namespace

**Problema:** um GUID de objeto é interpretável dentro de um diretório/emissor. Usá-lo sozinho em caches, consentimento e auditoria cria risco quando surgirem múltiplos tenants, issuers ou migração de identidade.

**Correção:** a chave de identidade deve incluir ao menos `(issuer, oid)` e, quando disponível/estável, tenant/policy conforme a estratégia aprovada. Nunca copie `oid` de header não assinado; obtenha-o do token validado ou de uma credencial interna assinada.

### F-10 — Token app-only B2C não deve presumir `roles`

**Onde aparece:** exemplo da fintech e regra `roles=[fintech.api.access]`.

**Problema:** na plataforma Entra comum, app-only normalmente usa `roles`; porém a documentação específica de client credentials do B2C mostra permissões expostas no `scp`. O arquivo apresenta `roles` como possibilidade, mas depois constrói autorização dependente dela.

**Correção:** não escolher `roles` ou `scp` por memória. Gere um token real da policy usada, registre seu contrato de claims e teste ambos os casos negativos. A feature de client credentials no B2C continua documentada como preview, o que também deve entrar no risk assessment.

**Base auditável:** [Microsoft — client credentials no Azure AD B2C](https://learn.microsoft.com/en-us/azure/active-directory-b2c/client-credentials-grant-flow).

### F-11 — Diagrama inicial inverte o início do OAuth

**Problema:** o diagrama mostra `MCP → B2C`. No fluxo normal, o MCP responde `401` com descoberta; o **Cursor** descobre o Authorization Server e inicia `/authorize`. O MCP não autentica o usuário diretamente no B2C.

**Correção:** substituir a seta por `Cursor → B2C`, mantendo `B2C → API de consentimento` e `B2C → callback do Cursor`.

### F-12 — Gargalo editorial e operacional

O arquivo cresceu para aproximadamente 9,7 mil palavras. Conceitos como scope, `oid`, passthrough e HMAC aparecem em introdução, glossário, seções numeradas, Q&A e conclusão. Isso aumenta a chance de uma decisão ser atualizada em um ponto e permanecer antiga em outro — exatamente o que ocorreu com `mcp.read`.

**Correção:** separar em três artefatos:

1. **Decisão/ADR curta:** estado atual, riscos aceitos, prazo e gate de produção;
2. **Guia didático:** OAuth, claims, consentimento e fluxos;
3. **Runbook técnico:** configurações .NET, HMAC/message signatures e testes.

---

## A propagação continua grave se os dados e o `oid` são os mesmos?

Sim, mas a gravidade deve ser descrita com precisão.

O problema não é a API de Negócio consultar os mesmos dados. O problema é ampliar silenciosamente o poder de uma credencial Bearer. Um token roubado deveria funcionar apenas no MCP; ao fazer a API de Negócio aceitar `aud=MCP`, ele passa a funcionar em dois recursos. Isso aumenta a superfície de replay, contorna a autorização por tool que existe no MCP e dificulta políticas específicas de recurso.

O HMAC muda parcialmente o risco: quem roubar somente o token não consegue chamar diretamente a API de Negócio sem conhecer a chave e gerar uma assinatura válida. Portanto, HMAC + nonce + expiração + rota privada é uma compensação relevante para ambiente temporário. Mesmo assim:

- o token continua com audiência errada;
- o MCP continua repassando a credencial recebida do cliente;
- a API de Negócio mantém código de confiança excepcional;
- o HMAC é uma segunda credencial compartilhada, não um token B2C;
- a solução não adquire scopes próprios da API de Negócio.

A especificação MCP é normativa: se o MCP chama uma API upstream, deve usar um token separado e **MUST NOT** repassar o access token recebido. [MCP — Access Token Privilege Restriction](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/security-considerations).

---

## O que o Azure AD B2C oferece para substituir isso?

### Resposta direta

O Azure AD B2C **não fornece OBO** para trocar o token do MCP por outro token delegado à API de Negócio. Também não há fundamento para presumir suporte nativo a RFC 8693 Token Exchange.

Ele oferece **client credentials**, ainda documentado como preview, para o MCP obter um token app-only destinado à API de Negócio. Esse token prova a identidade do MCP, mas não preserva o investidor como usuário delegado. O contexto do investidor precisa viajar separadamente e com integridade verificável.

### Opção 1 — Recomendação prática: identidade do MCP + contexto assinado

```mermaid
sequenceDiagram
    participant C as Cliente MCP
    participant M as MCP
    participant A as Authorization Server
    participant B as API de Negócio

    C->>M: Token usuário, aud=MCP
    M->>M: Valida token, cliente, consentimento e tool
    M->>A: Client credentials / workload identity
    A-->>M: Token app-only, aud=API de Negócio
    M->>B: Token app-only + contexto de usuário assinado
    B->>B: Valida workload e contexto; resolve issuer+oid
    B-->>M: Dados autorizados
```

O contexto mínimo pode conter:

```json
{
  "user_iss": "<issuer-B2C>",
  "user_oid": "<oid>",
  "client_id": "<azp-validado>",
  "consent_id": "<id/version>",
  "operation": "position.read",
  "iat": 0,
  "exp": 0,
  "jti": "<nonce>",
  "correlation_id": "<trace-id>"
}
```

Esse contexto pode ser protegido por HTTP Message Signature/HMAC ou, preferencialmente, por JWS assimétrico de curta duração assinado pelo MCP. A API de Negócio autoriza a combinação **identidade do workload + contexto do usuário + operação**, e não aceita o Bearer original.

Vantagens: audiência correta, token roubado do MCP não chega ao downstream, rotação de chave pode ser isolada e o `oid` permanece disponível para resolver o investidor. Limitação: não é delegação B2C padrão; é um contrato interno que precisa de threat model e testes.

> [!NOTE]
> Em AKS, uma identidade de workload/managed identity do tenant corporativo pode ser preferível ao client secret. Se a API de Negócio só confia no B2C hoje, será necessário adicionar um esquema de autenticação para essa identidade de serviço ou usar o client credentials B2C consciente de que está em preview.

### Opção 2 — Token exchange/STS próprio

Um Authorization Server intermediário pode validar o token MCP e emitir um token curto com:

- `aud=API de Negócio`;
- sujeito do investidor (`sub`/`oid`, com issuer de origem);
- `act` identificando o MCP como ator;
- scopes reduzidos à operação autorizada;
- `jti`, `iat`, `nbf`, `exp` curto e, idealmente, sender constraint.

Esse desenho se aproxima da RFC 8693, que define `subject_token`, `resource`/`audience` e a claim `act` para representar delegação. É a melhor semântica se a organização realmente precisa de um token delegado downstream, mas criar um STS é uma responsabilidade de segurança elevada e não deve ser tratado como utilitário do MCP.

**Base auditável:** [RFC 8693 — OAuth 2.0 Token Exchange](https://www.rfc-editor.org/rfc/rfc8693.html).

### Opção 3 — Exceção atual: Bearer MCP + HMAC

Aceitável somente como finding temporário em desenvolvimento/homologação se houver:

- feature flag proibida em produção;
- rota/hostname privado não publicado externamente;
- firewall/NetworkPolicy restringindo o chamador;
- TLS e, se possível, mTLS/identidade do workload;
- assinatura padronizada, chave por ambiente e rotação;
- nonce consumido atomicamente e janela de poucos minutos;
- autorização por tool já concluída no MCP;
- testes que provem que token sem HMAC, HMAC sem token, replay, path/query alterado e origem externa são rejeitados;
- responsável e data-limite antes de produção.

Essa opção é uma redução de risco, não conformidade MCP nem token exchange.

---

## Recomendação final para o time

Para não paralisar a entrega, mantenha a solução atual apenas no ambiente de teste e fortaleça o HMAC usando RFC 9421 ou um perfil interno formal. Em paralelo, implemente a opção 1: o MCP obtém um token de serviço destinado à API de Negócio e envia `issuer + oid + client_id + consent/operation` em contexto assinado de vida curtíssima. Ela remove o passthrough sem depender do OBO inexistente no B2C.

Antes de produção, a API de Negócio deve deixar de aceitar `aud=MCP`. Se a área de identidade exigir delegação OAuth verdadeira e não aceitar o contexto interno assinado, a decisão correta é um STS/token broker compatível com RFC 8693 ou uma plataforma de identidade que suporte OBO para esse tipo de usuário — não tentar simular OBO com HMAC.

## Checklist de correção

- [ ] Reintroduzir `client_id`/`azp` na chave de consentimento.
- [ ] Escolher definitivamente se `mcp.read` é obrigatório; remover a alternativa contraditória.
- [ ] Separar URI `resource` do valor real de `aud` B2C.
- [ ] Corrigir o diagrama para Cursor → B2C.
- [ ] Trocar chave de usuário de `oid` para `(iss/tenant, oid)`.
- [ ] Documentar que Graph usa credencial própria, não o token MCP.
- [ ] Marcar o multi-JWT MCP na API de Negócio como feature flag não produtiva.
- [ ] Padronizar HMAC com RFC 9421/9530 ou especificar canonicalização completa.
- [ ] Testar replay de nonce em múltiplas réplicas.
- [ ] Validar tokens reais B2C para `aud`, `azp`, `scp`, `tfp`/`acr` e app-only.
- [ ] Definir a solução definitiva: workload token + contexto assinado ou STS.
- [ ] Remover passthrough e audiência MCP da API de Negócio antes da produção.

## Fontes primárias

- [MCP 2026-07-28 — Authorization Security Considerations](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/security-considerations)
- [MCP 2026-07-28 — Authorization](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization)
- [Azure AD B2C — Access tokens e ausência de OBO](https://learn.microsoft.com/en-us/azure/active-directory-b2c/access-tokens)
- [Azure AD B2C — Tipos de aplicação e OBO não suportado](https://learn.microsoft.com/en-us/azure/active-directory-b2c/application-types)
- [Azure AD B2C — Client credentials](https://learn.microsoft.com/en-us/azure/active-directory-b2c/client-credentials-grant-flow)
- [Microsoft Entra ID — OAuth 2.0 On-Behalf-Of](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-on-behalf-of-flow)
- [Microsoft Graph — Acesso app-only](https://learn.microsoft.com/en-us/graph/auth-v2-service)
- [RFC 8693 — OAuth 2.0 Token Exchange](https://www.rfc-editor.org/rfc/rfc8693.html)
- [RFC 9421 — HTTP Message Signatures](https://www.rfc-editor.org/rfc/rfc9421.html)
- [RFC 9530 — Digest Fields](https://www.rfc-editor.org/rfc/rfc9530.html)
