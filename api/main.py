import os

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import health, lives, sellers, analytics, ai
from api.security import require_api_key


# -------------------------------------------------------------------
# PayLive AI Copilot REST API
# -------------------------------------------------------------------
# This FastAPI application exposes cleaned and aggregated PayLive data
# stored in PostgreSQL.
#
# Public endpoint:
# - GET /health
#
# Protected endpoints:
# - /api/v1/lives
# - /api/v1/sellers
# - /api/v1/analytics
# -------------------------------------------------------------------


def get_allowed_origins() -> list[str]:
    """
    Return the list of frontend origins allowed to call the API.

    In development, the local frontend origins are allowed by default.
    In staging/pre-production, ALLOWED_ORIGINS must contain the public
    frontend URL, for example:
    https://paylive-ai-preprod.onrender.com
    """
    raw_origins = os.getenv(
        "ALLOWED_ORIGINS",
        "http://127.0.0.1:8080,http://localhost:8080",
    )

    return [
        origin.strip().rstrip("/")
        for origin in raw_origins.split(",")
        if origin.strip()
    ]


ALLOWED_ORIGINS = get_allowed_origins()


app = FastAPI(
    title="PayLive AI Copilot API",
    description=(
        "REST API exposing cleaned and aggregated live commerce data "
        "for the PayLive AI Copilot project."
    ),
    version="1.0.0",
    contact={
        "name": "PayLive AI Copilot Project",
    },
    openapi_tags=[
        {
            "name": "Health",
            "description": "API and database health checks.",
        },
        {
            "name": "Lives",
            "description": "Endpoints exposing final live sales analytics data.",
        },
        {
            "name": "Sellers",
            "description": "Endpoints exposing sellers and seller-level analytics.",
        },
        {
            "name": "Analytics",
            "description": "Aggregated analytics endpoints for live commerce performance.",
        },
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "X-API-Key"],
)


app.include_router(health.router)

app.include_router(
    lives.router,
    prefix="/api/v1",
    dependencies=[Depends(require_api_key)],
)

app.include_router(
    sellers.router,
    prefix="/api/v1",
    dependencies=[Depends(require_api_key)],
)

app.include_router(
    analytics.router,
    prefix="/api/v1",
    dependencies=[Depends(require_api_key)],
)

app.include_router(ai.router, prefix="/api/v1/ai", tags=["AI service"])


@app.get("/", tags=["Health"])
def root() -> dict:
    """
    Return a simple API welcome message.
    """
    return {
        "application": "PayLive AI Copilot API",
        "version": "1.0.0",
        "documentation_url": "/docs",
        "health_url": "/health",
    }
