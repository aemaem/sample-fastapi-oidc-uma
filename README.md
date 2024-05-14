# Sample FastAPI with OIDC and UMA

Sample Application with Python FastAPI and Keycloak with OpenID Connect and User-Managed-Access.

## Run it

1. Start Keycloak: `docker compose up`
2. Setup project: `poetry install && source .venv/bin/activate`
3. Start Sample App: `python sample_fastapi_oidc_uma`
4. Create user in Keycloak and set password.
5. Try out at http://localhost:8080/docs

## Implementations

1. Authentication with OpenID Connect

## Credentials

**Keycloak Admin**

Username: `admin`
Password: `admin`
