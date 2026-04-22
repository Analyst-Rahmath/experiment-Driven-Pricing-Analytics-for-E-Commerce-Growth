-- ═══════════════════════════════════════════════════════════
-- Project: Experiment-Driven Pricing Analytics
-- Author:  Rahmath B
-- Date:    April 2026
-- Purpose: A/B Test Analysis Queries
-- ═══════════════════════════════════════════════════════════


-- ── QUERY 1: Overall A/B Test Results ─────────────────────
-- Core question: Which variant performs better?

SELECT
    experiment_variant,
    COUNT(order_id)                          AS total_orders,
    ROUND(SUM(total_amount), 2)              AS total_revenue,
    ROUND(AVG(total_amount), 2)              AS avg_order_value,
    ROUND(MIN(total_amount), 2)              AS min_order_value,
    ROUND(MAX(total_amount), 2)              AS max_order_value
FROM ab_test_data
GROUP BY experiment_variant
ORDER BY avg_order_value DESC;


-- ── QUERY 2: Uplift % by Category ─────────────────────────
-- Which categories respond best to dynamic pricing?

SELECT
    category,
    ROUND(AVG(CASE WHEN experiment_variant = 'Control'   THEN total_amount END), 2) AS aov_control,
    ROUND(AVG(CASE WHEN experiment_variant = 'Variant A' THEN total_amount END), 2) AS aov_variant,
    ROUND(
        (AVG(CASE WHEN experiment_variant = 'Variant A' THEN total_amount END) -
         AVG(CASE WHEN experiment_variant = 'Control'   THEN total_amount END)) /
         AVG(CASE WHEN experiment_variant = 'Control'   THEN total_amount END) * 100
    , 2)                                                                             AS uplift_pct
FROM ab_test_data
GROUP BY category
ORDER BY uplift_pct DESC;


-- ── QUERY 3: Uplift % by Country ──────────────────────────
-- Which markets respond best to dynamic pricing?

SELECT
    country,
    ROUND(AVG(CASE WHEN experiment_variant = 'Control'   THEN total_amount END), 2) AS aov_control,
    ROUND(AVG(CASE WHEN experiment_variant = 'Variant A' THEN total_amount END), 2) AS aov_variant,
    ROUND(
        (AVG(CASE WHEN experiment_variant = 'Variant A' THEN total_amount END) -
         AVG(CASE WHEN experiment_variant = 'Control'   THEN total_amount END)) /
         AVG(CASE WHEN experiment_variant = 'Control'   THEN total_amount END) * 100
    , 2)                                                                             AS uplift_pct
FROM ab_test_data
GROUP BY country
ORDER BY uplift_pct DESC;


-- ── QUERY 4: Monthly Revenue Trend ────────────────────────
-- Does Variant A show consistent uplift over time?

SELECT
    month,
    ROUND(SUM(CASE WHEN experiment_variant = 'Control'   THEN total_amount END), 2) AS revenue_control,
    ROUND(SUM(CASE WHEN experiment_variant = 'Variant A' THEN total_amount END), 2) AS revenue_variant,
    ROUND(
        (SUM(CASE WHEN experiment_variant = 'Variant A' THEN total_amount END) -
         SUM(CASE WHEN experiment_variant = 'Control'   THEN total_amount END)) /
         SUM(CASE WHEN experiment_variant = 'Control'   THEN total_amount END) * 100
    , 2)                                                                             AS monthly_uplift_pct
FROM ab_test_data
GROUP BY month
ORDER BY month;


-- ── QUERY 5: Top 10 Revenue Segments ──────────────────────
-- Best performing country + category combinations

SELECT
    country,
    category,
    experiment_variant,
    COUNT(order_id)                 AS total_orders,
    ROUND(SUM(total_amount), 2)     AS total_revenue,
    ROUND(AVG(total_amount), 2)     AS avg_order_value
FROM ab_test_data
GROUP BY country, category, experiment_variant
ORDER BY total_revenue DESC
LIMIT 10;


-- ── QUERY 6: Quarterly Performance ────────────────────────
-- Does Variant A show consistent uplift across quarters?

SELECT
    quarter,
    experiment_variant,
    COUNT(order_id)                 AS total_orders,
    ROUND(SUM(total_amount), 2)     AS total_revenue,
    ROUND(AVG(total_amount), 2)     AS avg_order_value
FROM ab_test_data
GROUP BY quarter, experiment_variant
ORDER BY quarter, avg_order_value DESC;

-- ── QUERY 7: Statistical Summary ──────────────────────────
-- Quick sanity check on experiment balance

SELECT
    experiment_variant,
    COUNT(*)                        AS total_orders,
    ROUND(COUNT(*) * 100.0 / 
          SUM(COUNT(*)) OVER(), 2)  AS pct_of_total,
    ROUND(AVG(total_amount), 2)     AS mean_aov,
    ROUND(SUM(total_amount), 2)     AS total_gmv
FROM ab_test_data
GROUP BY experiment_variant;