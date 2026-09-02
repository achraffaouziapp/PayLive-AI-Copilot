from src.application_monitoring.analyze_application_monitoring import (
    build_alerts,
    calculate_summary,
)


def test_summary_calculates_required_metrics():
    rows = [
        {"status_code": "200", "response_time_ms": "100", "is_5xx": "false", "error_type": ""},
        {"status_code": "404", "response_time_ms": "200", "is_5xx": "false", "error_type": ""},
        {"status_code": "500", "response_time_ms": "300", "is_5xx": "true", "error_type": "RuntimeError"},
    ]
    summary = calculate_summary(rows)
    assert summary["request_count"] == 3
    assert summary["average_latency_ms"] == 200.0
    assert summary["max_latency_ms"] == 300.0
    assert summary["http_5xx_count"] == 1
    assert summary["http_5xx_rate_percent"] == 33.33
    assert summary["api_error_count"] == 2


def test_latency_above_1000ms_creates_warning():
    alerts = build_alerts(
        {"average_latency_ms": 1200.0, "http_5xx_rate_percent": 0.0},
        api_available=True,
        frontend_available=True,
    )
    assert any(a["alert_type"] == "APP_API_LATENCY_HIGH" and a["severity"] == "WARNING" for a in alerts)


def test_5xx_rate_above_5_percent_creates_critical():
    alerts = build_alerts(
        {"average_latency_ms": 100.0, "http_5xx_rate_percent": 6.0},
        api_available=True,
        frontend_available=True,
    )
    assert any(a["alert_type"] == "APP_HTTP_5XX_RATE_HIGH" and a["severity"] == "CRITICAL" for a in alerts)


def test_unavailable_api_creates_critical():
    alerts = build_alerts(
        {"average_latency_ms": 100.0, "http_5xx_rate_percent": 0.0},
        api_available=False,
        frontend_available=True,
    )
    assert any(a["alert_type"] == "APP_API_UNAVAILABLE" and a["severity"] == "CRITICAL" for a in alerts)


def test_unavailable_frontend_creates_critical():
    alerts = build_alerts(
        {"average_latency_ms": 100.0, "http_5xx_rate_percent": 0.0},
        api_available=True,
        frontend_available=False,
    )
    assert any(a["alert_type"] == "APP_FRONTEND_UNAVAILABLE" and a["severity"] == "CRITICAL" for a in alerts)


def test_summary_snapshot_is_written_as_json(tmp_path):
    import json
    from src.application_monitoring.analyze_application_monitoring import write_summary

    path = tmp_path / "app_summary.json"
    result = {
        "request_count": 3,
        "average_latency_ms": 120.0,
        "max_latency_ms": 180.0,
        "http_5xx_count": 0,
        "http_5xx_rate_percent": 0.0,
        "api_error_count": 0,
        "api_available": True,
        "frontend_available": True,
        "alerts": [],
    }
    write_summary(result, path)
    stored = json.loads(path.read_text(encoding="utf-8"))
    assert stored["request_count"] == 3
    assert stored["api_available"] is True
