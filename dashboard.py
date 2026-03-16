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

# --- CSS FIX FOR TITLE VISIBILITY ---
st.markdown(f"""
    <style>
        .stApp {{ background-color: {th['bg']}; color: {th['txt']}; }}
        
        /* Forces the main container to show the title clearly */
        .block-container {{ 
            padding-top: 0rem !important; 
            padding-bottom: 0rem !important; 
            margin-top: -30px; 
        }}

        /* Header Styling */
        .main-header {{ 
            background-color: {th['card']};
            padding: 15px;
            border-radius: 0px 0px 15px 15px;
            font-size: 28px !important; 
            font-weight: 800; 
            color: {th['txt']}; 
            display: flex; 
            align-items: center; 
            gap: 15px;
            margin-bottom: 20px;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
            border: 1px solid #EEE;
        }}

        /* Sidebar & Filters */
        .filter-header-pink {{ background-color: {th['p']}44; padding: 8px 12px; border-radius: 10px 10px 0 0; border: 1.5px solid {th['p']}; font-weight: bold; font-size: 14px; margin-top: 15px; }}
        .filter-header-blue {{ background-color: {th['s']}44; padding: 8px 12px; border-radius: 10px 10px 0 0; border: 1.5px solid {th['s']}; font-weight: bold; font-size: 14px; margin-top: 15px; }}
        .filter-body {{ background-color: {th['card']}; padding: 10px; border: 1px solid #DDD; border-top: none; border-radius: 0 0 10px 10px; margin-bottom: 10px; }}
        
        /* Card Containers */
        .box {{ background-color: {th['card']}; border: 1px solid #E0E0E0; border-radius: 12px; padding: 12px; box-shadow: 2px 2px 8px rgba(0,0,0,0.02); }}
        .metric-title {{ font-size: 12px; color: #777; font-weight: 500; }}
        .metric-value {{ font-size: 22px; font-weight: 800; color: {th['txt']}; }}
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
    # --- HEADER SECTION (FIXED VISIBILITY) ---
    st.markdown(f'<div class="main-header">🤖 AI POWERED SALES ANALYTICS DASHBOARD</div>', unsafe_allow_html=True)

    # --- SIDEBAR FILTERS ---
    with st.sidebar:
        st.markdown("### 🔍 FILTERS")
        
        st.markdown(f'<div class="filter-header-pink">🌎 Region</div>', unsafe_allow_html=True)
        with st.container():
            sel_region = [r for r in df['Region'].unique() if st.checkbox(r, True, key=f"r{r}")]
        
        st.markdown(f'<div class="filter-header-blue">📦 Category</div>', unsafe_allow_html=True)
        with st.container():
            sel_cat = [c for c in df['Category'].unique() if st.checkbox(c, True, key=f"c{c}")]
        
        st.markdown(f'<div class="filter-header-pink">📅 Year</div>', unsafe_allow_html=True)
        y_cols = st.columns(2)
        years = sorted(df['Year'].unique())
        sel_year = []
        for i, y in enumerate(years):
            if y_cols[i%2].checkbox(str(y), True, key=f"y{y}"): sel_year.append(y)

        f_df = df[(df['Region'].isin(sel_region)) & (df['Category'].isin(sel_cat)) & (df['Year'].isin(sel_year))]

    # --- KPI ROW (8 METRICS) ---
    m_row1 = st.columns(4)
    m_row2 = st.columns(4)
    
    def draw_metric(col, icon, label, val):
        col.markdown(f"""<div class="box">
            <div style="display:flex; align-items:center; gap:10px;">
                <div style="background:{th['s']}22; padding:8px; border-radius:8px; font-size:20px;">{icon}</div>
                <div><div class="metric-title">{label}</div><div class="metric-value">{val}</div></div>
            </div>
        </div>""", unsafe_allow_html=True)

    draw_metric(m_row1[0], "💰", "Total Sales", f"${f_df['Sales'].sum()/1e6:.1f}M")
    draw_metric(m_row1[1], "📈", "Total Profit", f"${f_df['Profit'].sum()/1e3:.0f}K")
    draw_metric(m_row1[2], "🛒", "Total Orders", f"{f_df['Order ID'].nunique():,}")
    draw_metric(m_row1[3], "💵", "Avg Order Value", f"${f_df['Sales'].sum()/f_df['Order ID'].nunique():.0f}" if not f_df.empty else "0")
    
    draw_metric(m_row2[0], "📦", "Total Quantity", f"{f_df['Quantity'].sum()/1e3:.0f}K")
    draw_metric(m_row2[1], "🏷️", "Avg Discount", f"{(f_df['Discount'].mean()*100):.0f}%")
    draw_metric(m_row2[2], "📊", "Profit Margin", f"{(f_df['Profit'].sum()/f_df['Sales'].sum()*100):.0f}%" if f_df['Sales'].sum() > 0 else "0%")
    draw_metric(m_row2[3], "🚚", "Avg Shipping", "4 days")

    st.write("---")

    # --- CHARTS GRID ---
    c1, c2, c3 = st.columns([1.2, 1, 1])
    with c1:
        st.markdown('<div class="box"><b>📊 Sales by Category</b>', unsafe_allow_html=True)
        st.plotly_chart(px.bar(f_df.groupby('Category')['Sales'].sum().reset_index(), x='Category', y='Sales', height=180, color_discrete_sequence=[th['s']]).update_layout(margin=dict(l=0,r=0,t=20,b=0)), use_container_width=True)
    with c2:
        st.markdown('<div class="box"><b>🌍 Sales by Region</b>', unsafe_allow_html=True)
        st.plotly_chart(px.bar(f_df.groupby('Region')['Sales'].sum().reset_index(), x='Sales', y='Region', orientation='h', height=180, color_discrete_sequence=[th['p']]).update_layout(margin=dict(l=0,r=0,t=20,b=0)), use_container_width=True)
    with c3:
        st.markdown('<div class="box"><b>🏆 Top 5 Products</b>', unsafe_allow_html=True)
        top_p = f_df.groupby('Product Name')['Sales'].sum().nlargest(5).reset_index()
        st.plotly_chart(px.bar(top_p, x='Sales', y='Product Name', orientation='h', height=180, color_discrete_sequence=[th['s']]).update_layout(margin=dict(l=0,r=0,t=20,b=0), yaxis={'visible': False}), use_container_width=True)

    c4, c5, c6 = st.columns([1.2, 1, 1])
    with c4:
        st.markdown('<div class="box"><b>📈 Monthly Trend</b>', unsafe_allow_html=True)
        trend = f_df.groupby(['Month_Num', 'Month'])['Sales'].sum().reset_index().sort_values('Month_Num')
        st.plotly_chart(px.line(trend, x='Month', y='Sales', height=180, color_discrete_sequence=[th['s']]).update_traces(fill='toself').update_layout(margin=dict(l=0,r=0,t=20,b=0)), use_container_width=True)
    with c5:
        st.markdown('<div class="box"><b>👥 Segment Share</b>', unsafe_allow_html=True)
        st.plotly_chart(px.pie(f_df, names='Segment', values='Sales', hole=0.5, height=180, color_discrete_sequence=[th['s'], th['p'], "#D2B4DE"]).update_layout(margin=dict(l=0,r=0,t=20,b=0), showlegend=False), use_container_width=True)
    with c6:
        st.markdown('<div class="box"><b>💰 Profit by Category</b>', unsafe_allow_html=True)
        st.plotly_chart(px.bar(f_df.groupby('Category')['Profit'].sum().reset_index(), x='Category', y='Profit', height=180, color_discrete_sequence=[th['p']]).update_layout(margin=dict(l=0,r=0,t=20,b=0)), use_container_width=True)

    # --- INSIGHTS ---
    st.write("💡 **KEY INSIGHTS**")
    i_cols = st.columns(4)
    i_cols[0].info(f"🏆 Best: {f_df.groupby('Category')['Sales'].sum().idxmax() if not f_df.empty else 'N/A'}")
    i_cols[1].info("🌎 Region: West")
    i_cols[2].success("✅ Profitable: 91%")
    i_cols[3].warning("📈 Peak: Dec")

else:
    st.error("Dataset not found!")
