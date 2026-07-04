from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging
import re

import pandas as pd


# -------------------------------------------------------------------
# Extracted data quality analysis
# -------------------------------------------------------------------
# This script analyzes the quality of raw and extracted datasets.
#
# It does not clean the data.
# It only detects and documents data quality issues before the cleaning,
# normalization, and aggregation phase.
#
# The script checks:
# - file-level quality;
# - column-level quality;
# - missing values;
# - duplicate primary keys;
# - invalid dates;
# - invalid emails;
# - invalid numeric values;
# - negative values;
# - invalid allowed values;
# - referential integrity issues;
# - temporal consistency issues;
# - calculated amount inconsistencies.
#
# Outputs are saved in data/interim.
# -------------------------------------------------------------------


BASE_DIR = Path(__file__).resolve().parents[2]

RAW_DIR = BASE_DIR / "data" / "raw"
INTERIM_DIR = BASE_DIR / "data" / "interim"
LOG_DIR = BASE_DIR / "logs"

OUTPUT_FILE_REPORT = INTERIM_DIR / "extracted_quality_file_report.csv"
OUTPUT_COLUMN_REPORT = INTERIM_DIR / "extracted_quality_column_report.csv"
OUTPUT_BUSINESS_RULES_REPORT = INTERIM_DIR / "extracted_quality_business_rules_report.csv"
OUTPUT_SUMMARY = INTERIM_DIR / "extracted_quality_summary.csv"

LOG_FILE = LOG_DIR / "analyze_extracted_data_quality.log"


# Values considered as missing during the quality analysis.
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


# Files that should not be analyzed as business datasets.
EXCLUDED_RAW_FILES = {
    "data_quality_issues_summary.csv",
}


# Folders containing datasets to analyze.
DATASET_LOCATIONS = [
    {
        "source_category": "raw",
        "folder": RAW_DIR,
        "pattern": "*.csv",
    },
    {
        "source_category": "file_extracts",
        "folder": INTERIM_DIR / "file_extracts",
        "pattern": "*.csv",
    },
    {
        "source_category": "api_extracts",
        "folder": INTERIM_DIR / "api_extracts",
        "pattern": "*.csv",
    },
    {
        "source_category": "scraping_extracts",
        "folder": INTERIM_DIR / "scraping_extracts",
        "pattern": "*.csv",
    },
    {
        "source_category": "database_extracts",
        "folder": INTERIM_DIR / "database_extracts",
        "pattern": "*.csv",
    },
    {
        "source_category": "bigdata_extracts",
        "folder": INTERIM_DIR / "bigdata_extracts",
        "pattern": "*.csv",
    },
]


PRIMARY_KEYS = {
    "sellers": ["seller_id"],
    "customers": ["customer_id"],
    "products": ["product_id"],
    "live_sessions": ["live_id"],
    "live_products": ["live_product_id"],
    "live_comments": ["comment_id"],
    "carts": ["cart_id"],
    "cart_items": ["cart_item_id"],
    "orders": ["order_id"],
    "payments": ["payment_id"],
    "stock_movements": ["stock_movement_id"],
    "live_events": ["event_id"],
}


DATE_COLUMNS = {
    "sellers": ["created_at"],
    "customers": ["created_at"],
    "products": ["created_at"],
    "live_sessions": ["scheduled_start_at", "actual_start_at", "ended_at", "created_at"],
    "live_comments": ["commented_at"],
    "carts": ["created_at", "updated_at"],
    "orders": ["created_at", "confirmed_at"],
    "payments": ["paid_at"],
    "stock_movements": ["created_at"],
    "live_events": ["event_timestamp"],
}


EMAIL_COLUMNS = {
    "sellers": ["email"],
    "customers": ["email"],
}


NUMERIC_COLUMNS = {
    "products": ["unit_price", "stock_quantity"],
    "live_sessions": ["peak_viewers"],
    "live_products": ["display_order", "special_live_price", "initial_stock", "remaining_stock"],
    "cart_items": ["quantity", "unit_price", "line_total"],
    "carts": ["total_amount"],
    "orders": ["order_amount"],
    "payments": ["payment_amount"],
    "stock_movements": ["quantity_change"],
}


ALLOWED_VALUES = {
    "platform": {"tiktok", "instagram", "facebook_live", "youtube_live", "other"},
    "main_platform": {"tiktok", "instagram", "facebook_live", "youtube_live", "other"},
    "seller_status": {"active", "inactive", "suspended"},
    "product_status": {"active", "inactive", "out_of_stock"},
    "live_status": {"scheduled", "live", "ended", "cancelled"},
    "cart_status": {"open", "paid", "abandoned", "cancelled"},
    "order_status": {"pending", "confirmed", "paid", "cancelled", "refunded"},
    "payment_status": {"pending", "succeeded", "failed", "cancelled", "refunded"},
    "manual_intent_label": {
        "purchase_intent",
        "product_question",
        "payment_question",
        "shipping_question",
        "other",
        "unknown",
    },
    "event_type": {
        "comment_sent",
        "cart_opened",
        "payment_clicked",
        "payment_succeeded",
        "api_error",
        "product_viewed",
    },
}


REFERENCE_RULES = [
    {
        "source_entity": "live_sessions",
        "source_column": "seller_id",
        "target_entity": "sellers",
        "target_column": "seller_id",
    },
    {
        "source_entity": "live_products",
        "source_column": "live_id",
        "target_entity": "live_sessions",
        "target_column": "live_id",
    },
    {
        "source_entity": "live_products",
        "source_column": "product_id",
        "target_entity": "products",
        "target_column": "product_id",
    },
    {
        "source_entity": "live_comments",
        "source_column": "live_id",
        "target_entity": "live_sessions",
        "target_column": "live_id",
    },
    {
        "source_entity": "live_comments",
        "source_column": "customer_id",
        "target_entity": "customers",
        "target_column": "customer_id",
    },
    {
        "source_entity": "carts",
        "source_column": "live_id",
        "target_entity": "live_sessions",
        "target_column": "live_id",
    },
    {
        "source_entity": "carts",
        "source_column": "customer_id",
        "target_entity": "customers",
        "target_column": "customer_id",
    },
    {
        "source_entity": "cart_items",
        "source_column": "cart_id",
        "target_entity": "carts",
        "target_column": "cart_id",
    },
    {
        "source_entity": "cart_items",
        "source_column": "product_id",
        "target_entity": "products",
        "target_column": "product_id",
    },
    {
        "source_entity": "orders",
        "source_column": "cart_id",
        "target_entity": "carts",
        "target_column": "cart_id",
    },
    {
        "source_entity": "orders",
        "source_column": "customer_id",
        "target_entity": "customers",
        "target_column": "customer_id",
    },
    {
        "source_entity": "orders",
        "source_column": "seller_id",
        "target_entity": "sellers",
        "target_column": "seller_id",
    },
    {
        "source_entity": "payments",
        "source_column": "order_id",
        "target_entity": "orders",
        "target_column": "order_id",
    },
    {
        "source_entity": "stock_movements",
        "source_column": "product_id",
        "target_entity": "products",
        "target_column": "product_id",
    },
    {
        "source_entity": "stock_movements",
        "source_column": "live_id",
        "target_entity": "live_sessions",
        "target_column": "live_id",
    },
    {
        "source_entity": "live_events",
        "source_column": "live_id",
        "target_entity": "live_sessions",
        "target_column": "live_id",
    },
    {
        "source_entity": "live_events",
        "source_column": "customer_id",
        "target_entity": "customers",
        "target_column": "customer_id",
    },
]


TEMPORAL_RULES = [
    {
        "entity": "live_sessions",
        "start_column": "actual_start_at",
        "end_column": "ended_at",
        "issue_type": "ended_at_before_actual_start_at",
    },
    {
        "entity": "carts",
        "start_column": "created_at",
        "end_column": "updated_at",
        "issue_type": "updated_at_before_created_at",
    },
    {
        "entity": "orders",
        "start_column": "created_at",
        "end_column": "confirmed_at",
        "issue_type": "confirmed_at_before_created_at",
    },
]


def ensure_directories() -> None:
    """
    Create required folders for reports and logs.
    """
    INTERIM_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def setup_logging() -> None:
    """
    Configure logging for the quality analysis script.
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
    Return True if a value should be considered missing.
    """
    if value is None:
        return True

    value_as_string = str(value).strip()

    return value_as_string in MISSING_VALUES


def build_missing_mask(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build a boolean DataFrame indicating missing values.

    This avoids relying on pandas default NA detection because raw files
    may contain many textual placeholders for missing values.
    """
    return df.apply(lambda column: column.map(is_missing_value))


def normalize_dataset_name(file_stem: str) -> str:
    """
    Normalize a file stem into a logical dataset name.

    Examples:
    - sellers_raw -> sellers
    - sellers_file_extract -> sellers
    - products_api_extract -> products_api
    - events_by_live_extract -> events_by_live
    """
    dataset_name = file_stem

    suffixes = [
        "_file_extract",
        "_scraped_extract",
        "_scraping_extract",
        "_api_extract",
        "_raw",
        "_extract",
    ]

    changed = True

    while changed:
        changed = False

        for suffix in suffixes:
            if dataset_name.endswith(suffix):
                dataset_name = dataset_name[: -len(suffix)]
                changed = True

    return dataset_name


def discover_dataset_files() -> List[Dict[str, Any]]:
    """
    Discover all CSV datasets to analyze.

    Technical report files are not included, only raw and extracted
    business datasets.
    """
    dataset_files = []

    for location in DATASET_LOCATIONS:
        source_category = location["source_category"]
        folder = location["folder"]
        pattern = location["pattern"]

        if not folder.exists():
            logging.warning("Dataset folder does not exist: %s", folder)
            continue

        for file_path in sorted(folder.glob(pattern)):
            if source_category == "raw" and file_path.name in EXCLUDED_RAW_FILES:
                continue

            dataset_files.append(
                {
                    "source_category": source_category,
                    "file_path": file_path,
                    "file_name": file_path.name,
                    "dataset_name": normalize_dataset_name(file_path.stem),
                }
            )

    return dataset_files


def read_csv_as_raw(file_path: Path) -> pd.DataFrame:
    """
    Read a CSV file while preserving raw values as strings.
    """
    return pd.read_csv(
        file_path,
        dtype=str,
        keep_default_na=False,
        encoding="utf-8",
    )


def load_datasets() -> List[Dict[str, Any]]:
    """
    Load all discovered datasets.
    """
    loaded_datasets = []

    for dataset_file in discover_dataset_files():
        file_path = dataset_file["file_path"]

        try:
            df = read_csv_as_raw(file_path)

            loaded_datasets.append(
                {
                    **dataset_file,
                    "dataframe": df,
                    "status": "loaded",
                    "error_message": "",
                }
            )

            logging.info("Loaded dataset %s with %s rows.", file_path, len(df))

        except Exception as error:
            loaded_datasets.append(
                {
                    **dataset_file,
                    "dataframe": pd.DataFrame(),
                    "status": "load_error",
                    "error_message": str(error),
                }
            )

            logging.exception("Failed to load dataset: %s", file_path)

    return loaded_datasets


def parse_datetime_series(series: pd.Series) -> pd.Series:
    """
    Parse a pandas Series as datetime.

    Invalid values become NaT.
    """
    cleaned_series = series.astype(str).str.strip()
    cleaned_series = cleaned_series.mask(cleaned_series.map(is_missing_value))

    return pd.to_datetime(cleaned_series, errors="coerce")


def parse_numeric_series(series: pd.Series) -> pd.Series:
    """
    Parse a pandas Series as numeric.

    Commas are converted to dots to support decimal values written with
    French-style separators.
    """
    cleaned_series = series.astype(str).str.strip().str.replace(",", ".", regex=False)
    cleaned_series = cleaned_series.mask(cleaned_series.map(is_missing_value))

    return pd.to_numeric(cleaned_series, errors="coerce")


def is_valid_email(value: Any) -> bool:
    """
    Validate a simple email format.
    """
    if is_missing_value(value):
        return True

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    return re.match(pattern, str(value).strip()) is not None


def column_looks_like_date(column_name: str) -> bool:
    """
    Detect whether a column name looks like a date or timestamp column.
    """
    lower_name = column_name.lower()

    return (
        lower_name.endswith("_at")
        or "date" in lower_name
        or "timestamp" in lower_name
    )


def column_looks_like_numeric(column_name: str) -> bool:
    """
    Detect whether a column name looks like a numeric column.
    """
    lower_name = column_name.lower()

    numeric_keywords = [
        "price",
        "amount",
        "quantity",
        "stock",
        "viewers",
        "total",
        "count",
        "rate",
        "ratio",
        "order",
        "payment",
        "revenue",
        "hour",
    ]

    return any(keyword in lower_name for keyword in numeric_keywords)


def get_configured_columns(config: Dict[str, List[str]], dataset_name: str) -> List[str]:
    """
    Return configured columns for a dataset.
    """
    return config.get(dataset_name, [])


def build_file_level_report(datasets: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Build a report at file level.

    It summarizes row counts, column counts, missing cells, and duplicate rows.
    """
    rows = []

    for dataset in datasets:
        df = dataset["dataframe"]

        if dataset["status"] != "loaded":
            rows.append(
                {
                    "source_category": dataset["source_category"],
                    "dataset_name": dataset["dataset_name"],
                    "file_name": dataset["file_name"],
                    "file_path": str(dataset["file_path"]),
                    "row_count": 0,
                    "column_count": 0,
                    "missing_cells_count": 0,
                    "missing_cells_rate": 0,
                    "duplicate_full_rows_count": 0,
                    "empty_columns_count": 0,
                    "status": dataset["status"],
                    "error_message": dataset["error_message"],
                }
            )
            continue

        missing_mask = build_missing_mask(df)
        total_cells = int(df.shape[0] * df.shape[1])
        missing_cells_count = int(missing_mask.sum().sum())

        empty_columns_count = int(
            sum(missing_mask[column].all() for column in df.columns)
        )

        duplicate_full_rows_count = int(df.duplicated().sum())

        rows.append(
            {
                "source_category": dataset["source_category"],
                "dataset_name": dataset["dataset_name"],
                "file_name": dataset["file_name"],
                "file_path": str(dataset["file_path"]),
                "row_count": int(len(df)),
                "column_count": int(len(df.columns)),
                "missing_cells_count": missing_cells_count,
                "missing_cells_rate": round(
                    missing_cells_count / total_cells, 4
                )
                if total_cells > 0
                else 0,
                "duplicate_full_rows_count": duplicate_full_rows_count,
                "empty_columns_count": empty_columns_count,
                "status": dataset["status"],
                "error_message": dataset["error_message"],
            }
        )

    return pd.DataFrame(rows)


def build_column_level_report(datasets: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Build a report at column level.

    It detects missing values, invalid dates, invalid emails, invalid
    numeric values, negative values, and invalid allowed values.
    """
    rows = []

    for dataset in datasets:
        if dataset["status"] != "loaded":
            continue

        df = dataset["dataframe"]
        dataset_name = dataset["dataset_name"]
        row_count = len(df)

        missing_mask = build_missing_mask(df)

        configured_date_columns = set(get_configured_columns(DATE_COLUMNS, dataset_name))
        configured_email_columns = set(get_configured_columns(EMAIL_COLUMNS, dataset_name))
        configured_numeric_columns = set(
            get_configured_columns(NUMERIC_COLUMNS, dataset_name)
        )

        for column in df.columns:
            missing_count = int(missing_mask[column].sum())
            non_missing_count = int(row_count - missing_count)

            non_missing_values = df.loc[~missing_mask[column], column].astype(str)
            unique_count = int(non_missing_values.nunique())

            sample_values = non_missing_values.drop_duplicates().head(5).tolist()

            invalid_date_count: Optional[int] = None
            invalid_email_count: Optional[int] = None
            invalid_numeric_count: Optional[int] = None
            negative_numeric_count: Optional[int] = None
            invalid_allowed_value_count: Optional[int] = None

            should_check_date = (
                column in configured_date_columns or column_looks_like_date(column)
            )

            should_check_email = (
                column in configured_email_columns or column.lower() == "email"
            )

            should_check_numeric = (
                column in configured_numeric_columns or column_looks_like_numeric(column)
            )

            if should_check_date:
                parsed_dates = parse_datetime_series(df[column])
                invalid_date_count = int(
                    ((~missing_mask[column]) & parsed_dates.isna()).sum()
                )

            if should_check_email:
                invalid_email_count = int(
                    df.loc[~missing_mask[column], column]
                    .map(lambda value: not is_valid_email(value))
                    .sum()
                )

            if should_check_numeric:
                parsed_numeric = parse_numeric_series(df[column])
                invalid_numeric_count = int(
                    ((~missing_mask[column]) & parsed_numeric.isna()).sum()
                )
                negative_numeric_count = int((parsed_numeric < 0).sum())

            if column in ALLOWED_VALUES:
                allowed = ALLOWED_VALUES[column]
                normalized_values = df[column].astype(str).str.strip().str.lower()

                invalid_allowed_value_count = int(
                    (
                        (~missing_mask[column])
                        & (~normalized_values.isin(allowed))
                    ).sum()
                )

            rows.append(
                {
                    "source_category": dataset["source_category"],
                    "dataset_name": dataset_name,
                    "file_name": dataset["file_name"],
                    "column_name": column,
                    "row_count": row_count,
                    "missing_count": missing_count,
                    "missing_rate": round(missing_count / row_count, 4)
                    if row_count > 0
                    else 0,
                    "non_missing_count": non_missing_count,
                    "unique_count": unique_count,
                    "sample_values": " | ".join(sample_values),
                    "invalid_date_count": invalid_date_count,
                    "invalid_email_count": invalid_email_count,
                    "invalid_numeric_count": invalid_numeric_count,
                    "negative_numeric_count": negative_numeric_count,
                    "invalid_allowed_value_count": invalid_allowed_value_count,
                }
            )

    return pd.DataFrame(rows)


def add_business_issue(
    rows: List[Dict[str, Any]],
    source_category: str,
    dataset_name: str,
    issue_type: str,
    severity: str,
    column_name: str,
    affected_rows_count: int,
    rule_description: str,
    recommendation: str,
) -> None:
    """
    Add one business rule issue to the report.
    """
    if affected_rows_count <= 0:
        return

    rows.append(
        {
            "source_category": source_category,
            "dataset_name": dataset_name,
            "issue_type": issue_type,
            "severity": severity,
            "column_name": column_name,
            "affected_rows_count": int(affected_rows_count),
            "rule_description": rule_description,
            "recommendation": recommendation,
        }
    )


def choose_canonical_datasets(datasets: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    Choose one canonical dataset per entity for business rule checks.

    Priority:
    1. raw datasets;
    2. file extracts;
    3. other extracted datasets.
    """
    priority = {
        "raw": 1,
        "file_extracts": 2,
        "api_extracts": 3,
        "scraping_extracts": 4,
        "database_extracts": 5,
        "bigdata_extracts": 6,
    }

    canonical: Dict[str, Dict[str, Any]] = {}

    for dataset in datasets:
        if dataset["status"] != "loaded":
            continue

        dataset_name = dataset["dataset_name"]

        if dataset_name not in PRIMARY_KEYS:
            continue

        if dataset_name not in canonical:
            canonical[dataset_name] = dataset
            continue

        current_priority = priority.get(dataset["source_category"], 99)
        existing_priority = priority.get(canonical[dataset_name]["source_category"], 99)

        if current_priority < existing_priority:
            canonical[dataset_name] = dataset

    return canonical


def check_primary_keys(
    canonical: Dict[str, Dict[str, Any]],
    rows: List[Dict[str, Any]],
) -> None:
    """
    Check missing and duplicated primary keys.
    """
    for dataset_name, dataset in canonical.items():
        df = dataset["dataframe"]
        primary_key_columns = PRIMARY_KEYS.get(dataset_name, [])

        for primary_key_column in primary_key_columns:
            if primary_key_column not in df.columns:
                add_business_issue(
                    rows,
                    dataset["source_category"],
                    dataset_name,
                    "missing_primary_key_column",
                    "critical",
                    primary_key_column,
                    len(df),
                    "The expected primary key column is missing from the dataset.",
                    "Check the source schema and extraction script.",
                )
                continue

            missing_mask = df[primary_key_column].map(is_missing_value)

            add_business_issue(
                rows,
                dataset["source_category"],
                dataset_name,
                "missing_primary_key_value",
                "critical",
                primary_key_column,
                int(missing_mask.sum()),
                "Primary key values must not be missing.",
                "Remove corrupted rows or regenerate valid identifiers.",
            )

            valid_keys = df.loc[~missing_mask, primary_key_column].astype(str)
            duplicated_count = int(valid_keys.duplicated(keep=False).sum())

            add_business_issue(
                rows,
                dataset["source_category"],
                dataset_name,
                "duplicated_primary_key",
                "critical",
                primary_key_column,
                duplicated_count,
                "Primary key values must be unique.",
                "Deduplicate rows and keep one reliable version per identifier.",
            )


def check_dates(
    canonical: Dict[str, Dict[str, Any]],
    rows: List[Dict[str, Any]],
) -> None:
    """
    Check invalid dates in configured date columns.
    """
    for dataset_name, date_columns in DATE_COLUMNS.items():
        if dataset_name not in canonical:
            continue

        dataset = canonical[dataset_name]
        df = dataset["dataframe"]

        for column in date_columns:
            if column not in df.columns:
                continue

            missing_mask = df[column].map(is_missing_value)
            parsed_dates = parse_datetime_series(df[column])

            invalid_count = int(((~missing_mask) & parsed_dates.isna()).sum())

            add_business_issue(
                rows,
                dataset["source_category"],
                dataset_name,
                "invalid_date_format",
                "major",
                column,
                invalid_count,
                "Date columns must contain parseable date or datetime values.",
                "Standardize date formats during the cleaning phase.",
            )


def check_emails(
    canonical: Dict[str, Dict[str, Any]],
    rows: List[Dict[str, Any]],
) -> None:
    """
    Check invalid email formats.
    """
    for dataset_name, email_columns in EMAIL_COLUMNS.items():
        if dataset_name not in canonical:
            continue

        dataset = canonical[dataset_name]
        df = dataset["dataframe"]

        for column in email_columns:
            if column not in df.columns:
                continue

            missing_mask = df[column].map(is_missing_value)

            invalid_count = int(
                df.loc[~missing_mask, column]
                .map(lambda value: not is_valid_email(value))
                .sum()
            )

            add_business_issue(
                rows,
                dataset["source_category"],
                dataset_name,
                "invalid_email_format",
                "major",
                column,
                invalid_count,
                "Email values must follow a valid email format.",
                "Correct invalid emails or set them to null if they are unusable.",
            )


def check_numeric_values(
    canonical: Dict[str, Dict[str, Any]],
    rows: List[Dict[str, Any]],
) -> None:
    """
    Check invalid and negative numeric values.
    """
    for dataset_name, numeric_columns in NUMERIC_COLUMNS.items():
        if dataset_name not in canonical:
            continue

        dataset = canonical[dataset_name]
        df = dataset["dataframe"]

        for column in numeric_columns:
            if column not in df.columns:
                continue

            missing_mask = df[column].map(is_missing_value)
            parsed_numeric = parse_numeric_series(df[column])

            invalid_count = int(((~missing_mask) & parsed_numeric.isna()).sum())
            negative_count = int((parsed_numeric < 0).sum())

            add_business_issue(
                rows,
                dataset["source_category"],
                dataset_name,
                "invalid_numeric_value",
                "major",
                column,
                invalid_count,
                "Numeric columns must contain parseable numeric values.",
                "Convert numeric formats and remove unusable values during cleaning.",
            )

            add_business_issue(
                rows,
                dataset["source_category"],
                dataset_name,
                "negative_numeric_value",
                "major",
                column,
                negative_count,
                "This numeric column should not contain negative values in this business context.",
                "Investigate negative values and correct or remove corrupted rows.",
            )


def check_allowed_values(
    canonical: Dict[str, Dict[str, Any]],
    rows: List[Dict[str, Any]],
) -> None:
    """
    Check invalid categorical values.
    """
    for dataset_name, dataset in canonical.items():
        df = dataset["dataframe"]

        for column, allowed_values in ALLOWED_VALUES.items():
            if column not in df.columns:
                continue

            missing_mask = df[column].map(is_missing_value)
            normalized_values = df[column].astype(str).str.strip().str.lower()

            invalid_count = int(
                (
                    (~missing_mask)
                    & (~normalized_values.isin(allowed_values))
                ).sum()
            )

            add_business_issue(
                rows,
                dataset["source_category"],
                dataset_name,
                "invalid_allowed_value",
                "major",
                column,
                invalid_count,
                "Categorical values must belong to the authorized list.",
                "Normalize categorical values during the cleaning phase.",
            )


def check_referential_integrity(
    canonical: Dict[str, Dict[str, Any]],
    rows: List[Dict[str, Any]],
) -> None:
    """
    Check foreign key consistency between canonical datasets.
    """
    for rule in REFERENCE_RULES:
        source_entity = rule["source_entity"]
        source_column = rule["source_column"]
        target_entity = rule["target_entity"]
        target_column = rule["target_column"]

        if source_entity not in canonical or target_entity not in canonical:
            continue

        source_dataset = canonical[source_entity]
        target_dataset = canonical[target_entity]

        source_df = source_dataset["dataframe"]
        target_df = target_dataset["dataframe"]

        if source_column not in source_df.columns or target_column not in target_df.columns:
            continue

        source_missing_mask = source_df[source_column].map(is_missing_value)
        target_missing_mask = target_df[target_column].map(is_missing_value)

        target_values = set(
            target_df.loc[~target_missing_mask, target_column].astype(str).str.strip()
        )

        source_values = source_df[source_column].astype(str).str.strip()

        invalid_reference_count = int(
            (
                (~source_missing_mask)
                & (~source_values.isin(target_values))
            ).sum()
        )

        add_business_issue(
            rows,
            source_dataset["source_category"],
            source_entity,
            "invalid_foreign_key_reference",
            "critical",
            source_column,
            invalid_reference_count,
            f"{source_entity}.{source_column} must exist in {target_entity}.{target_column}.",
            "Remove corrupted rows, fix references, or create missing referenced entities.",
        )


def check_temporal_consistency(
    canonical: Dict[str, Dict[str, Any]],
    rows: List[Dict[str, Any]],
) -> None:
    """
    Check temporal consistency rules.
    """
    for rule in TEMPORAL_RULES:
        entity = rule["entity"]
        start_column = rule["start_column"]
        end_column = rule["end_column"]
        issue_type = rule["issue_type"]

        if entity not in canonical:
            continue

        dataset = canonical[entity]
        df = dataset["dataframe"]

        if start_column not in df.columns or end_column not in df.columns:
            continue

        start_dates = parse_datetime_series(df[start_column])
        end_dates = parse_datetime_series(df[end_column])

        invalid_count = int(
            (
                start_dates.notna()
                & end_dates.notna()
                & (end_dates < start_dates)
            ).sum()
        )

        add_business_issue(
            rows,
            dataset["source_category"],
            entity,
            issue_type,
            "major",
            f"{start_column}, {end_column}",
            invalid_count,
            "The end date must not be earlier than the start date.",
            "Correct inconsistent dates or remove corrupted rows.",
        )


def check_calculated_amounts(
    canonical: Dict[str, Dict[str, Any]],
    rows: List[Dict[str, Any]],
) -> None:
    """
    Check calculated financial consistency rules.
    """
    if "cart_items" in canonical:
        dataset = canonical["cart_items"]
        df = dataset["dataframe"]

        required_columns = ["quantity", "unit_price", "line_total"]

        if all(column in df.columns for column in required_columns):
            quantity = parse_numeric_series(df["quantity"])
            unit_price = parse_numeric_series(df["unit_price"])
            line_total = parse_numeric_series(df["line_total"])

            expected_line_total = quantity * unit_price

            inconsistent_count = int(
                (
                    quantity.notna()
                    & unit_price.notna()
                    & line_total.notna()
                    & ((expected_line_total - line_total).abs() > 0.01)
                ).sum()
            )

            add_business_issue(
                rows,
                dataset["source_category"],
                "cart_items",
                "inconsistent_line_total",
                "major",
                "quantity, unit_price, line_total",
                inconsistent_count,
                "line_total should be equal to quantity multiplied by unit_price.",
                "Recalculate line totals during the cleaning phase.",
            )

    if "orders" in canonical and "payments" in canonical:
        orders_dataset = canonical["orders"]
        payments_dataset = canonical["payments"]

        orders_df = orders_dataset["dataframe"]
        payments_df = payments_dataset["dataframe"]

        if (
            "order_id" in orders_df.columns
            and "order_amount" in orders_df.columns
            and "currency" in orders_df.columns
            and "order_id" in payments_df.columns
            and "payment_amount" in payments_df.columns
            and "currency" in payments_df.columns
        ):
            merged_df = payments_df.merge(
                orders_df[["order_id", "order_amount", "currency"]],
                on="order_id",
                how="left",
                suffixes=("_payment", "_order"),
            )

            order_amount = parse_numeric_series(merged_df["order_amount"])
            payment_amount = parse_numeric_series(merged_df["payment_amount"])

            amount_mismatch_count = int(
                (
                    order_amount.notna()
                    & payment_amount.notna()
                    & ((order_amount - payment_amount).abs() > 0.01)
                ).sum()
            )

            currency_mismatch_count = int(
                (
                    merged_df["currency_payment"].astype(str).str.strip().str.upper()
                    != merged_df["currency_order"].astype(str).str.strip().str.upper()
                )
                .fillna(False)
                .sum()
            )

            add_business_issue(
                rows,
                payments_dataset["source_category"],
                "payments",
                "payment_order_amount_mismatch",
                "major",
                "payment_amount, order_amount",
                amount_mismatch_count,
                "Payment amount should match the related order amount.",
                "Investigate mismatches and decide which source is authoritative.",
            )

            add_business_issue(
                rows,
                payments_dataset["source_category"],
                "payments",
                "payment_order_currency_mismatch",
                "major",
                "currency",
                currency_mismatch_count,
                "Payment currency should match the related order currency.",
                "Normalize and validate currency values during cleaning.",
            )

    if "carts" in canonical and "cart_items" in canonical:
        carts_dataset = canonical["carts"]
        cart_items_dataset = canonical["cart_items"]

        carts_df = carts_dataset["dataframe"]
        items_df = cart_items_dataset["dataframe"]

        if (
            "cart_id" in carts_df.columns
            and "total_amount" in carts_df.columns
            and "cart_id" in items_df.columns
            and "line_total" in items_df.columns
        ):
            items_df = items_df.copy()
            items_df["line_total_numeric"] = parse_numeric_series(items_df["line_total"])

            item_totals = (
                items_df.groupby("cart_id", dropna=False)["line_total_numeric"]
                .sum()
                .reset_index()
                .rename(columns={"line_total_numeric": "calculated_cart_total"})
            )

            merged_df = carts_df.merge(item_totals, on="cart_id", how="left")

            cart_total = parse_numeric_series(merged_df["total_amount"])
            calculated_total = merged_df["calculated_cart_total"]

            inconsistent_count = int(
                (
                    cart_total.notna()
                    & calculated_total.notna()
                    & ((cart_total - calculated_total).abs() > 0.01)
                ).sum()
            )

            add_business_issue(
                rows,
                carts_dataset["source_category"],
                "carts",
                "cart_total_amount_mismatch",
                "major",
                "total_amount",
                inconsistent_count,
                "Cart total amount should match the sum of cart item line totals.",
                "Recalculate cart totals during the cleaning phase.",
            )


def build_business_rules_report(datasets: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Build a business rules quality report.
    """
    rows: List[Dict[str, Any]] = []

    canonical = choose_canonical_datasets(datasets)

    check_primary_keys(canonical, rows)
    check_dates(canonical, rows)
    check_emails(canonical, rows)
    check_numeric_values(canonical, rows)
    check_allowed_values(canonical, rows)
    check_referential_integrity(canonical, rows)
    check_temporal_consistency(canonical, rows)
    check_calculated_amounts(canonical, rows)

    return pd.DataFrame(rows)


def build_summary_report(
    file_report_df: pd.DataFrame,
    column_report_df: pd.DataFrame,
    business_rules_report_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build a global summary report.
    """
    rows = []

    rows.append(
        {
            "metric": "analysis_timestamp",
            "value": get_current_timestamp(),
        }
    )

    rows.append(
        {
            "metric": "datasets_analyzed",
            "value": int(len(file_report_df)),
        }
    )

    rows.append(
        {
            "metric": "loaded_datasets",
            "value": int((file_report_df["status"] == "loaded").sum())
            if "status" in file_report_df.columns
            else 0,
        }
    )

    rows.append(
        {
            "metric": "total_rows_analyzed",
            "value": int(file_report_df["row_count"].sum())
            if "row_count" in file_report_df.columns
            else 0,
        }
    )

    rows.append(
        {
            "metric": "total_missing_cells",
            "value": int(file_report_df["missing_cells_count"].sum())
            if "missing_cells_count" in file_report_df.columns
            else 0,
        }
    )

    rows.append(
        {
            "metric": "total_duplicate_full_rows",
            "value": int(file_report_df["duplicate_full_rows_count"].sum())
            if "duplicate_full_rows_count" in file_report_df.columns
            else 0,
        }
    )

    rows.append(
        {
            "metric": "total_business_rule_issues",
            "value": int(len(business_rules_report_df)),
        }
    )

    if not business_rules_report_df.empty:
        severity_counts = (
            business_rules_report_df.groupby("severity")["affected_rows_count"]
            .sum()
            .reset_index()
        )

        for _, row in severity_counts.iterrows():
            rows.append(
                {
                    "metric": f"affected_rows_{row['severity']}",
                    "value": int(row["affected_rows_count"]),
                }
            )

        issue_counts = (
            business_rules_report_df.groupby("issue_type")["affected_rows_count"]
            .sum()
            .reset_index()
        )

        for _, row in issue_counts.iterrows():
            rows.append(
                {
                    "metric": f"issue_{row['issue_type']}",
                    "value": int(row["affected_rows_count"]),
                }
            )

    if not column_report_df.empty:
        numeric_columns = [
            "invalid_date_count",
            "invalid_email_count",
            "invalid_numeric_count",
            "negative_numeric_count",
            "invalid_allowed_value_count",
        ]

        for column in numeric_columns:
            if column in column_report_df.columns:
                rows.append(
                    {
                        "metric": f"column_report_total_{column}",
                        "value": int(column_report_df[column].fillna(0).sum()),
                    }
                )

    return pd.DataFrame(rows)


def save_reports(
    file_report_df: pd.DataFrame,
    column_report_df: pd.DataFrame,
    business_rules_report_df: pd.DataFrame,
    summary_df: pd.DataFrame,
) -> None:
    """
    Save all generated reports.
    """
    file_report_df.to_csv(OUTPUT_FILE_REPORT, index=False, encoding="utf-8")
    column_report_df.to_csv(OUTPUT_COLUMN_REPORT, index=False, encoding="utf-8")
    business_rules_report_df.to_csv(
        OUTPUT_BUSINESS_RULES_REPORT,
        index=False,
        encoding="utf-8",
    )
    summary_df.to_csv(OUTPUT_SUMMARY, index=False, encoding="utf-8")


def analyze_extracted_data_quality() -> None:
    """
    Run the full extracted data quality analysis.
    """
    logging.info("Starting extracted data quality analysis.")

    datasets = load_datasets()

    file_report_df = build_file_level_report(datasets)
    column_report_df = build_column_level_report(datasets)
    business_rules_report_df = build_business_rules_report(datasets)

    summary_df = build_summary_report(
        file_report_df=file_report_df,
        column_report_df=column_report_df,
        business_rules_report_df=business_rules_report_df,
    )

    save_reports(
        file_report_df=file_report_df,
        column_report_df=column_report_df,
        business_rules_report_df=business_rules_report_df,
        summary_df=summary_df,
    )

    logging.info("Extracted data quality analysis completed successfully.")


def main() -> None:
    """
    Entry point of the script.
    """
    ensure_directories()
    setup_logging()
    analyze_extracted_data_quality()

    file_report_df = pd.read_csv(OUTPUT_FILE_REPORT)
    business_rules_report_df = pd.read_csv(OUTPUT_BUSINESS_RULES_REPORT)
    summary_df = pd.read_csv(OUTPUT_SUMMARY)

    print("Extracted data quality analysis completed successfully.")
    print(f"File report: {OUTPUT_FILE_REPORT}")
    print(f"Column report: {OUTPUT_COLUMN_REPORT}")
    print(f"Business rules report: {OUTPUT_BUSINESS_RULES_REPORT}")
    print(f"Summary report: {OUTPUT_SUMMARY}")
    print(f"Log file: {LOG_FILE}")
    print("")
    print("Datasets analyzed:")
    print(file_report_df["source_category"].value_counts().to_string())
    print("")
    print("Business issue count:")
    print(len(business_rules_report_df))
    print("")
    print("Summary:")
    print(summary_df.to_string(index=False))


if __name__ == "__main__":
    main()