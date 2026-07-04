from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional
import os
import sys
import time

import pandas as pd
import pytest
from fastapi.testclient import TestClient


# -------------------------------------------------------------------
# Automated API tests
# -------------------------------------------------------------------
# These tests validate the PayLive AI Copilot REST API.
#
# They check:
# - public endpoints;
# - protected endpoints without API key;
# - protected endpoints with invalid API key;
# - protected endpoints with valid API key;
# - PostgreSQL-backed routes;
# - analytics routes;
# - OpenAPI documentation availability.
#
# The tests generate a CSV report in data/processed/reports/api_tests/api_test_report.csv.
# -------------------------------------------------------------------


BASE_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_REPORTS_DIR = PROCESSED_DIR / "reports"
API_TEST_REPORTS_DIR = PROCESSED_REPORTS_DIR / "api_tests"

API_TEST_REPORT_PATH = API_TEST_REPORTS_DIR / "api_test_report.csv"

sys.path.insert(0, str(BASE_DIR))


try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


if load_dotenv is not None:
    load_dotenv(BASE_DIR / ".env")


from api.main import app  # noqa: E402


client = TestClient(app)

API_KEY = os.getenv("API_KEY", "paylive-dev-api-key")

VALID_HEADERS = {
    "X-API-Key": API_KEY,
}

INVALID_HEADERS = {
    "X-API-Key": "invalid-api-key",
}

API_TEST_RESULTS: List[Dict[str, Any]] = []


def get_current_timestamp() -> str:
    """
    Return the current timestamp.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def ensure_output_directory() -> None:
    """
    Create the output directory for the test report.
    """
    API_TEST_REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def safe_json(response) -> Any:
    """
    Return response JSON if available.
    """
    try:
        return response.json()
    except Exception:
        return None


def build_response_sample(json_body: Any, max_length: int = 500) -> str:
    """
    Build a short response sample for the CSV test report.
    """
    if json_body is None:
        return ""

    sample = str(json_body)

    if len(sample) > max_length:
        return sample[:max_length] + "..."

    return sample


def run_api_test(
    test_name: str,
    method: str,
    path: str,
    expected_status_code: int,
    headers: Optional[Dict[str, str]] = None,
    expected_response_type: Optional[str] = None,
    minimum_items: Optional[int] = None,
    required_keys: Optional[List[str]] = None,
) -> Any:
    """
    Run one API request and record the result.

    Parameters:
    - test_name: readable test name;
    - method: HTTP method;
    - path: API path;
    - expected_status_code: expected HTTP response code;
    - headers: optional request headers;
    - expected_response_type: list or dict;
    - minimum_items: minimum expected items for list responses;
    - required_keys: keys expected in the JSON body or first list item.
    """
    started = time.perf_counter()

    response = client.request(
        method=method,
        url=path,
        headers=headers or {},
    )

    duration_ms = round((time.perf_counter() - started) * 1000, 2)

    json_body = safe_json(response)

    issues = []

    if response.status_code != expected_status_code:
        issues.append(
            f"Expected status {expected_status_code}, got {response.status_code}."
        )

    if expected_response_type == "list" and not isinstance(json_body, list):
        issues.append("Expected response body to be a list.")

    if expected_response_type == "dict" and not isinstance(json_body, dict):
        issues.append("Expected response body to be a dictionary.")

    if minimum_items is not None:
        if not isinstance(json_body, list):
            issues.append("Minimum item count check requires a list response.")
        elif len(json_body) < minimum_items:
            issues.append(
                f"Expected at least {minimum_items} item(s), got {len(json_body)}."
            )

    if required_keys:
        if isinstance(json_body, list):
            if not json_body:
                issues.append("Cannot check required keys because response list is empty.")
            else:
                first_item = json_body[0]
                for key in required_keys:
                    if key not in first_item:
                        issues.append(f"Missing required key in first list item: {key}.")
        elif isinstance(json_body, dict):
            for key in required_keys:
                if key not in json_body:
                    issues.append(f"Missing required key in response body: {key}.")
        else:
            issues.append("Cannot check required keys because response body is invalid.")

    test_status = "success" if not issues else "failed"

    API_TEST_RESULTS.append(
        {
            "tested_at": get_current_timestamp(),
            "test_name": test_name,
            "method": method,
            "path": path,
            "expected_status_code": expected_status_code,
            "actual_status_code": response.status_code,
            "duration_ms": duration_ms,
            "status": test_status,
            "error_message": " | ".join(issues),
            "response_sample": build_response_sample(json_body),
        }
    )

    assert not issues, " | ".join(issues)

    return json_body


@pytest.fixture(scope="session", autouse=True)
def write_api_test_report_after_session():
    """
    Write the API test report after the pytest session.
    """
    ensure_output_directory()

    yield

    if API_TEST_RESULTS:
        report_df = pd.DataFrame(API_TEST_RESULTS)
        report_df.to_csv(API_TEST_REPORT_PATH, index=False, encoding="utf-8")


def test_root_endpoint_is_public():
    """
    Test the public root endpoint.
    """
    run_api_test(
        test_name="root_endpoint_is_public",
        method="GET",
        path="/",
        expected_status_code=200,
        expected_response_type="dict",
        required_keys=[
            "application",
            "version",
            "documentation_url",
            "health_url",
        ],
    )


def test_health_endpoint_is_public_and_database_available():
    """
    Test the public health endpoint.
    """
    response_body = run_api_test(
        test_name="health_endpoint_is_public",
        method="GET",
        path="/health",
        expected_status_code=200,
        expected_response_type="dict",
        required_keys=[
            "status",
            "application",
            "database_available",
            "database_name",
        ],
    )

    assert response_body["database_available"] is True
    assert response_body["database_name"] == "paylive_ai_copilot"


def test_openapi_documentation_is_available():
    """
    Test that OpenAPI documentation JSON is available.
    """
    run_api_test(
        test_name="openapi_documentation_is_available",
        method="GET",
        path="/openapi.json",
        expected_status_code=200,
        expected_response_type="dict",
        required_keys=[
            "openapi",
            "info",
            "paths",
        ],
    )


def test_protected_route_without_api_key_returns_401():
    """
    Test that protected routes reject requests without API key.
    """
    response_body = run_api_test(
        test_name="protected_route_without_api_key_returns_401",
        method="GET",
        path="/api/v1/sellers?limit=5&offset=0",
        expected_status_code=401,
        expected_response_type="dict",
        required_keys=["detail"],
    )

    assert "Missing API key" in response_body["detail"]


def test_protected_route_with_invalid_api_key_returns_403():
    """
    Test that protected routes reject invalid API keys.
    """
    response_body = run_api_test(
        test_name="protected_route_with_invalid_api_key_returns_403",
        method="GET",
        path="/api/v1/sellers?limit=5&offset=0",
        headers=INVALID_HEADERS,
        expected_status_code=403,
        expected_response_type="dict",
        required_keys=["detail"],
    )

    assert response_body["detail"] == "Invalid API key."


def test_list_sellers_with_valid_api_key():
    """
    Test the sellers listing endpoint with a valid API key.
    """
    run_api_test(
        test_name="list_sellers_with_valid_api_key",
        method="GET",
        path="/api/v1/sellers?limit=5&offset=0",
        headers=VALID_HEADERS,
        expected_status_code=200,
        expected_response_type="list",
        minimum_items=1,
        required_keys=[
            "seller_id",
            "shop_name",
            "country",
            "main_platform",
            "seller_status",
        ],
    )


def test_list_lives_with_valid_api_key():
    """
    Test the final live sales dataset endpoint.
    """
    run_api_test(
        test_name="list_lives_with_valid_api_key",
        method="GET",
        path="/api/v1/lives?limit=5&offset=0",
        headers=VALID_HEADERS,
        expected_status_code=200,
        expected_response_type="list",
        minimum_items=1,
        required_keys=[
            "live_id",
            "seller_id",
            "platform",
            "total_comments",
            "total_carts",
            "total_orders",
            "total_revenue",
            "final_dataset_status",
        ],
    )


def test_get_one_live_by_id_with_valid_api_key():
    """
    Test the live detail endpoint using a live_id returned by the list endpoint.
    """
    lives = run_api_test(
        test_name="get_one_live_by_id_prepare_live_id",
        method="GET",
        path="/api/v1/lives?limit=1&offset=0",
        headers=VALID_HEADERS,
        expected_status_code=200,
        expected_response_type="list",
        minimum_items=1,
        required_keys=["live_id"],
    )

    live_id = lives[0]["live_id"]

    run_api_test(
        test_name="get_one_live_by_id_with_valid_api_key",
        method="GET",
        path=f"/api/v1/lives/{live_id}",
        headers=VALID_HEADERS,
        expected_status_code=200,
        expected_response_type="dict",
        required_keys=[
            "live_id",
            "seller_id",
            "total_revenue",
            "final_dataset_status",
        ],
    )


def test_get_unknown_live_returns_404():
    """
    Test that an unknown live_id returns 404.
    """
    run_api_test(
        test_name="get_unknown_live_returns_404",
        method="GET",
        path="/api/v1/lives/UNKNOWN_LIVE_ID",
        headers=VALID_HEADERS,
        expected_status_code=404,
        expected_response_type="dict",
        required_keys=["detail"],
    )


def test_list_seller_lives_with_valid_api_key():
    """
    Test seller lives endpoint using a seller_id returned by the sellers endpoint.
    """
    sellers = run_api_test(
        test_name="list_seller_lives_prepare_seller_id",
        method="GET",
        path="/api/v1/sellers?limit=1&offset=0",
        headers=VALID_HEADERS,
        expected_status_code=200,
        expected_response_type="list",
        minimum_items=1,
        required_keys=["seller_id"],
    )

    seller_id = sellers[0]["seller_id"]

    run_api_test(
        test_name="list_seller_lives_with_valid_api_key",
        method="GET",
        path=f"/api/v1/sellers/{seller_id}/lives?limit=5&offset=0",
        headers=VALID_HEADERS,
        expected_status_code=200,
        expected_response_type="list",
    )


def test_seller_performance_summary_with_valid_api_key():
    """
    Test seller performance summary endpoint.
    """
    run_api_test(
        test_name="seller_performance_summary_with_valid_api_key",
        method="GET",
        path="/api/v1/sellers/summary/performance?limit=5",
        headers=VALID_HEADERS,
        expected_status_code=200,
        expected_response_type="list",
        minimum_items=1,
        required_keys=[
            "seller_id",
            "live_count",
            "total_revenue",
            "average_revenue",
            "average_conversion_rate",
        ],
    )


def test_top_lives_analytics_endpoint_with_valid_api_key():
    """
    Test top lives analytics endpoint.
    """
    run_api_test(
        test_name="top_lives_analytics_endpoint_with_valid_api_key",
        method="GET",
        path="/api/v1/analytics/top-lives?metric=total_revenue&limit=5",
        headers=VALID_HEADERS,
        expected_status_code=200,
        expected_response_type="list",
        minimum_items=1,
        required_keys=[
            "live_id",
            "total_revenue",
            "conversion_rate",
            "final_dataset_status",
        ],
    )


def test_platform_summary_endpoint_with_valid_api_key():
    """
    Test platform summary analytics endpoint.
    """
    run_api_test(
        test_name="platform_summary_endpoint_with_valid_api_key",
        method="GET",
        path="/api/v1/analytics/platform-summary",
        headers=VALID_HEADERS,
        expected_status_code=200,
        expected_response_type="list",
        minimum_items=1,
        required_keys=[
            "platform",
            "live_count",
            "total_revenue",
            "average_revenue",
            "average_conversion_rate",
            "total_comments",
            "total_carts",
            "total_orders",
        ],
    )


def test_conversion_insights_endpoint_with_valid_api_key():
    """
    Test conversion insights analytics endpoint.
    """
    run_api_test(
        test_name="conversion_insights_endpoint_with_valid_api_key",
        method="GET",
        path="/api/v1/analytics/conversion-insights?min_peak_viewers=1&limit=5",
        headers=VALID_HEADERS,
        expected_status_code=200,
        expected_response_type="list",
        minimum_items=1,
        required_keys=[
            "live_id",
            "conversion_rate",
            "peak_viewers",
            "total_revenue",
        ],
    )