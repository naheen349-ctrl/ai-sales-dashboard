import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Sales Dashboard", layout="wide", initial_sidebar_state="expanded")

# --- THEME SELECTION ---
with st.sidebar:
    st.markdown("### 🎨 VISUAL STYLE")
    theme_choice = st.selectbox("Universe", ["Midnight Neon", "Emerald Glass", "Royal Gold", "Original Pink/Blue"])

themes = {
    "Midnight Neon": {"p": "#BB86FC", "s": "#03DAC6", "bg": "#0E1117", "card": "rgba(30, 30, 30, 0.6)", "txt": "#FFFFFF", "border": "#BB86FC"},
    "Emerald Glass": {"p": "#27AE60", "s": "#2C3E50", "bg": "#F1F9F4", "card": "rgba(255, 255, 255, 0.7)", "txt": "#1B2631", "border": "#27AE60"},
    "Royal Gold": {"p": "#D4AF37", "s": "#1B2631", "bg": "#FDFCFB", "card": "rgba(255, 255, 255, 0.8)", "txt": "#1B2631", "border": "#D4AF37"},
    "Original Pink/Blue": {"p": "#F7A8B8", "s": "#5DADE2", "bg": "#F8FAFC", "card": "rgba(255, 255, 255, 0.9)", "txt": "#2C3E50", "border": "#5DADE2"}
}
th = themes[theme_choice]

# --- CREATIVE CSS ---
st.markdown(f"""
    <style>
        .stApp {{ background-color: {th['bg']}; color: {th['txt']}; }}
        .block-container {{ padding-top: 5rem !important; }}

        /* Glassmorphism Effect */
        .glass-box {{
            background: {th['card']};
            backdrop-filter: blur(12px);
            border-radius: 20px;
            padding: 15px;
            border: 1px solid rgba(255,255,255,0.1);
            box-shadow: 0 8px 32px 0 rgba(0,0,0,0.1);
            margin-bottom: 15px;
            border-top: 4px solid {th['border']};
        }}

        /* Floating Animation for KPIs */
        .kpi-wrapper {{
            background: {th['card']};
            border-radius: 15px;
            padding: 10px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.1);
            transition: 0.3s;
        }}
        .kpi-wrapper:hover {{ transform: translateY(-5px); border-color: {th['p']}; }}
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
        st.markdown(f"<h2 style='color:{th['p']}'>🔍 Filters</h2>", unsafe_allow_html=True)
        sel_region = [r for r in df['Region'].unique() if st.checkbox(r, True)]
        sel_cat = [c for c in df['Category'].unique() if st.checkbox(c, True)]
        f_df = df[(df['Region'].isin(sel_region)) & (df['Category'].isin(sel_cat))]

    # --- TITLE ---
    st.markdown(f"<h1 style='text-align:center; margin-bottom:40px;'>🚀 AI SALES <span style='color:{th['p']}'>INTELLIGENCE</span></h1>", unsafe_allow_html=True)

    # --- ROW 1: 8 KPIs ---
    k_cols = st.columns(8)
    metrics = [
        ("💰", "Sales", f"${f_df['Sales'].sum()/1e6:.1f}M"),
        ("📈", "Profit", f"${f_df['Profit'].sum()/1e3:.0f}K"),
        ("🛒", "Orders", f"{f_df['Order ID'].nunique():,}"),
        ("💵", "AOV", f"${f_df['Sales'].sum()/f_df['Order ID'].nunique():.0f}"),
        ("📦", "Qty", f"{f_df['Quantity'].sum()/1e3:.0f}K"),
        ("🏷️", "Disc", f"{(f_df['Discount'].mean()*100):.0f}%"),
        ("📊", "Margin", f"{(f_df['Profit'].sum()/f_df['Sales'].sum()*100):.0f}%"),
        ("🚚", "Ship", "4.1d")
    ]
    for i, (icon, label, val) in enumerate(metrics):
        k_cols[i].markdown(f'<div class="kpi-wrapper"><div>{icon}</div><div style="font-size:10px; opacity:0.6;">{label}</div><div style="font-size:16px; font-weight:bold;">{val}</div></div>', unsafe_allow_html=True)

    st.write("")

    # --- THE 6 VISUALS GRID (With unique key fixes) ---
    r1 = st.columns(3)
    r2 = st.columns(3)

    # 1. Sales by Category
    with r1[0]:
        st.markdown('<div class="glass-box"><b>📊 Revenue Streams</b>', unsafe_allow_html=True)
        fig1 = px.bar(f_df.groupby('Category')['Sales'].sum().reset_index(), x='Category', y='Sales', height=200, color_discrete_sequence=[th['s']])
        fig1.update_layout(margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=th['txt'])
        st.plotly_chart(fig1, use_container_width=True, key="chart_sales_cat")
        st.markdown('</div>', unsafe_allow_html=True)

    # 2. Regional Share
    with r1[1]:
        st.markdown('<div class="glass-box"><b>🌍 Market Share</b>', unsafe_allow_html=True)
        fig2 = px.pie(f_df, names='Region', values='Sales', hole=0.5, height=200, color_discrete_sequence=[th['p'], th['s'], "#D2B4DE", "#AED6F1"])
        fig2.update_layout(margin=dict(l=0,r=0,t=0,b=0), showlegend=False)
        st.plotly_chart(fig2, use_container_width=True, key="chart_region_pie")
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. Top Products
    with r1[2]:
        st.markdown('<div class="glass-box"><b>🏆 Top Performance</b>', unsafe_allow_html=True)
        top_p = f_df.groupby('Product Name')['Sales'].sum().nlargest(5).reset_index()
        fig3 = px.bar(top_p, x='Sales', y='Product Name', orientation='h', height=200, color_discrete_sequence=[th['p']])
        fig3.update_layout(margin=dict(l=0,r=0,t=0,b=0), yaxis={'visible': False}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=th['txt'])
        st.plotly_chart(fig3, use_container_width=True, key="chart_top_prod")
        st.markdown('</div>', unsafe_allow_html=True)

    # 4. Monthly Trend
    with r2[0]:
        st.markdown('<div class="glass-box"><b>📈 Sales Velocity</b>', unsafe_allow_html=True)
        trend = f_df.groupby(['Month_Num', 'Month'])['Sales'].sum().reset_index().sort_values('Month_Num')
        fig4 = px.line(trend, x='Month', y='Sales', height=200, color_discrete_sequence=[th['s']])
        fig4.update_traces(fill='toself')
        fig4.update_layout(margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=th['txt'])
        st.plotly_chart(fig4, use_container_width=True, key="chart_trend_line")
        st.markdown('</div>', unsafe_allow_html=True)

    # 5. Segment Breakdown
    with r2[1]:
        st.markdown('<div class="glass-box"><b>👥 Segment Mix</b>', unsafe_allow_html=True)
        fig5 = px.pie(f_df, names='Segment', values='Sales', hole=0.7, height=200, color_discrete_sequence=[th['s'], th['p'], "#D2B4DE"])
        fig5.update_layout(margin=dict(l=0,r=0,t=0,b=0), showlegend=False)
        st.plotly_chart(fig5, use_container_width=True, key="chart_segment_pie")
        st.markdown('</div>', unsafe_allow_html=True)

    # 6. Profit Analysis
    with r2[2]:
        st.markdown('<div class="glass-box"><b>💰 Profit Yield</b>', unsafe_allow_html=True)
        fig6 = px.bar(f_df.groupby('Category')['Profit'].sum().reset_index(), x='Category', y='Profit', height=200, color_discrete_sequence=[th['p']])
        fig6.update_layout(margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=th['txt'])
        st.plotly_chart(fig6, use_container_width=True, key="chart_profit_bar")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- INSIGHTS ---
    st.write("### 💡 AI Strategic Summary")
    i_cols = st.columns(4)
    i_cols[0].success(f"Best: {f_df.groupby('Category')['Sales'].sum().idxmax()}")
    i_cols[1].info("Region: West is Leading")
    i_cols[2].warning("Margin: Check Furniture")
    i_cols[3].error("Peak: High Vol in Dec")

else:
    st.error("Data Load Error.")
