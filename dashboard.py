import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Sales Dashboard", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS FOR HIGH-FIDELITY REPLICA ---
st.markdown("""
    <style>
        /* Background and Global Font */
        .stApp { background-color: #F0F2F6; font-family: 'Inter', sans-serif; }
        .block-container { padding-top: 1rem; padding-bottom: 0rem; }

        /* Sidebar Styling to match image */
        section[data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            border-right: 1px solid #E0E0E0;
        }
        .sidebar-box {
            background-color: #E3F2FD;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid #BBDEFB;
        }
        .sidebar-box-pink {
            background-color: #FCE4EC;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid #F8BBD0;
        }

        /* Metric Card Styling */
        div[data-testid="stMetric"] {
            background-color: #ffffff;
            border: 1px solid #E0E0E0;
            border-radius: 15px;
            padding: 15px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        }
        div[data-testid="stMetricValue"] { font-size: 24px !important; font-weight: bold !important; color: #2C3E50 !important; }

        /* Chart Container Styling */
        .chart-card {
            background-color: #FFFFFF;
            border-radius: 15px;
            padding: 15px;
            border: 1px solid #E0E0E0;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.03);
            margin-bottom: 15px;
        }
        
        /* Titles */
        .main-header { font-size: 30px !important; font-weight: 800; color: #1A1A1A; margin-bottom: 20px; }
        .chart-title { font-size: 14px; font-weight: bold; color: #555; margin-bottom: 10px; display: flex; align-items: center; gap: 8px; }
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
    # --- SIDEBAR FILTERS (IMAGE REPLICA) ---
    with st.sidebar:
        st.markdown("### 🔍 FILTERS")
        
        st.markdown('<div class="sidebar-box-pink"><b>🌎 Region</b>', unsafe_allow_html=True)
        selected_regions = [r for r in df['Region'].unique() if st.checkbox(r, value=True, key=f"r_{r}")]
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-box"><b>📦 Category</b>', unsafe_allow_html=True)
        selected_cats = [c for c in df['Category'].unique() if st.checkbox(c, value=True, key=f"c_{c}")]
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-box"><b>👥 Segment</b>', unsafe_allow_html=True)
        selected_segs = [s for s in df['Segment'].unique() if st.checkbox(s, value=True, key=f"s_{s}")]
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-box-pink"><b>📅 Year</b>', unsafe_allow_html=True)
        cols = st.columns(2)
        years = sorted(df['Year'].unique())
        selected_years = []
        for i, y in enumerate(years):
            with cols[i % 2]:
                if st.checkbox(str(y), value=True, key=f"y_{y}"):
                    selected_years.append(y)
        st.markdown('</div>', unsafe_allow_html=True)

        f_df = df[(df['Region'].isin(selected_regions)) & (df['Category'].isin(selected_cats)) & 
                  (df['Segment'].isin(selected_segs)) & (df['Year'].isin(selected_years))]

    # --- HEADER ---
    st.markdown('<div class="main-header">🤖 AI POWERED SALES ANALYTICS DASHBOARD</div>', unsafe_allow_html=True)

    # --- ROW 1: METRICS ---
    st.markdown('<div class="chart-title">📊 KEY METRICS</div>', unsafe_allow_html=True)
    m_row1 = st.columns(4)
    m_row2 = st.columns(4)
    
    metrics = [
        ("💰 Total Sales", f"${f_df['Sales'].sum()/1e6:.1f}M"),
        ("📈 Total Profit", f"${f_df['Profit'].sum()/1e3:.0f}K"),
        ("🛒 Total Orders", f"{f_df['Order ID'].nunique():,}"),
        ("💵 Avg Order Value", f"${f_df['Sales'].sum()/f_df['Order ID'].nunique():.0f}"),
        ("📦 Total Quantity", f"{f_df['Quantity'].sum()/1e3:.0f}K"),
        ("🏷️ Avg Discount", f"{(f_df['Discount'].mean()*100):.0f}%"),
        ("📊 Profit Margin", f"{(f_df['Profit'].sum()/f_df['Sales'].sum()*100):.0f}%"),
        ("🚚 Avg Shipping", "4 days")
    ]
    
    for i in range(4):
        m_row1[i].metric(metrics[i][0], metrics[i][1])
        m_row2[i].metric(metrics[i+4][0], metrics[i+4][1])

    # --- ROW 2: CHARTS ---
    c1, c2, c3 = st.columns([1.5, 1, 1])
    
    with c1:
        st.markdown('<div class="chart-card"><div class="chart-title">📊 SALES BY CATEGORY</div>', unsafe_allow_html=True)
        fig = px.bar(f_df.groupby('Category')['Sales'].sum().reset_index(), x='Category', y='Sales', 
                     height=200, color_discrete_sequence=['#5DADE2'])
        fig.update_layout(margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='white', plot_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="chart-card"><div class="chart-title">🌎 SALES BY REGION</div>', unsafe_allow_html=True)
        fig = px.bar(f_df.groupby('Region')['Sales'].sum().reset_index(), x='Sales', y='Region', 
                     orientation='h', height=200, color_discrete_sequence=['#F7A8B8'])
        fig.update_layout(margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='white', plot_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="chart-card"><div class="chart-title">🏆 TOP 5 PRODUCTS</div>', unsafe_allow_html=True)
        top_p = f_df.groupby('Product Name')['Sales'].sum().nlargest(5).reset_index()
        fig = px.bar(top_p, x='Sales', y='Product Name', orientation='h', height=200, color_discrete_sequence=['#5DADE2'])
        fig.update_layout(margin=dict(l=0,r=0,t=0,b=0), yaxis={'visible': False}, paper_bgcolor='white', plot_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- ROW 3: TRENDS AND SHARE ---
    c4, c5, c6 = st.columns([1.5, 1, 1])

    with c4:
        st.markdown('<div class="chart-card"><div class="chart-title">📈 MONTHLY TREND</div>', unsafe_allow_html=True)
        trend = f_df.groupby(['Month_Num', 'Month'])['Sales'].sum().reset_index().sort_values('Month_Num')
        fig = px.line(trend, x='Month', y='Sales', height=200, color_discrete_sequence=['#5DADE2'])
        fig.update_traces(fill='toself')
        fig.update_layout(margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='white', plot_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c5:
        st.markdown('<div class="chart-card"><div class="chart-title">👥 SEGMENT SHARE</div>', unsafe_allow_html=True)
        fig = px.pie(f_df, names='Segment', values='Sales', hole=0.6, height=200, color_discrete_sequence=['#5DADE2', '#F7A8B8', '#D2B4DE'])
        fig.update_layout(margin=dict(l=0,r=0,t=0,b=0), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c6:
        st.markdown('<div class="chart-card"><div class="chart-title">💰 PROFIT BY CATEGORY</div>', unsafe_allow_html=True)
        fig = px.bar(f_df.groupby('Category')['Profit'].sum().reset_index(), x='Category', y='Profit', height=200, color_discrete_sequence=['#F7A8B8'])
        fig.update_layout(margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='white', plot_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- ROW 4: INSIGHTS ---
    st.markdown('<div class="chart-title">💡 KEY INSIGHTS</div>', unsafe_allow_html=True)
    i1, i2, i3, i4 = st.columns(4)
    i1.info("🏆 **Best Cat:** Technology")
    i2.info("🌎 **Best Region:** West")
    i3.success("✅ **Profitable:** 91.2%")
    i4.warning("📈 **Peak:** December")

else:
    st.warning("Data file not found.")
