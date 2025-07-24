import pandas as pd
import sqlite3
from pathlib import Path

# Input/output paths
input_file = Path("../datasets/amazon/amazon.csv")
output_clean_csv = Path("../cleaned_data/clean_amazon.csv")
sqlite_db = Path("../sqlite/amazon.db")   # ✅ changed

# Load data
df = pd.read_csv(input_file)

# ---- Cleaning Steps ----
df['discounted_price'] = df['discounted_price'].str.replace('₹', '').str.replace(',', '').astype(float)
df['actual_price'] = df['actual_price'].str.replace('₹', '').str.replace(',', '').astype(float)
df['discount_percentage'] = df['discount_percentage'].str.replace('%', '').astype(float)

def clean_rating(val):
    try:
        return float(val)
    except:
        return None

df['rating'] = df['rating'].apply(clean_rating)
df['rating_count'] = df['rating_count'].fillna("0").str.replace(',', '').astype(int)
df.drop_duplicates(inplace=True)

# Save cleaned CSV
output_clean_csv.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output_clean_csv, index=False)

# Save to SQLite DB
conn = sqlite3.connect(sqlite_db)   # ✅ uses amazon.db
df.to_sql("amazon_products", conn, if_exists="replace", index=False)
conn.close()

print("✅ Cleaned and saved to CSV and SQLite DB.")
