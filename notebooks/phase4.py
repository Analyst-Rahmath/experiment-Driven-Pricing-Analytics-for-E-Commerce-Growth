import pandas as pd
import os

# Base path
base_path = r"C:\Users\PC\Desktop\My Portfolio Projects\Experiment-Driven Pricing Analytics for E-Commerce Growth"

# File path
input_path = os.path.join(base_path, "data", "processed", "ab_test_data.csv")

# Load data
df = pd.read_csv(input_path)

print("✅ Data Loaded for KPI Analysis\n")


# -------------------------------
# Step 1: Overall KPI Summary
# -------------------------------
kpi_summary = df.groupby("experiment_variant").agg(
    total_orders=("order_id", "count"),
    total_revenue=("adjusted_amount", "sum"),
    avg_order_value=("adjusted_amount", "mean")
).round(2)

print("📊 Overall KPI Summary:")
print(kpi_summary)


# -------------------------------
# -------------------------------
# Step 2: Calculate Uplift %
# -------------------------------
control_aov = kpi_summary.loc["Control", "avg_order_value"]
variant_aov = kpi_summary.loc["Variant A", "avg_order_value"]

uplift = ((variant_aov - control_aov) / control_aov) * 100

print(f"\n🚀 AOV Uplift: {uplift:.2f}%")

# Add uplift column safely
kpi_summary["uplift_%"] = None
kpi_summary.loc["Variant A", "uplift_%"] = round(uplift, 2)


# -------------------------------
# Step 3: Country-Level Analysis
# -------------------------------
country_analysis = df.groupby(["country", "experiment_variant"])["adjusted_amount"].mean().unstack().round(2)

country_analysis["uplift_%"] = (
    (country_analysis["Variant A"] - country_analysis["Control"]) 
    / country_analysis["Control"] * 100
).round(2)

print("\n🌍 Country-Level AOV Analysis:")
print(country_analysis)


# -------------------------------
# Step 4: Category-Level Analysis
# -------------------------------
category_analysis = df.groupby(["category", "experiment_variant"])["adjusted_amount"].mean().unstack().round(2)

category_analysis["uplift_%"] = (
    (category_analysis["Variant A"] - category_analysis["Control"]) 
    / category_analysis["Control"] * 100
).round(2)

print("\n🛍️ Category-Level AOV Analysis:")
print(category_analysis)


# -------------------------------
# Step 5: Save Outputs
# -------------------------------
output_path = os.path.join(base_path, "outputs", "kpi_summary.csv")
kpi_summary.to_csv(output_path)

print("\n✅ KPI Summary saved!")
print(f"📁 Location: {output_path}")