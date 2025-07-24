import pandas as pd
import sqlite3
from pathlib import Path

# Paths
input_file = Path("../datasets/bigbasket/BigBasket Products.csv")
output_clean_csv = Path("../cleaned_data/clean_bigbasket.csv")
sqlite_db = Path("../sqlite/bigbasket.db")

# Load dataset
df = pd.read_csv(input_file)

# --- Cleaning ---

# 1. Drop 'index' column if it just duplicates row numbers
if "index" in df.columns:
    df.drop(columns=["index"], inplace=True)

# 2. Drop rows with missing product or brand
df.dropna(subset=["product", "brand"], inplace=True)

# 3. Clean 'rating' — keep as float, missing left as-is
# (you can choose to fillna(df['rating'].mean()) if needed)

# 4. Fill missing description with empty string
df["description"] = df["description"].fillna("")

# 5. Remove rows with negative or zero prices (optional)
df = df[(df["sale_price"] > 0) & (df["market_price"] > 0)]

# 6. Add discount percentage column
df["discount_percentage"] = ((df["market_price"] - df["sale_price"]) / df["market_price"]) * 100
df["discount_percentage"] = df["discount_percentage"].round(2)

# 7. Clean 'type' column formatting
df["type"] = df["type"].str.strip().str.lower()

# 8. Remove duplicates
df.drop_duplicates(inplace=True)

# --- Save cleaned data ---

# CSV
output_clean_csv.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output_clean_csv, index=False)

# SQLite DB
conn = sqlite3.connect(sqlite_db)
df.to_sql("bigbasket_products", conn, if_exists="replace", index=False)
conn.close()

print("✅ BigBasket data cleaned and saved to CSV and SQLite DB.")
