from typing import Optional, List
from datetime import date, datetime

from pydantic import BaseModel, Field


# -------------------------------------------------------------------
# API response schemas
# -------------------------------------------------------------------
# These schemas document the JSON responses returned by the FastAPI app.
# -------------------------------------------------------------------


class HealthResponse(BaseModel):
    """
    Health check response.
    """

    status: str
    application: str
    database_available: bool
    database_name: Optional[str] = None


class LiveSalesRow(BaseModel):
    """
    Final AI dataset row.

    One row represents one live session.
    """

    live_id: str
    seller_id: str
    shop_name: Optional[str] = None
    seller_country: Optional[str] = None
    main_platform: Optional[str] = None
    seller_status: Optional[str] = None
    platform: Optional[str] = None
    live_title: Optional[str] = None
    live_status: Optional[str] = None
    live_date: Optional[date] = None
    peak_viewers: Optional[int] = None
    currency: Optional[str] = None

    total_comments: Optional[int] = None
    purchase_intent_comments: Optional[int] = None
    product_question_comments: Optional[int] = None
    payment_question_comments: Optional[int] = None
    shipping_question_comments: Optional[int] = None
    other_comments: Optional[int] = None
    unknown_intent_comments: Optional[int] = None
    unique_comment_customers: Optional[int] = None
    purchase_intent_rate: Optional[float] = None

    total_carts: Optional[int] = None
    paid_carts: Optional[int] = None
    abandoned_carts: Optional[int] = None
    open_carts: Optional[int] = None
    cancelled_carts: Optional[int] = None
    unique_cart_customers: Optional[int] = None
    cart_abandonment_rate: Optional[float] = None
    comment_to_cart_rate: Optional[float] = None

    total_orders: Optional[int] = None
    paid_orders: Optional[int] = None
    confirmed_orders: Optional[int] = None
    pending_orders: Optional[int] = None
    cancelled_orders: Optional[int] = None
    refunded_orders: Optional[int] = None
    total_order_amount: Optional[float] = None
    average_order_amount: Optional[float] = None

    total_payments: Optional[int] = None
    successful_payments: Optional[int] = None
    failed_payments: Optional[int] = None
    pending_payments: Optional[int] = None
    cancelled_payments: Optional[int] = None
    refunded_payments: Optional[int] = None
    total_revenue: Optional[float] = None
    payment_success_rate: Optional[float] = None

    conversion_rate: Optional[float] = None
    revenue_per_viewer: Optional[float] = None
    revenue_per_order: Optional[float] = None

    total_products_presented: Optional[int] = None
    total_initial_stock: Optional[float] = None
    total_remaining_stock: Optional[float] = None
    estimated_sold_quantity: Optional[float] = None
    average_live_product_price: Optional[float] = None
    top_product_category: Optional[str] = None

    total_events: Optional[int] = None
    comment_event_count: Optional[int] = None
    cart_opened_events: Optional[int] = None
    payment_clicked_events: Optional[int] = None
    payment_succeeded_events: Optional[int] = None
    api_error_events: Optional[int] = None
    product_view_events: Optional[int] = None
    unique_event_customers: Optional[int] = None

    final_dataset_created_at: Optional[datetime] = None
    final_dataset_status: Optional[str] = None


class SellerRow(BaseModel):
    """
    Seller response.
    """

    seller_id: str
    shop_name: Optional[str] = None
    country: Optional[str] = None
    main_platform: Optional[str] = None
    seller_status: Optional[str] = None
    created_at: Optional[datetime] = None


class PlatformSummaryRow(BaseModel):
    """
    Platform-level analytics response.
    """

    platform: str
    live_count: int
    total_revenue: float
    average_revenue: float
    average_conversion_rate: float
    total_comments: int
    total_carts: int
    total_orders: int


class SellerSummaryRow(BaseModel):
    """
    Seller-level analytics response.
    """

    seller_id: str
    shop_name: Optional[str] = None
    live_count: int
    total_revenue: float
    average_revenue: float
    average_conversion_rate: float


class MessageResponse(BaseModel):
    """
    Generic message response.
    """

    message: str = Field(..., example="Operation completed successfully.")