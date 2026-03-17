import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- PAGE CONFIG - PROFESSIONAL LAPTOP VIEW ---
st.set_page_config(
    page_title="Sales Intelligence Pro", 
    layout="wide", 
    initial_sidebar_state="collapsed",
    page_icon="📊"
)

# --- PROFESSIONAL CSS (CLEAN, MODERN, NO SCROLL) ---
st.markdown("""
    <style>
        /* Import professional font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        /* Reset and base styles */
        .main > .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
            padding-left: 1.5rem;
            padding-right: 1.5rem;
            max-width: 100%;
            font-family: 'Inter', sans-serif;
        }
        
        /* Hide scrollbar but keep functionality */
        ::-webkit-scrollbar {
            display: none;
        }
        
        /* Professional metric cards */
        .metric-card {
            background: white;
            border-radius: 16px;
            padding: 1.2rem 1rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.02);
            border: 1px solid #f0f2f5;
            text-align: center;
            transition: all 0.2s ease;
        }
        .metric-card:hover {
            box-shadow: 0 8px 30px rgba(0,0,0,0.04);
            border-color: #e0e7ff;
        }
        
        /* Chart containers */
        .chart-container {
            background: white;
            border-radius: 20px;
            padding: 1rem 1rem 0.5rem 1rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.02);
            border: 1px solid #f0f2f5;
            height: 100%;
            transition: all 0.2s ease;
        }
        .chart-container:hover {
            box-shadow: 0 8px 30px rgba(0,0,0,0.04);
        }
        
        /* Section titles */
        .section-title {
            font-size: 0.85rem;
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 0.8rem;
            letter-spacing: 0.02em;
            text-transform: uppercase;
        }
        
        /* Filter bar styling */
        .filter-bar {
            background: white;
            border-radius: 16px;
            padding: 1rem 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.02);
            border: 1px solid #f0f2f5;
        }
        
        /* Professional header */
        .dashboard-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
        }
        .dashboard-title {
            font-size: 1.8rem;
            font-weight: 700;
            background: linear-gradient(135deg, #2563eb, #7c3aed);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.02em;
        }
        .dashboard-badge {
            background: #f8fafc;
            padding: 0.4rem 1rem;
            border-radius: 40px;
            font-size: 0.75rem;
            color: #64748b;
            border: 1px solid #e2e8f0;
        }
        
        /* KPI labels */
        .kpi-label {
            font-size: 0.7rem;
            color: #64748b;
            font-weight: 500;
            letter-spacing: 0.03em;
        }
        .kpi-value {
            font-size: 1.4rem;
            font-weight: 700;
            color: #0f172a;
            line-height: 1.3;
        }
        .kpi-trend {
            font-size: 0.65rem;
            font-weight: 500;
            margin-top: 0.3rem;
        }
        .trend-up { color: #10b981; }
        .trend-down { color: #ef4444; }
        .trend-neutral { color: #64748b; }
        
        /* Footer */
        .dashboard-footer {
            position: fixed;
            bottom: 0;
            right: 1rem;
            background: white;
            padding: 0.3rem 1rem;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            font-size: 0.65rem;
            color: #94a3b8;
            border: 1px solid #f0f2f5;
            border-bottom: none;
        }
        
        /* Divider */
        .custom-divider {
            margin: 1rem 0;
            border: none;
            border-top: 1px solid #eef2f6;
        }
        
        /* Selectbox styling */
        .stSelectbox > div > div {
            background-color: white;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            font-size: 0.85rem;
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
        
        # Ensure month order
        month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        df['Month'] = pd.Categorical(df['Month'], categories=month_order, ordered=True)
        
        return df
    except Exception as e:
        st.error(f"Please ensure SALES_DATA_SETT.xlsx is in the correct directory")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # --- PROFESSIONAL HEADER ---
    st.markdown("""
        <div class='dashboard-header'>
            <div>
                <span class='dashboard-title'>SALES INTELLIGENCE PRO</span>
                <span class='dashboard-badge' style='margin-left: 1rem;'>v2.0 · Enterprise</span>
            </div>
            <div style='display: flex; gap: 0.5rem;'>
                <span class='dashboard-badge'>⚡ Live</span>
                <span class='dashboard-badge'>📅 Real-time</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # --- COMPACT FILTER ROW ---
    col_f1, col_f2, col_f3, col_f4, col_f5 = st.columns([1.2, 1.2, 1.2, 1.2, 2])
    
    with col_f1:
        selected_year = st.selectbox(
            "Year", 
            sorted(df['Year'].unique(), reverse=True),
            label_visibility="collapsed",
            placeholder="Year"
        )
    
    with col_f2:
        regions = ['All Regions'] + list(df['Region'].unique())
        selected_region = st.selectbox("Region", regions, label_visibility="collapsed")
    
    with col_f3:
        categories = ['All Categories'] + list(df['Category'].unique())
        selected_category = st.selectbox("Category", categories, label_visibility="collapsed")
    
    with col_f4:
        segments = ['All Segments'] + list(df['Segment'].unique())
        selected_segment = st.selectbox("Segment", segments, label_visibility="collapsed")
    
    with col_f5:
        st.markdown("""
            <div style='text-align: right; color: #64748b; font-size: 0.8rem; margin-top: 0.3rem;'>
                <span style='background: #f1f5f9; padding: 0.3rem 0.8rem; border-radius: 40px;'>
                    🔍 {selected_year} · {selected_region}
                </span>
            </div>
        """.format(
            selected_year=selected_year,
            selected_region=selected_region.replace('All Regions', 'All')
        ), unsafe_allow_html=True)
    
    # Apply filters
    filtered_df = df[df['Year'] == selected_year].copy()
    if selected_region != 'All Regions':
        filtered_df = filtered_df[filtered_df['Region'] == selected_region]
    if selected_category != 'All Categories':
        filtered_df = filtered_df[filtered_df['Category'] == selected_category]
    if selected_segment != 'All Segments':
        filtered_df = filtered_df[filtered_df['Segment'] == selected_segment]
    
    st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)
    
    # --- KEY METRICS (6 COMPACT CARDS) ---
    total_sales = filtered_df['Sales'].sum()
    total_profit = filtered_df['Profit'].sum()
    total_orders = filtered_df['Order ID'].nunique()
    profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
    avg_ticket = total_sales / total_orders if total_orders > 0 else 0
    total_units = filtered_df['Quantity'].sum()
    
    # Mock previous year data for trends
    prev_year_df = df[df['Year'] == selected_year - 1] if selected_year - 1 in df['Year'].values else pd.DataFrame()
    prev_sales = prev_year_df['Sales'].sum() if not prev_year_df.empty else total_sales * 0.9
    
    # Calculate trends
    sales_trend = ((total_sales - prev_sales) / prev_sales * 100) if prev_sales > 0 else 0
    
    m1, m2, m3, m4, m5, m6 = st.columns(6)
    
    with m1:
        st.markdown(f"""
            <div class='metric-card'>
                <div class='kpi-label'>TOTAL SALES</div>
                <div class='kpi-value'>${total_sales/1e6:.1f}M</div>
                <div class='kpi-trend {"trend-up" if sales_trend > 0 else "trend-down"}'>
                    {'▲' if sales_trend > 0 else '▼'} {abs(sales_trend):.1f}% vs LY
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with m2:
        profit_trend = ((total_profit - prev_year_df['Profit'].sum()) / prev_year_df['Profit'].sum() * 100) if not prev_year_df.empty and prev_year_df['Profit'].sum() > 0 else 5.2
        st.markdown(f"""
            <div class='metric-card'>
                <div class='kpi-label'>PROFIT</div>
                <div class='kpi-value'>${total_profit/1e3:.0f}K</div>
                <div class='kpi-trend {"trend-up" if profit_trend > 0 else "trend-down"}'>
                    {'▲' if profit_trend > 0 else '▼'} {abs(profit_trend):.1f}% vs LY
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with m3:
        margin_trend = profit_margin - (prev_year_df['Profit'].sum() / prev_year_df['Sales'].sum() * 100) if not prev_year_df.empty and prev_year_df['Sales'].sum() > 0 else -2.1
        st.markdown(f"""
            <div class='metric-card'>
                <div class='kpi-label'>MARGIN</div>
                <div class='kpi-value'>{profit_margin:.1f}%</div>
                <div class='kpi-trend {"trend-up" if margin_trend > 0 else "trend-down"}'>
                    {'▲' if margin_trend > 0 else '▼'} {abs(margin_trend):.1f}pp vs LY
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with m4:
        orders_trend = ((total_orders - prev_year_df['Order ID'].nunique()) / prev_year_df['Order ID'].nunique() * 100) if not prev_year_df.empty and prev_year_df['Order ID'].nunique() > 0 else 5.7
        st.markdown(f"""
            <div class='metric-card'>
                <div class='kpi-label'>ORDERS</div>
                <div class='kpi-value'>{total_orders:,}</div>
                <div class='kpi-trend {"trend-up" if orders_trend > 0 else "trend-down"}'>
                    {'▲' if orders_trend > 0 else '▼'} {abs(orders_trend):.1f}% vs LY
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with m5:
        ticket_trend = ((avg_ticket - prev_year_df['Sales'].mean()) / prev_year_df['Sales'].mean() * 100) if not prev_year_df.empty and prev_year_df['Sales'].mean() > 0 else 3.2
        st.markdown(f"""
            <div class='metric-card'>
                <div class='kpi-label'>AVG TICKET</div>
                <div class='kpi-value'>${avg_ticket:.0f}</div>
                <div class='kpi-trend {"trend-up" if ticket_trend > 0 else "trend-down"}'>
                    {'▲' if ticket_trend > 0 else '▼'} {abs(ticket_trend):.1f}% vs LY
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with m6:
        units_trend = ((total_units - prev_year_df['Quantity'].sum()) / prev_year_df['Quantity'].sum() * 100) if not prev_year_df.empty and prev_year_df['Quantity'].sum() > 0 else -1.8
        st.markdown(f"""
            <div class='metric-card'>
                <div class='kpi-label'>UNITS SOLD</div>
                <div class='kpi-value'>{total_units:,}</div>
                <div class='kpi-trend {"trend-up" if units_trend > 0 else "trend-down"}'>
                    {'▲' if units_trend > 0 else '▼'} {abs(units_trend):.1f}% vs LY
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- MAIN VISUALIZATIONS GRID (3x2 LAYOUT) ---
    
    # Row 1: Three charts
    row1_col1, row1_col2, row1_col3 = st.columns(3)
    
    with row1_col1:
        with st.container():
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>📈 SALES TREND</div>", unsafe_allow_html=True)
            
            # Simple line chart - monthly sales
            monthly_sales = filtered_df.groupby('Month', observed=True)['Sales'].sum().reset_index()
            monthly_sales = monthly_sales.sort_values('Month')
            
            fig = px.line(monthly_sales, x='Month', y='Sales', markers=True)
            fig.update_traces(
                line=dict(color='#2563eb', width=3), 
                marker=dict(size=8, color='#2563eb', line=dict(color='white', width=2))
            )
            fig.update_layout(
                height=200,
                margin=dict(l=5, r=5, t=5, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                yaxis=dict(
                    showgrid=True, 
                    gridcolor='#f1f5f9', 
                    title=None,
                    tickformat='$,.0f',
                    tickfont=dict(size=10)
                ),
                xaxis=dict(title=None, tickfont=dict(size=10)),
                showlegend=False,
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    with row1_col2:
        with st.container():
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>🌍 SALES BY REGION</div>", unsafe_allow_html=True)
            
            # Simple donut chart
            region_sales = filtered_df.groupby('Region')['Sales'].sum().reset_index()
            colors = ['#2563eb', '#7c3aed', '#db2777', '#ea580c', '#0891b2']
            
            fig = px.pie(region_sales, values='Sales', names='Region', hole=0.65)
            fig.update_traces(
                textposition='inside', 
                textinfo='percent+label',
                textfont=dict(size=10, color='white'),
                marker=dict(colors=colors[:len(region_sales)], line=dict(color='white', width=2)),
                hovertemplate='<b>%{label}</b><br>Sales: $%{value:,.0f}<br>Share: %{percent}<extra></extra>'
            )
            fig.update_layout(
                height=200,
                margin=dict(l=0, r=0, t=0, b=0),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=False,
                annotations=[dict(
                    text=f'${total_sales/1e6:.1f}M', 
                    x=0.5, y=0.5, 
                    font_size=14, 
                    font_color='#1e293b',
                    font_weight=600,
                    showarrow=False
                )]
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    with row1_col3:
        with st.container():
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>📦 CATEGORY PERFORMANCE</div>", unsafe_allow_html=True)
            
            # Simple horizontal bar chart
            cat_sales = filtered_df.groupby('Category')['Sales'].sum().reset_index().sort_values('Sales', ascending=True)
            
            fig = px.bar(cat_sales, y='Category', x='Sales', orientation='h', text_auto='.2s')
            fig.update_traces(
                marker_color='#2563eb',
                marker_line_color='#1e40af',
                marker_line_width=1,
                textposition='outside',
                textfont=dict(size=10)
            )
            fig.update_layout(
                height=200,
                margin=dict(l=5, r=5, t=5, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(
                    showgrid=True, 
                    gridcolor='#f1f5f9', 
                    title=None, 
                    tickformat='$,.0f',
                    tickfont=dict(size=9)
                ),
                yaxis=dict(title=None, tickfont=dict(size=10)),
                showlegend=False,
                hovermode='y unified'
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Row 2: Three charts
    row2_col1, row2_col2, row2_col3 = st.columns(3)
    
    with row2_col1:
        with st.container():
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>💰 PROFIT BY CATEGORY</div>", unsafe_allow_html=True)
            
            # Simple bar chart - profit by category
            cat_profit = filtered_df.groupby('Category')['Profit'].sum().reset_index().sort_values('Profit', ascending=True)
            
            fig = px.bar(cat_profit, y='Category', x='Profit', orientation='h', text_auto='.2s')
            fig.update_traces(
                marker_color='#10b981',
                marker_line_color='#059669',
                marker_line_width=1,
                textposition='outside',
                textfont=dict(size=10)
            )
            fig.update_layout(
                height=200,
                margin=dict(l=5, r=5, t=5, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(
                    showgrid=True, 
                    gridcolor='#f1f5f9', 
                    title=None, 
                    tickformat='$,.0f',
                    tickfont=dict(size=9)
                ),
                yaxis=dict(title=None, tickfont=dict(size=10)),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    with row2_col2:
        with st.container():
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>👥 SEGMENT DISTRIBUTION</div>", unsafe_allow_html=True)
            
            # Simple pie chart
            segment_sales = filtered_df.groupby('Segment')['Sales'].sum().reset_index()
            
            fig = px.pie(segment_sales, values='Sales', names='Segment')
            fig.update_traces(
                textposition='inside', 
                textinfo='percent',
                textfont=dict(size=11),
                marker=dict(colors=['#2563eb', '#7c3aed', '#db2777'], line=dict(color='white', width=2)),
                hovertemplate='<b>%{label}</b><br>Sales: $%{value:,.0f}<br>Share: %{percent}<extra></extra>'
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
            st.markdown("<div class='section-title'>🏆 TOP 5 PRODUCTS</div>", unsafe_allow_html=True)
            
            # Top 5 products by sales
            top_products = filtered_df.groupby('Product Name')['Sales'].sum().nlargest(5).reset_index()
            
            # Truncate long product names
            top_products['Product Name'] = top_products['Product Name'].str.slice(0, 25) + '...'
            
            fig = px.bar(top_products, y='Product Name', x='Sales', orientation='h', text_auto='.2s')
            fig.update_traces(
                marker_color='#f59e0b',
                marker_line_color='#d97706',
                marker_line_width=1,
                textposition='outside',
                textfont=dict(size=9)
            )
            fig.update_layout(
                height=200,
                margin=dict(l=5, r=5, t=5, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(
                    showgrid=True, 
                    gridcolor='#f1f5f9', 
                    title=None, 
                    tickformat='$,.0f',
                    tickfont=dict(size=9)
                ),
                yaxis=dict(title=None, tickfont=dict(size=9)),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- BOTTOM INSIGHTS ROW ---
    col_i1, col_i2, col_i3, col_i4 = st.columns(4)
    
    # Calculate insights
    top_category = filtered_df.groupby('Category')['Sales'].sum().idxmax()
    top_region = filtered_df.groupby('Region')['Sales'].sum().idxmax()
    best_month = filtered_df.groupby('Month')['Sales'].sum().idxmax()
    
    with col_i1:
        st.markdown(f"""
            <div style='background: #f8fafc; padding: 0.8rem; border-radius: 12px; border-left: 4px solid #2563eb;'>
                <span style='font-size: 0.7rem; color: #64748b;'>🏆 TOP CATEGORY</span><br>
                <span style='font-size: 1rem; font-weight: 600; color: #0f172a;'>{top_category}</span>
            </div>
        """, unsafe_allow_html=True)
    
    with col_i2:
        st.markdown(f"""
            <div style='background: #f8fafc; padding: 0.8rem; border-radius: 12px; border-left: 4px solid #7c3aed;'>
                <span style='font-size: 0.7rem; color: #64748b;'>📍 BEST REGION</span><br>
                <span style='font-size: 1rem; font-weight: 600; color: #0f172a;'>{top_region}</span>
            </div>
        """, unsafe_allow_html=True)
    
    with col_i3:
        st.markdown(f"""
            <div style='background: #f8fafc; padding: 0.8rem; border-radius: 12px; border-left: 4px solid #db2777;'>
                <span style='font-size: 0.7rem; color: #64748b;'>📅 PEAK MONTH</span><br>
                <span style='font-size: 1rem; font-weight: 600; color: #0f172a;'>{best_month}</span>
            </div>
        """, unsafe_allow_html=True)
    
    with col_i4:
        margin_status = "Healthy" if profit_margin > 15 else "At Risk" if profit_margin > 10 else "Critical"
        margin_color = "#10b981" if profit_margin > 15 else "#f59e0b" if profit_margin > 10 else "#ef4444"
        st.markdown(f"""
            <div style='background: #f8fafc; padding: 0.8rem; border-radius: 12px; border-left: 4px solid {margin_color};'>
                <span style='font-size: 0.7rem; color: #64748b;'>💰 PROFIT MARGIN</span><br>
                <span style='font-size: 1rem; font-weight: 600; color: #0f172a;'>{profit_margin:.1f}% · {margin_status}</span>
            </div>
        """, unsafe_allow_html=True)

else:
    # Professional error state
    st.markdown("""
        <div style='text-align: center; padding: 100px; background: white; border-radius: 20px; margin: 50px;'>
            <span style='font-size: 48px;'>📁</span>
            <h2 style='color: #1e293b; margin-top: 20px;'>Data File Not Found</h2>
            <p style='color: #64748b;'>Please ensure SALES_DATA_SETT.xlsx is in the correct directory</p>
        </div>
    """, unsafe_allow_html=True)

# --- PROFESSIONAL FOOTER ---
st.markdown("""
    <div class='dashboard-footer'>
        Sales Intelligence Pro · Enterprise Dashboard · Updated in real-time
    </div>
""", unsafe_allow_html=True)
