import pandas as pd


# -----------------------------
# Phase 1: Inspect Raw Datasets
# -----------------------------

# File path
DATA_PATH = "data/raw/nutrition_indicators_npl.csv"


def main():
    # Load dataset
    df = pd.read_csv(DATA_PATH)

    print("\n========== DATASET SHAPE ==========")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    print("\n========== FIRST 5 ROWS ==========")
    print(df.head())

    print("\n========== COLUMN NAMES ==========")
    for col in df.columns:
        print("-", col)

    print("\n========== DATA TYPES ==========")
    print(df.dtypes)

    print("\n========== MISSING VALUES ==========")
    print(df.isnull().sum())

    print("\n========== DUPLICATE ROWS ==========")
    print(f"Duplicate rows: {df.duplicated().sum()}")

    print("\n========== UNIQUE INDICATORS COUNT ==========")
    print(df["GHO (DISPLAY)"].nunique())

    print("\n========== UNIQUE NUTRITION INDICATORS ==========")
    for indicator in df["GHO (DISPLAY)"].dropna().unique():
        print("-", indicator)

    print("\n========== YEAR RANGE ==========")
    print(f"From {df['YEAR (DISPLAY)'].min()} to {df['YEAR (DISPLAY)'].max()}")

    print("\n========== COUNTRY VALUES ==========")
    print(df["COUNTRY (DISPLAY)"].unique())

    print("\n========== DIMENSION TYPES ==========")
    print(df["DIMENSION (TYPE)"].dropna().unique())


if __name__ == "__main__":
    main()