import pandas as pd
import numpy as np
import os

# Base project path
base_path = r"C:\Users\PC\Desktop\My Portfolio Projects\Experiment-Driven Pricing Analytics for E-Commerce Growth"

# File paths
input_path = os.path.join(base_path, "data", "processed", "cleaned_data_final.csv")
output_path = os.path.join(base_path, "data", "processed", "ab_test_data.csv")

# Load dataset
df = pd.read_csv(input_path)

print("✅ Data Loaded Successfully")
print(df.head())


# -------------------------------
# Step 1: Create A/B Split
# -------------------------------
np.random.seed(42)

df["experiment_variant"] = np.random.choice(
    ["Control", "Variant A"],
    size=len(df)
)

print("\n📊 Variant Distribution:")
print(df["experiment_variant"].value_counts())


# -------------------------------
# Step 2: Simulate Pricing Impact
# -------------------------------
df["adjusted_amount"] = df["total_amount"]

df.loc[df["experiment_variant"] == "Variant A", "adjusted_amount"] = (
    df["total_amount"] * 1.12
).round(2)


# -------------------------------
# Step 3: Quick Business Check
# -------------------------------
summary = df.groupby("experiment_variant")["adjusted_amount"].agg(["count", "mean", "sum"])

print("\n📈 A/B Summary:")
print(summary)


# -------------------------------
# Step 4: Save Dataset
# -------------------------------
df.to_csv(output_path, index=False)

print("\n✅ A/B Test dataset created successfully!")
print(f"📁 Saved at: {output_path}")