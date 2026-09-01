"""
Tests E2E de l'intégration frontend -> API IA.

Pré-requis :
- l'application Docker est démarrée ;
- le frontend est accessible (par défaut : http://127.0.0.1:8080) ;
- l'API IA est accessible derrière le proxy Nginx ;
- le modèle IA est chargé.

Variables d'environnement optionnelles :
- PAYLIVE_FRONTEND_URL
- PAYLIVE_API_KEY

Exécution :
    pytest tests\\e2e\\test_frontend_ai.py -v

Mode navigateur visible :
    pytest tests\\e2e\\test_frontend_ai.py -v --headed --browser chromium
"""

import json
import os
import re

import pytest
from playwright.sync_api import Page, expect


FRONTEND_URL = os.getenv("PAYLIVE_FRONTEND_URL", "http://127.0.0.1:8080")
VALID_API_KEY = os.getenv("PAYLIVE_API_KEY", "paylive-dev-api-key")
INVALID_API_KEY = "invalid-e2e-api-key"


@pytest.fixture(autouse=True)
def configure_page(page: Page) -> None:
    """Prépare une page propre avant chaque scénario E2E."""
    page.set_default_timeout(10_000)
    page.goto(FRONTEND_URL, wait_until="domcontentloaded")

    # Vérifie immédiatement que le frontend attendu est bien chargé.
    expect(page.locator("h1")).to_have_text("PayLive AI Copilot")
    expect(page.locator("#apiBaseUrl")).to_have_value("/api/v1/ai")


def set_api_key(page: Page, api_key: str) -> None:
    """Renseigne la clé API utilisée par les appels JavaScript du frontend."""
    page.locator("#apiKey").fill(api_key)


def test_protected_connection_with_valid_api_key(page: Page) -> None:
    """Le frontend doit valider une vraie route protégée avec une clé correcte."""
    set_api_key(page, VALID_API_KEY)

    with page.expect_response(
        lambda response: response.url.endswith("/api/v1/ai/model-info")
    ) as response_info:
        page.locator("#healthBtn").click()

    response = response_info.value
    assert response.status == 200

    expect(page.locator("#connectionStatus")).to_have_text(
        "API IA disponible et clé API valide."
    )


def test_invalid_api_key_is_rejected(page: Page) -> None:
    """Une mauvaise clé doit être refusée par l'API et affichée dans l'interface."""
    set_api_key(page, INVALID_API_KEY)

    with page.expect_response(
        lambda response: response.url.endswith("/api/v1/ai/model-info")
    ) as response_info:
        page.locator("#healthBtn").click()

    response = response_info.value
    assert response.status == 403

    expect(page.locator("#connectionStatus")).to_contain_text(
        "Clé API invalide."
    )


def test_predict_intent_from_frontend(page: Page) -> None:
    """Un commentaire saisi dans l'interface doit traverser l'API et afficher une prédiction."""
    set_api_key(page, VALID_API_KEY)
    page.locator("#commentText").fill("je prends la robe noire en M")

    with page.expect_response(
        lambda response: response.url.endswith("/api/v1/ai/predict-intent")
    ) as response_info:
        page.locator("#predictBtn").click()

    response = response_info.value
    assert response.status == 200

    prediction = page.locator("#predictionResult")
    expect(prediction).to_be_visible()

    intent = page.locator("#predictedIntent").inner_text().strip()
    confidence_text = page.locator("#confidenceScore").inner_text().strip()
    response_time_text = page.locator("#responseTime").inner_text().strip()
    model_version = page.locator("#modelVersion").inner_text().strip()

    assert intent not in {"", "-"}
    assert re.fullmatch(r"\d+\.\d{4}", confidence_text), confidence_text

    confidence = float(confidence_text)
    assert 0.0 <= confidence <= 1.0

    assert re.fullmatch(r"\d+(?:\.\d+)? ms", response_time_text), response_time_text
    assert model_version not in {"", "-"}


def test_model_info_from_frontend(page: Page) -> None:
    """Le bouton Informations modèle doit consommer /model-info et afficher du JSON."""
    set_api_key(page, VALID_API_KEY)

    with page.expect_response(
        lambda response: response.url.endswith("/api/v1/ai/model-info")
    ) as response_info:
        page.locator("#modelInfoBtn").click()

    response = response_info.value
    assert response.status == 200

    output = page.locator("#modelInfoOutput")
    expect(output).not_to_have_text("Chargement...")

    raw_text = output.inner_text().strip()
    assert raw_text
    data = json.loads(raw_text)
    assert isinstance(data, dict)
    assert data


def test_model_metrics_from_frontend(page: Page) -> None:
    """Le bouton Métriques doit consommer /model-metrics et afficher du JSON."""
    set_api_key(page, VALID_API_KEY)

    with page.expect_response(
        lambda response: response.url.endswith("/api/v1/ai/model-metrics")
    ) as response_info:
        page.locator("#modelMetricsBtn").click()

    response = response_info.value
    assert response.status == 200

    output = page.locator("#modelMetricsOutput")
    expect(output).not_to_have_text("Chargement...")

    raw_text = output.inner_text().strip()
    assert raw_text
    data = json.loads(raw_text)
    assert isinstance(data, dict)
    assert data


def test_monitoring_dashboard_from_frontend(page: Page) -> None:
    """Le frontend doit récupérer le dashboard HTML via l'endpoint protégé."""
    set_api_key(page, VALID_API_KEY)

    with page.expect_response(
        lambda response: response.url.endswith("/api/v1/ai/monitoring/dashboard")
    ) as response_info:
        page.locator("#openDashboardBtn").click()

    response = response_info.value
    assert response.status == 200

    content_type = response.headers.get("content-type", "")
    assert "text/html" in content_type.lower()

    expect(page.locator("#monitoringStatus")).to_have_text(
        "Dashboard ouvert dans un nouvel onglet."
    )


def test_monitoring_alerts_from_frontend(page: Page) -> None:
    """Le frontend doit récupérer /monitoring/alerts et déclencher le téléchargement CSV."""
    set_api_key(page, VALID_API_KEY)

    with page.expect_response(
        lambda response: response.url.endswith("/api/v1/ai/monitoring/alerts")
    ) as response_info:
        with page.expect_download() as download_info:
            page.locator("#downloadAlertsBtn").click()

    response = response_info.value
    download = download_info.value

    assert response.status == 200
    assert download.suggested_filename == "model_monitoring_alerts.csv"

    expect(page.locator("#monitoringStatus")).to_have_text(
        "Alertes téléchargées."
    )
