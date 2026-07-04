from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd
from sklearn.model_selection import train_test_split


# -------------------------------------------------------------------
# NLP dataset preparation for PayLive AI Copilot
# -------------------------------------------------------------------
# This script prepares the NLP dataset used in Bloc 2.
#
# Source:
# - data/processed/clean/live_comments_clean.csv
#
# Outputs:
# - data/ai/datasets/comments_intent_dataset.csv
# - data/ai/datasets/train.csv
# - data/ai/datasets/validation.csv
# - data/ai/datasets/test.csv
# - data/ai/reports/nlp_dataset_quality_report.csv
# - data/ai/reports/train_validation_test_split_report.csv
# -------------------------------------------------------------------


BASE_DIR = Path(__file__).resolve().parents[3]

PROCESSED_CLEAN_DIR = BASE_DIR / "data" / "processed" / "clean"
AI_DATASETS_DIR = BASE_DIR / "data" / "ai" / "datasets"
AI_REPORTS_DIR = BASE_DIR / "data" / "ai" / "reports"

SOURCE_COMMENTS_PATH = PROCESSED_CLEAN_DIR / "live_comments_clean.csv"

FULL_NLP_DATASET_PATH = AI_DATASETS_DIR / "comments_intent_dataset.csv"
TRAIN_DATASET_PATH = AI_DATASETS_DIR / "train.csv"
VALIDATION_DATASET_PATH = AI_DATASETS_DIR / "validation.csv"
TEST_DATASET_PATH = AI_DATASETS_DIR / "test.csv"

NLP_QUALITY_REPORT_PATH = AI_REPORTS_DIR / "nlp_dataset_quality_report.csv"
SPLIT_REPORT_PATH = AI_REPORTS_DIR / "train_validation_test_split_report.csv"


RANDOM_STATE = 42

TRAIN_SIZE = 0.70
VALIDATION_SIZE = 0.15
TEST_SIZE = 0.15


REQUIRED_COLUMNS = [
    "comment_text",
    "manual_intent_label",
]


OPTIONAL_COLUMNS = [
    "comment_id",
    "live_id",
    "customer_id",
    "platform",
    "username",
    "commented_at",
    "comment_language",
    "extracted_product_keyword",
    "data_quality_status",
]


OUTPUT_COLUMNS = [
    "comment_id",
    "live_id",
    "customer_id",
    "platform",
    "comment_text",
    "comment_language",
    "manual_intent_label",
]


ALLOWED_INTENT_LABELS = {
    "purchase_intent",
    "product_question",
    "payment_question",
    "shipping_question",
    "other",
    "unknown",
}


LABEL_NORMALIZATION_MAP = {
    "purchase": "purchase_intent",
    "purchase_intent": "purchase_intent",
    "buy": "purchase_intent",
    "order": "purchase_intent",
    "achat": "purchase_intent",
    "intention_achat": "purchase_intent",

    "product": "product_question",
    "product_question": "product_question",
    "question_product": "product_question",
    "question_produit": "product_question",
    "produit": "product_question",

    "payment": "payment_question",
    "payment_question": "payment_question",
    "question_payment": "payment_question",
    "question_paiement": "payment_question",
    "paiement": "payment_question",

    "shipping": "shipping_question",
    "shipping_question": "shipping_question",
    "delivery": "shipping_question",
    "delivery_question": "shipping_question",
    "question_livraison": "shipping_question",
    "livraison": "shipping_question",

    "other": "other",
    "autre": "other",
    "neutral": "other",
    "general": "other",

    "unknown": "unknown",
    "inconnu": "unknown",
    "ambiguous": "unknown",
    "ambigu": "unknown",
}

MIN_EXAMPLES_PER_CLASS = 20


CURATED_INTENT_EXAMPLES = {
    "purchase_intent": [
        "je prends le pull rouge en M",
        "je veux commander cette robe",
        "je prends deux pièces",
        "mets-moi le sac noir de côté",
        "réserve-moi le bleu",
        "je prends la robe rouge",
        "je commande celui-là",
        "ajoute-le à mon panier",
        "je veux le même que le précédent",
        "je prends le modèle noir",
        "je confirme pour le pantalon",
        "je veux acheter ce produit",
        "garde-moi une taille M",
        "je prends 2 exemplaires",
        "ok je le prends",
    ],
    "product_question": [
        "combien coûte cette robe ?",
        "quel est le prix ?",
        "elle existe en noir ?",
        "disponible en rouge ?",
        "vous avez la taille M ?",
        "il reste du stock ?",
        "c'est quelle matière ?",
        "le pull taille grand ?",
        "vous avez d'autres couleurs ?",
        "la robe est encore disponible ?",
        "c'est disponible en taille L ?",
        "prix du sac noir ?",
        "il existe en bleu ?",
        "vous avez du medium ?",
        "c'est quelle marque ?",
    ],
    "payment_question": [
        "comment payer ?",
        "je peux payer par carte ?",
        "le lien de paiement marche ?",
        "vous acceptez paypal ?",
        "je paie maintenant",
        "paiement par CB possible ?",
        "où est le lien de paiement ?",
        "je n'arrive pas à payer",
        "vous prenez la carte bancaire ?",
        "le paiement est sécurisé ?",
        "je peux payer en plusieurs fois ?",
        "comment valider le paiement ?",
        "je dois payer où ?",
        "le paiement ne passe pas",
        "vous envoyez un lien de paiement ?",
    ],
    "shipping_question": [
        "vous livrez en Belgique ?",
        "livraison possible demain ?",
        "combien coûte la livraison ?",
        "les frais de port sont combien ?",
        "vous livrez en point relais ?",
        "livraison en France uniquement ?",
        "c'est envoyé quand ?",
        "vous faites mondial relay ?",
        "combien de temps pour recevoir ?",
        "la livraison est gratuite ?",
        "vous expédiez à l'étranger ?",
        "livraison rapide possible ?",
        "vous livrez à domicile ?",
        "quel est le délai de livraison ?",
        "je peux choisir le mode de livraison ?",
    ],
    "other": [
        "coucou",
        "merci beaucoup",
        "trop beau",
        "super live",
        "j'adore",
        "bonjour",
        "ça va ?",
        "trop sympa",
        "magnifique",
        "bravo",
        "je regarde seulement",
        "bonne soirée",
        "vous êtes au top",
        "j'aime beaucoup",
        "hello",
    ],
    "unknown": [
        "je ne sais pas",
        "peut-être",
        "à voir",
        "pas sûr",
        "hmm",
        "je réfléchis",
        "je reviens après",
        "je regarde encore",
        "pourquoi pas",
        "ça dépend",
        "je vais voir",
        "plus tard peut-être",
        "je ne comprends pas",
        "attends",
        "pas maintenant",
    ],
}


def contains_any(text: str, keywords: List[str]) -> bool:
    """
    Check if one keyword is present in the text.
    """
    return any(keyword in text for keyword in keywords)


def infer_intent_from_comment(comment_text: object) -> str:
    """
    Infer a reliable intent label from the comment text.

    This rule-based consolidation is used because the simulated raw labels
    may contain inconsistencies for identical comments.
    """
    text = normalize_text(comment_text).lower()
    text = text.replace("’", "'")

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


def consolidate_intent_label(row: pd.Series) -> str:
    """
    Consolidate the final AI label.

    The text-based label has priority because it is more consistent
    than the simulated manual label for this project.
    """
    inferred_label = infer_intent_from_comment(row.get("comment_text", ""))

    if inferred_label in ALLOWED_INTENT_LABELS:
        return inferred_label

    original_label = normalize_label(row.get("manual_intent_label", ""))

    if original_label in ALLOWED_INTENT_LABELS:
        return original_label

    return "unknown"


def add_curated_examples(df: pd.DataFrame) -> Tuple[pd.DataFrame, int]:
    """
    Add curated synthetic examples if some classes are under-represented.

    This is acceptable in this project because the dataset is simulated
    and the goal is to build a pedagogical proof of concept.
    """
    class_counts = df["manual_intent_label"].value_counts().to_dict()
    rows = []

    for label, examples in CURATED_INTENT_EXAMPLES.items():
        current_count = int(class_counts.get(label, 0))
        examples_to_add = max(0, MIN_EXAMPLES_PER_CLASS - current_count)

        for index in range(examples_to_add):
            example_text = examples[index % len(examples)]

            rows.append(
                {
                    "comment_id": f"synthetic_ai_{label}_{index + 1}",
                    "live_id": "synthetic_live",
                    "customer_id": "synthetic_customer",
                    "platform": "tiktok",
                    "username": "synthetic_user",
                    "commented_at": "",
                    "comment_language": "fr",
                    "comment_text": example_text,
                    "manual_intent_label": label,
                    "extracted_product_keyword": "",
                    "data_quality_status": "synthetic_ai_training_example",
                }
            )

    if not rows:
        return df, 0

    curated_df = pd.DataFrame(rows)
    enriched_df = pd.concat([df, curated_df], ignore_index=True)

    return enriched_df, len(rows)


def ensure_directories() -> None:
    """
    Create required directories for AI datasets and reports.
    """
    AI_DATASETS_DIR.mkdir(parents=True, exist_ok=True)
    AI_REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def is_missing_value(value: object) -> bool:
    """
    Detect missing values in a robust way.
    """
    if pd.isna(value):
        return True

    value_as_text = str(value).strip().lower()

    return value_as_text in {"", "nan", "none", "null", "na", "n/a"}


def normalize_text(value: object) -> str:
    """
    Normalize comment text without destroying useful information.
    """
    if is_missing_value(value):
        return ""

    text = str(value)
    text = " ".join(text.split())

    return text.strip()


def normalize_label(value: object) -> str:
    """
    Normalize intent labels to the expected label list.
    """
    if is_missing_value(value):
        return ""

    label = str(value).strip().lower()
    label = label.replace("-", "_").replace(" ", "_")

    return LABEL_NORMALIZATION_MAP.get(label, label)


def load_source_comments() -> pd.DataFrame:
    """
    Load cleaned live comments from Bloc 1.
    """
    if not SOURCE_COMMENTS_PATH.exists():
        raise FileNotFoundError(
            f"Source file not found: {SOURCE_COMMENTS_PATH}. "
            "Run the Bloc 1 cleaning pipeline before preparing the NLP dataset."
        )

    df = pd.read_csv(
        SOURCE_COMMENTS_PATH,
        dtype=str,
        keep_default_na=False,
        encoding="utf-8",
    )

    return df


def validate_required_columns(df: pd.DataFrame) -> None:
    """
    Validate that required columns exist in the source dataset.
    """
    missing_columns = [
        column for column in REQUIRED_COLUMNS if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing required columns in live_comments_clean.csv: "
            f"{missing_columns}"
        )


def build_nlp_dataset(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, int]]:
    """
    Build the NLP dataset used for model training.
    """
    initial_row_count = len(df)

    working_df = df.copy()

    validate_required_columns(working_df)

    for column in OPTIONAL_COLUMNS:
        if column not in working_df.columns:
            working_df[column] = ""

    working_df["comment_text"] = working_df["comment_text"].apply(normalize_text)
    working_df["manual_intent_label"] = working_df["manual_intent_label"].apply(
        normalize_label
    )

    empty_comment_count = int(
        working_df["comment_text"].apply(is_missing_value).sum()
    )

    missing_label_count = int(
        working_df["manual_intent_label"].apply(is_missing_value).sum()
    )

    working_df = working_df[
        ~working_df["comment_text"].apply(is_missing_value)
    ].copy()

    working_df = working_df[
        ~working_df["manual_intent_label"].apply(is_missing_value)
    ].copy()

    # Consolidate labels from comment text to avoid inconsistent labels.
    working_df["manual_intent_label"] = working_df.apply(
        consolidate_intent_label,
        axis=1,
    )

    invalid_label_mask = ~working_df["manual_intent_label"].isin(
        ALLOWED_INTENT_LABELS
    )

    invalid_label_count = int(invalid_label_mask.sum())

    working_df = working_df[~invalid_label_mask].copy()

    # Add curated synthetic examples to make every class learnable.
    working_df, curated_examples_added = add_curated_examples(working_df)

    duplicate_rows_before = len(working_df)

    # Keep only one label per unique comment text.
    working_df = working_df.drop_duplicates(
        subset=["comment_text"]
    ).copy()

    duplicate_rows_removed = duplicate_rows_before - len(working_df)

    available_output_columns = [
        column for column in OUTPUT_COLUMNS if column in working_df.columns
    ]

    nlp_df = working_df[available_output_columns].copy()

    nlp_df = nlp_df.sort_values(
        by=["manual_intent_label", "comment_text"],
        ascending=[True, True],
    ).reset_index(drop=True)

    preparation_stats = {
        "initial_row_count": initial_row_count,
        "curated_examples_added": curated_examples_added,
        "final_row_count": len(nlp_df),
        "empty_comment_count": empty_comment_count,
        "missing_label_count": missing_label_count,
        "invalid_label_count": invalid_label_count,
        "duplicate_rows_removed": duplicate_rows_removed,
        "removed_total_count": initial_row_count + curated_examples_added - len(nlp_df),
    }

    return nlp_df, preparation_stats


def can_stratify(labels: pd.Series) -> bool:
    """
    Check whether stratified split is possible.

    Stratified split requires at least 2 samples per class.
    """
    class_counts = labels.value_counts()

    if class_counts.empty:
        return False

    return bool((class_counts >= 2).all())


def split_dataset(
    nlp_df: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, str]:
    """
    Split the NLP dataset into train, validation and test datasets.

    Target split:
    - train: 70%
    - validation: 15%
    - test: 15%
    """
    if len(nlp_df) < 10:
        raise ValueError(
            "The NLP dataset is too small to be split correctly. "
            f"Current row count: {len(nlp_df)}"
        )

    labels = nlp_df["manual_intent_label"]

    stratify_labels: Optional[pd.Series] = labels if can_stratify(labels) else None

    train_df, temp_df = train_test_split(
        nlp_df,
        test_size=(VALIDATION_SIZE + TEST_SIZE),
        random_state=RANDOM_STATE,
        stratify=stratify_labels,
    )

    temp_labels = temp_df["manual_intent_label"]

    temp_stratify_labels: Optional[pd.Series] = (
        temp_labels if can_stratify(temp_labels) else None
    )

    validation_df, test_df = train_test_split(
        temp_df,
        test_size=0.50,
        random_state=RANDOM_STATE,
        stratify=temp_stratify_labels,
    )

    split_mode = "stratified" if stratify_labels is not None else "non_stratified"

    train_df = train_df.reset_index(drop=True)
    validation_df = validation_df.reset_index(drop=True)
    test_df = test_df.reset_index(drop=True)

    return train_df, validation_df, test_df, split_mode


def build_quality_report(
    nlp_df: pd.DataFrame,
    preparation_stats: Dict[str, int],
) -> pd.DataFrame:
    """
    Build a quality report for the NLP dataset.
    """
    rows: List[dict] = []

    for metric_name, metric_value in preparation_stats.items():
        rows.append(
            {
                "report_section": "preparation_summary",
                "metric_name": metric_name,
                "metric_value": metric_value,
                "details": "",
            }
        )

    class_distribution = nlp_df["manual_intent_label"].value_counts().to_dict()

    for label in sorted(ALLOWED_INTENT_LABELS):
        label_count = int(class_distribution.get(label, 0))
        label_rate = (
            round((label_count / len(nlp_df)) * 100, 2)
            if len(nlp_df) > 0
            else 0
        )

        rows.append(
            {
                "report_section": "class_distribution",
                "metric_name": label,
                "metric_value": label_count,
                "details": f"{label_rate}% of final NLP dataset",
            }
        )

    rows.append(
        {
            "report_section": "dataset_status",
            "metric_name": "has_required_columns",
            "metric_value": 1,
            "details": "Required columns are present.",
        }
    )

    rows.append(
        {
            "report_section": "dataset_status",
            "metric_name": "allowed_labels_only",
            "metric_value": int(
                nlp_df["manual_intent_label"].isin(ALLOWED_INTENT_LABELS).all()
            ),
            "details": "All labels belong to the allowed label list.",
        }
    )

    rows.append(
        {
            "report_section": "dataset_status",
            "metric_name": "empty_comments_remaining",
            "metric_value": int(
                nlp_df["comment_text"].apply(is_missing_value).sum()
            ),
            "details": "Should be equal to 0.",
        }
    )

    return pd.DataFrame(rows)


def build_split_report(
    train_df: pd.DataFrame,
    validation_df: pd.DataFrame,
    test_df: pd.DataFrame,
    split_mode: str,
) -> pd.DataFrame:
    """
    Build a report describing train, validation and test splits.
    """
    full_count = len(train_df) + len(validation_df) + len(test_df)

    datasets = {
        "train": train_df,
        "validation": validation_df,
        "test": test_df,
    }

    rows: List[dict] = []

    for split_name, split_df in datasets.items():
        split_count = len(split_df)
        split_rate = round((split_count / full_count) * 100, 2) if full_count else 0

        rows.append(
            {
                "report_section": "split_summary",
                "split_name": split_name,
                "label": "all",
                "row_count": split_count,
                "percentage": split_rate,
                "split_mode": split_mode,
            }
        )

        class_counts = split_df["manual_intent_label"].value_counts().to_dict()

        for label in sorted(ALLOWED_INTENT_LABELS):
            label_count = int(class_counts.get(label, 0))
            label_rate = (
                round((label_count / split_count) * 100, 2)
                if split_count
                else 0
            )

            rows.append(
                {
                    "report_section": "class_distribution_by_split",
                    "split_name": split_name,
                    "label": label,
                    "row_count": label_count,
                    "percentage": label_rate,
                    "split_mode": split_mode,
                }
            )

    return pd.DataFrame(rows)


def save_outputs(
    nlp_df: pd.DataFrame,
    train_df: pd.DataFrame,
    validation_df: pd.DataFrame,
    test_df: pd.DataFrame,
    quality_report: pd.DataFrame,
    split_report: pd.DataFrame,
) -> None:
    """
    Save datasets and reports.
    """
    nlp_df.to_csv(FULL_NLP_DATASET_PATH, index=False, encoding="utf-8")
    train_df.to_csv(TRAIN_DATASET_PATH, index=False, encoding="utf-8")
    validation_df.to_csv(VALIDATION_DATASET_PATH, index=False, encoding="utf-8")
    test_df.to_csv(TEST_DATASET_PATH, index=False, encoding="utf-8")

    quality_report.to_csv(NLP_QUALITY_REPORT_PATH, index=False, encoding="utf-8")
    split_report.to_csv(SPLIT_REPORT_PATH, index=False, encoding="utf-8")


def main() -> None:
    """
    Run the full NLP dataset preparation pipeline.
    """
    ensure_directories()

    source_df = load_source_comments()

    nlp_df, preparation_stats = build_nlp_dataset(source_df)

    if nlp_df.empty:
        raise ValueError(
            "The prepared NLP dataset is empty. "
            "Check comment_text and manual_intent_label values."
        )

    train_df, validation_df, test_df, split_mode = split_dataset(nlp_df)

    quality_report = build_quality_report(nlp_df, preparation_stats)
    split_report = build_split_report(train_df, validation_df, test_df, split_mode)

    save_outputs(
        nlp_df=nlp_df,
        train_df=train_df,
        validation_df=validation_df,
        test_df=test_df,
        quality_report=quality_report,
        split_report=split_report,
    )

    print("NLP dataset preparation completed successfully.")
    print(f"Source file: {SOURCE_COMMENTS_PATH}")
    print(f"Full NLP dataset: {FULL_NLP_DATASET_PATH}")
    print(f"Train dataset: {TRAIN_DATASET_PATH}")
    print(f"Validation dataset: {VALIDATION_DATASET_PATH}")
    print(f"Test dataset: {TEST_DATASET_PATH}")
    print(f"NLP quality report: {NLP_QUALITY_REPORT_PATH}")
    print(f"Split report: {SPLIT_REPORT_PATH}")
    print(f"Final NLP dataset rows: {len(nlp_df)}")
    print(f"Train rows: {len(train_df)}")
    print(f"Validation rows: {len(validation_df)}")
    print(f"Test rows: {len(test_df)}")
    print(f"Split mode: {split_mode}")


if __name__ == "__main__":
    main()