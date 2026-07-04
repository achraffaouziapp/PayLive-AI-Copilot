from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime
import uuid

import pandas as pd


# -------------------------------------------------------------------
# AI prediction monitoring for PayLive AI Copilot
# -------------------------------------------------------------------
# This module logs AI predictions and generates monitoring reports.
#
# Outputs:
# - data/ai/predictions/ai_predictions_log.csv
# - data/ai/reports/model_monitoring_report.csv
# -------------------------------------------------------------------


BASE_DIR = Path(__file__).resolve().parents[3]

AI_PREDICTIONS_DIR = BASE_DIR / "data" / "ai" / "predictions"
AI_REPORTS_DIR = BASE_DIR / "data" / "ai" / "reports"

PREDICTION_LOG_PATH = AI_PREDICTIONS_DIR / "ai_predictions_log.csv"
MONITORING_REPORT_PATH = AI_REPORTS_DIR / "model_monitoring_report.csv"

LOW_CONFIDENCE_THRESHOLD = 0.60


PREDICTION_LOG_COLUMNS = [
    "prediction_id",
    "predicted_at",
    "comment_text",
    "predicted_intent",
    "confidence_score",
    "model_name",
    "model_version",
    "response_time_ms",
    "is_low_confidence",
    "low_confidence_threshold",
    "source",
]


def ensure_directories() -> None:
    """
    Create required directories for predictions and reports.
    """
    AI_PREDICTIONS_DIR.mkdir(parents=True, exist_ok=True)
    AI_REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def normalize_prediction_for_log(
    prediction: Dict[str, Any],
    source: str = "unknown",
) -> Dict[str, Any]:
    """
    Convert one prediction dictionary into a normalized log row.
    """
    confidence_score = float(prediction.get("confidence_score", 0.0))
    response_time_ms = float(prediction.get("response_time_ms", 0.0))

    is_low_confidence = bool(
        prediction.get(
            "is_low_confidence",
            confidence_score < LOW_CONFIDENCE_THRESHOLD,
        )
    )

    low_confidence_threshold = float(
        prediction.get(
            "low_confidence_threshold",
            LOW_CONFIDENCE_THRESHOLD,
        )
    )

    return {
        "prediction_id": str(uuid.uuid4()),
        "predicted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "comment_text": str(prediction.get("comment_text", "")),
        "predicted_intent": str(prediction.get("predicted_intent", "unknown")),
        "confidence_score": round(confidence_score, 4),
        "model_name": str(prediction.get("model_name", "intent_classifier")),
        "model_version": str(
            prediction.get("model_version", "intent_classifier_v1")
        ),
        "response_time_ms": round(response_time_ms, 2),
        "is_low_confidence": is_low_confidence,
        "low_confidence_threshold": low_confidence_threshold,
        "source": source,
    }


def load_prediction_log() -> pd.DataFrame:
    """
    Load the existing prediction log.

    If the log does not exist, return an empty DataFrame with expected columns.
    """
    ensure_directories()

    if not PREDICTION_LOG_PATH.exists():
        return pd.DataFrame(columns=PREDICTION_LOG_COLUMNS)

    return pd.read_csv(
        PREDICTION_LOG_PATH,
        dtype=str,
        keep_default_na=False,
        encoding="utf-8",
    )


def save_prediction_log(log_df: pd.DataFrame) -> None:
    """
    Save the prediction log.
    """
    ensure_directories()

    log_df.to_csv(
        PREDICTION_LOG_PATH,
        index=False,
        encoding="utf-8",
    )


def log_prediction(
    prediction: Dict[str, Any],
    source: str = "api_single",
) -> Dict[str, Any]:
    """
    Append one prediction to the monitoring log.

    The original prediction dictionary is not modified.
    """
    ensure_directories()

    log_df = load_prediction_log()
    log_row = normalize_prediction_for_log(prediction, source=source)

    updated_log_df = pd.concat(
        [log_df, pd.DataFrame([log_row])],
        ignore_index=True,
    )

    save_prediction_log(updated_log_df)

    return log_row


def log_batch_predictions(
    batch_result: Dict[str, Any],
    source: str = "api_batch",
) -> List[Dict[str, Any]]:
    """
    Append several predictions to the monitoring log.
    """
    predictions = batch_result.get("predictions", [])

    if not isinstance(predictions, list):
        raise ValueError("batch_result['predictions'] must be a list.")

    logged_rows = []

    for prediction in predictions:
        logged_rows.append(
            log_prediction(
                prediction=prediction,
                source=source,
            )
        )

    return logged_rows


def safe_to_float(series: pd.Series) -> pd.Series:
    """
    Convert a pandas Series to float safely.
    """
    return pd.to_numeric(series, errors="coerce").fillna(0.0)


def safe_to_bool(series: pd.Series) -> pd.Series:
    """
    Convert a pandas Series to boolean safely.
    """
    return series.astype(str).str.lower().isin(["true", "1", "yes"])


def build_empty_monitoring_report() -> pd.DataFrame:
    """
    Build a monitoring report when no prediction is available yet.
    """
    rows = [
        {
            "report_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "report_section": "global_summary",
            "metric_name": "prediction_count",
            "metric_value": 0,
            "details": "No prediction has been logged yet.",
        },
        {
            "report_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "report_section": "global_summary",
            "metric_name": "monitoring_status",
            "metric_value": "empty",
            "details": "Run the API prediction routes to generate logs.",
        },
    ]

    return pd.DataFrame(rows)


def build_global_summary(log_df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Build global monitoring metrics.
    """
    report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    confidence_scores = safe_to_float(log_df["confidence_score"])
    response_times = safe_to_float(log_df["response_time_ms"])
    low_confidence_flags = safe_to_bool(log_df["is_low_confidence"])

    prediction_count = len(log_df)
    low_confidence_count = int(low_confidence_flags.sum())

    low_confidence_rate = (
        round((low_confidence_count / prediction_count) * 100, 2)
        if prediction_count
        else 0.0
    )

    rows = [
        {
            "report_date": report_date,
            "report_section": "global_summary",
            "metric_name": "prediction_count",
            "metric_value": prediction_count,
            "details": "Total number of logged predictions.",
        },
        {
            "report_date": report_date,
            "report_section": "global_summary",
            "metric_name": "average_confidence_score",
            "metric_value": round(float(confidence_scores.mean()), 4),
            "details": "Average confidence score across predictions.",
        },
        {
            "report_date": report_date,
            "report_section": "global_summary",
            "metric_name": "minimum_confidence_score",
            "metric_value": round(float(confidence_scores.min()), 4),
            "details": "Minimum confidence score observed.",
        },
        {
            "report_date": report_date,
            "report_section": "global_summary",
            "metric_name": "maximum_confidence_score",
            "metric_value": round(float(confidence_scores.max()), 4),
            "details": "Maximum confidence score observed.",
        },
        {
            "report_date": report_date,
            "report_section": "global_summary",
            "metric_name": "low_confidence_count",
            "metric_value": low_confidence_count,
            "details": "Number of predictions below the confidence threshold.",
        },
        {
            "report_date": report_date,
            "report_section": "global_summary",
            "metric_name": "low_confidence_rate_percent",
            "metric_value": low_confidence_rate,
            "details": "Share of predictions below the confidence threshold.",
        },
        {
            "report_date": report_date,
            "report_section": "global_summary",
            "metric_name": "average_response_time_ms",
            "metric_value": round(float(response_times.mean()), 2),
            "details": "Average prediction response time in milliseconds.",
        },
        {
            "report_date": report_date,
            "report_section": "global_summary",
            "metric_name": "maximum_response_time_ms",
            "metric_value": round(float(response_times.max()), 2),
            "details": "Maximum prediction response time in milliseconds.",
        },
    ]

    return rows


def build_intent_distribution(log_df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Build predicted intent distribution metrics.
    """
    report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    prediction_count = len(log_df)
    intent_counts = log_df["predicted_intent"].value_counts().to_dict()

    rows = []

    for intent, count in sorted(intent_counts.items()):
        percentage = (
            round((int(count) / prediction_count) * 100, 2)
            if prediction_count
            else 0.0
        )

        rows.append(
            {
                "report_date": report_date,
                "report_section": "predicted_intent_distribution",
                "metric_name": intent,
                "metric_value": int(count),
                "details": f"{percentage}% of logged predictions.",
            }
        )

    return rows


def build_model_version_distribution(log_df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Build model version distribution metrics.
    """
    report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    version_counts = log_df["model_version"].value_counts().to_dict()

    rows = []

    for model_version, count in sorted(version_counts.items()):
        rows.append(
            {
                "report_date": report_date,
                "report_section": "model_version_distribution",
                "metric_name": model_version,
                "metric_value": int(count),
                "details": "Number of predictions using this model version.",
            }
        )

    return rows


def build_source_distribution(log_df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Build prediction source distribution metrics.
    """
    report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    source_counts = log_df["source"].value_counts().to_dict()

    rows = []

    for source, count in sorted(source_counts.items()):
        rows.append(
            {
                "report_date": report_date,
                "report_section": "prediction_source_distribution",
                "metric_name": source,
                "metric_value": int(count),
                "details": "Number of predictions from this source.",
            }
        )

    return rows


def build_low_confidence_examples(
    log_df: pd.DataFrame,
    max_examples: int = 10,
) -> List[Dict[str, Any]]:
    """
    Add a few low-confidence examples to the monitoring report.
    """
    report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    working_df = log_df.copy()
    working_df["confidence_score_float"] = safe_to_float(
        working_df["confidence_score"]
    )
    working_df["is_low_confidence_bool"] = safe_to_bool(
        working_df["is_low_confidence"]
    )

    low_confidence_df = working_df[
        working_df["is_low_confidence_bool"]
    ].sort_values(
        by="confidence_score_float",
        ascending=True,
    )

    rows = []

    for _, row in low_confidence_df.head(max_examples).iterrows():
        rows.append(
            {
                "report_date": report_date,
                "report_section": "low_confidence_examples",
                "metric_name": row.get("predicted_intent", "unknown"),
                "metric_value": row.get("confidence_score", ""),
                "details": str(row.get("comment_text", ""))[:250],
            }
        )

    return rows


def build_monitoring_report(log_df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """
    Build the complete model monitoring report.
    """
    if log_df is None:
        log_df = load_prediction_log()

    if log_df.empty:
        return build_empty_monitoring_report()

    rows: List[Dict[str, Any]] = []

    rows.extend(build_global_summary(log_df))
    rows.extend(build_intent_distribution(log_df))
    rows.extend(build_model_version_distribution(log_df))
    rows.extend(build_source_distribution(log_df))
    rows.extend(build_low_confidence_examples(log_df))

    return pd.DataFrame(rows)


def save_monitoring_report(report_df: pd.DataFrame) -> None:
    """
    Save the monitoring report.
    """
    ensure_directories()

    report_df.to_csv(
        MONITORING_REPORT_PATH,
        index=False,
        encoding="utf-8",
    )


def generate_monitoring_report() -> pd.DataFrame:
    """
    Generate and save the monitoring report.
    """
    log_df = load_prediction_log()
    report_df = build_monitoring_report(log_df)

    save_monitoring_report(report_df)

    return report_df


def main() -> None:
    """
    Generate monitoring report from logged predictions.
    """
    ensure_directories()

    report_df = generate_monitoring_report()

    print("AI model monitoring report generated successfully.")
    print(f"Prediction log: {PREDICTION_LOG_PATH}")
    print(f"Monitoring report: {MONITORING_REPORT_PATH}")
    print(f"Monitoring rows: {len(report_df)}")

    if PREDICTION_LOG_PATH.exists():
        log_df = load_prediction_log()
        print(f"Logged predictions: {len(log_df)}")


if __name__ == "__main__":
    main()