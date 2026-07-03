from pathlib import Path
import random
import string
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


# -------------------------------------------------------------------
# Global configuration
# -------------------------------------------------------------------
# This script generates raw simulated datasets for the PayLive AI Copilot project.
# The generated data intentionally contains duplicates, missing values,
# invalid dates, incorrect statuses, and inconsistent references.
#
# These issues are useful for the next step of the project:
# data cleaning, normalization, aggregation, and quality control.
# -------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"

RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)


def ensure_directories() -> None:
    """
    Create the raw data directory if it does not already exist.

    This function makes sure that the folder `data/raw` is available
    before saving the generated CSV files.
    """
    RAW_DIR.mkdir(parents=True, exist_ok=True)


def random_id(prefix: str, number: int, width: int = 4) -> str:
    """
    Generate a readable technical identifier.

    Example:
    random_id("SEL", 1) returns "SEL0001".

    This is used to create IDs for sellers, customers, products,
    lives, carts, orders, payments, and events.
    """
    return f"{prefix}{str(number).zfill(width)}"


def random_date(start_date: datetime, max_days: int = 90) -> datetime:
    """
    Generate a random datetime starting from a given date.

    This function helps simulate realistic creation dates,
    live dates, payment dates, and event timestamps.
    """
    return start_date + timedelta(
        days=random.randint(0, max_days),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59),
    )


def random_email(name: str, domain: str = "example.com") -> str:
    """
    Generate a fake email address from a name.

    The generated emails are not real. They are only used for simulation
    and RGPD-friendly testing purposes.
    """
    clean_name = name.lower().replace(" ", ".").replace("_", ".")
    return f"{clean_name}@{domain}"


def inject_duplicate_rows(df: pd.DataFrame, n_duplicates: int) -> pd.DataFrame:
    """
    Add duplicated rows to a DataFrame.

    This function intentionally injects duplicate records into the data.
    These duplicates will later be detected and removed during
    the cleaning phase.
    """
    if len(df) == 0 or n_duplicates <= 0:
        return df

    duplicates = df.sample(n=min(n_duplicates, len(df)), random_state=RANDOM_SEED)
    return pd.concat([df, duplicates], ignore_index=True)


def save_csv(df: pd.DataFrame, filename: str) -> None:
    """
    Save a DataFrame as a CSV file inside the raw data folder.

    All raw generated files are saved in `data/raw`.
    These files must not be manually modified later.
    """
    output_path = RAW_DIR / filename
    df.to_csv(output_path, index=False, encoding="utf-8")


def generate_sellers(n: int = 20) -> pd.DataFrame:
    """
    Generate fake seller data.

    This dataset represents sellers using the PayLive platform.
    It includes shop names, owner names, emails, phone numbers,
    countries, preferred platforms, creation dates, and statuses.

    Intentional data quality issues are added:
    - invalid email;
    - missing country;
    - duplicated seller ID;
    - invalid creation date;
    - missing phone number;
    - non-standard platform names;
    - invalid seller statuses.
    """
    platforms = ["tiktok", "instagram", "TikTok", "insta", "tik tok", "Instagram"]
    countries = ["France", "Belgique", "Maroc", "Espagne", "Allemagne", ""]
    statuses = ["active", "inactive", "suspended", "actif", "ok", "deleted"]

    rows = []

    for i in range(1, n + 1):
        shop_name = f"LiveShop_{i}"
        first_name = random.choice(
            ["Lina", "Sofia", "Karim", "Nora", "Adam", "Yanis", "Emma", "Sarah"]
        )
        last_name = random.choice(
            ["Martin", "Benali", "Durand", "Moreau", "Petit", "Robert"]
        )

        rows.append(
            {
                "seller_id": random_id("SEL", i),
                "shop_name": shop_name,
                "owner_first_name": first_name,
                "owner_last_name": last_name,
                "email": random_email(f"{first_name}.{last_name}.{i}"),
                "phone_number": f"+33{random.randint(600000000, 799999999)}",
                "country": random.choice(countries),
                "main_platform": random.choice(platforms),
                "created_at": random_date(datetime(2025, 1, 1)).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "seller_status": random.choice(statuses),
            }
        )

    df = pd.DataFrame(rows)

    # Intentional issues for future cleaning.
    df.loc[1, "email"] = "email_invalide"
    df.loc[3, "country"] = ""
    df.loc[5, "seller_id"] = df.loc[4, "seller_id"]
    df.loc[7, "created_at"] = "invalid_date"
    df.loc[9, "phone_number"] = ""

    df = inject_duplicate_rows(df, n_duplicates=3)

    return df


def generate_customers(n: int = 80) -> pd.DataFrame:
    """
    Generate fake customer data.

    This dataset represents viewers or buyers interacting during live sales.
    Customers are simulated with usernames, platforms, optional emails,
    countries, and creation dates.

    Intentional data quality issues are added:
    - missing username;
    - invalid email;
    - duplicated customer ID;
    - invalid date;
    - non-standard platform values.
    """
    platforms = ["tiktok", "instagram", "TikTok", "insta", "ig", "Instagram"]
    countries = ["France", "Belgique", "Maroc", "Espagne", "", "Italie"]

    rows = []

    for i in range(1, n + 1):
        username = random.choice(
            ["lina", "sarah", "mode", "shop", "nora", "adam", "client", "livefan"]
        )
        username = f"{username}_{random.randint(10, 9999)}"

        rows.append(
            {
                "customer_id": random_id("CUS", i),
                "username": username,
                "platform": random.choice(platforms),
                "email": random_email(username) if random.random() > 0.30 else "",
                "country": random.choice(countries),
                "created_at": random_date(datetime(2025, 6, 1)).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
            }
        )

    df = pd.DataFrame(rows)

    # Intentional issues for future cleaning.
    df.loc[2, "username"] = ""
    df.loc[4, "email"] = "client@@bad-email"
    df.loc[8, "customer_id"] = df.loc[7, "customer_id"]
    df.loc[11, "created_at"] = "2025/99/99"
    df.loc[15, "platform"] = "tik tok"

    df = inject_duplicate_rows(df, n_duplicates=5)

    return df


def generate_products(n: int = 60) -> pd.DataFrame:
    """
    Generate fake product catalog data.

    This dataset represents products that can be presented and sold
    during live shopping sessions.

    Intentional data quality issues are added:
    - negative price;
    - negative stock;
    - missing category;
    - duplicated product ID;
    - invalid date;
    - inconsistent product names;
    - non-standard product statuses.
    """
    categories = [
        "clothing",
        "beauty",
        "accessories",
        "home",
        "Clothes",
        "mode",
        "",
        "cosmetics",
    ]
    brands = ["PayLive Demo", "UrbanStyle", "ModaPlus", "BeautyLab", "NoBrand", ""]
    product_names = [
        "Robe rouge",
        "Sac noir",
        "Jean slim",
        "T-shirt blanc",
        "Veste beige",
        "Sneakers",
        "Montre dorée",
        "Palette maquillage",
        "Pull oversize",
        "Chemise bleue",
    ]

    rows = []

    for i in range(1, n + 1):
        price = round(random.uniform(9.90, 129.90), 2)
        stock = random.randint(0, 200)

        rows.append(
            {
                "product_id": random_id("PROD", i),
                "product_name": random.choice(product_names),
                "category": random.choice(categories),
                "brand": random.choice(brands),
                "description": f"Produit de démonstration numéro {i}",
                "unit_price": price,
                "stock_quantity": stock,
                "product_status": random.choice(
                    ["active", "inactive", "out_of_stock", "available", "ok"]
                ),
                "source": "simulation",
                "created_at": random_date(datetime(2025, 5, 1)).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
            }
        )

    df = pd.DataFrame(rows)

    # Intentional issues for future cleaning.
    df.loc[0, "unit_price"] = -15.00
    df.loc[3, "stock_quantity"] = -4
    df.loc[5, "category"] = ""
    df.loc[7, "product_name"] = df.loc[6, "product_name"].upper()
    df.loc[9, "created_at"] = "not_a_date"
    df.loc[12, "product_id"] = df.loc[11, "product_id"]

    df = inject_duplicate_rows(df, n_duplicates=4)

    return df


def generate_live_sessions(sellers: pd.DataFrame, n: int = 35) -> pd.DataFrame:
    """
    Generate fake live session data.

    This dataset represents TikTok, Instagram, or other live shopping sessions.
    Each live is linked to a seller.

    Intentional data quality issues are added:
    - seller ID that does not exist;
    - end date before start date;
    - invalid start date;
    - duplicated live ID;
    - missing currency;
    - non-standard platform and status values.
    """
    seller_ids = sellers["seller_id"].dropna().unique().tolist()
    platforms = ["tiktok", "instagram", "TikTok", "insta", "youtube_live"]

    rows = []

    for i in range(1, n + 1):
        start = random_date(datetime(2026, 1, 1), max_days=120)
        end = start + timedelta(hours=random.randint(1, 4), minutes=random.randint(0, 59))

        rows.append(
            {
                "live_id": random_id("LIVE", i),
                "seller_id": random.choice(seller_ids),
                "platform": random.choice(platforms),
                "live_title": random.choice(
                    [
                        "Live nouveautés mode",
                        "Déstockage spécial",
                        "Collection printemps",
                        "Offres beauté",
                        "Live accessoires",
                    ]
                ),
                "scheduled_start_at": (start - timedelta(days=1)).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "actual_start_at": start.strftime("%Y-%m-%d %H:%M:%S"),
                "ended_at": end.strftime("%Y-%m-%d %H:%M:%S"),
                "live_status": random.choice(
                    ["scheduled", "live", "ended", "cancelled", "done", "active"]
                ),
                "peak_viewers": random.randint(20, 2500),
                "currency": random.choice(["EUR", "eur", "€", "", "USD"]),
                "created_at": (start - timedelta(days=random.randint(1, 20))).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
            }
        )

    df = pd.DataFrame(rows)

    # Intentional issues for future cleaning.
    df.loc[1, "seller_id"] = "SEL9999"
    df.loc[3, "ended_at"] = "2024-01-01 10:00:00"
    df.loc[5, "actual_start_at"] = "invalid_date"
    df.loc[7, "live_id"] = df.loc[6, "live_id"]
    df.loc[9, "currency"] = ""

    df = inject_duplicate_rows(df, n_duplicates=3)

    return df


def generate_live_products(
    live_sessions: pd.DataFrame,
    products: pd.DataFrame,
    n: int = 120,
) -> pd.DataFrame:
    """
    Generate the relationship between lives and products.

    This dataset shows which products were presented during each live session.

    Intentional data quality issues are added:
    - product ID that does not exist;
    - live ID that does not exist;
    - remaining stock greater than initial stock;
    - negative live price;
    - duplicated live-product relationships.
    """
    live_ids = live_sessions["live_id"].dropna().unique().tolist()
    product_ids = products["product_id"].dropna().unique().tolist()

    rows = []

    for i in range(1, n + 1):
        initial_stock = random.randint(5, 120)
        remaining_stock = random.randint(0, initial_stock)

        rows.append(
            {
                "live_product_id": random_id("LPR", i),
                "live_id": random.choice(live_ids),
                "product_id": random.choice(product_ids),
                "display_order": random.randint(1, 30),
                "special_live_price": round(random.uniform(5.0, 120.0), 2),
                "initial_stock": initial_stock,
                "remaining_stock": remaining_stock,
            }
        )

    df = pd.DataFrame(rows)

    # Intentional issues for future cleaning.
    df.loc[2, "product_id"] = "PROD9999"
    df.loc[4, "live_id"] = "LIVE9999"
    df.loc[6, "remaining_stock"] = df.loc[6, "initial_stock"] + 20
    df.loc[8, "special_live_price"] = -8.90
    df.loc[10, "live_id"] = df.loc[11, "live_id"]
    df.loc[10, "product_id"] = df.loc[11, "product_id"]

    df = inject_duplicate_rows(df, n_duplicates=5)

    return df


def generate_live_comments(
    live_sessions: pd.DataFrame,
    customers: pd.DataFrame,
    n: int = 350,
) -> pd.DataFrame:
    """
    Generate fake live comments.

    This dataset is important for the future AI part of the project.
    It simulates comments written by viewers during live shopping sessions.

    Intentional data quality issues are added:
    - duplicated comments;
    - missing live ID;
    - customer ID that does not exist;
    - invalid date;
    - missing username;
    - empty comment text;
    - non-standard platform names;
    - spelling mistakes in comments;
    - non-normalized intent labels.
    """
    live_ids = live_sessions["live_id"].dropna().unique().tolist()
    customer_ids = customers["customer_id"].dropna().unique().tolist()
    usernames = customers["username"].dropna().tolist()

    platforms = ["tiktok", "instagram", "TikTok", "insta", "ig"]

    labels = [
        "purchase_intent",
        "price_question",
        "stock_question",
        "payment_question",
        "complaint",
        "other",
        "achat",
        "question",
    ]

    comments = [
        "Je prends la robe rouge en M",
        "Prix ?",
        "Dispo en noir taille L ?",
        "Réserve-moi le bleu",
        "Je veux 2 pièces",
        "Comment payer ?",
        "C’est trop cher",
        "Je prends le sac noir",
        "Tu as la taille medium ?",
        "Je veux le même que le précédent",
        "Disponible en rouge ?",
        "Je paye maintenant",
        "Mets-moi de côté le pull beige",
        "Je prend le rouge en meduim",
        "Coucou",
        "",
    ]

    rows = []

    for i in range(1, n + 1):
        commented_at = random_date(datetime(2026, 1, 1), max_days=120)

        rows.append(
            {
                "comment_id": random_id("COM", i, width=5),
                "live_id": random.choice(live_ids),
                "customer_id": random.choice(customer_ids),
                "platform": random.choice(platforms),
                "username": random.choice(usernames),
                "comment_text": random.choice(comments),
                "commented_at": random.choice(
                    [
                        commented_at.strftime("%Y-%m-%d %H:%M:%S"),
                        commented_at.strftime("%d/%m/%Y %H:%M"),
                        commented_at.strftime("%Y/%m/%d"),
                    ]
                ),
                "comment_language": random.choice(["fr", "en", "ar", "", "FR"]),
                "manual_intent_label": random.choice(labels),
                "extracted_product_keyword": random.choice(
                    ["robe", "sac", "pull", "jean", "veste", "", "unknown"]
                ),
                "data_quality_status": "raw",
            }
        )

    df = pd.DataFrame(rows)

    # Intentional issues for future cleaning.
    df.loc[0, "comment_id"] = df.loc[1, "comment_id"]
    df.loc[3, "live_id"] = ""
    df.loc[5, "customer_id"] = "CUS9999"
    df.loc[7, "commented_at"] = "invalid_date"
    df.loc[9, "username"] = ""
    df.loc[11, "comment_text"] = ""
    df.loc[13, "platform"] = "tik tok"

    df = inject_duplicate_rows(df, n_duplicates=15)

    return df


def generate_carts(
    live_sessions: pd.DataFrame,
    customers: pd.DataFrame,
    n: int = 120,
) -> pd.DataFrame:
    """
    Generate fake shopping carts.

    This dataset represents carts created during or after live sessions.

    Intentional data quality issues are added:
    - missing customer;
    - live ID that does not exist;
    - negative total amount;
    - update date before creation date;
    - invalid cart status;
    - duplicated cart ID.
    """
    live_ids = live_sessions["live_id"].dropna().unique().tolist()
    customer_ids = customers["customer_id"].dropna().unique().tolist()

    rows = []

    for i in range(1, n + 1):
        created_at = random_date(datetime(2026, 1, 1), max_days=120)
        total_amount = round(random.uniform(10.0, 250.0), 2)

        rows.append(
            {
                "cart_id": random_id("CART", i),
                "live_id": random.choice(live_ids),
                "customer_id": random.choice(customer_ids),
                "cart_status": random.choice(
                    [
                        "created",
                        "pending_payment",
                        "paid",
                        "abandoned",
                        "cancelled",
                        "done",
                        "waiting",
                    ]
                ),
                "created_at": created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": (created_at + timedelta(minutes=random.randint(1, 120))).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "total_amount": total_amount,
                "currency": random.choice(["EUR", "eur", "€", "", "USD"]),
            }
        )

    df = pd.DataFrame(rows)

    # Intentional issues for future cleaning.
    df.loc[2, "customer_id"] = ""
    df.loc[4, "live_id"] = "LIVE9999"
    df.loc[6, "total_amount"] = -20.00
    df.loc[8, "updated_at"] = "2020-01-01 10:00:00"
    df.loc[10, "cart_status"] = "unknown_status"
    df.loc[12, "cart_id"] = df.loc[11, "cart_id"]

    df = inject_duplicate_rows(df, n_duplicates=6)

    return df


def generate_cart_items(
    carts: pd.DataFrame,
    products: pd.DataFrame,
    n: int = 220,
) -> pd.DataFrame:
    """
    Generate fake cart item lines.

    This dataset contains the products added to each cart.

    Intentional data quality issues are added:
    - zero quantity;
    - negative quantity;
    - product ID that does not exist;
    - missing unit price;
    - incorrect line total;
    - cart ID that does not exist;
    - duplicated cart item ID;
    - non-normalized sizes and colors.
    """
    cart_ids = carts["cart_id"].dropna().unique().tolist()
    product_ids = products["product_id"].dropna().unique().tolist()

    sizes = ["XS", "S", "M", "L", "XL", "m", "Medium", "meduim", "", "unique"]
    colors = ["red", "rouge", "rge", "black", "noir", "blue", "bleu", "", "beige"]

    rows = []

    for i in range(1, n + 1):
        quantity = random.randint(1, 4)
        unit_price = round(random.uniform(8.0, 120.0), 2)

        rows.append(
            {
                "cart_item_id": random_id("CI", i),
                "cart_id": random.choice(cart_ids),
                "product_id": random.choice(product_ids),
                "quantity": quantity,
                "unit_price": unit_price,
                "line_total": round(quantity * unit_price, 2),
                "selected_size": random.choice(sizes),
                "selected_color": random.choice(colors),
            }
        )

    df = pd.DataFrame(rows)

    # Intentional issues for future cleaning.
    df.loc[1, "quantity"] = 0
    df.loc[3, "quantity"] = -2
    df.loc[5, "product_id"] = "PROD9999"
    df.loc[7, "unit_price"] = np.nan
    df.loc[9, "line_total"] = 9999.99
    df.loc[11, "cart_id"] = "CART9999"
    df.loc[13, "cart_item_id"] = df.loc[12, "cart_item_id"]

    df = inject_duplicate_rows(df, n_duplicates=8)

    return df


def generate_orders(
    carts: pd.DataFrame,
    sellers: pd.DataFrame,
    n: int = 90,
) -> pd.DataFrame:
    """
    Generate fake order data.

    Orders are created from carts and linked to sellers and customers.

    Intentional data quality issues are added:
    - missing cart ID;
    - customer ID that does not exist;
    - negative order amount;
    - confirmation date before creation date;
    - invalid order status;
    - duplicated order ID.
    """
    cart_ids = carts["cart_id"].dropna().unique().tolist()
    seller_ids = sellers["seller_id"].dropna().unique().tolist()
    customer_ids = carts["customer_id"].dropna().unique().tolist()

    rows = []

    for i in range(1, n + 1):
        created_at = random_date(datetime(2026, 1, 1), max_days=120)
        amount = round(random.uniform(10.0, 300.0), 2)

        rows.append(
            {
                "order_id": random_id("ORD", i),
                "cart_id": random.choice(cart_ids),
                "customer_id": random.choice(customer_ids),
                "seller_id": random.choice(seller_ids),
                "order_status": random.choice(
                    ["pending", "confirmed", "paid", "cancelled", "refunded", "done", "ok"]
                ),
                "order_amount": amount,
                "currency": random.choice(["EUR", "eur", "€", "", "USD"]),
                "created_at": created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "confirmed_at": (created_at + timedelta(minutes=random.randint(1, 180))).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
            }
        )

    df = pd.DataFrame(rows)

    # Intentional issues for future cleaning.
    df.loc[2, "cart_id"] = ""
    df.loc[4, "customer_id"] = "CUS9999"
    df.loc[6, "order_amount"] = -50.00
    df.loc[8, "confirmed_at"] = "2020-01-01 10:00:00"
    df.loc[10, "order_status"] = "unknown"
    df.loc[12, "order_id"] = df.loc[11, "order_id"]

    df = inject_duplicate_rows(df, n_duplicates=5)

    return df


def generate_payments(orders: pd.DataFrame, n: int = 95) -> pd.DataFrame:
    """
    Generate fake payment data.

    This dataset simulates payment transactions.
    No real banking data is used.

    Intentional data quality issues are added:
    - order ID that does not exist;
    - negative payment amount;
    - successful payment without payment date;
    - invalid currency;
    - duplicated transaction reference;
    - duplicated payment ID;
    - non-standard payment statuses.
    """
    order_ids = orders["order_id"].dropna().unique().tolist()

    rows = []

    for i in range(1, n + 1):
        paid_at = random_date(datetime(2026, 1, 1), max_days=120)

        rows.append(
            {
                "payment_id": random_id("PAY", i),
                "order_id": random.choice(order_ids),
                "payment_provider": random.choice(
                    ["stripe", "paypal", "paylive_mock", "Stripe", ""]
                ),
                "payment_status": random.choice(
                    ["pending", "succeeded", "failed", "refunded", "success", "ok"]
                ),
                "payment_amount": round(random.uniform(10.0, 300.0), 2),
                "currency": random.choice(["EUR", "eur", "€", "", "USD"]),
                "payment_method": random.choice(["card", "wallet", "bank_transfer", "", "cb"]),
                "paid_at": paid_at.strftime("%Y-%m-%d %H:%M:%S"),
                "transaction_reference": "TX-"
                + "".join(random.choices(string.ascii_uppercase + string.digits, k=10)),
            }
        )

    df = pd.DataFrame(rows)

    # Intentional issues for future cleaning.
    df.loc[1, "order_id"] = "ORD9999"
    df.loc[3, "payment_amount"] = -10.00
    df.loc[5, "payment_status"] = "succeeded"
    df.loc[5, "paid_at"] = ""
    df.loc[7, "currency"] = "GBP"
    df.loc[9, "transaction_reference"] = df.loc[8, "transaction_reference"]
    df.loc[11, "payment_id"] = df.loc[10, "payment_id"]

    df = inject_duplicate_rows(df, n_duplicates=7)

    return df


def generate_stock_movements(
    products: pd.DataFrame,
    live_sessions: pd.DataFrame,
    n: int = 160,
) -> pd.DataFrame:
    """
    Generate fake stock movement data.

    This dataset tracks stock changes caused by sales, returns,
    manual corrections, or restocking.

    Intentional data quality issues are added:
    - product ID that does not exist;
    - zero quantity change;
    - invalid movement type;
    - invalid date;
    - duplicated stock movement ID.
    """
    product_ids = products["product_id"].dropna().unique().tolist()
    live_ids = live_sessions["live_id"].dropna().unique().tolist()

    rows = []

    for i in range(1, n + 1):
        movement_type = random.choice(
            ["sale", "return", "adjustment", "restock", "sold", "unknown"]
        )
        quantity = random.randint(-20, 50)

        rows.append(
            {
                "stock_movement_id": random_id("SM", i),
                "product_id": random.choice(product_ids),
                "live_id": random.choice(live_ids),
                "movement_type": movement_type,
                "quantity_change": quantity,
                "movement_reason": random.choice(
                    ["live sale", "manual correction", "return", "new stock", ""]
                ),
                "created_at": random_date(datetime(2026, 1, 1), max_days=120).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
            }
        )

    df = pd.DataFrame(rows)

    # Intentional issues for future cleaning.
    df.loc[2, "product_id"] = "PROD9999"
    df.loc[4, "quantity_change"] = 0
    df.loc[6, "movement_type"] = "bad_type"
    df.loc[8, "created_at"] = "invalid_date"
    df.loc[10, "stock_movement_id"] = df.loc[9, "stock_movement_id"]

    df = inject_duplicate_rows(df, n_duplicates=6)

    return df


def generate_live_events(
    live_sessions: pd.DataFrame,
    customers: pd.DataFrame,
    n: int = 1000,
) -> pd.DataFrame:
    """
    Generate fake live event logs.

    This dataset simulates a high-volume event source.
    It can later be processed as a big data-like source.

    Events include comments, cart openings, payment clicks,
    successful payments, API errors, and product views.

    Intentional data quality issues are added:
    - duplicated event ID;
    - live ID that does not exist;
    - invalid timestamp;
    - unknown event type;
    - missing source system.
    """
    live_ids = live_sessions["live_id"].dropna().unique().tolist()
    customer_ids = customers["customer_id"].dropna().unique().tolist()

    event_types = [
        "comment_sent",
        "cart_opened",
        "payment_clicked",
        "payment_succeeded",
        "api_error",
        "product_viewed",
        "unknown_event",
    ]

    rows = []

    for i in range(1, n + 1):
        rows.append(
            {
                "event_id": random_id("EVT", i, width=6),
                "live_id": random.choice(live_ids),
                "customer_id": random.choice(customer_ids),
                "event_type": random.choice(event_types),
                "event_timestamp": random_date(datetime(2026, 1, 1), max_days=120).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "event_value": random.choice(
                    ["", "success", "timeout", "button_click", "checkout"]
                ),
                "source_system": random.choice(
                    ["web_app", "payment_service", "live_connector", "", "api_gateway"]
                ),
            }
        )

    df = pd.DataFrame(rows)

    # Intentional issues for future cleaning.
    df.loc[2, "event_id"] = df.loc[1, "event_id"]
    df.loc[4, "live_id"] = "LIVE9999"
    df.loc[6, "event_timestamp"] = "invalid_date"
    df.loc[8, "event_type"] = "bad_event"
    df.loc[10, "source_system"] = ""

    df = inject_duplicate_rows(df, n_duplicates=20)

    return df


def generate_quality_summary() -> pd.DataFrame:
    """
    Generate a summary of the intentional data quality issues.

    This file is useful for documentation and for the final report.
    It explains which problems were injected into each raw dataset
    and why they were useful for the project.
    """
    rows = [
        {
            "file_name": "sellers_raw.csv",
            "injected_issues": (
                "invalid emails, duplicated seller_id, missing country, "
                "non-standard platform, invalid date"
            ),
            "purpose": "Test seller normalization and identifier quality.",
        },
        {
            "file_name": "customers_raw.csv",
            "injected_issues": (
                "missing username, invalid emails, duplicated customer_id, "
                "non-standard platforms"
            ),
            "purpose": "Test customer data quality and pseudonymization logic.",
        },
        {
            "file_name": "live_sessions_raw.csv",
            "injected_issues": (
                "non-existing seller_id, invalid date, end before start, "
                "missing currency, incorrect statuses"
            ),
            "purpose": "Test temporal and relational consistency of live sessions.",
        },
        {
            "file_name": "products_raw.csv",
            "injected_issues": (
                "negative price, negative stock, missing category, duplicated product_id"
            ),
            "purpose": "Test product catalog cleaning.",
        },
        {
            "file_name": "live_comments_raw.csv",
            "injected_issues": (
                "duplicates, empty text, missing live_id, invalid date, "
                "spelling mistakes, non-normalized labels"
            ),
            "purpose": "Prepare future AI analysis of purchase intentions.",
        },
        {
            "file_name": "payments_raw.csv",
            "injected_issues": (
                "non-existing order, negative amount, successful payment without date, "
                "invalid currency, duplicated transaction reference"
            ),
            "purpose": "Test payment consistency checks.",
        },
        {
            "file_name": "live_events_raw.csv",
            "injected_issues": (
                "duplicated events, non-existing live, invalid timestamp, unknown event type"
            ),
            "purpose": "Simulate a high-volume event log source.",
        },
    ]

    return pd.DataFrame(rows)


def main() -> None:
    """
    Run the full raw data generation process.

    This function orchestrates the whole script:
    - create the raw data directory;
    - generate all raw datasets;
    - inject intentional data quality issues;
    - save every dataset as a CSV file;
    - print a short execution summary.
    """
    ensure_directories()

    sellers = generate_sellers()
    customers = generate_customers()
    products = generate_products()
    live_sessions = generate_live_sessions(sellers)
    live_products = generate_live_products(live_sessions, products)
    live_comments = generate_live_comments(live_sessions, customers)
    carts = generate_carts(live_sessions, customers)
    cart_items = generate_cart_items(carts, products)
    orders = generate_orders(carts, sellers)
    payments = generate_payments(orders)
    stock_movements = generate_stock_movements(products, live_sessions)
    live_events = generate_live_events(live_sessions, customers)
    quality_summary = generate_quality_summary()

    save_csv(sellers, "sellers_raw.csv")
    save_csv(customers, "customers_raw.csv")
    save_csv(products, "products_raw.csv")
    save_csv(live_sessions, "live_sessions_raw.csv")
    save_csv(live_products, "live_products_raw.csv")
    save_csv(live_comments, "live_comments_raw.csv")
    save_csv(carts, "carts_raw.csv")
    save_csv(cart_items, "cart_items_raw.csv")
    save_csv(orders, "orders_raw.csv")
    save_csv(payments, "payments_raw.csv")
    save_csv(stock_movements, "stock_movements_raw.csv")
    save_csv(live_events, "live_events_raw.csv")
    save_csv(quality_summary, "data_quality_issues_summary.csv")

    print("Raw simulated data generated successfully in data/raw/")
    print(f"Sellers generated: {len(sellers)}")
    print(f"Customers generated: {len(customers)}")
    print(f"Products generated: {len(products)}")
    print(f"Live sessions generated: {len(live_sessions)}")
    print(f"Live comments generated: {len(live_comments)}")
    print(f"Payments generated: {len(payments)}")
    print(f"Live events generated: {len(live_events)}")


if __name__ == "__main__":
    main()