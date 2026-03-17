import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# --- HELPER FUNCTIONS ---
def adjust_color(color, amount):
    """Helper function to adjust color brightness for gradients"""
    if color.startswith('#'):
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(min(255, max(0, c + amount)) for c in rgb)
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
    return color

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AI Sales Intelligence Pro", 
    layout="wide", 
    initial_sidebar_state="expanded",
    page_icon="🚀"
)

# --- THEME DICTIONARY (EXPANDED CREATIVE OPTIONS) ---
themes = {
    "Cyber Fusion": {"p": "#FF007A", "s": "#00E5FF", "bg": "#050505", "card": "rgba(15, 15, 25, 0.92)", "txt": "#FFFFFF", "grid": "#222222"},
    "Tokyo Night": {"p": "#7AA2F7", "s": "#BB9AF7", "bg": "#1A1B26", "card": "rgba(36, 40, 59, 0.95)", "txt": "#C0CAF5", "grid": "#292E42"},
    "Luxury Gold": {"p": "#D4AF37", "s": "#856404", "bg": "#121212", "card": "rgba(30, 30, 30, 0.98)", "txt": "#F5F5F5", "grid": "#333333"},
    "Nordic Frost": {"p": "#88C0D0", "s": "#5E81AC", "bg": "#2E3440", "card": "rgba(59, 66, 82, 0.95)", "txt": "#ECEFF4", "grid": "#4C566A"},
    "Midnight Neon": {"p": "#BB86FC", "s": "#03DAC6", "bg": "#0E1117", "card": "rgba(20, 20, 20, 0.95)", "txt": "#FFFFFF", "grid": "#333333"},
    "Solaris": {"p": "#FF4E50", "s": "#FC913A", "bg": "#F9F7E8", "card": "rgba(255, 255, 255, 0.98)", "txt": "#2C3E50", "grid": "#E1E1E1"},
    "Retro Wave": {"p": "#F92672", "s": "#66D9EF", "bg": "#272822", "card": "rgba(35, 36, 31, 0.95)", "txt": "#F8F8F2", "grid": "#49483E"}
}

with st.sidebar:
    st.markdown(f"## 🎨 THEME ENGINE")
    theme_choice = st.selectbox("Select Visual Identity", list(themes.keys()))
    enable_forecast = st.checkbox("Enable AI Forecasting", True)
    
th = themes[theme_choice]

# --- DYNAMIC CSS INJECTION ---
st.markdown(f"""
    <style>
        @keyframes glow {{
            0% {{ box-shadow: 0 0 5px {th['p']}20; }}
            50% {{ box-shadow: 0 0 20px {th['p']}50; }}
            100% {{ box-shadow: 0 0 5px {th['p']}20; }}
        }}

        .stApp {{ 
            background: radial-gradient(circle at top right, {adjust_color(th['bg'], 15)}, {th['bg']});
            color: {th['txt']}; 
        }}

        .main-title {{
            font-size: 50px !important;
            font-weight: 900 !important;
            background: linear-gradient(to right, {th['p']}, {th['s']});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            letter-spacing: -2px;
            margin-top: -40px;
        }}

        .glass-container {{
            background: {th['card']};
            backdrop-filter: blur(15px);
            border-radius: 20px;
            padding: 20px;
            border: 1px solid {th['p']}40;
            transition: all 0.3s ease;
            margin-bottom: 20px;
        }}

        .glass-container:hover {{
            border: 1px solid {th['p']};
            transform: translateY(-3px);
            animation: glow 2s infinite ease-in-out;
        }}

        .kpi-box {{
            text-align: center;
            padding: 15px;
            background: {th['card']};
            border-radius: 15px;
            border-bottom: 4px solid {th['p']};
        }}
        
        .kpi-val {{ font-size: 26px; font-weight: 900; color: {th['p']}; }}
        .kpi-lab {{ font-size: 11px; text-transform: uppercase; letter-spacing: 1px; opacity: 0.7; }}

        [data-testid="stSidebar"] {{ background: {th['bg']} !important; border-right: 1px solid {th['p']}30; }}
    </style>
""", unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("SALES_DATA_SETT.xlsx")
        df['Order Date'] = pd.to_datetime(df['Order Date'])
        df['Month'] = df['Order Date'].dt.strftime('%b')
        df['Month_Num'] = df['Order Date'].dt.month
        return df
    except: return pd.DataFrame()

df = load_data()

if not df.empty:
    # --- FILTERS ---
    with st.sidebar:
        st.markdown("---")
        sel_region = st.multiselect("Region", df['Region'].unique(), default=df['Region'].unique())
        sel_cat = st.multiselect("Category", df['Category'].unique(), default=df['Category'].unique())
        f_df = df[(df['Region'].isin(sel_region)) & (df['Category'].isin(sel_cat))]

    # --- HEADER ---
    st.markdown(f'<div class="main-title">{theme_choice.upper()} INTELLIGENCE</div>', unsafe_allow_html=True)

    # --- KPI ROW ---
    k_cols = st.columns(6)
    metrics = [
        ("REVENUE", f"${f_df['Sales'].sum()/1e6:.1f}M"),
        ("PROFIT", f"${f_df['Profit'].sum()/1e3:.1f}K"),
        ("ORDERS", f"{f_df['Order ID'].nunique():,}"),
        ("MARGIN", f"{(f_df['Profit'].sum()/f_df['Sales'].sum()*100):.1f}%"),
        ("UNITS", f"{f_df['Quantity'].sum():,}"),
        ("DISCOUNT", f"{(f_df['Discount'].mean()*100):.1f}%")
    ]
    for i, (label, val) in enumerate(metrics):
        k_cols[i].markdown(f'<div class="kpi-box"><div class="kpi-lab">{label}</div><div class="kpi-val">{val}</div></div>', unsafe_allow_html=True)

    st.write("")

    # --- CHARTS GRID ---
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.markdown('<div class="glass-container"><b>📈 PERFORMANCE TREND LINE</b>', unsafe_allow_html=True)
        trend_data = f_df.groupby('Month_Num')['Sales'].sum().reset_index()
        fig = px.area(trend_data, x='Month_Num', y='Sales', color_discrete_sequence=[th['p']])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=th['txt'], height=350)
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(gridcolor=th['grid'])
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="glass-container"><b>🎯 SEGMENT SHARE</b>', unsafe_allow_html=True)
        fig = px.pie(f_df, names='Segment', values='Sales', hole=0.6, color_discrete_sequence=[th['p'], th['s'], "#888888"])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', showlegend=False, height=350)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    c3, c4, c5 = st.columns(3)

    with c3:
        st.markdown('<div class="glass-container"><b>🏆 TOP REGIONS</b>', unsafe_allow_html=True)
        reg_data = f_df.groupby('Region')['Sales'].sum().reset_index()
        fig = px.bar(reg_data, x='Region', y='Sales', color_discrete_sequence=[th['s']])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=th['txt'], height=250)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c4:
        st.markdown('<div class="glass-container"><b>📦 CATEGORY HEAT</b>', unsafe_allow_html=True)
        fig = px.treemap(f_df, path=['Category', 'Sub-Category'], values='Sales', color_discrete_sequence=[th['p'], th['s']])
        fig.update_layout(margin=dict(t=0, l=0, r=0, b=0), height=250)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c5:
        st.markdown('<div class="glass-container"><b>🔬 PROFIT ANALYSIS</b>', unsafe_allow_html=True)
        fig = px.scatter(f_df.sample(min(len(f_df), 500)), x='Sales', y='Profit', color='Category', color_discrete_sequence=[th['p'], th['s'], "#FFFFFF"])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=th['txt'], height=250, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.error("Please place SALES_DATA_SETT.xlsx in the same folder as this script.")
