from pathlib import Path
import sys

import pandas as pd
import pytest


# -------------------------------------------------------------------
# Intent model tests for PayLive AI Copilot
# -------------------------------------------------------------------


BASE_DIR = Path(__file__).resolve().parents[1]

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


from src.ai.inference.intent_predictor import (
    load_model_artifacts,
    predict_intent,
    predict_batch,
    get_model_info,
    get_model_metrics,
)


MODEL_DIR = BASE_DIR / "models" / "intent_classifier"
AI_REPORTS_DIR = BASE_DIR / "data" / "ai" / "reports"

MODEL_PATH = MODEL_DIR / "model.joblib"
VECTORIZER_PATH = MODEL_DIR / "vectorizer.joblib"
LABEL_ENCODER_PATH = MODEL_DIR / "label_encoder.joblib"
MODEL_METADATA_PATH = MODEL_DIR / "model_metadata.json"

MODEL_TRAINING_REPORT_PATH = AI_REPORTS_DIR / "model_training_report.csv"
MODEL_EVALUATION_REPORT_PATH = AI_REPORTS_DIR / "model_evaluation_report.csv"
CLASSIFICATION_REPORT_PATH = AI_REPORTS_DIR / "classification_report.csv"
CONFUSION_MATRIX_PATH = AI_REPORTS_DIR / "confusion_matrix.csv"

TEST_REPORT_PATH = AI_REPORTS_DIR / "intent_model_test_report.csv"

ALLOWED_INTENT_LABELS = {
    "purchase_intent",
    "product_question",
    "payment_question",
    "shipping_question",
    "other",
    "unknown",
}


test_results = []


def add_test_result(test_name: str, status: str, details: str = "") -> None:
    """
    Store test execution result for CSV reporting.
    """
    test_results.append(
        {
            "test_name": test_name,
            "status": status,
            "details": details,
        }
    )


def save_test_report() -> None:
    """
    Save intent model test report.
    """
    AI_REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(test_results).to_csv(
        TEST_REPORT_PATH,
        index=False,
        encoding="utf-8",
    )


def test_model_artifacts_exist():
    """
    Check that trained model artifacts exist.
    """
    expected_files = [
        MODEL_PATH,
        VECTORIZER_PATH,
        LABEL_ENCODER_PATH,
        MODEL_METADATA_PATH,
    ]

    missing_files = [str(path) for path in expected_files if not path.exists()]

    assert not missing_files, f"Missing model artifacts: {missing_files}"

    add_test_result(
        "test_model_artifacts_exist",
        "passed",
        "All model artifacts exist.",
    )


def test_model_reports_exist():
    """
    Check that training and evaluation reports exist.
    """
    expected_files = [
        MODEL_TRAINING_REPORT_PATH,
        MODEL_EVALUATION_REPORT_PATH,
        CLASSIFICATION_REPORT_PATH,
        CONFUSION_MATRIX_PATH,
    ]

    missing_files = [str(path) for path in expected_files if not path.exists()]

    assert not missing_files, f"Missing model reports: {missing_files}"

    add_test_result(
        "test_model_reports_exist",
        "passed",
        "All model reports exist.",
    )


def test_model_artifacts_can_be_loaded():
    """
    Check that model artifacts can be loaded.
    """
    artifacts = load_model_artifacts(force_reload=True)

    assert "model" in artifacts
    assert "vectorizer" in artifacts
    assert "label_encoder" in artifacts
    assert "metadata" in artifacts

    add_test_result(
        "test_model_artifacts_can_be_loaded",
        "passed",
        "Model, vectorizer, label encoder and metadata loaded.",
    )


def test_single_prediction_format():
    """
    Check that a single prediction returns the expected format.
    """
    prediction = predict_intent("je prends la robe noire en M")

    expected_keys = {
        "comment_text",
        "predicted_intent",
        "confidence_score",
        "model_name",
        "model_version",
        "response_time_ms",
    }

    missing_keys = expected_keys - set(prediction.keys())

    assert not missing_keys, f"Missing prediction keys: {missing_keys}"
    assert prediction["predicted_intent"] in ALLOWED_INTENT_LABELS
    assert 0 <= float(prediction["confidence_score"]) <= 1
    assert float(prediction["response_time_ms"]) >= 0

    add_test_result(
        "test_single_prediction_format",
        "passed",
        f"Prediction: {prediction}",
    )


def test_purchase_intent_prediction():
    """
    Check that a clear purchase comment is predicted as purchase intent.
    """
    prediction = predict_intent("je prends le pull rouge en M")

    assert prediction["predicted_intent"] == "purchase_intent"

    add_test_result(
        "test_purchase_intent_prediction",
        "passed",
        f"Predicted intent: {prediction['predicted_intent']}",
    )


def test_payment_question_prediction():
    """
    Check that a payment question can be classified.
    """
    prediction = predict_intent("comment payer ?")

    assert prediction["predicted_intent"] in ALLOWED_INTENT_LABELS

    add_test_result(
        "test_payment_question_prediction",
        "passed",
        f"Predicted intent: {prediction['predicted_intent']}",
    )


def test_empty_comment_raises_value_error():
    """
    Check that empty comments are rejected.
    """
    with pytest.raises(ValueError):
        predict_intent("   ")

    add_test_result(
        "test_empty_comment_raises_value_error",
        "passed",
        "Empty comment raises ValueError.",
    )


def test_batch_prediction_format():
    """
    Check that batch prediction returns the expected format.
    """
    result = predict_batch(
        [
            "je prends le pull rouge en M",
            "comment payer ?",
            "vous livrez en Belgique ?",
            "trop beau",
        ]
    )

    assert "prediction_count" in result
    assert "total_response_time_ms" in result
    assert "predictions" in result
    assert result["prediction_count"] == 4
    assert len(result["predictions"]) == 4

    for prediction in result["predictions"]:
        assert prediction["predicted_intent"] in ALLOWED_INTENT_LABELS
        assert 0 <= float(prediction["confidence_score"]) <= 1

    add_test_result(
        "test_batch_prediction_format",
        "passed",
        f"Batch prediction count: {result['prediction_count']}",
    )


def test_model_info_format():
    """
    Check model information format.
    """
    model_info = get_model_info()

    expected_keys = {
        "model_name",
        "model_version",
        "algorithm",
        "classes",
        "test_accuracy",
        "test_macro_f1",
        "test_weighted_f1",
    }

    missing_keys = expected_keys - set(model_info.keys())

    assert not missing_keys, f"Missing model info keys: {missing_keys}"
    assert isinstance(model_info["classes"], list)

    add_test_result(
        "test_model_info_format",
        "passed",
        f"Model version: {model_info.get('model_version')}",
    )


def test_model_metrics_format():
    """
    Check model metrics format.
    """
    metrics = get_model_metrics()

    expected_keys = {
        "model_name",
        "model_version",
        "test_accuracy",
        "test_macro_f1",
        "test_weighted_f1",
    }

    missing_keys = expected_keys - set(metrics.keys())

    assert not missing_keys, f"Missing metric keys: {missing_keys}"

    add_test_result(
        "test_model_metrics_format",
        "passed",
        f"Metrics: {metrics}",
    )


def test_model_test_report_is_saved():
    """
    Save test report at the end of model tests.
    """
    add_test_result(
        "test_model_test_report_is_saved",
        "passed",
        f"Report saved to {TEST_REPORT_PATH}",
    )

    save_test_report()

    assert TEST_REPORT_PATH.exists(), "Intent model test report was not saved."