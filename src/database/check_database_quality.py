from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional
import logging
import os

import pandas as pd
import psycopg2
from psycopg2 import sql


try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


# -------------------------------------------------------------------
# PostgreSQL database quality checks
# -------------------------------------------------------------------
# This script checks the quality and consistency of data imported into
# the PostgreSQL database for the PayLive AI Copilot project.
#
# It checks:
# - table existence;
# - row counts;
# - primary keys;
# - duplicated primary keys;
# - foreign key integrity;
# - allowed categorical values;
# - non-negative numeric values;
# - final AI dataset availability;
# - audit import status.
#
# Reports are generated in data/processed.
# -------------------------------------------------------------------


BASE_DIR = Path(__file__).resolve().parents[2]

PROCESSED_DIR = BASE_DIR / "data" / "processed"
LOG_DIR = BASE_DIR / "logs"

LOG_FILE = LOG_DIR / "check_database_quality.log"

TABLE_REPORT_PATH = PROCESSED_DIR / "database_quality_table_report.csv"
RELATIONSHIP_REPORT_PATH = PROCESSED_DIR / "database_quality_relationship_report.csv"
BUSINESS_REPORT_PATH = PROCESSED_DIR / "database_quality_business_report.csv"
SUMMARY_REPORT_PATH = PROCESSED_DIR / "database_quality_summary.csv"


TABLES_TO_CHECK = [
    {"schema_name": "core", "table_name": "sellers"},
    {"schema_name": "core", "table_name": "customers"},
    {"schema_name": "core", "table_name": "products"},
    {"schema_name": "core", "table_name": "live_sessions"},
    {"schema_name": "core", "table_name": "live_products"},
    {"schema_name": "core", "table_name": "live_comments"},
    {"schema_name": "core", "table_name": "carts"},
    {"schema_name": "core", "table_name": "cart_items"},
    {"schema_name": "core", "table_name": "orders"},
    {"schema_name": "core", "table_name": "payments"},
    {"schema_name": "core", "table_name": "stock_movements"},
    {"schema_name": "core", "table_name": "live_events"},
    {"schema_name": "analytics", "table_name": "dataset_final_live_sales"},
    {"schema_name": "audit", "table_name": "import_batches"},
    {"schema_name": "audit", "table_name": "import_logs"},
]


ALLOWED_VALUE_RULES = [
    {
        "schema_name": "core",
        "table_name": "sellers",
        "column_name": "main_platform",
        "allowed_values": ["tiktok", "instagram", "facebook_live", "youtube_live", "other"],
    },
    {
        "schema_name": "core",
        "table_name": "sellers",
        "column_name": "seller_status",
        "allowed_values": ["active", "inactive", "suspended"],
    },
    {
        "schema_name": "core",
        "table_name": "customers",
        "column_name": "platform",
        "allowed_values": ["tiktok", "instagram", "facebook_live", "youtube_live", "other"],
    },
    {
        "schema_name": "core",
        "table_name": "products",
        "column_name": "product_status",
        "allowed_values": ["active", "inactive", "out_of_stock"],
    },
    {
        "schema_name": "core",
        "table_name": "live_sessions",
        "column_name": "platform",
        "allowed_values": ["tiktok", "instagram", "facebook_live", "youtube_live", "other"],
    },
    {
        "schema_name": "core",
        "table_name": "live_sessions",
        "column_name": "live_status",
        "allowed_values": ["scheduled", "live", "ended", "cancelled"],
    },
    {
        "schema_name": "core",
        "table_name": "live_sessions",
        "column_name": "currency",
        "allowed_values": ["EUR", "USD", "GBP", "CAD", "CHF"],
    },
    {
        "schema_name": "core",
        "table_name": "live_comments",
        "column_name": "manual_intent_label",
        "allowed_values": [
            "purchase_intent",
            "product_question",
            "payment_question",
            "shipping_question",
            "other",
            "unknown",
        ],
    },
    {
        "schema_name": "core",
        "table_name": "carts",
        "column_name": "cart_status",
        "allowed_values": ["open", "paid", "abandoned", "cancelled"],
    },
    {
        "schema_name": "core",
        "table_name": "orders",
        "column_name": "order_status",
        "allowed_values": ["pending", "confirmed", "paid", "cancelled", "refunded"],
    },
    {
        "schema_name": "core",
        "table_name": "payments",
        "column_name": "payment_status",
        "allowed_values": ["pending", "succeeded", "failed", "cancelled", "refunded"],
    },
    {
        "schema_name": "core",
        "table_name": "live_events",
        "column_name": "event_type",
        "allowed_values": [
            "comment_sent",
            "cart_opened",
            "payment_clicked",
            "payment_succeeded",
            "api_error",
            "product_viewed",
        ],
    },
    {
        "schema_name": "analytics",
        "table_name": "dataset_final_live_sales",
        "column_name": "final_dataset_status",
        "allowed_values": ["ready_for_ai"],
    },
]


NON_NEGATIVE_RULES = [
    {"schema_name": "core", "table_name": "products", "column_name": "unit_price"},
    {"schema_name": "core", "table_name": "products", "column_name": "stock_quantity"},
    {"schema_name": "core", "table_name": "live_sessions", "column_name": "peak_viewers"},
    {"schema_name": "core", "table_name": "live_products", "column_name": "special_live_price"},
    {"schema_name": "core", "table_name": "live_products", "column_name": "initial_stock"},
    {"schema_name": "core", "table_name": "live_products", "column_name": "remaining_stock"},
    {"schema_name": "core", "table_name": "carts", "column_name": "total_amount"},
    {"schema_name": "core", "table_name": "cart_items", "column_name": "quantity"},
    {"schema_name": "core", "table_name": "cart_items", "column_name": "unit_price"},
    {"schema_name": "core", "table_name": "cart_items", "column_name": "line_total"},
    {"schema_name": "core", "table_name": "orders", "column_name": "order_amount"},
    {"schema_name": "core", "table_name": "payments", "column_name": "payment_amount"},
    {"schema_name": "analytics", "table_name": "dataset_final_live_sales", "column_name": "peak_viewers"},
    {"schema_name": "analytics", "table_name": "dataset_final_live_sales", "column_name": "total_comments"},
    {"schema_name": "analytics", "table_name": "dataset_final_live_sales", "column_name": "total_carts"},
    {"schema_name": "analytics", "table_name": "dataset_final_live_sales", "column_name": "total_orders"},
    {"schema_name": "analytics", "table_name": "dataset_final_live_sales", "column_name": "total_revenue"},
    {"schema_name": "analytics", "table_name": "dataset_final_live_sales", "column_name": "total_events"},
]


RATE_RULES = [
    {"schema_name": "analytics", "table_name": "dataset_final_live_sales", "column_name": "purchase_intent_rate"},
    {"schema_name": "analytics", "table_name": "dataset_final_live_sales", "column_name": "cart_abandonment_rate"},
    {"schema_name": "analytics", "table_name": "dataset_final_live_sales", "column_name": "payment_success_rate"},
    {"schema_name": "analytics", "table_name": "dataset_final_live_sales", "column_name": "conversion_rate"},
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
    Load environment variables from .env if available.
    """
    env_path = BASE_DIR / ".env"

    if load_dotenv is not None and env_path.exists():
        load_dotenv(env_path)
        logging.info("Loaded environment variables from %s.", env_path)


def get_current_timestamp() -> str:
    """
    Return the current timestamp.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_database_config() -> Dict[str, Any]:
    """
    Return PostgreSQL connection configuration.
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


def fetch_one_value(connection, query, params: Optional[tuple] = None) -> Any:
    """
    Execute a query and return the first value.
    """
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        result = cursor.fetchone()

    if result is None:
        return None

    return result[0]


def table_exists(connection, schema_name: str, table_name: str) -> bool:
    """
    Return True if the table exists.
    """
    query = """
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = %s
              AND table_name = %s
        );
    """

    return bool(fetch_one_value(connection, query, (schema_name, table_name)))


def get_table_columns(connection, schema_name: str, table_name: str) -> List[str]:
    """
    Return table columns ordered by ordinal position.
    """
    query = """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = %s
          AND table_name = %s
        ORDER BY ordinal_position;
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (schema_name, table_name))
        rows = cursor.fetchall()

    return [row[0] for row in rows]


def get_primary_key_columns(connection, schema_name: str, table_name: str) -> List[str]:
    """
    Return primary key columns for a table.
    """
    query = """
        SELECT kcu.column_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
          ON tc.constraint_name = kcu.constraint_name
         AND tc.table_schema = kcu.table_schema
         AND tc.table_name = kcu.table_name
        WHERE tc.constraint_type = 'PRIMARY KEY'
          AND tc.table_schema = %s
          AND tc.table_name = %s
        ORDER BY kcu.ordinal_position;
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (schema_name, table_name))
        rows = cursor.fetchall()

    return [row[0] for row in rows]


def count_table_rows(connection, schema_name: str, table_name: str) -> int:
    """
    Count rows in a table.
    """
    query = sql.SQL("SELECT COUNT(*) FROM {}.{};").format(
        sql.Identifier(schema_name),
        sql.Identifier(table_name),
    )

    return int(fetch_one_value(connection, query))


def count_missing_primary_key_rows(
    connection,
    schema_name: str,
    table_name: str,
    primary_key_columns: List[str],
) -> int:
    """
    Count rows with missing primary key values.
    """
    if not primary_key_columns:
        return 0

    conditions = []

    for column_name in primary_key_columns:
        conditions.append(
            sql.SQL("{} IS NULL OR {}::text = ''").format(
                sql.Identifier(column_name),
                sql.Identifier(column_name),
            )
        )

    query = sql.SQL("SELECT COUNT(*) FROM {}.{} WHERE {};").format(
        sql.Identifier(schema_name),
        sql.Identifier(table_name),
        sql.SQL(" OR ").join(conditions),
    )

    return int(fetch_one_value(connection, query))


def count_duplicate_primary_key_values(
    connection,
    schema_name: str,
    table_name: str,
    primary_key_columns: List[str],
) -> int:
    """
    Count duplicated primary key groups.
    """
    if not primary_key_columns:
        return 0

    grouped_columns = sql.SQL(", ").join(
        sql.Identifier(column_name)
        for column_name in primary_key_columns
    )

    query = sql.SQL(
        """
        SELECT COUNT(*)
        FROM (
            SELECT {}, COUNT(*) AS duplicate_count
            FROM {}.{}
            GROUP BY {}
            HAVING COUNT(*) > 1
        ) duplicate_groups;
        """
    ).format(
        grouped_columns,
        sql.Identifier(schema_name),
        sql.Identifier(table_name),
        grouped_columns,
    )

    return int(fetch_one_value(connection, query))


def build_table_report(connection) -> pd.DataFrame:
    """
    Build the table quality report.
    """
    rows = []

    for table_config in TABLES_TO_CHECK:
        schema_name = table_config["schema_name"]
        table_name = table_config["table_name"]
        table_full_name = f"{schema_name}.{table_name}"

        exists = table_exists(connection, schema_name, table_name)

        row = {
            "checked_at": get_current_timestamp(),
            "schema_name": schema_name,
            "table_name": table_name,
            "table_full_name": table_full_name,
            "table_exists": exists,
            "row_count": 0,
            "column_count": 0,
            "primary_key_columns": "",
            "missing_primary_key_rows": 0,
            "duplicate_primary_key_values": 0,
            "status": "failed",
            "message": "",
        }

        if not exists:
            row["message"] = "Table does not exist."
            rows.append(row)
            continue

        columns = get_table_columns(connection, schema_name, table_name)
        primary_key_columns = get_primary_key_columns(connection, schema_name, table_name)
        row_count = count_table_rows(connection, schema_name, table_name)

        missing_pk_count = count_missing_primary_key_rows(
            connection,
            schema_name,
            table_name,
            primary_key_columns,
        )

        duplicate_pk_count = count_duplicate_primary_key_values(
            connection,
            schema_name,
            table_name,
            primary_key_columns,
        )

        if row_count == 0:
            status = "warning"
            message = "Table exists but contains no rows."
        elif missing_pk_count > 0 or duplicate_pk_count > 0:
            status = "failed"
            message = "Primary key quality issue detected."
        else:
            status = "success"
            message = "Table quality checks passed."

        row.update(
            {
                "row_count": row_count,
                "column_count": len(columns),
                "primary_key_columns": " | ".join(primary_key_columns),
                "missing_primary_key_rows": missing_pk_count,
                "duplicate_primary_key_values": duplicate_pk_count,
                "status": status,
                "message": message,
            }
        )

        rows.append(row)

    return pd.DataFrame(rows)


def get_foreign_keys(connection) -> List[Dict[str, str]]:
    """
    Return foreign key definitions from the database.
    """
    query = """
        SELECT
            tc.constraint_name,
            tc.table_schema AS source_schema,
            tc.table_name AS source_table,
            kcu.column_name AS source_column,
            ccu.table_schema AS target_schema,
            ccu.table_name AS target_table,
            ccu.column_name AS target_column
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
          ON tc.constraint_name = kcu.constraint_name
         AND tc.table_schema = kcu.table_schema
         AND tc.table_name = kcu.table_name
        JOIN information_schema.constraint_column_usage ccu
          ON ccu.constraint_name = tc.constraint_name
         AND ccu.constraint_schema = tc.constraint_schema
        WHERE tc.constraint_type = 'FOREIGN KEY'
          AND tc.table_schema IN ('core', 'analytics', 'audit')
        ORDER BY
            tc.table_schema,
            tc.table_name,
            tc.constraint_name;
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    foreign_keys = []

    for row in rows:
        foreign_keys.append(
            {
                "constraint_name": row[0],
                "source_schema": row[1],
                "source_table": row[2],
                "source_column": row[3],
                "target_schema": row[4],
                "target_table": row[5],
                "target_column": row[6],
            }
        )

    return foreign_keys


def count_orphan_foreign_key_rows(
    connection,
    foreign_key: Dict[str, str],
) -> int:
    """
    Count rows where a foreign key value has no matching parent row.
    """
    query = sql.SQL(
        """
        SELECT COUNT(*)
        FROM {}.{} AS child_table
        LEFT JOIN {}.{} AS parent_table
          ON child_table.{} = parent_table.{}
        WHERE child_table.{} IS NOT NULL
          AND parent_table.{} IS NULL;
        """
    ).format(
        sql.Identifier(foreign_key["source_schema"]),
        sql.Identifier(foreign_key["source_table"]),
        sql.Identifier(foreign_key["target_schema"]),
        sql.Identifier(foreign_key["target_table"]),
        sql.Identifier(foreign_key["source_column"]),
        sql.Identifier(foreign_key["target_column"]),
        sql.Identifier(foreign_key["source_column"]),
        sql.Identifier(foreign_key["target_column"]),
    )

    return int(fetch_one_value(connection, query))


def build_relationship_report(connection) -> pd.DataFrame:
    """
    Build the foreign key relationship quality report.
    """
    rows = []

    for foreign_key in get_foreign_keys(connection):
        orphan_rows = count_orphan_foreign_key_rows(connection, foreign_key)

        status = "success" if orphan_rows == 0 else "failed"

        rows.append(
            {
                "checked_at": get_current_timestamp(),
                "constraint_name": foreign_key["constraint_name"],
                "source_table": f"{foreign_key['source_schema']}.{foreign_key['source_table']}",
                "source_column": foreign_key["source_column"],
                "target_table": f"{foreign_key['target_schema']}.{foreign_key['target_table']}",
                "target_column": foreign_key["target_column"],
                "orphan_rows": orphan_rows,
                "status": status,
                "message": "No orphan foreign key values found."
                if status == "success"
                else "Orphan foreign key values detected.",
            }
        )

    return pd.DataFrame(rows)


def column_exists(
    connection,
    schema_name: str,
    table_name: str,
    column_name: str,
) -> bool:
    """
    Return True if a column exists in a table.
    """
    return column_name in get_table_columns(connection, schema_name, table_name)


def count_invalid_allowed_values(
    connection,
    schema_name: str,
    table_name: str,
    column_name: str,
    allowed_values: List[str],
) -> int:
    """
    Count values that are not in the allowed list.
    """
    allowed_literals = sql.SQL(", ").join(
        sql.Literal(value)
        for value in allowed_values
    )

    query = sql.SQL(
        """
        SELECT COUNT(*)
        FROM {}.{}
        WHERE {} IS NOT NULL
          AND {}::text <> ''
          AND {}::text NOT IN ({});
        """
    ).format(
        sql.Identifier(schema_name),
        sql.Identifier(table_name),
        sql.Identifier(column_name),
        sql.Identifier(column_name),
        sql.Identifier(column_name),
        allowed_literals,
    )

    return int(fetch_one_value(connection, query))


def count_negative_values(
    connection,
    schema_name: str,
    table_name: str,
    column_name: str,
) -> int:
    """
    Count negative numeric values.
    """
    query = sql.SQL(
        """
        SELECT COUNT(*)
        FROM {}.{}
        WHERE {} IS NOT NULL
          AND {} < 0;
        """
    ).format(
        sql.Identifier(schema_name),
        sql.Identifier(table_name),
        sql.Identifier(column_name),
        sql.Identifier(column_name),
    )

    return int(fetch_one_value(connection, query))


def count_invalid_rate_values(
    connection,
    schema_name: str,
    table_name: str,
    column_name: str,
) -> int:
    """
    Count ratio values outside the [0, 1] interval.
    """
    query = sql.SQL(
        """
        SELECT COUNT(*)
        FROM {}.{}
        WHERE {} IS NOT NULL
          AND ({} < 0 OR {} > 1);
        """
    ).format(
        sql.Identifier(schema_name),
        sql.Identifier(table_name),
        sql.Identifier(column_name),
        sql.Identifier(column_name),
        sql.Identifier(column_name),
    )

    return int(fetch_one_value(connection, query))


def add_business_check_row(
    rows: List[Dict[str, Any]],
    rule_name: str,
    schema_name: str,
    table_name: str,
    column_name: str,
    severity: str,
    issue_count: int,
    message_success: str,
    message_failure: str,
) -> None:
    """
    Add one row to the business report.
    """
    status = "success" if issue_count == 0 else "failed"

    rows.append(
        {
            "checked_at": get_current_timestamp(),
            "rule_name": rule_name,
            "schema_name": schema_name,
            "table_name": table_name,
            "table_full_name": f"{schema_name}.{table_name}",
            "column_name": column_name,
            "severity": severity,
            "issue_count": int(issue_count),
            "status": status,
            "message": message_success if status == "success" else message_failure,
        }
    )


def check_allowed_value_rules(connection, rows: List[Dict[str, Any]]) -> None:
    """
    Check allowed categorical values.
    """
    for rule in ALLOWED_VALUE_RULES:
        schema_name = rule["schema_name"]
        table_name = rule["table_name"]
        column_name = rule["column_name"]

        if not table_exists(connection, schema_name, table_name):
            continue

        if not column_exists(connection, schema_name, table_name, column_name):
            continue

        issue_count = count_invalid_allowed_values(
            connection,
            schema_name,
            table_name,
            column_name,
            rule["allowed_values"],
        )

        add_business_check_row(
            rows,
            "allowed_values_check",
            schema_name,
            table_name,
            column_name,
            "major",
            issue_count,
            "All values belong to the authorized list.",
            "Unauthorized categorical values detected.",
        )


def check_non_negative_rules(connection, rows: List[Dict[str, Any]]) -> None:
    """
    Check non-negative numeric values.
    """
    for rule in NON_NEGATIVE_RULES:
        schema_name = rule["schema_name"]
        table_name = rule["table_name"]
        column_name = rule["column_name"]

        if not table_exists(connection, schema_name, table_name):
            continue

        if not column_exists(connection, schema_name, table_name, column_name):
            continue

        issue_count = count_negative_values(
            connection,
            schema_name,
            table_name,
            column_name,
        )

        add_business_check_row(
            rows,
            "non_negative_numeric_check",
            schema_name,
            table_name,
            column_name,
            "major",
            issue_count,
            "No negative values detected.",
            "Negative numeric values detected.",
        )


def check_rate_rules(connection, rows: List[Dict[str, Any]]) -> None:
    """
    Check ratio values between 0 and 1.
    """
    for rule in RATE_RULES:
        schema_name = rule["schema_name"]
        table_name = rule["table_name"]
        column_name = rule["column_name"]

        if not table_exists(connection, schema_name, table_name):
            continue

        if not column_exists(connection, schema_name, table_name, column_name):
            continue

        issue_count = count_invalid_rate_values(
            connection,
            schema_name,
            table_name,
            column_name,
        )

        add_business_check_row(
            rows,
            "rate_between_0_and_1_check",
            schema_name,
            table_name,
            column_name,
            "major",
            issue_count,
            "All rate values are between 0 and 1.",
            "Rate values outside the [0, 1] interval detected.",
        )


def check_final_dataset_consistency(connection, rows: List[Dict[str, Any]]) -> None:
    """
    Check final AI dataset consistency.
    """
    if not table_exists(connection, "analytics", "dataset_final_live_sales"):
        add_business_check_row(
            rows,
            "final_dataset_exists_check",
            "analytics",
            "dataset_final_live_sales",
            "live_id",
            "critical",
            1,
            "Final AI dataset exists.",
            "Final AI dataset table is missing.",
        )
        return

    final_row_count = count_table_rows(
        connection,
        "analytics",
        "dataset_final_live_sales",
    )

    live_sessions_row_count = count_table_rows(
        connection,
        "core",
        "live_sessions",
    ) if table_exists(connection, "core", "live_sessions") else 0

    missing_final_rows = max(live_sessions_row_count - final_row_count, 0)

    add_business_check_row(
        rows,
        "final_dataset_row_count_check",
        "analytics",
        "dataset_final_live_sales",
        "live_id",
        "critical",
        missing_final_rows,
        "The final AI dataset contains one row per live session.",
        "The final AI dataset has fewer rows than live_sessions.",
    )

    zero_revenue_count = 0
    if column_exists(connection, "analytics", "dataset_final_live_sales", "total_revenue"):
        query = """
            SELECT COUNT(*)
            FROM analytics.dataset_final_live_sales
            WHERE COALESCE(total_revenue, 0) = 0;
        """
        zero_revenue_count = int(fetch_one_value(connection, query))

    add_business_check_row(
        rows,
        "final_dataset_zero_revenue_information",
        "analytics",
        "dataset_final_live_sales",
        "total_revenue",
        "info",
        0,
        f"{zero_revenue_count} live sessions have zero revenue. This can be normal for inactive or unsuccessful lives.",
        "Zero revenue information check failed.",
    )


def check_latest_import_batch(connection, rows: List[Dict[str, Any]]) -> None:
    """
    Check the latest import batch status.
    """
    if not table_exists(connection, "audit", "import_batches"):
        return

    query = """
        SELECT status
        FROM audit.import_batches
        ORDER BY started_at DESC
        LIMIT 1;
    """

    latest_status = fetch_one_value(connection, query)

    issue_count = 0 if latest_status == "success" else 1

    add_business_check_row(
        rows,
        "latest_import_batch_status_check",
        "audit",
        "import_batches",
        "status",
        "major",
        issue_count,
        "The latest import batch has status success.",
        f"The latest import batch status is not success: {latest_status}.",
    )


def build_business_report(connection) -> pd.DataFrame:
    """
    Build the business quality report.
    """
    rows: List[Dict[str, Any]] = []

    check_allowed_value_rules(connection, rows)
    check_non_negative_rules(connection, rows)
    check_rate_rules(connection, rows)
    check_final_dataset_consistency(connection, rows)
    check_latest_import_batch(connection, rows)

    return pd.DataFrame(rows)


def build_summary_report(
    table_report_df: pd.DataFrame,
    relationship_report_df: pd.DataFrame,
    business_report_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build the global database quality summary.
    """
    failed_tables = int((table_report_df["status"] == "failed").sum()) if not table_report_df.empty else 0
    warning_tables = int((table_report_df["status"] == "warning").sum()) if not table_report_df.empty else 0

    failed_relationships = int((relationship_report_df["status"] == "failed").sum()) if not relationship_report_df.empty else 0

    failed_business_rules = int((business_report_df["status"] == "failed").sum()) if not business_report_df.empty else 0

    total_rows_in_database = int(table_report_df["row_count"].sum()) if not table_report_df.empty else 0

    if failed_tables > 0 or failed_relationships > 0 or failed_business_rules > 0:
        global_status = "failed"
    elif warning_tables > 0:
        global_status = "warning"
    else:
        global_status = "success"

    rows = [
        {"metric": "checked_at", "value": get_current_timestamp()},
        {"metric": "global_status", "value": global_status},
        {"metric": "tables_checked", "value": int(len(table_report_df))},
        {"metric": "failed_tables", "value": failed_tables},
        {"metric": "warning_tables", "value": warning_tables},
        {"metric": "relationships_checked", "value": int(len(relationship_report_df))},
        {"metric": "failed_relationships", "value": failed_relationships},
        {"metric": "business_rules_checked", "value": int(len(business_report_df))},
        {"metric": "failed_business_rules", "value": failed_business_rules},
        {"metric": "total_rows_in_checked_tables", "value": total_rows_in_database},
        {"metric": "table_report", "value": str(TABLE_REPORT_PATH)},
        {"metric": "relationship_report", "value": str(RELATIONSHIP_REPORT_PATH)},
        {"metric": "business_report", "value": str(BUSINESS_REPORT_PATH)},
    ]

    return pd.DataFrame(rows)


def save_reports(
    table_report_df: pd.DataFrame,
    relationship_report_df: pd.DataFrame,
    business_report_df: pd.DataFrame,
    summary_report_df: pd.DataFrame,
) -> None:
    """
    Save all database quality reports.
    """
    table_report_df.to_csv(TABLE_REPORT_PATH, index=False, encoding="utf-8")
    relationship_report_df.to_csv(RELATIONSHIP_REPORT_PATH, index=False, encoding="utf-8")
    business_report_df.to_csv(BUSINESS_REPORT_PATH, index=False, encoding="utf-8")
    summary_report_df.to_csv(SUMMARY_REPORT_PATH, index=False, encoding="utf-8")


def run_database_quality_checks() -> None:
    """
    Run all database quality checks.
    """
    connection = connect_to_database()

    try:
        table_report_df = build_table_report(connection)
        relationship_report_df = build_relationship_report(connection)
        business_report_df = build_business_report(connection)

        summary_report_df = build_summary_report(
            table_report_df=table_report_df,
            relationship_report_df=relationship_report_df,
            business_report_df=business_report_df,
        )

        save_reports(
            table_report_df=table_report_df,
            relationship_report_df=relationship_report_df,
            business_report_df=business_report_df,
            summary_report_df=summary_report_df,
        )

        logging.info("Database quality checks completed successfully.")

    finally:
        connection.close()


def main() -> None:
    """
    Entry point of the script.
    """
    ensure_directories()
    setup_logging()
    load_environment_variables()

    run_database_quality_checks()

    table_report_df = pd.read_csv(TABLE_REPORT_PATH)
    relationship_report_df = pd.read_csv(RELATIONSHIP_REPORT_PATH)
    business_report_df = pd.read_csv(BUSINESS_REPORT_PATH)
    summary_report_df = pd.read_csv(SUMMARY_REPORT_PATH)

    print("Database quality checks completed.")
    print(f"Table report: {TABLE_REPORT_PATH}")
    print(f"Relationship report: {RELATIONSHIP_REPORT_PATH}")
    print(f"Business report: {BUSINESS_REPORT_PATH}")
    print(f"Summary report: {SUMMARY_REPORT_PATH}")
    print(f"Log file: {LOG_FILE}")
    print("")
    print("Summary:")
    print(summary_report_df.to_string(index=False))
    print("")
    print("Table status:")
    print(table_report_df[["table_full_name", "row_count", "status"]].to_string(index=False))
    print("")
    print("Relationship issues:")
    print(relationship_report_df[["constraint_name", "orphan_rows", "status"]].to_string(index=False))
    print("")
    print("Business rule failures:")
    failed_business_df = business_report_df[business_report_df["status"] == "failed"]
    if failed_business_df.empty:
        print("No failed business rule.")
    else:
        print(
            failed_business_df[
                ["rule_name", "table_full_name", "column_name", "issue_count", "status"]
            ].to_string(index=False)
        )


if __name__ == "__main__":
    main()