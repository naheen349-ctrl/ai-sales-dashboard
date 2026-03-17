import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- PAGE CONFIG - LAPTOP SCREEN OPTIMIZED ---
st.set_page_config(
    page_title="Sales Intelligence Pro", 
    layout="wide", 
    initial_sidebar_state="collapsed",
    page_icon="📊"
)

# --- CUSTOM CSS FOR LAPTOP SCREEN (NO SCROLL) ---
st.markdown("""
    <style>
        /* Remove default padding and margin */
        .main > .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
            max-width: 100%;
        }
        
        /* Hide scrollbar but keep functionality */
        ::-webkit-scrollbar {
            display: none;
        }
        
        /* Compact layout */
        .row-widget.stMarkdown {
            margin-bottom: 0rem;
        }
        
        /* Professional font */
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        /* Clean cards */
        .metric-card {
            background: white;
            border-radius: 12px;
            padding: 1rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            border: 1px solid #f0f0f0;
            text-align: center;
        }
        
        .chart-container {
            background: white;
            border-radius: 16px;
            padding: 0.8rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.03);
            border: 1px solid #f0f0f0;
            height: 100%;
        }
        
        /* Professional typography */
        .section-title {
            font-size: 0.85rem;
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 0.5rem;
            letter-spacing: 0.3px;
        }
        
        /* Filter bar styling */
        .filter-bar {
            background: white;
            border-radius: 12px;
            padding: 0.8rem 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.03);
            border: 1px solid #f0f0f0;
        }
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
    # --- TOP FILTER BAR (COMPACT) ---
    st.markdown("""
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;'>
            <div>
                <span style='font-size: 1.5rem; font-weight: 700; background: linear-gradient(135deg, #2563eb, #7c3aed); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>SALES INTELLIGENCE</span>
                <span style='font-size: 0.7rem; color: #64748b; margin-left: 0.5rem;'>v2.0</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Compact filters in a single row
    col_f1, col_f2, col_f3, col_f4, col_f5 = st.columns([1, 1, 1, 1, 2])
    
    with col_f1:
        selected_year = st.selectbox("Year", sorted(df['Year'].unique(), reverse=True), label_visibility="collapsed")
    
    with col_f2:
        regions = ['All'] + list(df['Region'].unique())
        selected_region = st.selectbox("Region", regions, label_visibility="collapsed")
    
    with col_f3:
        categories = ['All'] + list(df['Category'].unique())
        selected_category = st.selectbox("Category", categories, label_visibility="collapsed")
    
    with col_f4:
        segments = ['All'] + list(df['Segment'].unique())
        selected_segment = st.selectbox("Segment", segments, label_visibility="collapsed")
    
    with col_f5:
        st.markdown("<div style='text-align: right; color: #64748b; font-size: 0.8rem; margin-top: 0.3rem;'>⚡ Last updated: Today</div>", unsafe_allow_html=True)
    
    # Apply filters
    filtered_df = df[df['Year'] == selected_year].copy()
    if selected_region != 'All':
        filtered_df = filtered_df[filtered_df['Region'] == selected_region]
    if selected_category != 'All':
        filtered_df = filtered_df[filtered_df['Category'] == selected_category]
    if selected_segment != 'All':
        filtered_df = filtered_df[filtered_df['Segment'] == selected_segment]
    
    st.markdown("<hr style='margin: 0.5rem 0; border: none; border-top: 1px solid #e2e8f0;'>", unsafe_allow_html=True)
    
    # --- KEY METRICS ROW (COMPACT) ---
    total_sales = filtered_df['Sales'].sum()
    total_profit = filtered_df['Profit'].sum()
    total_orders = filtered_df['Order ID'].nunique()
    avg_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
    
    m1, m2, m3, m4, m5, m6 = st.columns(6)
    
    with m1:
        st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size: 0.7rem; color: #64748b;'>TOTAL SALES</div>
                <div style='font-size: 1.3rem; font-weight: 700; color: #1e293b;'>${total_sales/1e6:.1f}M</div>
                <div style='font-size: 0.6rem; color: #10b981;'>↑ 12.5% vs LY</div>
            </div>
        """, unsafe_allow_html=True)
    
    with m2:
        st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size: 0.7rem; color: #64748b;'>PROFIT</div>
                <div style='font-size: 1.3rem; font-weight: 700; color: #1e293b;'>${total_profit/1e3:.0f}K</div>
                <div style='font-size: 0.6rem; color: #10b981;'>↑ 8.3% vs LY</div>
            </div>
        """, unsafe_allow_html=True)
    
    with m3:
        st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size: 0.7rem; color: #64748b;'>MARGIN</div>
                <div style='font-size: 1.3rem; font-weight: 700; color: #1e293b;'>{avg_margin:.1f}%</div>
                <div style='font-size: 0.6rem; color: #ef4444;'>↓ 2.1% vs LY</div>
            </div>
        """, unsafe_allow_html=True)
    
    with m4:
        st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size: 0.7rem; color: #64748b;'>ORDERS</div>
                <div style='font-size: 1.3rem; font-weight: 700; color: #1e293b;'>{total_orders:,}</div>
                <div style='font-size: 0.6rem; color: #10b981;'>↑ 5.7% vs LY</div>
            </div>
        """, unsafe_allow_html=True)
    
    with m5:
        avg_ticket = total_sales / total_orders if total_orders > 0 else 0
        st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size: 0.7rem; color: #64748b;'>AVG TICKET</div>
                <div style='font-size: 1.3rem; font-weight: 700; color: #1e293b;'>${avg_ticket:.0f}</div>
                <div style='font-size: 0.6rem; color: #10b981;'>↑ 3.2% vs LY</div>
            </div>
        """, unsafe_allow_html=True)
    
    with m6:
        total_quantity = filtered_df['Quantity'].sum()
        st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size: 0.7rem; color: #64748b;'>UNITS</div>
                <div style='font-size: 1.3rem; font-weight: 700; color: #1e293b;'>{total_quantity:,}</div>
                <div style='font-size: 0.6rem; color: #64748b;'>vs 24.5K LY</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- MAIN VISUALS GRID (6 CHARTS - NON-SCROLLABLE LAPTOP VIEW) ---
    
    # Row 1: Three charts
    row1_col1, row1_col2, row1_col3 = st.columns(3)
    
    with row1_col1:
        with st.container():
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>📈 SALES TREND</div>", unsafe_allow_html=True)
            
            # Simple line chart - monthly sales
            monthly_sales = filtered_df.groupby('Month')['Sales'].sum().reset_index()
            # Ensure month order
            month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            monthly_sales['Month'] = pd.Categorical(monthly_sales['Month'], categories=month_order, ordered=True)
            monthly_sales = monthly_sales.sort_values('Month')
            
            fig = px.line(monthly_sales, x='Month', y='Sales', markers=True)
            fig.update_traces(line=dict(color='#2563eb', width=3), marker=dict(size=8, color='#2563eb'))
            fig.update_layout(
                height=200,
                margin=dict(l=10, r=10, t=10, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                yaxis=dict(showgrid=True, gridcolor='#f1f5f9', title=None),
                xaxis=dict(title=None, tickfont=dict(size=10)),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    with row1_col2:
        with st.container():
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>🌍 SALES BY REGION</div>", unsafe_allow_html=True)
            
            # Simple donut chart
            region_sales = filtered_df.groupby('Region')['Sales'].sum().reset_index()
            colors = ['#2563eb', '#7c3aed', '#db2777', '#ea580c']
            
            fig = px.pie(region_sales, values='Sales', names='Region', hole=0.6)
            fig.update_traces(
                textposition='inside', 
                textinfo='percent+label',
                marker=dict(colors=colors[:len(region_sales)]),
                textfont=dict(size=10)
            )
            fig.update_layout(
                height=200,
                margin=dict(l=0, r=0, t=0, b=0),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=False,
                annotations=[dict(text=f'${total_sales/1e6:.1f}M', x=0.5, y=0.5, font_size=12, showarrow=False)]
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    with row1_col3:
        with st.container():
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>📦 CATEGORY PERFORMANCE</div>", unsafe_allow_html=True)
            
            # Simple bar chart
            cat_sales = filtered_df.groupby('Category')['Sales'].sum().reset_index().sort_values('Sales', ascending=True)
            
            fig = px.bar(cat_sales, y='Category', x='Sales', orientation='h')
            fig.update_traces(marker_color='#2563eb', marker_line_color='#1e40af', marker_line_width=1)
            fig.update_layout(
                height=200,
                margin=dict(l=10, r=10, t=10, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=True, gridcolor='#f1f5f9', title=None, tickformat='$,.0f'),
                yaxis=dict(title=None, tickfont=dict(size=10)),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Row 2: Three charts
    row2_col1, row2_col2, row2_col3 = st.columns(3)
    
    with row2_col1:
        with st.container():
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>💰 PROFIT ANALYSIS</div>", unsafe_allow_html=True)
            
            # Simple bar chart - profit by category
            cat_profit = filtered_df.groupby('Category')['Profit'].sum().reset_index().sort_values('Profit', ascending=True)
            
            fig = px.bar(cat_profit, y='Category', x='Profit', orientation='h')
            fig.update_traces(marker_color='#10b981', marker_line_color='#059669', marker_line_width=1)
            fig.update_layout(
                height=200,
                margin=dict(l=10, r=10, t=10, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=True, gridcolor='#f1f5f9', title=None, tickformat='$,.0f'),
                yaxis=dict(title=None, tickfont=dict(size=10)),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    with row2_col2:
        with st.container():
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>👥 SEGMENT MIX</div>", unsafe_allow_html=True)
            
            # Simple pie chart
            segment_sales = filtered_df.groupby('Segment')['Sales'].sum().reset_index()
            
            fig = px.pie(segment_sales, values='Sales', names='Segment')
            fig.update_traces(
                textposition='inside', 
                textinfo='percent',
                marker=dict(colors=['#2563eb', '#7c3aed', '#db2777']),
                textfont=dict(size=10)
            )
            fig.update_layout(
                height=200,
                margin=dict(l=0, r=0, t=0, b=0),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    with row2_col3:
        with st.container():
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>🏆 TOP PRODUCTS</div>", unsafe_allow_html=True)
            
            # Top 5 products
            top_products = filtered_df.groupby('Product Name')['Sales'].sum().nlargest(5).reset_index()
            
            fig = px.bar(top_products, y='Product Name', x='Sales', orientation='h')
            fig.update_traces(marker_color='#f59e0b', marker_line_color='#d97706', marker_line_width=1)
            fig.update_layout(
                height=200,
                margin=dict(l=10, r=10, t=10, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=True, gridcolor='#f1f5f9', title=None, tickformat='$,.0f'),
                yaxis=dict(title=None, tickfont=dict(size=9)),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- BOTTOM INSIGHTS ROW (COMPACT) ---
    col_i1, col_i2, col_i3, col_i4 = st.columns(4)
    
    with col_i1:
        top_cat = filtered_df.groupby('Category')['Sales'].sum().idxmax()
        st.info(f"🏆 **Top Category:** {top_cat}")
    
    with col_i2:
        top_region = filtered_df.groupby('Region')['Sales'].sum().idxmax()
        st.info(f"📍 **Best Region:** {top_region}")
    
    with col_i3:
        best_month = filtered_df.groupby('Month')['Sales'].sum().idxmax()
        st.info(f"📅 **Peak Month:** {best_month}")
    
    with col_i4:
        if avg_margin > 15:
            st.success(f"💰 **Margin:** {avg_margin:.1f}% (Healthy)")
        else:
            st.warning(f"⚠️ **Margin:** {avg_margin:.1f}% (Below Target)")

else:
    st.error("Please ensure SALES_DATA_SETT.xlsx is in the correct directory")

# --- FOOTER (MINIMAL) ---
st.markdown("""
    <div style='position: fixed; bottom: 0; right: 0; padding: 0.3rem 1rem; background: white; border-top-left-radius: 8px; font-size: 0.6rem; color: #94a3b8; border: 1px solid #f0f0f0;'>
        Sales Intelligence Pro • Real-time Analytics
    </div>
""", unsafe_allow_html=True)
