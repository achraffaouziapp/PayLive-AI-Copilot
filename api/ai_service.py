from typing import Any, Dict, List
from pathlib import Path
from src.ai.monitoring.monitor_predictions import (
    log_prediction,
    log_batch_predictions,
)

import pandas as pd

from src.ai.inference.intent_predictor import (
    predict_intent,
    predict_batch,
    get_model_info,
    get_model_metrics,
)


# -------------------------------------------------------------------
# AI service layer for PayLive AI Copilot API
# -------------------------------------------------------------------
# This file acts as a bridge between FastAPI routes and the trained
# intent prediction model.
# -------------------------------------------------------------------


BASE_DIR = Path(__file__).resolve().parents[1]

AI_REPORTS_DIR = BASE_DIR / "data" / "ai" / "reports"

MODEL_EVALUATION_REPORT_PATH = AI_REPORTS_DIR / "model_evaluation_report.csv"
MODEL_BENCHMARK_SELECTION_REPORT_PATH = (
    AI_REPORTS_DIR / "model_benchmark_selection_report.csv"
)

LOW_CONFIDENCE_THRESHOLD = 0.60


def add_prediction_status(prediction: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add a low-confidence flag to a prediction result.
    """
    confidence_score = float(prediction.get("confidence_score", 0.0))

    prediction["is_low_confidence"] = confidence_score < LOW_CONFIDENCE_THRESHOLD
    prediction["low_confidence_threshold"] = LOW_CONFIDENCE_THRESHOLD

    return prediction


def predict_single_comment(comment_text: str) -> Dict[str, Any]:
    """
    Predict the intent of a single comment and log the prediction.
    """
    prediction = predict_intent(comment_text)

    prediction = add_prediction_status(prediction)

    log_prediction(
        prediction=prediction,
        source="api_single",
    )

    return prediction


def predict_multiple_comments(comments: List[str]) -> Dict[str, Any]:
    """
    Predict intents for several comments and log predictions.
    """
    batch_result = predict_batch(comments)

    enriched_predictions = [
        add_prediction_status(prediction)
        for prediction in batch_result.get("predictions", [])
    ]

    batch_result["predictions"] = enriched_predictions
    batch_result["low_confidence_threshold"] = LOW_CONFIDENCE_THRESHOLD
    batch_result["low_confidence_count"] = sum(
        1 for prediction in enriched_predictions
        if prediction.get("is_low_confidence") is True
    )

    log_batch_predictions(
        batch_result=batch_result,
        source="api_batch",
    )

    return batch_result


def load_model_evaluation_metrics() -> Dict[str, Any]:
    """
    Load evaluation metrics from the model evaluation report if available.
    """
    if not MODEL_EVALUATION_REPORT_PATH.exists():
        return {
            "evaluation_report_available": False,
            "evaluation_report_path": str(MODEL_EVALUATION_REPORT_PATH),
            "metrics": [],
        }

    evaluation_df = pd.read_csv(MODEL_EVALUATION_REPORT_PATH)

    return {
        "evaluation_report_available": True,
        "evaluation_report_path": str(MODEL_EVALUATION_REPORT_PATH),
        "metrics": evaluation_df.to_dict(orient="records"),
    }


def load_benchmark_selection() -> Dict[str, Any]:
    """
    Load benchmark model selection report if available.
    """
    if not MODEL_BENCHMARK_SELECTION_REPORT_PATH.exists():
        return {
            "benchmark_selection_available": False,
            "benchmark_selection_report_path": str(
                MODEL_BENCHMARK_SELECTION_REPORT_PATH
            ),
            "selection": [],
        }

    selection_df = pd.read_csv(MODEL_BENCHMARK_SELECTION_REPORT_PATH)

    return {
        "benchmark_selection_available": True,
        "benchmark_selection_report_path": str(
            MODEL_BENCHMARK_SELECTION_REPORT_PATH
        ),
        "selection": selection_df.to_dict(orient="records"),
    }


def get_ai_model_information() -> Dict[str, Any]:
    """
    Return model information for the API.
    """
    model_info = get_model_info()
    benchmark_selection = load_benchmark_selection()

    return {
        "model": model_info,
        "benchmark_selection": benchmark_selection,
        "low_confidence_threshold": LOW_CONFIDENCE_THRESHOLD,
    }


def get_ai_model_metrics() -> Dict[str, Any]:
    """
    Return model metrics for the API.
    """
    metadata_metrics = get_model_metrics()
    evaluation_report = load_model_evaluation_metrics()
    benchmark_selection = load_benchmark_selection()

    return {
        "metadata_metrics": metadata_metrics,
        "evaluation_report": evaluation_report,
        "benchmark_selection": benchmark_selection,
        "low_confidence_threshold": LOW_CONFIDENCE_THRESHOLD,
    }