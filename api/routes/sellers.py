from typing import List

from fastapi import APIRouter, HTTPException, Query, status

from api.database import fetch_all, fetch_one
from api.schemas import LiveSalesRow, SellerRow, SellerSummaryRow


router = APIRouter(
    prefix="/sellers",
    tags=["Sellers"],
)


@router.get(
    "",
    response_model=List[SellerRow],
    summary="List sellers",
)
def list_sellers(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
) -> List[SellerRow]:
    """
    Return sellers from the cleaned core schema.
    """
    query = """
        SELECT
            seller_id,
            shop_name,
            country,
            main_platform,
            seller_status,
            created_at
        FROM core.sellers
        ORDER BY seller_id
        LIMIT %s OFFSET %s;
    """

    rows = fetch_all(query, (limit, offset))

    return [SellerRow(**row) for row in rows]


@router.get(
    "/{seller_id}/lives",
    response_model=List[LiveSalesRow],
    summary="List final live analytics rows for one seller",
)
def list_seller_lives(
    seller_id: str,
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
) -> List[LiveSalesRow]:
    """
    Return final live analytics rows for a specific seller.
    """
    seller = fetch_one(
        """
        SELECT seller_id
        FROM core.sellers
        WHERE seller_id = %s;
        """,
        (seller_id,),
    )

    if seller is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Seller not found: {seller_id}",
        )

    rows = fetch_all(
        """
        SELECT *
        FROM analytics.dataset_final_live_sales
        WHERE seller_id = %s
        ORDER BY live_date DESC NULLS LAST, total_revenue DESC NULLS LAST
        LIMIT %s OFFSET %s;
        """,
        (seller_id, limit, offset),
    )

    return [LiveSalesRow(**row) for row in rows]


@router.get(
    "/summary/performance",
    response_model=List[SellerSummaryRow],
    summary="Get seller performance summary",
)
def seller_performance_summary(
    limit: int = Query(20, ge=1, le=100),
) -> List[SellerSummaryRow]:
    """
    Return seller-level performance indicators from the final dataset.
    """
    query = """
        SELECT
            seller_id,
            MAX(shop_name) AS shop_name,
            COUNT(*)::int AS live_count,
            COALESCE(SUM(total_revenue), 0)::float AS total_revenue,
            COALESCE(AVG(total_revenue), 0)::float AS average_revenue,
            COALESCE(AVG(conversion_rate), 0)::float AS average_conversion_rate
        FROM analytics.dataset_final_live_sales
        GROUP BY seller_id
        ORDER BY total_revenue DESC
        LIMIT %s;
    """

    rows = fetch_all(query, (limit,))

    return [SellerSummaryRow(**row) for row in rows]