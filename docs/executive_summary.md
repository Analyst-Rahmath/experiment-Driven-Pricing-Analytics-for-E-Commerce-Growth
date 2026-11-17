# Executive Summary
## Experiment-Driven Pricing Analytics for E-Commerce Growth

---

### 🎯 Business Problem
Does dynamic pricing (Variant A) generate higher Average Order Value 
than fixed pricing (Control) across global e-commerce markets?

---

### 🔬 Methodology
- **Dataset:** 1,200 orders · $1.51M GMV · Jan–Dec 2025
- **Split:** 50/50 · Control (601) vs Variant A (599)
- **Scope:** 10 countries · 8 product categories
- **Tests:** Independent t-test · Mann-Whitney U · Cohen's d · 95% CI
“Experiment groups were randomly assigned (simulation).”

---

### 📊 Key Findings

| Metric            | Control  | Variant A | Difference |
|-------------------|----------|-----------|------------|
| AOV               | $1,238   | $1,282    | +$44       |
| Total Revenue     | $744K    | $768K     | +$24K      |
| Orders            | 601      | 599       | —          |
| Uplift %          | —        | +3.6%     | —          |

- **T-test p-value:** 0.4679 — not statistically significant
- **Cohen's d:** 0.042 — small effect size
- **95% CI:** [-$71 → +$159]

---

### 🌍 Segment Analysis(exploratory)
Each country–variant group has only about 45–75 orders and nothing was corrected for multiple testing. These differences are consistent with random variation and shouldn’t drive rollout decisions.”

---

### 💡 Recommendations

1. **Do NOT deploy globally** — p-value insufficient for full rollout
2. **Run targeted pilot** “Run a larger, properly sized test before any rollout decision.”
3. **Increase sample size** to 3,000+ orders for statistical power
4. **Monitor seasonality** — December drop affects both variants equally


---

### 🚀 Next Steps

- Extend experiment duration → “Calculate the required sample size before extending the test.”
- A/B test pricing tiers within Variant A segments

---

*Analysis conducted by Rahmath B · April 2026*