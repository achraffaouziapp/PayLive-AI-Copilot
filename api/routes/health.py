from fastapi import APIRouter

from api.database import check_database_connection
from api.schemas import HealthResponse


router = APIRouter(
    tags=["Health"],
)


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Check API and database health",
)
def health_check() -> HealthResponse:
    """
    Check if the API is running and if PostgreSQL is reachable.
    """
    database_status = check_database_connection()

    api_status = "ok" if database_status["database_available"] else "degraded"

    return HealthResponse(
        status=api_status,
        application="PayLive AI Copilot API",
        database_available=database_status["database_available"],
        database_name=database_status.get("database_name"),
    )