import pandas as pd
import numpy as np
from scipy import stats

# Load data
df = pd.read_csv("data/processed/ab_test_data.csv")

print("✅ Data Loaded for Advanced Statistical Testing\n")

# -------------------------------
# Step 1: Remove Outliers (1%–99%)
# -------------------------------
q_low = df["total_amount"].quantile(0.01)
q_high = df["total_amount"].quantile(0.99)

df = df[(df["total_amount"] >= q_low) & (df["total_amount"] <= q_high)]

print("✅ Outliers removed\n")

# -------------------------------
# Step 2: Log Transformation
# -------------------------------
df["log_amount"] = np.log1p(df["total_amount"])

# -------------------------------
# Step 3: Split Groups
# -------------------------------
control = df[df["experiment_variant"] == "Control"]["log_amount"]
variant = df[df["experiment_variant"] == "Variant A"]["log_amount"]

# -------------------------------
# Step 4: T-Test
# -------------------------------
t_stat, p_value = stats.ttest_ind(variant, control, equal_var=False)

# -------------------------------
# Step 5: Mann-Whitney U Test
# -------------------------------
u_stat, p_mwu = stats.mannwhitneyu(variant, control)

# -------------------------------
# Step 6: Effect Size (Cohen's d)
# -------------------------------
def cohens_d(a, b):
    return (np.mean(a) - np.mean(b)) / np.sqrt((np.var(a) + np.var(b)) / 2)

effect_size = cohens_d(variant, control)

# -------------------------------
# Step 7: Confidence Interval
# -------------------------------
diff = variant.mean() - control.mean()

se = np.sqrt(variant.var()/len(variant) + control.var()/len(control))
ci_low = diff - 1.96 * se
ci_high = diff + 1.96 * se

# -------------------------------
# Step 8: Results
# -------------------------------
print("📊 T-Test Results:")
print("T-Statistic:", round(t_stat, 4))
print("P-Value:", round(p_value, 6))

print("\n📊 Mann-Whitney U Test:")
print("P-Value:", round(p_mwu, 6))

print("\n📈 Effect Size (Cohen's d):", round(effect_size, 3))

print("\n📉 95% Confidence Interval:")
print(f"[{round(ci_low,4)}, {round(ci_high,4)}]")

# -------------------------------
# Step 9: Decision
# -------------------------------
alpha = 0.05

print("\n🧠 Final Interpretation:")

if p_value < alpha:
    print("✅ Statistically Significant (T-Test)")
else:
    print("❌ Not Significant (T-Test)")

if p_mwu < alpha:
    print("✅ Significant (Non-parametric test)")
else:
    print("❌ Not Significant (Mann-Whitney)")

if abs(effect_size) < 0.2:
    print("⚠️ Effect size is SMALL")
elif abs(effect_size) < 0.5:
    print("⚠️ Effect size is MEDIUM")
else:
    print("🔥 Effect size is LARGE")

# -------------------------------
# Step 10: Mean Comparison
# -------------------------------
print("\n📊 Mean Comparison (Log Scale):")
print("Control:", round(control.mean(), 4))
print("Variant:", round(variant.mean(), 4))

if p_value < 0.05:
    print("🚀 Roll out Variant A")
else:
    print("⚠️ No strong evidence → Run further experiments")