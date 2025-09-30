# 🔐 OAuth Discovery Helper MCP Server

A lightweight MCP-compatible FastAPI service that discovers the OpenID Connect metadata for a given domain.

This is currently deployed on Render, using free tier. 

Heads up: Render’s free tier means there’s about a 50-second delay on first request after inactivity (cold start). But hey, it’s free and reliable enough for testing and demos!

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

### Example/test

curl -X POST https://discover-oidc-mcp.onrender.com/discover_oidc \
  -H "Content-Type: application/json" \
  -d '{"domain": "login.microsoftonline.com"}'

```json
{
  "token_endpoint": "https://login.microsoftonline.com/common/oauth2/v2.0/token",
  "token_endpoint_auth_methods_supported": [
    "client_secret_post",
    "private_key_jwt",
    "client_secret_basic"
  ],
  "jwks_uri": "https://login.microsoftonline.com/common/discovery/v2.0/keys",
  "response_modes_supported": ["query", "fragment", "form_post"],
  "subject_types_supported": ["pairwise"],
  "id_token_signing_alg_values_supported": ["RS256"],
  "response_types_supported": [
    "code",
    "id_token",
    "code id_token",
    "id_token token"
  ],
  "scopes_supported": ["openid", "profile", "email", "offline_access"],
  "issuer": "https://login.microsoftonline.com/{tenantid}/v2.0",
  "request_uri_parameter_supported": false,
  "userinfo_endpoint": "https://graph.microsoft.com/oidc/userinfo",
  "authorization_endpoint": "https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
  "device_authorization_endpoint": "https://login.microsoftonline.com/common/oauth2/v2.0/devicecode",
  "http_logout_supported": true,
  "frontchannel_logout_supported": true,
  "end_session_endpoint": "https://login.microsoftonline.com/common/oauth2/v2.0/logout",
  "claims_supported": [
    "sub",
    "iss",
    "cloud_instance_name",
    "cloud_instance_host_name",
    "cloud_graph_host_name",
    "msgraph_host",
    "aud",
    "exp",
    "iat",
    "auth_time",
    "acr",
    "nonce",
    "preferred_username",
    "name",
    "tid",
    "ver",
    "at_hash",
    "c_hash",
    "email"
  ],
  "kerberos_endpoint": "https://login.microsoftonline.com/common/kerberos",
  "cloud_instance_name": "microsoftonline.com",
  "cloud_graph_host_name": "graph.windows.net",
  "msgraph_host": "graph.microsoft.com",
  "rbac_url": "https://pas.windows.net"
}

```
