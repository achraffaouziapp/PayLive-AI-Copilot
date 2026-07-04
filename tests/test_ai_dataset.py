from pathlib import Path
import sys

import pandas as pd


# -------------------------------------------------------------------
# AI dataset tests for PayLive AI Copilot
# -------------------------------------------------------------------


BASE_DIR = Path(__file__).resolve().parents[1]

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


AI_DATASETS_DIR = BASE_DIR / "data" / "ai" / "datasets"
AI_REPORTS_DIR = BASE_DIR / "data" / "ai" / "reports"

FULL_DATASET_PATH = AI_DATASETS_DIR / "comments_intent_dataset.csv"
TRAIN_DATASET_PATH = AI_DATASETS_DIR / "train.csv"
VALIDATION_DATASET_PATH = AI_DATASETS_DIR / "validation.csv"
TEST_DATASET_PATH = AI_DATASETS_DIR / "test.csv"

NLP_QUALITY_REPORT_PATH = AI_REPORTS_DIR / "nlp_dataset_quality_report.csv"
SPLIT_REPORT_PATH = AI_REPORTS_DIR / "train_validation_test_split_report.csv"
TEST_REPORT_PATH = AI_REPORTS_DIR / "ai_dataset_test_report.csv"

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

REQUIRED_DATASET_COLUMNS = {
    TEXT_COLUMN,
    LABEL_COLUMN,
}


test_results = []


def add_test_result(test_name: str, status: str, details: str = "") -> None:
    """
    Store test execution result for CSV reporting.
    """
    test_results.append(
        {
            "test_name": test_name,
            "status": status,
            "details": details,
        }
    )


def save_test_report() -> None:
    """
    Save AI dataset test report.
    """
    AI_REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(test_results).to_csv(
        TEST_REPORT_PATH,
        index=False,
        encoding="utf-8",
    )


def load_csv(path: Path) -> pd.DataFrame:
    """
    Load a CSV file as string columns.
    """
    return pd.read_csv(
        path,
        dtype=str,
        keep_default_na=False,
        encoding="utf-8",
    )


def test_ai_dataset_files_exist():
    """
    Check that all expected AI dataset files exist.
    """
    expected_files = [
        FULL_DATASET_PATH,
        TRAIN_DATASET_PATH,
        VALIDATION_DATASET_PATH,
        TEST_DATASET_PATH,
    ]

    missing_files = [str(path) for path in expected_files if not path.exists()]

    assert not missing_files, f"Missing dataset files: {missing_files}"

    add_test_result(
        "test_ai_dataset_files_exist",
        "passed",
        "All AI dataset files exist.",
    )


def test_ai_report_files_exist():
    """
    Check that preparation reports exist.
    """
    expected_files = [
        NLP_QUALITY_REPORT_PATH,
        SPLIT_REPORT_PATH,
    ]

    missing_files = [str(path) for path in expected_files if not path.exists()]

    assert not missing_files, f"Missing report files: {missing_files}"

    add_test_result(
        "test_ai_report_files_exist",
        "passed",
        "NLP quality and split reports exist.",
    )


def test_full_dataset_has_required_columns():
    """
    Check required columns in the full NLP dataset.
    """
    df = load_csv(FULL_DATASET_PATH)

    missing_columns = REQUIRED_DATASET_COLUMNS - set(df.columns)

    assert not missing_columns, f"Missing columns: {missing_columns}"

    add_test_result(
        "test_full_dataset_has_required_columns",
        "passed",
        "Required columns are present.",
    )


def test_full_dataset_is_not_empty():
    """
    Check that the full NLP dataset is not empty.
    """
    df = load_csv(FULL_DATASET_PATH)

    assert len(df) > 0, "The full NLP dataset is empty."

    add_test_result(
        "test_full_dataset_is_not_empty",
        "passed",
        f"Dataset rows: {len(df)}",
    )


def test_comment_texts_are_not_empty():
    """
    Check that no comment text is empty.
    """
    df = load_csv(FULL_DATASET_PATH)

    empty_count = int(df[TEXT_COLUMN].astype(str).str.strip().eq("").sum())

    assert empty_count == 0, f"Empty comments found: {empty_count}"

    add_test_result(
        "test_comment_texts_are_not_empty",
        "passed",
        "No empty comments found.",
    )


def test_labels_are_allowed():
    """
    Check that labels belong to the allowed intent list.
    """
    df = load_csv(FULL_DATASET_PATH)

    invalid_labels = sorted(set(df[LABEL_COLUMN].unique()) - ALLOWED_INTENT_LABELS)

    assert not invalid_labels, f"Invalid labels found: {invalid_labels}"

    add_test_result(
        "test_labels_are_allowed",
        "passed",
        "All labels are allowed.",
    )


def test_expected_classes_are_present():
    """
    Check that all expected classes are present in the full dataset.
    """
    df = load_csv(FULL_DATASET_PATH)

    existing_labels = set(df[LABEL_COLUMN].unique())
    missing_labels = sorted(ALLOWED_INTENT_LABELS - existing_labels)

    assert not missing_labels, f"Missing labels in full dataset: {missing_labels}"

    add_test_result(
        "test_expected_classes_are_present",
        "passed",
        "All expected classes are present.",
    )


def test_train_validation_test_are_not_empty():
    """
    Check that train, validation and test splits are not empty.
    """
    train_df = load_csv(TRAIN_DATASET_PATH)
    validation_df = load_csv(VALIDATION_DATASET_PATH)
    test_df = load_csv(TEST_DATASET_PATH)

    assert len(train_df) > 0, "Train dataset is empty."
    assert len(validation_df) > 0, "Validation dataset is empty."
    assert len(test_df) > 0, "Test dataset is empty."

    add_test_result(
        "test_train_validation_test_are_not_empty",
        "passed",
        (
            f"train={len(train_df)}, "
            f"validation={len(validation_df)}, "
            f"test={len(test_df)}"
        ),
    )


def test_split_total_matches_full_dataset():
    """
    Check that train + validation + test equals the full NLP dataset size.
    """
    full_df = load_csv(FULL_DATASET_PATH)
    train_df = load_csv(TRAIN_DATASET_PATH)
    validation_df = load_csv(VALIDATION_DATASET_PATH)
    test_df = load_csv(TEST_DATASET_PATH)

    split_total = len(train_df) + len(validation_df) + len(test_df)

    assert split_total == len(full_df), (
        f"Split total {split_total} does not match full dataset {len(full_df)}."
    )

    add_test_result(
        "test_split_total_matches_full_dataset",
        "passed",
        f"Split total matches full dataset: {split_total}",
    )


def test_dataset_report_is_saved():
    """
    Save test report at the end of dataset tests.
    """
    add_test_result(
        "test_dataset_report_is_saved",
        "passed",
        f"Report saved to {TEST_REPORT_PATH}",
    )

    save_test_report()

    assert TEST_REPORT_PATH.exists(), "AI dataset test report was not saved."