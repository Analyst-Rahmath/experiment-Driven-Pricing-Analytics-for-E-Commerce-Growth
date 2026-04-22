# 📊 A/B Test Analysis – Pricing Strategy Experiment

## 🎯 Objective

Evaluate whether the dynamic pricing strategy (Variant A) improves revenue performance compared to the Control group.

---

## 📈 Key Observations

* Variant A shows a higher average order value compared to Control
* Observed uplift is present but relatively moderate

---

## 🧪 Statistical Testing Approach

To ensure robustness, multiple statistical techniques were applied:

### 1. Independent T-Test

Used to compare mean differences between groups.

### 2. Mann-Whitney U Test

Non-parametric test used to validate results without assuming normal distribution.

### 3. Data Preprocessing

* Outliers removed (1st–99th percentile)
* Log transformation applied to reduce skewness

---

## 📊 Results Summary

* T-Test: Not statistically significant (p > 0.05)
* Mann-Whitney Test: Not statistically significant
* Effect Size: Small
* Small dataset (1200 rows) may limit statistical power.
* Confidence Interval: Includes zero → indicates uncertainty

---

## 🧠 Interpretation

Although Variant A demonstrates a higher average revenue, the statistical analysis indicates that the difference is not strong enough to confidently conclude a true effect.

This suggests that:

* The observed uplift may be influenced by data variability
* The pricing strategy impact is inconsistent across observations

---

## 🌍 Segment-Level Insights

Further analysis revealed:

### Country-Level

* Strong uplift in emerging markets (India, Brazil, Pakistan)
* Weak or negative impact in developed markets (Australia)

### Category-Level

* Electronics and Home Decor show strong positive impact
* Sports and some categories underperform

---

## 🚀 Business Recommendations

1. Extend experiment duration to increase statistical power
2. Focus on high-performing segments instead of global rollout
3. Reduce variance by refining pricing strategy
4. Conduct segmented A/B testing for more precise insights

---

## 🏁 Final Conclusion

The experiment does not provide sufficient statistical evidence to support a full rollout of the new pricing strategy. However, targeted implementation in specific segments shows promising potential.

---

## 💡 Analyst Note

This analysis highlights the importance of validating observed trends with statistical rigor and demonstrates a data-driven approach to decision-making.
