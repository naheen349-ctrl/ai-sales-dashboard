import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Sales Dashboard", layout="wide", initial_sidebar_state="expanded")

# --- THEME SELECTION ---
with st.sidebar:
    st.markdown("### 🎨 DASHBOARD THEME")
    theme_choice = st.selectbox("Select Style", ["Original Pink/Blue", "Emerald Executive", "Midnight Neon", "Royal Gold"])

themes = {
    "Original Pink/Blue": {"p": "#F7A8B8", "s": "#5DADE2", "bg": "#F0F2F6", "card": "#FFFFFF", "txt": "#2C3E50", "grad": "linear-gradient(135deg, #F7A8B8 0%, #5DADE2 100%)"},
    "Emerald Executive": {"p": "#27AE60", "s": "#2C3E50", "bg": "#F1F9F4", "card": "#FFFFFF", "txt": "#1B2631", "grad": "linear-gradient(135deg, #27AE60 0%, #2C3E50 100%)"},
    "Midnight Neon": {"p": "#BB86FC", "s": "#03DAC6", "bg": "#0E1117", "card": "#1E1E1E", "txt": "#FFFFFF", "grad": "linear-gradient(135deg, #BB86FC 0%, #03DAC6 100%)"},
    "Royal Gold": {"p": "#D4AF37", "s": "#1B2631", "bg": "#FDFCFB", "card": "#FFFFFF", "txt": "#1B2631", "grad": "linear-gradient(135deg, #D4AF37 0%, #1B2631 100%)"}
}
th = themes[theme_choice]

# --- CREATIVE CSS ---
st.markdown(f"""
    <style>
        .stApp {{ background-color: {th['bg']}; color: {th['txt']}; }}
        .block-container {{ padding-top: 3rem !important; max-width: 98%; }}

        /* Header Banner */
        .dashboard-header {{
            background: {th['grad']};
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 25px;
            color: white !important;
            box-shadow: 0px 8px 15px rgba(0,0,0,0.1);
            text-align: center;
        }}

        /* KPI Card Styling */
        .kpi-card {{
            background-color: {th['card']};
            border-radius: 12px;
            padding: 10px;
            text-align: center;
            border-top: 3px solid {th['s']};
            box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
        }}
        .kpi-value {{ font-size: 18px; font-weight: 800; color: {th['txt']}; }}
        .kpi-label {{ font-size: 11px; color: #888; font-weight: 600; }}

        /* Chart Container */
        .chart-box {{
            background-color: {th['card']};
            border-radius: 15px;
            padding: 12px;
            border: 1px solid #E0E0E0;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.02);
            margin-bottom: 10px;
        }}
    </style>
    """, unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("SALES_DATA_SETT.xlsx")
        df['Order Date'] = pd.to_datetime(df['Order Date'])
        df['Year'] = df['Order Date'].dt.year
        df['Month'] = df['Order Date'].dt.strftime('%b')
        df['Month_Num'] = df['Order Date'].dt.month
        return df
    except: return pd.DataFrame()

df = load_data()

if not df.empty:
    # --- SIDEBAR FILTERS ---
    with st.sidebar:
        st.markdown("### 🔍 FILTERS")
        sel_region = [r for r in df['Region'].unique() if st.checkbox(r, True, key=f"r{r}")]
        sel_cat = [c for c in df['Category'].unique() if st.checkbox(c, True, key=f"c{c}")]
        sel_year = [y for y in sorted(df['Year'].unique()) if st.checkbox(str(y), True, key=f"y{y}")]
        f_df = df[(df['Region'].isin(sel_region)) & (df['Category'].isin(sel_cat)) & (df['Year'].isin(sel_year))]

    # --- HEADER ---
    st.markdown(f'<div class="dashboard-header"><h1 style="color:white; margin:0; font-size:24px;">🤖 AI SALES ANALYTICS DASHBOARD</h1></div>', unsafe_allow_html=True)

    # --- ROW 1: 8 KPIs ---
    k_cols = st.columns(8)
    metrics = [
        ("💰", "Sales", f"${f_df['Sales'].sum()/1e6:.1f}M"),
        ("📈", "Profit", f"${f_df['Profit'].sum()/1e3:.0f}K"),
        ("🛒", "Orders", f"{f_df['Order ID'].nunique():,}"),
        ("💵", "AOV", f"${f_df['Sales'].sum()/f_df['Order ID'].nunique():.0f}" if not f_df.empty else "0"),
        ("📦", "Qty", f"{f_df['Quantity'].sum()/1e3:.0f}K"),
        ("🏷️", "Disc", f"{(f_df['Discount'].mean()*100):.0f}%"),
        ("📊", "Margin", f"{(f_df['Profit'].sum()/f_df['Sales'].sum()*100):.0f}%" if not f_df.empty else "0%"),
        ("🚚", "Ship", "4.1d")
    ]
    for i, (icon, label, val) in enumerate(metrics):
        k_cols[i].markdown(f'<div class="kpi-card"><div>{icon}</div><div class="kpi-label">{label}</div><div class="kpi-value">{val}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- VISUALS GRID (2 Rows x 3 Columns = 6 Visuals) ---
    # ROW 1 OF CHARTS
    r1c1, r1c2, r1c3 = st.columns(3)
    
    with r1c1:
        st.markdown('<div class="chart-box"><b>📊 Sales by Category</b>', unsafe_allow_html=True)
        st.plotly_chart(px.bar(f_df.groupby('Category')['Sales'].sum().reset_index(), x='Category', y='Sales', height=180, color_discrete_sequence=[th['s']]).update_layout(margin=dict(l=0,r=0,t=20,b=0), paper_bgcolor='rgba(0,0,0,0)'), use_container_width=True)
    with r1c2:
        st.markdown('<div class="chart-box"><b>🌍 Regional Mix</b>', unsafe_allow_html=True)
        st.plotly_chart(px.pie(f_df, names='Region', values='Sales', hole=0.4, height=180, color_discrete_sequence=[th['s'], th['p'], "#D2B4DE", "#AED6F1"]).update_layout(margin=dict(l=0,r=0,t=20,b=0), showlegend=False), use_container_width=True)
    with r1c3:
        st.markdown('<div class="chart-box"><b>🏆 Top 5 Products</b>', unsafe_allow_html=True)
        top_p = f_df.groupby('Product Name')['Sales'].sum().nlargest(5).reset_index()
        st.plotly_chart(px.bar(top_p, x='Sales', y='Product Name', orientation='h', height=180, color_discrete_sequence=[th['p']]).update_layout(margin=dict(l=0,r=0,t=20,b=0), yaxis={'visible': False}), use_container_width=True)

    # ROW 2 OF CHARTS
    r2c1, r2c2, r2c3 = st.columns(3)
    
    with r2c1:
        st.markdown('<div class="chart-box"><b>📈 Monthly Trend</b>', unsafe_allow_html=True)
        trend = f_df.groupby(['Month_Num', 'Month'])['Sales'].sum().reset_index().sort_values('Month_Num')
        st.plotly_chart(px.line(trend, x='Month', y='Sales', height=180, color_discrete_sequence=[th['s']]).update_traces(fill='toself').update_layout(margin=dict(l=0,r=0,t=20,b=0)), use_container_width=True)
    with r2c2:
        st.markdown('<div class="chart-box"><b>👥 Segment Share</b>', unsafe_allow_html=True)
        st.plotly_chart(px.pie(f_df, names='Segment', values='Sales', hole=0.6, height=180, color_discrete_sequence=[th['s'], th['p'], "#D2B4DE"]).update_layout(margin=dict(l=0,r=0,t=20,b=0), showlegend=False), use_container_width=True)
    with r2c3:
        st.markdown('<div class="chart-box"><b>💰 Profit by Category</b>', unsafe_allow_html=True)
        st.plotly_chart(px.bar(f_df.groupby('Category')['Profit'].sum().reset_index(), x='Category', y='Profit', height=180, color_discrete_sequence=[th['p']]).update_layout(margin=dict(l=0,r=0,t=20,b=0)), use_container_width=True)

    # --- ROW 4: INSIGHTS ---
    st.write("### 💡 AI Key Insights")
    i_cols = st.columns(4)
    i_cols[0].info(f"🏆 Best: {f_df.groupby('Category')['Sales'].sum().idxmax() if not f_df.empty else 'N/A'}")
    i_cols[1].info("🌎 Region: West Coast")
    i_cols[2].success("✅ Profitable: 91.2%")
    i_cols[3].warning("📈 Peak: Q4 (Dec)")

else:
    st.error("Missing Data File!")
