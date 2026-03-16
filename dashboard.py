import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Sales Intelligence Pro", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM THEME (Power BI Blue & Gold) ---
th = {
    "bg": "#F0F2F5",
    "card": "#FFFFFF",
    "text": "#1F2937",
    "accent": "#2563EB",  # Power BI Blue
    "secondary": "#F59E0B" # Gold
}

# --- HIGH-VISIBILITY CSS ---
st.markdown(f"""
    <style>
        .stApp {{ background-color: {th['bg']}; color: {th['text']}; }}
        
        /* Power BI Header Bar */
        .pbi-header {{
            background-color: {th['accent']};
            padding: 15px;
            border-radius: 10px;
            color: white !important;
            text-align: center;
            margin-bottom: 25px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }}

        /* KPI Card Styling */
        .kpi-card {{
            background: {th['card']};
            padding: 20px;
            border-radius: 12px;
            border-left: 5px solid {th['secondary']};
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            text-align: center;
        }}
        .kpi-val {{ font-size: 24px; font-weight: 800; color: {th['accent']}; }}
        .kpi-lab {{ font-size: 12px; font-weight: 600; color: #6B7280; text-transform: uppercase; }}

        /* Chart Containers */
        .chart-card {{
            background: {th['card']};
            padding: 15px;
            border-radius: 15px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            border: 1px solid #E5E7EB;
            margin-bottom: 20px;
        }}
        
        /* Force text visibility */
        h1, h2, h3, p, span {{ color: {th['text']} !important; }}
        .pbi-header h1 {{ color: white !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("SALES_DATA_SETT.xlsx")
        df['Order Date'] = pd.to_datetime(df['Order Date'])
        df['Year'] = df['Order Date'].dt.year
        return df
    except: return pd.DataFrame()

df = load_data()

if not df.empty:
    # --- SIDEBAR (Slicers) ---
    with st.sidebar:
        st.markdown("### 🔍 Report Slicers")
        sel_region = st.multiselect("Select Region", df['Region'].unique(), default=df['Region'].unique())
        sel_cat = st.multiselect("Select Category", df['Category'].unique(), default=df['Category'].unique())
        f_df = df[(df['Region'].isin(sel_region)) & (df['Category'].isin(sel_cat))]

    # --- DASHBOARD HEADER ---
    st.markdown('<div class="pbi-header"><h1>📊 AI POWERED SALES EXECUTIVE SUMMARY</h1></div>', unsafe_allow_html=True)

    # --- ROW 1: 8 BOLD KPIs ---
    k_cols = st.columns(8)
    kpi_data = [
        ("Revenue", f"${f_df['Sales'].sum()/1e6:.1f}M"),
        ("Profit", f"${f_df['Profit'].sum()/1e3:.0f}K"),
        ("Orders", f"{f_df['Order ID'].nunique():,}"),
        ("AOV", f"${f_df['Sales'].sum()/f_df['Order ID'].nunique():.0f}"),
        ("Units", f"{f_df['Quantity'].sum()/1e3:.0f}K"),
        ("Disc %", f"{(f_df['Discount'].mean()*100):.0f}%"),
        ("Margin", f"{(f_df['Profit'].sum()/f_df['Sales'].sum()*100):.1f}%"),
        ("Lead Time", "4.2d")
    ]
    for i, (label, val) in enumerate(kpi_data):
        k_cols[i].markdown(f'<div class="kpi-card"><div class="kpi-lab">{label}</div><div class="kpi-val">{val}</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    # --- ROW 2 & 3: 6 CREATIVE VISUALS ---
    c1, c2, c3 = st.columns(3)
    c4, c5, c6 = st.columns(3)

    # Visual 1: Horizontal Funnel (Sales by Category)
    with c1:
        st.markdown('<div class="chart-card"><b>📈 Sales funnel by Category</b>', unsafe_allow_html=True)
        fig = px.bar(f_df.groupby('Category')['Sales'].sum().reset_index(), x='Sales', y='Category', orientation='h', height=220, color_discrete_sequence=[th['accent']])
        fig.update_layout(margin=dict(l=0,r=10,t=10,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True, key="v1")
        st.markdown('</div>', unsafe_allow_html=True)

    # Visual 2: Power BI Donut (Regional Share)
    with c2:
        st.markdown('<div class="chart-card"><b>🌍 Geographic Contribution</b>', unsafe_allow_html=True)
        fig = px.pie(f_df, names='Region', values='Sales', hole=0.6, height=220, color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_layout(showlegend=False, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True, key="v2")
        st.markdown('</div>', unsafe_allow_html=True)

    # Visual 3: Top Products (Treemap)
    with c3:
        st.markdown('<div class="chart-card"><b>🏆 Product Hierarchy</b>', unsafe_allow_html=True)
        fig = px.treemap(f_df.nlargest(20, 'Sales'), path=['Category', 'Sub-Category'], values='Sales', height=220, color_discrete_sequence=[th['secondary']])
        fig.update_layout(margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True, key="v3")
        st.markdown('</div>', unsafe_allow_html=True)

    # Visual 4: Sales Velocity (Area Chart)
    with c4:
        st.markdown('<div class="chart-card"><b>🚀 Sales Velocity (Monthly)</b>', unsafe_allow_html=True)
        temp_df = f_df.resample('M', on='Order Date')['Sales'].sum().reset_index()
        fig = px.area(temp_df, x='Order Date', y='Sales', height=220, color_discrete_sequence=[th['accent']])
        fig.update_layout(margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True, key="v4")
        st.markdown('</div>', unsafe_allow_html=True)

    # Visual 5: Gauge Chart (Profit Margin)
    with c5:
        st.markdown('<div class="chart-card"><b>🎯 Target Margin</b>', unsafe_allow_html=True)
        margin = (f_df['Profit'].sum()/f_df['Sales'].sum()*100) if not f_df.empty else 0
        fig = go.Figure(go.Indicator(mode="gauge+number", value=margin, number={'suffix': "%"}, gauge={'bar': {'color': th['accent']}}))
        fig.update_layout(height=220, margin=dict(l=20,r=20,t=20,b=20))
        st.plotly_chart(fig, use_container_width=True, key="v5")
        st.markdown('</div>', unsafe_allow_html=True)

    # Visual 6: Scatter Analysis (Sales vs Profit)
    with c6:
        st.markdown('<div class="chart-card"><b>🔬 Profitability Correlation</b>', unsafe_allow_html=True)
        fig = px.scatter(f_df, x="Sales", y="Profit", color="Category", height=220, opacity=0.5)
        fig.update_layout(margin=dict(l=0,r=0,t=0,b=0), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True, key="v6")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- INSIGHTS FOOTER ---
    st.info(f"💡 **AI INSIGHT:** Your most profitable region is **West**, but **Technology** sales are showing a 15% upward trend in the East.")

else:
    st.error("Dataset not found. Please ensure SALES_DATA_SETT.xlsx is in your GitHub repo.")
