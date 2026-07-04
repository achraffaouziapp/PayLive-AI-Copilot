from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import hashlib
import json
import logging
import time

import pandas as pd
import requests


# -------------------------------------------------------------------
# API-based data collection
# -------------------------------------------------------------------
# This script collects product data from an external REST API.
#
# In the PayLive AI Copilot project, this API source is used to simulate
# an external product catalog that could be connected to a live shopping
# platform.
#
# Important:
# This script does not clean the data.
# It only:
# - calls the external API;
# - checks the HTTP response;
# - saves the raw JSON response;
# - extracts product records into a tabular format;
# - adds extraction metadata;
# - saves extracts in data/interim/extracts/api;
# - saves reports in data/interim/reports/api_collection.
#
# Cleaning, normalization, deduplication, and business corrections will
# be done later in dedicated data processing scripts.
# -------------------------------------------------------------------


BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"
INTERIM_DIR = BASE_DIR / "data" / "interim"

INTERIM_EXTRACTS_DIR = INTERIM_DIR / "extracts"
INTERIM_REPORTS_DIR = INTERIM_DIR / "reports"

API_EXTRACT_DIR = INTERIM_EXTRACTS_DIR / "api"
API_REPORTS_DIR = INTERIM_REPORTS_DIR / "api_collection"

LOG_DIR = BASE_DIR / "logs"

API_SOURCE_NAME = "dummyjson_products_api"
API_URL = "https://dummyjson.com/products"
API_LIMIT = 100
API_TIMEOUT_SECONDS = 15
MAX_RETRIES = 3
RETRY_SLEEP_SECONDS = 2

RAW_JSON_OUTPUT = RAW_DIR / "products_api_raw.json"
API_EXTRACT_OUTPUT = API_EXTRACT_DIR / "products_api_extract.csv"

API_MANIFEST_REPORT_PATH = API_REPORTS_DIR / "api_extraction_manifest.csv"
API_SCHEMA_REPORT_PATH = API_REPORTS_DIR / "api_extraction_schema_report.csv"
API_ERRORS_REPORT_PATH = API_REPORTS_DIR / "api_extraction_errors.csv"

EXPECTED_API_PRODUCT_FIELDS = [
    "id",
    "title",
    "description",
    "category",
    "price",
    "discountPercentage",
    "rating",
    "stock",
    "brand",
    "sku",
    "weight",
    "warrantyInformation",
    "shippingInformation",
    "availabilityStatus",
    "returnPolicy",
    "minimumOrderQuantity",
    "thumbnail",
    "images",
]


def ensure_directories() -> None:
    """
    Create all folders required by the API extraction script.

    The raw JSON response is saved in `data/raw`.
    The extracted tabular data is saved in `data/interim/extracts/api`.
    Reports are saved in `data/interim/reports/api_collection`.
    The execution log is saved in `logs`.
    """
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    API_EXTRACT_DIR.mkdir(parents=True, exist_ok=True)
    API_REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def setup_logging() -> None:
    """
    Configure the logging system.

    Logs are useful to prove that the API extraction was executed
    and to debug connection or response issues.
    """
    log_file = LOG_DIR / "collect_from_api.log"

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        encoding="utf-8",
    )


def get_current_batch_id() -> str:
    """
    Generate a unique extraction batch ID.

    A batch ID links the raw JSON file, the extracted CSV file,
    and the extraction reports produced during the same run.
    """
    return datetime.now().strftime("API_BATCH_%Y%m%d_%H%M%S")


def get_current_timestamp() -> str:
    """
    Return the current timestamp in a standard format.

    This timestamp is added to extracted records for traceability.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def calculate_text_hash(text: str) -> str:
    """
    Calculate a SHA256 hash from a text value.

    This is used to create a traceability hash for the raw API response.
    If the response content changes, the hash will also change.
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def build_api_params() -> Dict[str, Any]:
    """
    Build query parameters for the API call.

    The `limit` parameter controls how many product records are returned.
    """
    return {
        "limit": API_LIMIT,
    }


def call_api_with_retries(
    url: str,
    params: Dict[str, Any],
    timeout_seconds: int,
    max_retries: int,
) -> requests.Response:
    """
    Call the external API with a simple retry mechanism.

    Network calls can fail temporarily.
    This function retries the request before raising the last exception.
    """
    last_error: Optional[Exception] = None

    for attempt in range(1, max_retries + 1):
        try:
            logging.info(
                "Calling API attempt %s/%s: %s",
                attempt,
                max_retries,
                url,
            )

            response = requests.get(
                url,
                params=params,
                timeout=timeout_seconds,
            )

            response.raise_for_status()

            logging.info(
                "API call succeeded with status code %s.",
                response.status_code,
            )

            return response

        except requests.RequestException as error:
            last_error = error

            logging.warning(
                "API call failed on attempt %s/%s: %s",
                attempt,
                max_retries,
                error,
            )

            if attempt < max_retries:
                time.sleep(RETRY_SLEEP_SECONDS)

    raise RuntimeError(f"API call failed after {max_retries} attempts: {last_error}")


def save_raw_json_response(response_json: Dict[str, Any]) -> str:
    """
    Save the complete raw API response as JSON.

    This file is kept as the original API extraction result.
    It must not be manually modified later.
    """
    raw_text = json.dumps(response_json, ensure_ascii=False, indent=2)

    RAW_JSON_OUTPUT.write_text(raw_text, encoding="utf-8")

    return raw_text


def get_products_from_response(response_json: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extract the product list from the API JSON response.

    DummyJSON returns products inside the `products` key.
    If the key is missing, the function returns an empty list.
    """
    products = response_json.get("products", [])

    if not isinstance(products, list):
        logging.warning("The API response key `products` is not a list.")
        return []

    return products


def serialize_complex_value(value: Any) -> Any:
    """
    Convert complex values into JSON strings for CSV export.

    Some API fields can contain lists or dictionaries, for example images.
    CSV files cannot store nested structures directly, so we serialize them.
    """
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False)

    return value


def build_product_extract_dataframe(
    products: List[Dict[str, Any]],
    batch_id: str,
    extracted_at: str,
) -> pd.DataFrame:
    """
    Convert API product records into a tabular DataFrame.

    This step is an extraction formatting step, not a cleaning step.
    The original API field names are preserved.
    """
    rows = []

    for product in products:
        row = {
            "extraction_batch_id": batch_id,
            "source_system": API_SOURCE_NAME,
            "source_url": API_URL,
            "extracted_at": extracted_at,
        }

        for field in EXPECTED_API_PRODUCT_FIELDS:
            row[field] = serialize_complex_value(product.get(field, ""))

        rows.append(row)

    return pd.DataFrame(rows)


def save_product_extract(df: pd.DataFrame) -> None:
    """
    Save the API product extraction as a CSV file.

    The output is stored in `data/interim/extracts/api`.
    """
    df.to_csv(API_EXTRACT_OUTPUT, index=False, encoding="utf-8")


def check_api_schema(products: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Check whether expected API product fields are present.

    This report helps document the structure of the API response.
    """
    if not products:
        return pd.DataFrame(
            [
                {
                    "source_name": API_SOURCE_NAME,
                    "field_name": field,
                    "is_expected": True,
                    "is_present": False,
                    "presence_rate_percent": 0,
                }
                for field in EXPECTED_API_PRODUCT_FIELDS
            ]
        )

    rows = []
    total_products = len(products)

    for field in EXPECTED_API_PRODUCT_FIELDS:
        present_count = sum(1 for product in products if field in product)
        presence_rate = round((present_count / total_products) * 100, 2)

        rows.append(
            {
                "source_name": API_SOURCE_NAME,
                "field_name": field,
                "is_expected": True,
                "is_present": present_count > 0,
                "presence_rate_percent": presence_rate,
            }
        )

    observed_fields = sorted(
        {
            field
            for product in products
            for field in product.keys()
        }
    )

    unexpected_fields = [
        field for field in observed_fields if field not in EXPECTED_API_PRODUCT_FIELDS
    ]

    for field in unexpected_fields:
        present_count = sum(1 for product in products if field in product)
        presence_rate = round((present_count / total_products) * 100, 2)

        rows.append(
            {
                "source_name": API_SOURCE_NAME,
                "field_name": field,
                "is_expected": False,
                "is_present": True,
                "presence_rate_percent": presence_rate,
            }
        )

    return pd.DataFrame(rows)


def build_manifest_report(
    batch_id: str,
    extracted_at: str,
    status: str,
    response_status_code: Optional[int],
    product_count: int,
    raw_response_hash: str,
    error_message: str = "",
) -> pd.DataFrame:
    """
    Build the API extraction manifest.

    The manifest gives a high-level summary of the extraction run.
    It is useful for traceability and final documentation.
    """
    return pd.DataFrame(
        [
            {
                "extraction_batch_id": batch_id,
                "source_name": API_SOURCE_NAME,
                "source_type": "REST API",
                "source_url": API_URL,
                "query_params": json.dumps(build_api_params(), ensure_ascii=False),
                "extracted_at": extracted_at,
                "status": status,
                "response_status_code": response_status_code,
                "product_count": product_count,
                "raw_output_path": str(RAW_JSON_OUTPUT),
                "extract_output_path": str(API_EXTRACT_OUTPUT),
                "raw_response_hash_sha256": raw_response_hash,
                "error_message": error_message,
            }
        ]
    )


def build_error_report(
    batch_id: str,
    extracted_at: str,
    error_message: str,
) -> pd.DataFrame:
    """
    Build an error report when the API extraction fails.

    This makes the failure explicit and documented instead of silent.
    """
    return pd.DataFrame(
        [
            {
                "extraction_batch_id": batch_id,
                "source_name": API_SOURCE_NAME,
                "source_url": API_URL,
                "extracted_at": extracted_at,
                "error_message": error_message,
            }
        ]
    )


def save_reports(
    manifest_df: pd.DataFrame,
    schema_df: pd.DataFrame,
    error_df: pd.DataFrame,
) -> None:
    """
    Save all API extraction reports.

    Reports are saved in `data/interim/reports/api_collection`.
    """
    manifest_df.to_csv(
        API_MANIFEST_REPORT_PATH,
        index=False,
        encoding="utf-8",
    )

    schema_df.to_csv(
        API_SCHEMA_REPORT_PATH,
        index=False,
        encoding="utf-8",
    )

    error_df.to_csv(
        API_ERRORS_REPORT_PATH,
        index=False,
        encoding="utf-8",
    )


def collect_products_from_api() -> None:
    """
    Run the full API extraction process.

    This function:
    - calls the external REST API;
    - saves the raw JSON response;
    - extracts product records into CSV;
    - generates a manifest report;
    - generates a schema report;
    - generates an error report if needed.
    """
    batch_id = get_current_batch_id()
    extracted_at = get_current_timestamp()

    logging.info("Starting API extraction batch: %s", batch_id)

    try:
        response = call_api_with_retries(
            url=API_URL,
            params=build_api_params(),
            timeout_seconds=API_TIMEOUT_SECONDS,
            max_retries=MAX_RETRIES,
        )

        response_json = response.json()
        raw_text = save_raw_json_response(response_json)
        raw_response_hash = calculate_text_hash(raw_text)

        products = get_products_from_response(response_json)
        product_extract_df = build_product_extract_dataframe(
            products=products,
            batch_id=batch_id,
            extracted_at=extracted_at,
        )

        save_product_extract(product_extract_df)

        schema_df = check_api_schema(products)

        manifest_df = build_manifest_report(
            batch_id=batch_id,
            extracted_at=extracted_at,
            status="success",
            response_status_code=response.status_code,
            product_count=len(products),
            raw_response_hash=raw_response_hash,
            error_message="",
        )

        error_df = pd.DataFrame(
            columns=[
                "extraction_batch_id",
                "source_name",
                "source_url",
                "extracted_at",
                "error_message",
            ]
        )

        save_reports(
            manifest_df=manifest_df,
            schema_df=schema_df,
            error_df=error_df,
        )

        logging.info(
            "API extraction batch completed successfully: %s",
            batch_id,
        )

    except Exception as error:
        error_message = str(error)

        logging.exception(
            "API extraction batch failed: %s",
            batch_id,
        )

        manifest_df = build_manifest_report(
            batch_id=batch_id,
            extracted_at=extracted_at,
            status="extraction_error",
            response_status_code=None,
            product_count=0,
            raw_response_hash="",
            error_message=error_message,
        )

        schema_df = check_api_schema([])

        error_df = build_error_report(
            batch_id=batch_id,
            extracted_at=extracted_at,
            error_message=error_message,
        )

        save_reports(
            manifest_df=manifest_df,
            schema_df=schema_df,
            error_df=error_df,
        )

        raise


def main() -> None:
    """
    Entry point of the script.

    It prepares folders, configures logging, runs the API extraction,
    and prints a short execution summary.
    """
    ensure_directories()
    setup_logging()
    collect_products_from_api()

    manifest_df = pd.read_csv(API_MANIFEST_REPORT_PATH)

    print("API-based data collection completed successfully.")
    print(f"Raw JSON output: {RAW_JSON_OUTPUT}")
    print(f"API extract output: {API_EXTRACT_OUTPUT}")
    print(f"Manifest report: {API_MANIFEST_REPORT_PATH}")
    print(f"Schema report: {API_SCHEMA_REPORT_PATH}")
    print(f"Error report: {API_ERRORS_REPORT_PATH}")
    print("Status summary:")
    print(manifest_df["status"].value_counts().to_string())


if __name__ == "__main__":
    main()