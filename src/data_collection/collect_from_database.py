from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import hashlib
import logging
import sqlite3

import pandas as pd


# -------------------------------------------------------------------
# Database-based data collection
# -------------------------------------------------------------------
# This script simulates a legacy SQL database and extracts data from it.
#
# In the PayLive AI Copilot project, we do not have access to a real
# company database. For this reason, we create a local SQLite database
# called `paylive_legacy.db`.
#
# The database represents an old transactional system containing sellers,
# live sessions, carts, orders, and payments.
#
# Important:
# This script does not clean the data.
# It only:
# - creates a simulated legacy database;
# - imports selected raw CSV files into SQL tables;
# - executes documented SQL extraction queries;
# - saves query results as CSV files;
# - generates manifest, schema, query, and error reports.
#
# Cleaning, normalization, deduplication, and business corrections will
# be done later in dedicated data processing scripts.
# -------------------------------------------------------------------


BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"
INTERIM_DIR = BASE_DIR / "data" / "interim"
INTERIM_EXTRACTS_DIR = INTERIM_DIR / "extracts"
INTERIM_REPORTS_DIR = INTERIM_DIR / "reports"

DATABASE_EXTRACT_DIR = INTERIM_EXTRACTS_DIR / "database"
DATABASE_COLLECTION_REPORTS_DIR = INTERIM_REPORTS_DIR / "database_collection"

LEGACY_DATABASE_DIR = RAW_DIR / "legacy_database"
LOG_DIR = BASE_DIR / "logs"
SQL_DIR = BASE_DIR / "sql"

LEGACY_DATABASE_PATH = LEGACY_DATABASE_DIR / "paylive_legacy.db"
SQL_QUERIES_OUTPUT = SQL_DIR / "04_extraction_queries.sql"

SOURCE_NAME = "paylive_legacy_sqlite_database"


# These raw files will be imported into the simulated legacy database.
# The table names are prefixed with `legacy_` to make it clear that
# they represent a source system, not the final cleaned database.
LEGACY_TABLE_SOURCES = {
    "legacy_sellers": "sellers_raw.csv",
    "legacy_customers": "customers_raw.csv",
    "legacy_live_sessions": "live_sessions_raw.csv",
    "legacy_carts": "carts_raw.csv",
    "legacy_orders": "orders_raw.csv",
    "legacy_payments": "payments_raw.csv",
}


# SQL extraction queries used to demonstrate extraction from a database.
# The queries include selections, joins, filters, and aggregations.
SQL_EXTRACTION_QUERIES = {
    "legacy_sellers": """
        SELECT
            seller_id,
            shop_name,
            owner_first_name,
            owner_last_name,
            email,
            country,
            main_platform,
            created_at,
            seller_status
        FROM legacy_sellers;
    """,
    "legacy_live_sessions": """
        SELECT
            live_id,
            seller_id,
            platform,
            live_title,
            actual_start_at,
            ended_at,
            live_status,
            peak_viewers,
            currency
        FROM legacy_live_sessions;
    """,
    "paid_orders_with_payments": """
        SELECT
            o.order_id,
            o.cart_id,
            o.customer_id,
            o.seller_id,
            s.shop_name,
            c.live_id,
            l.platform AS live_platform,
            o.order_status,
            CAST(NULLIF(o.order_amount, '') AS REAL) AS order_amount,
            o.currency AS order_currency,
            p.payment_id,
            p.payment_provider,
            p.payment_status,
            CAST(NULLIF(p.payment_amount, '') AS REAL) AS payment_amount,
            p.currency AS payment_currency,
            p.payment_method,
            p.paid_at,
            p.transaction_reference
        FROM legacy_orders AS o
        LEFT JOIN legacy_payments AS p
            ON o.order_id = p.order_id
        LEFT JOIN legacy_carts AS c
            ON o.cart_id = c.cart_id
        LEFT JOIN legacy_live_sessions AS l
            ON c.live_id = l.live_id
        LEFT JOIN legacy_sellers AS s
            ON o.seller_id = s.seller_id
        WHERE p.payment_status IN ('succeeded', 'success', 'ok');
    """,
    "revenue_by_live": """
        SELECT
            c.live_id,
            l.seller_id,
            s.shop_name,
            l.platform AS live_platform,
            COUNT(DISTINCT o.order_id) AS total_orders,
            COUNT(DISTINCT p.payment_id) AS total_payments,
            COUNT(
                DISTINCT CASE
                    WHEN p.payment_status IN ('succeeded', 'success', 'ok')
                    THEN p.payment_id
                END
            ) AS successful_payments,
            ROUND(
                SUM(
                    CASE
                        WHEN p.payment_status IN ('succeeded', 'success', 'ok')
                        THEN CAST(NULLIF(p.payment_amount, '') AS REAL)
                        ELSE 0
                    END
                ),
                2
            ) AS gross_revenue
        FROM legacy_orders AS o
        LEFT JOIN legacy_payments AS p
            ON o.order_id = p.order_id
        LEFT JOIN legacy_carts AS c
            ON o.cart_id = c.cart_id
        LEFT JOIN legacy_live_sessions AS l
            ON c.live_id = l.live_id
        LEFT JOIN legacy_sellers AS s
            ON l.seller_id = s.seller_id
        GROUP BY
            c.live_id,
            l.seller_id,
            s.shop_name,
            l.platform;
    """,
    "incomplete_orders": """
        SELECT
            o.order_id,
            o.cart_id,
            o.customer_id,
            o.seller_id,
            o.order_status,
            o.order_amount,
            o.currency,
            o.created_at,
            p.payment_id,
            p.payment_status,
            p.payment_amount,
            CASE
                WHEN o.cart_id IS NULL OR TRIM(o.cart_id) = ''
                    THEN 'missing_cart_id'
                WHEN o.customer_id IS NULL OR TRIM(o.customer_id) = ''
                    THEN 'missing_customer_id'
                WHEN o.seller_id IS NULL OR TRIM(o.seller_id) = ''
                    THEN 'missing_seller_id'
                WHEN p.payment_id IS NULL
                    THEN 'missing_payment'
                WHEN CAST(NULLIF(o.order_amount, '') AS REAL) < 0
                    THEN 'negative_order_amount'
                ELSE 'other_issue'
            END AS issue_reason
        FROM legacy_orders AS o
        LEFT JOIN legacy_payments AS p
            ON o.order_id = p.order_id
        WHERE
            o.cart_id IS NULL
            OR TRIM(o.cart_id) = ''
            OR o.customer_id IS NULL
            OR TRIM(o.customer_id) = ''
            OR o.seller_id IS NULL
            OR TRIM(o.seller_id) = ''
            OR p.payment_id IS NULL
            OR CAST(NULLIF(o.order_amount, '') AS REAL) < 0;
    """,
}


def ensure_directories() -> None:
    """
    Create all folders required by the database extraction script.

    The simulated legacy database is saved in `data/raw/legacy_database`.
    Extracted query results are saved in `data/interim/extracts/database`.
    SQL query documentation is saved in `sql`.
    Execution logs are saved in `logs`.
    """
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    INTERIM_EXTRACTS_DIR.mkdir(parents=True, exist_ok=True)
    INTERIM_REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    DATABASE_EXTRACT_DIR.mkdir(parents=True, exist_ok=True)
    DATABASE_COLLECTION_REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    LEGACY_DATABASE_DIR.mkdir(parents=True, exist_ok=True)
    SQL_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def setup_logging() -> None:
    """
    Configure the logging system.

    Logs prove that the database extraction was executed and help debug
    problems related to database creation, imports, or SQL queries.
    """
    log_file = LOG_DIR / "collect_from_database.log"

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        encoding="utf-8",
    )


def get_current_batch_id() -> str:
    """
    Generate a unique extraction batch ID.

    This ID links the database file, SQL queries, extracted CSV files,
    and reports produced during the same execution.
    """
    return datetime.now().strftime("DB_BATCH_%Y%m%d_%H%M%S")


def get_current_timestamp() -> str:
    """
    Return the current timestamp in a standard format.

    This timestamp is written in the manifest and extraction reports.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def calculate_file_hash(file_path: Path) -> str:
    """
    Calculate the SHA256 hash of a file.

    The hash is used for traceability. If the database file changes,
    the hash will also change.
    """
    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        for block in iter(lambda: file.read(4096), b""):
            sha256.update(block)

    return sha256.hexdigest()


def calculate_text_hash(text: str) -> str:
    """
    Calculate a SHA256 hash from a text value.

    This is used to track the exact SQL query executed.
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_raw_csv(file_name: str) -> pd.DataFrame:
    """
    Read a raw CSV file as strings.

    All values are loaded as strings because raw data can contain mixed
    values such as invalid dates, invalid numbers, or empty fields.
    """
    file_path = RAW_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(
            f"Required raw file not found: {file_path}. "
            "Run the raw data generation step before this script."
        )

    return pd.read_csv(
        file_path,
        dtype=str,
        keep_default_na=False,
        encoding="utf-8",
    )


def reset_legacy_database() -> None:
    """
    Delete the previous simulated legacy database if it exists.

    This keeps the extraction reproducible by creating a fresh database
    at every execution.
    """
    if LEGACY_DATABASE_PATH.exists():
        LEGACY_DATABASE_PATH.unlink()


def connect_to_legacy_database() -> sqlite3.Connection:
    """
    Open a connection to the simulated legacy SQLite database.
    """
    return sqlite3.connect(LEGACY_DATABASE_PATH)


def import_raw_files_to_legacy_database(connection: sqlite3.Connection) -> pd.DataFrame:
    """
    Import selected raw CSV files into SQL tables.

    Each imported file becomes a `legacy_*` table inside the SQLite
    database. This simulates a real source database extraction scenario.
    """
    import_rows = []

    for table_name, raw_file_name in LEGACY_TABLE_SOURCES.items():
        df = read_raw_csv(raw_file_name)

        df.to_sql(
            name=table_name,
            con=connection,
            if_exists="replace",
            index=False,
        )

        import_rows.append(
            {
                "table_name": table_name,
                "source_file_name": raw_file_name,
                "row_count": len(df),
                "column_count": len(df.columns),
                "status": "imported",
            }
        )

        logging.info(
            "Imported raw file %s into table %s with %s rows.",
            raw_file_name,
            table_name,
            len(df),
        )

    return pd.DataFrame(import_rows)


def write_sql_queries_to_file() -> None:
    """
    Save all SQL extraction queries in a dedicated SQL file.

    This file is a technical deliverable and can be included in the
    final report to document filters, joins, and aggregations.
    """
    lines = [
        "-- SQL extraction queries for PayLive AI Copilot",
        "-- Source: simulated legacy SQLite database",
        "-- This file is generated by src/data_collection/collect_from_database.py",
        "",
    ]

    for query_name, query in SQL_EXTRACTION_QUERIES.items():
        lines.append(f"-- ============================================================")
        lines.append(f"-- Query name: {query_name}")
        lines.append(f"-- Purpose: Extract data from the simulated legacy SQL database.")
        lines.append(f"-- ============================================================")
        lines.append(query.strip())
        lines.append(";")
        lines.append("")

    SQL_QUERIES_OUTPUT.write_text("\n".join(lines), encoding="utf-8")


def build_output_file_name(query_name: str) -> str:
    """
    Build the CSV output file name for one SQL query result.
    """
    return f"{query_name}_extract.csv"


def execute_one_query(
    connection: sqlite3.Connection,
    query_name: str,
    query: str,
    batch_id: str,
    extracted_at: str,
) -> Dict[str, object]:
    """
    Execute one SQL query and save the result as a CSV file.

    Extraction metadata columns are added to the result for traceability.
    """
    output_file_path = DATABASE_EXTRACT_DIR / build_output_file_name(query_name)

    try:
        result_df = pd.read_sql_query(query, connection)

        result_df.insert(0, "extraction_batch_id", batch_id)
        result_df.insert(1, "source_system", SOURCE_NAME)
        result_df.insert(2, "query_name", query_name)
        result_df.insert(3, "extracted_at", extracted_at)

        result_df.to_csv(output_file_path, index=False, encoding="utf-8")

        logging.info(
            "SQL query %s executed successfully with %s rows.",
            query_name,
            len(result_df),
        )

        return {
            "query_name": query_name,
            "status": "success",
            "row_count": len(result_df),
            "column_count": len(result_df.columns),
            "output_file_path": str(output_file_path),
            "query_hash_sha256": calculate_text_hash(query),
            "error_message": "",
        }

    except Exception as error:
        logging.exception("SQL query %s failed.", query_name)

        return {
            "query_name": query_name,
            "status": "query_error",
            "row_count": 0,
            "column_count": 0,
            "output_file_path": "",
            "query_hash_sha256": calculate_text_hash(query),
            "error_message": str(error),
        }


def execute_extraction_queries(
    connection: sqlite3.Connection,
    batch_id: str,
    extracted_at: str,
) -> pd.DataFrame:
    """
    Execute all SQL extraction queries.

    Each query result is saved as a separate CSV file.
    """
    query_report_rows = []

    for query_name, query in SQL_EXTRACTION_QUERIES.items():
        result = execute_one_query(
            connection=connection,
            query_name=query_name,
            query=query,
            batch_id=batch_id,
            extracted_at=extracted_at,
        )

        query_report_rows.append(result)

    return pd.DataFrame(query_report_rows)


def get_database_tables(connection: sqlite3.Connection) -> List[str]:
    """
    Return the list of tables available in the SQLite database.
    """
    table_df = pd.read_sql_query(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name;
        """,
        connection,
    )

    return table_df["name"].tolist()


def build_schema_report(connection: sqlite3.Connection) -> pd.DataFrame:
    """
    Build a schema report from the simulated legacy database.

    This report lists the tables and columns imported into SQLite.
    """
    rows = []

    for table_name in get_database_tables(connection):
        pragma_df = pd.read_sql_query(
            f"PRAGMA table_info({table_name});",
            connection,
        )

        for _, column in pragma_df.iterrows():
            rows.append(
                {
                    "table_name": table_name,
                    "column_id": column["cid"],
                    "column_name": column["name"],
                    "sqlite_type": column["type"],
                    "not_null": column["notnull"],
                    "default_value": column["dflt_value"],
                    "primary_key": column["pk"],
                }
            )

    return pd.DataFrame(rows)


def build_manifest_report(
    batch_id: str,
    extracted_at: str,
    status: str,
    imported_tables_count: int,
    executed_queries_count: int,
    successful_queries_count: int,
    error_message: str = "",
) -> pd.DataFrame:
    """
    Build the database extraction manifest.

    The manifest gives a high-level summary of the database extraction run.
    """
    database_hash = ""

    if LEGACY_DATABASE_PATH.exists():
        database_hash = calculate_file_hash(LEGACY_DATABASE_PATH)

    return pd.DataFrame(
        [
            {
                "extraction_batch_id": batch_id,
                "source_name": SOURCE_NAME,
                "source_type": "SQL database",
                "database_engine": "SQLite",
                "database_path": str(LEGACY_DATABASE_PATH),
                "database_hash_sha256": database_hash,
                "sql_queries_file": str(SQL_QUERIES_OUTPUT),
                "extracted_at": extracted_at,
                "status": status,
                "imported_tables_count": imported_tables_count,
                "executed_queries_count": executed_queries_count,
                "successful_queries_count": successful_queries_count,
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
    Build an error report when the database extraction fails.
    """
    return pd.DataFrame(
        [
            {
                "extraction_batch_id": batch_id,
                "source_name": SOURCE_NAME,
                "database_path": str(LEGACY_DATABASE_PATH),
                "extracted_at": extracted_at,
                "error_message": error_message,
            }
        ]
    )


def save_reports(
    manifest_df: pd.DataFrame,
    schema_df: pd.DataFrame,
    query_report_df: pd.DataFrame,
    import_report_df: pd.DataFrame,
    error_df: pd.DataFrame,
) -> None:
    """
    Save all database extraction reports as CSV files.
    """
    manifest_df.to_csv(
        DATABASE_COLLECTION_REPORTS_DIR / "database_extraction_manifest.csv",
        index=False,
        encoding="utf-8",
    )

    schema_df.to_csv(
        DATABASE_COLLECTION_REPORTS_DIR / "database_extraction_schema_report.csv",
        index=False,
        encoding="utf-8",
    )

    query_report_df.to_csv(
        DATABASE_COLLECTION_REPORTS_DIR / "database_extraction_query_report.csv",
        index=False,
        encoding="utf-8",
    )

    import_report_df.to_csv(
        DATABASE_COLLECTION_REPORTS_DIR / "database_import_report.csv",
        index=False,
        encoding="utf-8",
    )

    error_df.to_csv(
        DATABASE_COLLECTION_REPORTS_DIR / "database_extraction_errors.csv",
        index=False,
        encoding="utf-8",
    )


def collect_from_database() -> None:
    """
    Run the full database extraction process.

    This function:
    - creates the simulated legacy database;
    - imports raw CSV files into SQL tables;
    - writes SQL queries to a documentation file;
    - executes extraction queries;
    - saves CSV outputs and reports.
    """
    batch_id = get_current_batch_id()
    extracted_at = get_current_timestamp()

    logging.info("Starting database extraction batch: %s", batch_id)

    connection: Optional[sqlite3.Connection] = None

    try:
        reset_legacy_database()
        connection = connect_to_legacy_database()

        import_report_df = import_raw_files_to_legacy_database(connection)
        write_sql_queries_to_file()

        schema_df = build_schema_report(connection)

        query_report_df = execute_extraction_queries(
            connection=connection,
            batch_id=batch_id,
            extracted_at=extracted_at,
        )

        successful_queries_count = int(
            (query_report_df["status"] == "success").sum()
        )

        manifest_df = build_manifest_report(
            batch_id=batch_id,
            extracted_at=extracted_at,
            status="success",
            imported_tables_count=len(import_report_df),
            executed_queries_count=len(query_report_df),
            successful_queries_count=successful_queries_count,
            error_message="",
        )

        error_df = query_report_df[
            query_report_df["status"] != "success"
        ][["query_name", "status", "error_message"]].copy()

        save_reports(
            manifest_df=manifest_df,
            schema_df=schema_df,
            query_report_df=query_report_df,
            import_report_df=import_report_df,
            error_df=error_df,
        )

        logging.info("Database extraction batch completed successfully: %s", batch_id)

    except Exception as error:
        error_message = str(error)

        logging.exception("Database extraction batch failed: %s", batch_id)

        manifest_df = build_manifest_report(
            batch_id=batch_id,
            extracted_at=extracted_at,
            status="extraction_error",
            imported_tables_count=0,
            executed_queries_count=0,
            successful_queries_count=0,
            error_message=error_message,
        )

        schema_df = pd.DataFrame()
        query_report_df = pd.DataFrame()
        import_report_df = pd.DataFrame()
        error_df = build_error_report(
            batch_id=batch_id,
            extracted_at=extracted_at,
            error_message=error_message,
        )

        save_reports(
            manifest_df=manifest_df,
            schema_df=schema_df,
            query_report_df=query_report_df,
            import_report_df=import_report_df,
            error_df=error_df,
        )

        raise

    finally:
        if connection is not None:
            connection.close()


def main() -> None:
    """
    Entry point of the script.

    It prepares folders, configures logging, runs the database extraction,
    and prints a short execution summary.
    """
    ensure_directories()
    setup_logging()
    collect_from_database()

    manifest_path = DATABASE_COLLECTION_REPORTS_DIR / "database_extraction_manifest.csv"
    schema_path = DATABASE_COLLECTION_REPORTS_DIR / "database_extraction_schema_report.csv"
    query_report_path = DATABASE_COLLECTION_REPORTS_DIR / "database_extraction_query_report.csv"
    import_report_path = DATABASE_COLLECTION_REPORTS_DIR / "database_import_report.csv"
    errors_path = DATABASE_COLLECTION_REPORTS_DIR / "database_extraction_errors.csv"

    manifest_df = pd.read_csv(manifest_path)
    query_report_df = pd.read_csv(query_report_path)

    print("Database-based data collection completed successfully.")
    print(f"Legacy database: {LEGACY_DATABASE_PATH}")
    print(f"SQL queries file: {SQL_QUERIES_OUTPUT}")
    print(f"Database extracts folder: {DATABASE_EXTRACT_DIR}")
    print(f"Manifest report: {manifest_path}")
    print(f"Schema report: {schema_path}")
    print(f"Query report: {query_report_path}")
    print(f"Import report: {import_report_path}")
    print(f"Error report: {errors_path}")
    print("Manifest status:")
    print(manifest_df["status"].value_counts().to_string())
    print("Query status summary:")
    print(query_report_df["status"].value_counts().to_string())


if __name__ == "__main__":
    main()