import pandas as pd

file_path = "../datasets/bigbasket/BigBasket Products.csv"

# Load CSV
df = pd.read_csv(file_path)

# Basic Info
print(f"📊 Shape: {df.shape}\n")
print(f"🧱 Columns: {list(df.columns)}\n")

print("🔍 First 5 rows:")
print(df.head(), "\n")

print("📌 Info:")
print(df.info(), "\n")

# Check for missing values
print("📉 Missing values:")
print(df.isnull().sum(), "\n")

# Describe and stats
print("📈 Stats:")
print(df.describe(include='all'), "\n")

# Unique values per column
print("🔢 Unique values per column:")
for col in df.columns:
    print(f"{col}: {df[col].nunique()}")
