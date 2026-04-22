import pandas as pd
import os

def clean_data():
    # Absolute base path (your project folder)
    base_path = r"C:\Users\PC\Desktop\My Portfolio Projects\Experiment-Driven Pricing Analytics for E-Commerce Growth"

    # File paths
    input_path = os.path.join(base_path, "data", "raw", "global_ecommerce_sales.csv")
    output_path = os.path.join(base_path, "data", "processed", "cleaned_data_final.csv")

    # Load data
    df = pd.read_csv(input_path)

    # Convert date (handle mixed formats properly)
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], format='mixed', dayfirst=True)

    # Create time features
    df["Month"] = df["Order_Date"].dt.month.astype(int)
    df["Quarter"] = df["Order_Date"].dt.quarter.astype(int)
    df["Year"] = df["Order_Date"].dt.year.astype(int)

    # Validate revenue (optional check)
    df["calculated_amount"] = (df["Unit_Price"] * df["Quantity"]).round(2)

    # Standardize column names
    df.columns = df.columns.str.lower()

    # Drop helper column safely
    df.drop(columns=["calculated_amount"], inplace=True, errors='ignore')

    # Save cleaned data
    df.to_csv(output_path, index=False)

    print("✅ Data cleaned and saved successfully!")
    print(f"📁 Output file: {output_path}")


if __name__ == "__main__":
    clean_data()