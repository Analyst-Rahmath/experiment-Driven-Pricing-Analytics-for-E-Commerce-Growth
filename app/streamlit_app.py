import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

# ── PAGE CONFIG ────────────────────────────────
st.set_page_config(
    page_title="Experiment-Driven Pricing Analytics",
    page_icon="📈",
    layout="wide"
)

# ── HEADER ─────────────────────────────────────
st.markdown("""
    <div style='text-align: center; padding: 1.5rem 0 1rem 0;'>
        <h1 style='color: #F1F5F9; font-size: 2rem; font-weight: 700; margin-bottom: 0.3rem;'>
            📈 Experiment-Driven Pricing Analytics
        </h1>
        <p style='color: #94A3B8; font-size: 1rem; margin-top: 0;'>
            for E-Commerce Growth
        </p>
        <p style='color: #64748B; font-size: 0.85rem;'>
            simulated A/B Test · 1,200 Orders · $1.51M GMV · 10 Countries · 8 Categories
        </p>
    </div>
    <hr style='border: 1px solid #1E293B; margin-bottom: 1.5rem;'>
""", unsafe_allow_html=True)


# ── LOAD DATA ──────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/ab_test_data.csv")
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

df = load_data()

# ── SIDEBAR ────────────────────────────────────
st.sidebar.markdown("""
    <div style='padding: 0.5rem 0 1rem 0;'>
        <h2 style='color: #F1F5F9; font-size: 1.1rem; font-weight: 700;'>⚙️ Dashboard Filters</h2>
        <p style='color: #475569; font-size: 0.75rem;'>Adjust to explore segments</p>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("**🌍 Country**")
country_options = sorted(df['country'].unique().tolist())
country = st.sidebar.selectbox(
    "Select Country",
    options=["All Countries"] + country_options,
    label_visibility="collapsed"
)

st.sidebar.markdown("**🛍️ Category**")
category_options = sorted(df['category'].unique().tolist())
category = st.sidebar.selectbox(
    "Select Category",
    options=["All Categories"] + category_options,
    label_visibility="collapsed"
)

st.sidebar.markdown("**🧪 Variant**")
variant_option = st.sidebar.selectbox(
    "Select Variant",
    options=["Both", "Control", "Variant A"],
    label_visibility="collapsed"
)

st.sidebar.divider()
st.sidebar.markdown("""
    <div style='padding: 0.5rem 0;'>
        <p style='color: #475569; font-size: 0.72rem; line-height: 1.6;'>
            📦 1,200 Orders<br>
            💰 $1.51M GMV<br>
            🌍 10 Countries<br>
            🗂️ 8 Categories<br>
            📅 Jan–Dec 2025
        </p>
    </div>
""", unsafe_allow_html=True)

# Apply filters
df_filtered = df.copy()
if country != "All Countries":
    df_filtered = df_filtered[df_filtered['country'] == country]
if category != "All Categories":
    df_filtered = df_filtered[df_filtered['category'] == category]
if variant_option != "Both":
    df_filtered = df_filtered[df_filtered['experiment_variant'] == variant_option]

# ── TABS ───────────────────────────────────────
tab1, tab2, tab3  = st.tabs([
    "📊 Executive Dashboard",
    "🔬 Statistical Test",
    "🌍 Segment Analysis",

])

# ── TAB 1: EXECUTIVE DASHBOARD ─────────────────
# ── TAB 1: EXECUTIVE DASHBOARD ─────────────────
with tab1:
    st.markdown("### 📊 Executive Dashboard")

    # KPI Row
    control = df_filtered[df_filtered['experiment_variant'] == 'Control']
    variant = df_filtered[df_filtered['experiment_variant'] == 'Variant A']

    total_gmv = df_filtered['total_amount'].sum()
    aov_control = control['total_amount'].mean() if not control.empty else np.nan
    aov_variant = variant['total_amount'].mean() if not variant.empty else np.nan
    uplift = ((aov_variant - aov_control) / aov_control * 100) if not np.isnan(aov_control) and aov_control > 0 else 0
    total_orders = len(df_filtered)

    gmv_display = f"${total_gmv:,.0f}" if total_gmv > 0 else "—"
    aov_control_display = f"${aov_control:,.0f}" if not np.isnan(aov_control) else "—"
    aov_variant_display = f"${aov_variant:,.0f}" if not np.isnan(aov_variant) else "—"
    uplift_display = f"+{uplift:.1f}%" if uplift != 0 else "—"

    st.markdown(f"""
    <div style='display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 1.5rem;'>
      <div style='background:#1E293B; border:1px solid #334155; border-top:3px solid #3B82F6; border-radius:10px; padding:1.2rem 1.5rem;'>
        <div style='color:#64748B; font-size:0.72rem; font-weight:600; letter-spacing:0.08em; text-transform:uppercase;'>💰 Total GMV</div>
        <div style='color:#F1F5F9; font-size:1.8rem; font-weight:700; font-family:monospace; margin:0.4rem 0;'>{gmv_display}</div>
        <div style='color:#22C55E; font-size:0.78rem;'>↑ Full Dataset Revenue</div>
      </div>
      <div style='background:#1E293B; border:1px solid #334155; border-top:3px solid #3B82F6; border-radius:10px; padding:1.2rem 1.5rem;'>
        <div style='color:#64748B; font-size:0.72rem; font-weight:600; letter-spacing:0.08em; text-transform:uppercase;'>🛒 AOV — Control</div>
        <div style='color:#3B82F6; font-size:1.8rem; font-weight:700; font-family:monospace; margin:0.4rem 0;'>{aov_control_display}</div>
        <div style='color:#94A3B8; font-size:0.78rem;'>Fixed Pricing Baseline</div>
      </div>
      <div style='background:#1E293B; border:1px solid #334155; border-top:3px solid #EC4899; border-radius:10px; padding:1.2rem 1.5rem;'>
        <div style='color:#64748B; font-size:0.72rem; font-weight:600; letter-spacing:0.08em; text-transform:uppercase;'>🚀 AOV — Variant A</div>
        <div style='color:#EC4899; font-size:1.8rem; font-weight:700; font-family:monospace; margin:0.4rem 0;'>{aov_variant_display}</div>
        <div style='color:#94A3B8; font-size:0.78rem;'>Dynamic Pricing Strategy</div>
      </div>
      <div style='background:#1E293B; border:1px solid #334155; border-top:3px solid #22C55E; border-radius:10px; padding:1.2rem 1.5rem;'>
        <div style='color:#64748B; font-size:0.72rem; font-weight:600; letter-spacing:0.08em; text-transform:uppercase;'>📈 AOV Uplift</div>
        <div style='color:#22C55E; font-size:1.8rem; font-weight:700; font-family:monospace; margin:0.4rem 0;'>{uplift_display}</div>
        <div style='color:#94A3B8; font-size:0.78rem;'>vs Control · {total_orders:,} Orders</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Row 2 — A/B Chart + Revenue Trend
    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown("#### AOV by Variant")
        ab_data = df_filtered.groupby('experiment_variant')['total_amount'].mean().reset_index()
        fig_ab = px.bar(
            ab_data,
            x='experiment_variant',
            y='total_amount',
            color='experiment_variant',
            color_discrete_map={'Control': '#3B82F6', 'Variant A': '#EC4899'},
            text='total_amount',
            labels={'total_amount': 'AOV ($)', 'experiment_variant': 'Variant'}
        )
        fig_ab.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
        fig_ab.update_layout(
            plot_bgcolor='#1E293B',
            paper_bgcolor='#1E293B',
            font_color='#FFFFFF',
            showlegend=False,
            height=350
        )
        st.plotly_chart(fig_ab, use_container_width=True)

    with col_right:
        st.markdown("#### Revenue Trend by Variant")
        trend = df_filtered.groupby(
            [df_filtered['order_date'].dt.to_period('M').astype(str), 'experiment_variant']
        )['total_amount'].sum().reset_index()
        trend.columns = ['month', 'variant', 'revenue']
        fig_trend = px.line(
            trend,
            x='month',
            y='revenue',
            color='variant',
            color_discrete_map={'Control': '#3B82F6', 'Variant A': '#EC4899'},
            markers=True,
            labels={'revenue': 'Revenue ($)', 'month': 'Month'}
        )
        fig_trend.update_layout(
            plot_bgcolor='#1E293B',
            paper_bgcolor='#1E293B',
            font_color='#FFFFFF',
            height=350
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    st.divider()

    # Insight Box
    st.info("""
    Key Finding: Variant A shows +3.6% AOV ($1,282 vs $1,238), but p = 0.47, so the difference is not statistically significant. This is a simulated experiment, so no real pricing effect is implied. Recommendation: do not roll out; a larger test would be needed
    """)

    # ── TAB 2: STATISTICAL TEST ─────────────────────
with tab2:
    st.markdown("### 🔬 Statistical Test Results")

    control_vals = control['total_amount'].dropna()
    variant_vals = variant['total_amount'].dropna()

    t_stat, p_value = stats.ttest_ind(control_vals, variant_vals)
    mean_diff = aov_variant - aov_control
    pooled_std = np.sqrt((control_vals.std()**2 + variant_vals.std()**2) / 2)
    cohens_d = mean_diff / pooled_std
    ci = stats.t.interval(0.95, df=len(df_filtered)-2,
                          loc=mean_diff,
                          scale=stats.sem(df_filtered['total_amount']))

    # Result banner
    if p_value < 0.05:
        st.success(f"✅ Statistically Significant — p = {p_value:.4f} (< 0.05). We reject the null hypothesis.")
    else:
        st.error(f"❌ Not Significant — p = {p_value:.4f} (> 0.05). Fail to reject null hypothesis.")

    st.divider()

    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("T-Statistic", f"{t_stat:.3f}")
    col2.metric("P-Value", f"{p_value:.4f}")
    col3.metric("Cohen's d", f"{cohens_d:.3f}")
    col4.metric("Mean Difference", f"${mean_diff:,.0f}")

    st.divider()

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("#### AOV Distribution by Variant")
        fig_box = go.Figure()
        fig_box.add_trace(go.Box(
            y=control_vals,
            name='Control',
            marker_color='#3B82F6',
            boxmean=True
        ))
        fig_box.add_trace(go.Box(
            y=variant_vals,
            name='Variant A',
            marker_color='#EC4899',
            boxmean=True
        ))
        fig_box.update_layout(
            plot_bgcolor='#1E293B',
            paper_bgcolor='#1E293B',
            font_color='#FFFFFF',
            height=400,
            yaxis_title='Order Value ($)'
        )
        st.plotly_chart(fig_box, use_container_width=True)

    with col_right:
        st.markdown("#### Confidence Interval (95%)")
        fig_ci = go.Figure()
        fig_ci.add_trace(go.Scatter(
            x=['Lower Bound', 'Mean Difference', 'Upper Bound'],
            y=[ci[0], mean_diff, ci[1]],
            mode='markers+lines',
            marker=dict(size=12, color='#22C55E'),
            line=dict(color='#22C55E', dash='dash')
        ))
        fig_ci.add_hline(y=0, line_dash='solid',
                         line_color='#EF4444',
                         annotation_text='Zero (No Effect)')
        fig_ci.update_layout(
            plot_bgcolor='#1E293B',
            paper_bgcolor='#1E293B',
            font_color='#FFFFFF',
            height=400,
            yaxis_title='Difference in AOV ($)'
        )
        st.plotly_chart(fig_ci, use_container_width=True)

    st.divider()
    st.markdown("#### 📋 Interpretation")
    st.warning("""
    #### 📋 Interpretation & Business Context
    - **$44 AOV difference exists** (Control $1,238 → Variant A $1,282) but p = 0.47 means
      this could be due to random variation
    - **Why not significant?**  The difference is within what random variation produces.
    - **What this means for business:** Do NOT roll out Variant A globally yet
    - **Recommendation:** Run experiment for 60 more days OR “Run a larger test.” The “+18%” was Home Decor, not UAE
   
    """)

# ── TAB 3: SEGMENT ANALYSIS ─────────────────────
with tab3:
    st.markdown("### 🌍 Segment Analysis")

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("#### AOV by Category")
        cat_data = df_filtered.groupby(
            ['category', 'experiment_variant']
        )['total_amount'].mean().reset_index()
        fig_cat = px.bar(
            cat_data,
            x='total_amount',
            y='category',
            color='experiment_variant',
            barmode='group',
            orientation='h',
            color_discrete_map={'Control': '#3B82F6', 'Variant A': '#EC4899'},
            text='total_amount',
            labels={'total_amount': 'AOV ($)', 'category': 'Category'}
        )
        fig_cat.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
        fig_cat.update_layout(
            plot_bgcolor='#1E293B',
            paper_bgcolor='#1E293B',
            font_color='#FFFFFF',
            height=400,
            legend_title='Variant'
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    with col_right:
        st.markdown("#### AOV by Country")
        country_data = df_filtered.groupby(
            ['country', 'experiment_variant']
        )['total_amount'].mean().reset_index()
        fig_country = px.bar(
            country_data,
            x='total_amount',
            y='country',
            color='experiment_variant',
            barmode='group',
            orientation='h',
            color_discrete_map={'Control': '#3B82F6', 'Variant A': '#EC4899'},
            text='total_amount',
            labels={'total_amount': 'AOV ($)', 'country': 'Country'}
        )
        fig_country.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
        fig_country.update_layout(
            plot_bgcolor='#1E293B',
            paper_bgcolor='#1E293B',
            font_color='#FFFFFF',
            height=400,
            legend_title='Variant'
        )
        st.plotly_chart(fig_country, use_container_width=True)

    st.divider()

    # Uplift table
    st.markdown("#### 📊 Uplift % by Category")
    pivot = df_filtered.groupby(
        ['category', 'experiment_variant']
    )['total_amount'].mean().unstack()
    pivot.columns = ['AOV Control', 'AOV Variant A']
    pivot['Uplift %'] = ((pivot['AOV Variant A'] - pivot['AOV Control']) / pivot['AOV Control'] * 100).round(2)
    pivot['AOV Control'] = pivot['AOV Control'].map('${:,.0f}'.format)
    pivot['AOV Variant A'] = pivot['AOV Variant A'].map('${:,.0f}'.format)
    pivot['Uplift %'] = pivot['Uplift %'].map('{:+.2f}%'.format)
    st.dataframe(pivot, use_container_width=True)

    st.divider()
    st.info("""
    💡 **Segment Insight:**
    - **Best Category:** Electronics +36.86% · Home Decor +18.41%
    - **Best Country:** Brazil +26.12% · Pakistan +19.43%
    - **Avoid:** Sports -16.03% · Australia -30.14%
    - **Q4 strongest quarter** — Variant A AOV $1,326 vs Control $1,252
    Exploratory: each country–variant group has about 45–75 orders, differences aren’t statistically tested, and they’re consistent with chance
    """)


    # ── FOOTER ─────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <hr style='border: 1px solid #1E293B;'>
    <div style='text-align: center; padding: 1rem 0;'>
        <p style='color: #64748B; font-size: 0.85rem;'>
            Built by <strong style='color: #94A3B8;'>Rahmath B</strong> · 
            <a href='https://github.com/YOUR_GITHUB' 
               target='_blank' 
               style='color: #3B82F6; text-decoration: none;'>
                ⭐ GitHub Portfolio
            </a> · 
            <a href='https://linkedin.com/in/YOUR_LINKEDIN' 
               target='_blank' 
               style='color: #3B82F6; text-decoration: none;'>
                💼 LinkedIn
            </a>
        </p>
        <p style='color: #475569; font-size: 0.75rem;'>
            Stack: Python · Streamlit · Plotly · Scikit-learn · Power BI · SciPy
        </p>
    </div>
""", unsafe_allow_html=True)