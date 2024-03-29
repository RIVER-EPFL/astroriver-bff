# astroriver-bff
The backend-for-frontend (BFF) API for the astroriver project.

## Application relationships

The resources required in this API require the database and endpoints served
by:

- [river-api](https://github.com/RIVER-EPFL/river-api)

and supports the following applications:

- [astroriver-ui](https://github.com/RIVER-EPFL/astroriver-ui)

## Getting started

The app requires the following environment variables:
```
KEYCLOAK_REALM
KEYCLOAK_URL

KEYCLOAK_CLIENT_ID   # The UI client ID

KEYCLOAK_BFF_ID      # The BFF client ID
KEYCLOAK_BFF_SECRET  # The BFF client's secret
```

To start the app run:

```
KEYCLOAK_CLIENT_ID=test \
    KEYCLOAK_BFF_ID=test \
    KEYCLOAK_BFF_SECRET=test \
    KEYCLOAK_REALM=realmtest \
    KEYCLOAK_URL=https://test.com \
    poetry run uvicorn app.main:app --reload
```

There will be a route available at"

```
http://127.0.0.1:8000/config/keycloak
```
