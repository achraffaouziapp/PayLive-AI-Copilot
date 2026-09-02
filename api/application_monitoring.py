import csv
import logging
import os
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Awaitable, Callable

from fastapi import Request
from starlette.responses import Response

APP_MONITORING_DIR = Path("data/application_monitoring")
APP_METRICS_PATH = Path(
    os.getenv(
        "APPLICATION_MONITORING_METRICS_PATH",
        str(APP_MONITORING_DIR / "app_metrics.csv"),
    )
)

METRICS_HEADER = [
    "timestamp",
    "method",
    "path",
    "status_code",
    "response_time_ms",
    "is_5xx",
    "error_type",
]

_WRITE_LOCK = threading.Lock()
LOGGER = logging.getLogger(__name__)


def ensure_metrics_file(path: Path = APP_METRICS_PATH) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=METRICS_HEADER)
            writer.writeheader()
    return path


def append_metric(row: dict[str, str], path: Path = APP_METRICS_PATH) -> None:
    with _WRITE_LOCK:
        ensure_metrics_file(path)
        with path.open("a", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=METRICS_HEADER)
            writer.writerow(row)


async def application_monitoring_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    started = time.perf_counter()
    status_code = 500
    error_type = ""

    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    except Exception as exc:
        status_code = 500
        error_type = type(exc).__name__
        raise
    finally:
        duration_ms = (time.perf_counter() - started) * 1000
        metric_row = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "method": request.method,
            "path": request.url.path,
            "status_code": str(status_code),
            "response_time_ms": f"{duration_ms:.2f}",
            "is_5xx": "true" if status_code >= 500 else "false",
            "error_type": error_type,
        }

        try:
            append_metric(metric_row)
        except OSError:
            LOGGER.exception("Unable to write application monitoring metric")
