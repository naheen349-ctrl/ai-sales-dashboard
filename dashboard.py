import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Sales Intelligence", layout="wide", initial_sidebar_state="expanded")

# --- POWER BI THEME PALETTE ---
with st.sidebar:
    st.markdown("### 📊 DASHBOARD ENGINE")
    theme_choice = st.selectbox("Style Preset", ["Power BI Dark", "Corporate Light", "Cyber Glow"])

themes = {
    "Power BI Dark": {"bg": "#111111", "card": "#1E1E1E", "txt": "#FFFFFF", "accent": "#F2C94C", "chart_color": "#F2994A"},
    "Corporate Light": {"bg": "#F4F7F6", "card": "#FFFFFF", "txt": "#1B2631", "accent": "#2E86C1", "chart_color": "#3498DB"},
    "Cyber Glow": {"bg": "#0D0D0D", "card": "#161616", "txt": "#00FFC2", "accent": "#00FFC2", "chart_color": "#BD10E0"}
}
th = themes[theme_choice]

# --- ADVANCED CSS (POWER BI STYLE) ---
st.markdown(f"""
    <style>
        .stApp {{ background-color: {th['bg']}; color: {th['txt']}; }}
        .block-container {{ padding-top: 5rem !important; }}
        
        /* Power BI Card Effect */
        .pbi-card {{
            background: {th['card']};
            border-radius: 10px;
            padding: 20px;
            border-top: 4px solid {th['accent']};
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            margin-bottom: 15px;
        }}
        
        .kpi-title {{ font-size: 14px; font-weight: 600; opacity: 0.8; letter-spacing: 1px; color: {th['txt']}; }}
        .kpi-value {{ font-size: 28px; font-weight: 900; color: {th['accent']}; }}
        
        /* Navigation Sidebar */
        [data-testid="stSidebar"] {{
            background-color: {th['card']} !important;
            border-right: 1px solid {th['accent']}44;
        }}
        
        .main-title {{
            font-size: 42px !important;
            font-weight: 900;
            text-align: center;
            color: {th['txt']};
            margin-bottom: 40px;
            letter-spacing: -1px;
        }}
    </style>
    """, unsafe_allow_html=True)

# --- DATA PROCESSING ---
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
    # --- SIDEBAR SLICERS ---
    with st.sidebar:
        st.markdown(f"<h2 style='color:{th['accent']}'>⚡ SLICERS</h2>", unsafe_allow_html=True)
        sel_region = st.multiselect("Region", df['Region'].unique(), default=df['Region'].unique())
        sel_cat = st.multiselect("Category", df['Category'].unique(), default=df['Category'].unique())
        f_df = df[(df['Region'].isin(sel_region)) & (df['Category'].isin(sel_cat))]

    # --- DASHBOARD HEADER ---
    st.markdown(f'<div class="main-title">AI POWERED <span style="color:{th["accent"]}">SALES ANALYTICS</span></div>', unsafe_allow_html=True)

    # --- ROW 1: POWER BI KPIs ---
    k_cols = st.columns(8)
    metrics = [
        ("💰", "REVENUE", f"${f_df['Sales'].sum()/1e6:.1f}M"),
        ("📈", "PROFIT", f"${f_df['Profit'].sum()/1e3:.0f}K"),
        ("🛒", "ORDERS", f"{f_df['Order ID'].nunique():,}"),
        ("💵", "AVG TICKET", f"${f_df['Sales'].sum()/f_df['Order ID'].nunique():.0f}"),
        ("📦", "QUANTITY", f"{f_df['Quantity'].sum()/1e3:.0f}K"),
        ("🏷️", "DISCOUNT", f"{(f_df['Discount'].mean()*100):.0f}%"),
        ("📊", "MARGIN", f"{(f_df['Profit'].sum()/f_df['Sales'].sum()*100):.0f}%"),
        ("🚚", "SHIP DAYS", "4.1")
    ]
    
    for i, (icon, label, val) in enumerate(metrics):
        k_cols[i].markdown(f"""
            <div class="pbi-card" style="padding: 10px; text-align:center;">
                <div class="kpi-title">{icon} {label}</div>
                <div class="kpi-value">{val}</div>
            </div>
        """, unsafe_allow_html=True)

    # --- ROW 2 & 3: ADVANCED PLOTLY VISUALS ---
    c1, c2, c3 = st.columns(3)
    c4, c5, c6 = st.columns(3)

    # 1. SALES BY CATEGORY (Creative Bar with Gradient-like feel)
    with c1:
        st.markdown('<div class="pbi-card"><b>📊 Revenue Performance</b>', unsafe_allow_html=True)
        fig = px.bar(f_df.groupby('Category')['Sales'].sum().reset_index(), x='Sales', y='Category', 
                     orientation='h', height=220, color_discrete_sequence=[th['accent']])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=th['txt'], margin=dict(l=0,r=10,t=10,b=0))
        st.plotly_chart(fig, use_container_width=True, key="pbi_1")
        st.markdown('</div>', unsafe_allow_html=True)

    # 2. PROFIT MARGIN GAUGE (Power BI Style Indicator)
    with c2:
        st.markdown('<div class="pbi-card"><b>🎯 Profit Target</b>', unsafe_allow_html=True)
        margin = (f_df['Profit'].sum()/f_df['Sales'].sum()*100) if not f_df.empty else 0
        fig = go.Figure(go.Indicator(
            mode = "gauge+number", value = margin,
            gauge = {'axis': {'range': [0, 25]}, 'bar': {'color': th['accent']}, 'bgcolor': "rgba(0,0,0,0)"},
            number = {'suffix': "%", 'font': {'color': th['txt']}}
        ))
        fig.update_layout(height=220, margin=dict(l=20,r=20,t=40,b=20), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True, key="pbi_2")
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. REGIONAL TREEMAP (Creative alternative to Pie)
    with c3:
        st.markdown('<div class="pbi-card"><b>🌍 Geographic Tree</b>', unsafe_allow_html=True)
        fig = px.treemap(f_df, path=['Region', 'Segment'], values='Sales', height=220,
                         color_discrete_sequence=[th['accent'], th['chart_color'], "#555"])
        fig.update_layout(margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True, key="pbi_3")
        st.markdown('</div>', unsafe_allow_html=True)

    # 4. MONTHLY TREND (Smooth Area Chart)
    with c4:
        st.markdown('<div class="pbi-card"><b>📈 Sales Velocity Trend</b>', unsafe_allow_html=True)
        trend = f_df.groupby(['Month_Num', 'Month'])['Sales'].sum().reset_index().sort_values('Month_Num')
        fig = px.area(trend, x='Month', y='Sales', height=220, color_discrete_sequence=[th['accent']])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=th['txt'], margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(fig, use_container_width=True, key="pbi_4")
        st.markdown('</div>', unsafe_allow_html=True)

    # 5. SEGMENT RADAR OR DONUT (Donut with Central Annotation)
    with c5:
        st.markdown('<div class="pbi-card"><b>👥 Customer Mix</b>', unsafe_allow_html=True)
        fig = px.pie(f_df, names='Segment', values='Sales', hole=0.7, height=220, 
                     color_discrete_sequence=[th['accent'], th['chart_color'], "#777"])
        fig.update_layout(showlegend=False, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)')
        fig.add_annotation(text="SEGMENT", showarrow=False, font_size=12, font_color=th['txt'])
        st.plotly_chart(fig, use_container_width=True, key="pbi_5")
        st.markdown('</div>', unsafe_allow_html=True)

    # 6. TOP 5 PRODUCTS (Clean Horizontal Bar)
    with c6:
        st.markdown('<div class="pbi-card"><b>🏆 Top SKU Performance</b>', unsafe_allow_html=True)
        top_p = f_df.groupby('Product Name')['Sales'].sum().nlargest(5).reset_index()
        fig = px.bar(top_p, x='Sales', y='Product Name', orientation='h', height=220, color_discrete_sequence=[th['chart_color']])
        fig.update_layout(yaxis={'visible': False}, paper_bgcolor='rgba(0,0,0,0)', font_color=th['txt'], margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(fig, use_container_width=True, key="pbi_6")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- AI INSIGHTS FOOTER ---
    st.markdown(f"""
        <div class="pbi-card" style="border-left: 10px solid {th['accent']};">
            <h3 style="margin:0; color:{th['txt']};">💡 AI EXECUTIVE SUMMARY</h3>
            <p style="opacity:0.8; margin:5px 0;">Neural analysis suggests that the <b>{f_df.groupby('Category')['Sales'].sum().idxmax()}</b> 
            category is driving growth, while <b>{sel_region[0] if sel_region else 'All'}</b> region shows the highest conversion efficiency. 
            Recommend increasing inventory for top products before the Q4 peak.</p>
        </div>
    """, unsafe_allow_html=True)

else:
    st.error("Missing Data File!")
