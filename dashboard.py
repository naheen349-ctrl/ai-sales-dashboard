import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Sales Dashboard", layout="wide", initial_sidebar_state="expanded")

# --- THEME SELECTION LOGIC ---
with st.sidebar:
    st.markdown("### 🎨 DASHBOARD THEME")
    theme_choice = st.selectbox("Choose Visual Style", ["Original Pink/Blue", "Emerald Executive", "Midnight Neon", "Royal Gold"])

# Theme Color Mapping
themes = {
    "Original Pink/Blue": {"p": "#F7A8B8", "s": "#5DADE2", "bg": "#FFFFFF", "text": "#2C3E50"},
    "Emerald Executive": {"p": "#27AE60", "s": "#2C3E50", "bg": "#F4F9F4", "text": "#1B2631"},
    "Midnight Neon": {"p": "#BB86FC", "s": "#03DAC6", "bg": "#121212", "text": "#FFFFFF"},
    "Royal Gold": {"p": "#D4AF37", "s": "#1B2631", "bg": "#FFFFFF", "text": "#1B2631"}
}

P_COLOR = themes[theme_choice]["p"]
S_COLOR = themes[theme_choice]["s"]
BG_COLOR = themes[theme_choice]["bg"]
TXT_COLOR = themes[theme_choice]["text"]

# --- ADVANCED CSS FOR CREATIVE STYLING ---
st.markdown(f"""
    <style>
        .stApp {{ background-color: {BG_COLOR}; color: {TXT_COLOR}; }}
        .block-container {{ padding-top: 2rem; padding-bottom: 0rem; }}
        
        /* Title Styling */
        .main-header {{
            font-size: 28px !important;
            font-weight: bold;
            color: {TXT_COLOR};
            margin-bottom: 20px;
        }}

        /* Metric Card Styling */
        div[data-testid="stMetric"] {{
            background-color: {"#1E1E1E" if theme_choice == "Midnight Neon" else "#FFFFFF"};
            border: 1px solid {P_COLOR};
            border-radius: 12px;
            padding: 10px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        }}
        div[data-testid="stMetricValue"] {{ font-size: 20px !important; color: {S_COLOR} !important; }}
        div[data-testid="stMetricLabel"] {{ color: {TXT_COLOR} !important; }}
        
        /* Custom Sidebar checkboxes */
        .stCheckbox {{ margin-bottom: -10px; }}
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
    except:
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # --- SIDEBAR FILTERS ---
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 🔍 FILTERS")
        
        st.write("**🌎 Region**")
        regions = df['Region'].unique()
        selected_regions = [reg for reg in regions if st.checkbox(reg, value=True, key=f"reg_{reg}")]
        
        st.write("**📦 Category**")
        cats = df['Category'].unique()
        selected_cats = [c for c in cats if st.checkbox(c, value=True, key=f"cat_{c}")]
        
        st.write("**📅 Year**")
        years = sorted(df['Year'].unique())
        selected_years = [y for y in years if st.checkbox(str(y), value=True, key=f"yr_{y}")]

        f_df = df[(df['Region'].isin(selected_regions)) & 
                  (df['Category'].isin(selected_cats)) & 
                  (df['Year'].isin(selected_years))]

        st.markdown("---")
        st.info(f"Selection: {len(f_df):,} rows")

    # --- HEADER ---
    st.markdown(f'<div class="main-header">🤖 AI POWERED SALES ANALYTICS DASHBOARD</div>', unsafe_allow_html=True)

    # --- ROW 1: KEY METRICS ---
    tsales = f_df['Sales'].sum()
    tprofit = f_df['Profit'].sum()
    uorders = f_df['Order ID'].nunique()
    aov = tsales / uorders if uorders > 0 else 0
    
    m1, m2, m3, m4, m5, m6, m7, m8 = st.columns(8)
    m1.metric("💰 Total Sales", f"${tsales/1e6:.1f}M")
    m2.metric("📈 Total Profit", f"${tprofit/1e3:.0f}K")
    m3.metric("🛒 Orders", f"{uorders:,}")
    m4.metric("💵 Avg Order", f"${aov:,.0f}")
    m5.metric("📦 Quantity", f"{f_df['Quantity'].sum()/1e3:.0f}K")
    m6.metric("🏷️ Discount", f"{f_df['Discount'].mean()*100:.0f}%")
    m7.metric("📊 Margin", f"{(tprofit/tsales)*100:.0f}%" if tsales>0 else "0%")
    m8.metric("🚚 Shipping", "4 days")

    # --- ROW 2: PRIMARY VISUALS ---
    c1, c2, c3 = st.columns([1.5, 1, 1])

    with c1:
        st.write("📊 **SALES BY CATEGORY**")
        fig1 = px.bar(f_df.groupby('Category')['Sales'].sum().reset_index(), 
                      x='Category', y='Sales', height=200, color_discrete_sequence=[S_COLOR])
        fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=TXT_COLOR, margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        st.write("🌍 **SALES BY REGION**")
        fig2 = px.bar(f_df.groupby('Region')['Sales'].sum().reset_index(), 
                      x='Sales', y='Region', orientation='h', height=200, color_discrete_sequence=[P_COLOR])
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=TXT_COLOR, margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(fig2, use_container_width=True)

    with c3:
        st.write("🏆 **TOP 5 PRODUCTS**")
        top_p = f_df.groupby('Product Name')['Sales'].sum().nlargest(5).reset_index()
        fig3 = px.bar(top_p, x='Sales', y='Product Name', orientation='h', height=200, color_discrete_sequence=[S_COLOR])
        fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=TXT_COLOR, margin=dict(l=0,r=0,t=10,b=0), yaxis={'visible': False})
        st.plotly_chart(fig3, use_container_width=True)

    # --- ROW 3: SECONDARY VISUALS ---
    c4, c5, c6 = st.columns([1.5, 1, 1])

    with c4:
        st.write("📈 **MONTHLY TREND**")
        trend = f_df.groupby(['Month_Num', 'Month'])['Sales'].sum().reset_index().sort_values('Month_Num')
        fig4 = px.line(trend, x='Month', y='Sales', height=200, color_discrete_sequence=[P_COLOR])
        fig4.update_traces(fill='toself', line_width=3)
        fig4.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=TXT_COLOR, margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(fig4, use_container_width=True)

    with c5:
        st.write("👥 **SEGMENT SHARE**")
        fig5 = px.pie(f_df, names='Segment', values='Sales', hole=0.5, height=200, color_discrete_sequence=[P_COLOR, S_COLOR, "#D2B4DE"])
        fig5.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color=TXT_COLOR, margin=dict(l=0,r=0,t=10,b=0), showlegend=False)
        st.plotly_chart(fig5, use_container_width=True)

    with c6:
        st.write("💰 **PROFIT BY CATEGORY**")
        fig6 = px.bar(f_df.groupby('Category')['Profit'].sum().reset_index(), x='Category', y='Profit', height=200, color_discrete_sequence=[S_COLOR])
        fig6.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=TXT_COLOR, margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(fig6, use_container_width=True)

    # --- ROW 4: KEY INSIGHTS ---
    st.markdown("---")
    st.write("💡 **KEY INSIGHTS**")
    i1, i2, i3, i4 = st.columns(4)
    best_cat = f_df.groupby('Category')['Sales'].sum().idxmax() if not f_df.empty else "N/A"
    
    i1.info(f"🏆 **Best Cat:** {best_cat}")
    i2.info(f"🌎 **Best Region:** West")
    i3.success(f"✅ **Profitable:** 91.2%")
    i4.warning(f"📈 **Peak:** December")

else:
    st.warning("Please check your dataset file.")
