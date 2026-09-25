# Ícones em conectores MCP customizados (2026-07-28)

Este texto mostra como um conector customizado publica o **ícone do servidor** pelo MCP e como conferir isso no fio antes de avaliar o resultado visual no cliente.

O alvo do teste é `Implementation.icons`: o identificador visual do conector. Isso é distinto dos ícones opcionais de ferramenta, recurso ou prompt (`Tool.icons`, `Resource.icons`, `Prompt.icons`).

O cliente que renderiza ícones lê o ícone do conector em `_meta["io.modelcontextprotocol/serverInfo"].icons`. O servidor **deve** (`MUST`) implementar `server/discover`. O cliente **pode** (`MAY`) chamá-lo antes de outras RPCs. O servidor **deve, por recomendação** (`SHOULD`), incluir `io.modelcontextprotocol/serverInfo` no `_meta` de cada resultado — inclusive `server/discover`, `tools/list`, `resources/list` e `prompts/list`.

Fontes: [descoberta](https://modelcontextprotocol.io/specification/2026-07-28/server/discover), [`_meta` e `icons`](https://modelcontextprotocol.io/specification/2026-07-28/basic/index), [schema](https://modelcontextprotocol.io/specification/2026-07-28/schema).

## 1. Campos do ícone

O campo `icons` fica no bloco `Implementation` (`serverInfo`), com a estrutura da especificação de ícones ([SEP-973](https://modelcontextprotocol.io/seps/973-expose-additional-metadata-for-implementations-res); [schema `Icon`](https://modelcontextprotocol.io/specification/2026-07-28/schema)):

| Campo | Obrigatório | Descrição |
|---|---|---|
| `src` | sim | URI HTTPS ou `data:` da imagem |
| `mimeType` | não | ex.: `image/png`, `image/svg+xml` |
| `sizes` | não | ex.: `["128x128"]`, `["any"]` |
| `theme` | não | `light` ou `dark` |

No SDK C#, a propriedade é `Icon.Source` e serializa como `src`. Clientes que renderizam ícones **devem** (`MUST`) aceitar `image/png` e `image/jpeg`; **devem, por recomendação** (`SHOULD`), aceitar `image/svg+xml` e `image/webp`. O consumidor **deve** (`MUST`) buscar o `src` sem credenciais (`Authorization`, cookies ou credenciais de cliente).

O SDK não faz *bind* automático de `appsettings.json` para `Implementation`. O conector declara `icons` no registro do servidor; URLs, nome e versão vêm de `IConfiguration`.

## 2. Contrato a conferir no teste

Requisição a `server/discover`. O cabeçalho `MCP-Protocol-Version` **deve** (`MUST`) coincidir com `_meta["io.modelcontextprotocol/protocolVersion"]`. `Mcp-Method` **deve** (`MUST`) coincidir com `method`. `protocolVersion` e `clientCapabilities` são obrigatórios no `_meta` da requisição.

Fontes: [Streamable HTTP](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http), [descoberta](https://modelcontextprotocol.io/specification/2026-07-28/server/discover).

```http
POST https://<host>/mcp
Content-Type: application/json
MCP-Protocol-Version: 2026-07-28
Mcp-Method: server/discover
Authorization: Bearer <token>

{"jsonrpc":"2.0","id":1,"method":"server/discover","params":{"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientCapabilities":{}}}}
```

Resposta esperada (contrato do teste, não captura de servidor real):

```json
{"jsonrpc":"2.0","id":1,"result":{
  "resultType":"complete",
  "supportedVersions":["2026-07-28"],
  "capabilities":{"tools":{}},
  "_meta":{"io.modelcontextprotocol/serverInfo":{
    "name":"mcp-b3i",
    "title":"B3 – Área do Investidor",
    "version":"1.0.0",
    "websiteUrl":"https://www.b3.com.br",
    "icons":[
      {"src":"https://<host>/assets/b3-128-light.png","mimeType":"image/png","sizes":["128x128"],"theme":"light"},
      {"src":"https://<host>/assets/b3-128-dark.png","mimeType":"image/png","sizes":["128x128"],"theme":"dark"}
    ]
  }}
}}
```

Em `tools/list`, conferir o **mesmo** bloco em `result._meta["io.modelcontextprotocol/serverInfo"].icons`. Não confundir com `result.tools[].icons`, que é o ícone da ferramenta, não do conector. Fonte: [tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools).

## 3. Conector de teste — .NET 10, SDK C# v2.0

### `McpServer.csproj`

```xml
<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
    <Nullable>enable</Nullable>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="ModelContextProtocol.AspNetCore" Version="2.0.0" />
  </ItemGroup>
  <ItemGroup>
    <None Update="wwwroot\icon-light.png"><CopyToOutputDirectory>PreserveNewest</CopyToOutputDirectory></None>
    <None Update="wwwroot\icon-dark.png"><CopyToOutputDirectory>PreserveNewest</CopyToOutputDirectory></None>
  </ItemGroup>
</Project>
```

### `appsettings.json`

```json
{
  "ServerBranding": {
    "WebsiteUrl": "https://example.com",
    "IconLightUrl": "https://mcp.example.com/assets/icon-light.png",
    "IconDarkUrl": "https://mcp.example.com/assets/icon-dark.png"
  },
  "McpServerInfo": {
    "Name": "my-mcp-server",
    "Title": "Meu Servidor MCP",
    "Version": "1.0.0"
  }
}
```

Use `appsettings.Production.json` para sobrescrever essas URLs por ambiente (homologação vs. produção), mantendo o `Program.cs` idêntico entre eles.

### `Program.cs`

```csharp
using ModelContextProtocol.Protocol;

var builder = WebApplication.CreateBuilder(args);

var branding = builder.Configuration.GetSection("ServerBranding");
var info = builder.Configuration.GetSection("McpServerInfo");

builder.Services.AddMcpServer(options =>
{
    options.ServerInfo = new Implementation
    {
        Name = info["Name"]!,
        Title = info["Title"],
        Version = info["Version"]!,
        WebsiteUrl = branding["WebsiteUrl"],
        Icons =
        [
            new Icon
            {
                Source = branding["IconLightUrl"]!,
                MimeType = "image/png",
                Sizes = ["128x128"],
                Theme = "light"
            },
            new Icon
            {
                Source = branding["IconDarkUrl"]!,
                MimeType = "image/png",
                Sizes = ["128x128"],
                Theme = "dark"
            }
        ]
    };
})
.WithHttpTransport()
.WithToolsFromAssembly();

var app = builder.Build();

app.MapMcp("/mcp");

app.Run();
```

`options.ServerInfo.Icons` é o que o conector publica. O SDK coloca esse bloco em `server/discover` e, por recomendação da revisão 2026-07-28, no `_meta` de cada resultado. Fontes: [`McpServerOptions.ServerInfo`](https://csharp.sdk.modelcontextprotocol.io/v2/api/ModelContextProtocol.Server.McpServerOptions.html), [`Implementation`](https://csharp.sdk.modelcontextprotocol.io/v2/api/ModelContextProtocol.Protocol.Implementation.html), [`Icon`](https://csharp.sdk.modelcontextprotocol.io/v2/api/ModelContextProtocol.Protocol.Icon.html), [transporte HTTP](https://csharp.sdk.modelcontextprotocol.io/v2/concepts/transports/transports.html).

## 4. Roteiro do teste

1. Adicionar `ModelContextProtocol.AspNetCore` v2.0.0 ou superior ao `.csproj`, com `TargetFramework` `net10.0`.
2. Criar as seções `ServerBranding` e `McpServerInfo` em `appsettings.json` e no `appsettings.Production.json` correspondente, com as URLs corretas por ambiente. Não hardcodar URLs no código.
3. No `Program.cs`, montar `options.ServerInfo = new Implementation { ... Icons = [...] }` lendo os valores de `IConfiguration`, como no exemplo da seção 3.
4. Colocar os arquivos de imagem (PNG, 128×128, variante clara e escura) em `wwwroot/`, e servi-los **sem autenticação**. O cliente **deve** (`MUST`) buscar o `src` sem token.
5. Subir o conector e chamar `server/discover` (`curl` ou Postman) com o contrato da seção 2. Confirmar `_meta["io.modelcontextprotocol/serverInfo"].icons` com `src`, `mimeType`, `sizes` e `theme`, e que o `Content-Type` da imagem bate com o `mimeType`.
6. Repetir em `tools/list` e confirmar o mesmo bloco em `result._meta["io.modelcontextprotocol/serverInfo"].icons` — não em `result.tools[].icons`.
7. No cliente, conferir a variante clara e a escura. Ícones podem ficar em cache no host: orientação operacional é remover e readicionar o conector customizado antes de avaliar o visual. Isso **não** é requisito do protocolo.

## 5. O que encerra o teste

O fio confirma que o conector publicou os ícones do servidor em `_meta["io.modelcontextprotocol/serverInfo"].icons`. A tela só confirma se aquele cliente lê esse campo na revisão 2026-07-28. Os dois resultados entram no registro do teste, por cliente.

## 6. Referências técnicas

Protocolo (modelcontextprotocol.io, revisão 2026-07-28):

- [`_meta`, `icons` e `Implementation`](https://modelcontextprotocol.io/specification/2026-07-28/basic/index)
- [Schema (`Icon`, `Implementation`, `RequestMetaObject`)](https://modelcontextprotocol.io/specification/2026-07-28/schema)
- [`server/discover`](https://modelcontextprotocol.io/specification/2026-07-28/server/discover)
- [Streamable HTTP (`MCP-Protocol-Version`, `Mcp-Method`)](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)
- [`tools/list` e ícones de ferramenta](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
- [SEP-973 — metadados de implementação, recurso, ferramenta e prompt](https://modelcontextprotocol.io/seps/973-expose-additional-metadata-for-implementations-res)

SDK C# v2 (csharp.sdk.modelcontextprotocol.io):

- [`McpServerOptions.ServerInfo`](https://csharp.sdk.modelcontextprotocol.io/v2/api/ModelContextProtocol.Server.McpServerOptions.html)
- [`Implementation` (`Icons`, `WebsiteUrl`, `Title`)](https://csharp.sdk.modelcontextprotocol.io/v2/api/ModelContextProtocol.Protocol.Implementation.html)
- [`Icon` (`Source`, `MimeType`, `Sizes`, `Theme`)](https://csharp.sdk.modelcontextprotocol.io/v2/api/ModelContextProtocol.Protocol.Icon.html)
- [Transporte HTTP (`AddMcpServer`, `WithHttpTransport`, `MapMcp`)](https://csharp.sdk.modelcontextprotocol.io/v2/concepts/transports/transports.html)
