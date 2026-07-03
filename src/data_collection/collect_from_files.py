from pathlib import Path
from datetime import datetime
from typing import Dict, List
import hashlib
import logging

import pandas as pd


# -------------------------------------------------------------------
# File-based data collection
# -------------------------------------------------------------------
# This script is responsible for collecting data from local CSV files.
#
# In the PayLive AI Copilot project, these files represent simulated
# business exports: sellers, customers, live sessions, comments,
# products, carts, orders, payments, and events.
#
# Important:
# This script does not clean the data.
# It only extracts the raw files, checks that they exist, verifies that
# their expected columns are available, and saves an extracted copy in
# the interim data folder.
#
# Cleaning, normalization, deduplication, and business corrections will
# be done later in dedicated data processing scripts.
# -------------------------------------------------------------------


BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"
INTERIM_DIR = BASE_DIR / "data" / "interim"
EXTRACT_DIR = INTERIM_DIR / "file_extracts"
LOG_DIR = BASE_DIR / "logs"


# Expected schemas for each raw CSV file.
# These schemas are used to verify that the file extraction step receives
# the columns required by the project data dictionary.
EXPECTED_FILE_SCHEMAS: Dict[str, List[str]] = {
    "sellers_raw.csv": [
        "seller_id",
        "shop_name",
        "owner_first_name",
        "owner_last_name",
        "email",
        "phone_number",
        "country",
        "main_platform",
        "created_at",
        "seller_status",
    ],
    "customers_raw.csv": [
        "customer_id",
        "username",
        "platform",
        "email",
        "country",
        "created_at",
    ],
    "products_raw.csv": [
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
    ],
    "live_sessions_raw.csv": [
        "live_id",
        "seller_id",
        "platform",
        "live_title",
        "scheduled_start_at",
        "actual_start_at",
        "ended_at",
        "live_status",
        "peak_viewers",
        "currency",
        "created_at",
    ],
    "live_products_raw.csv": [
        "live_product_id",
        "live_id",
        "product_id",
        "display_order",
        "special_live_price",
        "initial_stock",
        "remaining_stock",
    ],
    "live_comments_raw.csv": [
        "comment_id",
        "live_id",
        "customer_id",
        "platform",
        "username",
        "comment_text",
        "commented_at",
        "comment_language",
        "manual_intent_label",
        "extracted_product_keyword",
        "data_quality_status",
    ],
    "carts_raw.csv": [
        "cart_id",
        "live_id",
        "customer_id",
        "cart_status",
        "created_at",
        "updated_at",
        "total_amount",
        "currency",
    ],
    "cart_items_raw.csv": [
        "cart_item_id",
        "cart_id",
        "product_id",
        "quantity",
        "unit_price",
        "line_total",
        "selected_size",
        "selected_color",
    ],
    "orders_raw.csv": [
        "order_id",
        "cart_id",
        "customer_id",
        "seller_id",
        "order_status",
        "order_amount",
        "currency",
        "created_at",
        "confirmed_at",
    ],
    "payments_raw.csv": [
        "payment_id",
        "order_id",
        "payment_provider",
        "payment_status",
        "payment_amount",
        "currency",
        "payment_method",
        "paid_at",
        "transaction_reference",
    ],
    "stock_movements_raw.csv": [
        "stock_movement_id",
        "product_id",
        "live_id",
        "movement_type",
        "quantity_change",
        "movement_reason",
        "created_at",
    ],
    "live_events_raw.csv": [
        "event_id",
        "live_id",
        "customer_id",
        "event_type",
        "event_timestamp",
        "event_value",
        "source_system",
    ],
}


def ensure_directories() -> None:
    """
    Create all folders required by the extraction script.

    The extracted files are saved in `data/interim/file_extracts`.
    The execution log is saved in `logs`.
    """
    INTERIM_DIR.mkdir(parents=True, exist_ok=True)
    EXTRACT_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def setup_logging() -> None:
    """
    Configure the logging system.

    Logs help prove that the extraction process was executed and make it
    easier to debug problems if a file is missing or unreadable.
    """
    log_file = LOG_DIR / "collect_from_files.log"

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        encoding="utf-8",
    )


def get_current_batch_id() -> str:
    """
    Generate a unique extraction batch ID.

    A batch ID allows all extracted files and reports from the same run
    to be linked together.
    """
    return datetime.now().strftime("FILE_BATCH_%Y%m%d_%H%M%S")


def calculate_file_hash(file_path: Path) -> str:
    """
    Calculate the SHA256 hash of a file.

    This hash is used for traceability. If the raw file changes later,
    the hash will also change.
    """
    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        for block in iter(lambda: file.read(4096), b""):
            sha256.update(block)

    return sha256.hexdigest()


def read_csv_as_raw(file_path: Path) -> pd.DataFrame:
    """
    Read a CSV file while preserving raw values as much as possible.

    All columns are loaded as strings to avoid automatic type conversion.
    This is important because raw files may contain invalid dates,
    invalid numbers, empty values, or inconsistent formats.
    """
    return pd.read_csv(
        file_path,
        dtype=str,
        keep_default_na=False,
        encoding="utf-8",
    )


def build_output_file_name(raw_file_name: str) -> str:
    """
    Build the output file name for an extracted file.

    Example:
    sellers_raw.csv becomes sellers_file_extract.csv.
    """
    return raw_file_name.replace("_raw.csv", "_file_extract.csv")


def add_extraction_metadata(
    df: pd.DataFrame,
    source_file_name: str,
    batch_id: str,
    extracted_at: str,
) -> pd.DataFrame:
    """
    Add technical extraction metadata to the extracted dataset.

    These metadata columns are useful for traceability.
    They are not business columns and can be ignored during business
    analysis if needed.
    """
    extracted_df = df.copy()

    extracted_df.insert(0, "extraction_batch_id", batch_id)
    extracted_df.insert(1, "source_file_name", source_file_name)
    extracted_df.insert(2, "extracted_at", extracted_at)

    return extracted_df


def check_schema(
    file_name: str,
    actual_columns: List[str],
    expected_columns: List[str],
) -> Dict[str, List[str]]:
    """
    Compare actual file columns with expected columns.

    The function returns missing columns and unexpected columns.
    Missing columns are more serious because they can block downstream
    processing.
    """
    actual_set = set(actual_columns)
    expected_set = set(expected_columns)

    missing_columns = sorted(list(expected_set - actual_set))
    unexpected_columns = sorted(list(actual_set - expected_set))

    return {
        "missing_columns": missing_columns,
        "unexpected_columns": unexpected_columns,
    }


def collect_one_file(
    file_name: str,
    expected_columns: List[str],
    batch_id: str,
    extracted_at: str,
) -> Dict[str, object]:
    """
    Extract one raw CSV file.

    This function:
    - checks if the file exists;
    - reads the file as raw data;
    - checks its schema;
    - adds extraction metadata;
    - saves an extracted copy in the interim folder;
    - returns metadata for the extraction manifest.
    """
    file_path = RAW_DIR / file_name

    if not file_path.exists():
        logging.error("Missing expected raw file: %s", file_name)

        return {
            "file_name": file_name,
            "status": "missing_file",
            "raw_file_path": str(file_path),
            "output_file_path": "",
            "row_count": 0,
            "column_count": 0,
            "file_size_bytes": 0,
            "file_hash_sha256": "",
            "missing_columns": ",".join(expected_columns),
            "unexpected_columns": "",
            "error_message": "Expected raw file was not found.",
        }

    try:
        raw_df = read_csv_as_raw(file_path)
        schema_check = check_schema(
            file_name=file_name,
            actual_columns=list(raw_df.columns),
            expected_columns=expected_columns,
        )

        output_file_name = build_output_file_name(file_name)
        output_file_path = EXTRACT_DIR / output_file_name

        extracted_df = add_extraction_metadata(
            df=raw_df,
            source_file_name=file_name,
            batch_id=batch_id,
            extracted_at=extracted_at,
        )

        extracted_df.to_csv(output_file_path, index=False, encoding="utf-8")

        if schema_check["missing_columns"]:
            status = "schema_warning"
            logging.warning(
                "File %s extracted with missing columns: %s",
                file_name,
                schema_check["missing_columns"],
            )
        else:
            status = "success"
            logging.info("File %s extracted successfully.", file_name)

        return {
            "file_name": file_name,
            "status": status,
            "raw_file_path": str(file_path),
            "output_file_path": str(output_file_path),
            "row_count": len(raw_df),
            "column_count": len(raw_df.columns),
            "file_size_bytes": file_path.stat().st_size,
            "file_hash_sha256": calculate_file_hash(file_path),
            "missing_columns": ",".join(schema_check["missing_columns"]),
            "unexpected_columns": ",".join(schema_check["unexpected_columns"]),
            "error_message": "",
        }

    except Exception as error:
        logging.exception("Error while extracting file %s", file_name)

        return {
            "file_name": file_name,
            "status": "extraction_error",
            "raw_file_path": str(file_path),
            "output_file_path": "",
            "row_count": 0,
            "column_count": 0,
            "file_size_bytes": file_path.stat().st_size if file_path.exists() else 0,
            "file_hash_sha256": "",
            "missing_columns": "",
            "unexpected_columns": "",
            "error_message": str(error),
        }


def build_schema_report(
    file_name: str,
    expected_columns: List[str],
    actual_columns: List[str],
) -> List[Dict[str, object]]:
    """
    Build a schema report for one file.

    This report shows whether each expected column is present in the
    raw source file.
    """
    rows = []

    for position, column in enumerate(expected_columns, start=1):
        rows.append(
            {
                "file_name": file_name,
                "column_name": column,
                "expected_position": position,
                "is_expected": True,
                "is_present": column in actual_columns,
            }
        )

    unexpected_columns = [
        column for column in actual_columns if column not in expected_columns
    ]

    for column in unexpected_columns:
        rows.append(
            {
                "file_name": file_name,
                "column_name": column,
                "expected_position": "",
                "is_expected": False,
                "is_present": True,
            }
        )

    return rows


def build_reports(
    manifest_rows: List[Dict[str, object]],
    schema_rows: List[Dict[str, object]],
) -> None:
    """
    Save the extraction reports.

    Three reports are generated:
    - extraction manifest;
    - schema report;
    - error report.
    """
    manifest_df = pd.DataFrame(manifest_rows)
    schema_df = pd.DataFrame(schema_rows)

    error_df = manifest_df[
        manifest_df["status"].isin(
            ["missing_file", "schema_warning", "extraction_error"]
        )
    ].copy()

    manifest_df.to_csv(
        INTERIM_DIR / "file_extraction_manifest.csv",
        index=False,
        encoding="utf-8",
    )

    schema_df.to_csv(
        INTERIM_DIR / "file_extraction_schema_report.csv",
        index=False,
        encoding="utf-8",
    )

    error_df.to_csv(
        INTERIM_DIR / "file_extraction_errors.csv",
        index=False,
        encoding="utf-8",
    )


def collect_all_files() -> None:
    """
    Run the full file-based extraction process.

    This is the main orchestration function for local CSV extraction.
    """
    batch_id = get_current_batch_id()
    extracted_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    manifest_rows = []
    schema_rows = []

    logging.info("Starting file extraction batch: %s", batch_id)

    for file_name, expected_columns in EXPECTED_FILE_SCHEMAS.items():
        result = collect_one_file(
            file_name=file_name,
            expected_columns=expected_columns,
            batch_id=batch_id,
            extracted_at=extracted_at,
        )

        manifest_rows.append(result)

        file_path = RAW_DIR / file_name

        if file_path.exists():
            try:
                df = read_csv_as_raw(file_path)
                schema_rows.extend(
                    build_schema_report(
                        file_name=file_name,
                        expected_columns=expected_columns,
                        actual_columns=list(df.columns),
                    )
                )
            except Exception as error:
                logging.exception(
                    "Unable to build schema report for file %s: %s",
                    file_name,
                    error,
                )

    build_reports(manifest_rows, schema_rows)

    logging.info("File extraction batch completed: %s", batch_id)


def main() -> None:
    """
    Entry point of the script.

    It prepares the folders, configures logging, launches the extraction,
    and prints a short execution summary.
    """
    ensure_directories()
    setup_logging()
    collect_all_files()

    manifest_path = INTERIM_DIR / "file_extraction_manifest.csv"
    schema_path = INTERIM_DIR / "file_extraction_schema_report.csv"
    errors_path = INTERIM_DIR / "file_extraction_errors.csv"

    manifest_df = pd.read_csv(manifest_path)

    print("File-based data collection completed successfully.")
    print(f"Extracted files folder: {EXTRACT_DIR}")
    print(f"Manifest report: {manifest_path}")
    print(f"Schema report: {schema_path}")
    print(f"Error report: {errors_path}")
    print(f"Files processed: {len(manifest_df)}")
    print("Status summary:")
    print(manifest_df["status"].value_counts().to_string())


if __name__ == "__main__":
    main()