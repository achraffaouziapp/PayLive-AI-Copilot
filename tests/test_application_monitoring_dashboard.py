import csv
import json

from src.application_monitoring.generate_application_monitoring_dashboard import generate_dashboard


def test_dashboard_contains_required_application_metrics(tmp_path):
    summary_path = tmp_path / "app_summary.json"
    alerts_path = tmp_path / "app_alerts.csv"
    output_path = tmp_path / "app_monitoring_dashboard.html"

    summary_path.write_text(json.dumps({
        "request_count": 10,
        "average_latency_ms": 120.5,
        "max_latency_ms": 800.0,
        "http_5xx_count": 1,
        "http_5xx_rate_percent": 10.0,
        "api_error_count": 2,
        "api_available": True,
        "frontend_available": True,
        "alerts": [],
    }), encoding="utf-8")

    with alerts_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=[
            "timestamp", "severity", "alert_type", "metric_value", "threshold", "message"
        ])
        writer.writeheader()
        writer.writerow({
            "timestamp": "2026-09-02T00:00:00+00:00",
            "severity": "CRITICAL",
            "alert_type": "APP_HTTP_5XX_RATE_HIGH",
            "metric_value": "10.00 %",
            "threshold": ">5 %",
            "message": "Le taux de réponses HTTP 5xx dépasse 5 %.",
        })

    generate_dashboard(summary_path, alerts_path, output_path)
    html = output_path.read_text(encoding="utf-8")

    assert "Monitoring applicatif" in html
    assert "Disponibilité API" in html
    assert "Disponibilité frontend" in html
    assert "Nombre de requêtes" in html
    assert "Taux HTTP 5xx" in html
    assert "Latence HTTP moyenne" in html
    assert "Erreurs API" in html
    assert "APP_HTTP_5XX_RATE_HIGH" in html
    assert "<table" in html
    assert "<caption>" in html
