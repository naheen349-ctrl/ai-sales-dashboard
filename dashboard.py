import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Sales Intelligence", layout="wide", initial_sidebar_state="expanded")

# --- THEME CONFIG ---
with st.sidebar:
    st.markdown("### 🎨 VISUAL UNIVERSE")
    theme_choice = st.selectbox("Select Theme", ["Midnight Neon", "Emerald Glass", "Oceanic Pro", "Sunset Rose"])

themes = {
    "Midnight Neon": {"p": "#BB86FC", "s": "#03DAC6", "bg": "#0E1117", "card": "rgba(20, 20, 20, 0.85)", "txt": "#FFFFFF", "sub": "#BB86FC"},
    "Emerald Glass": {"p": "#1E8449", "s": "#2C3E50", "bg": "#F1F9F4", "card": "rgba(255, 255, 255, 0.95)", "txt": "#000000", "sub": "#1E8449"},
    "Oceanic Pro": {"p": "#1F618D", "s": "#21618C", "bg": "#EBF5FB", "card": "rgba(255, 255, 255, 0.95)", "txt": "#000000", "sub": "#1F618D"},
    "Sunset Rose": {"p": "#C0392B", "s": "#641E16", "bg": "#FDF2F4", "card": "rgba(255, 255, 255, 0.95)", "txt": "#000000", "sub": "#C0392B"}
}
th = themes[theme_choice]

# --- REFINED HIGH-VISIBILITY CSS ---
st.markdown(f"""
    <style>
        .stApp {{ background-color: {th['bg']}; color: {th['txt']}; }}
        
        /* 1. Header Visibility */
        .main-title {{
            font-size: 38px !important;
            font-weight: 900 !important;
            color: {th['txt']};
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            text-align: center;
            margin-bottom: 20px;
        }}

        /* 2. KPI Box Visibility - Darker text, bolder fonts */
        .kpi-box {{
            text-align: center;
            padding: 15px;
            background: {th['card']};
            border-radius: 15px;
            border: 2px solid {th['p']};
            box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        }}
        .kpi-label {{
            font-size: 13px !important;
            color: {th['txt']};
            opacity: 0.8;
            font-weight: 700 !important;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .kpi-value {{
            font-size: 24px !important;
            font-weight: 900 !important;
            color: {th['p']};
            text-shadow: 1px 1px 0px rgba(0,0,0,0.05);
        }}

        /* 3. Visuals Visibility */
        .glass-container {{
            background: {th['card']};
            border-radius: 20px;
            padding: 20px;
            border: 1px solid rgba(0, 0, 0, 0.1);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.05);
            margin-bottom: 20px;
            color: {th['txt']} !important;
        }}
        
        /* 4. Sidebar/Filter Visibility */
        [data-testid="stSidebar"] {{
            background-color: {th['card']} !important;
            border-right: 2px solid {th['p']};
        }}
        .stCheckbox label {{
            font-weight: 700 !important;
            color: {th['txt']} !important;
        }}

        .block-container {{ padding-top: 4rem !important; }}
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
        st.markdown(f"<h2 style='color:{th['p']}; font-weight:900;'>🔍 CONTROL PANEL</h2>", unsafe_allow_html=True)
        st.markdown("---")
        sel_region = [r for r in df['Region'].unique() if st.checkbox(f"🌎 {r}", True)]
        st.markdown("---")
        sel_cat = [c for c in df['Category'].unique() if st.checkbox(f"📦 {c}", True)]
        st.markdown("---")
        sel_year = [y for y in sorted(df['Year'].unique()) if st.checkbox(f"📅 {y}", True)]
        
        f_df = df[(df['Region'].isin(sel_region)) & (df['Category'].isin(sel_cat)) & (df['Year'].isin(sel_year))]

    # --- MAIN TITLE ---
    st.markdown(f'<div class="main-title">🤖 AI SALES INTELLIGENCE PRO</div>', unsafe_allow_html=True)

    # --- 8 KPIs (ROW 1) ---
    k_cols = st.columns(8)
    metrics = [
        ("💰", "Revenue", f"${f_df['Sales'].sum()/1e6:.1f}M"),
        ("📈", "Profit", f"${f_df['Profit'].sum()/1e3:.0f}K"),
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
                <div style='font-size:26px;'>{icon}</div>
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{val}</div>
            </div>
        """, unsafe_allow_html=True)

    st.write("")

    # --- 6 VISUALS GRID ---
    r1 = st.columns(3)
    r2 = st.columns(3)

    # Helper for charts to ensure visibility
    def update_fig(fig):
        fig.update_layout(
            margin=dict(l=10, r=10, t=30, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=th['txt'], size=12, family="Arial Black"),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False)
        )
        return fig

    with r1[0]:
        st.markdown('<div class="glass-container"><b>📊 SALES DYNAMICS</b>', unsafe_allow_html=True)
        fig1 = px.bar(f_df.groupby('Category')['Sales'].sum().reset_index(), x='Category', y='Sales', height=210, color_discrete_sequence=[th['p']])
        st.plotly_chart(update_fig(fig1), use_container_width=True, key="c1")
        st.markdown('</div>', unsafe_allow_html=True)

    with r1[1]:
        st.markdown('<div class="glass-container"><b>🌍 REGIONAL MIX</b>', unsafe_allow_html=True)
        fig2 = px.pie(f_df, names='Region', values='Sales', hole=0.5, height=210, color_discrete_sequence=[th['p'], th['s'], "#8E44AD", "#34495E"])
        fig2.update_layout(showlegend=False)
        st.plotly_chart(update_fig(fig2), use_container_width=True, key="c2")
        st.markdown('</div>', unsafe_allow_html=True)

    with r1[2]:
        st.markdown('<div class="glass-container"><b>🏆 ELITE PRODUCTS</b>', unsafe_allow_html=True)
        top_p = f_df.groupby('Product Name')['Sales'].sum().nlargest(5).reset_index()
        fig3 = px.bar(top_p, x='Sales', y='Product Name', orientation='h', height=210, color_discrete_sequence=[th['s']])
        fig3.update_layout(yaxis={'visible': False})
        st.plotly_chart(update_fig(fig3), use_container_width=True, key="c3")
        st.markdown('</div>', unsafe_allow_html=True)

    with r2[0]:
        st.markdown('<div class="glass-container"><b>📈 GROWTH TREND</b>', unsafe_allow_html=True)
        trend = f_df.groupby(['Month_Num', 'Month'])['Sales'].sum().reset_index().sort_values('Month_Num')
        fig4 = px.area(trend, x='Month', y='Sales', height=210, color_discrete_sequence=[th['p']])
        st.plotly_chart(update_fig(fig4), use_container_width=True, key="c4")
        st.markdown('</div>', unsafe_allow_html=True)

    with r2[1]:
        st.markdown('<div class="glass-container"><b>👥 SEGMENT SHARE</b>', unsafe_allow_html=True)
        fig5 = px.pie(f_df, names='Segment', values='Sales', height=210, color_discrete_sequence=[th['s'], th['p'], "#D2B4DE"])
        fig5.update_layout(showlegend=False)
        st.plotly_chart(update_fig(fig5), use_container_width=True, key="c5")
        st.markdown('</div>', unsafe_allow_html=True)

    with r2[2]:
        st.markdown('<div class="glass-container"><b>💰 PROFIT YIELD</b>', unsafe_allow_html=True)
        fig6 = px.bar(f_df.groupby('Category')['Profit'].sum().reset_index(), x='Category', y='Profit', height=210, color_discrete_sequence=[th['s']])
        st.plotly_chart(update_fig(fig6), use_container_width=True, key="c6")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- BOTTOM INSIGHTS ---
    st.markdown(f"<h3 style='color:{th['txt']}; font-weight:900;'>💡 STRATEGIC INSIGHTS</h3>", unsafe_allow_html=True)
    i_cols = st.columns(4)
    with i_cols[0]: st.success(f"**TOP CAT:** {f_df.groupby('Category')['Sales'].sum().idxmax()}")
    with i_cols[1]: st.info("**REGION:** West Leads")
    with i_cols[2]: st.warning("**RISK:** Supply Chain")
    with i_cols[3]: st.error("**ACTION:** Q4 Prep")

else:
    st.error("Missing SALES_DATA_SETT.xlsx!")
