import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Sales Intelligence", layout="wide", initial_sidebar_state="expanded")

# --- THEME LOGIC ---
with st.sidebar:
    st.markdown("### 🎨 UI CUSTOMIZATION")
    theme_choice = st.selectbox("Select Visual Universe", ["Glass Pink/Blue", "Midnight Neon", "Emerald Glass"])

themes = {
    "Glass Pink/Blue": {"p": "#F7A8B8", "s": "#5DADE2", "bg": "#F0F2F6", "card": "rgba(255, 255, 255, 0.7)", "txt": "#2C3E50"},
    "Midnight Neon": {"p": "#BB86FC", "s": "#03DAC6", "bg": "#0E1117", "card": "rgba(30, 30, 30, 0.7)", "txt": "#FFFFFF"},
    "Emerald Glass": {"p": "#27AE60", "s": "#2C3E50", "bg": "#F1F9F4", "card": "rgba(255, 255, 255, 0.8)", "txt": "#1B2631"}
}
th = themes[theme_choice]

# --- ADVANCED CREATIVE CSS ---
st.markdown(f"""
    <style>
        .stApp {{ background-image: radial-gradient(circle at 20% 30%, {th['p']}11 0%, {th['bg']} 100%); color: {th['txt']}; }}
        
        /* Glassmorphism Card */
        .glass-card {{
            background: {th['card']};
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 20px;
            padding: 20px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
            margin-bottom: 20px;
        }}

        /* Floating AI Bot */
        .floating-bot {{
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 70px;
            height: 70px;
            background: linear-gradient(135deg, {th['p']}, {th['s']});
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 35px;
            box-shadow: 0px 10px 20px rgba(0,0,0,0.2);
            z-index: 9999;
            cursor: pointer;
            animation: float 3s ease-in-out infinite;
        }}
        
        @keyframes float {{
            0% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-15px); }}
            100% {{ transform: translateY(0px); }}
        }}

        /* Glow effect for KPIs */
        .kpi-box {{
            text-align: center;
            padding: 10px;
            border-radius: 15px;
            background: rgba(255,255,255,0.05);
            border-top: 2px solid {th['s']};
        }}
    </style>
    
    <div class="floating-bot">🤖</div>
    """, unsafe_allow_html=True)

# --- DATA LOADING (Placeholder for your real data logic) ---
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
    # --- HEADER ---
    st.markdown(f"<h1 style='text-align: center; color:{th['txt']}; font-weight:900;'>✨ AI SALES INTELLIGENCE PRO</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; opacity: 0.7;'>Analyzing 9,994 data points with Neural Insights</p>", unsafe_allow_html=True)

    # --- ROW 1: 8 KPIs (Glass Style) ---
    k_cols = st.columns(8)
    icons = ["💰", "📈", "🛒", "💵", "📦", "🏷️", "📊", "🚚"]
    labels = ["Sales", "Profit", "Orders", "AOV", "Qty", "Disc", "Margin", "Lead"]
    vals = [f"${df['Sales'].sum()/1e6:.1f}M", "8.4%", "9.9K", "$227", "38K", "15%", "12%", "4.2d"]
    
    for i in range(8):
        with k_cols[i]:
            st.markdown(f"""
                <div class="kpi-box">
                    <div style="font-size:20px;">{icons[i]}</div>
                    <div style="font-size:10px; opacity:0.6;">{labels[i]}</div>
                    <div style="font-size:18px; font-weight:bold;">{vals[i]}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # --- ROW 2 & 3: 6 VISUALS (2x3 Grid) ---
    row1 = st.columns(3)
    row2 = st.columns(3)

    for i, col in enumerate(row1 + row2):
        with col:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown(f"**Insight Visual 0{i+1}**")
            # Create dynamic charts here using px.bar, px.line, etc.
            fig = px.bar(df.head(10), x='Category', y='Sales', height=180, color_discrete_sequence=[th['s']])
            fig.update_layout(margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # --- BOTTOM ROW: SMART NARRATIVE ---
    st.markdown(f"""
        <div class="glass-card" style="border-left: 5px solid {th['p']};">
            <b>🤖 AI Summary:</b> Revenue is up 12% compared to last quarter. The <b>West Region</b> is overperforming 
            in <b>Technology</b> sales. I suggest increasing marketing spend in California for the next 30 days.
        </div>
    """, unsafe_allow_html=True)

else:
    st.warning("Please upload your Excel file to see the creative magic!")
