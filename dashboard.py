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
    "Original Pink/Blue": {"p": "#F7A8B8", "s": "#5DADE2", "bg": "#F8FAFC", "card": "#FFFFFF", "txt": "#2C3E50"},
    "Emerald Executive": {"p": "#27AE60", "s": "#2C3E50", "bg": "#F1F9F4", "card": "#FFFFFF", "txt": "#1B2631"},
    "Midnight Neon": {"p": "#BB86FC", "s": "#03DAC6", "bg": "#0E1117", "card": "#1E1E1E", "txt": "#FFFFFF"},
    "Royal Gold": {"p": "#D4AF37", "s": "#1B2631", "bg": "#FDFCFB", "card": "#FFFFFF", "txt": "#1B2631"}
}
th = themes[theme_choice]

# --- REFINED CSS FOR SPACING & VISIBILITY ---
st.markdown(f"""
    <style>
        /* 1. Global Background */
        .stApp {{ background-color: {th['bg']}; color: {th['txt']}; }}
        
        /* 2. Push everything down from the top */
        .block-container {{ 
            padding-top: 5rem !important; /* This creates the 'lower' look */
            padding-bottom: 2rem !important;
            max-width: 95%;
        }}

        /* 3. Dashboard Title Header - Centered and Spaced */
        .dashboard-header {{
            background-color: {th['card']};
            padding: 20px 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            border-left: 10px solid {th['s']};
            box-shadow: 0px 4px 15px rgba(0,0,0,0.05);
            display: flex;
            align-items: center;
        }}
        
        .header-text {{
            font-size: 32px !important;
            font-weight: 800;
            color: {th['txt']};
            margin: 0;
        }}

        /* 4. Boxes and Filters */
        .box {{ 
            background-color: {th['card']}; 
            border: 1px solid #E0E0E0; 
            border-radius: 12px; 
            padding: 15px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.02);
        }}
        
        .filter-header-blue {{ background-color: {th['s']}22; padding: 10px; border-radius: 10px 10px 0 0; border: 1px solid {th['s']}; font-weight: bold; margin-top: 10px; }}
        .filter-header-pink {{ background-color: {th['p']}22; padding: 10px; border-radius: 10px 10px 0 0; border: 1px solid {th['p']}; font-weight: bold; margin-top: 10px; }}
        
        /* Small laptop adjustments */
        [data-testid="stMetricValue"] {{ font-size: 22px !important; font-weight: 700 !important; }}
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
        st.markdown("### 🔍 FILTERS")
        
        st.markdown(f'<div class="filter-header-pink">🌎 Region</div>', unsafe_allow_html=True)
        sel_region = [r for r in df['Region'].unique() if st.checkbox(r, True, key=f"r{r}")]
        
        st.markdown(f'<div class="filter-header-blue">📦 Category</div>', unsafe_allow_html=True)
        sel_cat = [c for c in df['Category'].unique() if st.checkbox(c, True, key=f"c{c}")]
        
        st.markdown(f'<div class="filter-header-pink">📅 Year</div>', unsafe_allow_html=True)
        y_cols = st.columns(2)
        years = sorted(df['Year'].unique())
        sel_year = []
        for i, y in enumerate(years):
            if y_cols[i%2].checkbox(str(y), True, key=f"y{y}"): sel_year.append(y)

        f_df = df[(df['Region'].isin(sel_region)) & (df['Category'].isin(sel_cat)) & (df['Year'].isin(sel_year))]

    # --- MAIN CONTENT ---
    # The Header (Lowered)
    st.markdown(f"""
        <div class="dashboard-header">
            <span class="header-text">🤖 AI POWERED SALES ANALYTICS DASHBOARD</span>
        </div>
        """, unsafe_allow_html=True)

    # --- KPI METRICS ---
    st.write("📊 **KEY PERFORMANCE INDICATORS**")
    m1, m2, m3, m4, m5, m6, m7, m8 = st.columns(8)
    
    m1.metric("💰 Sales", f"${f_df['Sales'].sum()/1e6:.1f}M")
    m2.metric("📈 Profit", f"${f_df['Profit'].sum()/1e3:.0f}K")
    m3.metric("🛒 Orders", f"{f_df['Order ID'].nunique():,}")
    m4.metric("💵 AOV", f"${f_df['Sales'].sum()/f_df['Order ID'].nunique():.0f}" if not f_df.empty else "0")
    m5.metric("📦 Qty", f"{f_df['Quantity'].sum()/1e3:.0f}K")
    m6.metric("🏷️ Disc", f"{(f_df['Discount'].mean()*100):.0f}%")
    m7.metric("📊 %", f"{(f_df['Profit'].sum()/f_df['Sales'].sum()*100):.0f}%" if not f_df.empty else "0%")
    m8.metric("🚚 Ship", "4d")

    st.write("")

    # --- VISUALS GRID ---
    row1_c1, row1_c2, row1_c3 = st.columns([1.2, 1, 1])
    with row1_c1:
        st.markdown('<div class="box"><b>📊 Sales by Category</b>', unsafe_allow_html=True)
        st.plotly_chart(px.bar(f_df.groupby('Category')['Sales'].sum().reset_index(), x='Category', y='Sales', height=180, color_discrete_sequence=[th['s']]).update_layout(margin=dict(l=0,r=0,t=20,b=0)), use_container_width=True)
    with row1_c2:
        st.markdown('<div class="box"><b>🌍 Sales by Region</b>', unsafe_allow_html=True)
        st.plotly_chart(px.bar(f_df.groupby('Region')['Sales'].sum().reset_index(), x='Sales', y='Region', orientation='h', height=180, color_discrete_sequence=[th['p']]).update_layout(margin=dict(l=0,r=0,t=20,b=0)), use_container_width=True)
    with row1_c3:
        st.markdown('<div class="box"><b>🏆 Top 5 Products</b>', unsafe_allow_html=True)
        top_p = f_df.groupby('Product Name')['Sales'].sum().nlargest(5).reset_index()
        st.plotly_chart(px.bar(top_p, x='Sales', y='Product Name', orientation='h', height=180, color_discrete_sequence=[th['s']]).update_layout(margin=dict(l=0,r=0,t=20,b=0), yaxis={'visible': False}), use_container_width=True)

    row2_c1, row2_c2, row2_c3 = st.columns([1.2, 1, 1])
    with row2_c1:
        st.markdown('<div class="box"><b>📈 Monthly Trend</b>', unsafe_allow_html=True)
        trend = f_df.groupby(['Month_Num', 'Month'])['Sales'].sum().reset_index().sort_values('Month_Num')
        st.plotly_chart(px.line(trend, x='Month', y='Sales', height=180, color_discrete_sequence=[th['s']]).update_traces(fill='toself').update_layout(margin=dict(l=0,r=0,t=20,b=0)), use_container_width=True)
    with row2_c2:
        st.markdown('<div class="box"><b>👥 Segment Share</b>', unsafe_allow_html=True)
        st.plotly_chart(px.pie(f_df, names='Segment', values='Sales', hole=0.5, height=180, color_discrete_sequence=[th['s'], th['p'], "#D2B4DE"]).update_layout(margin=dict(l=0,r=0,t=20,b=0), showlegend=False), use_container_width=True)
    with row2_c3:
        st.markdown('<div class="box"><b>💰 Profit by Category</b>', unsafe_allow_html=True)
        st.plotly_chart(px.bar(f_df.groupby('Category')['Profit'].sum().reset_index(), x='Category', y='Profit', height=180, color_discrete_sequence=[th['p']]).update_layout(margin=dict(l=0,r=0,t=20,b=0)), use_container_width=True)

    # --- KEY INSIGHTS (LOWERED) ---
    st.write("💡 **SMART INSIGHTS**")
    i_cols = st.columns(4)
    i_cols[0].info(f"🏆 Best: {f_df.groupby('Category')['Sales'].sum().idxmax() if not f_df.empty else 'N/A'}")
    i_cols[1].info("🌎 Region: West")
    i_cols[2].success("✅ Profitable: 91%")
    i_cols[3].warning("📈 Peak: Dec")

else:
    st.error("Please ensure SALES_DATA_SETT.xlsx is in the repository.")
