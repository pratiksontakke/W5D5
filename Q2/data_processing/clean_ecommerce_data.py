import pandas as pd
import sqlite3
from pathlib import Path

# === Setup paths ===
input_dir = Path("../datasets/ecommerce")
output_csv_dir = Path("../cleaned_data/ecommerce")
sqlite_db_path = Path("../sqlite/ecommerce.db")

# Create folders if they don’t exist
output_csv_dir.mkdir(parents=True, exist_ok=True)
sqlite_db_path.parent.mkdir(parents=True, exist_ok=True)

# Connect to DB
conn = sqlite3.connect(sqlite_db_path)

# 1. olist_order_items_dataset.csv
df_items = pd.read_csv(input_dir / "olist_order_items_dataset.csv")
# No nulls, but remove duplicates
df_items.drop_duplicates(inplace=True)
df_items.to_csv(output_csv_dir / "clean_order_items.csv", index=False)
df_items.to_sql("order_items", conn, if_exists="replace", index=False)

# 2. olist_order_reviews_dataset.csv
df_reviews = pd.read_csv(input_dir / "olist_order_reviews_dataset.csv")
df_reviews["review_comment_title"] = df_reviews["review_comment_title"].fillna("")
df_reviews["review_comment_message"] = df_reviews["review_comment_message"].fillna("")
df_reviews["review_creation_date"] = pd.to_datetime(df_reviews["review_creation_date"])
df_reviews["review_answer_timestamp"] = pd.to_datetime(df_reviews["review_answer_timestamp"])
df_reviews.drop_duplicates(inplace=True)
df_reviews.to_csv(output_csv_dir / "clean_order_reviews.csv", index=False)
df_reviews.to_sql("order_reviews", conn, if_exists="replace", index=False)

# 3. olist_orders_dataset.csv
df_orders = pd.read_csv(input_dir / "olist_orders_dataset.csv")
df_orders["order_approved_at"] = pd.to_datetime(df_orders["order_approved_at"])
df_orders["order_purchase_timestamp"] = pd.to_datetime(df_orders["order_purchase_timestamp"])
df_orders["order_delivered_carrier_date"] = pd.to_datetime(df_orders["order_delivered_carrier_date"])
df_orders["order_delivered_customer_date"] = pd.to_datetime(df_orders["order_delivered_customer_date"])
df_orders["order_estimated_delivery_date"] = pd.to_datetime(df_orders["order_estimated_delivery_date"])
df_orders.drop_duplicates(inplace=True)
df_orders.to_csv(output_csv_dir / "clean_orders.csv", index=False)
df_orders.to_sql("orders", conn, if_exists="replace", index=False)

# 4. olist_products_dataset.csv
df_products = pd.read_csv(input_dir / "olist_products_dataset.csv")
df_products.dropna(subset=["product_id"], inplace=True)
df_products.fillna({
    "product_category_name": "",
    "product_name_lenght": 0,
    "product_description_lenght": 0,
    "product_photos_qty": 0,
    "product_weight_g": 0,
    "product_length_cm": 0,
    "product_height_cm": 0,
    "product_width_cm": 0
}, inplace=True)
df_products.drop_duplicates(inplace=True)
df_products.to_csv(output_csv_dir / "clean_products.csv", index=False)
df_products.to_sql("products", conn, if_exists="replace", index=False)

# 5. product_category_name_translation.csv
df_translation = pd.read_csv(input_dir / "product_category_name_translation.csv")
df_translation.drop_duplicates(inplace=True)
df_translation.to_csv(output_csv_dir / "clean_category_translation.csv", index=False)
df_translation.to_sql("category_translation", conn, if_exists="replace", index=False)

# Close DB
conn.close()

print("✅ All ecommerce files cleaned and saved to CSV & SQLite DB.")
