import csv
import importlib

from fastapi import FastAPI
from fastapi.testclient import TestClient


def _load_monitoring_module(monkeypatch, tmp_path):
    metrics_path = tmp_path / "app_metrics.csv"
    monkeypatch.setenv("APPLICATION_MONITORING_METRICS_PATH", str(metrics_path))

    import api.application_monitoring as module
    module = importlib.reload(module)
    return module, metrics_path


def test_successful_request_is_written_to_metrics_csv(monkeypatch, tmp_path):
    module, metrics_path = _load_monitoring_module(monkeypatch, tmp_path)
    app = FastAPI()
    app.middleware("http")(module.application_monitoring_middleware)

    @app.get("/ok")
    def ok():
        return {"status": "ok"}

    response = TestClient(app).get("/ok")
    assert response.status_code == 200

    with metrics_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 1
    assert rows[0]["method"] == "GET"
    assert rows[0]["path"] == "/ok"
    assert rows[0]["status_code"] == "200"
    assert rows[0]["is_5xx"] == "false"
    assert float(rows[0]["response_time_ms"]) >= 0


def test_5xx_response_is_flagged(monkeypatch, tmp_path):
    module, metrics_path = _load_monitoring_module(monkeypatch, tmp_path)
    app = FastAPI()
    app.middleware("http")(module.application_monitoring_middleware)

    @app.get("/failure")
    def failure():
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"detail": "failure"})

    response = TestClient(app).get("/failure")
    assert response.status_code == 500

    with metrics_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    assert rows[0]["status_code"] == "500"
    assert rows[0]["is_5xx"] == "true"


def test_unhandled_exception_is_logged(monkeypatch, tmp_path):
    module, metrics_path = _load_monitoring_module(monkeypatch, tmp_path)
    app = FastAPI()
    app.middleware("http")(module.application_monitoring_middleware)

    @app.get("/boom")
    def boom():
        raise RuntimeError("boom")

    response = TestClient(app, raise_server_exceptions=False).get("/boom")
    assert response.status_code == 500

    with metrics_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    assert rows[0]["status_code"] == "500"
    assert rows[0]["is_5xx"] == "true"
    assert rows[0]["error_type"] == "RuntimeError"


def test_main_application_registers_monitoring_middleware(monkeypatch, tmp_path):
    metrics_path = tmp_path / "main_app_metrics.csv"
    monkeypatch.setenv("APPLICATION_MONITORING_METRICS_PATH", str(metrics_path))

    import api.application_monitoring as monitoring_module
    monitoring_module = importlib.reload(monitoring_module)

    import api.main as main_module
    main_module = importlib.reload(main_module)

    response = TestClient(main_module.app).get("/")
    assert response.status_code == 200

    with metrics_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    assert any(row["path"] == "/" for row in rows)


def test_monitoring_write_failure_does_not_break_request(monkeypatch, tmp_path):
    module, _ = _load_monitoring_module(monkeypatch, tmp_path)

    def fail_write(*args, **kwargs):
        raise OSError("monitoring disk unavailable")

    monkeypatch.setattr(module, "append_metric", fail_write)

    app = FastAPI()
    app.middleware("http")(module.application_monitoring_middleware)

    @app.get("/ok")
    def ok():
        return {"status": "ok"}

    response = TestClient(app).get("/ok")
    assert response.status_code == 200
