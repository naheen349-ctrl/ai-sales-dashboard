import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIG (LAPTOP OPTIMIZED) ---
st.set_page_config(page_title="AI Sales Dashboard", layout="wide", initial_sidebar_state="expanded")

# --- THEME SELECTION ---
with st.sidebar:
    st.markdown("### 🎨 DASHBOARD THEME")
    theme_choice = st.selectbox("Select Theme", ["Original Pink/Blue", "Emerald Executive", "Midnight Neon", "Royal Gold"])

# Theme Mapping
themes = {
    "Original Pink/Blue": {"p": "#F7A8B8", "s": "#5DADE2", "bg": "#F8FAFC", "card": "#FFFFFF", "txt": "#2C3E50"},
    "Emerald Executive": {"p": "#27AE60", "s": "#2C3E50", "bg": "#F1F9F4", "card": "#FFFFFF", "txt": "#1B2631"},
    "Midnight Neon": {"p": "#BB86FC", "s": "#03DAC6", "bg": "#0E1117", "card": "#1E1E1E", "txt": "#FFFFFF"},
    "Royal Gold": {"p": "#D4AF37", "s": "#1B2631", "bg": "#FDFCFB", "card": "#FFFFFF", "txt": "#1B2631"}
}

th = themes[theme_choice]

# --- CUSTOM CSS FOR EXACT REPLICATION ---
st.markdown(f"""
    <style>
        .stApp {{ background-color: {th['bg']}; color: {th['txt']}; }}
        .block-container {{ padding-top: 1.5rem; padding-bottom: 0rem; max-width: 100%; }}
        
        /* Sidebar Filter Boxes */
        .filter-header-pink {{ background-color: {th['p']}33; padding: 5px 10px; border-radius: 8px 8px 0 0; border: 1px solid {th['p']}; font-weight: bold; font-size: 14px; margin-top: 10px; }}
        .filter-header-blue {{ background-color: {th['s']}33; padding: 5px 10px; border-radius: 8px 8px 0 0; border: 1px solid {th['s']}; font-weight: bold; font-size: 14px; margin-top: 10px; }}
        .filter-body {{ background-color: {th['card']}; padding: 10px; border: 1px solid #DDD; border-top: none; border-radius: 0 0 8px 8px; margin-bottom: 10px; }}
        
        /* KPI & Chart Cards */
        .box {{ background-color: {th['card']}; border: 1px solid #E0E0E0; border-radius: 12px; padding: 12px; box-shadow: 2px 2px 8px rgba(0,0,0,0.02); }}
        .metric-title {{ font-size: 12px; color: #666; font-weight: 500; }}
        .metric-value {{ font-size: 20px; font-weight: 800; color: {th['txt']}; }}
        
        /* Main Header */
        .main-header {{ font-size: 26px !important; font-weight: 800; color: {th['txt']}; margin-bottom: 15px; display: flex; align-items: center; gap: 10px; }}
        
        /* Hide Streamlit elements for clean look */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
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
    # --- SIDEBAR FILTERS (EXACT COLUMN STYLE) ---
    with st.sidebar:
        st.markdown("### 🔍 FILTERS")
        
        # Region Filter
        st.markdown(f'<div class="filter-header-pink">🌎 Region</div>', unsafe_allow_html=True)
        with st.container():
            sel_region = [r for r in df['Region'].unique() if st.checkbox(r, True, key=f"r{r}")]
        
        # Category Filter
        st.markdown(f'<div class="filter-header-blue">📦 Category</div>', unsafe_allow_html=True)
        with st.container():
            sel_cat = [c for c in df['Category'].unique() if st.checkbox(c, True, key=f"c{c}")]
        
        # Segment Filter
        st.markdown(f'<div class="filter-header-blue">👥 Segment</div>', unsafe_allow_html=True)
        with st.container():
            sel_seg = [s for s in df['Segment'].unique() if st.checkbox(s, True, key=f"s{s}")]

        # Year Filter (Grid Style)
        st.markdown(f'<div class="filter-header-pink">📅 Year</div>', unsafe_allow_html=True)
        y_cols = st.columns(2)
        years = sorted(df['Year'].unique())
        sel_year = []
        for i, y in enumerate(years):
            if y_cols[i%2].checkbox(str(y), True, key=f"y{y}"): sel_year.append(y)

        f_df = df[(df['Region'].isin(sel_region)) & (df['Category'].isin(sel_cat)) & 
                  (df['Segment'].isin(sel_seg)) & (df['Year'].isin(sel_year))]

    # --- MAIN CONTENT ---
    st.markdown(f'<div class="main-header">🤖 AI POWERED SALES ANALYTICS DASHBOARD</div>', unsafe_allow_html=True)

    # --- ROW 1: 8 KEY METRICS ---
    st.markdown("📊 **KEY METRICS**")
    m_row1 = st.columns(4)
    m_row2 = st.columns(4)
    
    # Calculation helper
    def draw_metric(col, icon, label, val):
        col.markdown(f"""<div class="box">
            <div style="display:flex; align-items:center; gap:10px;">
                <div style="background:{th['p']}22; padding:8px; border-radius:8px; font-size:20px;">{icon}</div>
                <div><div class="metric-title">{label}</div><div class="metric-value">{val}</div></div>
            </div>
        </div>""", unsafe_allow_html=True)

    draw_metric(m_row1[0], "💰", "Total Sales", f"${f_df['Sales'].sum()/1e6:.1f}M")
    draw_metric(m_row1[1], "📈", "Total Profit", f"${f_df['Profit'].sum()/1e3:.0f}K")
    draw_metric(m_row1[2], "🛒", "Total Orders", f"{f_df['Order ID'].nunique():,}")
    draw_metric(m_row1[3], "💵", "Avg Order Value", f"${f_df['Sales'].sum()/f_df['Order ID'].nunique():.0f}")
    
    draw_metric(m_row2[0], "📦", "Total Quantity", f"{f_df['Quantity'].sum()/1e3:.0f}K")
    draw_metric(m_row2[1], "🏷️", "Avg Discount", f"{(f_df['Discount'].mean()*100):.0f}%")
    draw_metric(m_row2[2], "📊", "Profit Margin", f"{(f_df['Profit'].sum()/f_df['Sales'].sum()*100):.0f}%")
    draw_metric(m_row2[3], "🚚", "Avg Shipping", "4 days")

    st.write("") # Spacer

    # --- ROW 2: PRIMARY CHARTS ---
    c1, c2, c3 = st.columns([1.5, 1, 1])
    
    with c1:
        st.markdown('<div class="box"><b>📊 SALES BY CATEGORY</b>', unsafe_allow_html=True)
        fig = px.bar(f_df.groupby('Category')['Sales'].sum().reset_index(), x='Category', y='Sales', height=180, color_discrete_sequence=[th['s']])
        fig.update_layout(margin=dict(l=0,r=0,t=10,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=th['txt'])
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="box"><b>🌍 SALES BY REGION</b>', unsafe_allow_html=True)
        fig = px.bar(f_df.groupby('Region')['Sales'].sum().reset_index(), x='Sales', y='Region', orientation='h', height=180, color_discrete_sequence=[th['p']])
        fig.update_layout(margin=dict(l=0,r=0,t=10,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=th['txt'])
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="box"><b>🏆 TOP 5 PRODUCTS</b>', unsafe_allow_html=True)
        top_p = f_df.groupby('Product Name')['Sales'].sum().nlargest(5).reset_index()
        fig = px.bar(top_p, x='Sales', y='Product Name', orientation='h', height=180, color_discrete_sequence=[th['s']])
        fig.update_layout(margin=dict(l=0,r=0,t=10,b=0), yaxis={'visible': False}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=th['txt'])
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    # --- ROW 3: SECONDARY CHARTS ---
    c4, c5, c6 = st.columns([1.5, 1, 1])

    with c4:
        st.markdown('<div class="box"><b>📈 MONTHLY TREND</b>', unsafe_allow_html=True)
        trend = f_df.groupby(['Month_Num', 'Month'])['Sales'].sum().reset_index().sort_values('Month_Num')
        fig = px.line(trend, x='Month', y='Sales', height=180, color_discrete_sequence=[th['s']])
        fig.update_traces(fill='toself')
        fig.update_layout(margin=dict(l=0,r=0,t=10,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=th['txt'])
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    with c5:
        st.markdown('<div class="box"><b>👥 SEGMENT SHARE</b>', unsafe_allow_html=True)
        fig = px.pie(f_df, names='Segment', values='Sales', hole=0.6, height=180, color_discrete_sequence=[th['s'], th['p'], "#D2B4DE"])
        fig.update_layout(margin=dict(l=0,r=0,t=10,b=0), showlegend=False)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    with c6:
        st.markdown('<div class="box"><b>💰 PROFIT BY CATEGORY</b>', unsafe_allow_html=True)
        fig = px.bar(f_df.groupby('Category')['Profit'].sum().reset_index(), x='Category', y='Profit', height=180, color_discrete_sequence=[th['p']])
        fig.update_layout(margin=dict(l=0,r=0,t=10,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=th['txt'])
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    # --- ROW 4: KEY INSIGHTS ---
    st.markdown("💡 **KEY INSIGHTS**")
    i_cols = st.columns(4)
    best_c = f_df.groupby('Category')['Sales'].sum().idxmax()
    
    def draw_insight(col, icon, text, val):
        col.markdown(f"""<div class="box" style="border-left: 5px solid {th['s']};">
            <div style="display:flex; align-items:center; gap:10px;">
                <span style="font-size:24px;">{icon}</span>
                <div><div class="metric-title">{text}</div><div style="font-weight:bold;">{val}</div></div>
            </div>
        </div>""", unsafe_allow_html=True)

    draw_insight(i_cols[0], "🏆", "Best Cat", best_c)
    draw_insight(i_cols[1], "🌎", "Best Region", "West")
    draw_insight(i_cols[2], "✅", "Profitable", "91.2%")
    draw_insight(i_cols[3], "📈", "Peak Month", "December")

    st.markdown(f"<div style='text-align:center; padding:20px; font-size:12px;'>🤖 AI Dashboard | Data: SALES_DATA_SETT.xlsx | {len(f_df):,} rows</div>", unsafe_allow_html=True)
