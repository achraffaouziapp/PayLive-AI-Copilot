from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional
import logging
import re

import pandas as pd


# -------------------------------------------------------------------
# Data cleaning and standardization
# -------------------------------------------------------------------
# This script cleans and standardizes the datasets collected for the
# PayLive AI Copilot project.
#
# It uses the raw datasets and some extracted datasets to produce clean
# tables in data/processed/clean and cleaning reports in
# data/processed/reports/cleaning.
#
# Main operations:
# - remove rows with missing primary keys;
# - remove duplicate identifiers;
# - normalize text values;
# - normalize platforms, statuses, currencies and intents;
# - standardize dates;
# - standardize numeric values;
# - remove corrupted references;
# - recalculate financial totals;
# - merge product data coming from simulation, API and scraping;
# - generate cleaning reports.
# -------------------------------------------------------------------


BASE_DIR = Path(__file__).resolve().parents[2]

RAW_DIR = BASE_DIR / "data" / "raw"
INTERIM_DIR = BASE_DIR / "data" / "interim"
INTERIM_EXTRACTS_DIR = INTERIM_DIR / "extracts"

API_EXTRACT_DIR = INTERIM_EXTRACTS_DIR / "api"
SCRAPING_EXTRACT_DIR = INTERIM_EXTRACTS_DIR / "scraping"

LEGACY_API_EXTRACT_DIR = INTERIM_DIR / "api_extracts"
LEGACY_SCRAPING_EXTRACT_DIR = INTERIM_DIR / "scraping_extracts"

PROCESSED_DIR = BASE_DIR / "data" / "processed"

PROCESSED_CLEAN_DIR = PROCESSED_DIR / "clean"
PROCESSED_REPORTS_DIR = PROCESSED_DIR / "reports"
CLEANING_REPORTS_DIR = PROCESSED_REPORTS_DIR / "cleaning"

LOG_DIR = BASE_DIR / "logs"

LOG_FILE = LOG_DIR / "clean_and_standardize_data.log"

CLEANING_SUMMARY_PATH = CLEANING_REPORTS_DIR / "cleaning_summary.csv"
CLEANING_OPERATIONS_REPORT_PATH = CLEANING_REPORTS_DIR / "cleaning_operations_report.csv"
PROCESSED_MANIFEST_PATH = CLEANING_REPORTS_DIR / "processed_manifest.csv"


MISSING_VALUES = {
    "",
    " ",
    "nan",
    "NaN",
    "NAN",
    "none",
    "None",
    "NONE",
    "null",
    "Null",
    "NULL",
    "n/a",
    "N/A",
    "na",
    "NA",
    "unknown",
    "Unknown",
    "UNKNOWN",
}


PLATFORM_MAPPING = {
    "tiktok": "tiktok",
    "tik tok": "tiktok",
    "tiktok_live": "tiktok",
    "tiktok live": "tiktok",
    "instagram": "instagram",
    "instagram_live": "instagram",
    "instagram live": "instagram",
    "ig": "instagram",
    "facebook": "facebook_live",
    "facebook_live": "facebook_live",
    "facebook live": "facebook_live",
    "fb_live": "facebook_live",
    "youtube": "youtube_live",
    "youtube_live": "youtube_live",
    "youtube live": "youtube_live",
}

SELLER_STATUS_MAPPING = {
    "active": "active",
    "actif": "active",
    "inactive": "inactive",
    "inactif": "inactive",
    "suspended": "suspended",
    "suspendu": "suspended",
}

PRODUCT_STATUS_MAPPING = {
    "active": "active",
    "available": "active",
    "inactive": "inactive",
    "out_of_stock": "out_of_stock",
    "out of stock": "out_of_stock",
    "sold_out": "out_of_stock",
}

LIVE_STATUS_MAPPING = {
    "scheduled": "scheduled",
    "planned": "scheduled",
    "live": "live",
    "ended": "ended",
    "finished": "ended",
    "cancelled": "cancelled",
    "canceled": "cancelled",
}

CART_STATUS_MAPPING = {
    "open": "open",
    "paid": "paid",
    "abandoned": "abandoned",
    "cancelled": "cancelled",
    "canceled": "cancelled",
}

ORDER_STATUS_MAPPING = {
    "pending": "pending",
    "confirmed": "confirmed",
    "paid": "paid",
    "cancelled": "cancelled",
    "canceled": "cancelled",
    "refunded": "refunded",
}

PAYMENT_STATUS_MAPPING = {
    "pending": "pending",
    "succeeded": "succeeded",
    "success": "succeeded",
    "ok": "succeeded",
    "paid": "succeeded",
    "failed": "failed",
    "error": "failed",
    "cancelled": "cancelled",
    "canceled": "cancelled",
    "refunded": "refunded",
}

INTENT_MAPPING = {
    "purchase_intent": "purchase_intent",
    "buy": "purchase_intent",
    "order": "purchase_intent",
    "reservation": "purchase_intent",
    "product_question": "product_question",
    "question_product": "product_question",
    "payment_question": "payment_question",
    "shipping_question": "shipping_question",
    "other": "other",
    "unknown": "unknown",
}

EVENT_TYPE_MAPPING = {
    "comment_sent": "comment_sent",
    "comment": "comment_sent",
    "cart_opened": "cart_opened",
    "payment_clicked": "payment_clicked",
    "payment_succeeded": "payment_succeeded",
    "api_error": "api_error",
    "product_viewed": "product_viewed",
}

VALID_CURRENCIES = {"EUR", "USD", "GBP", "CAD", "CHF"}


class CleaningTracker:
    """
    Store cleaning statistics and detailed cleaning operations.
    """

    def __init__(self) -> None:
        self.summary: Dict[str, Dict[str, Any]] = {}
        self.operations: List[Dict[str, Any]] = []

    def start_dataset(self, dataset_name: str, input_rows: int) -> None:
        """
        Initialize summary statistics for one dataset.
        """
        self.summary[dataset_name] = {
            "dataset_name": dataset_name,
            "input_rows": int(input_rows),
            "output_rows": 0,
            "removed_rows": 0,
            "missing_primary_key_removed": 0,
            "duplicate_rows_removed": 0,
            "invalid_reference_removed": 0,
            "invalid_business_rows_removed": 0,
            "values_standardized": 0,
            "financial_values_recalculated": 0,
        }

    def add_operation(
        self,
        dataset_name: str,
        operation_name: str,
        rows_affected: int,
        description: str,
    ) -> None:
        """
        Add one detailed cleaning operation.
        """
        rows_affected = int(rows_affected)

        if rows_affected <= 0:
            return

        self.operations.append(
            {
                "operation_timestamp": get_current_timestamp(),
                "dataset_name": dataset_name,
                "operation_name": operation_name,
                "rows_affected": rows_affected,
                "description": description,
            }
        )

        if dataset_name not in self.summary:
            return

        if operation_name == "missing_primary_key_removed":
            self.summary[dataset_name]["missing_primary_key_removed"] += rows_affected
        elif operation_name == "duplicate_rows_removed":
            self.summary[dataset_name]["duplicate_rows_removed"] += rows_affected
        elif operation_name == "invalid_reference_removed":
            self.summary[dataset_name]["invalid_reference_removed"] += rows_affected
        elif operation_name == "invalid_business_rows_removed":
            self.summary[dataset_name]["invalid_business_rows_removed"] += rows_affected
        elif operation_name == "values_standardized":
            self.summary[dataset_name]["values_standardized"] += rows_affected
        elif operation_name == "financial_values_recalculated":
            self.summary[dataset_name]["financial_values_recalculated"] += rows_affected

    def finish_dataset(self, dataset_name: str, output_rows: int) -> None:
        """
        Finalize summary statistics for one dataset.
        """
        if dataset_name not in self.summary:
            return

        self.summary[dataset_name]["output_rows"] = int(output_rows)
        self.summary[dataset_name]["removed_rows"] = int(
            self.summary[dataset_name]["input_rows"] - output_rows
        )

    def build_summary_dataframe(self) -> pd.DataFrame:
        """
        Return the global cleaning summary as a DataFrame.
        """
        return pd.DataFrame(list(self.summary.values()))

    def build_operations_dataframe(self) -> pd.DataFrame:
        """
        Return detailed cleaning operations as a DataFrame.
        """
        return pd.DataFrame(self.operations)


def ensure_directories() -> None:
    """
    Create required output folders.
    """
    PROCESSED_CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    CLEANING_REPORTS_DIR.mkdir(parents=True, exist_ok=True)
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


def is_missing_value(value: Any) -> bool:
    """
    Return True if a value is considered missing.
    """
    if value is None:
        return True

    value_as_string = str(value).strip()

    return value_as_string in MISSING_VALUES


def normalize_text(value: Any) -> str:
    """
    Normalize a text value by trimming spaces.
    """
    if is_missing_value(value):
        return ""

    return str(value).strip()


def normalize_identifier(value: Any) -> str:
    """
    Normalize an identifier value.
    """
    return normalize_text(value)


def normalize_lower_key(value: Any) -> str:
    """
    Normalize a value for mapping comparison.
    """
    return normalize_text(value).lower().replace("-", "_")


def normalize_with_mapping(value: Any, mapping: Dict[str, str], default_value: str) -> str:
    """
    Normalize a categorical value using a mapping.
    """
    key = normalize_lower_key(value)

    if key in mapping:
        return mapping[key]

    key_with_spaces = key.replace("_", " ")

    if key_with_spaces in mapping:
        return mapping[key_with_spaces]

    if is_missing_value(value):
        return default_value

    return default_value


def normalize_platform(value: Any) -> str:
    """
    Normalize platform names.
    """
    return normalize_with_mapping(value, PLATFORM_MAPPING, "other")


def normalize_currency(value: Any) -> str:
    """
    Normalize currency values.
    """
    currency = normalize_text(value).upper()

    if currency in VALID_CURRENCIES:
        return currency

    return "EUR"


def clean_datetime_value(value: Any) -> str:
    """
    Convert a value to a standard datetime string.

    Invalid dates become empty strings.
    """
    if is_missing_value(value):
        return ""

    parsed = pd.to_datetime(value, errors="coerce")

    if pd.isna(parsed):
        return ""

    return parsed.strftime("%Y-%m-%d %H:%M:%S")


def clean_date_value(value: Any) -> str:
    """
    Convert a value to a standard date string.

    Invalid dates become empty strings.
    """
    if is_missing_value(value):
        return ""

    parsed = pd.to_datetime(value, errors="coerce")

    if pd.isna(parsed):
        return ""

    return parsed.strftime("%Y-%m-%d")


def clean_numeric_value(
    value: Any,
    default_value: float = 0.0,
    allow_negative: bool = False,
) -> float:
    """
    Convert a value to a numeric value.

    Invalid values are replaced by a default value.
    Negative values can be forbidden depending on the business context.
    """
    if is_missing_value(value):
        return default_value

    value_as_string = str(value).strip().replace(",", ".")
    value_as_string = re.sub(r"[^0-9.\-]", "", value_as_string)

    if value_as_string in {"", "-", ".", "-."}:
        return default_value

    try:
        numeric_value = float(value_as_string)
    except ValueError:
        return default_value

    if not allow_negative and numeric_value < 0:
        return default_value

    return numeric_value


def clean_integer_value(
    value: Any,
    default_value: int = 0,
    allow_negative: bool = False,
) -> int:
    """
    Convert a value to an integer value.
    """
    numeric_value = clean_numeric_value(
        value=value,
        default_value=float(default_value),
        allow_negative=allow_negative,
    )

    return int(round(numeric_value))


def is_valid_email(value: Any) -> bool:
    """
    Validate email format.
    """
    if is_missing_value(value):
        return False

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    return re.match(pattern, str(value).strip()) is not None


def read_raw_csv(file_name: str) -> pd.DataFrame:
    """
    Read a raw CSV file as strings.
    """
    file_path = RAW_DIR / file_name

    if not file_path.exists():
        logging.warning("Missing raw file: %s", file_path)
        return pd.DataFrame()

    return pd.read_csv(
        file_path,
        dtype=str,
        keep_default_na=False,
        encoding="utf-8",
    )


def read_optional_csv(file_path: Path) -> pd.DataFrame:
    """
    Read an optional CSV file as strings.
    """
    if not file_path.exists():
        logging.warning("Missing optional file: %s", file_path)
        return pd.DataFrame()

    return pd.read_csv(
        file_path,
        dtype=str,
        keep_default_na=False,
        encoding="utf-8",
    )


def resolve_input_path(preferred_path: Path, legacy_path: Path) -> Path:
    """
    Return the preferred file path when it exists, otherwise return the legacy path.

    This keeps the script compatible during the transition from the old interim
    structure to the new structure:
    - data/interim/extracts/api
    - data/interim/extracts/scraping
    """
    if preferred_path.exists():
        return preferred_path

    if legacy_path.exists():
        return legacy_path

    return preferred_path


def save_processed_dataset(df: pd.DataFrame, file_name: str) -> None:
    """
    Save a cleaned dataset in data/processed/clean.
    """
    output_path = PROCESSED_CLEAN_DIR / file_name
    df.to_csv(output_path, index=False, encoding="utf-8")
    logging.info("Saved processed dataset: %s", output_path)


def clean_string_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Trim spaces in all object columns.
    """
    df = df.copy()

    for column in df.columns:
        df[column] = df[column].map(normalize_text)

    return df


def remove_missing_primary_key(
    df: pd.DataFrame,
    dataset_name: str,
    primary_key: str,
    tracker: CleaningTracker,
) -> pd.DataFrame:
    """
    Remove rows with missing primary key.
    """
    if df.empty or primary_key not in df.columns:
        return df

    before = len(df)
    missing_mask = df[primary_key].map(is_missing_value)
    df = df.loc[~missing_mask].copy()
    removed = before - len(df)

    tracker.add_operation(
        dataset_name=dataset_name,
        operation_name="missing_primary_key_removed",
        rows_affected=removed,
        description=f"Removed rows with missing primary key: {primary_key}.",
    )

    return df


def remove_duplicate_primary_key(
    df: pd.DataFrame,
    dataset_name: str,
    primary_key: str,
    tracker: CleaningTracker,
) -> pd.DataFrame:
    """
    Remove duplicated primary key rows.
    """
    if df.empty or primary_key not in df.columns:
        return df

    before = len(df)
    duplicate_mask = df.duplicated(subset=[primary_key], keep="first")
    df = df.loc[~duplicate_mask].copy()
    removed = before - len(df)

    tracker.add_operation(
        dataset_name=dataset_name,
        operation_name="duplicate_rows_removed",
        rows_affected=removed,
        description=f"Removed duplicated rows based on primary key: {primary_key}.",
    )

    return df


def basic_entity_cleaning(
    df: pd.DataFrame,
    dataset_name: str,
    primary_key: str,
    tracker: CleaningTracker,
) -> pd.DataFrame:
    """
    Apply common cleaning steps to an entity dataset.
    """
    tracker.start_dataset(dataset_name, len(df))

    if df.empty:
        tracker.finish_dataset(dataset_name, 0)
        return df

    df = clean_string_columns(df)

    if primary_key in df.columns:
        df[primary_key] = df[primary_key].map(normalize_identifier)

    df = remove_missing_primary_key(df, dataset_name, primary_key, tracker)
    df = remove_duplicate_primary_key(df, dataset_name, primary_key, tracker)

    return df


def add_cleaning_metadata(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add standard metadata columns to a cleaned dataset.
    """
    df = df.copy()
    df["cleaned_at"] = get_current_timestamp()
    df["data_quality_status"] = "cleaned"

    return df


def first_existing_column(df: pd.DataFrame, candidates: List[str]) -> Optional[str]:
    """
    Return the first existing column among candidates.
    """
    for column in candidates:
        if column in df.columns:
            return column

    return None


def row_value(row: pd.Series, column: Optional[str], default_value: Any = "") -> Any:
    """
    Safely get a value from a row.
    """
    if column is None:
        return default_value

    if column not in row.index:
        return default_value

    return row[column]


def clean_sellers(tracker: CleaningTracker) -> pd.DataFrame:
    """
    Clean sellers.
    """
    dataset_name = "sellers"
    df = read_raw_csv("sellers_raw.csv")
    df = basic_entity_cleaning(df, dataset_name, "seller_id", tracker)

    if df.empty:
        return df

    if "main_platform" in df.columns:
        before_values = df["main_platform"].copy()
        df["main_platform"] = df["main_platform"].map(normalize_platform)
        changed = int((before_values != df["main_platform"]).sum())
        tracker.add_operation(dataset_name, "values_standardized", changed, "Normalized seller main platform values.")

    if "seller_status" in df.columns:
        before_values = df["seller_status"].copy()
        df["seller_status"] = df["seller_status"].map(
            lambda value: normalize_with_mapping(value, SELLER_STATUS_MAPPING, "inactive")
        )
        changed = int((before_values != df["seller_status"]).sum())
        tracker.add_operation(dataset_name, "values_standardized", changed, "Normalized seller status values.")

    if "email" in df.columns:
        invalid_mask = ~df["email"].map(is_valid_email)
        invalid_count = int(invalid_mask.sum())
        df.loc[invalid_mask, "email"] = ""
        tracker.add_operation(dataset_name, "values_standardized", invalid_count, "Invalid seller emails were set to empty values.")

    if "created_at" in df.columns:
        df["created_at"] = df["created_at"].map(clean_datetime_value)

    df = add_cleaning_metadata(df)
    tracker.finish_dataset(dataset_name, len(df))

    return df


def clean_customers(tracker: CleaningTracker) -> pd.DataFrame:
    """
    Clean customers.
    """
    dataset_name = "customers"
    df = read_raw_csv("customers_raw.csv")
    df = basic_entity_cleaning(df, dataset_name, "customer_id", tracker)

    if df.empty:
        return df

    if "platform" in df.columns:
        before_values = df["platform"].copy()
        df["platform"] = df["platform"].map(normalize_platform)
        changed = int((before_values != df["platform"]).sum())
        tracker.add_operation(dataset_name, "values_standardized", changed, "Normalized customer platform values.")

    if "username" in df.columns:
        missing_username_mask = df["username"].map(is_missing_value)
        missing_count = int(missing_username_mask.sum())
        df.loc[missing_username_mask, "username"] = "anonymous_user"
        tracker.add_operation(dataset_name, "values_standardized", missing_count, "Missing usernames were replaced by anonymous_user.")

    if "email" in df.columns:
        invalid_mask = ~df["email"].map(is_valid_email)
        invalid_count = int(invalid_mask.sum())
        df.loc[invalid_mask, "email"] = ""
        tracker.add_operation(dataset_name, "values_standardized", invalid_count, "Invalid customer emails were set to empty values.")

    if "created_at" in df.columns:
        df["created_at"] = df["created_at"].map(clean_datetime_value)

    df = add_cleaning_metadata(df)
    tracker.finish_dataset(dataset_name, len(df))

    return df


def build_api_products_dataframe() -> pd.DataFrame:
    """
    Convert API product extraction to the common product schema.
    """
    api_path = resolve_input_path(
        API_EXTRACT_DIR / "products_api_extract.csv",
        LEGACY_API_EXTRACT_DIR / "products_api_extract.csv",
    )
    api_df = read_optional_csv(api_path)

    if api_df.empty:
        return pd.DataFrame()

    id_column = first_existing_column(api_df, ["id", "api_product_id", "product_id"])
    name_column = first_existing_column(api_df, ["title", "product_name", "name"])
    category_column = first_existing_column(api_df, ["category"])
    brand_column = first_existing_column(api_df, ["brand"])
    description_column = first_existing_column(api_df, ["description"])
    price_column = first_existing_column(api_df, ["price", "unit_price"])
    stock_column = first_existing_column(api_df, ["stock", "stock_quantity"])
    created_at_column = first_existing_column(api_df, ["extracted_at", "created_at"])

    rows = []

    for index, row in api_df.iterrows():
        source_id = normalize_identifier(row_value(row, id_column, index))

        rows.append(
            {
                "product_id": f"API_{source_id}",
                "product_name": row_value(row, name_column, "api_product"),
                "category": row_value(row, category_column, "external_api"),
                "brand": row_value(row, brand_column, ""),
                "description": row_value(row, description_column, ""),
                "unit_price": row_value(row, price_column, 0),
                "stock_quantity": row_value(row, stock_column, 0),
                "product_status": "active",
                "source": "api",
                "created_at": row_value(row, created_at_column, get_current_timestamp()),
            }
        )

    return pd.DataFrame(rows)


def build_scraped_products_dataframe() -> pd.DataFrame:
    """
    Convert scraped product extraction to the common product schema.
    """
    scraped_path = resolve_input_path(
        SCRAPING_EXTRACT_DIR / "products_scraped_extract.csv",
        LEGACY_SCRAPING_EXTRACT_DIR / "products_scraped_extract.csv",
    )
    scraped_df = read_optional_csv(scraped_path)

    if scraped_df.empty:
        return pd.DataFrame()

    id_column = first_existing_column(scraped_df, ["scraped_product_id", "product_id", "upc"])
    name_column = first_existing_column(scraped_df, ["product_name", "title", "name"])
    category_column = first_existing_column(scraped_df, ["category"])
    brand_column = first_existing_column(scraped_df, ["brand"])
    description_column = first_existing_column(scraped_df, ["description"])
    price_column = first_existing_column(scraped_df, ["price", "product_price", "raw_price"])
    stock_column = first_existing_column(scraped_df, ["stock_quantity", "stock", "availability"])
    created_at_column = first_existing_column(scraped_df, ["extracted_at", "created_at"])

    rows = []

    for index, row in scraped_df.iterrows():
        source_id = normalize_identifier(row_value(row, id_column, index))

        rows.append(
            {
                "product_id": f"SCRAPED_{source_id}",
                "product_name": row_value(row, name_column, "scraped_product"),
                "category": row_value(row, category_column, "scraping"),
                "brand": row_value(row, brand_column, ""),
                "description": row_value(row, description_column, ""),
                "unit_price": row_value(row, price_column, 0),
                "stock_quantity": row_value(row, stock_column, 0),
                "product_status": "active",
                "source": "scraping",
                "created_at": row_value(row, created_at_column, get_current_timestamp()),
            }
        )

    return pd.DataFrame(rows)


def clean_products(tracker: CleaningTracker) -> pd.DataFrame:
    """
    Clean and aggregate products from simulation, API and scraping.
    """
    dataset_name = "products"

    raw_products_df = read_raw_csv("products_raw.csv")
    api_products_df = build_api_products_dataframe()
    scraped_products_df = build_scraped_products_dataframe()

    product_frames = [
        frame for frame in [raw_products_df, api_products_df, scraped_products_df]
        if not frame.empty
    ]

    if product_frames:
        df = pd.concat(product_frames, ignore_index=True, sort=False)
    else:
        df = pd.DataFrame()

    df = basic_entity_cleaning(df, dataset_name, "product_id", tracker)

    if df.empty:
        return df

    expected_columns = [
        "product_id",
        "product_name",
        "category",
        "brand",
        "description",
        "unit_price",
        "stock_quantity",
        "product_status",
        "source",
        "created_at",
    ]

    for column in expected_columns:
        if column not in df.columns:
            df[column] = ""

    df["product_name"] = df["product_name"].map(normalize_text)
    df["category"] = df["category"].map(lambda value: normalize_text(value).lower())
    df["brand"] = df["brand"].map(normalize_text)
    df["description"] = df["description"].map(normalize_text)

    before_price = df["unit_price"].copy()
    df["unit_price"] = df["unit_price"].map(lambda value: round(clean_numeric_value(value, 0.0, False), 2))
    changed_price = int((before_price.astype(str) != df["unit_price"].astype(str)).sum())

    before_stock = df["stock_quantity"].copy()
    df["stock_quantity"] = df["stock_quantity"].map(lambda value: clean_integer_value(value, 0, False))
    changed_stock = int((before_stock.astype(str) != df["stock_quantity"].astype(str)).sum())

    tracker.add_operation(dataset_name, "values_standardized", changed_price + changed_stock, "Standardized product prices and stock quantities.")

    if "product_status" in df.columns:
        before_status = df["product_status"].copy()
        df["product_status"] = df.apply(
            lambda row: "out_of_stock"
            if int(row["stock_quantity"]) <= 0
            else normalize_with_mapping(row["product_status"], PRODUCT_STATUS_MAPPING, "active"),
            axis=1,
        )
        changed = int((before_status.astype(str) != df["product_status"].astype(str)).sum())
        tracker.add_operation(dataset_name, "values_standardized", changed, "Normalized product status values.")

    df["source"] = df["source"].map(lambda value: normalize_text(value).lower() or "simulation")
    df["created_at"] = df["created_at"].map(clean_datetime_value)

    df = add_cleaning_metadata(df)
    tracker.finish_dataset(dataset_name, len(df))

    return df


def clean_live_sessions(tracker: CleaningTracker) -> pd.DataFrame:
    """
    Clean live sessions.
    """
    dataset_name = "live_sessions"
    df = read_raw_csv("live_sessions_raw.csv")
    df = basic_entity_cleaning(df, dataset_name, "live_id", tracker)

    if df.empty:
        return df

    if "seller_id" in df.columns:
        df["seller_id"] = df["seller_id"].map(normalize_identifier)

    if "platform" in df.columns:
        before = df["platform"].copy()
        df["platform"] = df["platform"].map(normalize_platform)
        tracker.add_operation(dataset_name, "values_standardized", int((before != df["platform"]).sum()), "Normalized live platform values.")

    if "live_status" in df.columns:
        before = df["live_status"].copy()
        df["live_status"] = df["live_status"].map(lambda value: normalize_with_mapping(value, LIVE_STATUS_MAPPING, "cancelled"))
        tracker.add_operation(dataset_name, "values_standardized", int((before != df["live_status"]).sum()), "Normalized live status values.")

    for date_column in ["scheduled_start_at", "actual_start_at", "ended_at", "created_at"]:
        if date_column in df.columns:
            df[date_column] = df[date_column].map(clean_datetime_value)

    if "peak_viewers" in df.columns:
        df["peak_viewers"] = df["peak_viewers"].map(lambda value: clean_integer_value(value, 0, False))

    if "currency" in df.columns:
        df["currency"] = df["currency"].map(normalize_currency)

    df = add_cleaning_metadata(df)
    tracker.finish_dataset(dataset_name, len(df))

    return df


def clean_live_products(tracker: CleaningTracker) -> pd.DataFrame:
    """
    Clean live products.
    """
    dataset_name = "live_products"
    df = read_raw_csv("live_products_raw.csv")
    df = basic_entity_cleaning(df, dataset_name, "live_product_id", tracker)

    if df.empty:
        return df

    for column in ["live_id", "product_id"]:
        if column in df.columns:
            df[column] = df[column].map(normalize_identifier)

    numeric_defaults = {
        "display_order": 0,
        "special_live_price": 0.0,
        "initial_stock": 0,
        "remaining_stock": 0,
    }

    for column, default_value in numeric_defaults.items():
        if column in df.columns:
            if column in {"display_order", "initial_stock", "remaining_stock"}:
                df[column] = df[column].map(lambda value: clean_integer_value(value, int(default_value), False))
            else:
                df[column] = df[column].map(lambda value: round(clean_numeric_value(value, float(default_value), False), 2))

    df = add_cleaning_metadata(df)
    tracker.finish_dataset(dataset_name, len(df))

    return df


def clean_live_comments(tracker: CleaningTracker) -> pd.DataFrame:
    """
    Clean live comments.
    """
    dataset_name = "live_comments"
    df = read_raw_csv("live_comments_raw.csv")
    df = basic_entity_cleaning(df, dataset_name, "comment_id", tracker)

    if df.empty:
        return df

    for column in ["live_id", "customer_id"]:
        if column in df.columns:
            df[column] = df[column].map(normalize_identifier)

    if "platform" in df.columns:
        df["platform"] = df["platform"].map(normalize_platform)

    if "username" in df.columns:
        df["username"] = df["username"].map(lambda value: normalize_text(value) or "anonymous_user")

    if "comment_text" in df.columns:
        before = len(df)
        empty_comment_mask = df["comment_text"].map(is_missing_value)
        df = df.loc[~empty_comment_mask].copy()
        removed = before - len(df)
        tracker.add_operation(dataset_name, "invalid_business_rows_removed", removed, "Removed comments with empty comment text.")

    if "commented_at" in df.columns:
        df["commented_at"] = df["commented_at"].map(clean_datetime_value)

    if "comment_language" in df.columns:
        df["comment_language"] = df["comment_language"].map(lambda value: normalize_text(value).lower() or "unknown")

    if "manual_intent_label" in df.columns:
        df["manual_intent_label"] = df["manual_intent_label"].map(
            lambda value: normalize_with_mapping(value, INTENT_MAPPING, "unknown")
        )

    if "extracted_product_keyword" in df.columns:
        df["extracted_product_keyword"] = df["extracted_product_keyword"].map(normalize_text)

    df = add_cleaning_metadata(df)
    tracker.finish_dataset(dataset_name, len(df))

    return df


def clean_carts(tracker: CleaningTracker) -> pd.DataFrame:
    """
    Clean carts.
    """
    dataset_name = "carts"
    df = read_raw_csv("carts_raw.csv")
    df = basic_entity_cleaning(df, dataset_name, "cart_id", tracker)

    if df.empty:
        return df

    for column in ["live_id", "customer_id"]:
        if column in df.columns:
            df[column] = df[column].map(normalize_identifier)

    if "cart_status" in df.columns:
        df["cart_status"] = df["cart_status"].map(lambda value: normalize_with_mapping(value, CART_STATUS_MAPPING, "open"))

    for date_column in ["created_at", "updated_at"]:
        if date_column in df.columns:
            df[date_column] = df[date_column].map(clean_datetime_value)

    if "total_amount" in df.columns:
        df["total_amount"] = df["total_amount"].map(lambda value: round(clean_numeric_value(value, 0.0, False), 2))

    if "currency" in df.columns:
        df["currency"] = df["currency"].map(normalize_currency)

    df = add_cleaning_metadata(df)
    tracker.finish_dataset(dataset_name, len(df))

    return df


def clean_cart_items(tracker: CleaningTracker) -> pd.DataFrame:
    """
    Clean cart items.
    """
    dataset_name = "cart_items"
    df = read_raw_csv("cart_items_raw.csv")
    df = basic_entity_cleaning(df, dataset_name, "cart_item_id", tracker)

    if df.empty:
        return df

    for column in ["cart_id", "product_id"]:
        if column in df.columns:
            df[column] = df[column].map(normalize_identifier)

    if "quantity" in df.columns:
        df["quantity"] = df["quantity"].map(lambda value: max(clean_integer_value(value, 1, False), 1))

    if "unit_price" in df.columns:
        df["unit_price"] = df["unit_price"].map(lambda value: round(clean_numeric_value(value, 0.0, False), 2))

    if "line_total" in df.columns:
        df["line_total"] = df["line_total"].map(lambda value: round(clean_numeric_value(value, 0.0, False), 2))

    if "selected_size" in df.columns:
        df["selected_size"] = df["selected_size"].map(lambda value: normalize_text(value).upper())

    if "selected_color" in df.columns:
        df["selected_color"] = df["selected_color"].map(lambda value: normalize_text(value).lower())

    if {"quantity", "unit_price", "line_total"}.issubset(df.columns):
        expected_total = (df["quantity"].astype(float) * df["unit_price"].astype(float)).round(2)
        mismatch_mask = (expected_total - df["line_total"].astype(float)).abs() > 0.01
        mismatch_count = int(mismatch_mask.sum())
        df.loc[mismatch_mask, "line_total"] = expected_total.loc[mismatch_mask]
        tracker.add_operation(dataset_name, "financial_values_recalculated", mismatch_count, "Recalculated inconsistent cart item line totals.")

    df = add_cleaning_metadata(df)
    tracker.finish_dataset(dataset_name, len(df))

    return df


def clean_orders(tracker: CleaningTracker) -> pd.DataFrame:
    """
    Clean orders.
    """
    dataset_name = "orders"
    df = read_raw_csv("orders_raw.csv")
    df = basic_entity_cleaning(df, dataset_name, "order_id", tracker)

    if df.empty:
        return df

    for column in ["cart_id", "customer_id", "seller_id"]:
        if column in df.columns:
            df[column] = df[column].map(normalize_identifier)

    if "order_status" in df.columns:
        df["order_status"] = df["order_status"].map(lambda value: normalize_with_mapping(value, ORDER_STATUS_MAPPING, "pending"))

    if "order_amount" in df.columns:
        df["order_amount"] = df["order_amount"].map(lambda value: round(clean_numeric_value(value, 0.0, False), 2))

    if "currency" in df.columns:
        df["currency"] = df["currency"].map(normalize_currency)

    for date_column in ["created_at", "confirmed_at"]:
        if date_column in df.columns:
            df[date_column] = df[date_column].map(clean_datetime_value)

    df = add_cleaning_metadata(df)
    tracker.finish_dataset(dataset_name, len(df))

    return df


def clean_payments(tracker: CleaningTracker) -> pd.DataFrame:
    """
    Clean payments.
    """
    dataset_name = "payments"
    df = read_raw_csv("payments_raw.csv")
    df = basic_entity_cleaning(df, dataset_name, "payment_id", tracker)

    if df.empty:
        return df

    if "order_id" in df.columns:
        df["order_id"] = df["order_id"].map(normalize_identifier)

    if "payment_provider" in df.columns:
        df["payment_provider"] = df["payment_provider"].map(lambda value: normalize_text(value).lower())

    if "payment_status" in df.columns:
        df["payment_status"] = df["payment_status"].map(lambda value: normalize_with_mapping(value, PAYMENT_STATUS_MAPPING, "failed"))

    if "payment_amount" in df.columns:
        df["payment_amount"] = df["payment_amount"].map(lambda value: round(clean_numeric_value(value, 0.0, False), 2))

    if "currency" in df.columns:
        df["currency"] = df["currency"].map(normalize_currency)

    if "payment_method" in df.columns:
        df["payment_method"] = df["payment_method"].map(lambda value: normalize_text(value).lower())

    if "paid_at" in df.columns:
        df["paid_at"] = df["paid_at"].map(clean_datetime_value)

    if "transaction_reference" in df.columns:
        df["transaction_reference"] = df["transaction_reference"].map(normalize_text)

    df = add_cleaning_metadata(df)
    tracker.finish_dataset(dataset_name, len(df))

    return df


def clean_stock_movements(tracker: CleaningTracker) -> pd.DataFrame:
    """
    Clean stock movements.
    """
    dataset_name = "stock_movements"
    df = read_raw_csv("stock_movements_raw.csv")
    df = basic_entity_cleaning(df, dataset_name, "stock_movement_id", tracker)

    if df.empty:
        return df

    for column in ["product_id", "live_id"]:
        if column in df.columns:
            df[column] = df[column].map(normalize_identifier)

    if "movement_type" in df.columns:
        df["movement_type"] = df["movement_type"].map(lambda value: normalize_text(value).lower())

    if "quantity_change" in df.columns:
        df["quantity_change"] = df["quantity_change"].map(lambda value: clean_integer_value(value, 0, True))

    if "movement_reason" in df.columns:
        df["movement_reason"] = df["movement_reason"].map(lambda value: normalize_text(value).lower())

    if "created_at" in df.columns:
        df["created_at"] = df["created_at"].map(clean_datetime_value)

    df = add_cleaning_metadata(df)
    tracker.finish_dataset(dataset_name, len(df))

    return df


def clean_live_events(tracker: CleaningTracker) -> pd.DataFrame:
    """
    Clean live events.
    """
    dataset_name = "live_events"
    df = read_raw_csv("live_events_raw.csv")
    df = basic_entity_cleaning(df, dataset_name, "event_id", tracker)

    if df.empty:
        return df

    for column in ["live_id", "customer_id"]:
        if column in df.columns:
            df[column] = df[column].map(normalize_identifier)

    if "event_type" in df.columns:
        df["event_type"] = df["event_type"].map(lambda value: normalize_with_mapping(value, EVENT_TYPE_MAPPING, "invalid_event"))

        before = len(df)
        invalid_event_mask = df["event_type"] == "invalid_event"
        df = df.loc[~invalid_event_mask].copy()
        removed = before - len(df)
        tracker.add_operation(dataset_name, "invalid_business_rows_removed", removed, "Removed live events with invalid event types.")

    if "event_timestamp" in df.columns:
        df["event_timestamp"] = df["event_timestamp"].map(clean_datetime_value)

        before = len(df)
        invalid_timestamp_mask = df["event_timestamp"].map(is_missing_value)
        df = df.loc[~invalid_timestamp_mask].copy()
        removed = before - len(df)
        tracker.add_operation(dataset_name, "invalid_business_rows_removed", removed, "Removed live events with invalid timestamps.")

    if "event_value" in df.columns:
        df["event_value"] = df["event_value"].map(normalize_text)

    if "source_system" in df.columns:
        df["source_system"] = df["source_system"].map(lambda value: normalize_text(value).lower() or "simulation")

    df = add_cleaning_metadata(df)
    tracker.finish_dataset(dataset_name, len(df))

    return df


def apply_reference_filter(
    df: pd.DataFrame,
    dataset_name: str,
    column_name: str,
    valid_values: set,
    tracker: CleaningTracker,
    required: bool = True,
) -> pd.DataFrame:
    """
    Remove rows with invalid foreign key references.
    """
    if df.empty or column_name not in df.columns:
        return df

    before = len(df)

    normalized_valid_values = {
        normalize_identifier(value)
        for value in valid_values
        if not is_missing_value(value)
    }

    column_values = df[column_name].map(normalize_identifier)
    missing_mask = column_values.map(is_missing_value)
    invalid_mask = ~missing_mask & ~column_values.isin(normalized_valid_values)

    if required:
        remove_mask = missing_mask | invalid_mask
    else:
        remove_mask = invalid_mask

    df = df.loc[~remove_mask].copy()
    removed = before - len(df)

    tracker.add_operation(
        dataset_name=dataset_name,
        operation_name="invalid_reference_removed",
        rows_affected=removed,
        description=f"Removed rows with invalid reference in column: {column_name}.",
    )

    return df


def enforce_referential_integrity(
    datasets: Dict[str, pd.DataFrame],
    tracker: CleaningTracker,
) -> Dict[str, pd.DataFrame]:
    """
    Remove corrupted foreign key references between cleaned datasets.
    """
    sellers = datasets["sellers"]
    customers = datasets["customers"]
    products = datasets["products"]
    live_sessions = datasets["live_sessions"]
    live_products = datasets["live_products"]
    live_comments = datasets["live_comments"]
    carts = datasets["carts"]
    cart_items = datasets["cart_items"]
    orders = datasets["orders"]
    payments = datasets["payments"]
    stock_movements = datasets["stock_movements"]
    live_events = datasets["live_events"]

    valid_seller_ids = set(sellers["seller_id"]) if "seller_id" in sellers.columns else set()
    valid_customer_ids = set(customers["customer_id"]) if "customer_id" in customers.columns else set()
    valid_product_ids = set(products["product_id"]) if "product_id" in products.columns else set()

    live_sessions = apply_reference_filter(live_sessions, "live_sessions", "seller_id", valid_seller_ids, tracker)

    valid_live_ids = set(live_sessions["live_id"]) if "live_id" in live_sessions.columns else set()

    live_products = apply_reference_filter(live_products, "live_products", "live_id", valid_live_ids, tracker)
    live_products = apply_reference_filter(live_products, "live_products", "product_id", valid_product_ids, tracker)

    live_comments = apply_reference_filter(live_comments, "live_comments", "live_id", valid_live_ids, tracker)
    live_comments = apply_reference_filter(live_comments, "live_comments", "customer_id", valid_customer_ids, tracker)

    carts = apply_reference_filter(carts, "carts", "live_id", valid_live_ids, tracker)
    carts = apply_reference_filter(carts, "carts", "customer_id", valid_customer_ids, tracker)

    valid_cart_ids = set(carts["cart_id"]) if "cart_id" in carts.columns else set()

    cart_items = apply_reference_filter(cart_items, "cart_items", "cart_id", valid_cart_ids, tracker)
    cart_items = apply_reference_filter(cart_items, "cart_items", "product_id", valid_product_ids, tracker)

    orders = apply_reference_filter(orders, "orders", "cart_id", valid_cart_ids, tracker)
    orders = apply_reference_filter(orders, "orders", "customer_id", valid_customer_ids, tracker)
    orders = apply_reference_filter(orders, "orders", "seller_id", valid_seller_ids, tracker)

    valid_order_ids = set(orders["order_id"]) if "order_id" in orders.columns else set()

    payments = apply_reference_filter(payments, "payments", "order_id", valid_order_ids, tracker)

    stock_movements = apply_reference_filter(stock_movements, "stock_movements", "product_id", valid_product_ids, tracker)
    stock_movements = apply_reference_filter(stock_movements, "stock_movements", "live_id", valid_live_ids, tracker)

    live_events = apply_reference_filter(live_events, "live_events", "live_id", valid_live_ids, tracker)
    live_events = apply_reference_filter(live_events, "live_events", "customer_id", valid_customer_ids, tracker)

    datasets["live_sessions"] = live_sessions
    datasets["live_products"] = live_products
    datasets["live_comments"] = live_comments
    datasets["carts"] = carts
    datasets["cart_items"] = cart_items
    datasets["orders"] = orders
    datasets["payments"] = payments
    datasets["stock_movements"] = stock_movements
    datasets["live_events"] = live_events

    return datasets


def recalculate_financial_totals(
    datasets: Dict[str, pd.DataFrame],
    tracker: CleaningTracker,
) -> Dict[str, pd.DataFrame]:
    """
    Recalculate totals for cart items, carts, orders and payments.
    """
    cart_items = datasets["cart_items"]
    carts = datasets["carts"]
    orders = datasets["orders"]
    payments = datasets["payments"]

    if not cart_items.empty and {"quantity", "unit_price", "line_total"}.issubset(cart_items.columns):
        expected_line_total = (
            cart_items["quantity"].astype(float)
            * cart_items["unit_price"].astype(float)
        ).round(2)

        mismatch_mask = (expected_line_total - cart_items["line_total"].astype(float)).abs() > 0.01
        mismatch_count = int(mismatch_mask.sum())
        cart_items.loc[mismatch_mask, "line_total"] = expected_line_total.loc[mismatch_mask]

        tracker.add_operation(
            "cart_items",
            "financial_values_recalculated",
            mismatch_count,
            "Recalculated cart item line totals after reference filtering.",
        )

    if (
        not carts.empty
        and not cart_items.empty
        and "cart_id" in carts.columns
        and "cart_id" in cart_items.columns
        and "line_total" in cart_items.columns
        and "total_amount" in carts.columns
    ):
        cart_totals = (
            cart_items.groupby("cart_id", as_index=False)["line_total"]
            .sum()
            .rename(columns={"line_total": "calculated_total_amount"})
        )

        carts = carts.merge(cart_totals, on="cart_id", how="left")
        carts["calculated_total_amount"] = carts["calculated_total_amount"].fillna(0).round(2)

        mismatch_mask = (
            carts["total_amount"].astype(float) - carts["calculated_total_amount"].astype(float)
        ).abs() > 0.01

        mismatch_count = int(mismatch_mask.sum())
        carts.loc[mismatch_mask, "total_amount"] = carts.loc[mismatch_mask, "calculated_total_amount"]
        carts = carts.drop(columns=["calculated_total_amount"])

        tracker.add_operation(
            "carts",
            "financial_values_recalculated",
            mismatch_count,
            "Recalculated cart total amounts from cart items.",
        )

    if (
        not orders.empty
        and not carts.empty
        and "cart_id" in orders.columns
        and "cart_id" in carts.columns
        and "order_amount" in orders.columns
        and "total_amount" in carts.columns
    ):
        cart_amounts = carts[["cart_id", "total_amount"]].rename(
            columns={"total_amount": "calculated_order_amount"}
        )

        orders = orders.merge(cart_amounts, on="cart_id", how="left")
        orders["calculated_order_amount"] = orders["calculated_order_amount"].fillna(orders["order_amount"])

        mismatch_mask = (
            orders["order_amount"].astype(float) - orders["calculated_order_amount"].astype(float)
        ).abs() > 0.01

        mismatch_count = int(mismatch_mask.sum())
        orders.loc[mismatch_mask, "order_amount"] = orders.loc[mismatch_mask, "calculated_order_amount"]
        orders = orders.drop(columns=["calculated_order_amount"])

        tracker.add_operation(
            "orders",
            "financial_values_recalculated",
            mismatch_count,
            "Recalculated order amounts from related cart totals.",
        )

    if (
        not payments.empty
        and not orders.empty
        and "order_id" in payments.columns
        and "order_id" in orders.columns
        and "payment_amount" in payments.columns
        and "order_amount" in orders.columns
        and "payment_status" in payments.columns
    ):
        order_amounts = orders[["order_id", "order_amount"]].rename(
            columns={"order_amount": "related_order_amount"}
        )

        payments = payments.merge(order_amounts, on="order_id", how="left")
        missing_or_zero_success_mask = (
            (payments["payment_status"] == "succeeded")
            & (payments["payment_amount"].astype(float) <= 0)
            & (payments["related_order_amount"].notna())
        )

        mismatch_count = int(missing_or_zero_success_mask.sum())
        payments.loc[missing_or_zero_success_mask, "payment_amount"] = payments.loc[
            missing_or_zero_success_mask,
            "related_order_amount",
        ]
        payments = payments.drop(columns=["related_order_amount"])

        tracker.add_operation(
            "payments",
            "financial_values_recalculated",
            mismatch_count,
            "Recalculated successful payment amounts from related orders when missing or zero.",
        )

    datasets["cart_items"] = cart_items
    datasets["carts"] = carts
    datasets["orders"] = orders
    datasets["payments"] = payments

    return datasets


def update_output_rows_after_global_cleaning(
    datasets: Dict[str, pd.DataFrame],
    tracker: CleaningTracker,
) -> None:
    """
    Update final output row counts after reference filtering.
    """
    for dataset_name, df in datasets.items():
        tracker.finish_dataset(dataset_name, len(df))


def build_processed_manifest(datasets: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Build a manifest of processed datasets.
    """
    rows = []

    for dataset_name, df in datasets.items():
        rows.append(
            {
                "processed_at": get_current_timestamp(),
                "dataset_name": dataset_name,
                "output_file": str(PROCESSED_CLEAN_DIR / f"{dataset_name}_clean.csv"),
                "row_count": int(len(df)),
                "column_count": int(len(df.columns)),
                "status": "created",
            }
        )

    rows.append(
        {
            "processed_at": get_current_timestamp(),
            "dataset_name": "cleaning_summary",
            "output_file": str(CLEANING_SUMMARY_PATH),
            "row_count": 0,
            "column_count": 0,
            "status": "created",
        }
    )

    rows.append(
        {
            "processed_at": get_current_timestamp(),
            "dataset_name": "cleaning_operations_report",
            "output_file": str(CLEANING_OPERATIONS_REPORT_PATH),
            "row_count": 0,
            "column_count": 0,
            "status": "created",
        }
    )

    return pd.DataFrame(rows)


def save_all_processed_datasets(
    datasets: Dict[str, pd.DataFrame],
    tracker: CleaningTracker,
) -> None:
    """
    Save all cleaned datasets and reports.
    """
    for dataset_name, df in datasets.items():
        save_processed_dataset(df, f"{dataset_name}_clean.csv")

    summary_df = tracker.build_summary_dataframe()
    operations_df = tracker.build_operations_dataframe()
    manifest_df = build_processed_manifest(datasets)

    summary_df.to_csv(CLEANING_SUMMARY_PATH, index=False, encoding="utf-8")
    operations_df.to_csv(CLEANING_OPERATIONS_REPORT_PATH, index=False, encoding="utf-8")
    manifest_df.to_csv(PROCESSED_MANIFEST_PATH, index=False, encoding="utf-8")


def clean_and_standardize_data() -> Dict[str, pd.DataFrame]:
    """
    Run the full cleaning and standardization pipeline.
    """
    tracker = CleaningTracker()

    logging.info("Starting data cleaning and standardization pipeline.")

    datasets = {
        "sellers": clean_sellers(tracker),
        "customers": clean_customers(tracker),
        "products": clean_products(tracker),
        "live_sessions": clean_live_sessions(tracker),
        "live_products": clean_live_products(tracker),
        "live_comments": clean_live_comments(tracker),
        "carts": clean_carts(tracker),
        "cart_items": clean_cart_items(tracker),
        "orders": clean_orders(tracker),
        "payments": clean_payments(tracker),
        "stock_movements": clean_stock_movements(tracker),
        "live_events": clean_live_events(tracker),
    }

    datasets = enforce_referential_integrity(datasets, tracker)
    datasets = recalculate_financial_totals(datasets, tracker)

    update_output_rows_after_global_cleaning(datasets, tracker)
    save_all_processed_datasets(datasets, tracker)

    logging.info("Data cleaning and standardization pipeline completed successfully.")

    return datasets


def main() -> None:
    """
    Entry point of the script.
    """
    ensure_directories()
    setup_logging()

    datasets = clean_and_standardize_data()

    summary_df = pd.read_csv(CLEANING_SUMMARY_PATH)
    operations_df = pd.read_csv(CLEANING_OPERATIONS_REPORT_PATH)

    print("Data cleaning and standardization completed successfully.")
    print(f"Processed clean folder: {PROCESSED_CLEAN_DIR}")
    print(f"Cleaning reports folder: {CLEANING_REPORTS_DIR}")
    print(f"Cleaning summary: {CLEANING_SUMMARY_PATH}")
    print(f"Cleaning operations report: {CLEANING_OPERATIONS_REPORT_PATH}")
    print(f"Processed manifest: {PROCESSED_MANIFEST_PATH}")
    print(f"Log file: {LOG_FILE}")
    print("")
    print("Processed datasets:")
    for dataset_name, df in datasets.items():
        print(f"- {dataset_name}_clean.csv: {len(df)} rows, {len(df.columns)} columns")
    print("")
    print("Cleaning summary:")
    print(summary_df.to_string(index=False))
    print("")
    print("Cleaning operations count:")
    print(len(operations_df))


if __name__ == "__main__":
    main()