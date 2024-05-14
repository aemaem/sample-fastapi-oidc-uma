from contextlib import asynccontextmanager
from typing import Any

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.security import OpenIdConnect
from keycloak import KeycloakOpenID
from keycloak.urls_patterns import URL_WELL_KNOWN
from loguru import logger
from pydantic import BaseModel

keycloak = KeycloakOpenID(
    server_url="http://localhost:8088/",
    realm_name="Sample",
    client_id="sample-app",
    client_secret_key="v9NZCoutf5ZR9WPM46tAMckbzV5UYRAK",
)
oidc = OpenIdConnect(
    openIdConnectUrl=keycloak.connection.base_url
    + URL_WELL_KNOWN.format(**{"realm-name": keycloak.realm_name})
)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    oidc_config = keycloak.well_known()
    logger.debug(f"Got OpenID Connect endpoints:\n{oidc_config}")
    logger.info("HTTP server up and running")
    yield
    logger.info("Application shutting down")


app = FastAPI(
    lifespan=lifespan,
    swagger_ui_init_oauth={
        "usePkceWithAuthorizationCodeGrant": True,
        "clientId": keycloak.client_id,
        "clientSecret": keycloak.client_secret_key,
    },
)


@app.get("/health")
def route_health():
    return {"status": "UP"}


class LoginReq(BaseModel):
    username: str
    password: str


@app.post("/login")
def route_login(req: LoginReq) -> dict[str, Any]:
    return keycloak.token(req.username, req.password)


@app.get("/read", dependencies=[Depends(oidc)])
def route_read() -> dict[str, Any]:
    return {"resource": "Foo"}


@app.post("/write")
def route_write() -> dict[str, Any]:
    raise NotImplementedError


@app.delete("/delete")
def route_delete() -> dict[str, Any]:
    raise NotImplementedError


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
