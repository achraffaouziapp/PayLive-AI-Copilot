"""
Tests C15 — configuration CORS de la préproduction.

Ces tests doivent être ajoutés AVANT la modification de api/main.py.
Avec la configuration actuelle (origines="*" et méthodes GET uniquement),
ils doivent mettre en évidence que le frontend de préproduction ne peut
pas effectuer correctement un POST cross-origin vers predict-intent.
"""

import importlib

from fastapi.testclient import TestClient


PREPROD_ORIGIN = "https://paylive-ai-preprod.onrender.com"
UNTRUSTED_ORIGIN = "https://example.invalid"


def _make_client(monkeypatch, allowed_origins: str) -> TestClient:
    """
    Recharge api.main après définition de ALLOWED_ORIGINS afin de tester
    la configuration telle qu'elle sera utilisée en staging.
    """
    monkeypatch.setenv("ALLOWED_ORIGINS", allowed_origins)

    import api.main as main_module

    main_module = importlib.reload(main_module)
    return TestClient(main_module.app)


def test_preprod_origin_can_preflight_predict_post(monkeypatch):
    client = _make_client(monkeypatch, PREPROD_ORIGIN)

    response = client.options(
        "/api/v1/ai/predict-intent",
        headers={
            "Origin": PREPROD_ORIGIN,
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type,x-api-key",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == PREPROD_ORIGIN

    allowed_methods = response.headers.get("access-control-allow-methods", "")
    assert "POST" in allowed_methods

    allowed_headers = response.headers.get("access-control-allow-headers", "").lower()
    assert "x-api-key" in allowed_headers
    assert "content-type" in allowed_headers


def test_local_frontend_origin_can_be_configured(monkeypatch):
    origins = (
        "https://paylive-ai-preprod.onrender.com,"
        "http://127.0.0.1:8080,"
        "http://localhost:8080"
    )
    client = _make_client(monkeypatch, origins)

    response = client.options(
        "/api/v1/ai/predict-intent",
        headers={
            "Origin": "http://127.0.0.1:8080",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type,x-api-key",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://127.0.0.1:8080"


def test_untrusted_origin_is_not_allowed(monkeypatch):
    client = _make_client(monkeypatch, PREPROD_ORIGIN)

    response = client.options(
        "/api/v1/ai/predict-intent",
        headers={
            "Origin": UNTRUSTED_ORIGIN,
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type,x-api-key",
        },
    )

    assert response.status_code == 400
    assert response.headers.get("access-control-allow-origin") != UNTRUSTED_ORIGIN
