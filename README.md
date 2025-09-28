# 🔐 OAuth Discovery Helper MCP Server

A lightweight MCP-compatible FastAPI service that discovers the OpenID Connect metadata for a given domain.

---

## 📦 API Endpoint

### `POST /discover_oidc`

Returns discovery metadata from a known `.well-known/openid-configuration` path.

#### Request

```json
{ "domain": "login.microsoftonline.com" }
```

#### Response

```json
{
  "issuer": "https://login.microsoftonline.com/common/v2.0",
  "authorization_endpoint": "...",
  "token_endpoint": "...",
  "jwks_uri": "...",
  ...
}
```

### MCP Manifest

The manifest is served at:

GET /mcp-manifest.json
