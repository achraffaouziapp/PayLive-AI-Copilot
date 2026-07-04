from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query, status

from api.database import fetch_all, fetch_one
from api.schemas import LiveSalesRow


router = APIRouter(
    prefix="/lives",
    tags=["Lives"],
)


@router.get(
    "",
    response_model=List[LiveSalesRow],
    summary="List final live sales analytics rows",
)
def list_lives(
    platform: Optional[str] = Query(None, description="Filter by platform."),
    seller_id: Optional[str] = Query(None, description="Filter by seller identifier."),
    min_revenue: Optional[float] = Query(None, ge=0, description="Minimum total revenue."),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of rows."),
    offset: int = Query(0, ge=0, description="Pagination offset."),
) -> List[LiveSalesRow]:
    """
    Return live analytics rows from the final AI dataset.

    Optional filters:
    - platform;
    - seller_id;
    - minimum revenue.
    """
    query = """
        SELECT *
        FROM analytics.dataset_final_live_sales
        WHERE (%s IS NULL OR platform = %s)
          AND (%s IS NULL OR seller_id = %s)
          AND (%s IS NULL OR total_revenue >= %s)
        ORDER BY live_date DESC NULLS LAST, total_revenue DESC NULLS LAST
        LIMIT %s OFFSET %s;
    """

    rows = fetch_all(
        query,
        (
            platform,
            platform,
            seller_id,
            seller_id,
            min_revenue,
            min_revenue,
            limit,
            offset,
        ),
    )

    return [LiveSalesRow(**row) for row in rows]


@router.get(
    "/{live_id}",
    response_model=LiveSalesRow,
    summary="Get one live analytics row by live_id",
)
def get_live_by_id(live_id: str) -> LiveSalesRow:
    """
    Return one final dataset row by live identifier.
    """
    query = """
        SELECT *
        FROM analytics.dataset_final_live_sales
        WHERE live_id = %s;
    """

    row = fetch_one(query, (live_id,))

    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Live not found: {live_id}",
        )

    return LiveSalesRow(**row)