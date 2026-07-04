from pathlib import Path
from typing import Dict, List, Optional
import json
import time

import joblib
import pandas as pd


# -------------------------------------------------------------------
# Intent predictor for PayLive AI Copilot
# -------------------------------------------------------------------
# This module loads the trained intent classification model and exposes
# simple prediction functions.
#
# Inputs:
# - a single comment text
# - or a list of comment texts
#
# Required artifacts:
# - models/intent_classifier/model.joblib
# - models/intent_classifier/vectorizer.joblib
# - models/intent_classifier/label_encoder.joblib
# - models/intent_classifier/model_metadata.json
#
# Main functions:
# - load_model_artifacts()
# - predict_intent(comment_text)
# - predict_batch(comment_texts)
# - get_model_info()
# -------------------------------------------------------------------


BASE_DIR = Path(__file__).resolve().parents[3]

MODEL_DIR = BASE_DIR / "models" / "intent_classifier"

MODEL_PATH = MODEL_DIR / "model.joblib"
VECTORIZER_PATH = MODEL_DIR / "vectorizer.joblib"
LABEL_ENCODER_PATH = MODEL_DIR / "label_encoder.joblib"
MODEL_METADATA_PATH = MODEL_DIR / "model_metadata.json"

DEFAULT_MODEL_VERSION = "intent_classifier_v1"

ALLOWED_INTENT_LABELS = {
    "purchase_intent",
    "product_question",
    "payment_question",
    "shipping_question",
    "other",
    "unknown",
}


_MODEL_CACHE: Dict[str, object] = {}


def normalize_comment_text(comment_text: object) -> str:
    """
    Normalize a comment before prediction.

    The goal is to remove useless spaces while keeping the original meaning.
    """
    if pd.isna(comment_text):
        return ""

    text = str(comment_text)
    text = " ".join(text.split())

    return text.strip()


def validate_comment_text(comment_text: object) -> str:
    """
    Validate and normalize a comment text.

    Raises:
        ValueError: if the comment is empty.
    """
    normalized_text = normalize_comment_text(comment_text)

    if not normalized_text:
        raise ValueError("Comment text cannot be empty.")

    return normalized_text


def check_model_artifacts_exist() -> None:
    """
    Check that all required model artifacts exist.
    """
    required_files = [
        MODEL_PATH,
        VECTORIZER_PATH,
        LABEL_ENCODER_PATH,
        MODEL_METADATA_PATH,
    ]

    missing_files = [str(path) for path in required_files if not path.exists()]

    if missing_files:
        raise FileNotFoundError(
            "Some model artifacts are missing. "
            "Run src/ai/training/train_intent_classifier.py first. "
            f"Missing files: {missing_files}"
        )


def load_model_metadata() -> Dict[str, object]:
    """
    Load model metadata from JSON file.
    """
    if not MODEL_METADATA_PATH.exists():
        return {
            "model_name": "intent_classifier",
            "model_version": DEFAULT_MODEL_VERSION,
            "algorithm": "TF-IDF + Logistic Regression",
            "classes": sorted(ALLOWED_INTENT_LABELS),
        }

    with open(MODEL_METADATA_PATH, "r", encoding="utf-8") as file:
        metadata = json.load(file)

    return metadata


def load_model_artifacts(force_reload: bool = False) -> Dict[str, object]:
    """
    Load model, vectorizer, label encoder and metadata.

    A small in-memory cache is used to avoid reloading artifacts at every
    prediction.
    """
    if _MODEL_CACHE and not force_reload:
        return _MODEL_CACHE

    check_model_artifacts_exist()

    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    label_encoder = joblib.load(LABEL_ENCODER_PATH)
    metadata = load_model_metadata()

    _MODEL_CACHE.clear()
    _MODEL_CACHE.update(
        {
            "model": model,
            "vectorizer": vectorizer,
            "label_encoder": label_encoder,
            "metadata": metadata,
        }
    )

    return _MODEL_CACHE


def get_model_version(metadata: Dict[str, object]) -> str:
    """
    Return the model version from metadata.
    """
    return str(metadata.get("model_version", DEFAULT_MODEL_VERSION))


def get_model_name(metadata: Dict[str, object]) -> str:
    """
    Return the model name from metadata.
    """
    return str(metadata.get("model_name", "intent_classifier"))


def get_confidence_score(model: object, vectorized_text: object) -> float:
    """
    Compute confidence score for one prediction.

    Logistic Regression exposes predict_proba, so the confidence score is
    the highest predicted probability.
    """
    if not hasattr(model, "predict_proba"):
        return 0.0

    probabilities = model.predict_proba(vectorized_text)

    if probabilities.size == 0:
        return 0.0

    return round(float(probabilities.max(axis=1)[0]), 4)


def predict_intent(comment_text: object) -> Dict[str, object]:
    """
    Predict the intent of a single comment.

    Args:
        comment_text: comment to classify.

    Returns:
        A dictionary containing the prediction result.
    """
    start_time = time.perf_counter()

    normalized_text = validate_comment_text(comment_text)

    artifacts = load_model_artifacts()

    model = artifacts["model"]
    vectorizer = artifacts["vectorizer"]
    label_encoder = artifacts["label_encoder"]
    metadata = artifacts["metadata"]

    vectorized_text = vectorizer.transform([normalized_text])

    predicted_encoded_label = model.predict(vectorized_text)
    predicted_label = label_encoder.inverse_transform(predicted_encoded_label)[0]

    confidence_score = get_confidence_score(model, vectorized_text)

    response_time_ms = round((time.perf_counter() - start_time) * 1000, 2)

    return {
        "comment_text": normalized_text,
        "predicted_intent": str(predicted_label),
        "confidence_score": confidence_score,
        "model_name": get_model_name(metadata),
        "model_version": get_model_version(metadata),
        "response_time_ms": response_time_ms,
    }


def predict_batch(comment_texts: List[object]) -> Dict[str, object]:
    """
    Predict intents for a list of comments.

    Args:
        comment_texts: list of comments to classify.

    Returns:
        A dictionary containing all prediction results.
    """
    if not isinstance(comment_texts, list):
        raise ValueError("comment_texts must be a list.")

    if not comment_texts:
        raise ValueError("comment_texts cannot be empty.")

    start_time = time.perf_counter()

    predictions = []

    for comment_text in comment_texts:
        predictions.append(predict_intent(comment_text))

    total_response_time_ms = round((time.perf_counter() - start_time) * 1000, 2)

    return {
        "prediction_count": len(predictions),
        "total_response_time_ms": total_response_time_ms,
        "predictions": predictions,
    }


def get_model_info() -> Dict[str, object]:
    """
    Return model information from metadata and artifact paths.
    """
    artifacts = load_model_artifacts()
    metadata = artifacts["metadata"]
    label_encoder = artifacts["label_encoder"]

    classes = metadata.get("classes")

    if not classes:
        classes = sorted(label_encoder.classes_.tolist())

    return {
        "model_name": get_model_name(metadata),
        "model_version": get_model_version(metadata),
        "algorithm": metadata.get("algorithm", "TF-IDF + Logistic Regression"),
        "training_date": metadata.get("training_date", ""),
        "classes": classes,
        "text_column": metadata.get("text_column", "comment_text"),
        "label_column": metadata.get("label_column", "manual_intent_label"),
        "test_accuracy": metadata.get("test_accuracy"),
        "test_macro_f1": metadata.get("test_macro_f1"),
        "test_weighted_f1": metadata.get("test_weighted_f1"),
        "model_file": str(MODEL_PATH),
        "vectorizer_file": str(VECTORIZER_PATH),
        "label_encoder_file": str(LABEL_ENCODER_PATH),
        "metadata_file": str(MODEL_METADATA_PATH),
    }


def get_model_metrics() -> Dict[str, object]:
    """
    Return the main evaluation metrics stored in metadata.
    """
    metadata = load_model_metadata()

    return {
        "model_name": get_model_name(metadata),
        "model_version": get_model_version(metadata),
        "test_accuracy": metadata.get("test_accuracy"),
        "test_macro_f1": metadata.get("test_macro_f1"),
        "test_weighted_f1": metadata.get("test_weighted_f1"),
    }


def run_manual_test() -> None:
    """
    Run a few manual predictions from the command line.
    """
    examples = [
        "je prends le pull rouge en M",
        "comment payer ?",
        "vous livrez en Belgique ?",
        "elle existe en noir ?",
        "trop beau",
        "je ne sais pas",
    ]

    print("Model information:")
    print(json.dumps(get_model_info(), ensure_ascii=False, indent=4))

    print("\nManual predictions:")

    for example in examples:
        prediction = predict_intent(example)
        print(json.dumps(prediction, ensure_ascii=False, indent=4))


if __name__ == "__main__":
    run_manual_test()