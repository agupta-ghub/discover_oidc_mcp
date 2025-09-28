from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
import json

app = FastAPI(title="OAuth Discovery Helper MCP Server")


# ---------- Models ----------
class DomainRequest(BaseModel):
    domain: str


# ---------- Main Discovery Endpoint ----------
@app.post("/discover_oidc")
def discover_oidc(req: DomainRequest):
    """
    Attempts to find the OIDC discovery metadata for a given domain by probing common well-known URLs.
    """

    # Normalize domain (strip http/https if user passed them)
    domain = req.domain.replace("https://", "").replace("http://", "").strip("/")

    candidates = [
        f"https://{domain}/.well-known/openid-configuration",
        f"https://{domain}/v2.0/.well-known/openid-configuration",
        f"https://{domain}/common/v2.0/.well-known/openid-configuration",
        f"https://{domain}/oauth2/.well-known/openid-configuration",
        f"https://login.{domain}/.well-known/openid-configuration",
        f"https://auth.{domain}/.well-known/openid-configuration",
        f"https://accounts.{domain}/.well-known/openid-configuration",
    ]

    results = []
    for url in candidates:
        try:
            resp = requests.get(url, timeout=4)
            if resp.status_code == 200 and "issuer" in resp.text:
                return resp.json()
            results.append({"url": url, "status": resp.status_code})
        except Exception as e:
            results.append({"url": url, "error": str(e)})

    raise HTTPException(
        status_code=404,
        detail={
            "message": "OIDC Discovery URL not found for this domain.",
            "attempted_urls": results
        }
    )


# ---------- MCP Manifest ----------
@app.get("/mcp-manifest.json")
def get_manifest():
    """
    Serves the MCP manifest required for LLM integration.
    """

    manifest = {
        "schema_version": "v1",
        "name": "OAuth Discovery Helper",
        "description": "Discovers OpenID Connect metadata for a given domain.",
        "contact_email": "you@example.com",
        "capabilities": [
            {
                "name": "discover_oidc",
                "description": "Finds OIDC discovery metadata for a given domain.",
                "url": "/discover_oidc",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "domain": {
                            "type": "string",
                            "description": "Domain to search for OIDC metadata"
                        }
                    },
                    "required": ["domain"]
                },
                "output_schema": {
                    "type": "object",
                    "description": "OIDC metadata as defined in OpenID Connect Discovery 1.0",
                    "additionalProperties": True
                }
            }
        ]
    }

    return manifest


# ---------- Root Endpoint ----------
@app.get("/")
def root():
    return {
        "message": "✅ OAuth Discovery Helper MCP Server is running",
        "docs": "/docs",
        "manifest": "/mcp-manifest.json"
    }
