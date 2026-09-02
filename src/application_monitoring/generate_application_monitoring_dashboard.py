import csv
import html
import json
from datetime import datetime, timezone
from pathlib import Path

APP_MONITORING_DIR = Path("data/application_monitoring")
DEFAULT_SUMMARY_PATH = APP_MONITORING_DIR / "app_summary.json"
DEFAULT_ALERTS_PATH = APP_MONITORING_DIR / "app_alerts.csv"
DEFAULT_DASHBOARD_PATH = APP_MONITORING_DIR / "app_monitoring_dashboard.html"


def _read_alerts(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _availability_label(value: bool) -> str:
    return "Disponible" if value else "Indisponible"


def generate_dashboard(
    summary_path: Path = DEFAULT_SUMMARY_PATH,
    alerts_path: Path = DEFAULT_ALERTS_PATH,
    output_path: Path = DEFAULT_DASHBOARD_PATH,
) -> Path:
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    alerts = _read_alerts(alerts_path)

    alert_rows = "".join(
        f"""
        <tr>
          <td>{html.escape(alert['timestamp'])}</td>
          <td>{html.escape(alert['severity'])}</td>
          <td>{html.escape(alert['alert_type'])}</td>
          <td>{html.escape(alert['metric_value'])}</td>
          <td>{html.escape(alert['threshold'])}</td>
          <td>{html.escape(alert['message'])}</td>
        </tr>
        """
        for alert in alerts
    )

    if not alert_rows:
        alert_rows = '<tr><td colspan="6">Aucune alerte active.</td></tr>'

    generated_at = str(summary.get("generated_at") or datetime.now(timezone.utc).isoformat())

    document = f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Monitoring applicatif</title>
  <style>
    body {{ font-family: Arial, sans-serif; max-width: 1100px; margin: 0 auto; padding: 1rem; line-height: 1.5; }}
    .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; }}
    .metric {{ border: 1px solid #bbb; border-radius: 6px; padding: 1rem; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 1rem; }}
    th, td {{ border: 1px solid #bbb; padding: 0.6rem; text-align: left; vertical-align: top; }}
  </style>
</head>
<body>
  <main>
    <h1>Monitoring applicatif</h1>
    <p>Généré le {html.escape(generated_at)}</p>

    <section aria-labelledby="summary-title">
      <h2 id="summary-title">Synthèse</h2>
      <div class="metrics">
        <div class="metric"><strong>Disponibilité API</strong><br>{_availability_label(bool(summary['api_available']))}</div>
        <div class="metric"><strong>Disponibilité frontend</strong><br>{_availability_label(bool(summary['frontend_available']))}</div>
        <div class="metric"><strong>Nombre de requêtes</strong><br>{summary['request_count']}</div>
        <div class="metric"><strong>HTTP 5xx</strong><br>{summary['http_5xx_count']}</div>
        <div class="metric"><strong>Taux HTTP 5xx</strong><br>{summary['http_5xx_rate_percent']} %</div>
        <div class="metric"><strong>Latence HTTP moyenne</strong><br>{summary['average_latency_ms']} ms</div>
        <div class="metric"><strong>Latence HTTP maximale</strong><br>{summary['max_latency_ms']} ms</div>
        <div class="metric"><strong>Erreurs API</strong><br>{summary['api_error_count']}</div>
      </div>
    </section>

    <section aria-labelledby="alerts-title">
      <h2 id="alerts-title">Alertes actives</h2>
      <table>
        <caption>Alertes du monitoring applicatif</caption>
        <thead>
          <tr>
            <th scope="col">Horodatage</th>
            <th scope="col">Sévérité</th>
            <th scope="col">Type</th>
            <th scope="col">Valeur</th>
            <th scope="col">Seuil</th>
            <th scope="col">Message</th>
          </tr>
        </thead>
        <tbody>{alert_rows}</tbody>
      </table>
    </section>
  </main>
</body>
</html>
"""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(document, encoding="utf-8")
    return output_path


def main() -> None:
    output = generate_dashboard()
    print(f"Dashboard generated: {output}")


if __name__ == "__main__":
    main()
