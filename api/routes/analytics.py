from typing import List, Optional

from fastapi import APIRouter, Query

from api.database import fetch_all
from api.schemas import LiveSalesRow, PlatformSummaryRow


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get(
    "/top-lives",
    response_model=List[LiveSalesRow],
    summary="Get top performing lives",
)
def get_top_lives(
    metric: str = Query(
        "total_revenue",
        description="Ranking metric: total_revenue, conversion_rate, total_comments, paid_carts.",
    ),
    platform: Optional[str] = Query(None, description="Optional platform filter."),
    limit: int = Query(10, ge=1, le=100),
) -> List[LiveSalesRow]:
    """
    Return the top performing lives according to a selected metric.
    """
    allowed_metrics = {
        "total_revenue",
        "conversion_rate",
        "total_comments",
        "paid_carts",
    }

    if metric not in allowed_metrics:
        metric = "total_revenue"

    query = f"""
        SELECT *
        FROM analytics.dataset_final_live_sales
        WHERE (%s IS NULL OR platform = %s)
        ORDER BY {metric} DESC NULLS LAST
        LIMIT %s;
    """

    rows = fetch_all(query, (platform, platform, limit))

    return [LiveSalesRow(**row) for row in rows]


@router.get(
    "/platform-summary",
    response_model=List[PlatformSummaryRow],
    summary="Get analytics summary by platform",
)
def get_platform_summary() -> List[PlatformSummaryRow]:
    """
    Return aggregated indicators by platform.
    """
    query = """
        SELECT
            platform,
            COUNT(*)::int AS live_count,
            COALESCE(SUM(total_revenue), 0)::float AS total_revenue,
            COALESCE(AVG(total_revenue), 0)::float AS average_revenue,
            COALESCE(AVG(conversion_rate), 0)::float AS average_conversion_rate,
            COALESCE(SUM(total_comments), 0)::int AS total_comments,
            COALESCE(SUM(total_carts), 0)::int AS total_carts,
            COALESCE(SUM(total_orders), 0)::int AS total_orders
        FROM analytics.dataset_final_live_sales
        GROUP BY platform
        ORDER BY total_revenue DESC;
    """

    rows = fetch_all(query)

    return [PlatformSummaryRow(**row) for row in rows]


@router.get(
    "/conversion-insights",
    response_model=List[LiveSalesRow],
    summary="Get lives with the best conversion rates",
)
def get_conversion_insights(
    min_peak_viewers: int = Query(1, ge=0),
    limit: int = Query(10, ge=1, le=100),
) -> List[LiveSalesRow]:
    """
    Return lives with the highest conversion rates.
    """
    query = """
        SELECT *
        FROM analytics.dataset_final_live_sales
        WHERE peak_viewers >= %s
        ORDER BY conversion_rate DESC NULLS LAST, total_revenue DESC NULLS LAST
        LIMIT %s;
    """

    rows = fetch_all(query, (min_peak_viewers, limit))

    return [LiveSalesRow(**row) for row in rows]