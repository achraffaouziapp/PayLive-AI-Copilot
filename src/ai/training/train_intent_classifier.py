from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime
import json
import time

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_recall_fscore_support,
)


# -------------------------------------------------------------------
# Intent classifier training for PayLive AI Copilot
# -------------------------------------------------------------------
# This script trains the first baseline NLP model for Bloc 2.
#
# Model:
# - TF-IDF vectorizer
# - Logistic Regression classifier
#
# Inputs:
# - data/ai/datasets/train.csv
# - data/ai/datasets/validation.csv
# - data/ai/datasets/test.csv
#
# Outputs:
# - models/intent_classifier/model.joblib
# - models/intent_classifier/vectorizer.joblib
# - models/intent_classifier/label_encoder.joblib
# - models/intent_classifier/model_metadata.json
# - data/ai/reports/model_training_report.csv
# - data/ai/reports/model_evaluation_report.csv
# - data/ai/reports/classification_report.csv
# - data/ai/reports/confusion_matrix.csv
# -------------------------------------------------------------------


BASE_DIR = Path(__file__).resolve().parents[3]

AI_DATASETS_DIR = BASE_DIR / "data" / "ai" / "datasets"
AI_REPORTS_DIR = BASE_DIR / "data" / "ai" / "reports"
MODEL_DIR = BASE_DIR / "models" / "intent_classifier"

TRAIN_DATASET_PATH = AI_DATASETS_DIR / "train.csv"
VALIDATION_DATASET_PATH = AI_DATASETS_DIR / "validation.csv"
TEST_DATASET_PATH = AI_DATASETS_DIR / "test.csv"

MODEL_PATH = MODEL_DIR / "model.joblib"
VECTORIZER_PATH = MODEL_DIR / "vectorizer.joblib"
LABEL_ENCODER_PATH = MODEL_DIR / "label_encoder.joblib"
MODEL_METADATA_PATH = MODEL_DIR / "model_metadata.json"

TRAINING_REPORT_PATH = AI_REPORTS_DIR / "model_training_report.csv"
EVALUATION_REPORT_PATH = AI_REPORTS_DIR / "model_evaluation_report.csv"
CLASSIFICATION_REPORT_PATH = AI_REPORTS_DIR / "classification_report.csv"
CONFUSION_MATRIX_PATH = AI_REPORTS_DIR / "confusion_matrix.csv"

MODEL_NAME = "intent_classifier"
MODEL_VERSION = "intent_classifier_v1"
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


def ensure_directories() -> None:
    """
    Create required output directories.
    """
    AI_REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    MODEL_DIR.mkdir(parents=True, exist_ok=True)


def load_dataset(path: Path, split_name: str) -> pd.DataFrame:
    """
    Load one NLP dataset split.
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
    Validate required columns and basic quality rules.
    """
    required_columns = {TEXT_COLUMN, LABEL_COLUMN}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing columns in {split_name} dataset: {sorted(missing_columns)}"
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


def build_vectorizer() -> TfidfVectorizer:
    """
    Build the TF-IDF vectorizer.
    """
    return TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
        min_df=1,
        max_features=5000,
    )


def build_classifier() -> LogisticRegression:
    """
    Build the Logistic Regression classifier.
    """
    return LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        random_state=RANDOM_STATE,
    )


def fit_label_encoder(
    train_df: pd.DataFrame,
    validation_df: pd.DataFrame,
    test_df: pd.DataFrame,
) -> LabelEncoder:
    """
    Fit a label encoder on all labels available in the prepared datasets.

    The model itself is trained only on the train split.
    """
    all_labels = pd.concat(
        [
            train_df[LABEL_COLUMN],
            validation_df[LABEL_COLUMN],
            test_df[LABEL_COLUMN],
        ],
        axis=0,
    )

    label_encoder = LabelEncoder()
    label_encoder.fit(all_labels)

    return label_encoder


def train_model(
    train_df: pd.DataFrame,
    label_encoder: LabelEncoder,
) -> Tuple[TfidfVectorizer, LogisticRegression, float]:
    """
    Train the TF-IDF + Logistic Regression model.
    """
    start_time = time.perf_counter()

    vectorizer = build_vectorizer()
    classifier = build_classifier()

    x_train_text = train_df[TEXT_COLUMN].astype(str)
    y_train = label_encoder.transform(train_df[LABEL_COLUMN])

    x_train_vectorized = vectorizer.fit_transform(x_train_text)

    classifier.fit(x_train_vectorized, y_train)

    training_duration_seconds = round(time.perf_counter() - start_time, 4)

    return vectorizer, classifier, training_duration_seconds


def predict_dataset(
    df: pd.DataFrame,
    vectorizer: TfidfVectorizer,
    classifier: LogisticRegression,
    label_encoder: LabelEncoder,
) -> Tuple[List[str], List[float]]:
    """
    Predict labels and confidence scores for a dataset.
    """
    x_text = df[TEXT_COLUMN].astype(str)
    x_vectorized = vectorizer.transform(x_text)

    predicted_encoded = classifier.predict(x_vectorized)
    predicted_labels = label_encoder.inverse_transform(predicted_encoded).tolist()

    if hasattr(classifier, "predict_proba"):
        probabilities = classifier.predict_proba(x_vectorized)
        confidence_scores = probabilities.max(axis=1).round(4).tolist()
    else:
        confidence_scores = [0.0 for _ in predicted_labels]

    return predicted_labels, confidence_scores


def evaluate_split(
    split_name: str,
    df: pd.DataFrame,
    vectorizer: TfidfVectorizer,
    classifier: LogisticRegression,
    label_encoder: LabelEncoder,
) -> Dict[str, object]:
    """
    Evaluate the model on one dataset split.
    """
    true_labels = df[LABEL_COLUMN].astype(str).tolist()
    predicted_labels, confidence_scores = predict_dataset(
        df=df,
        vectorizer=vectorizer,
        classifier=classifier,
        label_encoder=label_encoder,
    )

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
        "split_name": split_name,
        "row_count": len(df),
        "accuracy": round(float(accuracy), 4),
        "macro_precision": round(float(macro_precision), 4),
        "macro_recall": round(float(macro_recall), 4),
        "macro_f1": round(float(macro_f1), 4),
        "weighted_precision": round(float(weighted_precision), 4),
        "weighted_recall": round(float(weighted_recall), 4),
        "weighted_f1": round(float(weighted_f1), 4),
        "average_confidence_score": round(
            float(sum(confidence_scores) / len(confidence_scores)), 4
        )
        if confidence_scores
        else 0.0,
    }


def build_evaluation_report(
    validation_df: pd.DataFrame,
    test_df: pd.DataFrame,
    vectorizer: TfidfVectorizer,
    classifier: LogisticRegression,
    label_encoder: LabelEncoder,
) -> pd.DataFrame:
    """
    Build global evaluation metrics for validation and test datasets.
    """
    rows = [
        evaluate_split(
            split_name="validation",
            df=validation_df,
            vectorizer=vectorizer,
            classifier=classifier,
            label_encoder=label_encoder,
        ),
        evaluate_split(
            split_name="test",
            df=test_df,
            vectorizer=vectorizer,
            classifier=classifier,
            label_encoder=label_encoder,
        ),
    ]

    return pd.DataFrame(rows)


def build_classification_report_df(
    split_name: str,
    df: pd.DataFrame,
    vectorizer: TfidfVectorizer,
    classifier: LogisticRegression,
    label_encoder: LabelEncoder,
) -> pd.DataFrame:
    """
    Build a detailed classification report for one split.
    """
    true_labels = df[LABEL_COLUMN].astype(str).tolist()
    predicted_labels, _ = predict_dataset(
        df=df,
        vectorizer=vectorizer,
        classifier=classifier,
        label_encoder=label_encoder,
    )

    labels = sorted(label_encoder.classes_)

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
                    "split_name": split_name,
                    "label": label,
                    "precision": "",
                    "recall": "",
                    "f1_score": round(float(metrics), 4),
                    "support": "",
                }
            )

    return pd.DataFrame(rows)


def build_full_classification_report(
    validation_df: pd.DataFrame,
    test_df: pd.DataFrame,
    vectorizer: TfidfVectorizer,
    classifier: LogisticRegression,
    label_encoder: LabelEncoder,
) -> pd.DataFrame:
    """
    Build classification reports for validation and test datasets.
    """
    validation_report = build_classification_report_df(
        split_name="validation",
        df=validation_df,
        vectorizer=vectorizer,
        classifier=classifier,
        label_encoder=label_encoder,
    )

    test_report = build_classification_report_df(
        split_name="test",
        df=test_df,
        vectorizer=vectorizer,
        classifier=classifier,
        label_encoder=label_encoder,
    )

    return pd.concat([validation_report, test_report], ignore_index=True)


def build_confusion_matrix_df(
    split_name: str,
    df: pd.DataFrame,
    vectorizer: TfidfVectorizer,
    classifier: LogisticRegression,
    label_encoder: LabelEncoder,
) -> pd.DataFrame:
    """
    Build a confusion matrix report for one split.
    """
    true_labels = df[LABEL_COLUMN].astype(str).tolist()
    predicted_labels, _ = predict_dataset(
        df=df,
        vectorizer=vectorizer,
        classifier=classifier,
        label_encoder=label_encoder,
    )

    labels = sorted(label_encoder.classes_)

    matrix = confusion_matrix(
        true_labels,
        predicted_labels,
        labels=labels,
    )

    matrix_df = pd.DataFrame(
        matrix,
        index=labels,
        columns=labels,
    )

    matrix_df.insert(0, "actual_label", matrix_df.index)
    matrix_df.insert(0, "split_name", split_name)

    return matrix_df.reset_index(drop=True)


def build_full_confusion_matrix_report(
    validation_df: pd.DataFrame,
    test_df: pd.DataFrame,
    vectorizer: TfidfVectorizer,
    classifier: LogisticRegression,
    label_encoder: LabelEncoder,
) -> pd.DataFrame:
    """
    Build confusion matrices for validation and test datasets.
    """
    validation_matrix = build_confusion_matrix_df(
        split_name="validation",
        df=validation_df,
        vectorizer=vectorizer,
        classifier=classifier,
        label_encoder=label_encoder,
    )

    test_matrix = build_confusion_matrix_df(
        split_name="test",
        df=test_df,
        vectorizer=vectorizer,
        classifier=classifier,
        label_encoder=label_encoder,
    )

    return pd.concat([validation_matrix, test_matrix], ignore_index=True)


def build_training_report(
    train_df: pd.DataFrame,
    validation_df: pd.DataFrame,
    test_df: pd.DataFrame,
    vectorizer: TfidfVectorizer,
    classifier: LogisticRegression,
    label_encoder: LabelEncoder,
    training_duration_seconds: float,
) -> pd.DataFrame:
    """
    Build a technical training report.
    """
    rows: List[Dict[str, object]] = []

    rows.extend(
        [
            {
                "report_section": "model",
                "metric_name": "model_name",
                "metric_value": MODEL_NAME,
                "details": "",
            },
            {
                "report_section": "model",
                "metric_name": "model_version",
                "metric_value": MODEL_VERSION,
                "details": "",
            },
            {
                "report_section": "model",
                "metric_name": "algorithm",
                "metric_value": "TF-IDF + Logistic Regression",
                "details": "",
            },
            {
                "report_section": "model",
                "metric_name": "training_date",
                "metric_value": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "details": "",
            },
            {
                "report_section": "model",
                "metric_name": "training_duration_seconds",
                "metric_value": training_duration_seconds,
                "details": "",
            },
            {
                "report_section": "datasets",
                "metric_name": "train_rows",
                "metric_value": len(train_df),
                "details": str(TRAIN_DATASET_PATH),
            },
            {
                "report_section": "datasets",
                "metric_name": "validation_rows",
                "metric_value": len(validation_df),
                "details": str(VALIDATION_DATASET_PATH),
            },
            {
                "report_section": "datasets",
                "metric_name": "test_rows",
                "metric_value": len(test_df),
                "details": str(TEST_DATASET_PATH),
            },
            {
                "report_section": "vectorizer",
                "metric_name": "max_features",
                "metric_value": vectorizer.max_features,
                "details": "",
            },
            {
                "report_section": "vectorizer",
                "metric_name": "ngram_range",
                "metric_value": str(vectorizer.ngram_range),
                "details": "",
            },
            {
                "report_section": "classifier",
                "metric_name": "class_weight",
                "metric_value": str(classifier.class_weight),
                "details": "",
            },
            {
                "report_section": "classifier",
                "metric_name": "max_iter",
                "metric_value": classifier.max_iter,
                "details": "",
            },
            {
                "report_section": "labels",
                "metric_name": "classes",
                "metric_value": ", ".join(label_encoder.classes_),
                "details": "",
            },
        ]
    )

    datasets = {
        "train": train_df,
        "validation": validation_df,
        "test": test_df,
    }

    for split_name, split_df in datasets.items():
        class_counts = split_df[LABEL_COLUMN].value_counts().to_dict()

        for label in sorted(label_encoder.classes_):
            rows.append(
                {
                    "report_section": "class_distribution",
                    "metric_name": f"{split_name}_{label}",
                    "metric_value": int(class_counts.get(label, 0)),
                    "details": f"Number of {label} rows in {split_name} split.",
                }
            )

    return pd.DataFrame(rows)


def save_model_artifacts(
    vectorizer: TfidfVectorizer,
    classifier: LogisticRegression,
    label_encoder: LabelEncoder,
    evaluation_report: pd.DataFrame,
) -> None:
    """
    Save trained model artifacts and metadata.
    """
    joblib.dump(classifier, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    joblib.dump(label_encoder, LABEL_ENCODER_PATH)

    test_metrics = (
        evaluation_report[evaluation_report["split_name"] == "test"]
        .iloc[0]
        .to_dict()
    )

    metadata = {
        "model_name": MODEL_NAME,
        "model_version": MODEL_VERSION,
        "algorithm": "TF-IDF + Logistic Regression",
        "training_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "random_state": RANDOM_STATE,
        "text_column": TEXT_COLUMN,
        "label_column": LABEL_COLUMN,
        "classes": sorted(label_encoder.classes_.tolist()),
        "train_file": str(TRAIN_DATASET_PATH),
        "validation_file": str(VALIDATION_DATASET_PATH),
        "test_file": str(TEST_DATASET_PATH),
        "model_file": str(MODEL_PATH),
        "vectorizer_file": str(VECTORIZER_PATH),
        "label_encoder_file": str(LABEL_ENCODER_PATH),
        "test_accuracy": test_metrics.get("accuracy"),
        "test_macro_f1": test_metrics.get("macro_f1"),
        "test_weighted_f1": test_metrics.get("weighted_f1"),
    }

    with open(MODEL_METADATA_PATH, "w", encoding="utf-8") as file:
        json.dump(metadata, file, ensure_ascii=False, indent=4)


def save_reports(
    training_report: pd.DataFrame,
    evaluation_report: pd.DataFrame,
    classification_report_df: pd.DataFrame,
    confusion_matrix_df: pd.DataFrame,
) -> None:
    """
    Save all model training and evaluation reports.
    """
    training_report.to_csv(
        TRAINING_REPORT_PATH,
        index=False,
        encoding="utf-8",
    )

    evaluation_report.to_csv(
        EVALUATION_REPORT_PATH,
        index=False,
        encoding="utf-8",
    )

    classification_report_df.to_csv(
        CLASSIFICATION_REPORT_PATH,
        index=False,
        encoding="utf-8",
    )

    confusion_matrix_df.to_csv(
        CONFUSION_MATRIX_PATH,
        index=False,
        encoding="utf-8",
    )


def main() -> None:
    """
    Run the full intent classifier training pipeline.
    """
    ensure_directories()

    train_df, validation_df, test_df = load_all_datasets()

    label_encoder = fit_label_encoder(
        train_df=train_df,
        validation_df=validation_df,
        test_df=test_df,
    )

    vectorizer, classifier, training_duration_seconds = train_model(
        train_df=train_df,
        label_encoder=label_encoder,
    )

    evaluation_report = build_evaluation_report(
        validation_df=validation_df,
        test_df=test_df,
        vectorizer=vectorizer,
        classifier=classifier,
        label_encoder=label_encoder,
    )

    classification_report_df = build_full_classification_report(
        validation_df=validation_df,
        test_df=test_df,
        vectorizer=vectorizer,
        classifier=classifier,
        label_encoder=label_encoder,
    )

    confusion_matrix_df = build_full_confusion_matrix_report(
        validation_df=validation_df,
        test_df=test_df,
        vectorizer=vectorizer,
        classifier=classifier,
        label_encoder=label_encoder,
    )

    training_report = build_training_report(
        train_df=train_df,
        validation_df=validation_df,
        test_df=test_df,
        vectorizer=vectorizer,
        classifier=classifier,
        label_encoder=label_encoder,
        training_duration_seconds=training_duration_seconds,
    )

    save_model_artifacts(
        vectorizer=vectorizer,
        classifier=classifier,
        label_encoder=label_encoder,
        evaluation_report=evaluation_report,
    )

    save_reports(
        training_report=training_report,
        evaluation_report=evaluation_report,
        classification_report_df=classification_report_df,
        confusion_matrix_df=confusion_matrix_df,
    )

    test_metrics = (
        evaluation_report[evaluation_report["split_name"] == "test"]
        .iloc[0]
        .to_dict()
    )

    print("Intent classifier training completed successfully.")
    print(f"Model: {MODEL_PATH}")
    print(f"Vectorizer: {VECTORIZER_PATH}")
    print(f"Label encoder: {LABEL_ENCODER_PATH}")
    print(f"Metadata: {MODEL_METADATA_PATH}")
    print(f"Training report: {TRAINING_REPORT_PATH}")
    print(f"Evaluation report: {EVALUATION_REPORT_PATH}")
    print(f"Classification report: {CLASSIFICATION_REPORT_PATH}")
    print(f"Confusion matrix: {CONFUSION_MATRIX_PATH}")
    print(f"Test accuracy: {test_metrics.get('accuracy')}")
    print(f"Test macro F1: {test_metrics.get('macro_f1')}")
    print(f"Test weighted F1: {test_metrics.get('weighted_f1')}")


if __name__ == "__main__":
    main()