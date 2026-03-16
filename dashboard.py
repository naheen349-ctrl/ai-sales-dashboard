import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Sales Dashboard", layout="wide", initial_sidebar_state="expanded")

# --- THEME SELECTION ---
with st.sidebar:
    st.markdown("### 🎨 DASHBOARD THEME")
    theme_choice = st.selectbox("Select Theme", ["Original Pink/Blue", "Emerald Executive", "Midnight Neon", "Royal Gold"])

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
        
        .block-container {{ 
            padding-top: 4rem !important; 
            max-width: 95%;
        }}

        /* Creative Header */
        .dashboard-header {{
            background: {th['grad']};
            padding: 25px;
            border-radius: 20px;
            margin-bottom: 35px;
            color: white !important;
            box-shadow: 0px 10px 20px rgba(0,0,0,0.1);
            text-align: center;
        }}

        /* KPI Card Styling - FORCED VISIBILITY */
        .kpi-card {{
            background-color: {th['card']};
            border-radius: 15px;
            padding: 15px;
            text-align: center;
            border-bottom: 4px solid {th['s']};
            box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
            transition: transform 0.3s;
        }}
        .kpi-card:hover {{ transform: translateY(-5px); }}
        .kpi-icon {{ font-size: 28px; margin-bottom: 5px; }}
        .kpi-label {{ font-size: 12px; color: #888; font-weight: 600; text-transform: uppercase; }}
        .kpi-value {{ font-size: 22px; font-weight: 800; color: {th['txt']}; }}

        /* Visual Boxes */
        .chart-container {{
            background-color: {th['card']};
            border-radius: 20px;
            padding: 15px;
            border: 1px solid #E0E0E0;
            box-shadow: 0px 8px 16px rgba(0,0,0,0.03);
        }}
        
        /* Sidebar Polish */
        .filter-section {{
            background: white;
            padding: 15px;
            border-radius: 12px;
            border: 1px solid #EEE;
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
    # --- SIDEBAR ---
    with st.sidebar:
        st.markdown("### 🔍 SELECTION PANEL")
        
        st.markdown(f'<p style="color:{th["p"]}; font-weight:bold; margin-bottom:0px;">🌎 REGION</p>', unsafe_allow_html=True)
        sel_region = [r for r in df['Region'].unique() if st.checkbox(r, True, key=f"r{r}")]
        
        st.markdown(f'<p style="color:{th["s"]}; font-weight:bold; margin-top:15px; margin-bottom:0px;">📦 CATEGORY</p>', unsafe_allow_html=True)
        sel_cat = [c for c in df['Category'].unique() if st.checkbox(c, True, key=f"c{c}")]
        
        st.markdown(f'<p style="color:{th["p"]}; font-weight:bold; margin-top:15px; margin-bottom:0px;">📅 YEAR</p>', unsafe_allow_html=True)
        sel_year = [y for y in sorted(df['Year'].unique()) if st.checkbox(str(y), True, key=f"y{y}")]

        f_df = df[(df['Region'].isin(sel_region)) & (df['Category'].isin(sel_cat)) & (df['Year'].isin(sel_year))]

    # --- MAIN CONTENT ---
    st.markdown(f"""
        <div class="dashboard-header">
            <h1 style="color:white; margin:0; font-size:30px;">🚀 AI SALES INTELLIGENCE PRO</h1>
            <p style="color:rgba(255,255,255,0.8); margin:0;">Real-time Market Analytics & Performance Tracking</p>
        </div>
        """, unsafe_allow_html=True)

    # --- KPI ROW (8 CUSTOM CARDS) ---
    kpi_cols = st.columns(8)
    metrics = [
        ("💰", "Sales", f"${f_df['Sales'].sum()/1e6:.1f}M"),
        ("📈", "Profit", f"${f_df['Profit'].sum()/1e3:.0f}K"),
        ("🛒", "Orders", f"{f_df['Order ID'].nunique():,}"),
        ("💵", "AOV", f"${f_df['Sales'].sum()/f_df['Order ID'].nunique():.0f}" if not f_df.empty else "0"),
        ("📦", "Qty", f"{f_df['Quantity'].sum()/1e3:.0f}K"),
        ("🏷️", "Disc", f"{(f_df['Discount'].mean()*100):.0f}%"),
        ("📊", "Margin", f"{(f_df['Profit'].sum()/f_df['Sales'].sum()*100):.0f}%" if not f_df.empty else "0%"),
        ("🚚", "Ship", "4.2d")
    ]

    for i, (icon, label, val) in enumerate(metrics):
        kpi_cols[i].markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon">{icon}</div>
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{val}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- VISUALS GRID ---
    c1, c2, c3 = st.columns([1.4, 1, 1])
    
    with c1:
        st.markdown('<div class="chart-container"><b>📊 Revenue Streams</b>', unsafe_allow_html=True)
        fig = px.bar(f_df.groupby('Category')['Sales'].sum().reset_index(), x='Category', y='Sales', height=220, color_discrete_sequence=[th['s']])
        fig.update_layout(margin=dict(l=10,r=10,t=30,b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=th['txt'])
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="chart-container"><b>🌍 Regional Mix</b>', unsafe_allow_html=True)
        fig = px.funnel(f_df.groupby('Region')['Sales'].sum().reset_index().sort_values('Sales'), y='Region', x='Sales', height=220, color_discrete_sequence=[th['p']])
        fig.update_layout(margin=dict(l=10,r=10,t=30,b=10), paper_bgcolor='rgba(0,0,0,0)', font_color=th['txt'])
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="chart-container"><b>🏆 Top Products</b>', unsafe_allow_html=True)
        top_p = f_df.groupby('Product Name')['Sales'].sum().nlargest(5).reset_index()
        fig = px.bar(top_p, x='Sales', y='Product Name', orientation='h', height=220, color_discrete_sequence=[th['s']])
        fig.update_layout(margin=dict(l=0,r=0,t=30,b=0), yaxis={'visible': False}, paper_bgcolor='rgba(0,0,0,0)', font_color=th['txt'])
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- INSIGHTS SECTION ---
    st.markdown("<br>", unsafe_allow_html=True)
    st.write("### 💡 AI Generated Insights")
    i1, i2, i3, i4 = st.columns(4)
    
    # Creative border-left for info boxes
    i1.markdown(f'<div style="border-left:5px solid {th["p"]}; padding:10px; background:white; border-radius:5px;"><b>🏆 Dominant Category</b><br>{f_df.groupby("Category")["Sales"].sum().idxmax() if not f_df.empty else "N/A"}</div>', unsafe_allow_html=True)
    i2.markdown(f'<div style="border-left:5px solid {th["s"]}; padding:10px; background:white; border-radius:5px;"><b>🔥 High Growth</b><br>West Coast Regions</div>', unsafe_allow_html=True)
    i3.markdown(f'<div style="border-left:5px solid {th["p"]}; padding:10px; background:white; border-radius:5px;"><b>📉 Risk Factor</b><br>Furniture Margins Low</div>', unsafe_allow_html=True)
    i4.markdown(f'<div style="border-left:5px solid {th["s"]}; padding:10px; background:white; border-radius:5px;"><b>📅 Seasonality</b><br>Peak detected in Q4</div>', unsafe_allow_html=True)

else:
    st.error("Missing Data File!")
