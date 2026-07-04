from pathlib import Path
import re
from typing import Dict, List, Optional

import pandas as pd


# -------------------------------------------------------------------
# Raw data quality analysis
# -------------------------------------------------------------------
# This script analyzes all raw CSV files generated for the PayLive AI
# Copilot project.
#
# The goal is not to clean the data yet.
# The goal is to identify and document data quality issues before
# building the cleaning rules.
#
# The generated reports will be used as evidence in the final report:
# - missing values;
# - duplicated rows;
# - duplicated identifiers;
# - invalid dates;
# - invalid emails;
# - invalid statuses;
# - negative amounts;
# - broken relationships between files.
#
# Reports are saved in data/interim/reports/raw_quality.
# -------------------------------------------------------------------


BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"
INTERIM_DIR = BASE_DIR / "data" / "interim"

INTERIM_REPORTS_DIR = INTERIM_DIR / "reports"
RAW_QUALITY_REPORTS_DIR = INTERIM_REPORTS_DIR / "raw_quality"

QUALITY_FILE_REPORT_PATH = RAW_QUALITY_REPORTS_DIR / "quality_report_files.csv"
QUALITY_COLUMN_REPORT_PATH = RAW_QUALITY_REPORTS_DIR / "quality_report_columns.csv"
QUALITY_BUSINESS_RULE_REPORT_PATH = RAW_QUALITY_REPORTS_DIR / "quality_report_business_rules.csv"


PRIMARY_KEYS = {
    "sellers_raw.csv": "seller_id",
    "customers_raw.csv": "customer_id",
    "products_raw.csv": "product_id",
    "live_sessions_raw.csv": "live_id",
    "live_products_raw.csv": "live_product_id",
    "live_comments_raw.csv": "comment_id",
    "carts_raw.csv": "cart_id",
    "cart_items_raw.csv": "cart_item_id",
    "orders_raw.csv": "order_id",
    "payments_raw.csv": "payment_id",
    "stock_movements_raw.csv": "stock_movement_id",
    "live_events_raw.csv": "event_id",
}


DATE_COLUMNS = {
    "sellers_raw.csv": ["created_at"],
    "customers_raw.csv": ["created_at"],
    "products_raw.csv": ["created_at"],
    "live_sessions_raw.csv": [
        "scheduled_start_at",
        "actual_start_at",
        "ended_at",
        "created_at",
    ],
    "live_comments_raw.csv": ["commented_at"],
    "carts_raw.csv": ["created_at", "updated_at"],
    "orders_raw.csv": ["created_at", "confirmed_at"],
    "payments_raw.csv": ["paid_at"],
    "stock_movements_raw.csv": ["created_at"],
    "live_events_raw.csv": ["event_timestamp"],
}


ALLOWED_VALUES = {
    "platform": {
        "tiktok",
        "instagram",
        "facebook_live",
        "youtube_live",
        "other",
    },
    "seller_status": {
        "active",
        "inactive",
        "suspended",
    },
    "live_status": {
        "scheduled",
        "live",
        "ended",
        "cancelled",
    },
    "product_status": {
        "active",
        "inactive",
        "out_of_stock",
    },
    "cart_status": {
        "created",
        "pending_payment",
        "paid",
        "abandoned",
        "cancelled",
    },
    "order_status": {
        "pending",
        "confirmed",
        "paid",
        "cancelled",
        "refunded",
    },
    "payment_status": {
        "pending",
        "succeeded",
        "failed",
        "refunded",
    },
    "movement_type": {
        "sale",
        "return",
        "adjustment",
        "restock",
    },
    "event_type": {
        "comment_sent",
        "cart_opened",
        "payment_clicked",
        "payment_succeeded",
        "api_error",
        "product_viewed",
    },
    "currency": {
        "EUR",
    },
}


NUMERIC_COLUMNS = {
    "products_raw.csv": ["unit_price", "stock_quantity"],
    "live_sessions_raw.csv": ["peak_viewers"],
    "live_products_raw.csv": [
        "display_order",
        "special_live_price",
        "initial_stock",
        "remaining_stock",
    ],
    "carts_raw.csv": ["total_amount"],
    "cart_items_raw.csv": ["quantity", "unit_price", "line_total"],
    "orders_raw.csv": ["order_amount"],
    "payments_raw.csv": ["payment_amount"],
    "stock_movements_raw.csv": ["quantity_change"],
}


EMAIL_COLUMNS = {
    "sellers_raw.csv": ["email"],
    "customers_raw.csv": ["email"],
}


REFERENCE_RULES = [
    {
        "file_name": "live_sessions_raw.csv",
        "column": "seller_id",
        "reference_file": "sellers_raw.csv",
        "reference_column": "seller_id",
    },
    {
        "file_name": "live_products_raw.csv",
        "column": "live_id",
        "reference_file": "live_sessions_raw.csv",
        "reference_column": "live_id",
    },
    {
        "file_name": "live_products_raw.csv",
        "column": "product_id",
        "reference_file": "products_raw.csv",
        "reference_column": "product_id",
    },
    {
        "file_name": "live_comments_raw.csv",
        "column": "live_id",
        "reference_file": "live_sessions_raw.csv",
        "reference_column": "live_id",
    },
    {
        "file_name": "live_comments_raw.csv",
        "column": "customer_id",
        "reference_file": "customers_raw.csv",
        "reference_column": "customer_id",
    },
    {
        "file_name": "carts_raw.csv",
        "column": "live_id",
        "reference_file": "live_sessions_raw.csv",
        "reference_column": "live_id",
    },
    {
        "file_name": "carts_raw.csv",
        "column": "customer_id",
        "reference_file": "customers_raw.csv",
        "reference_column": "customer_id",
    },
    {
        "file_name": "cart_items_raw.csv",
        "column": "cart_id",
        "reference_file": "carts_raw.csv",
        "reference_column": "cart_id",
    },
    {
        "file_name": "cart_items_raw.csv",
        "column": "product_id",
        "reference_file": "products_raw.csv",
        "reference_column": "product_id",
    },
    {
        "file_name": "orders_raw.csv",
        "column": "cart_id",
        "reference_file": "carts_raw.csv",
        "reference_column": "cart_id",
    },
    {
        "file_name": "orders_raw.csv",
        "column": "customer_id",
        "reference_file": "customers_raw.csv",
        "reference_column": "customer_id",
    },
    {
        "file_name": "orders_raw.csv",
        "column": "seller_id",
        "reference_file": "sellers_raw.csv",
        "reference_column": "seller_id",
    },
    {
        "file_name": "payments_raw.csv",
        "column": "order_id",
        "reference_file": "orders_raw.csv",
        "reference_column": "order_id",
    },
    {
        "file_name": "stock_movements_raw.csv",
        "column": "product_id",
        "reference_file": "products_raw.csv",
        "reference_column": "product_id",
    },
    {
        "file_name": "live_events_raw.csv",
        "column": "live_id",
        "reference_file": "live_sessions_raw.csv",
        "reference_column": "live_id",
    },
]


def ensure_directories() -> None:
    """
    Create the output directory for raw data quality reports.

    Raw quality reports are saved in `data/interim/reports/raw_quality`
    to keep interim extracts and technical reports separated.
    """
    RAW_QUALITY_REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def load_raw_csv_files() -> Dict[str, pd.DataFrame]:
    """
    Load all raw CSV files from the raw data folder.

    All columns are loaded as strings first.
    This avoids type errors when raw data contains mixed values,
    such as invalid dates, empty strings, or invalid numeric values.
    """
    datasets = {}

    for file_path in sorted(RAW_DIR.glob("*.csv")):
        datasets[file_path.name] = pd.read_csv(
            file_path,
            dtype=str,
            keep_default_na=False,
            encoding="utf-8",
        )

    return datasets


def is_missing_value(value: object) -> bool:
    """
    Detect whether a value should be considered missing.

    In raw CSV files, missing values can appear as empty strings,
    spaces, textual null values, or actual pandas null values.
    """
    if pd.isna(value):
        return True

    value_as_text = str(value).strip().lower()

    return value_as_text in {"", "nan", "none", "null", "na", "n/a"}


def count_missing_values(df: pd.DataFrame) -> int:
    """
    Count all missing values in a DataFrame.

    This function applies the project-specific missing value logic
    to every cell of the dataset.
    """
    return int(df.apply(lambda column: column.map(is_missing_value)).sum().sum())


def count_missing_values_in_column(series: pd.Series) -> int:
    """
    Count missing values in one column.

    This is used for the column-level quality report.
    """
    return int(series.map(is_missing_value).sum())


def count_duplicate_primary_keys(
    df: pd.DataFrame,
    primary_key: Optional[str],
) -> int:
    """
    Count duplicated primary key values.

    Empty primary keys are ignored here because they are counted
    separately as missing values.
    """
    if not primary_key or primary_key not in df.columns:
        return 0

    valid_keys = df[primary_key][~df[primary_key].map(is_missing_value)]

    return int(valid_keys.duplicated().sum())


def count_invalid_dates(
    df: pd.DataFrame,
    file_name: str,
) -> int:
    """
    Count invalid date values for a given raw dataset.

    A date is considered invalid if pandas cannot parse it.
    Empty values are ignored here because they are already counted
    as missing values.
    """
    invalid_count = 0

    for column in DATE_COLUMNS.get(file_name, []):
        if column not in df.columns:
            continue

        non_empty_values = df[column][~df[column].map(is_missing_value)]
        parsed_dates = pd.to_datetime(non_empty_values, errors="coerce")

        invalid_count += int(parsed_dates.isna().sum())

    return invalid_count


def count_invalid_emails(
    df: pd.DataFrame,
    file_name: str,
) -> int:
    """
    Count invalid email addresses.

    The goal is not to perfectly validate emails.
    The goal is to detect obvious invalid values in the simulated raw data.
    """
    email_pattern = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    invalid_count = 0

    for column in EMAIL_COLUMNS.get(file_name, []):
        if column not in df.columns:
            continue

        non_empty_values = df[column][~df[column].map(is_missing_value)]

        invalid_count += int(
            non_empty_values.apply(
                lambda value: not bool(email_pattern.match(str(value).strip()))
            ).sum()
        )

    return invalid_count


def count_negative_numeric_values(
    df: pd.DataFrame,
    file_name: str,
) -> int:
    """
    Count negative values in numeric columns.

    In this project, negative prices, amounts, stocks, or quantities
    are considered suspicious and must be reviewed during cleaning.
    """
    negative_count = 0

    for column in NUMERIC_COLUMNS.get(file_name, []):
        if column not in df.columns:
            continue

        numeric_values = pd.to_numeric(df[column], errors="coerce")
        negative_count += int((numeric_values < 0).sum())

    return negative_count


def count_invalid_allowed_values(
    df: pd.DataFrame,
) -> int:
    """
    Count values that are not part of the allowed business lists.

    For example, a platform should be `tiktok` or `instagram`,
    but raw data may contain values such as `insta`, `TikTok`, or `ig`.
    """
    invalid_count = 0

    for column, allowed_values in ALLOWED_VALUES.items():
        if column not in df.columns:
            continue

        non_empty_values = df[column][~df[column].map(is_missing_value)]

        invalid_count += int(
            non_empty_values.apply(
                lambda value: str(value).strip() not in allowed_values
            ).sum()
        )

    return invalid_count


def build_file_level_report(
    datasets: Dict[str, pd.DataFrame],
) -> pd.DataFrame:
    """
    Build a global quality report at file level.

    Each row of the report describes the quality status of one raw file.
    """
    rows = []

    for file_name, df in datasets.items():
        primary_key = PRIMARY_KEYS.get(file_name)

        row_count = len(df)
        column_count = len(df.columns)
        duplicate_rows = int(df.duplicated().sum())
        duplicate_primary_keys = count_duplicate_primary_keys(df, primary_key)
        missing_values = count_missing_values(df)
        total_cells = row_count * column_count if row_count and column_count else 0
        missing_rate = round((missing_values / total_cells) * 100, 2) if total_cells else 0

        invalid_dates = count_invalid_dates(df, file_name)
        invalid_emails = count_invalid_emails(df, file_name)
        negative_values = count_negative_numeric_values(df, file_name)
        invalid_allowed_values = count_invalid_allowed_values(df)

        rows.append(
            {
                "file_name": file_name,
                "row_count": row_count,
                "column_count": column_count,
                "primary_key": primary_key,
                "duplicate_rows": duplicate_rows,
                "duplicate_primary_keys": duplicate_primary_keys,
                "missing_values": missing_values,
                "missing_rate_percent": missing_rate,
                "invalid_dates": invalid_dates,
                "invalid_emails": invalid_emails,
                "negative_numeric_values": negative_values,
                "invalid_allowed_values": invalid_allowed_values,
            }
        )

    return pd.DataFrame(rows)


def build_column_level_report(
    datasets: Dict[str, pd.DataFrame],
) -> pd.DataFrame:
    """
    Build a detailed report at column level.

    This report helps identify which columns contain the most missing
    values and how many unique values each column contains.
    """
    rows = []

    for file_name, df in datasets.items():
        row_count = len(df)

        for column in df.columns:
            missing_count = count_missing_values_in_column(df[column])
            missing_rate = round((missing_count / row_count) * 100, 2) if row_count else 0
            unique_count = int(df[column].nunique(dropna=False))

            rows.append(
                {
                    "file_name": file_name,
                    "column_name": column,
                    "row_count": row_count,
                    "missing_count": missing_count,
                    "missing_rate_percent": missing_rate,
                    "unique_count": unique_count,
                }
            )

    return pd.DataFrame(rows)


def add_business_issue(
    issues: List[dict],
    rule_code: str,
    file_name: str,
    column_name: str,
    issue_type: str,
    issue_count: int,
    severity: str,
    details: str,
) -> None:
    """
    Add a business rule issue to the issue list.

    This helper keeps the business rule report consistent.
    """
    if issue_count <= 0:
        return

    issues.append(
        {
            "rule_code": rule_code,
            "file_name": file_name,
            "column_name": column_name,
            "issue_type": issue_type,
            "issue_count": issue_count,
            "severity": severity,
            "details": details,
        }
    )


def check_primary_keys(
    datasets: Dict[str, pd.DataFrame],
    issues: List[dict],
) -> None:
    """
    Check missing and duplicated primary keys.

    A primary key must be unique and not empty.
    """
    for file_name, primary_key in PRIMARY_KEYS.items():
        if file_name not in datasets:
            continue

        df = datasets[file_name]

        if primary_key not in df.columns:
            continue

        missing_count = count_missing_values_in_column(df[primary_key])
        duplicate_count = count_duplicate_primary_keys(df, primary_key)

        add_business_issue(
            issues,
            "PK_001",
            file_name,
            primary_key,
            "missing_primary_key",
            missing_count,
            "critical",
            "Primary key values must not be empty.",
        )

        add_business_issue(
            issues,
            "PK_002",
            file_name,
            primary_key,
            "duplicated_primary_key",
            duplicate_count,
            "critical",
            "Primary key values must be unique.",
        )


def check_dates(
    datasets: Dict[str, pd.DataFrame],
    issues: List[dict],
) -> None:
    """
    Check invalid date columns.

    Dates must be parseable before being imported into PostgreSQL.
    """
    for file_name, date_columns in DATE_COLUMNS.items():
        if file_name not in datasets:
            continue

        df = datasets[file_name]

        for column in date_columns:
            if column not in df.columns:
                continue

            non_empty_values = df[column][~df[column].map(is_missing_value)]
            parsed_dates = pd.to_datetime(non_empty_values, errors="coerce")
            invalid_count = int(parsed_dates.isna().sum())

            add_business_issue(
                issues,
                "DATE_001",
                file_name,
                column,
                "invalid_date",
                invalid_count,
                "major",
                "Date values must be converted to a valid ISO timestamp.",
            )


def check_allowed_values(
    datasets: Dict[str, pd.DataFrame],
    issues: List[dict],
) -> None:
    """
    Check values against allowed business lists.

    Raw values may need normalization before they become valid.
    For example: `TikTok`, `tik tok`, and `tiktok` should become `tiktok`.
    """
    for file_name, df in datasets.items():
        for column, allowed_values in ALLOWED_VALUES.items():
            if column not in df.columns:
                continue

            non_empty_values = df[column][~df[column].map(is_missing_value)]

            invalid_count = int(
                non_empty_values.apply(
                    lambda value: str(value).strip() not in allowed_values
                ).sum()
            )

            add_business_issue(
                issues,
                "VALUE_001",
                file_name,
                column,
                "invalid_allowed_value",
                invalid_count,
                "major",
                f"Values must belong to this list: {sorted(allowed_values)}.",
            )


def check_numeric_values(
    datasets: Dict[str, pd.DataFrame],
    issues: List[dict],
) -> None:
    """
    Check invalid numeric values.

    Numeric columns must be parseable.
    Prices, amounts, and stocks should not be negative in this project.
    """
    for file_name, columns in NUMERIC_COLUMNS.items():
        if file_name not in datasets:
            continue

        df = datasets[file_name]

        for column in columns:
            if column not in df.columns:
                continue

            numeric_values = pd.to_numeric(df[column], errors="coerce")
            non_empty_values = df[column][~df[column].map(is_missing_value)]

            invalid_numeric_count = int(
                pd.to_numeric(non_empty_values, errors="coerce").isna().sum()
            )

            negative_count = int((numeric_values < 0).sum())

            add_business_issue(
                issues,
                "NUM_001",
                file_name,
                column,
                "invalid_numeric_value",
                invalid_numeric_count,
                "major",
                "Numeric values must be parseable.",
            )

            add_business_issue(
                issues,
                "NUM_002",
                file_name,
                column,
                "negative_numeric_value",
                negative_count,
                "major",
                "Negative numeric values must be reviewed.",
            )


def check_emails(
    datasets: Dict[str, pd.DataFrame],
    issues: List[dict],
) -> None:
    """
    Check invalid email formats.

    Emails are simulated, but obvious invalid values must still be detected.
    """
    email_pattern = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    for file_name, columns in EMAIL_COLUMNS.items():
        if file_name not in datasets:
            continue

        df = datasets[file_name]

        for column in columns:
            if column not in df.columns:
                continue

            non_empty_values = df[column][~df[column].map(is_missing_value)]

            invalid_count = int(
                non_empty_values.apply(
                    lambda value: not bool(email_pattern.match(str(value).strip()))
                ).sum()
            )

            add_business_issue(
                issues,
                "EMAIL_001",
                file_name,
                column,
                "invalid_email",
                invalid_count,
                "minor",
                "Email values must match a basic email format.",
            )


def check_references(
    datasets: Dict[str, pd.DataFrame],
    issues: List[dict],
) -> None:
    """
    Check relationships between raw files.

    This detects foreign keys that do not exist in the reference dataset.
    For example, an order linked to a non-existing customer.
    """
    for rule in REFERENCE_RULES:
        file_name = rule["file_name"]
        column = rule["column"]
        reference_file = rule["reference_file"]
        reference_column = rule["reference_column"]

        if file_name not in datasets or reference_file not in datasets:
            continue

        df = datasets[file_name]
        ref_df = datasets[reference_file]

        if column not in df.columns or reference_column not in ref_df.columns:
            continue

        values = df[column][~df[column].map(is_missing_value)]
        reference_values = set(
            ref_df[reference_column][~ref_df[reference_column].map(is_missing_value)]
        )

        invalid_reference_count = int(
            values.apply(lambda value: value not in reference_values).sum()
        )

        add_business_issue(
            issues,
            "REF_001",
            file_name,
            column,
            "invalid_reference",
            invalid_reference_count,
            "critical",
            f"Values must exist in {reference_file}.{reference_column}.",
        )


def check_temporal_consistency(
    datasets: Dict[str, pd.DataFrame],
    issues: List[dict],
) -> None:
    """
    Check chronological consistency between date columns.

    Example:
    A live session end date should not be before its start date.
    """
    if "live_sessions_raw.csv" in datasets:
        df = datasets["live_sessions_raw.csv"]

        if {"actual_start_at", "ended_at"}.issubset(df.columns):
            start = pd.to_datetime(df["actual_start_at"], errors="coerce")
            end = pd.to_datetime(df["ended_at"], errors="coerce")

            issue_count = int(((end < start) & start.notna() & end.notna()).sum())

            add_business_issue(
                issues,
                "TIME_001",
                "live_sessions_raw.csv",
                "ended_at",
                "end_before_start",
                issue_count,
                "critical",
                "Live session end date must be after actual start date.",
            )

    if "carts_raw.csv" in datasets:
        df = datasets["carts_raw.csv"]

        if {"created_at", "updated_at"}.issubset(df.columns):
            created = pd.to_datetime(df["created_at"], errors="coerce")
            updated = pd.to_datetime(df["updated_at"], errors="coerce")

            issue_count = int(((updated < created) & created.notna() & updated.notna()).sum())

            add_business_issue(
                issues,
                "TIME_002",
                "carts_raw.csv",
                "updated_at",
                "update_before_creation",
                issue_count,
                "major",
                "Cart update date must be after creation date.",
            )

    if "orders_raw.csv" in datasets:
        df = datasets["orders_raw.csv"]

        if {"created_at", "confirmed_at"}.issubset(df.columns):
            created = pd.to_datetime(df["created_at"], errors="coerce")
            confirmed = pd.to_datetime(df["confirmed_at"], errors="coerce")

            issue_count = int(
                ((confirmed < created) & created.notna() & confirmed.notna()).sum()
            )

            add_business_issue(
                issues,
                "TIME_003",
                "orders_raw.csv",
                "confirmed_at",
                "confirmation_before_creation",
                issue_count,
                "major",
                "Order confirmation date must be after creation date.",
            )


def check_calculated_amounts(
    datasets: Dict[str, pd.DataFrame],
    issues: List[dict],
) -> None:
    """
    Check calculated amounts in cart item lines.

    The expected line total is quantity multiplied by unit price.
    A tolerance of 0.01 is accepted because prices are decimals.
    """
    if "cart_items_raw.csv" not in datasets:
        return

    df = datasets["cart_items_raw.csv"]

    required_columns = {"quantity", "unit_price", "line_total"}

    if not required_columns.issubset(df.columns):
        return

    quantity = pd.to_numeric(df["quantity"], errors="coerce")
    unit_price = pd.to_numeric(df["unit_price"], errors="coerce")
    line_total = pd.to_numeric(df["line_total"], errors="coerce")

    expected_total = quantity * unit_price

    issue_count = int(
        (
            line_total.notna()
            & expected_total.notna()
            & ((line_total - expected_total).abs() > 0.01)
        ).sum()
    )

    add_business_issue(
        issues,
        "AMOUNT_001",
        "cart_items_raw.csv",
        "line_total",
        "incorrect_line_total",
        issue_count,
        "major",
        "Line total must be equal to quantity multiplied by unit price.",
    )


def build_business_rule_report(
    datasets: Dict[str, pd.DataFrame],
) -> pd.DataFrame:
    """
    Build the business rule quality report.

    This report contains all detected issues that are related to
    business rules, data consistency, and relational integrity.
    """
    issues = []

    check_primary_keys(datasets, issues)
    check_dates(datasets, issues)
    check_allowed_values(datasets, issues)
    check_numeric_values(datasets, issues)
    check_emails(datasets, issues)
    check_references(datasets, issues)
    check_temporal_consistency(datasets, issues)
    check_calculated_amounts(datasets, issues)

    return pd.DataFrame(issues)


def save_reports(
    file_report: pd.DataFrame,
    column_report: pd.DataFrame,
    business_rule_report: pd.DataFrame,
) -> None:
    """
    Save all raw quality reports as CSV files.

    These files are saved under `data/interim/reports/raw_quality`
    to keep the interim folder organized.
    """
    file_report.to_csv(
        QUALITY_FILE_REPORT_PATH,
        index=False,
        encoding="utf-8",
    )

    column_report.to_csv(
        QUALITY_COLUMN_REPORT_PATH,
        index=False,
        encoding="utf-8",
    )

    business_rule_report.to_csv(
        QUALITY_BUSINESS_RULE_REPORT_PATH,
        index=False,
        encoding="utf-8",
    )


def main() -> None:
    """
    Run the full raw data quality analysis.

    The script loads raw data, builds three quality reports,
    saves them in `data/interim/reports/raw_quality`, and prints a short summary.
    """
    ensure_directories()

    datasets = load_raw_csv_files()

    if not datasets:
        raise FileNotFoundError(
            f"No CSV files were found in the raw data folder: {RAW_DIR}"
        )

    file_report = build_file_level_report(datasets)
    column_report = build_column_level_report(datasets)
    business_rule_report = build_business_rule_report(datasets)

    save_reports(file_report, column_report, business_rule_report)

    print("Raw data quality analysis completed successfully.")
    print(f"Analyzed files: {len(datasets)}")
    print(f"Raw quality reports folder: {RAW_QUALITY_REPORTS_DIR}")
    print(f"File-level report: {QUALITY_FILE_REPORT_PATH}")
    print(f"Column-level report: {QUALITY_COLUMN_REPORT_PATH}")
    print(f"Business rule report: {QUALITY_BUSINESS_RULE_REPORT_PATH}")
    print(f"Detected business rule issue groups: {len(business_rule_report)}")


if __name__ == "__main__":
    main()