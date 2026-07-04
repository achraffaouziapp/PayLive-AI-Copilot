from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import hashlib
import logging

import pandas as pd


# -------------------------------------------------------------------
# Final AI dataset aggregation
# -------------------------------------------------------------------
# This script builds the final analytical dataset for the PayLive AI
# Copilot project.
#
# It reads cleaned datasets from data/processed/clean and creates one
# final dataset in data/processed/final with one row per live session.
#
# The final dataset contains:
# - live information;
# - seller information;
# - comment indicators;
# - cart indicators;
# - order indicators;
# - payment indicators;
# - product indicators;
# - live event indicators;
# - business ratios useful for future AI tasks.
#
# This script does not train an AI model.
# It prepares the feature dataset that will be reused later in Bloc 2.
# -------------------------------------------------------------------


BASE_DIR = Path(__file__).resolve().parents[2]

PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_CLEAN_DIR = PROCESSED_DIR / "clean"
PROCESSED_FINAL_DIR = PROCESSED_DIR / "final"

PROCESSED_REPORTS_DIR = PROCESSED_DIR / "reports"
FINAL_DATASET_REPORTS_DIR = PROCESSED_REPORTS_DIR / "final_dataset"

LOG_DIR = BASE_DIR / "logs"

LOG_FILE = LOG_DIR / "build_final_ai_dataset.log"

FINAL_DATASET_PATH = PROCESSED_FINAL_DIR / "dataset_final_live_sales.csv"
FINAL_MANIFEST_PATH = FINAL_DATASET_REPORTS_DIR / "final_dataset_manifest.csv"
FINAL_QUALITY_REPORT_PATH = FINAL_DATASET_REPORTS_DIR / "final_dataset_quality_report.csv"
FINAL_AGGREGATION_REPORT_PATH = FINAL_DATASET_REPORTS_DIR / "final_dataset_aggregation_report.csv"


CLEAN_DATASETS = {
    "sellers": "sellers_clean.csv",
    "customers": "customers_clean.csv",
    "products": "products_clean.csv",
    "live_sessions": "live_sessions_clean.csv",
    "live_products": "live_products_clean.csv",
    "live_comments": "live_comments_clean.csv",
    "carts": "carts_clean.csv",
    "cart_items": "cart_items_clean.csv",
    "orders": "orders_clean.csv",
    "payments": "payments_clean.csv",
    "stock_movements": "stock_movements_clean.csv",
    "live_events": "live_events_clean.csv",
}


COMMENT_INTENT_COLUMNS = {
    "purchase_intent": "purchase_intent_comments",
    "product_question": "product_question_comments",
    "payment_question": "payment_question_comments",
    "shipping_question": "shipping_question_comments",
    "other": "other_comments",
    "unknown": "unknown_intent_comments",
}


CART_STATUS_COLUMNS = {
    "paid": "paid_carts",
    "abandoned": "abandoned_carts",
    "open": "open_carts",
    "cancelled": "cancelled_carts",
}


ORDER_STATUS_COLUMNS = {
    "paid": "paid_orders",
    "confirmed": "confirmed_orders",
    "pending": "pending_orders",
    "cancelled": "cancelled_orders",
    "refunded": "refunded_orders",
}


PAYMENT_STATUS_COLUMNS = {
    "succeeded": "successful_payments",
    "failed": "failed_payments",
    "pending": "pending_payments",
    "cancelled": "cancelled_payments",
    "refunded": "refunded_payments",
}


EVENT_TYPE_COLUMNS = {
    "comment_sent": "comment_event_count",
    "cart_opened": "cart_opened_events",
    "payment_clicked": "payment_clicked_events",
    "payment_succeeded": "payment_succeeded_events",
    "api_error": "api_error_events",
    "product_viewed": "product_view_events",
}


FINAL_COLUMN_ORDER = [
    "live_id",
    "seller_id",
    "shop_name",
    "seller_country",
    "main_platform",
    "seller_status",
    "platform",
    "live_title",
    "live_status",
    "live_date",
    "peak_viewers",
    "currency",
    "total_comments",
    "purchase_intent_comments",
    "product_question_comments",
    "payment_question_comments",
    "shipping_question_comments",
    "other_comments",
    "unknown_intent_comments",
    "unique_comment_customers",
    "purchase_intent_rate",
    "total_carts",
    "paid_carts",
    "abandoned_carts",
    "open_carts",
    "cancelled_carts",
    "unique_cart_customers",
    "cart_abandonment_rate",
    "comment_to_cart_rate",
    "total_orders",
    "paid_orders",
    "confirmed_orders",
    "pending_orders",
    "cancelled_orders",
    "refunded_orders",
    "total_order_amount",
    "average_order_amount",
    "total_payments",
    "successful_payments",
    "failed_payments",
    "pending_payments",
    "cancelled_payments",
    "refunded_payments",
    "total_revenue",
    "payment_success_rate",
    "conversion_rate",
    "revenue_per_viewer",
    "revenue_per_order",
    "total_products_presented",
    "total_initial_stock",
    "total_remaining_stock",
    "estimated_sold_quantity",
    "average_live_product_price",
    "top_product_category",
    "total_events",
    "comment_event_count",
    "cart_opened_events",
    "payment_clicked_events",
    "payment_succeeded_events",
    "api_error_events",
    "product_view_events",
    "unique_event_customers",
    "final_dataset_created_at",
    "final_dataset_status",
]

FINAL_INTEGER_COLUMNS = [
    "peak_viewers",
    "total_comments",
    "purchase_intent_comments",
    "product_question_comments",
    "payment_question_comments",
    "shipping_question_comments",
    "other_comments",
    "unknown_intent_comments",
    "unique_comment_customers",
    "total_carts",
    "paid_carts",
    "abandoned_carts",
    "open_carts",
    "cancelled_carts",
    "unique_cart_customers",
    "total_orders",
    "paid_orders",
    "confirmed_orders",
    "pending_orders",
    "cancelled_orders",
    "refunded_orders",
    "total_payments",
    "successful_payments",
    "failed_payments",
    "pending_payments",
    "cancelled_payments",
    "refunded_payments",
    "total_products_presented",
    "total_events",
    "comment_event_count",
    "cart_opened_events",
    "payment_clicked_events",
    "payment_succeeded_events",
    "api_error_events",
    "product_view_events",
    "unique_event_customers",
]

FINAL_FLOAT_COLUMNS = [
    "total_order_amount",
    "average_order_amount",
    "total_revenue",
    "total_initial_stock",
    "total_remaining_stock",
    "estimated_sold_quantity",
    "average_live_product_price",
]


def ensure_directories() -> None:
    """
    Create required folders.
    """
    PROCESSED_CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_FINAL_DIR.mkdir(parents=True, exist_ok=True)
    FINAL_DATASET_REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def setup_logging() -> None:
    """
    Configure logging.
    """
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        encoding="utf-8",
    )


def get_current_timestamp() -> str:
    """
    Return the current timestamp.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def calculate_file_hash(file_path: Path) -> str:
    """
    Calculate the SHA256 hash of a file.
    """
    if not file_path.exists():
        return ""

    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        for block in iter(lambda: file.read(4096), b""):
            sha256.update(block)

    return sha256.hexdigest()


def read_clean_dataset(file_name: str) -> pd.DataFrame:
    """
    Read a cleaned dataset from data/processed/clean.
    """
    file_path = PROCESSED_CLEAN_DIR / file_name

    if not file_path.exists():
        logging.warning("Clean dataset not found: %s", file_path)
        return pd.DataFrame()

    return pd.read_csv(
        file_path,
        dtype=str,
        keep_default_na=False,
        encoding="utf-8",
    )


def load_clean_datasets() -> Dict[str, pd.DataFrame]:
    """
    Load all cleaned datasets.
    """
    datasets = {}

    for dataset_name, file_name in CLEAN_DATASETS.items():
        df = read_clean_dataset(file_name)
        datasets[dataset_name] = df

        logging.info(
            "Loaded dataset %s with %s rows and %s columns.",
            dataset_name,
            len(df),
            len(df.columns),
        )

    return datasets


def ensure_columns(df: pd.DataFrame, columns: List[str], default_value: Any = "") -> pd.DataFrame:
    """
    Ensure that a DataFrame contains required columns.
    """
    df = df.copy()

    for column in columns:
        if column not in df.columns:
            df[column] = default_value

    return df


def to_numeric_series(series: pd.Series, default_value: float = 0.0) -> pd.Series:
    """
    Convert a Series to numeric values.
    """
    numeric_series = pd.to_numeric(series, errors="coerce")
    numeric_series = numeric_series.fillna(default_value)

    return numeric_series


def safe_divide(numerator: Any, denominator: Any) -> float:
    """
    Divide two values safely.

    If the denominator is missing or zero, return 0.
    """
    try:
        numerator_value = float(numerator)
        denominator_value = float(denominator)
    except (TypeError, ValueError):
        return 0.0

    if denominator_value == 0:
        return 0.0

    return round(numerator_value / denominator_value, 4)


def count_unique_non_empty(series: pd.Series) -> int:
    """
    Count unique non-empty values.
    """
    clean_series = series.astype(str).str.strip()
    clean_series = clean_series[clean_series != ""]

    return int(clean_series.nunique())


def most_frequent_value(series: pd.Series, default_value: str = "unknown") -> str:
    """
    Return the most frequent non-empty value of a Series.
    """
    clean_series = series.astype(str).str.strip()
    clean_series = clean_series[clean_series != ""]

    if clean_series.empty:
        return default_value

    return clean_series.value_counts().idxmax()


def build_base_live_dataset(live_sessions_df: pd.DataFrame, sellers_df: pd.DataFrame) -> pd.DataFrame:
    """
    Build the base dataset with one row per live session.
    """
    required_live_columns = [
        "live_id",
        "seller_id",
        "platform",
        "live_title",
        "actual_start_at",
        "scheduled_start_at",
        "live_status",
        "peak_viewers",
        "currency",
    ]

    live_sessions_df = ensure_columns(live_sessions_df, required_live_columns)

    base_df = live_sessions_df[required_live_columns].copy()

    actual_start_dates = pd.to_datetime(
        base_df["actual_start_at"],
        errors="coerce",
    )

    scheduled_start_dates = pd.to_datetime(
        base_df["scheduled_start_at"],
        errors="coerce",
    )

    live_dates = actual_start_dates.combine_first(scheduled_start_dates)

    base_df["live_date"] = live_dates.dt.strftime("%Y-%m-%d")
    base_df["live_date"] = base_df["live_date"].fillna("")

    base_df["peak_viewers"] = to_numeric_series(base_df["peak_viewers"], 0).astype(int)

    base_df = base_df[
        [
            "live_id",
            "seller_id",
            "platform",
            "live_title",
            "live_status",
            "live_date",
            "peak_viewers",
            "currency",
        ]
    ]

    required_seller_columns = [
        "seller_id",
        "shop_name",
        "country",
        "main_platform",
        "seller_status",
    ]

    sellers_df = ensure_columns(sellers_df, required_seller_columns)

    seller_info_df = sellers_df[required_seller_columns].copy()
    seller_info_df = seller_info_df.rename(columns={"country": "seller_country"})

    base_df = base_df.merge(
        seller_info_df,
        on="seller_id",
        how="left",
    )

    base_df = ensure_columns(
        base_df,
        [
            "shop_name",
            "seller_country",
            "main_platform",
            "seller_status",
        ],
    )

    return base_df


def build_comment_aggregation(live_comments_df: pd.DataFrame) -> pd.DataFrame:
    """
    Build comment indicators by live.
    """
    required_columns = [
        "live_id",
        "comment_id",
        "customer_id",
        "manual_intent_label",
    ]

    live_comments_df = ensure_columns(live_comments_df, required_columns)

    if live_comments_df.empty:
        return pd.DataFrame(columns=["live_id"])

    comment_base_df = (
        live_comments_df.groupby("live_id")
        .agg(
            total_comments=("comment_id", "count"),
            unique_comment_customers=("customer_id", count_unique_non_empty),
        )
        .reset_index()
    )

    intent_counts_df = (
        pd.crosstab(
            live_comments_df["live_id"],
            live_comments_df["manual_intent_label"],
        )
        .reset_index()
    )

    for intent_value, output_column in COMMENT_INTENT_COLUMNS.items():
        if intent_value not in intent_counts_df.columns:
            intent_counts_df[intent_value] = 0

        intent_counts_df = intent_counts_df.rename(columns={intent_value: output_column})

    selected_columns = ["live_id"] + list(COMMENT_INTENT_COLUMNS.values())
    intent_counts_df = intent_counts_df[selected_columns]

    return comment_base_df.merge(intent_counts_df, on="live_id", how="left")


def build_cart_aggregation(carts_df: pd.DataFrame) -> pd.DataFrame:
    """
    Build cart indicators by live.
    """
    required_columns = [
        "cart_id",
        "live_id",
        "customer_id",
        "cart_status",
    ]

    carts_df = ensure_columns(carts_df, required_columns)

    if carts_df.empty:
        return pd.DataFrame(columns=["live_id"])

    cart_base_df = (
        carts_df.groupby("live_id")
        .agg(
            total_carts=("cart_id", "count"),
            unique_cart_customers=("customer_id", count_unique_non_empty),
        )
        .reset_index()
    )

    cart_status_counts_df = (
        pd.crosstab(
            carts_df["live_id"],
            carts_df["cart_status"],
        )
        .reset_index()
    )

    for status_value, output_column in CART_STATUS_COLUMNS.items():
        if status_value not in cart_status_counts_df.columns:
            cart_status_counts_df[status_value] = 0

        cart_status_counts_df = cart_status_counts_df.rename(
            columns={status_value: output_column}
        )

    selected_columns = ["live_id"] + list(CART_STATUS_COLUMNS.values())
    cart_status_counts_df = cart_status_counts_df[selected_columns]

    return cart_base_df.merge(cart_status_counts_df, on="live_id", how="left")


def build_order_aggregation(orders_df: pd.DataFrame, carts_df: pd.DataFrame) -> pd.DataFrame:
    """
    Build order indicators by live.

    Orders are linked to lives through carts.
    """
    orders_df = ensure_columns(
        orders_df,
        [
            "order_id",
            "cart_id",
            "order_status",
            "order_amount",
        ],
    )

    carts_df = ensure_columns(
        carts_df,
        [
            "cart_id",
            "live_id",
        ],
    )

    if orders_df.empty or carts_df.empty:
        return pd.DataFrame(columns=["live_id"])

    order_live_df = orders_df.merge(
        carts_df[["cart_id", "live_id"]],
        on="cart_id",
        how="left",
    )

    order_live_df = order_live_df[order_live_df["live_id"].astype(str).str.strip() != ""].copy()
    order_live_df["order_amount"] = to_numeric_series(order_live_df["order_amount"], 0)

    if order_live_df.empty:
        return pd.DataFrame(columns=["live_id"])

    order_base_df = (
        order_live_df.groupby("live_id")
        .agg(
            total_orders=("order_id", "count"),
            total_order_amount=("order_amount", "sum"),
            average_order_amount=("order_amount", "mean"),
        )
        .reset_index()
    )

    order_base_df["total_order_amount"] = order_base_df["total_order_amount"].round(2)
    order_base_df["average_order_amount"] = order_base_df["average_order_amount"].round(2)

    order_status_counts_df = (
        pd.crosstab(
            order_live_df["live_id"],
            order_live_df["order_status"],
        )
        .reset_index()
    )

    for status_value, output_column in ORDER_STATUS_COLUMNS.items():
        if status_value not in order_status_counts_df.columns:
            order_status_counts_df[status_value] = 0

        order_status_counts_df = order_status_counts_df.rename(
            columns={status_value: output_column}
        )

    selected_columns = ["live_id"] + list(ORDER_STATUS_COLUMNS.values())
    order_status_counts_df = order_status_counts_df[selected_columns]

    return order_base_df.merge(order_status_counts_df, on="live_id", how="left")


def build_payment_aggregation(
    payments_df: pd.DataFrame,
    orders_df: pd.DataFrame,
    carts_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build payment indicators by live.

    Payments are linked to lives through orders and carts.
    """
    payments_df = ensure_columns(
        payments_df,
        [
            "payment_id",
            "order_id",
            "payment_status",
            "payment_amount",
        ],
    )

    orders_df = ensure_columns(
        orders_df,
        [
            "order_id",
            "cart_id",
        ],
    )

    carts_df = ensure_columns(
        carts_df,
        [
            "cart_id",
            "live_id",
        ],
    )

    if payments_df.empty or orders_df.empty or carts_df.empty:
        return pd.DataFrame(columns=["live_id"])

    payment_live_df = payments_df.merge(
        orders_df[["order_id", "cart_id"]],
        on="order_id",
        how="left",
    )

    payment_live_df = payment_live_df.merge(
        carts_df[["cart_id", "live_id"]],
        on="cart_id",
        how="left",
    )

    payment_live_df = payment_live_df[
        payment_live_df["live_id"].astype(str).str.strip() != ""
    ].copy()

    payment_live_df["payment_amount"] = to_numeric_series(
        payment_live_df["payment_amount"],
        0,
    )

    if payment_live_df.empty:
        return pd.DataFrame(columns=["live_id"])

    payment_live_df["successful_payment_amount"] = payment_live_df.apply(
        lambda row: row["payment_amount"]
        if row["payment_status"] == "succeeded"
        else 0,
        axis=1,
    )

    payment_base_df = (
        payment_live_df.groupby("live_id")
        .agg(
            total_payments=("payment_id", "count"),
            total_revenue=("successful_payment_amount", "sum"),
        )
        .reset_index()
    )

    payment_base_df["total_revenue"] = payment_base_df["total_revenue"].round(2)

    payment_status_counts_df = (
        pd.crosstab(
            payment_live_df["live_id"],
            payment_live_df["payment_status"],
        )
        .reset_index()
    )

    for status_value, output_column in PAYMENT_STATUS_COLUMNS.items():
        if status_value not in payment_status_counts_df.columns:
            payment_status_counts_df[status_value] = 0

        payment_status_counts_df = payment_status_counts_df.rename(
            columns={status_value: output_column}
        )

    selected_columns = ["live_id"] + list(PAYMENT_STATUS_COLUMNS.values())
    payment_status_counts_df = payment_status_counts_df[selected_columns]

    return payment_base_df.merge(payment_status_counts_df, on="live_id", how="left")


def build_product_aggregation(
    live_products_df: pd.DataFrame,
    products_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build product indicators by live.
    """
    live_products_df = ensure_columns(
        live_products_df,
        [
            "live_id",
            "product_id",
            "special_live_price",
            "initial_stock",
            "remaining_stock",
        ],
    )

    products_df = ensure_columns(
        products_df,
        [
            "product_id",
            "category",
            "unit_price",
        ],
    )

    if live_products_df.empty:
        return pd.DataFrame(columns=["live_id"])

    product_live_df = live_products_df.merge(
        products_df[["product_id", "category", "unit_price"]],
        on="product_id",
        how="left",
    )

    product_live_df["special_live_price"] = to_numeric_series(
        product_live_df["special_live_price"],
        0,
    )

    product_live_df["unit_price"] = to_numeric_series(
        product_live_df["unit_price"],
        0,
    )

    product_live_df["initial_stock"] = to_numeric_series(
        product_live_df["initial_stock"],
        0,
    )

    product_live_df["remaining_stock"] = to_numeric_series(
        product_live_df["remaining_stock"],
        0,
    )

    product_live_df["effective_live_price"] = product_live_df.apply(
        lambda row: row["special_live_price"]
        if row["special_live_price"] > 0
        else row["unit_price"],
        axis=1,
    )

    product_live_df["estimated_sold_quantity_row"] = (
        product_live_df["initial_stock"] - product_live_df["remaining_stock"]
    )

    product_live_df.loc[
        product_live_df["estimated_sold_quantity_row"] < 0,
        "estimated_sold_quantity_row",
    ] = 0

    product_agg_df = (
        product_live_df.groupby("live_id")
        .agg(
            total_products_presented=("product_id", "nunique"),
            total_initial_stock=("initial_stock", "sum"),
            total_remaining_stock=("remaining_stock", "sum"),
            estimated_sold_quantity=("estimated_sold_quantity_row", "sum"),
            average_live_product_price=("effective_live_price", "mean"),
            top_product_category=("category", most_frequent_value),
        )
        .reset_index()
    )

    numeric_columns = [
        "total_initial_stock",
        "total_remaining_stock",
        "estimated_sold_quantity",
        "average_live_product_price",
    ]

    for column in numeric_columns:
        product_agg_df[column] = product_agg_df[column].round(2)

    return product_agg_df


def build_event_aggregation(live_events_df: pd.DataFrame) -> pd.DataFrame:
    """
    Build event indicators by live.
    """
    live_events_df = ensure_columns(
        live_events_df,
        [
            "event_id",
            "live_id",
            "customer_id",
            "event_type",
        ],
    )

    if live_events_df.empty:
        return pd.DataFrame(columns=["live_id"])

    event_base_df = (
        live_events_df.groupby("live_id")
        .agg(
            total_events=("event_id", "count"),
            unique_event_customers=("customer_id", count_unique_non_empty),
        )
        .reset_index()
    )

    event_counts_df = (
        pd.crosstab(
            live_events_df["live_id"],
            live_events_df["event_type"],
        )
        .reset_index()
    )

    for event_type, output_column in EVENT_TYPE_COLUMNS.items():
        if event_type not in event_counts_df.columns:
            event_counts_df[event_type] = 0

        event_counts_df = event_counts_df.rename(columns={event_type: output_column})

    selected_columns = ["live_id"] + list(EVENT_TYPE_COLUMNS.values())
    event_counts_df = event_counts_df[selected_columns]

    return event_base_df.merge(event_counts_df, on="live_id", how="left")


def merge_aggregation(
    final_df: pd.DataFrame,
    aggregation_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Merge one aggregation DataFrame into the final dataset.
    """
    if aggregation_df.empty or "live_id" not in aggregation_df.columns:
        return final_df

    return final_df.merge(aggregation_df, on="live_id", how="left")


def fill_missing_indicator_columns(final_df: pd.DataFrame) -> pd.DataFrame:
    """
    Fill missing indicator columns with default values.

    Integer indicators are explicitly converted to integers to avoid
    PostgreSQL COPY errors such as "3.0" for INTEGER columns.
    """
    final_df = final_df.copy()

    for column in FINAL_INTEGER_COLUMNS:
        if column not in final_df.columns:
            final_df[column] = 0

        final_df[column] = (
            pd.to_numeric(final_df[column], errors="coerce")
            .fillna(0)
            .round(0)
            .astype(int)
        )

    for column in FINAL_FLOAT_COLUMNS:
        if column not in final_df.columns:
            final_df[column] = 0.0

        final_df[column] = (
            pd.to_numeric(final_df[column], errors="coerce")
            .fillna(0.0)
            .round(4)
        )

    if "top_product_category" not in final_df.columns:
        final_df["top_product_category"] = "unknown"

    final_df["top_product_category"] = final_df["top_product_category"].fillna("unknown")
    final_df.loc[
        final_df["top_product_category"].astype(str).str.strip() == "",
        "top_product_category",
    ] = "unknown"

    text_columns = [
        "shop_name",
        "seller_country",
        "main_platform",
        "seller_status",
        "platform",
        "live_title",
        "live_status",
        "live_date",
        "currency",
    ]

    for column in text_columns:
        if column not in final_df.columns:
            final_df[column] = ""

        final_df[column] = final_df[column].fillna("")

    return final_df


def add_business_ratios(final_df: pd.DataFrame) -> pd.DataFrame:
    """
    Add business ratios useful for future AI work.
    """
    final_df = final_df.copy()

    final_df["purchase_intent_rate"] = final_df.apply(
        lambda row: safe_divide(row["purchase_intent_comments"], row["total_comments"]),
        axis=1,
    )

    final_df["cart_abandonment_rate"] = final_df.apply(
        lambda row: safe_divide(row["abandoned_carts"], row["total_carts"]),
        axis=1,
    )

    final_df["comment_to_cart_rate"] = final_df.apply(
        lambda row: safe_divide(row["total_carts"], row["total_comments"]),
        axis=1,
    )

    final_df["payment_success_rate"] = final_df.apply(
        lambda row: safe_divide(row["successful_payments"], row["total_payments"]),
        axis=1,
    )

    final_df["conversion_rate"] = final_df.apply(
        lambda row: safe_divide(row["paid_carts"], row["peak_viewers"]),
        axis=1,
    )

    final_df["revenue_per_viewer"] = final_df.apply(
        lambda row: safe_divide(row["total_revenue"], row["peak_viewers"]),
        axis=1,
    )

    final_df["revenue_per_order"] = final_df.apply(
        lambda row: safe_divide(row["total_revenue"], row["total_orders"]),
        axis=1,
    )

    return final_df


def finalize_column_order(final_df: pd.DataFrame) -> pd.DataFrame:
    """
    Reorder columns in a stable and readable way.
    """
    final_df = final_df.copy()

    final_df["final_dataset_created_at"] = get_current_timestamp()
    final_df["final_dataset_status"] = "ready_for_ai"

    for column in FINAL_COLUMN_ORDER:
        if column not in final_df.columns:
            final_df[column] = ""

    return final_df[FINAL_COLUMN_ORDER]


def build_final_dataset(datasets: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Build the final AI dataset with one row per live.
    """
    base_df = build_base_live_dataset(
        live_sessions_df=datasets["live_sessions"],
        sellers_df=datasets["sellers"],
    )

    comment_agg_df = build_comment_aggregation(datasets["live_comments"])
    cart_agg_df = build_cart_aggregation(datasets["carts"])
    order_agg_df = build_order_aggregation(
        orders_df=datasets["orders"],
        carts_df=datasets["carts"],
    )
    payment_agg_df = build_payment_aggregation(
        payments_df=datasets["payments"],
        orders_df=datasets["orders"],
        carts_df=datasets["carts"],
    )
    product_agg_df = build_product_aggregation(
        live_products_df=datasets["live_products"],
        products_df=datasets["products"],
    )
    event_agg_df = build_event_aggregation(datasets["live_events"])

    final_df = base_df.copy()

    for aggregation_df in [
        comment_agg_df,
        cart_agg_df,
        order_agg_df,
        payment_agg_df,
        product_agg_df,
        event_agg_df,
    ]:
        final_df = merge_aggregation(final_df, aggregation_df)

    final_df = fill_missing_indicator_columns(final_df)
    final_df = add_business_ratios(final_df)
    final_df = finalize_column_order(final_df)

    return final_df


def build_quality_report(final_df: pd.DataFrame) -> pd.DataFrame:
    """
    Build a quality report for the final AI dataset.
    """
    total_cells = int(final_df.shape[0] * final_df.shape[1])
    missing_cells = int(final_df.isna().sum().sum())

    blank_cells = int(
        (final_df.astype(str).apply(lambda column: column.str.strip() == "")).sum().sum()
    )

    duplicate_live_ids = 0
    if "live_id" in final_df.columns:
        duplicate_live_ids = int(final_df["live_id"].duplicated().sum())

    metrics = [
        {
            "metric": "generated_at",
            "value": get_current_timestamp(),
        },
        {
            "metric": "row_count",
            "value": int(len(final_df)),
        },
        {
            "metric": "column_count",
            "value": int(len(final_df.columns)),
        },
        {
            "metric": "total_cells",
            "value": total_cells,
        },
        {
            "metric": "missing_cells",
            "value": missing_cells,
        },
        {
            "metric": "blank_cells",
            "value": blank_cells,
        },
        {
            "metric": "duplicate_live_id_count",
            "value": duplicate_live_ids,
        },
        {
            "metric": "lives_without_comments",
            "value": int((final_df["total_comments"].astype(float) == 0).sum())
            if "total_comments" in final_df.columns
            else 0,
        },
        {
            "metric": "lives_without_carts",
            "value": int((final_df["total_carts"].astype(float) == 0).sum())
            if "total_carts" in final_df.columns
            else 0,
        },
        {
            "metric": "lives_without_orders",
            "value": int((final_df["total_orders"].astype(float) == 0).sum())
            if "total_orders" in final_df.columns
            else 0,
        },
        {
            "metric": "lives_without_revenue",
            "value": int((final_df["total_revenue"].astype(float) == 0).sum())
            if "total_revenue" in final_df.columns
            else 0,
        },
        {
            "metric": "lives_with_zero_peak_viewers",
            "value": int((final_df["peak_viewers"].astype(float) == 0).sum())
            if "peak_viewers" in final_df.columns
            else 0,
        },
        {
            "metric": "negative_revenue_rows",
            "value": int((final_df["total_revenue"].astype(float) < 0).sum())
            if "total_revenue" in final_df.columns
            else 0,
        },
        {
            "metric": "dataset_status",
            "value": "ready_for_ai",
        },
    ]

    return pd.DataFrame(metrics)


def build_manifest(final_df: pd.DataFrame) -> pd.DataFrame:
    """
    Build the final dataset manifest.
    """
    source_files = [
        str(PROCESSED_CLEAN_DIR / file_name)
        for file_name in CLEAN_DATASETS.values()
    ]

    return pd.DataFrame(
        [
            {
                "generated_at": get_current_timestamp(),
                "dataset_name": "dataset_final_live_sales",
                "dataset_type": "final_ai_feature_dataset",
                "output_file": str(FINAL_DATASET_PATH),
                "output_file_hash_sha256": calculate_file_hash(FINAL_DATASET_PATH),
                "row_count": int(len(final_df)),
                "column_count": int(len(final_df.columns)),
                "granularity": "one_row_per_live_session",
                "source_files": " | ".join(source_files),
                "quality_report": str(FINAL_QUALITY_REPORT_PATH),
                "status": "created",
            }
        ]
    )

def build_aggregation_report(
    datasets: Dict[str, pd.DataFrame],
    final_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build a detailed report describing how the final AI dataset was aggregated.

    This report documents:
    - source datasets used;
    - source row counts;
    - aggregation level;
    - indicators created;
    - business purpose of each aggregation.
    """
    rows = [
        {
            "aggregation_step": "base_live_dataset",
            "source_datasets": "live_sessions_clean.csv, sellers_clean.csv",
            "source_row_count": len(datasets["live_sessions"]),
            "aggregation_level": "one row per live_id",
            "created_indicators": "live_date, peak_viewers, seller information",
            "business_purpose": "Create the base analytical dataset with live and seller context.",
        },
        {
            "aggregation_step": "comments_aggregation",
            "source_datasets": "live_comments_clean.csv",
            "source_row_count": len(datasets["live_comments"]),
            "aggregation_level": "group by live_id",
            "created_indicators": (
                "total_comments, purchase_intent_comments, "
                "product_question_comments, payment_question_comments, "
                "shipping_question_comments, unique_comment_customers, "
                "purchase_intent_rate"
            ),
            "business_purpose": "Measure audience engagement and buying intent during each live.",
        },
        {
            "aggregation_step": "carts_aggregation",
            "source_datasets": "carts_clean.csv",
            "source_row_count": len(datasets["carts"]),
            "aggregation_level": "group by live_id",
            "created_indicators": (
                "total_carts, paid_carts, abandoned_carts, open_carts, "
                "cancelled_carts, unique_cart_customers, cart_abandonment_rate"
            ),
            "business_purpose": "Measure commercial engagement and cart behavior.",
        },
        {
            "aggregation_step": "orders_aggregation",
            "source_datasets": "orders_clean.csv, carts_clean.csv",
            "source_row_count": len(datasets["orders"]),
            "aggregation_level": "orders linked to live_id through cart_id",
            "created_indicators": (
                "total_orders, paid_orders, confirmed_orders, pending_orders, "
                "cancelled_orders, refunded_orders, total_order_amount, "
                "average_order_amount"
            ),
            "business_purpose": "Measure order volume and commercial performance per live.",
        },
        {
            "aggregation_step": "payments_aggregation",
            "source_datasets": "payments_clean.csv, orders_clean.csv, carts_clean.csv",
            "source_row_count": len(datasets["payments"]),
            "aggregation_level": "payments linked to live_id through order_id and cart_id",
            "created_indicators": (
                "total_payments, successful_payments, failed_payments, "
                "pending_payments, cancelled_payments, refunded_payments, "
                "total_revenue, payment_success_rate"
            ),
            "business_purpose": "Calculate confirmed revenue and payment reliability per live.",
        },
        {
            "aggregation_step": "products_aggregation",
            "source_datasets": "live_products_clean.csv, products_clean.csv",
            "source_row_count": len(datasets["live_products"]),
            "aggregation_level": "group by live_id",
            "created_indicators": (
                "total_products_presented, total_initial_stock, "
                "total_remaining_stock, estimated_sold_quantity, "
                "average_live_product_price, top_product_category"
            ),
            "business_purpose": "Describe the product offer and stock movement for each live.",
        },
        {
            "aggregation_step": "events_aggregation",
            "source_datasets": "live_events_clean.csv",
            "source_row_count": len(datasets["live_events"]),
            "aggregation_level": "group by live_id",
            "created_indicators": (
                "total_events, comment_event_count, cart_opened_events, "
                "payment_clicked_events, payment_succeeded_events, "
                "api_error_events, product_view_events, unique_event_customers"
            ),
            "business_purpose": "Add behavioral and technical event indicators from the Big Data source.",
        },
        {
            "aggregation_step": "business_ratios",
            "source_datasets": "all aggregated indicators",
            "source_row_count": len(final_df),
            "aggregation_level": "one row per live_id",
            "created_indicators": (
                "conversion_rate, comment_to_cart_rate, purchase_intent_rate, "
                "cart_abandonment_rate, revenue_per_viewer, revenue_per_order"
            ),
            "business_purpose": "Create AI-ready features for future prediction and analysis.",
        },
        {
            "aggregation_step": "final_dataset",
            "source_datasets": "all cleaned datasets",
            "source_row_count": sum(len(df) for df in datasets.values()),
            "aggregation_level": "one row per live_id",
            "created_indicators": f"{len(final_df.columns)} final columns",
            "business_purpose": (
                f"Generate dataset_final_live_sales.csv with {len(final_df)} rows "
                "ready for future AI and analytics tasks."
            ),
        },
    ]

    return pd.DataFrame(rows)



def save_final_outputs(
    final_df: pd.DataFrame,
    datasets: Dict[str, pd.DataFrame],
) -> None:
    """
    Save the final dataset, manifest, quality report and aggregation report.
    """
    final_df.to_csv(FINAL_DATASET_PATH, index=False, encoding="utf-8")

    quality_report_df = build_quality_report(final_df)
    quality_report_df.to_csv(
        FINAL_QUALITY_REPORT_PATH,
        index=False,
        encoding="utf-8",
    )

    aggregation_report_df = build_aggregation_report(
        datasets=datasets,
        final_df=final_df,
    )
    aggregation_report_df.to_csv(
        FINAL_AGGREGATION_REPORT_PATH,
        index=False,
        encoding="utf-8",
    )

    manifest_df = build_manifest(final_df)
    manifest_df.to_csv(
        FINAL_MANIFEST_PATH,
        index=False,
        encoding="utf-8",
    )

    logging.info("Saved final AI dataset: %s", FINAL_DATASET_PATH)
    logging.info("Saved final dataset manifest: %s", FINAL_MANIFEST_PATH)
    logging.info("Saved final dataset quality report: %s", FINAL_QUALITY_REPORT_PATH)
    logging.info("Saved final dataset aggregation report: %s", FINAL_AGGREGATION_REPORT_PATH)


def build_final_ai_dataset() -> pd.DataFrame:
    """
    Run the full final dataset aggregation pipeline.
    """
    logging.info("Starting final AI dataset aggregation.")

    datasets = load_clean_datasets()
    final_df = build_final_dataset(datasets)

    save_final_outputs(final_df, datasets)

    logging.info("Final AI dataset aggregation completed successfully.")

    return final_df


def main() -> None:
    """
    Entry point of the script.
    """
    ensure_directories()
    setup_logging()

    final_df = build_final_ai_dataset()

    quality_report_df = pd.read_csv(FINAL_QUALITY_REPORT_PATH)
    manifest_df = pd.read_csv(FINAL_MANIFEST_PATH)
    aggregation_report_df = pd.read_csv(FINAL_AGGREGATION_REPORT_PATH)

    print("Final AI dataset aggregation completed successfully.")
    print(f"Final dataset: {FINAL_DATASET_PATH}")
    print(f"Final manifest: {FINAL_MANIFEST_PATH}")
    print(f"Final quality report: {FINAL_QUALITY_REPORT_PATH}")
    print(f"Final aggregation report: {FINAL_AGGREGATION_REPORT_PATH}")
    print(f"Log file: {LOG_FILE}")
    print("")
    print("Final dataset shape:")
    print(f"- rows: {len(final_df)}")
    print(f"- columns: {len(final_df.columns)}")
    print("")
    print("Manifest:")
    print(manifest_df.to_string(index=False))
    print("")
    print("Quality report:")
    print(quality_report_df.to_string(index=False))
    print("")
    print("Aggregation report:")
    print(aggregation_report_df.to_string(index=False))


if __name__ == "__main__":
    main()