import pandas as pd
import sqlite3

# ── Load CSV into SQLite in-memory database ──────────────
df = pd.read_csv("data/processed/ab_test_data.csv")
conn = sqlite3.connect(":memory:")
df.to_sql("ab_test_data", conn, index=False, if_exists="replace")
print("✅ Database loaded:", len(df), "rows\n")

# ── Run all queries ───────────────────────────────────────
queries = {
    "1. Overall A/B Results": """
        SELECT experiment_variant,
               COUNT(order_id)             AS total_orders,
               ROUND(SUM(total_amount), 2) AS total_revenue,
               ROUND(AVG(total_amount), 2) AS avg_order_value
        FROM ab_test_data
        GROUP BY experiment_variant
        ORDER BY avg_order_value DESC
    """,

    "2. Uplift by Category": """
        SELECT category,
               ROUND(AVG(CASE WHEN experiment_variant='Control'   THEN total_amount END), 2) AS aov_control,
               ROUND(AVG(CASE WHEN experiment_variant='Variant A' THEN total_amount END), 2) AS aov_variant,
               ROUND(
                   (AVG(CASE WHEN experiment_variant='Variant A' THEN total_amount END) -
                    AVG(CASE WHEN experiment_variant='Control'   THEN total_amount END)) /
                    AVG(CASE WHEN experiment_variant='Control'   THEN total_amount END) * 100
               , 2) AS uplift_pct
        FROM ab_test_data
        GROUP BY category
        ORDER BY uplift_pct DESC
    """,

    "3. Uplift by Country": """
        SELECT country,
               ROUND(AVG(CASE WHEN experiment_variant='Control'   THEN total_amount END), 2) AS aov_control,
               ROUND(AVG(CASE WHEN experiment_variant='Variant A' THEN total_amount END), 2) AS aov_variant,
               ROUND(
                   (AVG(CASE WHEN experiment_variant='Variant A' THEN total_amount END) -
                    AVG(CASE WHEN experiment_variant='Control'   THEN total_amount END)) /
                    AVG(CASE WHEN experiment_variant='Control'   THEN total_amount END) * 100
               , 2) AS uplift_pct
        FROM ab_test_data
        GROUP BY country
        ORDER BY uplift_pct DESC
    """,

    "4. Monthly Revenue Trend": """
        SELECT month,
               ROUND(SUM(CASE WHEN experiment_variant='Control'   THEN total_amount END), 2) AS revenue_control,
               ROUND(SUM(CASE WHEN experiment_variant='Variant A' THEN total_amount END), 2) AS revenue_variant,
               ROUND(
                   (SUM(CASE WHEN experiment_variant='Variant A' THEN total_amount END) -
                    SUM(CASE WHEN experiment_variant='Control'   THEN total_amount END)) /
                    SUM(CASE WHEN experiment_variant='Control'   THEN total_amount END) * 100
               , 2) AS monthly_uplift_pct
        FROM ab_test_data
        GROUP BY month
        ORDER BY month
    """,

    "5. Top 10 Revenue Segments": """
        SELECT country, category, experiment_variant,
               COUNT(order_id)                 AS total_orders,
               ROUND(SUM(total_amount), 2)     AS total_revenue,
               ROUND(AVG(total_amount), 2)     AS avg_order_value
        FROM ab_test_data
        GROUP BY country, category, experiment_variant
        ORDER BY total_revenue DESC
        LIMIT 10
    """,

    "6. Quarterly Performance": """
        SELECT quarter,
               experiment_variant,
               COUNT(order_id)                 AS total_orders,
               ROUND(SUM(total_amount), 2)     AS total_revenue,
               ROUND(AVG(total_amount), 2)     AS avg_order_value
        FROM ab_test_data
        GROUP BY quarter, experiment_variant
        ORDER BY quarter, avg_order_value DESC
    """,

    "7. Statistical Summary": """
        SELECT experiment_variant,
               COUNT(*)                        AS total_orders,
               ROUND(AVG(total_amount), 2)     AS mean_aov,
               ROUND(SUM(total_amount), 2)     AS total_gmv
        FROM ab_test_data
        GROUP BY experiment_variant
    """
}

# ── Print results ─────────────────────────────────────────
for name, query in queries.items():
    print(f"\n{'═'*60}")
    print(f"  QUERY {name}")
    print(f"{'═'*60}")
    result = pd.read_sql_query(query, conn)
    print(result.to_string(index=False))

conn.close()
print("\n✅ All queries completed.")