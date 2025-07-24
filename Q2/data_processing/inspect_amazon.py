import pandas as pd

df = pd.read_csv("../datasets/amazon/amazon.csv")

print("📊 Shape:", df.shape)
print("\n🧱 Columns:", df.columns.tolist())

print("\n🔍 First 5 rows:")
print(df.head())

print("\n📌 Info:")
print(df.info())

print("\n📉 Missing values:")
print(df.isnull().sum())

print("\n📈 Stats:")
print(df.describe())

print("\n🔢 Unique values per column:")
for col in df.columns:
    print(f"{col}: {df[col].nunique()}")
