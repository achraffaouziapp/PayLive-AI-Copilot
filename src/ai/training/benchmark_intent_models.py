from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime
import time

import numpy as np
import pandas as pd

from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    precision_recall_fscore_support,
)
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC


# -------------------------------------------------------------------
# Internal model benchmark for PayLive AI Copilot
# -------------------------------------------------------------------
# This script compares several intent classification approaches.
#
# Inputs:
# - data/ai/datasets/train.csv
# - data/ai/datasets/validation.csv
# - data/ai/datasets/test.csv
#
# Outputs:
# - data/ai/reports/model_benchmark_report.csv
# - data/ai/reports/model_benchmark_classification_report.csv
# - data/ai/reports/model_benchmark_selection_report.csv
# -------------------------------------------------------------------


BASE_DIR = Path(__file__).resolve().parents[3]

AI_DATASETS_DIR = BASE_DIR / "data" / "ai" / "datasets"
AI_REPORTS_DIR = BASE_DIR / "data" / "ai" / "reports"

TRAIN_DATASET_PATH = AI_DATASETS_DIR / "train.csv"
VALIDATION_DATASET_PATH = AI_DATASETS_DIR / "validation.csv"
TEST_DATASET_PATH = AI_DATASETS_DIR / "test.csv"

BENCHMARK_REPORT_PATH = AI_REPORTS_DIR / "model_benchmark_report.csv"
BENCHMARK_CLASSIFICATION_REPORT_PATH = (
    AI_REPORTS_DIR / "model_benchmark_classification_report.csv"
)
BENCHMARK_SELECTION_REPORT_PATH = AI_REPORTS_DIR / "model_benchmark_selection_report.csv"

RANDOM_STATE = 42

TEXT_COLUMN = "comment_text"
LABEL_COLUMN = "manual_intent_label"

ALLOWED_INTENT_LABELS = {
    "purchase_intent",
    "product_question",
    "payment_question",
    "shipping_question",
    "other",
    "unknown",
}


# -------------------------------------------------------------------
# Basic rule-based baseline
# -------------------------------------------------------------------


def contains_any(text: str, keywords: List[str]) -> bool:
    """
    Check if one keyword exists in a text.
    """
    return any(keyword in text for keyword in keywords)


def normalize_text(value: object) -> str:
    """
    Normalize text for rule-based prediction.
    """
    if pd.isna(value):
        return ""

    text = str(value).strip().lower()
    text = text.replace("’", "'")
    text = " ".join(text.split())

    return text


def infer_intent_from_comment(comment_text: object) -> str:
    """
    Predict an intent with simple business rules.

    This is used as a baseline only.
    It is not selected as the final ML model.
    """
    text = normalize_text(comment_text)

    if not text:
        return "unknown"

    payment_keywords = [
        "payer",
        "paie",
        "paiement",
        "paypal",
        "carte",
        "cb",
        "lien de paiement",
        "payer par",
        "paiement sécurisé",
    ]

    shipping_keywords = [
        "livraison",
        "livrez",
        "livrer",
        "livré",
        "frais de port",
        "point relais",
        "mondial relay",
        "colissimo",
        "expédi",
        "envoi",
        "recevoir",
        "domicile",
        "belgique",
        "étranger",
    ]

    purchase_keywords = [
        "je prends",
        "je prend",
        "je veux commander",
        "je commande",
        "je veux acheter",
        "j'achète",
        "jachete",
        "réserve",
        "reserve",
        "mets-moi",
        "mets moi",
        "met moi",
        "garde-moi",
        "garde moi",
        "ajoute",
        "panier",
        "je le prends",
        "ok je prends",
        "je confirme",
        "2 pièces",
        "deux pièces",
        "2 exemplaires",
    ]

    product_keywords = [
        "prix",
        "combien coûte",
        "combien coute",
        "dispo",
        "disponible",
        "taille",
        "couleur",
        "stock",
        "matière",
        "matiere",
        "marque",
        "existe",
        "rouge",
        "noir",
        "bleu",
        "medium",
        "taille m",
        "taille l",
        "taille xl",
    ]

    other_keywords = [
        "coucou",
        "merci",
        "super",
        "trop beau",
        "j'adore",
        "bonjour",
        "hello",
        "bravo",
        "bonne soirée",
        "magnifique",
    ]

    if contains_any(text, payment_keywords):
        return "payment_question"

    if contains_any(text, shipping_keywords):
        return "shipping_question"

    if contains_any(text, purchase_keywords):
        return "purchase_intent"

    if contains_any(text, product_keywords):
        return "product_question"

    if contains_any(text, other_keywords):
        return "other"

    return "unknown"


# -------------------------------------------------------------------
# Dataset loading and validation
# -------------------------------------------------------------------


def ensure_directories() -> None:
    """
    Create output report directory.
    """
    AI_REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def load_dataset(path: Path, split_name: str) -> pd.DataFrame:
    """
    Load one dataset split.
    """
    if not path.exists():
        raise FileNotFoundError(
            f"{split_name} dataset not found: {path}. "
            "Run src/ai/data_preparation/prepare_nlp_dataset.py first."
        )

    df = pd.read_csv(
        path,
        dtype=str,
        keep_default_na=False,
        encoding="utf-8",
    )

    return df


def validate_dataset(df: pd.DataFrame, split_name: str) -> None:
    """
    Validate required columns and labels.
    """
    required_columns = {TEXT_COLUMN, LABEL_COLUMN}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns in {split_name}: {sorted(missing_columns)}"
        )

    if df.empty:
        raise ValueError(f"{split_name} dataset is empty.")

    empty_text_count = int(df[TEXT_COLUMN].astype(str).str.strip().eq("").sum())

    if empty_text_count > 0:
        raise ValueError(
            f"{split_name} dataset contains {empty_text_count} empty comments."
        )

    invalid_labels = sorted(
        set(df[LABEL_COLUMN].dropna().unique()) - ALLOWED_INTENT_LABELS
    )

    if invalid_labels:
        raise ValueError(
            f"{split_name} dataset contains invalid labels: {invalid_labels}"
        )


def load_all_datasets() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Load train, validation and test datasets.
    """
    train_df = load_dataset(TRAIN_DATASET_PATH, "train")
    validation_df = load_dataset(VALIDATION_DATASET_PATH, "validation")
    test_df = load_dataset(TEST_DATASET_PATH, "test")

    validate_dataset(train_df, "train")
    validate_dataset(validation_df, "validation")
    validate_dataset(test_df, "test")

    return train_df, validation_df, test_df


# -------------------------------------------------------------------
# Model definitions
# -------------------------------------------------------------------


def build_tfidf_vectorizer() -> TfidfVectorizer:
    """
    Build the TF-IDF vectorizer used by ML models.
    """
    return TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
        min_df=1,
        max_features=5000,
    )


def build_model_candidates() -> List[Dict[str, object]]:
    """
    Build benchmark model candidates.
    """
    return [
        {
            "model_name": "business_rules_baseline",
            "model_family": "rules",
            "description": "Rule-based baseline using business keywords.",
            "eligible_for_final_selection": False,
            "estimator": None,
        },
        {
            "model_name": "dummy_most_frequent",
            "model_family": "baseline",
            "description": "Naive baseline predicting the most frequent class.",
            "eligible_for_final_selection": False,
            "estimator": DummyClassifier(
                strategy="most_frequent",
                random_state=RANDOM_STATE,
            ),
        },
        {
            "model_name": "tfidf_logistic_regression",
            "model_family": "machine_learning",
            "description": "TF-IDF vectorizer with Logistic Regression.",
            "eligible_for_final_selection": True,
            "estimator": Pipeline(
                steps=[
                    ("vectorizer", build_tfidf_vectorizer()),
                    (
                        "classifier",
                        LogisticRegression(
                            max_iter=1000,
                            class_weight="balanced",
                            random_state=RANDOM_STATE,
                        ),
                    ),
                ]
            ),
        },
        {
            "model_name": "tfidf_linear_svm",
            "model_family": "machine_learning",
            "description": "TF-IDF vectorizer with Linear SVM.",
            "eligible_for_final_selection": True,
            "estimator": Pipeline(
                steps=[
                    ("vectorizer", build_tfidf_vectorizer()),
                    (
                        "classifier",
                        LinearSVC(
                            class_weight="balanced",
                            random_state=RANDOM_STATE,
                            max_iter=3000,
                        ),
                    ),
                ]
            ),
        },
        {
            "model_name": "tfidf_multinomial_nb",
            "model_family": "machine_learning",
            "description": "TF-IDF vectorizer with Multinomial Naive Bayes.",
            "eligible_for_final_selection": True,
            "estimator": Pipeline(
                steps=[
                    ("vectorizer", build_tfidf_vectorizer()),
                    ("classifier", MultinomialNB(alpha=1.0)),
                ]
            ),
        },
        {
            "model_name": "tfidf_random_forest",
            "model_family": "machine_learning",
            "description": "TF-IDF vectorizer with Random Forest.",
            "eligible_for_final_selection": True,
            "estimator": Pipeline(
                steps=[
                    ("vectorizer", build_tfidf_vectorizer()),
                    (
                        "classifier",
                        RandomForestClassifier(
                            n_estimators=200,
                            class_weight="balanced",
                            random_state=RANDOM_STATE,
                            n_jobs=-1,
                        ),
                    ),
                ]
            ),
        },
    ]


# -------------------------------------------------------------------
# Training and prediction
# -------------------------------------------------------------------


def train_estimator(
    estimator: object,
    train_df: pd.DataFrame,
) -> float:
    """
    Train an estimator and return training duration.
    """
    start_time = time.perf_counter()

    estimator.fit(
        train_df[TEXT_COLUMN].astype(str),
        train_df[LABEL_COLUMN].astype(str),
    )

    training_duration_seconds = round(time.perf_counter() - start_time, 4)

    return training_duration_seconds


def predict_rules(df: pd.DataFrame) -> Tuple[List[str], List[float], float]:
    """
    Predict labels using business rules.
    """
    start_time = time.perf_counter()

    predicted_labels = [
        infer_intent_from_comment(comment)
        for comment in df[TEXT_COLUMN].astype(str).tolist()
    ]

    confidence_scores = [
        0.70 if label != "unknown" else 0.50
        for label in predicted_labels
    ]

    prediction_duration_seconds = round(time.perf_counter() - start_time, 4)

    return predicted_labels, confidence_scores, prediction_duration_seconds


def compute_confidence_scores(estimator: object, texts: pd.Series) -> List[float]:
    """
    Compute confidence scores when possible.

    Some models expose predict_proba.
    LinearSVC exposes decision_function instead.
    """
    if hasattr(estimator, "predict_proba"):
        probabilities = estimator.predict_proba(texts)
        return probabilities.max(axis=1).round(4).tolist()

    if hasattr(estimator, "decision_function"):
        decision_scores = estimator.decision_function(texts)

        if len(np.shape(decision_scores)) == 1:
            absolute_scores = np.abs(decision_scores)
            confidence_scores = absolute_scores / (1 + absolute_scores)
            return np.round(confidence_scores, 4).tolist()

        shifted_scores = decision_scores - np.max(
            decision_scores,
            axis=1,
            keepdims=True,
        )

        exp_scores = np.exp(shifted_scores)
        softmax_scores = exp_scores / exp_scores.sum(axis=1, keepdims=True)

        return softmax_scores.max(axis=1).round(4).tolist()

    return [0.0 for _ in texts]


def predict_estimator(
    estimator: object,
    df: pd.DataFrame,
) -> Tuple[List[str], List[float], float]:
    """
    Predict labels and confidence scores with a trained estimator.
    """
    texts = df[TEXT_COLUMN].astype(str)

    start_time = time.perf_counter()

    predicted_labels = estimator.predict(texts).tolist()
    confidence_scores = compute_confidence_scores(estimator, texts)

    prediction_duration_seconds = round(time.perf_counter() - start_time, 4)

    return predicted_labels, confidence_scores, prediction_duration_seconds


# -------------------------------------------------------------------
# Reports
# -------------------------------------------------------------------


def compute_global_metrics(
    true_labels: List[str],
    predicted_labels: List[str],
) -> Dict[str, float]:
    """
    Compute global benchmark metrics.
    """
    accuracy = accuracy_score(true_labels, predicted_labels)

    macro_precision, macro_recall, macro_f1, _ = precision_recall_fscore_support(
        true_labels,
        predicted_labels,
        average="macro",
        zero_division=0,
    )

    weighted_precision, weighted_recall, weighted_f1, _ = (
        precision_recall_fscore_support(
            true_labels,
            predicted_labels,
            average="weighted",
            zero_division=0,
        )
    )

    return {
        "accuracy": round(float(accuracy), 4),
        "macro_precision": round(float(macro_precision), 4),
        "macro_recall": round(float(macro_recall), 4),
        "macro_f1": round(float(macro_f1), 4),
        "weighted_precision": round(float(weighted_precision), 4),
        "weighted_recall": round(float(weighted_recall), 4),
        "weighted_f1": round(float(weighted_f1), 4),
    }


def build_benchmark_row(
    model_config: Dict[str, object],
    split_name: str,
    df: pd.DataFrame,
    predicted_labels: List[str],
    confidence_scores: List[float],
    training_duration_seconds: float,
    prediction_duration_seconds: float,
) -> Dict[str, object]:
    """
    Build one benchmark report row.
    """
    true_labels = df[LABEL_COLUMN].astype(str).tolist()
    metrics = compute_global_metrics(true_labels, predicted_labels)

    average_confidence = (
        round(float(np.mean(confidence_scores)), 4)
        if confidence_scores
        else 0.0
    )

    low_confidence_count = int(
        sum(score < 0.60 for score in confidence_scores)
    )

    return {
        "benchmark_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "model_name": model_config["model_name"],
        "model_family": model_config["model_family"],
        "description": model_config["description"],
        "eligible_for_final_selection": model_config[
            "eligible_for_final_selection"
        ],
        "split_name": split_name,
        "row_count": len(df),
        "training_duration_seconds": training_duration_seconds,
        "prediction_duration_seconds": prediction_duration_seconds,
        "average_confidence_score": average_confidence,
        "low_confidence_count": low_confidence_count,
        **metrics,
    }


def build_classification_report_rows(
    model_config: Dict[str, object],
    split_name: str,
    df: pd.DataFrame,
    predicted_labels: List[str],
) -> List[Dict[str, object]]:
    """
    Build detailed classification report rows.
    """
    true_labels = df[LABEL_COLUMN].astype(str).tolist()
    labels = sorted(ALLOWED_INTENT_LABELS)

    report = classification_report(
        true_labels,
        predicted_labels,
        labels=labels,
        output_dict=True,
        zero_division=0,
    )

    rows = []

    for label, metrics in report.items():
        if isinstance(metrics, dict):
            rows.append(
                {
                    "model_name": model_config["model_name"],
                    "model_family": model_config["model_family"],
                    "split_name": split_name,
                    "label": label,
                    "precision": round(float(metrics.get("precision", 0)), 4),
                    "recall": round(float(metrics.get("recall", 0)), 4),
                    "f1_score": round(float(metrics.get("f1-score", 0)), 4),
                    "support": int(metrics.get("support", 0)),
                }
            )
        else:
            rows.append(
                {
                    "model_name": model_config["model_name"],
                    "model_family": model_config["model_family"],
                    "split_name": split_name,
                    "label": label,
                    "precision": "",
                    "recall": "",
                    "f1_score": round(float(metrics), 4),
                    "support": "",
                }
            )

    return rows


def build_selection_report(benchmark_report: pd.DataFrame) -> pd.DataFrame:
    """
    Select the best eligible ML model using validation weighted F1.

    Rules-based baseline and dummy baseline are excluded from final selection.
    """
    eligible_validation_results = benchmark_report[
        (benchmark_report["split_name"] == "validation")
        & (benchmark_report["eligible_for_final_selection"] == True)
    ].copy()

    if eligible_validation_results.empty:
        raise ValueError("No eligible model found for final selection.")

    eligible_validation_results = eligible_validation_results.sort_values(
        by=["weighted_f1", "macro_f1", "accuracy"],
        ascending=[False, False, False],
    ).reset_index(drop=True)

    selected_model = eligible_validation_results.iloc[0].to_dict()

    rows = []

    rows.append(
        {
            "selection_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "selection_metric": "validation weighted_f1, then macro_f1, then accuracy",
            "selected_model_name": selected_model["model_name"],
            "selected_model_family": selected_model["model_family"],
            "validation_accuracy": selected_model["accuracy"],
            "validation_macro_f1": selected_model["macro_f1"],
            "validation_weighted_f1": selected_model["weighted_f1"],
            "decision": "Selected as best eligible ML model for API integration candidate.",
            "details": (
                "Rules baseline and dummy baseline are excluded from final ML "
                "selection because they are not trained ML models."
            ),
        }
    )

    return pd.DataFrame(rows)


def save_reports(
    benchmark_report: pd.DataFrame,
    classification_report_df: pd.DataFrame,
    selection_report: pd.DataFrame,
) -> None:
    """
    Save benchmark reports.
    """
    benchmark_report.to_csv(
        BENCHMARK_REPORT_PATH,
        index=False,
        encoding="utf-8",
    )

    classification_report_df.to_csv(
        BENCHMARK_CLASSIFICATION_REPORT_PATH,
        index=False,
        encoding="utf-8",
    )

    selection_report.to_csv(
        BENCHMARK_SELECTION_REPORT_PATH,
        index=False,
        encoding="utf-8",
    )


# -------------------------------------------------------------------
# Main benchmark pipeline
# -------------------------------------------------------------------


def run_benchmark() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Run the full internal benchmark.
    """
    train_df, validation_df, test_df = load_all_datasets()

    model_candidates = build_model_candidates()

    benchmark_rows: List[Dict[str, object]] = []
    classification_rows: List[Dict[str, object]] = []

    evaluation_splits = {
        "validation": validation_df,
        "test": test_df,
    }

    for model_config in model_candidates:
        model_name = str(model_config["model_name"])
        estimator = model_config["estimator"]

        print(f"Running benchmark for model: {model_name}")

        if model_name == "business_rules_baseline":
            training_duration_seconds = 0.0
        else:
            training_duration_seconds = train_estimator(estimator, train_df)

        for split_name, split_df in evaluation_splits.items():
            if model_name == "business_rules_baseline":
                predicted_labels, confidence_scores, prediction_duration_seconds = (
                    predict_rules(split_df)
                )
            else:
                predicted_labels, confidence_scores, prediction_duration_seconds = (
                    predict_estimator(estimator, split_df)
                )

            benchmark_rows.append(
                build_benchmark_row(
                    model_config=model_config,
                    split_name=split_name,
                    df=split_df,
                    predicted_labels=predicted_labels,
                    confidence_scores=confidence_scores,
                    training_duration_seconds=training_duration_seconds,
                    prediction_duration_seconds=prediction_duration_seconds,
                )
            )

            classification_rows.extend(
                build_classification_report_rows(
                    model_config=model_config,
                    split_name=split_name,
                    df=split_df,
                    predicted_labels=predicted_labels,
                )
            )

    benchmark_report = pd.DataFrame(benchmark_rows)
    classification_report_df = pd.DataFrame(classification_rows)
    selection_report = build_selection_report(benchmark_report)

    return benchmark_report, classification_report_df, selection_report


def main() -> None:
    """
    Run benchmark and save reports.
    """
    ensure_directories()

    benchmark_report, classification_report_df, selection_report = run_benchmark()

    save_reports(
        benchmark_report=benchmark_report,
        classification_report_df=classification_report_df,
        selection_report=selection_report,
    )

    selected_model_name = selection_report.iloc[0]["selected_model_name"]
    validation_weighted_f1 = selection_report.iloc[0]["validation_weighted_f1"]

    print("Internal model benchmark completed successfully.")
    print(f"Benchmark report: {BENCHMARK_REPORT_PATH}")
    print(f"Classification report: {BENCHMARK_CLASSIFICATION_REPORT_PATH}")
    print(f"Selection report: {BENCHMARK_SELECTION_REPORT_PATH}")
    print(f"Selected eligible model: {selected_model_name}")
    print(f"Selected model validation weighted F1: {validation_weighted_f1}")


if __name__ == "__main__":
    main()