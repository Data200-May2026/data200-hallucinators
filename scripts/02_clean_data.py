import pandas as pd 

RAW_DATA_PATH = "data/raw/nutrition_indicators_npl.csv"
CLEANED_DATA_PATH = "data/processed/cleaned_nutrition_indicators_npl.csv"


def main():
    # data set load garne  

    df = pd.read_csv(RAW_DATA_PATH)

    #shape[0] = rows and shape[1] for column

    print("\n========== BEFORE CLEANING ==========")
    print(f"Rows: {df.shape[0]}")
    print(f"Column: {df.shape[1]}")
    print(f"Duplicate rows:{df.duplicated().sum()}")
    print("\nMissing values before cleaning:")
    print(df.isnull().sum())


        # 2. Rename columns for easier use
    df = df.rename(columns={
        "GHO (CODE)": "indicator_code",
        "GHO (DISPLAY)": "indicator",
        "GHO (URL)": "indicator_url",
        "YEAR (DISPLAY)": "year",
        "STARTYEAR": "start_year",
        "ENDYEAR": "end_year",
        "REGION (CODE)": "region_code",
        "REGION (DISPLAY)": "region",
        "COUNTRY (CODE)": "country_code",
        "COUNTRY (DISPLAY)": "country",
        "DIMENSION (TYPE)": "dimension_type",
        "DIMENSION (CODE)": "dimension_code",
        "DIMENSION (NAME)": "dimension_name",
        "Numeric": "numeric_value",
        "Value": "value",
        "Low": "low",
        "High": "high"
    })

    # 3. Remove duplicate rows
    df = df.drop_duplicates()

    # 4. Remove rows where main numeric value is missing
    df = df.dropna(subset=["numeric_value"])

    # 5. Fill missing dimension values
    df["dimension_type"] = df["dimension_type"].fillna("TOTAL")
    df["dimension_code"] = df["dimension_code"].fillna("TOTAL")
    df["dimension_name"] = df["dimension_name"].fillna("Total")

    # 6. Convert columns to correct data types
    df["year"] = df["year"].astype(int)
    df["start_year"] = df["start_year"].astype(int)
    df["end_year"] = df["end_year"].astype(int)

    df["numeric_value"] = pd.to_numeric(df["numeric_value"], errors="coerce")
    df["low"] = pd.to_numeric(df["low"], errors="coerce")
    df["high"] = pd.to_numeric(df["high"], errors="coerce")

    # 7. Save cleaned dataset
    df.to_csv(CLEANED_DATA_PATH, index=False)

    print("\n========== AFTER CLEANING ==========")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")
    print(f"Duplicate rows: {df.duplicated().sum()}")

    print("\nMissing values after cleaning:")
    print(df.isnull().sum())

    print("\nCleaned dataset saved to:")
    print(CLEANED_DATA_PATH)




if __name__ == "__main__":
    main()



