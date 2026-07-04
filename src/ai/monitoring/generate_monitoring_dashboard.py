from pathlib import Path
from datetime import datetime
from html import escape

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[3]

AI_PREDICTIONS_DIR = BASE_DIR / "data" / "ai" / "predictions"
AI_REPORTS_DIR = BASE_DIR / "data" / "ai" / "reports"

PREDICTION_LOG_PATH = AI_PREDICTIONS_DIR / "ai_predictions_log.csv"
MONITORING_REPORT_PATH = AI_REPORTS_DIR / "model_monitoring_report.csv"
ALERTS_PATH = AI_REPORTS_DIR / "model_monitoring_alerts.csv"
DASHBOARD_PATH = AI_REPORTS_DIR / "model_monitoring_dashboard.html"

LOW_CONFIDENCE_THRESHOLD = 0.60
SLOW_RESPONSE_THRESHOLD_MS = 1000


def ensure_directories() -> None:
    AI_PREDICTIONS_DIR.mkdir(parents=True, exist_ok=True)
    AI_REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def safe_to_float(value, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def load_prediction_log() -> pd.DataFrame:
    if not PREDICTION_LOG_PATH.exists():
        return pd.DataFrame()

    try:
        return pd.read_csv(PREDICTION_LOG_PATH)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def normalize_predictions(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    normalized = df.copy()

    if "confidence_score" not in normalized.columns:
        normalized["confidence_score"] = 0.0

    if "response_time_ms" not in normalized.columns:
        normalized["response_time_ms"] = 0.0

    if "predicted_intent" not in normalized.columns:
        normalized["predicted_intent"] = "unknown"

    if "comment_text" not in normalized.columns:
        normalized["comment_text"] = ""

    if "source" not in normalized.columns:
        normalized["source"] = "unknown"

    if "model_version" not in normalized.columns:
        normalized["model_version"] = "unknown"

    if "timestamp" not in normalized.columns:
        normalized["timestamp"] = ""

    normalized["confidence_score"] = normalized["confidence_score"].apply(safe_to_float)
    normalized["response_time_ms"] = normalized["response_time_ms"].apply(safe_to_float)
    normalized["predicted_intent"] = normalized["predicted_intent"].fillna("unknown").astype(str)
    normalized["comment_text"] = normalized["comment_text"].fillna("").astype(str)
    normalized["source"] = normalized["source"].fillna("unknown").astype(str)
    normalized["model_version"] = normalized["model_version"].fillna("unknown").astype(str)
    normalized["timestamp"] = normalized["timestamp"].fillna("").astype(str)

    return normalized


def build_alerts(df: pd.DataFrame) -> pd.DataFrame:
    alerts = []

    if df.empty:
        alerts_df = pd.DataFrame(
            columns=[
                "generated_at",
                "timestamp",
                "source",
                "comment_text",
                "predicted_intent",
                "confidence_score",
                "response_time_ms",
                "model_version",
                "alert_type",
                "alert_level",
                "alert_message",
            ]
        )
        alerts_df.to_csv(ALERTS_PATH, index=False, encoding="utf-8")
        return alerts_df

    generated_at = datetime.now().isoformat(timespec="seconds")

    for _, row in df.iterrows():
        confidence_score = safe_to_float(row.get("confidence_score", 0.0))
        response_time_ms = safe_to_float(row.get("response_time_ms", 0.0))
        predicted_intent = str(row.get("predicted_intent", "unknown"))

        common_alert_data = {
            "generated_at": generated_at,
            "timestamp": row.get("timestamp", ""),
            "source": row.get("source", "unknown"),
            "comment_text": row.get("comment_text", ""),
            "predicted_intent": predicted_intent,
            "confidence_score": confidence_score,
            "response_time_ms": response_time_ms,
            "model_version": row.get("model_version", "unknown"),
        }

        if confidence_score < LOW_CONFIDENCE_THRESHOLD:
            alerts.append(
                {
                    **common_alert_data,
                    "alert_type": "LOW_CONFIDENCE",
                    "alert_level": "warning",
                    "alert_message": (
                        f"Score de confiance inférieur au seuil "
                        f"{LOW_CONFIDENCE_THRESHOLD:.2f}"
                    ),
                }
            )

        if response_time_ms > SLOW_RESPONSE_THRESHOLD_MS:
            alerts.append(
                {
                    **common_alert_data,
                    "alert_type": "SLOW_RESPONSE",
                    "alert_level": "warning",
                    "alert_message": (
                        f"Temps de réponse supérieur au seuil "
                        f"{SLOW_RESPONSE_THRESHOLD_MS} ms"
                    ),
                }
            )

        if predicted_intent.lower() == "unknown":
            alerts.append(
                {
                    **common_alert_data,
                    "alert_type": "UNKNOWN_INTENT",
                    "alert_level": "info",
                    "alert_message": "Intention prédite inconnue",
                }
            )

    alerts_df = pd.DataFrame(alerts)

    if alerts_df.empty:
        alerts_df = pd.DataFrame(
            columns=[
                "generated_at",
                "timestamp",
                "source",
                "comment_text",
                "predicted_intent",
                "confidence_score",
                "response_time_ms",
                "model_version",
                "alert_type",
                "alert_level",
                "alert_message",
            ]
        )

    alerts_df.to_csv(ALERTS_PATH, index=False, encoding="utf-8")
    return alerts_df


def compute_summary_metrics(df: pd.DataFrame, alerts_df: pd.DataFrame) -> dict:
    if df.empty:
        return {
            "total_predictions": 0,
            "avg_confidence": 0.0,
            "low_confidence_count": 0,
            "low_confidence_rate": 0.0,
            "avg_response_time_ms": 0.0,
            "unknown_intent_count": 0,
            "alerts_count": 0,
            "last_prediction_at": "N/A",
            "generated_at": datetime.now().isoformat(timespec="seconds"),
        }

    total_predictions = len(df)
    low_confidence_count = int((df["confidence_score"] < LOW_CONFIDENCE_THRESHOLD).sum())
    low_confidence_rate = (
        low_confidence_count / total_predictions if total_predictions > 0 else 0.0
    )
    unknown_intent_count = int((df["predicted_intent"].str.lower() == "unknown").sum())

    timestamps = df["timestamp"].dropna().astype(str)
    last_prediction_at = timestamps.max() if not timestamps.empty else "N/A"

    return {
        "total_predictions": total_predictions,
        "avg_confidence": round(float(df["confidence_score"].mean()), 4),
        "low_confidence_count": low_confidence_count,
        "low_confidence_rate": round(low_confidence_rate, 4),
        "avg_response_time_ms": round(float(df["response_time_ms"].mean()), 2),
        "unknown_intent_count": unknown_intent_count,
        "alerts_count": len(alerts_df),
        "last_prediction_at": last_prediction_at,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
    }


def dataframe_to_html_table(df: pd.DataFrame, max_rows: int = 20) -> str:
    if df.empty:
        return "<p>Aucune donnée disponible.</p>"

    display_df = df.head(max_rows).copy()

    rows = []
    header = "".join(f"<th>{escape(str(col))}</th>" for col in display_df.columns)
    rows.append(f"<tr>{header}</tr>")

    for _, row in display_df.iterrows():
        cells = "".join(f"<td>{escape(str(value))}</td>" for value in row.values)
        rows.append(f"<tr>{cells}</tr>")

    return f"<table>{''.join(rows)}</table>"


def build_distribution_table(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    if df.empty or column_name not in df.columns:
        return pd.DataFrame(columns=[column_name, "count", "percentage"])

    distribution = (
        df[column_name]
        .fillna("unknown")
        .astype(str)
        .value_counts()
        .reset_index()
    )
    distribution.columns = [column_name, "count"]
    distribution["percentage"] = (
        distribution["count"] / distribution["count"].sum() * 100
    ).round(2)

    return distribution


def get_health_status(summary: dict) -> tuple[str, str]:
    total_predictions = summary["total_predictions"]
    low_confidence_rate = summary["low_confidence_rate"]
    avg_response_time_ms = summary["avg_response_time_ms"]

    if total_predictions == 0:
        return "Aucune donnée", "Aucune prédiction n’a encore été journalisée."

    if low_confidence_rate >= 0.50:
        return "À surveiller", "Plus de 50% des prédictions ont une confiance faible."

    if avg_response_time_ms > SLOW_RESPONSE_THRESHOLD_MS:
        return "À surveiller", "Le temps de réponse moyen est supérieur au seuil défini."

    return "OK", "Le service IA fonctionne avec des métriques cohérentes."


def generate_dashboard_html(df: pd.DataFrame, alerts_df: pd.DataFrame, summary: dict) -> str:
    intent_distribution = build_distribution_table(df, "predicted_intent")
    source_distribution = build_distribution_table(df, "source")
    model_version_distribution = build_distribution_table(df, "model_version")

    low_confidence_examples = df[df["confidence_score"] < LOW_CONFIDENCE_THRESHOLD].copy()
    low_confidence_examples = low_confidence_examples[
        [
            "timestamp",
            "source",
            "comment_text",
            "predicted_intent",
            "confidence_score",
            "response_time_ms",
            "model_version",
        ]
    ].sort_values(by="confidence_score", ascending=True)

    recent_predictions = df.tail(20).copy()
    if not recent_predictions.empty:
        recent_predictions = recent_predictions[
            [
                "timestamp",
                "source",
                "comment_text",
                "predicted_intent",
                "confidence_score",
                "response_time_ms",
                "model_version",
            ]
        ]

    status_label, status_message = get_health_status(summary)

    html = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Dashboard Monitoring IA — PayLive AI Copilot</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 32px;
            background: #f6f8fa;
            color: #1f2937;
        }}
        h1, h2 {{
            color: #111827;
        }}
        .subtitle {{
            color: #4b5563;
            margin-bottom: 24px;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }}
        .card {{
            background: white;
            border-radius: 10px;
            padding: 18px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        }}
        .card-title {{
            font-size: 13px;
            color: #6b7280;
            margin-bottom: 8px;
        }}
        .card-value {{
            font-size: 28px;
            font-weight: bold;
        }}
        .status {{
            background: white;
            border-radius: 10px;
            padding: 18px;
            margin-bottom: 24px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            margin-bottom: 24px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        }}
        th, td {{
            border: 1px solid #e5e7eb;
            padding: 8px;
            text-align: left;
            font-size: 13px;
        }}
        th {{
            background: #eef2f7;
        }}
        .section {{
            margin-top: 32px;
        }}
        .footer {{
            margin-top: 40px;
            font-size: 12px;
            color: #6b7280;
        }}
        code {{
            background: #eef2f7;
            padding: 2px 4px;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
    <h1>Dashboard Monitoring IA — PayLive AI Copilot</h1>
    <p class="subtitle">
        Dashboard généré automatiquement à partir de <code>ai_predictions_log.csv</code>.
    </p>

    <div class="status">
        <h2>État global du service IA</h2>
        <p><strong>{escape(status_label)}</strong> — {escape(status_message)}</p>
        <p>Dernière prédiction journalisée : <strong>{escape(str(summary["last_prediction_at"]))}</strong></p>
        <p>Dashboard généré le : <strong>{escape(str(summary["generated_at"]))}</strong></p>
    </div>

    <div class="grid">
        <div class="card">
            <div class="card-title">Nombre total de prédictions</div>
            <div class="card-value">{summary["total_predictions"]}</div>
        </div>
        <div class="card">
            <div class="card-title">Confiance moyenne</div>
            <div class="card-value">{summary["avg_confidence"]}</div>
        </div>
        <div class="card">
            <div class="card-title">Prédictions faible confiance</div>
            <div class="card-value">{summary["low_confidence_count"]}</div>
        </div>
        <div class="card">
            <div class="card-title">Alertes générées</div>
            <div class="card-value">{summary["alerts_count"]}</div>
        </div>
    </div>

    <div class="grid">
        <div class="card">
            <div class="card-title">Taux faible confiance</div>
            <div class="card-value">{round(summary["low_confidence_rate"] * 100, 2)}%</div>
        </div>
        <div class="card">
            <div class="card-title">Temps moyen de réponse</div>
            <div class="card-value">{summary["avg_response_time_ms"]} ms</div>
        </div>
        <div class="card">
            <div class="card-title">Intentions inconnues</div>
            <div class="card-value">{summary["unknown_intent_count"]}</div>
        </div>
        <div class="card">
            <div class="card-title">Seuil faible confiance</div>
            <div class="card-value">{LOW_CONFIDENCE_THRESHOLD}</div>
        </div>
    </div>

    <div class="section">
        <h2>Répartition des intentions prédites</h2>
        {dataframe_to_html_table(intent_distribution)}
    </div>

    <div class="section">
        <h2>Répartition par source</h2>
        {dataframe_to_html_table(source_distribution)}
    </div>

    <div class="section">
        <h2>Répartition par version de modèle</h2>
        {dataframe_to_html_table(model_version_distribution)}
    </div>

    <div class="section">
        <h2>Alertes générées</h2>
        <p>
            Les alertes sont aussi exportées dans :
            <code>data/ai/reports/model_monitoring_alerts.csv</code>
        </p>
        {dataframe_to_html_table(alerts_df, max_rows=30)}
    </div>

    <div class="section">
        <h2>Exemples de prédictions à faible confiance</h2>
        {dataframe_to_html_table(low_confidence_examples, max_rows=20)}
    </div>

    <div class="section">
        <h2>Dernières prédictions journalisées</h2>
        {dataframe_to_html_table(recent_predictions, max_rows=20)}
    </div>

    <div class="footer">
        <p>
            Ce dashboard correspond à un monitoring IA léger.
            Il permet de suivre les prédictions, les scores de confiance,
            les temps de réponse et les alertes principales du service IA.
        </p>
    </div>
</body>
</html>
"""
    return html


def save_dashboard(html_content: str) -> None:
    DASHBOARD_PATH.write_text(html_content, encoding="utf-8")


def main() -> None:
    ensure_directories()

    predictions_df = load_prediction_log()
    predictions_df = normalize_predictions(predictions_df)

    alerts_df = build_alerts(predictions_df)
    summary = compute_summary_metrics(predictions_df, alerts_df)

    html_content = generate_dashboard_html(predictions_df, alerts_df, summary)
    save_dashboard(html_content)

    print("Dashboard monitoring IA généré avec succès.")
    print(f"Fichier dashboard : {DASHBOARD_PATH}")
    print(f"Fichier alertes   : {ALERTS_PATH}")


if __name__ == "__main__":
    main()