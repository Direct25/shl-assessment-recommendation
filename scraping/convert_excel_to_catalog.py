import pandas as pd

INPUT_FILE = "data/evaluation/Gen_AI Dataset.xlsx"
OUTPUT_FILE = "data/raw/shl_catalog_raw.csv"

# Load Excel file
df = pd.read_excel(INPUT_FILE)

print("Original columns:", df.columns.tolist())
print("Original rows:", len(df))

# Normalize column names
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

# Try to map useful columns
column_mapping = {}

for col in df.columns:
    if "name" in col:
        column_mapping[col] = "name"
    elif "url" in col:
        column_mapping[col] = "url"
    elif "description" in col or "desc" in col:
        column_mapping[col] = "description"
    elif "test" in col:
        column_mapping[col] = "test_type"

df = df.rename(columns=column_mapping)

# Keep only relevant columns if they exist
final_cols = [c for c in ["name", "url", "description", "test_type"] if c in df.columns]
df = df[final_cols].drop_duplicates()

# Save as raw catalog
df.to_csv(OUTPUT_FILE, index=False)

print("\nCatalog CSV created successfully")
print("Final columns:", df.columns.tolist())
print("Final rows:", len(df))
print("Saved to:", OUTPUT_FILE)
