import pandas as pd

CLEANED_DATA_PATH = "data/processed/cleaned_nutrition_indicators_npl.csv"

df = pd.read_csv(CLEANED_DATA_PATH)

#cleaned

print("\n========== CLEANED DATA CHECK ==========")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nMissing values:")
print(df.isnull().sum())

print("\nColumn names:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)

print("\nYear range:")
print(df["year"].min(), "to", df["year"].max())

print("\nUnique indicators:")
print(df["indicator"].nunique())

print("\nDimension types:")
print(df["dimension_type"].unique())