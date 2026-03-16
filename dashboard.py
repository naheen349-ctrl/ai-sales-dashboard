import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIG (Laptop Screen Optimized) ---
st.set_page_config(page_title="AI Intelligence Pro", layout="wide", initial_sidebar_state="expanded")

# --- THEME CONFIG ---
with st.sidebar:
    st.markdown("### 🎨 VISUAL UNIVERSE")
    theme_choice = st.selectbox("Select Theme", ["Midnight Neon", "Emerald Glass", "Oceanic Pro", "Sunset Rose"])

themes = {
    "Midnight Neon": {"p": "#BB86FC", "s": "#03DAC6", "bg": "#0E1117", "card": "rgba(30, 30, 30, 0.7)", "txt": "#FFFFFF", "accent": "#BB86FC"},
    "Emerald Glass": {"p": "#27AE60", "s": "#2C3E50", "bg": "#F1F9F4", "card": "rgba(255, 255, 255, 0.7)", "txt": "#1B2631", "accent": "#27AE60"},
    "Oceanic Pro": {"p": "#5DADE2", "s": "#21618C", "bg": "#EBF5FB", "card": "rgba(255, 255, 255, 0.8)", "txt": "#1B4F72", "accent": "#2E86C1"},
    "Sunset Rose": {"p": "#F7A8B8", "s": "#C0392B", "bg": "#FDF2F4", "card": "rgba(255, 255, 255, 0.9)", "txt": "#641E16", "accent": "#EC7063"}
}
th = themes[theme_choice]

# --- CUSTOM CREATIVE CSS ---
st.markdown(f"""
    <style>
        .stApp {{ background-color: {th['bg']}; color: {th['txt']}; }}
        
        /* Glassmorphism Containers */
        .glass-container {{
            background: {th['card']};
            backdrop-filter: blur(15px);
            border-radius: 20px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            transition: 0.4s ease;
        }}
        .glass-container:hover {{
            transform: translateY(-5px);
            border: 1px solid {th['p']};
        }}

        /* KPI Style */
        .kpi-box {{
            text-align: center;
            padding: 12px;
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            border-bottom: 3px solid {th['p']};
        }}

        /* Heading Style */
        .main-title {{
            font-size: 36px !important;
            font-weight: 900 !important;
            background: linear-gradient(90deg, {th['p']}, {th['s']});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 30px;
        }}

        /* Lower the content slightly */
        .block-container {{ padding-top: 5rem !important; }}
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
    # --- SIDEBAR (COLUMN STYLE FILTERS) ---
    with st.sidebar:
        st.markdown("### 🔍 DATA CONTROL")
        sel_region = [r for r in df['Region'].unique() if st.checkbox(f"🌎 {r}", True)]
        sel_cat = [c for c in df['Category'].unique() if st.checkbox(f"📦 {c}", True)]
        sel_year = [y for y in sorted(df['Year'].unique()) if st.checkbox(f"📅 {y}", True)]
        
        f_df = df[(df['Region'].isin(sel_region)) & (df['Category'].isin(sel_cat)) & (df['Year'].isin(sel_year))]

    # --- MAIN UI ---
    st.markdown('<div class="main-title">🚀 NEURAL SALES INTELLIGENCE PRO</div>', unsafe_allow_html=True)

    # --- 8 KPIs (ROW 1) ---
    k_cols = st.columns(8)
    metrics = [
        ("💰", "Revenue", f"${f_df['Sales'].sum()/1e6:.1f}M"),
        ("📈", "Net Profit", f"${f_df['Profit'].sum()/1e3:.0f}K"),
        ("🛒", "Orders", f"{f_df['Order ID'].nunique():,}"),
        ("💵", "Avg Ticket", f"${f_df['Sales'].sum()/f_df['Order ID'].nunique():.0f}"),
        ("📦", "Units", f"{f_df['Quantity'].sum()/1e3:.0f}K"),
        ("🏷️", "Discount", f"{(f_df['Discount'].mean()*100):.0f}%"),
        ("📊", "Margin", f"{(f_df['Profit'].sum()/f_df['Sales'].sum()*100):.0f}%"),
        ("🚚", "Delivery", "4.1d")
    ]
    
    for i, (icon, label, val) in enumerate(metrics):
        k_cols[i].markdown(f"""
            <div class="kpi-box">
                <div style='font-size:24px;'>{icon}</div>
                <div style='font-size:10px; opacity:0.7;'>{label}</div>
                <div style='font-size:18px; font-weight:bold;'>{val}</div>
            </div>
        """, unsafe_allow_html=True)

    st.write("")

    # --- 6 VISUALS (2 ROWS x 3 COLUMNS) ---
    r1_cols = st.columns(3)
    r2_cols = st.columns(3)

    # Chart 1: Category Bar
    with r1_cols[0]:
        st.markdown('<div class="glass-container"><b>📊 Sales Dynamics</b>', unsafe_allow_html=True)
        fig1 = px.bar(f_df.groupby('Category')['Sales'].sum().reset_index(), x='Category', y='Sales', height=200, color_discrete_sequence=[th['p']])
        fig1.update_layout(margin=dict(l=0,r=0,t=10,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=th['txt'])
        st.plotly_chart(fig1, use_container_width=True, key="unique_chart_1")
        st.markdown('</div>', unsafe_allow_html=True)

    # Chart 2: Regional Donut
    with r1_cols[1]:
        st.markdown('<div class="glass-container"><b>🌍 Market Dominance</b>', unsafe_allow_html=True)
        fig2 = px.pie(f_df, names='Region', values='Sales', hole=0.6, height=200, color_discrete_sequence=[th['p'], th['s'], "#8E44AD", "#34495E"])
        fig2.update_layout(margin=dict(l=0,r=0,t=10,b=0), showlegend=False)
        st.plotly_chart(fig2, use_container_width=True, key="unique_chart_2")
        st.markdown('</div>', unsafe_allow_html=True)

    # Chart 3: Product H-Bar
    with r1_cols[2]:
        st.markdown('<div class="glass-container"><b>🏆 Elite Products</b>', unsafe_allow_html=True)
        top_p = f_df.groupby('Product Name')['Sales'].sum().nlargest(5).reset_index()
        fig3 = px.bar(top_p, x='Sales', y='Product Name', orientation='h', height=200, color_discrete_sequence=[th['s']])
        fig3.update_layout(margin=dict(l=0,r=0,t=10,b=0), yaxis={'visible': False}, paper_bgcolor='rgba(0,0,0,0)', font_color=th['txt'])
        st.plotly_chart(fig3, use_container_width=True, key="unique_chart_3")
        st.markdown('</div>', unsafe_allow_html=True)

    # Chart 4: Monthly Area
    with r2_cols[0]:
        st.markdown('<div class="glass-container"><b>📈 Growth Velocity</b>', unsafe_allow_html=True)
        trend = f_df.groupby(['Month_Num', 'Month'])['Sales'].sum().reset_index().sort_values('Month_Num')
        fig4 = px.area(trend, x='Month', y='Sales', height=200, color_discrete_sequence=[th['p']])
        fig4.update_layout(margin=dict(l=0,r=0,t=10,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=th['txt'])
        st.plotly_chart(fig4, use_container_width=True, key="unique_chart_4")
        st.markdown('</div>', unsafe_allow_html=True)

    # Chart 5: Segment Pie
    with r2_cols[1]:
        st.markdown('<div class="glass-container"><b>👥 Customer Segments</b>', unsafe_allow_html=True)
        fig5 = px.pie(f_df, names='Segment', values='Sales', height=200, color_discrete_sequence=[th['s'], th['p'], "#D2B4DE"])
        fig5.update_layout(margin=dict(l=0,r=0,t=10,b=0), showlegend=False)
        st.plotly_chart(fig5, use_container_width=True, key="unique_chart_5")
        st.markdown('</div>', unsafe_allow_html=True)

    # Chart 6: Profit Bar
    with r2_cols[2]:
        st.markdown('<div class="glass-container"><b>💰 Profit Yield</b>', unsafe_allow_html=True)
        fig6 = px.bar(f_df.groupby('Category')['Profit'].sum().reset_index(), x='Category', y='Profit', height=200, color_discrete_sequence=[th['s']])
        fig6.update_layout(margin=dict(l=0,r=0,t=10,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=th['txt'])
        st.plotly_chart(fig6, use_container_width=True, key="unique_chart_6")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- INSIGHTS ---
    st.markdown("### 💡 AI NEURAL SUMMARY")
    i_cols = st.columns(4)
    with i_cols[0]: st.success("Best: Technology")
    with i_cols[1]: st.info("Region: West Coast")
    with i_cols[2]: st.warning("Risk: Supply Chain")
    with i_cols[3]: st.error("Action: Q4 Restock")

else:
    st.error("Missing Data File!")
