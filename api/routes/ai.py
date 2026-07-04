from typing import Any, Dict, List
import os
from pathlib import Path
from fastapi.responses import FileResponse
from src.ai.monitoring.generate_monitoring_dashboard import main as generate_monitoring_dashboard
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field
from api.ai_service import (
    predict_single_comment,
    predict_multiple_comments,
    get_ai_model_information,
    get_ai_model_metrics,
)


BASE_DIR = Path(__file__).resolve().parents[2]

AI_REPORTS_DIR = BASE_DIR / "data" / "ai" / "reports"
DASHBOARD_PATH = AI_REPORTS_DIR / "model_monitoring_dashboard.html"
ALERTS_PATH = AI_REPORTS_DIR / "model_monitoring_alerts.csv"


# -------------------------------------------------------------------
# AI routes for PayLive AI Copilot API
# -------------------------------------------------------------------
# Routes:
# - POST /api/v1/ai/predict-intent
# - POST /api/v1/ai/batch-predict-intents
# - GET  /api/v1/ai/model-info
# - GET  /api/v1/ai/model-metrics
# -------------------------------------------------------------------


load_dotenv()

router = APIRouter()

API_KEY = os.getenv("API_KEY", "paylive-dev-api-key")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def require_api_key(api_key: str = Depends(api_key_header)) -> str:
    """
    Validate API key from X-API-Key header.
    """
    if api_key is None:
        raise HTTPException(
            status_code=401,
            detail="Missing API key.",
        )

    if api_key != API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Invalid API key.",
        )

    return api_key


class IntentPredictionRequest(BaseModel):
    """
    Request body for a single intent prediction.
    """

    comment_text: str = Field(
        ...,
        example="je prends le pull rouge en M",
        description="Comment text to classify.",
    )


class IntentPredictionResponse(BaseModel):
    """
    Response body for a single intent prediction.
    """

    comment_text: str
    predicted_intent: str
    confidence_score: float
    model_name: str
    model_version: str
    response_time_ms: float
    is_low_confidence: bool
    low_confidence_threshold: float


class BatchIntentPredictionRequest(BaseModel):
    """
    Request body for batch intent prediction.
    """

    comments: List[str] = Field(
        ...,
        example=[
            "je prends le pull rouge en M",
            "comment payer ?",
            "vous livrez en Belgique ?",
        ],
        description="List of comments to classify.",
    )


class BatchIntentPredictionResponse(BaseModel):
    """
    Response body for batch intent prediction.
    """

    prediction_count: int
    total_response_time_ms: float
    low_confidence_threshold: float
    low_confidence_count: int
    predictions: List[IntentPredictionResponse]


class ModelInfoResponse(BaseModel):
    """
    Response body for model information.
    """

    model: Dict[str, Any]
    benchmark_selection: Dict[str, Any]
    low_confidence_threshold: float


class ModelMetricsResponse(BaseModel):
    """
    Response body for model metrics.
    """

    metadata_metrics: Dict[str, Any]
    evaluation_report: Dict[str, Any]
    benchmark_selection: Dict[str, Any]
    low_confidence_threshold: float


@router.post(
    "/predict-intent",
    response_model=IntentPredictionResponse,
    summary="Predict intent for one comment",
    description="Predict the intent of a single live shopping comment.",
)
def predict_intent_route(
    request: IntentPredictionRequest,
    _: str = Depends(require_api_key),
) -> Dict[str, Any]:
    """
    Predict the intent of a single comment.
    """
    comment_text = request.comment_text.strip()

    if not comment_text:
        raise HTTPException(
            status_code=400,
            detail="Comment text cannot be empty.",
        )

    try:
        return predict_single_comment(comment_text)
    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {error}",
        ) from error


@router.post(
    "/batch-predict-intents",
    response_model=BatchIntentPredictionResponse,
    summary="Predict intents for several comments",
    description="Predict intents for a list of live shopping comments.",
)
def batch_predict_intents_route(
    request: BatchIntentPredictionRequest,
    _: str = Depends(require_api_key),
) -> Dict[str, Any]:
    """
    Predict intents for several comments.
    """
    comments = [
        comment.strip()
        for comment in request.comments
        if isinstance(comment, str) and comment.strip()
    ]

    if not comments:
        raise HTTPException(
            status_code=400,
            detail="Comments list cannot be empty.",
        )

    try:
        return predict_multiple_comments(comments)
    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Batch prediction failed: {error}",
        ) from error


@router.get(
    "/model-info",
    response_model=ModelInfoResponse,
    summary="Get AI model information",
    description="Return metadata and benchmark selection information for the active AI model.",
)
def model_info_route(
    _: str = Depends(require_api_key),
) -> Dict[str, Any]:
    """
    Return model information.
    """
    try:
        return get_ai_model_information()
    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to load model information: {error}",
        ) from error


@router.get(
    "/model-metrics",
    response_model=ModelMetricsResponse,
    summary="Get AI model metrics",
    description="Return evaluation metrics and benchmark selection information for the active AI model.",
)
def model_metrics_route(
    _: str = Depends(require_api_key),
) -> Dict[str, Any]:
    """
    Return model metrics.
    """
    try:
        return get_ai_model_metrics()
    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to load model metrics: {error}",
        ) from error


@router.get("/monitoring/dashboard")
def get_ai_monitoring_dashboard(
    _: str = Depends(require_api_key),
):
    """
    Retourne le dashboard HTML de monitoring IA.

    Le dashboard est régénéré à chaque appel afin d'afficher les dernières
    prédictions journalisées dans ai_predictions_log.csv.
    """
    generate_monitoring_dashboard()

    if not DASHBOARD_PATH.exists():
        raise HTTPException(
            status_code=404,
            detail="Dashboard de monitoring IA introuvable.",
        )

    return FileResponse(
        path=str(DASHBOARD_PATH),
        media_type="text/html",
        filename="model_monitoring_dashboard.html",
    )


@router.get("/monitoring/alerts")
def get_ai_monitoring_alerts(
    _: str = Depends(require_api_key),
):
    """
    Retourne le fichier CSV des alertes de monitoring IA.
    """
    generate_monitoring_dashboard()

    if not ALERTS_PATH.exists():
        raise HTTPException(
            status_code=404,
            detail="Fichier d'alertes de monitoring IA introuvable.",
        )

    return FileResponse(
        path=str(ALERTS_PATH),
        media_type="text/csv",
        filename="model_monitoring_alerts.csv",
    )        