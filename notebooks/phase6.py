import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
sns.set_palette("pastel")
# Load dataset
file_path = r"C:\Users\PC\Desktop\My Portfolio Projects\Experiment-Driven Pricing Analytics for E-Commerce Growth\data\processed\ab_test_data.csv"
df = pd.read_csv(file_path)

print("✅ Data Loaded for Visualization")

# Create output folder path
output_path = r"C:\Users\PC\Desktop\My Portfolio Projects\Experiment-Driven Pricing Analytics for E-Commerce Growth\outputs\\"

# -----------------------------
# 1. Revenue by Variant
# -----------------------------
revenue = df.groupby("experiment_variant")["total_amount"].sum()

plt.figure()
bars = plt.bar(revenue.index, revenue.values, color=["#4CAF50", "#FF9800"])

plt.title("Total Revenue by Variant")
plt.ylabel("Revenue")

# Data labels
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval,
             round(yval, 2),
             ha='center', va='bottom')

plt.savefig(output_path + "revenue_by_variant.png")
plt.close()

# -----------------------------
# 2. Average Order Value (AOV)
# -----------------------------
aov = df.groupby("experiment_variant")["total_amount"].mean()

plt.figure()
bars = plt.bar(aov.index, aov.values, color=["#2196F3", "#E91E63"])

plt.title("Average Order Value (AOV) by Variant")
plt.ylabel("AOV")

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval,
             round(yval, 2),
             ha='center', va='bottom')

plt.savefig(output_path + "aov_by_variant.png")
plt.close()

# -----------------------------
# 3. Revenue by Country
# -----------------------------
country_rev = df.groupby("country")["total_amount"].sum().sort_values()

plt.figure(figsize=(10,5))
colors = sns.color_palette("viridis", len(country_rev))

bars = plt.barh(country_rev.index, country_rev.values, color=colors)

plt.title("Revenue by Country")
plt.xlabel("Revenue")

for i, v in enumerate(country_rev.values):
    plt.text(v, i, f"{round(v,2)}", va='center')

plt.savefig(output_path + "revenue_by_country.png")
plt.close()
# -----------------------------
# 4. Revenue by Category
# -----------------------------
category_rev = df.groupby("category")["total_amount"].sum().sort_values()

plt.figure(figsize=(10,5))
colors = sns.color_palette("coolwarm", len(category_rev))

bars = plt.barh(category_rev.index, category_rev.values, color=colors)

plt.title("Revenue by Category")
plt.xlabel("Revenue")

for i, v in enumerate(category_rev.values):
    plt.text(v, i, f"{round(v,2)}", va='center')

plt.savefig(output_path + "revenue_by_category.png")
plt.close()

#----------------------------
# 5. Revenue Trend Over Time
#----------------------------
df["order_date"] = pd.to_datetime(df["order_date"])

monthly_rev = df.groupby("order_date")["total_amount"].sum()

plt.figure(figsize=(10,5))
plt.plot(monthly_rev.index, monthly_rev.values, marker='o')

plt.title("Revenue Trend Over Time")
plt.xlabel("Date")
plt.ylabel("Revenue")

plt.xticks(rotation=45)

plt.savefig(output_path + "revenue_trend.png")
plt.close()
#-----------------------------

#-----------------------------
# 6. Heatmap: Country vs Category
#-----------------------------
pivot = df.pivot_table(
    values="total_amount",
    index="country",
    columns="category",
    aggfunc="sum"
)

plt.figure(figsize=(10,6))
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu")

plt.title("Revenue Heatmap (Country vs Category)")

plt.savefig(output_path + "heatmap_country_category.png")
plt.close()
#-----------------------------
# 7. Scatter Plot: Price vs Quantity
#-----------------------------
plt.figure(figsize=(8,5))

sns.scatterplot(
    data=df,
    x="unit_price",
    y="quantity",
    hue="experiment_variant"
)

plt.title("Price vs Quantity (Demand Analysis)")

plt.savefig(output_path + "price_vs_quantity.png")
plt.close()

#-----------------------------
# 8. Distribution of Order Value
#-----------------------------
plt.figure(figsize=(8,5))

sns.histplot(
    data=df,
    x="total_amount",
    hue="experiment_variant",
    kde=True,
    bins=30
)

plt.title("Distribution of Order Value")

plt.savefig(output_path + "aov_distribution.png")
plt.close()

#-----------------------------
# 9. Revenue Trend by Variant
#-----------------------------
# Convert date column
df['order_date'] = pd.to_datetime(df['order_date'])

# Aggregate revenue by date & variant
trend_variant = df.groupby(['order_date', 'experiment_variant'])['total_amount'].sum().reset_index()

plt.figure(figsize=(12,6))

sns.lineplot(data=trend_variant,
             x='order_date',
             y='total_amount',
             hue='experiment_variant',
             marker='o')

plt.title("Revenue Trend Over Time by Variant")
plt.xlabel("Date")
plt.ylabel("Revenue")
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig("outputs/revenue_trend_by_variant.png")
plt.show()

#-----------------------------
# 10. Category-wise A/B Comparison
#-----------------------------
category_variant = df.groupby(['category', 'experiment_variant'])['total_amount'].mean().reset_index()

plt.figure(figsize=(12,6))

sns.barplot(data=category_variant,
            x='category',
            y='total_amount',
            hue='experiment_variant')

plt.title("Category-wise A/B Comparison (Avg Revenue)")
plt.xlabel("Category")
plt.ylabel("Average Revenue")
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig("outputs/category_ab_comparison.png")
plt.show()

#-----------------------------
# 11. Boxplot: Order Value by Variant
#-----------------------------
plt.figure(figsize=(8,6))

sns.boxplot(data=df,
            x='experiment_variant',
            y='total_amount',
            palette=['#4CAF50', '#FF9800'])

plt.title("Order Value Distribution by Variant")
plt.xlabel("Variant")
plt.ylabel("Order Value")

plt.tight_layout()
plt.savefig("outputs/boxplot_aov.png")
plt.show()
print("📊 Visualizations saved successfully in outputs folder!")

