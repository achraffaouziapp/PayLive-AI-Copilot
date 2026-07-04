from pathlib import Path
import os
import sys

import pandas as pd
from fastapi.testclient import TestClient


# -------------------------------------------------------------------
# AI API tests for PayLive AI Copilot
# -------------------------------------------------------------------


BASE_DIR = Path(__file__).resolve().parents[1]

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


os.environ.setdefault("API_KEY", "paylive-dev-api-key")

from api.main import app


AI_REPORTS_DIR = BASE_DIR / "data" / "ai" / "reports"
TEST_REPORT_PATH = AI_REPORTS_DIR / "ai_api_test_report.csv"

VALID_API_KEY = os.getenv("API_KEY", "paylive-dev-api-key")
INVALID_API_KEY = "invalid-api-key"

client = TestClient(app)

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
    Save AI API test report.
    """
    AI_REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(test_results).to_csv(
        TEST_REPORT_PATH,
        index=False,
        encoding="utf-8",
    )


def get_valid_headers() -> dict:
    """
    Return valid API key header.
    """
    return {"X-API-Key": VALID_API_KEY}


def get_invalid_headers() -> dict:
    """
    Return invalid API key header.
    """
    return {"X-API-Key": INVALID_API_KEY}


def test_ai_predict_without_api_key_returns_401():
    """
    Check that prediction route rejects missing API key.
    """
    response = client.post(
        "/api/v1/ai/predict-intent",
        json={"comment_text": "je prends le pull rouge en M"},
    )

    assert response.status_code == 401

    add_test_result(
        "test_ai_predict_without_api_key_returns_401",
        "passed",
        "Missing API key returns 401.",
    )


def test_ai_predict_with_invalid_api_key_returns_403():
    """
    Check that prediction route rejects invalid API key.
    """
    response = client.post(
        "/api/v1/ai/predict-intent",
        headers=get_invalid_headers(),
        json={"comment_text": "je prends le pull rouge en M"},
    )

    assert response.status_code == 403

    add_test_result(
        "test_ai_predict_with_invalid_api_key_returns_403",
        "passed",
        "Invalid API key returns 403.",
    )


def test_ai_predict_with_valid_api_key_returns_prediction():
    """
    Check that prediction route returns a valid prediction.
    """
    response = client.post(
        "/api/v1/ai/predict-intent",
        headers=get_valid_headers(),
        json={"comment_text": "je prends le pull rouge en M"},
    )

    assert response.status_code == 200

    payload = response.json()

    expected_keys = {
        "comment_text",
        "predicted_intent",
        "confidence_score",
        "model_name",
        "model_version",
        "response_time_ms",
        "is_low_confidence",
        "low_confidence_threshold",
    }

    missing_keys = expected_keys - set(payload.keys())

    assert not missing_keys, f"Missing keys: {missing_keys}"
    assert payload["predicted_intent"] in {
        "purchase_intent",
        "product_question",
        "payment_question",
        "shipping_question",
        "other",
        "unknown",
    }
    assert 0 <= float(payload["confidence_score"]) <= 1

    add_test_result(
        "test_ai_predict_with_valid_api_key_returns_prediction",
        "passed",
        f"Prediction payload: {payload}",
    )


def test_ai_predict_empty_comment_returns_400():
    """
    Check that empty comment is rejected.
    """
    response = client.post(
        "/api/v1/ai/predict-intent",
        headers=get_valid_headers(),
        json={"comment_text": "   "},
    )

    assert response.status_code == 400

    add_test_result(
        "test_ai_predict_empty_comment_returns_400",
        "passed",
        "Empty comment returns 400.",
    )


def test_ai_batch_prediction_returns_predictions():
    """
    Check batch prediction route.
    """
    response = client.post(
        "/api/v1/ai/batch-predict-intents",
        headers=get_valid_headers(),
        json={
            "comments": [
                "je prends le pull rouge en M",
                "comment payer ?",
                "vous livrez en Belgique ?",
                "trop beau",
            ]
        },
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["prediction_count"] == 4
    assert "predictions" in payload
    assert len(payload["predictions"]) == 4
    assert "low_confidence_count" in payload

    add_test_result(
        "test_ai_batch_prediction_returns_predictions",
        "passed",
        f"Batch prediction count: {payload['prediction_count']}",
    )


def test_ai_batch_empty_list_returns_400():
    """
    Check that empty batch is rejected.
    """
    response = client.post(
        "/api/v1/ai/batch-predict-intents",
        headers=get_valid_headers(),
        json={"comments": []},
    )

    assert response.status_code == 400

    add_test_result(
        "test_ai_batch_empty_list_returns_400",
        "passed",
        "Empty batch returns 400.",
    )


def test_ai_model_info_route_returns_model_info():
    """
    Check model-info route.
    """
    response = client.get(
        "/api/v1/ai/model-info",
        headers=get_valid_headers(),
    )

    assert response.status_code == 200

    payload = response.json()

    assert "model" in payload
    assert "benchmark_selection" in payload
    assert "low_confidence_threshold" in payload
    assert "model_name" in payload["model"]
    assert "model_version" in payload["model"]

    add_test_result(
        "test_ai_model_info_route_returns_model_info",
        "passed",
        f"Model info: {payload['model'].get('model_version')}",
    )


def test_ai_model_metrics_route_returns_metrics():
    """
    Check model-metrics route.
    """
    response = client.get(
        "/api/v1/ai/model-metrics",
        headers=get_valid_headers(),
    )

    assert response.status_code == 200

    payload = response.json()

    assert "metadata_metrics" in payload
    assert "evaluation_report" in payload
    assert "benchmark_selection" in payload
    assert "low_confidence_threshold" in payload

    add_test_result(
        "test_ai_model_metrics_route_returns_metrics",
        "passed",
        "Model metrics route returned expected structure.",
    )


def test_ai_openapi_contains_ai_routes():
    """
    Check that AI routes are visible in OpenAPI schema.
    """
    response = client.get("/openapi.json")

    assert response.status_code == 200

    schema = response.json()
    paths = schema.get("paths", {})

    assert "/api/v1/ai/predict-intent" in paths
    assert "/api/v1/ai/batch-predict-intents" in paths
    assert "/api/v1/ai/model-info" in paths
    assert "/api/v1/ai/model-metrics" in paths

    add_test_result(
        "test_ai_openapi_contains_ai_routes",
        "passed",
        "AI routes are present in OpenAPI schema.",
    )


def test_ai_api_test_report_is_saved():
    """
    Save test report at the end of API tests.
    """
    add_test_result(
        "test_ai_api_test_report_is_saved",
        "passed",
        f"Report saved to {TEST_REPORT_PATH}",
    )

    save_test_report()

    assert TEST_REPORT_PATH.exists(), "AI API test report was not saved."