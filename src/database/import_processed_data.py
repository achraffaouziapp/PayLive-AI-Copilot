from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging
import os
import tempfile
import uuid

import pandas as pd
import psycopg2
from psycopg2 import sql


try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


# -------------------------------------------------------------------
# Processed data import into PostgreSQL
# -------------------------------------------------------------------
# This script imports cleaned and aggregated CSV files from data/processed
# into the PostgreSQL database used by the PayLive AI Copilot project.
#
# It imports:
# - cleaned business tables into the core schema;
# - the final AI dataset into the analytics schema;
# - technical import logs into the audit schema.
#
# The script is designed to be executed from the host machine while the
# PostgreSQL database runs in Docker.
# -------------------------------------------------------------------


BASE_DIR = Path(__file__).resolve().parents[2]

PROCESSED_DIR = BASE_DIR / "data" / "processed"
LOG_DIR = BASE_DIR / "logs"

LOG_FILE = LOG_DIR / "import_processed_data.log"

DATABASE_IMPORT_REPORT_PATH = PROCESSED_DIR / "database_import_report.csv"
DATABASE_IMPORT_SUMMARY_PATH = PROCESSED_DIR / "database_import_summary.csv"


IMPORT_TABLES = [
    {
        "schema_name": "core",
        "table_name": "sellers",
        "source_file": "sellers_clean.csv",
    },
    {
        "schema_name": "core",
        "table_name": "customers",
        "source_file": "customers_clean.csv",
    },
    {
        "schema_name": "core",
        "table_name": "products",
        "source_file": "products_clean.csv",
    },
    {
        "schema_name": "core",
        "table_name": "live_sessions",
        "source_file": "live_sessions_clean.csv",
    },
    {
        "schema_name": "core",
        "table_name": "live_products",
        "source_file": "live_products_clean.csv",
    },
    {
        "schema_name": "core",
        "table_name": "live_comments",
        "source_file": "live_comments_clean.csv",
    },
    {
        "schema_name": "core",
        "table_name": "carts",
        "source_file": "carts_clean.csv",
    },
    {
        "schema_name": "core",
        "table_name": "cart_items",
        "source_file": "cart_items_clean.csv",
    },
    {
        "schema_name": "core",
        "table_name": "orders",
        "source_file": "orders_clean.csv",
    },
    {
        "schema_name": "core",
        "table_name": "payments",
        "source_file": "payments_clean.csv",
    },
    {
        "schema_name": "core",
        "table_name": "stock_movements",
        "source_file": "stock_movements_clean.csv",
    },
    {
        "schema_name": "core",
        "table_name": "live_events",
        "source_file": "live_events_clean.csv",
    },
    {
        "schema_name": "analytics",
        "table_name": "dataset_final_live_sales",
        "source_file": "dataset_final_live_sales.csv",
    },
]


def ensure_directories() -> None:
    """
    Create required folders.
    """
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
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


def load_environment_variables() -> None:
    """
    Load environment variables from .env if python-dotenv is installed.
    """
    env_path = BASE_DIR / ".env"

    if load_dotenv is not None and env_path.exists():
        load_dotenv(env_path)
        logging.info("Loaded environment variables from %s.", env_path)
    else:
        logging.info("No .env file loaded. Default database parameters will be used.")


def get_current_timestamp() -> str:
    """
    Return the current timestamp.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_database_config() -> Dict[str, Any]:
    """
    Return PostgreSQL connection configuration.

    Default values are compatible with the Docker Compose setup:
    - host: localhost
    - port: 5433
    - database: paylive_ai_copilot
    - user: postgres
    - password: postgres
    """
    return {
        "host": os.getenv("POSTGRES_HOST", "localhost"),
        "port": int(os.getenv("POSTGRES_PORT", "5433")),
        "dbname": os.getenv("POSTGRES_DB", "paylive_ai_copilot"),
        "user": os.getenv("POSTGRES_USER", "postgres"),
        "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
    }


def connect_to_database():
    """
    Create a PostgreSQL connection.
    """
    config = get_database_config()

    logging.info(
        "Connecting to PostgreSQL database %s on %s:%s.",
        config["dbname"],
        config["host"],
        config["port"],
    )

    return psycopg2.connect(**config)


def generate_import_batch_id() -> str:
    """
    Generate a unique import batch identifier.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_part = uuid.uuid4().hex[:8]

    return f"IMPORT_{timestamp}_{random_part}"


def create_import_batch(connection, import_batch_id: str) -> None:
    """
    Create a new import batch in audit.import_batches.
    """
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO audit.import_batches (
                import_batch_id,
                started_at,
                status,
                source_folder,
                total_tables,
                total_rows_read,
                total_rows_inserted,
                error_message
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """,
            (
                import_batch_id,
                get_current_timestamp(),
                "started",
                str(PROCESSED_DIR),
                len(IMPORT_TABLES),
                0,
                0,
                "",
            ),
        )

    connection.commit()


def update_import_batch(
    connection,
    import_batch_id: str,
    status: str,
    total_rows_read: int,
    total_rows_inserted: int,
    error_message: str = "",
) -> None:
    """
    Update the import batch status.
    """
    with connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE audit.import_batches
            SET
                ended_at = %s,
                status = %s,
                total_rows_read = %s,
                total_rows_inserted = %s,
                error_message = %s
            WHERE import_batch_id = %s;
            """,
            (
                get_current_timestamp(),
                status,
                total_rows_read,
                total_rows_inserted,
                error_message,
                import_batch_id,
            ),
        )

    connection.commit()


def insert_import_log(
    connection,
    import_batch_id: str,
    schema_name: str,
    table_name: str,
    source_file: str,
    rows_read: int,
    rows_inserted: int,
    status: str,
    error_message: str,
) -> None:
    """
    Insert one import log into audit.import_logs.
    """
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO audit.import_logs (
                import_batch_id,
                schema_name,
                table_name,
                source_file,
                rows_read,
                rows_inserted,
                status,
                error_message,
                imported_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """,
            (
                import_batch_id,
                schema_name,
                table_name,
                source_file,
                rows_read,
                rows_inserted,
                status,
                error_message,
                get_current_timestamp(),
            ),
        )

    connection.commit()


def get_table_columns(
    connection,
    schema_name: str,
    table_name: str,
) -> List[str]:
    """
    Return PostgreSQL table columns ordered by ordinal position.
    """
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = %s
              AND table_name = %s
            ORDER BY ordinal_position;
            """,
            (schema_name, table_name),
        )

        rows = cursor.fetchall()

    return [row[0] for row in rows]


def count_table_rows(
    connection,
    schema_name: str,
    table_name: str,
) -> int:
    """
    Count rows in a PostgreSQL table.
    """
    with connection.cursor() as cursor:
        query = sql.SQL("SELECT COUNT(*) FROM {}.{};").format(
            sql.Identifier(schema_name),
            sql.Identifier(table_name),
        )
        cursor.execute(query)
        row_count = cursor.fetchone()[0]

    return int(row_count)


def truncate_target_tables(connection) -> None:
    """
    Truncate all target tables before importing data.

    Audit tables are not truncated in order to keep import history.
    """
    table_identifiers = [
        sql.SQL("{}.{}").format(
            sql.Identifier(table_config["schema_name"]),
            sql.Identifier(table_config["table_name"]),
        )
        for table_config in IMPORT_TABLES
    ]

    truncate_query = sql.SQL("TRUNCATE TABLE {} RESTART IDENTITY CASCADE;").format(
        sql.SQL(", ").join(table_identifiers)
    )

    with connection.cursor() as cursor:
        cursor.execute(truncate_query)

    connection.commit()
    logging.info("Target tables truncated successfully.")


def read_source_csv(source_file_path: Path) -> pd.DataFrame:
    """
    Read a processed CSV file as strings.
    """
    return pd.read_csv(
        source_file_path,
        dtype=str,
        keep_default_na=False,
        encoding="utf-8",
    )


def prepare_dataframe_for_copy(
    dataframe: pd.DataFrame,
    table_columns: List[str],
) -> pd.DataFrame:
    """
    Prepare a DataFrame for PostgreSQL COPY.

    Only columns existing in the target PostgreSQL table are kept.
    Missing columns are ignored because nullable columns can use NULL.
    """
    dataframe = dataframe.copy()

    matching_columns = [
        column
        for column in table_columns
        if column in dataframe.columns
    ]

    prepared_df = dataframe[matching_columns].copy()

    prepared_df = prepared_df.where(pd.notnull(prepared_df), "")

    return prepared_df


def write_temp_csv(dataframe: pd.DataFrame) -> Path:
    """
    Write a temporary CSV file used by PostgreSQL COPY.
    """
    temporary_file = tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".csv",
        encoding="utf-8",
        newline="",
        delete=False,
    )

    temp_path = Path(temporary_file.name)

    with temporary_file:
        dataframe.to_csv(temporary_file, index=False, encoding="utf-8")

    return temp_path


def copy_dataframe_to_postgres(
    connection,
    dataframe: pd.DataFrame,
    schema_name: str,
    table_name: str,
) -> int:
    """
    Import a DataFrame into PostgreSQL using COPY.
    """
    if dataframe.empty:
        return 0

    temp_csv_path = write_temp_csv(dataframe)

    columns = list(dataframe.columns)

    copy_query = sql.SQL(
        """
        COPY {}.{} ({})
        FROM STDIN
        WITH (
            FORMAT CSV,
            HEADER TRUE,
            NULL '',
            ENCODING 'UTF8'
        );
        """
    ).format(
        sql.Identifier(schema_name),
        sql.Identifier(table_name),
        sql.SQL(", ").join(sql.Identifier(column) for column in columns),
    )

    try:
        with connection.cursor() as cursor:
            with temp_csv_path.open("r", encoding="utf-8", newline="") as file:
                cursor.copy_expert(copy_query.as_string(connection), file)

        connection.commit()

    finally:
        if temp_csv_path.exists():
            temp_csv_path.unlink()

    return int(len(dataframe))


def import_one_table(
    connection,
    import_batch_id: str,
    table_config: Dict[str, str],
) -> Dict[str, Any]:
    """
    Import one processed CSV file into one PostgreSQL table.
    """
    schema_name = table_config["schema_name"]
    table_name = table_config["table_name"]
    source_file = table_config["source_file"]
    source_file_path = PROCESSED_DIR / source_file
    table_full_name = f"{schema_name}.{table_name}"

    report_row = {
        "import_batch_id": import_batch_id,
        "schema_name": schema_name,
        "table_name": table_name,
        "table_full_name": table_full_name,
        "source_file": str(source_file_path),
        "source_file_exists": source_file_path.exists(),
        "rows_read": 0,
        "rows_inserted": 0,
        "table_columns_count": 0,
        "imported_columns_count": 0,
        "skipped_source_columns": "",
        "missing_source_columns": "",
        "status": "failed",
        "error_message": "",
        "imported_at": get_current_timestamp(),
    }

    try:
        if not source_file_path.exists():
            raise FileNotFoundError(f"Source file not found: {source_file_path}")

        source_df = read_source_csv(source_file_path)
        rows_read = int(len(source_df))

        table_columns = get_table_columns(
            connection=connection,
            schema_name=schema_name,
            table_name=table_name,
        )

        if not table_columns:
            raise ValueError(f"Target table does not exist or has no columns: {table_full_name}")

        prepared_df = prepare_dataframe_for_copy(
            dataframe=source_df,
            table_columns=table_columns,
        )

        imported_columns = list(prepared_df.columns)
        skipped_source_columns = [
            column
            for column in source_df.columns
            if column not in table_columns
        ]
        missing_source_columns = [
            column
            for column in table_columns
            if column not in source_df.columns
        ]

        rows_inserted = copy_dataframe_to_postgres(
            connection=connection,
            dataframe=prepared_df,
            schema_name=schema_name,
            table_name=table_name,
        )

        final_table_count = count_table_rows(
            connection=connection,
            schema_name=schema_name,
            table_name=table_name,
        )

        report_row.update(
            {
                "rows_read": rows_read,
                "rows_inserted": rows_inserted,
                "table_columns_count": len(table_columns),
                "imported_columns_count": len(imported_columns),
                "skipped_source_columns": " | ".join(skipped_source_columns),
                "missing_source_columns": " | ".join(missing_source_columns),
                "status": "success",
                "error_message": "",
                "final_table_row_count": final_table_count,
                "imported_at": get_current_timestamp(),
            }
        )

        insert_import_log(
            connection=connection,
            import_batch_id=import_batch_id,
            schema_name=schema_name,
            table_name=table_name,
            source_file=str(source_file_path),
            rows_read=rows_read,
            rows_inserted=rows_inserted,
            status="success",
            error_message="",
        )

        logging.info(
            "Imported %s rows into %s.",
            rows_inserted,
            table_full_name,
        )

    except Exception as error:
        connection.rollback()

        error_message = str(error)

        report_row.update(
            {
                "status": "failed",
                "error_message": error_message,
                "imported_at": get_current_timestamp(),
            }
        )

        insert_import_log(
            connection=connection,
            import_batch_id=import_batch_id,
            schema_name=schema_name,
            table_name=table_name,
            source_file=str(source_file_path),
            rows_read=int(report_row["rows_read"]),
            rows_inserted=0,
            status="failed",
            error_message=error_message,
        )

        logging.exception("Failed to import table %s.", table_full_name)

    return report_row


def build_summary_report(
    import_batch_id: str,
    started_at: str,
    ended_at: str,
    report_rows: List[Dict[str, Any]],
) -> pd.DataFrame:
    """
    Build a global import summary report.
    """
    report_df = pd.DataFrame(report_rows)

    total_tables = len(report_rows)
    success_count = int((report_df["status"] == "success").sum()) if not report_df.empty else 0
    failed_count = int((report_df["status"] == "failed").sum()) if not report_df.empty else 0
    total_rows_read = int(report_df["rows_read"].sum()) if not report_df.empty else 0
    total_rows_inserted = int(report_df["rows_inserted"].sum()) if not report_df.empty else 0

    if failed_count == 0:
        status = "success"
    elif success_count > 0:
        status = "partial_success"
    else:
        status = "failed"

    rows = [
        {
            "metric": "import_batch_id",
            "value": import_batch_id,
        },
        {
            "metric": "started_at",
            "value": started_at,
        },
        {
            "metric": "ended_at",
            "value": ended_at,
        },
        {
            "metric": "status",
            "value": status,
        },
        {
            "metric": "total_tables",
            "value": total_tables,
        },
        {
            "metric": "successful_tables",
            "value": success_count,
        },
        {
            "metric": "failed_tables",
            "value": failed_count,
        },
        {
            "metric": "total_rows_read",
            "value": total_rows_read,
        },
        {
            "metric": "total_rows_inserted",
            "value": total_rows_inserted,
        },
        {
            "metric": "source_folder",
            "value": str(PROCESSED_DIR),
        },
    ]

    return pd.DataFrame(rows)


def save_import_reports(
    report_rows: List[Dict[str, Any]],
    summary_df: pd.DataFrame,
) -> None:
    """
    Save import reports as CSV files.
    """
    report_df = pd.DataFrame(report_rows)

    report_df.to_csv(
        DATABASE_IMPORT_REPORT_PATH,
        index=False,
        encoding="utf-8",
    )

    summary_df.to_csv(
        DATABASE_IMPORT_SUMMARY_PATH,
        index=False,
        encoding="utf-8",
    )


def run_database_import() -> None:
    """
    Run the full PostgreSQL import pipeline.
    """
    started_at = get_current_timestamp()
    import_batch_id = generate_import_batch_id()
    report_rows: List[Dict[str, Any]] = []

    connection = connect_to_database()

    try:
        create_import_batch(
            connection=connection,
            import_batch_id=import_batch_id,
        )

        truncate_target_tables(connection)

        for table_config in IMPORT_TABLES:
            report_row = import_one_table(
                connection=connection,
                import_batch_id=import_batch_id,
                table_config=table_config,
            )
            report_rows.append(report_row)

        ended_at = get_current_timestamp()

        summary_df = build_summary_report(
            import_batch_id=import_batch_id,
            started_at=started_at,
            ended_at=ended_at,
            report_rows=report_rows,
        )

        status = summary_df.loc[summary_df["metric"] == "status", "value"].iloc[0]
        total_rows_read = int(
            summary_df.loc[summary_df["metric"] == "total_rows_read", "value"].iloc[0]
        )
        total_rows_inserted = int(
            summary_df.loc[summary_df["metric"] == "total_rows_inserted", "value"].iloc[0]
        )

        error_message = ""
        if status != "success":
            failed_tables = [
                row["table_full_name"]
                for row in report_rows
                if row["status"] == "failed"
            ]
            error_message = "Failed tables: " + " | ".join(failed_tables)

        update_import_batch(
            connection=connection,
            import_batch_id=import_batch_id,
            status=status,
            total_rows_read=total_rows_read,
            total_rows_inserted=total_rows_inserted,
            error_message=error_message,
        )

        save_import_reports(
            report_rows=report_rows,
            summary_df=summary_df,
        )

        logging.info("Database import completed with status: %s.", status)

    finally:
        connection.close()


def main() -> None:
    """
    Entry point of the script.
    """
    ensure_directories()
    setup_logging()
    load_environment_variables()

    run_database_import()

    report_df = pd.read_csv(DATABASE_IMPORT_REPORT_PATH)
    summary_df = pd.read_csv(DATABASE_IMPORT_SUMMARY_PATH)

    print("Processed data import into PostgreSQL completed.")
    print(f"Import report: {DATABASE_IMPORT_REPORT_PATH}")
    print(f"Import summary: {DATABASE_IMPORT_SUMMARY_PATH}")
    print(f"Log file: {LOG_FILE}")
    print("")
    print("Import summary:")
    print(summary_df.to_string(index=False))
    print("")
    print("Tables imported:")
    print(report_df[["table_full_name", "rows_read", "rows_inserted", "status"]].to_string(index=False))


if __name__ == "__main__":
    main()