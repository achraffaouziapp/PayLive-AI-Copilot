from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import analytics, health, lives, sellers
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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
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