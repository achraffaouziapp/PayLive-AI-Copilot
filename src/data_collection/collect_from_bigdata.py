from pathlib import Path
from datetime import datetime
from typing import Dict, Optional
import hashlib
import logging
import shutil
import os
import sys

import pandas as pd

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F


# -------------------------------------------------------------------
# Big data-based data collection
# -------------------------------------------------------------------
# This script simulates and extracts data from a big data-style source.
#
# In the PayLive AI Copilot project, live events represent technical
# and behavioral logs generated during live shopping sessions:
# comments, cart openings, payment clicks, payment successes, API errors,
# and product views.
#
# In a real project, these events could come from a data lake, a Spark
# cluster, Hive, HDFS, S3, or another distributed storage system.
#
# In this student project, we simulate that environment by:
# - reading the raw live events CSV file;
# - converting it into a partitioned Parquet data source;
# - reading the Parquet source with PySpark;
# - executing Spark SQL extraction queries;
# - saving the extracted results as CSV files;
# - generating manifest, schema, query, and error reports.
#
# Important:
# This script does not clean the data.
# It only extracts, structures, and aggregates data from a big data-like
# source. Cleaning and normalization will be done later in dedicated
# data processing scripts.
# -------------------------------------------------------------------


BASE_DIR = Path(__file__).resolve().parents[2]

RAW_DIR = BASE_DIR / "data" / "raw"
INTERIM_DIR = BASE_DIR / "data" / "interim"
INTERIM_EXTRACTS_DIR = INTERIM_DIR / "extracts"
INTERIM_REPORTS_DIR = INTERIM_DIR / "reports"

BIGDATA_RAW_DIR = RAW_DIR / "bigdata"
BIGDATA_PARQUET_DIR = BIGDATA_RAW_DIR / "live_events_parquet"
BIGDATA_EXTRACT_DIR = INTERIM_EXTRACTS_DIR / "bigdata"
BIGDATA_COLLECTION_REPORTS_DIR = INTERIM_REPORTS_DIR / "bigdata_collection"
LOG_DIR = BASE_DIR / "logs"
SQL_DIR = BASE_DIR / "sql"

RAW_EVENTS_CSV = RAW_DIR / "live_events_raw.csv"
BIGDATA_SQL_QUERIES_OUTPUT = SQL_DIR / "05_bigdata_extraction_queries.sql"

SOURCE_NAME = "paylive_bigdata_live_events"
SPARK_APP_NAME = "PayLiveAI_BigData_Extraction"

# This multiplier is used to simulate a larger event volume from the
# original raw events file. The goal is to make the source look more
# like a log dataset without requiring huge files.
SIMULATION_MULTIPLIER = 8


SPARK_SQL_EXTRACTION_QUERIES: Dict[str, str] = {
    "events_by_live": """
        SELECT
            live_id,
            COUNT(*) AS total_events,
            COUNT(DISTINCT customer_id) AS unique_customers,
            SUM(CASE WHEN event_type = 'comment_sent' THEN 1 ELSE 0 END) AS comment_events,
            SUM(CASE WHEN event_type = 'cart_opened' THEN 1 ELSE 0 END) AS cart_opened_events,
            SUM(CASE WHEN event_type = 'payment_clicked' THEN 1 ELSE 0 END) AS payment_clicked_events,
            SUM(CASE WHEN event_type = 'payment_succeeded' THEN 1 ELSE 0 END) AS payment_succeeded_events,
            SUM(CASE WHEN event_type = 'api_error' THEN 1 ELSE 0 END) AS api_error_events
        FROM live_events_bigdata
        GROUP BY live_id
        ORDER BY total_events DESC
    """,
    "payment_funnel_by_live": """
        SELECT
            live_id,
            SUM(CASE WHEN event_type = 'cart_opened' THEN 1 ELSE 0 END) AS cart_opened_events,
            SUM(CASE WHEN event_type = 'payment_clicked' THEN 1 ELSE 0 END) AS payment_clicked_events,
            SUM(CASE WHEN event_type = 'payment_succeeded' THEN 1 ELSE 0 END) AS payment_succeeded_events,
            CASE
                WHEN SUM(CASE WHEN event_type = 'cart_opened' THEN 1 ELSE 0 END) = 0
                THEN 0
                ELSE ROUND(
                    SUM(CASE WHEN event_type = 'payment_succeeded' THEN 1 ELSE 0 END)
                    / SUM(CASE WHEN event_type = 'cart_opened' THEN 1 ELSE 0 END),
                    4
                )
            END AS payment_success_ratio
        FROM live_events_bigdata
        GROUP BY live_id
        ORDER BY payment_success_ratio DESC
    """,
    "api_errors_by_live": """
        SELECT
            live_id,
            source_system,
            COUNT(*) AS api_error_count
        FROM live_events_bigdata
        WHERE event_type = 'api_error'
        GROUP BY live_id, source_system
        ORDER BY api_error_count DESC
    """,
    "hourly_activity": """
        SELECT
            event_date,
            event_hour,
            event_type,
            COUNT(*) AS event_count
        FROM live_events_bigdata
        GROUP BY event_date, event_hour, event_type
        ORDER BY event_date, event_hour, event_count DESC
    """,
    "invalid_events_extract": """
        SELECT
            event_id,
            source_event_id,
            live_id,
            customer_id,
            event_type,
            event_timestamp,
            event_date,
            event_hour,
            event_value,
            source_system,
            simulation_copy_index
        FROM live_events_bigdata
        WHERE
            live_id IS NULL
            OR TRIM(live_id) = ''
            OR event_timestamp IS NULL
            OR TRIM(event_timestamp) = ''
            OR parsed_event_timestamp IS NULL
            OR event_type NOT IN (
                'comment_sent',
                'cart_opened',
                'payment_clicked',
                'payment_succeeded',
                'api_error',
                'product_viewed'
            )
        ORDER BY event_id
    """,
}


def ensure_directories() -> None:
    """
    Create all folders required by the big data extraction script.

    The partitioned Parquet source is saved in `data/raw/bigdata`.
    Extracted query results are saved in `data/interim/extracts/bigdata`.
    SQL query documentation is saved in `sql`.
    Execution logs are saved in `logs`.
    """
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    INTERIM_EXTRACTS_DIR.mkdir(parents=True, exist_ok=True)
    INTERIM_REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    BIGDATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
    BIGDATA_EXTRACT_DIR.mkdir(parents=True, exist_ok=True)
    BIGDATA_COLLECTION_REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    SQL_DIR.mkdir(parents=True, exist_ok=True)


def setup_logging() -> None:
    """
    Configure the logging system.

    Logs help prove that the big data extraction process was executed
    and make debugging easier if Spark fails.
    """
    log_file = LOG_DIR / "collect_from_bigdata.log"

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        encoding="utf-8",
    )


def get_current_batch_id() -> str:
    """
    Generate a unique extraction batch ID.

    This ID links the Parquet source, SQL queries, extracted CSV files,
    and reports produced during the same execution.
    """
    return datetime.now().strftime("BIGDATA_BATCH_%Y%m%d_%H%M%S")


def get_current_timestamp() -> str:
    """
    Return the current timestamp in a standard format.

    This timestamp is written in extraction reports for traceability.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def calculate_text_hash(text: str) -> str:
    """
    Calculate a SHA256 hash from a text value.

    This is used to track the exact Spark SQL query executed.
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def configure_python_for_pyspark() -> str:
    """
    Force PySpark to use the same Python executable as the current
    virtual environment.

    On Windows, Spark may try to call `python` from the system PATH.
    If the Microsoft Store Python alias is enabled, Spark workers fail
    with: "Python was not found".

    Using sys.executable ensures that Spark uses:
    .venv/Scripts/python.exe
    """
    python_executable = sys.executable

    os.environ["PYSPARK_PYTHON"] = python_executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = python_executable

    return python_executable


def create_spark_session() -> SparkSession:
    """
    Create a local Spark session.

    The session runs locally on the developer machine.

    On Windows, we explicitly force Spark to use the Python executable
    from the current virtual environment. This avoids Microsoft Store
    Python alias issues.
    """
    python_executable = configure_python_for_pyspark()

    spark = (
        SparkSession.builder
        .appName(SPARK_APP_NAME)
        .master("local[1]")
        .config("spark.sql.session.timeZone", "UTC")
        .config("spark.ui.showConsoleProgress", "false")
        .config("spark.sql.execution.arrow.pyspark.enabled", "false")
        .config("spark.pyspark.python", python_executable)
        .config("spark.pyspark.driver.python", python_executable)
        .config("spark.executorEnv.PYSPARK_PYTHON", python_executable)
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    return spark


def check_raw_events_file_exists() -> None:
    """
    Check that the raw live events CSV file exists.

    This file is generated by the raw data simulation script.
    """
    if not RAW_EVENTS_CSV.exists():
        raise FileNotFoundError(
            f"Required file not found: {RAW_EVENTS_CSV}. "
            "Run src/data_simulation/generate_raw_data.py before this script."
        )


def remove_existing_parquet_source() -> None:
    """
    Remove the previous Parquet source if it exists.

    On Windows, deleting a Spark-written folder manually can be unstable.
    Using shutil.rmtree is simpler and more reliable.
    """
    if BIGDATA_PARQUET_DIR.exists():
        shutil.rmtree(BIGDATA_PARQUET_DIR)


def read_raw_events_with_spark(spark: SparkSession) -> DataFrame:
    """
    Read the raw live events CSV file using Spark.

    All values are read as strings first because raw data can contain
    invalid timestamps, unknown event types, or missing values.
    """
    return (
        spark.read
        .option("header", True)
        .option("inferSchema", False)
        .option("encoding", "UTF-8")
        .csv(str(RAW_EVENTS_CSV))
    )


def simulate_larger_event_volume(events_df: DataFrame, spark: SparkSession) -> DataFrame:
    """
    Simulate a larger event log volume.

    The original raw CSV is intentionally small for the project.
    This function duplicates the rows several times and adds a
    `simulation_copy_index` column.

    This does not clean the data. It only creates a larger event source
    to make the extraction closer to a big data scenario.
    """
    multiplier_df = spark.range(0, SIMULATION_MULTIPLIER).withColumnRenamed(
        "id",
        "simulation_copy_index",
    )

    expanded_df = events_df.crossJoin(multiplier_df)

    expanded_df = expanded_df.withColumn(
        "source_event_id",
        F.col("event_id"),
    ).withColumn(
        "event_id",
        F.concat(
            F.col("event_id"),
            F.lit("_COPY_"),
            F.col("simulation_copy_index").cast("string"),
        ),
    )

    return expanded_df


def enrich_events_for_partitioning(events_df: DataFrame) -> DataFrame:
    """
    Add technical columns required for Parquet partitioning and SQL queries.

    `parsed_event_timestamp` is created only for extraction purposes.
    Invalid timestamps become null and will later be detected in the
    invalid events query.
    """
    enriched_df = events_df.withColumn(
        "parsed_event_timestamp",
        F.to_timestamp("event_timestamp"),
    ).withColumn(
        "event_date",
        F.to_date("parsed_event_timestamp"),
    ).withColumn(
        "event_hour",
        F.hour("parsed_event_timestamp"),
    )

    enriched_df = enriched_df.withColumn(
        "event_date_partition",
        F.coalesce(F.col("event_date").cast("string"), F.lit("invalid_date")),
    )

    return enriched_df


def create_partitioned_parquet_source(spark: SparkSession) -> pd.DataFrame:
    """
    Create the partitioned Parquet big data source.

    On Windows, Spark can require Hadoop winutils.exe when writing files.
    To avoid this environment dependency, the Parquet source is created
    with pandas and pyarrow.

    Spark is still used afterward to read the Parquet source and execute
    Spark SQL extraction queries.
    """
    check_raw_events_file_exists()
    remove_existing_parquet_source()

    raw_events_df = pd.read_csv(
        RAW_EVENTS_CSV,
        dtype=str,
        keep_default_na=False,
        encoding="utf-8",
    )

    expanded_frames = []

    for copy_index in range(SIMULATION_MULTIPLIER):
        copy_df = raw_events_df.copy()

        copy_df["simulation_copy_index"] = copy_index
        copy_df["source_event_id"] = copy_df["event_id"]
        copy_df["event_id"] = (
            copy_df["event_id"].astype(str)
            + "_COPY_"
            + str(copy_index)
        )

        expanded_frames.append(copy_df)

    expanded_df = pd.concat(expanded_frames, ignore_index=True)

    expanded_df["parsed_event_timestamp"] = pd.to_datetime(
        expanded_df["event_timestamp"],
        errors="coerce",
    )

    expanded_df["event_date"] = expanded_df["parsed_event_timestamp"].dt.strftime(
        "%Y-%m-%d"
    )

    expanded_df["event_hour"] = expanded_df["parsed_event_timestamp"].dt.hour

    expanded_df["event_date_partition"] = expanded_df["event_date"].fillna(
        "invalid_date"
    )

    row_count = len(expanded_df)
    column_count = len(expanded_df.columns)

    expanded_df.to_parquet(
        BIGDATA_PARQUET_DIR,
        engine="pyarrow",
        partition_cols=["event_date_partition"],
        index=False,
    )

    logging.info(
        "Partitioned Parquet source created with pandas/pyarrow at %s with %s rows.",
        BIGDATA_PARQUET_DIR,
        row_count,
    )

    return pd.DataFrame(
        [
            {
                "source_name": SOURCE_NAME,
                "raw_input_file": str(RAW_EVENTS_CSV),
                "parquet_output_folder": str(BIGDATA_PARQUET_DIR),
                "simulation_multiplier": SIMULATION_MULTIPLIER,
                "row_count": row_count,
                "column_count": column_count,
                "partition_column": "event_date_partition",
                "status": "created_with_pandas_pyarrow",
            }
        ]
    )

def prepare_pandas_dataframe_for_spark(pandas_df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare a pandas DataFrame before converting it to Spark.

    This avoids type inference issues when some columns contain mixed
    values, missing values, or timestamps.
    """
    string_columns = [
        "event_id",
        "source_event_id",
        "live_id",
        "customer_id",
        "event_type",
        "event_timestamp",
        "event_date",
        "event_value",
        "source_system",
        "event_date_partition",
    ]

    for column in string_columns:
        if column in pandas_df.columns:
            pandas_df[column] = pandas_df[column].astype(str)
            pandas_df.loc[pandas_df[column].isin(["nan", "NaT", "None"]), column] = None

    if "simulation_copy_index" in pandas_df.columns:
        pandas_df["simulation_copy_index"] = pd.to_numeric(
            pandas_df["simulation_copy_index"],
            errors="coerce",
        )

    if "event_hour" in pandas_df.columns:
        pandas_df["event_hour"] = pd.to_numeric(
            pandas_df["event_hour"],
            errors="coerce",
        )

    if "parsed_event_timestamp" in pandas_df.columns:
        pandas_df["parsed_event_timestamp"] = pd.to_datetime(
            pandas_df["parsed_event_timestamp"],
            errors="coerce",
        )

    pandas_df = pandas_df.astype(object).where(pd.notnull(pandas_df), None)

    return pandas_df



def read_parquet_source(spark: SparkSession) -> DataFrame:
    """
    Read the partitioned Parquet source with pandas/pyarrow, then convert
    it to a Spark DataFrame.

    This avoids Hadoop NativeIO issues on Windows while still allowing
    Spark SQL extraction queries.
    """
    pandas_df = pd.read_parquet(
        BIGDATA_PARQUET_DIR,
        engine="pyarrow",
    )

    pandas_df = prepare_pandas_dataframe_for_spark(pandas_df)

    return spark.createDataFrame(pandas_df)


def register_temp_view(events_df: DataFrame) -> None:
    """
    Register the Spark DataFrame as a temporary SQL view.

    This allows the extraction queries to be written in Spark SQL.
    """
    events_df.createOrReplaceTempView("live_events_bigdata")


def write_sql_queries_to_file() -> None:
    """
    Save all Spark SQL extraction queries in a dedicated SQL file.

    This file documents the queries used for big data extraction.
    """
    lines = [
        "-- Spark SQL extraction queries for PayLive AI Copilot",
        "-- Source: simulated big data live events Parquet dataset",
        "-- This file is generated by src/data_collection/collect_from_bigdata.py",
        "",
    ]

    for query_name, query in SPARK_SQL_EXTRACTION_QUERIES.items():
        lines.append("-- ============================================================")
        lines.append(f"-- Query name: {query_name}")
        lines.append("-- Purpose: Extract and aggregate events from the big data source.")
        lines.append("-- ============================================================")
        lines.append(query.strip())
        lines.append(";")
        lines.append("")

    BIGDATA_SQL_QUERIES_OUTPUT.write_text("\n".join(lines), encoding="utf-8")


def save_spark_result_as_csv(result_df: DataFrame, output_file_path: Path) -> None:
    """
    Save a Spark query result as a single CSV file.

    Spark normally writes multiple part files. For this project, the
    query outputs are small, so they are converted to pandas and saved
    as single CSV files for easier documentation and review.
    """
    pandas_df = result_df.toPandas()
    pandas_df.to_csv(output_file_path, index=False, encoding="utf-8")


def execute_one_query(
    spark: SparkSession,
    query_name: str,
    query: str,
    batch_id: str,
    extracted_at: str,
) -> Dict[str, object]:
    """
    Execute one Spark SQL query and save the result as a CSV file.

    Extraction metadata columns are added to each result for traceability.
    """
    output_file_path = BIGDATA_EXTRACT_DIR / f"{query_name}_extract.csv"

    try:
        result_df = spark.sql(query)

        result_df = (
            result_df
            .withColumn("extraction_batch_id", F.lit(batch_id))
            .withColumn("source_system", F.lit(SOURCE_NAME))
            .withColumn("query_name", F.lit(query_name))
            .withColumn("extracted_at", F.lit(extracted_at))
        )

        metadata_columns = [
            "extraction_batch_id",
            "source_system",
            "query_name",
            "extracted_at",
        ]

        ordered_columns = metadata_columns + [
            column for column in result_df.columns if column not in metadata_columns
        ]

        result_df = result_df.select(*ordered_columns)

        row_count = result_df.count()
        column_count = len(result_df.columns)

        save_spark_result_as_csv(result_df, output_file_path)

        logging.info(
            "Spark SQL query %s executed successfully with %s rows.",
            query_name,
            row_count,
        )

        return {
            "query_name": query_name,
            "status": "success",
            "row_count": row_count,
            "column_count": column_count,
            "output_file_path": str(output_file_path),
            "query_hash_sha256": calculate_text_hash(query),
            "error_message": "",
        }

    except Exception as error:
        logging.exception("Spark SQL query %s failed.", query_name)

        return {
            "query_name": query_name,
            "status": "query_error",
            "row_count": 0,
            "column_count": 0,
            "output_file_path": "",
            "query_hash_sha256": calculate_text_hash(query),
            "error_message": str(error),
        }


def execute_bigdata_queries(
    spark: SparkSession,
    batch_id: str,
    extracted_at: str,
) -> pd.DataFrame:
    """
    Execute all Spark SQL extraction queries.

    Each query result is saved as a separate CSV file.
    """
    query_report_rows = []

    for query_name, query in SPARK_SQL_EXTRACTION_QUERIES.items():
        result = execute_one_query(
            spark=spark,
            query_name=query_name,
            query=query,
            batch_id=batch_id,
            extracted_at=extracted_at,
        )

        query_report_rows.append(result)

    return pd.DataFrame(query_report_rows)


def build_schema_report(events_df: DataFrame) -> pd.DataFrame:
    """
    Build a schema report for the Parquet big data source.

    This report lists the columns and Spark data types detected.
    """
    rows = []

    for field in events_df.schema.fields:
        rows.append(
            {
                "source_name": SOURCE_NAME,
                "column_name": field.name,
                "spark_type": str(field.dataType),
                "nullable": field.nullable,
            }
        )

    return pd.DataFrame(rows)


def build_source_profile_report(events_df: DataFrame) -> pd.DataFrame:
    """
    Build a small profile report of the big data source.

    This report gives high-level information about event volume,
    distinct lives, distinct customers, and event types.
    """
    total_rows = events_df.count()

    distinct_lives = events_df.select("live_id").distinct().count()
    distinct_customers = events_df.select("customer_id").distinct().count()
    distinct_event_types = events_df.select("event_type").distinct().count()

    invalid_timestamp_count = events_df.filter(
        F.col("parsed_event_timestamp").isNull()
    ).count()

    return pd.DataFrame(
        [
            {
                "source_name": SOURCE_NAME,
                "total_rows": total_rows,
                "distinct_lives": distinct_lives,
                "distinct_customers": distinct_customers,
                "distinct_event_types": distinct_event_types,
                "invalid_timestamp_count": invalid_timestamp_count,
                "parquet_folder": str(BIGDATA_PARQUET_DIR),
            }
        ]
    )


def build_manifest_report(
    batch_id: str,
    extracted_at: str,
    status: str,
    source_row_count: int,
    executed_queries_count: int,
    successful_queries_count: int,
    error_message: str = "",
) -> pd.DataFrame:
    """
    Build the big data extraction manifest.

    The manifest gives a high-level summary of the extraction run.
    """
    return pd.DataFrame(
        [
            {
                "extraction_batch_id": batch_id,
                "source_name": SOURCE_NAME,
                "source_type": "big_data_parquet",
                "processing_engine": "PySpark",
                "spark_app_name": SPARK_APP_NAME,
                "raw_input_file": str(RAW_EVENTS_CSV),
                "parquet_source_folder": str(BIGDATA_PARQUET_DIR),
                "sql_queries_file": str(BIGDATA_SQL_QUERIES_OUTPUT),
                "extracted_at": extracted_at,
                "status": status,
                "source_row_count": source_row_count,
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
    Build an error report when the big data extraction fails.
    """
    return pd.DataFrame(
        [
            {
                "extraction_batch_id": batch_id,
                "source_name": SOURCE_NAME,
                "parquet_source_folder": str(BIGDATA_PARQUET_DIR),
                "extracted_at": extracted_at,
                "error_message": error_message,
            }
        ]
    )


def save_reports(
    manifest_df: pd.DataFrame,
    schema_df: pd.DataFrame,
    source_profile_df: pd.DataFrame,
    query_report_df: pd.DataFrame,
    parquet_creation_report_df: pd.DataFrame,
    error_df: pd.DataFrame,
) -> None:
    """
    Save all big data extraction reports as CSV files.
    """
    manifest_df.to_csv(
        BIGDATA_COLLECTION_REPORTS_DIR / "bigdata_extraction_manifest.csv",
        index=False,
        encoding="utf-8",
    )

    schema_df.to_csv(
        BIGDATA_COLLECTION_REPORTS_DIR / "bigdata_extraction_schema_report.csv",
        index=False,
        encoding="utf-8",
    )

    source_profile_df.to_csv(
        BIGDATA_COLLECTION_REPORTS_DIR / "bigdata_source_profile_report.csv",
        index=False,
        encoding="utf-8",
    )

    query_report_df.to_csv(
        BIGDATA_COLLECTION_REPORTS_DIR / "bigdata_extraction_query_report.csv",
        index=False,
        encoding="utf-8",
    )

    parquet_creation_report_df.to_csv(
        BIGDATA_COLLECTION_REPORTS_DIR / "bigdata_parquet_creation_report.csv",
        index=False,
        encoding="utf-8",
    )

    error_df.to_csv(
        BIGDATA_COLLECTION_REPORTS_DIR / "bigdata_extraction_errors.csv",
        index=False,
        encoding="utf-8",
    )


def collect_from_bigdata() -> None:
    """
    Run the full big data extraction process.

    This function:
    - starts a local Spark session;
    - creates a partitioned Parquet source from raw events;
    - reads the Parquet source with Spark;
    - registers a Spark SQL view;
    - writes the SQL queries to a documentation file;
    - executes the Spark SQL extraction queries;
    - saves CSV outputs and reports.
    """
    batch_id = get_current_batch_id()
    extracted_at = get_current_timestamp()

    logging.info("Starting big data extraction batch: %s", batch_id)

    spark: Optional[SparkSession] = None

    try:
        spark = create_spark_session()

        parquet_creation_report_df = create_partitioned_parquet_source(spark)

        events_df = read_parquet_source(spark)
        register_temp_view(events_df)

        source_row_count = events_df.count()

        write_sql_queries_to_file()

        schema_df = build_schema_report(events_df)
        source_profile_df = build_source_profile_report(events_df)

        query_report_df = execute_bigdata_queries(
            spark=spark,
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
            source_row_count=source_row_count,
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
            source_profile_df=source_profile_df,
            query_report_df=query_report_df,
            parquet_creation_report_df=parquet_creation_report_df,
            error_df=error_df,
        )

        logging.info("Big data extraction batch completed successfully: %s", batch_id)

    except Exception as error:
        error_message = str(error)

        logging.exception("Big data extraction batch failed: %s", batch_id)

        manifest_df = build_manifest_report(
            batch_id=batch_id,
            extracted_at=extracted_at,
            status="extraction_error",
            source_row_count=0,
            executed_queries_count=0,
            successful_queries_count=0,
            error_message=error_message,
        )

        schema_df = pd.DataFrame()
        source_profile_df = pd.DataFrame()
        query_report_df = pd.DataFrame()
        parquet_creation_report_df = pd.DataFrame()
        error_df = build_error_report(
            batch_id=batch_id,
            extracted_at=extracted_at,
            error_message=error_message,
        )

        save_reports(
            manifest_df=manifest_df,
            schema_df=schema_df,
            source_profile_df=source_profile_df,
            query_report_df=query_report_df,
            parquet_creation_report_df=parquet_creation_report_df,
            error_df=error_df,
        )

        raise

    finally:
        if spark is not None:
            spark.stop()


def main() -> None:
    """
    Entry point of the script.

    It prepares folders, configures logging, runs the big data extraction,
    and prints a short execution summary.
    """
    ensure_directories()
    setup_logging()
    collect_from_bigdata()

    manifest_path = BIGDATA_COLLECTION_REPORTS_DIR / "bigdata_extraction_manifest.csv"
    schema_path = BIGDATA_COLLECTION_REPORTS_DIR / "bigdata_extraction_schema_report.csv"
    profile_path = BIGDATA_COLLECTION_REPORTS_DIR / "bigdata_source_profile_report.csv"
    query_report_path = BIGDATA_COLLECTION_REPORTS_DIR / "bigdata_extraction_query_report.csv"
    parquet_report_path = BIGDATA_COLLECTION_REPORTS_DIR / "bigdata_parquet_creation_report.csv"
    errors_path = BIGDATA_COLLECTION_REPORTS_DIR / "bigdata_extraction_errors.csv"

    manifest_df = pd.read_csv(manifest_path)
    query_report_df = pd.read_csv(query_report_path)

    print("Big data-based data collection completed successfully.")
    print(f"Parquet source folder: {BIGDATA_PARQUET_DIR}")
    print(f"Big data extracts folder: {BIGDATA_EXTRACT_DIR}")
    print(f"Spark SQL queries file: {BIGDATA_SQL_QUERIES_OUTPUT}")
    print(f"Manifest report: {manifest_path}")
    print(f"Schema report: {schema_path}")
    print(f"Source profile report: {profile_path}")
    print(f"Query report: {query_report_path}")
    print(f"Parquet creation report: {parquet_report_path}")
    print(f"Error report: {errors_path}")
    print("Manifest status:")
    print(manifest_df["status"].value_counts().to_string())
    print("Query status summary:")
    print(query_report_df["status"].value_counts().to_string())


if __name__ == "__main__":
    main()