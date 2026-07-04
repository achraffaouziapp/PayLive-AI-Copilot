from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin
import hashlib
import logging
import re
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup


# -------------------------------------------------------------------
# Web scraping data collection
# -------------------------------------------------------------------
# This script collects product-like data from a public scraping sandbox.
#
# In the PayLive AI Copilot project, this scraping source is used to
# simulate the collection of product information from a web page.
#
# Important:
# This script does not clean the data.
# It only:
# - downloads HTML pages from a scraping practice website;
# - extracts product information from the HTML structure;
# - saves the raw HTML pages for traceability;
# - saves extracted records in data/interim/extracts/scraping;
# - saves reports in data/interim/reports/scraping_collection.
#
# Cleaning, normalization, deduplication, and business corrections will
# be done later in dedicated data processing scripts.
# -------------------------------------------------------------------


BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"
INTERIM_DIR = BASE_DIR / "data" / "interim"

INTERIM_EXTRACTS_DIR = INTERIM_DIR / "extracts"
INTERIM_REPORTS_DIR = INTERIM_DIR / "reports"

SCRAPING_HTML_DIR = RAW_DIR / "scraping_html"
SCRAPING_EXTRACT_DIR = INTERIM_EXTRACTS_DIR / "scraping"
SCRAPING_REPORTS_DIR = INTERIM_REPORTS_DIR / "scraping_collection"

LOG_DIR = BASE_DIR / "logs"

SOURCE_NAME = "books_to_scrape"
BASE_URL = "http://books.toscrape.com/"
CATALOGUE_PAGE_URL_TEMPLATE = "http://books.toscrape.com/catalogue/page-{page_number}.html"

# We limit the number of pages to keep the extraction reasonable
# and respectful of the target website.
MAX_PAGES_TO_SCRAPE = 3

REQUEST_TIMEOUT_SECONDS = 15
REQUEST_SLEEP_SECONDS = 0.7
MAX_RETRIES = 3

RAW_OUTPUT_CSV = RAW_DIR / "products_scraped_raw.csv"
EXTRACT_OUTPUT_CSV = SCRAPING_EXTRACT_DIR / "products_scraped_extract.csv"

SCRAPING_MANIFEST_REPORT_PATH = SCRAPING_REPORTS_DIR / "scraping_extraction_manifest.csv"
SCRAPING_SCHEMA_REPORT_PATH = SCRAPING_REPORTS_DIR / "scraping_extraction_schema_report.csv"
SCRAPING_PAGE_REPORT_PATH = SCRAPING_REPORTS_DIR / "scraping_extraction_page_report.csv"
SCRAPING_ERRORS_REPORT_PATH = SCRAPING_REPORTS_DIR / "scraping_extraction_errors.csv"

EXPECTED_SCRAPED_FIELDS = [
    "scraped_product_id",
    "product_name",
    "category",
    "brand",
    "description",
    "unit_price",
    "stock_quantity",
    "product_status",
    "source",
    "created_at",
    "source_product_url",
    "source_image_url",
    "price_raw",
    "availability_raw",
    "rating_raw",
    "upc_raw",
    "source_page_number",
]


def ensure_directories() -> None:
    """
    Create all folders required by the scraping extraction script.

    Raw HTML pages are saved in `data/raw/scraping_html`.
    Extracted tabular records are saved in `data/raw` and `data/interim/extracts/scraping`.
    Reports are saved in `data/interim/reports/scraping_collection`.
    Logs are saved in `logs`.
    """
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    SCRAPING_HTML_DIR.mkdir(parents=True, exist_ok=True)
    SCRAPING_EXTRACT_DIR.mkdir(parents=True, exist_ok=True)
    SCRAPING_REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def setup_logging() -> None:
    """
    Configure the logging system.

    The log file documents the execution of the scraping process.
    It is useful for traceability and debugging.
    """
    log_file = LOG_DIR / "collect_from_scraping.log"

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        encoding="utf-8",
    )


def get_current_batch_id() -> str:
    """
    Generate a unique extraction batch ID.

    The batch ID links all HTML pages, CSV outputs, and reports produced
    during the same scraping execution.
    """
    return datetime.now().strftime("SCRAPING_BATCH_%Y%m%d_%H%M%S")


def get_current_timestamp() -> str:
    """
    Return the current timestamp in a standard format.

    This timestamp is added to extracted records for traceability.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def calculate_text_hash(text: str) -> str:
    """
    Calculate a SHA256 hash from a text value.

    This is used to track the exact HTML content downloaded during
    the scraping process.
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def build_headers() -> Dict[str, str]:
    """
    Build HTTP headers for the scraping request.

    A clear User-Agent is used to identify the script as a student
    project data collection script.
    """
    return {
        "User-Agent": (
            "PayLiveAICopilotStudentProject/1.0 "
            "(educational scraping on public sandbox website)"
        )
    }


def fetch_url_with_retries(url: str) -> requests.Response:
    """
    Download a web page with a simple retry mechanism.

    Network calls can fail temporarily. This function retries the request
    before returning an error.

    The project uses the HTTP version of Books to Scrape to avoid SSL
    certificate issues that can happen on some Windows environments.
    """
    last_error: Optional[Exception] = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logging.info("Fetching URL attempt %s/%s: %s", attempt, MAX_RETRIES, url)

            response = requests.get(
                url,
                headers=build_headers(),
                timeout=REQUEST_TIMEOUT_SECONDS,
            )

            response.raise_for_status()

            logging.info("URL fetched successfully: %s", url)

            return response

        except requests.RequestException as error:
            last_error = error

            logging.warning(
                "URL fetch failed on attempt %s/%s for %s: %s",
                attempt,
                MAX_RETRIES,
                url,
                error,
            )

            if attempt < MAX_RETRIES:
                time.sleep(REQUEST_SLEEP_SECONDS)

    raise RuntimeError(
        f"Failed to fetch URL after {MAX_RETRIES} attempts: {url}. Error: {last_error}"
    )


def save_raw_html(html_text: str, file_name: str) -> Path:
    """
    Save raw HTML content for traceability.

    Keeping the raw HTML allows the extraction process to be audited later.
    """
    output_path = SCRAPING_HTML_DIR / file_name
    output_path.write_text(html_text, encoding="utf-8")
    return output_path


def parse_price_to_text(price_text: str) -> str:
    """
    Convert a displayed price into a raw numeric text value.

    This is still considered extraction formatting, not business cleaning.
    The final price validation and currency normalization will happen later.
    """
    if not price_text:
        return ""

    match = re.search(r"[\d]+(?:[.,]\d+)?", price_text)

    if not match:
        return ""

    return match.group(0).replace(",", ".")


def parse_stock_quantity_from_availability(availability_text: str) -> str:
    """
    Extract a stock quantity from an availability text when possible.

    Example:
    'In stock (22 available)' becomes '22'.

    If no quantity is available, the raw field is left empty.
    """
    if not availability_text:
        return ""

    match = re.search(r"(\d+)", availability_text)

    if not match:
        return ""

    return match.group(1)


def extract_rating_from_class(class_values: List[str]) -> str:
    """
    Extract the rating value from the HTML class list.

    Books to Scrape stores ratings as CSS classes such as:
    'star-rating Three'.
    """
    rating_values = {"One", "Two", "Three", "Four", "Five"}

    for class_value in class_values:
        if class_value in rating_values:
            return class_value

    return ""


def extract_text_or_empty(element: Optional[Any]) -> str:
    """
    Extract clean text from a BeautifulSoup element.

    If the element does not exist, return an empty string.
    """
    if element is None:
        return ""

    return element.get_text(strip=True)


def extract_product_cards_from_listing_page(
    html_text: str,
    page_number: int,
) -> List[Dict[str, str]]:
    """
    Extract product cards from a catalogue listing page.

    This function collects information visible on the listing page:
    title, price, availability, rating, detail URL, and image URL.
    """
    soup = BeautifulSoup(html_text, "html.parser")
    product_cards = soup.select("article.product_pod")

    products = []

    for card_index, card in enumerate(product_cards, start=1):
        title_link = card.select_one("h3 a")
        price_element = card.select_one(".price_color")
        availability_element = card.select_one(".availability")
        rating_element = card.select_one("p.star-rating")
        image_element = card.select_one("img")

        title = title_link.get("title", "").strip() if title_link else ""
        relative_product_url = title_link.get("href", "") if title_link else ""
        product_url = urljoin(CATALOGUE_PAGE_URL_TEMPLATE.format(page_number=page_number), relative_product_url)

        relative_image_url = image_element.get("src", "") if image_element else ""
        image_url = urljoin(CATALOGUE_PAGE_URL_TEMPLATE.format(page_number=page_number), relative_image_url)

        price_raw = extract_text_or_empty(price_element)
        availability_raw = extract_text_or_empty(availability_element)

        rating_raw = ""
        if rating_element is not None:
            rating_raw = extract_rating_from_class(rating_element.get("class", []))

        products.append(
            {
                "source_page_number": str(page_number),
                "source_card_index": str(card_index),
                "product_name": title,
                "source_product_url": product_url,
                "source_image_url": image_url,
                "price_raw": price_raw,
                "availability_raw": availability_raw,
                "rating_raw": rating_raw,
            }
        )

    return products


def extract_product_detail_page(product_url: str) -> Dict[str, str]:
    """
    Extract additional information from a product detail page.

    This function collects product category, UPC, description, and
    detailed availability when available.
    """
    response = fetch_url_with_retries(product_url)
    html_text = response.text

    html_hash = calculate_text_hash(html_text)
    safe_file_name = hashlib.sha256(product_url.encode("utf-8")).hexdigest()[:16]
    save_raw_html(html_text, f"detail_{safe_file_name}.html")

    soup = BeautifulSoup(html_text, "html.parser")

    breadcrumb_links = soup.select("ul.breadcrumb li a")
    category = ""

    if len(breadcrumb_links) >= 3:
        category = breadcrumb_links[-1].get_text(strip=True)

    description = ""
    description_header = soup.find(id="product_description")

    if description_header is not None:
        description_paragraph = description_header.find_next("p")
        description = extract_text_or_empty(description_paragraph)

    table_values = {}
    for row in soup.select("table.table.table-striped tr"):
        header = extract_text_or_empty(row.find("th"))
        value = extract_text_or_empty(row.find("td"))

        if header:
            table_values[header] = value

    return {
        "category": category,
        "description": description,
        "upc_raw": table_values.get("UPC", ""),
        "detail_availability_raw": table_values.get("Availability", ""),
        "detail_html_hash_sha256": html_hash,
    }


def build_scraped_product_row(
    listing_product: Dict[str, str],
    detail_product: Dict[str, str],
    batch_id: str,
    extracted_at: str,
    row_number: int,
) -> Dict[str, str]:
    """
    Build one product row from listing and detail page data.

    The output is shaped to be compatible with the project product model,
    while still keeping raw scraped fields for traceability.
    """
    availability_raw = (
        detail_product.get("detail_availability_raw")
        or listing_product.get("availability_raw", "")
    )

    product_status = availability_raw

    unit_price = parse_price_to_text(listing_product.get("price_raw", ""))
    stock_quantity = parse_stock_quantity_from_availability(availability_raw)

    return {
        "extraction_batch_id": batch_id,
        "source_system": SOURCE_NAME,
        "extracted_at": extracted_at,
        "scraped_product_id": f"SCRAPE_PROD_{str(row_number).zfill(4)}",
        "product_name": listing_product.get("product_name", ""),
        "category": detail_product.get("category", ""),
        "brand": "",
        "description": detail_product.get("description", ""),
        "unit_price": unit_price,
        "stock_quantity": stock_quantity,
        "product_status": product_status,
        "source": "scraping",
        "created_at": extracted_at,
        "source_product_url": listing_product.get("source_product_url", ""),
        "source_image_url": listing_product.get("source_image_url", ""),
        "price_raw": listing_product.get("price_raw", ""),
        "availability_raw": availability_raw,
        "rating_raw": listing_product.get("rating_raw", ""),
        "upc_raw": detail_product.get("upc_raw", ""),
        "source_page_number": listing_product.get("source_page_number", ""),
        "source_card_index": listing_product.get("source_card_index", ""),
        "detail_html_hash_sha256": detail_product.get("detail_html_hash_sha256", ""),
    }


def scrape_products(batch_id: str, extracted_at: str) -> Dict[str, Any]:
    """
    Run the full scraping extraction.

    The function downloads listing pages, extracts product cards,
    then visits each product detail page to enrich the extraction.
    """
    scraped_rows = []
    page_reports = []
    product_counter = 1

    for page_number in range(1, MAX_PAGES_TO_SCRAPE + 1):
        page_url = CATALOGUE_PAGE_URL_TEMPLATE.format(page_number=page_number)

        response = fetch_url_with_retries(page_url)
        html_text = response.text
        html_hash = calculate_text_hash(html_text)

        html_output_path = save_raw_html(
            html_text=html_text,
            file_name=f"listing_page_{page_number}.html",
        )

        listing_products = extract_product_cards_from_listing_page(
            html_text=html_text,
            page_number=page_number,
        )

        page_reports.append(
            {
                "extraction_batch_id": batch_id,
                "source_name": SOURCE_NAME,
                "page_number": page_number,
                "page_url": page_url,
                "status": "success",
                "http_status_code": response.status_code,
                "product_count": len(listing_products),
                "raw_html_path": str(html_output_path),
                "html_hash_sha256": html_hash,
                "error_message": "",
            }
        )

        for listing_product in listing_products:
            try:
                detail_product = extract_product_detail_page(
                    listing_product["source_product_url"]
                )

                product_row = build_scraped_product_row(
                    listing_product=listing_product,
                    detail_product=detail_product,
                    batch_id=batch_id,
                    extracted_at=extracted_at,
                    row_number=product_counter,
                )

                scraped_rows.append(product_row)
                product_counter += 1

                time.sleep(REQUEST_SLEEP_SECONDS)

            except Exception as error:
                logging.exception(
                    "Failed to extract product detail page: %s",
                    listing_product.get("source_product_url", ""),
                )

                product_row = build_scraped_product_row(
                    listing_product=listing_product,
                    detail_product={},
                    batch_id=batch_id,
                    extracted_at=extracted_at,
                    row_number=product_counter,
                )

                product_row["detail_extraction_error"] = str(error)
                scraped_rows.append(product_row)
                product_counter += 1

        time.sleep(REQUEST_SLEEP_SECONDS)

    return {
        "scraped_rows": scraped_rows,
        "page_reports": page_reports,
    }


def build_schema_report(scraped_df: pd.DataFrame) -> pd.DataFrame:
    """
    Build a schema report for the scraped product extraction.

    The report checks whether each expected field is present in the
    extracted dataset.
    """
    rows = []

    actual_columns = set(scraped_df.columns)

    for position, field_name in enumerate(EXPECTED_SCRAPED_FIELDS, start=1):
        rows.append(
            {
                "source_name": SOURCE_NAME,
                "field_name": field_name,
                "expected_position": position,
                "is_expected": True,
                "is_present": field_name in actual_columns,
            }
        )

    unexpected_columns = [
        column for column in scraped_df.columns
        if column not in EXPECTED_SCRAPED_FIELDS
        and column not in {"extraction_batch_id", "source_system", "extracted_at"}
    ]

    for column in unexpected_columns:
        rows.append(
            {
                "source_name": SOURCE_NAME,
                "field_name": column,
                "expected_position": "",
                "is_expected": False,
                "is_present": True,
            }
        )

    return pd.DataFrame(rows)


def build_manifest_report(
    batch_id: str,
    extracted_at: str,
    status: str,
    product_count: int,
    page_count: int,
    error_message: str = "",
) -> pd.DataFrame:
    """
    Build the scraping extraction manifest.

    The manifest summarizes the extraction execution.
    """
    return pd.DataFrame(
        [
            {
                "extraction_batch_id": batch_id,
                "source_name": SOURCE_NAME,
                "source_type": "web_scraping",
                "base_url": BASE_URL,
                "max_pages_requested": MAX_PAGES_TO_SCRAPE,
                "pages_scraped": page_count,
                "products_extracted": product_count,
                "extracted_at": extracted_at,
                "status": status,
                "raw_output_csv": str(RAW_OUTPUT_CSV),
                "extract_output_csv": str(EXTRACT_OUTPUT_CSV),
                "raw_html_folder": str(SCRAPING_HTML_DIR),
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
    Build an error report when the scraping extraction fails.

    This keeps extraction failures documented instead of silent.
    """
    return pd.DataFrame(
        [
            {
                "extraction_batch_id": batch_id,
                "source_name": SOURCE_NAME,
                "base_url": BASE_URL,
                "extracted_at": extracted_at,
                "error_message": error_message,
            }
        ]
    )


def save_scraping_outputs(
    scraped_df: pd.DataFrame,
    manifest_df: pd.DataFrame,
    schema_df: pd.DataFrame,
    page_report_df: pd.DataFrame,
    error_df: pd.DataFrame,
) -> None:
    """
    Save scraped data and scraping reports.

    The raw scraped CSV is saved in `data/raw`.
    The extraction copy is saved in `data/interim/extracts/scraping`.
    The reports are saved in `data/interim/reports/scraping_collection`.
    """
    scraped_df.to_csv(RAW_OUTPUT_CSV, index=False, encoding="utf-8")
    scraped_df.to_csv(EXTRACT_OUTPUT_CSV, index=False, encoding="utf-8")

    manifest_df.to_csv(
        SCRAPING_MANIFEST_REPORT_PATH,
        index=False,
        encoding="utf-8",
    )

    schema_df.to_csv(
        SCRAPING_SCHEMA_REPORT_PATH,
        index=False,
        encoding="utf-8",
    )

    page_report_df.to_csv(
        SCRAPING_PAGE_REPORT_PATH,
        index=False,
        encoding="utf-8",
    )

    error_df.to_csv(
        SCRAPING_ERRORS_REPORT_PATH,
        index=False,
        encoding="utf-8",
    )


def collect_products_from_scraping() -> None:
    """
    Run the complete scraping collection process.

    This function:
    - downloads product listing pages;
    - saves raw HTML;
    - extracts product information;
    - saves CSV outputs;
    - generates manifest, schema, page, and error reports.
    """
    batch_id = get_current_batch_id()
    extracted_at = get_current_timestamp()

    logging.info("Starting scraping extraction batch: %s", batch_id)

    try:
        scraping_result = scrape_products(
            batch_id=batch_id,
            extracted_at=extracted_at,
        )

        scraped_rows = scraping_result["scraped_rows"]
        page_reports = scraping_result["page_reports"]

        scraped_df = pd.DataFrame(scraped_rows)

        manifest_df = build_manifest_report(
            batch_id=batch_id,
            extracted_at=extracted_at,
            status="success",
            product_count=len(scraped_df),
            page_count=len(page_reports),
            error_message="",
        )

        schema_df = build_schema_report(scraped_df)
        page_report_df = pd.DataFrame(page_reports)

        error_df = pd.DataFrame(
            columns=[
                "extraction_batch_id",
                "source_name",
                "base_url",
                "extracted_at",
                "error_message",
            ]
        )

        save_scraping_outputs(
            scraped_df=scraped_df,
            manifest_df=manifest_df,
            schema_df=schema_df,
            page_report_df=page_report_df,
            error_df=error_df,
        )

        logging.info("Scraping extraction batch completed successfully: %s", batch_id)

    except Exception as error:
        error_message = str(error)

        logging.exception("Scraping extraction batch failed: %s", batch_id)

        scraped_df = pd.DataFrame(columns=EXPECTED_SCRAPED_FIELDS)

        manifest_df = build_manifest_report(
            batch_id=batch_id,
            extracted_at=extracted_at,
            status="extraction_error",
            product_count=0,
            page_count=0,
            error_message=error_message,
        )

        schema_df = build_schema_report(scraped_df)
        page_report_df = pd.DataFrame(
            columns=[
                "extraction_batch_id",
                "source_name",
                "page_number",
                "page_url",
                "status",
                "http_status_code",
                "product_count",
                "raw_html_path",
                "html_hash_sha256",
                "error_message",
            ]
        )

        error_df = build_error_report(
            batch_id=batch_id,
            extracted_at=extracted_at,
            error_message=error_message,
        )

        save_scraping_outputs(
            scraped_df=scraped_df,
            manifest_df=manifest_df,
            schema_df=schema_df,
            page_report_df=page_report_df,
            error_df=error_df,
        )

        raise


def main() -> None:
    """
    Entry point of the script.

    It prepares folders, configures logging, runs the scraping extraction,
    and prints a short execution summary.
    """
    ensure_directories()
    setup_logging()
    collect_products_from_scraping()

    manifest_df = pd.read_csv(SCRAPING_MANIFEST_REPORT_PATH)

    print("Web scraping data collection completed successfully.")
    print(f"Raw scraped CSV: {RAW_OUTPUT_CSV}")
    print(f"Scraping extract CSV: {EXTRACT_OUTPUT_CSV}")
    print(f"Raw HTML folder: {SCRAPING_HTML_DIR}")
    print(f"Manifest report: {SCRAPING_MANIFEST_REPORT_PATH}")
    print(f"Schema report: {SCRAPING_SCHEMA_REPORT_PATH}")
    print(f"Page report: {SCRAPING_PAGE_REPORT_PATH}")
    print(f"Error report: {SCRAPING_ERRORS_REPORT_PATH}")
    print("Status summary:")
    print(manifest_df["status"].value_counts().to_string())


if __name__ == "__main__":
    main()