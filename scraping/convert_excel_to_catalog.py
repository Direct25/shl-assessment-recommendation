import pandas as pd

INPUT_FILE = "data/evaluation/Gen_AI Dataset.xlsx"
OUTPUT_FILE = "data/raw/shl_catalog_raw.csv"

df = pd.read_excel(INPUT_FILE)

print("Original columns:", df.columns.tolist())
print("Original rows:", len(df))

df = df.rename(columns={
    "Query": "title",
    "Assessment_url": "url"
})

df = df[["title", "url"]].dropna().drop_duplicates()

df.to_csv(OUTPUT_FILE, index=False)

print("Catalog CSV created successfully")
print("Final columns:", df.columns.tolist())
print("Final rows:", len(df))
print(f"Saved to: {OUTPUT_FILE}")
