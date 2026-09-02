import csv
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

APP_MONITORING_DIR = Path("data/application_monitoring")
DEFAULT_METRICS_PATH = APP_MONITORING_DIR / "app_metrics.csv"
DEFAULT_ALERTS_PATH = APP_MONITORING_DIR / "app_alerts.csv"
DEFAULT_SUMMARY_PATH = APP_MONITORING_DIR / "app_summary.json"

LATENCY_WARNING_MS = 1000.0
HTTP_5XX_CRITICAL_PERCENT = 5.0

APP_ALERTS_HEADER = [
    "timestamp",
    "severity",
    "alert_type",
    "metric_value",
    "threshold",
    "message",
]


def load_metrics(path: Path = DEFAULT_METRICS_PATH) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def calculate_summary(rows: list[dict[str, str]]) -> dict[str, float | int]:
    request_count = len(rows)
    if request_count == 0:
        return {
            "request_count": 0,
            "average_latency_ms": 0.0,
            "max_latency_ms": 0.0,
            "http_5xx_count": 0,
            "http_5xx_rate_percent": 0.0,
            "api_error_count": 0,
        }

    latencies = [float(row.get("response_time_ms", 0) or 0) for row in rows]
    status_codes = [int(row.get("status_code", 0) or 0) for row in rows]

    http_5xx_count = sum(1 for code in status_codes if code >= 500)
    api_error_count = sum(1 for code in status_codes if code >= 400)

    return {
        "request_count": request_count,
        "average_latency_ms": round(sum(latencies) / request_count, 2),
        "max_latency_ms": round(max(latencies), 2),
        "http_5xx_count": http_5xx_count,
        "http_5xx_rate_percent": round((http_5xx_count / request_count) * 100, 2),
        "api_error_count": api_error_count,
    }


def probe_url(url: str, timeout: float = 5.0) -> bool:
    request = Request(url, headers={"User-Agent": "PayLive-Application-Monitoring/1.0"})
    try:
        with urlopen(request, timeout=timeout) as response:
            return 200 <= response.status < 400
    except (HTTPError, URLError, TimeoutError, OSError):
        return False


def build_alerts(
    summary: dict[str, float | int],
    api_available: bool,
    frontend_available: bool,
) -> list[dict[str, str]]:
    now = datetime.now(timezone.utc).isoformat()
    alerts: list[dict[str, str]] = []

    latency = float(summary.get("average_latency_ms", 0.0))
    rate_5xx = float(summary.get("http_5xx_rate_percent", 0.0))

    if latency > LATENCY_WARNING_MS:
        alerts.append({
            "timestamp": now,
            "severity": "WARNING",
            "alert_type": "APP_API_LATENCY_HIGH",
            "metric_value": f"{latency:.2f} ms",
            "threshold": f"> {LATENCY_WARNING_MS:.0f} ms",
            "message": "La latence HTTP moyenne de l'API dépasse 1000 ms.",
        })

    if rate_5xx > HTTP_5XX_CRITICAL_PERCENT:
        alerts.append({
            "timestamp": now,
            "severity": "CRITICAL",
            "alert_type": "APP_HTTP_5XX_RATE_HIGH",
            "metric_value": f"{rate_5xx:.2f} %",
            "threshold": f"> {HTTP_5XX_CRITICAL_PERCENT:.0f} %",
            "message": "Le taux de réponses HTTP 5xx dépasse 5 %.",
        })

    if not api_available:
        alerts.append({
            "timestamp": now,
            "severity": "CRITICAL",
            "alert_type": "APP_API_UNAVAILABLE",
            "metric_value": "unavailable",
            "threshold": "API available",
            "message": "L'API est indisponible.",
        })

    if not frontend_available:
        alerts.append({
            "timestamp": now,
            "severity": "CRITICAL",
            "alert_type": "APP_FRONTEND_UNAVAILABLE",
            "metric_value": "unavailable",
            "threshold": "Frontend available",
            "message": "Le frontend est indisponible.",
        })

    return alerts


def write_alerts(
    alerts: list[dict[str, str]],
    path: Path = DEFAULT_ALERTS_PATH,
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=APP_ALERTS_HEADER)
        writer.writeheader()
        writer.writerows(alerts)
    return path



def write_summary(
    result: dict[str, object],
    path: Path = DEFAULT_SUMMARY_PATH,
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    return path

def run_analysis(
    metrics_path: Path = DEFAULT_METRICS_PATH,
    alerts_path: Path = DEFAULT_ALERTS_PATH,
    summary_path: Path = DEFAULT_SUMMARY_PATH,
) -> dict[str, object]:
    rows = load_metrics(metrics_path)
    summary = calculate_summary(rows)

    api_url = os.getenv(
        "APPLICATION_MONITORING_API_URL",
        "http://127.0.0.1:8000/health",
    )
    frontend_url = os.getenv(
        "APPLICATION_MONITORING_FRONTEND_URL",
        "http://127.0.0.1:8080/",
    )

    api_available = probe_url(api_url)
    frontend_available = probe_url(frontend_url)

    alerts = build_alerts(summary, api_available, frontend_available)
    result: dict[str, object] = {
        **summary,
        "api_available": api_available,
        "frontend_available": frontend_available,
        "api_url": api_url,
        "frontend_url": frontend_url,
        "alerts": alerts,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }

    write_alerts(alerts, alerts_path)
    write_summary(result, summary_path)
    return result


def main() -> None:
    result = run_analysis()
    print("Application monitoring analysis")
    print(f"Requests: {result['request_count']}")
    print(f"Average latency: {result['average_latency_ms']} ms")
    print(f"HTTP 5xx rate: {result['http_5xx_rate_percent']} %")
    print(f"API errors: {result['api_error_count']}")
    print(f"API available: {result['api_available']}")
    print(f"Frontend available: {result['frontend_available']}")
    print(f"Alerts: {len(result['alerts'])}")


if __name__ == "__main__":
    main()
