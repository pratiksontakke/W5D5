import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # Q2/
ecom_path = BASE_DIR / "datasets" / "ecommerce"

files = sorted(ecom_path.glob("*.csv"))

print(f"🔎 Found {len(files)} files in {ecom_path.resolve()}")

for file in files:
    print(f"\n📁 Inspecting: {file.name}")
    try:
        df = pd.read_csv(file, encoding="utf-8", low_memory=False)
        print(f"📊 Shape: {df.shape}")
        print(f"🧱 Columns: {df.columns.tolist()}")
        print(df.head(3))
        print("📉 Null values:")
        print(df.isnull().sum())
    except Exception as e:
        print(f"❌ Error loading {file.name}: {e}")
    print("-" * 60)
