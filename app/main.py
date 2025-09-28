from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

class DomainRequest(BaseModel):
    domain: str

@app.post("/discover_oidc")
def discover_oidc(req: DomainRequest):
    candidates = [
        f"https://{req.domain}/.well-known/openid-configuration",
        f"https://login.{req.domain}/.well-known/openid-configuration",
        f"https://auth.{req.domain}/.well-known/openid-configuration",
        f"https://accounts.{req.domain}/.well-known/openid-configuration",
    ]

    for url in candidates:
        try:
            resp = requests.get(url, timeout=3)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            continue

    raise HTTPException(status_code=404, detail="OIDC Discovery URL not found for this domain.")
