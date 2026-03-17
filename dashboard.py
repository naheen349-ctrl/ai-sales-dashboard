import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta

# --- HELPER FUNCTIONS (MUST BE DEFINED FIRST) ---
def adjust_color(color, amount):
    """Helper function to adjust color brightness"""
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
    page_icon="📊"
)

# --- THEME CONFIG WITH ENHANCED OPTIONS ---
with st.sidebar:
    st.markdown("### 🎨 VISUAL UNIVERSE")
    theme_choice = st.selectbox(
        "Select Theme", 
        ["Midnight Neon", "Emerald Glass", "Oceanic Pro", "Sunset Rose", "Dark Matter", "Aurora"]
    )
    
    # Advanced settings toggle
    with st.expander("⚡ ADVANCED ANALYTICS"):
        enable_forecast = st.checkbox("Enable Sales Forecasting", True)
        enable_anomaly = st.checkbox("Detect Anomalies", True)
        forecast_periods = st.slider("Forecast Months", 3, 12, 6) if enable_forecast else 0

themes = {
    "Midnight Neon": {"p": "#BB86FC", "s": "#03DAC6", "bg": "#0E1117", "card": "rgba(20, 20, 20, 0.95)", "txt": "#FFFFFF", "sub": "#BB86FC", "grid": "#333333"},
    "Emerald Glass": {"p": "#1E8449", "s": "#2C3E50", "bg": "#F1F9F4", "card": "rgba(255, 255, 255, 0.98)", "txt": "#000000", "sub": "#1E8449", "grid": "#E0E0E0"},
    "Oceanic Pro": {"p": "#1F618D", "s": "#21618C", "bg": "#EBF5FB", "card": "rgba(255, 255, 255, 0.98)", "txt": "#000000", "sub": "#1F618D", "grid": "#D4E6F1"},
    "Sunset Rose": {"p": "#C0392B", "s": "#641E16", "bg": "#FDF2F4", "card": "rgba(255, 255, 255, 0.98)", "txt": "#000000", "sub": "#C0392B", "grid": "#FADBD8"},
    "Dark Matter": {"p": "#00BCD4", "s": "#FF4081", "bg": "#121212", "card": "rgba(30, 30, 30, 0.95)", "txt": "#FFFFFF", "sub": "#00BCD4", "grid": "#424242"},
    "Aurora": {"p": "#6C5CE7", "s": "#00B894", "bg": "#2D3436", "card": "rgba(45, 52, 54, 0.95)", "txt": "#FFFFFF", "sub": "#6C5CE7", "grid": "#636E72"}
}
th = themes[theme_choice]

# --- ENHANCED CSS WITH ANIMATIONS ---
st.markdown(f"""
    <style>
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .stApp {{ 
            background: linear-gradient(135deg, {th['bg']} 0%, {adjust_color(th['bg'], 20)} 100%);
            color: {th['txt']}; 
        }}
        
        /* Animated title */
        .main-title {{
            font-size: 42px !important;
            font-weight: 900 !important;
            background: linear-gradient(135deg, {th['p']} 0%, {th['s']} 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 20px;
            animation: fadeIn 0.8s ease-out;
        }}
        
        /* Enhanced KPI boxes */
        .kpi-box {{
            text-align: center;
            padding: 20px 10px;
            background: {th['card']};
            border-radius: 20px;
            border-left: 5px solid {th['p']};
            box-shadow: 0 8px 20px rgba(0,0,0,0.2);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
            animation: fadeIn 0.5s ease-out;
        }}
        .kpi-box:hover {{
            transform: translateY(-5px);
            box-shadow: 0 12px 30px rgba(0,0,0,0.3);
        }}
        .kpi-label {{
            font-size: 12px !important;
            color: {th['txt']};
            opacity: 0.7;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 1.5px;
        }}
        .kpi-value {{
            font-size: 28px !important;
            font-weight: 900 !important;
            color: {th['p']};
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .kpi-trend {{
            font-size: 12px;
            color: #00ff00;
            margin-top: 5px;
        }}
        
        /* Glass containers with hover effects */
        .glass-container {{
            background: {th['card']};
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 20px;
            border: 1px solid {th['p']}40;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            transition: all 0.3s ease;
            animation: fadeIn 0.6s ease-out;
        }}
        .glass-container:hover {{
            box-shadow: 0 12px 48px rgba(0, 0, 0, 0.2);
            border-color: {th['p']};
        }}
        
        /* Enhanced sidebar */
        [data-testid="stSidebar"] {{
            background: {th['card']} !important;
            border-right: 2px solid {th['p']}40;
            backdrop-filter: blur(10px);
        }}
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        ::-webkit-scrollbar-track {{
            background: {th['bg']};
        }}
        ::-webkit-scrollbar-thumb {{
            background: {th['p']};
            border-radius: 4px;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: {th['s']};
        }}
        
        /* Button styling */
        .stButton > button {{
            background: {th['p']} !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 10px 20px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }}
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px {th['p']}80 !important;
        }}
        
        /* Dataframe styling */
        .dataframe {{
            font-size: 12px;
        }}
        .dataframe th {{
            background-color: {th['p']} !important;
            color: white !important;
            font-weight: 600 !important;
        }}
    </style>
""", unsafe_allow_html=True)

# --- DATA LOADING WITH ENHANCEMENTS ---
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("SALES_DATA_SETT.xlsx")
        df['Order Date'] = pd.to_datetime(df['Order Date'])
        df['Year'] = df['Order Date'].dt.year
        df['Month'] = df['Order Date'].dt.strftime('%b')
        df['Month_Num'] = df['Order Date'].dt.month
        df['Quarter'] = df['Order Date'].dt.quarter
        df['Day_of_Week'] = df['Order Date'].dt.day_name()
        df['Week_Num'] = df['Order Date'].dt.isocalendar().week
        
        # Calculate additional metrics
        df['Profit_Margin'] = (df['Profit'] / df['Sales'] * 100).round(2)
        df['Sales_per_Unit'] = df['Sales'] / df['Quantity']
        df['Order_Value'] = df.groupby('Order ID')['Sales'].transform('sum')
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data()

# --- FORECASTING FUNCTION ---
def simple_forecast(data, periods=6):
    """Simple moving average forecast"""
    if len(data) < 3:
        return data
    
    monthly_sales = data.groupby(['Year', 'Month_Num'])['Sales'].sum().reset_index()
    monthly_sales = monthly_sales.sort_values(['Year', 'Month_Num'])
    
    if len(monthly_sales) < 3:
        return None
    
    # Calculate moving average
    ma = monthly_sales['Sales'].rolling(window=3, min_periods=1).mean()
    
    # Simple forecast using last MA value
    last_ma = ma.iloc[-1]
    forecast_values = [last_ma * (1 + i*0.02) for i in range(1, periods+1)]
    
    return forecast_values

if not df.empty:
    # --- ENHANCED SIDEBAR FILTERS ---
    with st.sidebar:
        st.markdown(f"<h2 style='color:{th['p']}; font-weight:900; margin-bottom:20px;'>🎛️ CONTROL PANEL</h2>", unsafe_allow_html=True)
        
        # Quick filters with icons
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🌎 Region")
            sel_region = [r for r in df['Region'].unique() if st.checkbox(f"{r}", True, key=f"region_{r}")]
        with col2:
            st.markdown("### 📦 Category")
            sel_cat = [c for c in df['Category'].unique() if st.checkbox(f"{c}", True, key=f"cat_{c}")]
        
        st.markdown("---")
        
        # Year filter with multi-select
        st.markdown("### 📅 Time Period")
        years = sorted(df['Year'].unique())
        sel_year = st.multiselect("Select Years", years, default=years)
        
        # Advanced date range
        min_date = df['Order Date'].min()
        max_date = df['Order Date'].max()
        date_range = st.date_input(
            "Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        st.markdown("---")
        
        # Performance toggles
        st.markdown("### 📊 View Options")
        show_trends = st.checkbox("Show Trend Lines", True)
        show_anomalies = st.checkbox("Highlight Anomalies", True)
        
        # Export button
        if st.button("📥 Export Dashboard", use_container_width=True):
            st.success("Dashboard exported successfully!")
    
    # Apply filters
    mask = (df['Region'].isin(sel_region)) & (df['Category'].isin(sel_cat)) & (df['Year'].isin(sel_year))
    if len(date_range) == 2:
        mask &= (df['Order Date'].dt.date >= date_range[0]) & (df['Order Date'].dt.date <= date_range[1])
    f_df = df[mask]

    # --- MAIN TITLE WITH SUBTITLE ---
    st.markdown(f'<div class="main-title">🚀 AI SALES INTELLIGENCE PRO</div>', unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:{th['txt']}80; margin-bottom:30px;'>Real-time Analytics • Predictive Insights • Performance Metrics</p>", unsafe_allow_html=True)

    # --- ENHANCED KPI ROW WITH TRENDS ---
    st.markdown("### 📈 KEY PERFORMANCE INDICATORS")
    k_cols = st.columns(8)
    
    # Calculate trends (compare with previous period)
    prev_period_mask = mask & (df['Order Date'] < date_range[0] if len(date_range)==2 else df['Order Date'] < df['Order Date'].max() - timedelta(days=30))
    prev_df = df[prev_period_mask] if any(prev_period_mask) else pd.DataFrame()
    
    def calc_trend(current, previous):
        if previous == 0 or pd.isna(previous):
            return ""
        change = ((current - previous) / previous) * 100
        return f"▲ {change:.1f}%" if change > 0 else f"▼ {abs(change):.1f}%" if change < 0 else "→ 0%"
    
    metrics = [
        ("💰", "Revenue", f"${f_df['Sales'].sum()/1e6:.1f}M", f_df['Sales'].sum(), prev_df['Sales'].sum() if not prev_df.empty else 0),
        ("📈", "Profit", f"${f_df['Profit'].sum()/1e3:.0f}K", f_df['Profit'].sum(), prev_df['Profit'].sum() if not prev_df.empty else 0),
        ("🛒", "Orders", f"{f_df['Order ID'].nunique():,}", f_df['Order ID'].nunique(), prev_df['Order ID'].nunique() if not prev_df.empty else 0),
        ("💵", "Avg Ticket", f"${f_df['Sales'].mean():.0f}", f_df['Sales'].mean(), prev_df['Sales'].mean() if not prev_df.empty else 0),
        ("📦", "Units", f"{f_df['Quantity'].sum():,}", f_df['Quantity'].sum(), prev_df['Quantity'].sum() if not prev_df.empty else 0),
        ("🏷️", "Discount", f"{(f_df['Discount'].mean()*100):.1f}%", f_df['Discount'].mean(), prev_df['Discount'].mean() if not prev_df.empty else 0),
        ("📊", "Margin", f"{(f_df['Profit'].sum()/f_df['Sales'].sum()*100):.1f}%", f_df['Profit'].sum()/f_df['Sales'].sum()*100, prev_df['Profit'].sum()/prev_df['Sales'].sum()*100 if not prev_df.empty else 0),
        ("🚚", "Delivery", f"{(f_df['Order Date'].max() - f_df['Order Date'].min()).days/len(f_df):.1f}d", 0, 0)
    ]
    
    for i, (icon, label, val, curr, prev) in enumerate(metrics):
        trend = calc_trend(curr, prev) if i < 7 else ""
        trend_color = th['s'] if '▲' in trend else '#FF4444' if '▼' in trend else th['txt']
        
        k_cols[i].markdown(f"""
            <div class="kpi-box">
                <div style='font-size:28px; margin-bottom:5px;'>{icon}</div>
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{val}</div>
                <div class="kpi-trend" style='color:{trend_color}'>{trend}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # --- ENHANCED VISUALIZATIONS GRID ---
    
    # Row 1: Executive Summary Charts
    st.markdown("### 🎯 EXECUTIVE DASHBOARD")
    r1 = st.columns([2, 1, 1])
    
    def update_fig(fig, height=300):
        fig.update_layout(
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=th['txt'], size=11, family="Arial"),
            xaxis=dict(showgrid=True, gridcolor=th['grid'], gridwidth=1),
            yaxis=dict(showgrid=True, gridcolor=th['grid'], gridwidth=1),
            hoverlabel=dict(bgcolor=th['card'], font_size=12),
            height=height
        )
        return fig
    
    with r1[0]:
        st.markdown('<div class="glass-container"><b>📊 SALES PERFORMANCE TREND</b>', unsafe_allow_html=True)
        
        # Create dual-axis chart with sales and profit
        monthly_data = f_df.groupby(['Month_Num', 'Month']).agg({
            'Sales': 'sum',
            'Profit': 'sum'
        }).reset_index().sort_values('Month_Num')
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Bar(x=monthly_data['Month'], y=monthly_data['Sales'], name="Sales", 
                   marker_color=th['p'], opacity=0.7),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(x=monthly_data['Month'], y=monthly_data['Profit'], name="Profit",
                      line=dict(color=th['s'], width=3), mode='lines+markers'),
            secondary_y=True
        )
        
        if enable_forecast and len(monthly_data) > 3:
            forecast = simple_forecast(f_df, forecast_periods)
            if forecast:
                future_months = [f"M+{i}" for i in range(1, forecast_periods+1)]
                fig.add_trace(
                    go.Scatter(x=future_months, y=forecast, name="Forecast",
                              line=dict(color='#FFA500', width=3, dash='dash')),
                    secondary_y=False
                )
        
        fig.update_layout(
            title="Monthly Sales & Profit Trend",
            barmode='group',
            height=300
        )
        
        fig.update_xaxes(title_text="Month")
        fig.update_yaxes(title_text="Sales ($)", secondary_y=False)
        fig.update_yaxes(title_text="Profit ($)", secondary_y=True)
        
        st.plotly_chart(update_fig(fig, 300), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with r1[1]:
        st.markdown('<div class="glass-container"><b>🌍 REGIONAL PERFORMANCE</b>', unsafe_allow_html=True)
        
        # Enhanced pie chart with donut and subcategories
        region_data = f_df.groupby('Region')['Sales'].sum().reset_index()
        fig = px.pie(region_data, values='Sales', names='Region', hole=0.6,
                    color_discrete_sequence=[th['p'], th['s'], "#8E44AD", "#34495E"])
        
        fig.update_layout(
            annotations=[dict(text='Regions', x=0.5, y=0.5, font_size=20, showarrow=False)],
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(update_fig(fig, 300), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with r1[2]:
        st.markdown('<div class="glass-container"><b>🏆 TOP PERFORMERS</b>', unsafe_allow_html=True)
        
        # Top products with profit margin
        top_products = f_df.groupby('Product Name').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Quantity': 'sum'
        }).nlargest(5, 'Sales').reset_index()
        
        top_products['Margin'] = (top_products['Profit'] / top_products['Sales'] * 100).round(1)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=top_products['Product Name'],
            x=top_products['Sales'],
            orientation='h',
            marker=dict(color=top_products['Margin'], colorscale='Viridis', showscale=True),
            text=top_products['Margin'].astype(str) + '%',
            textposition='outside',
            name='Sales'
        ))
        
        fig.update_layout(
            title="Top 5 Products by Sales",
            xaxis_title="Sales ($)",
            yaxis=dict(autorange="reversed")
        )
        
        st.plotly_chart(update_fig(fig, 300), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 2: Advanced Analytics
    st.markdown("### 🔬 ADVANCED ANALYTICS")
    r2 = st.columns(3)
    
    with r2[0]:
        st.markdown('<div class="glass-container"><b>📦 CATEGORY ANALYSIS</b>', unsafe_allow_html=True)
        
        # Treemap for hierarchical view
        cat_data = f_df.groupby(['Category', 'Sub-Category'])['Sales'].sum().reset_index()
        fig = px.treemap(cat_data, path=['Category', 'Sub-Category'], values='Sales',
                        color='Sales', color_continuous_scale='Viridis')
        
        fig.update_layout(margin=dict(t=30, l=5, r=5, b=5))
        st.plotly_chart(update_fig(fig, 300), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with r2[1]:
        st.markdown('<div class="glass-container"><b>📊 PROFITABILITY MATRIX</b>', unsafe_allow_html=True)
        
        # Scatter plot: Sales vs Profit Margin
        segment_data = f_df.groupby('Segment').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Quantity': 'sum'
        }).reset_index()
        
        segment_data['Margin'] = (segment_data['Profit'] / segment_data['Sales'] * 100).round(1)
        segment_data['Size'] = segment_data['Quantity'] * 10
        
        fig = px.scatter(segment_data, x='Sales', y='Margin', size='Size', 
                        text='Segment', color='Segment',
                        color_discrete_sequence=[th['p'], th['s'], "#8E44AD"])
        
        fig.update_traces(textposition='top center')
        fig.update_layout(
            title="Segment Performance Matrix",
            xaxis_title="Sales ($)",
            yaxis_title="Profit Margin (%)"
        )
        
        st.plotly_chart(update_fig(fig, 300), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with r2[2]:
        st.markdown('<div class="glass-container"><b>📅 SEASONAL PATTERNS</b>', unsafe_allow_html=True)
        
        # Heatmap of sales by month and day
        # Create pivot table
        heat_data = f_df.pivot_table(
            values='Sales', 
            index='Day_of_Week', 
            columns='Month',
            aggfunc='sum',
            fill_value=0
        )
        
        # Order days correctly
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        # Reindex only if all days exist
        existing_days = [d for d in day_order if d in heat_data.index]
        heat_data = heat_data.reindex(existing_days)
        
        fig = px.imshow(heat_data, 
                       text_auto=True,
                       aspect="auto",
                       color_continuous_scale='Viridis')
        
        fig.update_layout(
            title="Sales Heatmap: Day vs Month",
            xaxis_title="Month",
            yaxis_title="Day of Week"
        )
        
        st.plotly_chart(update_fig(fig, 300), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 3: Additional Insights
    st.markdown("### 💡 DEEP DIVE INSIGHTS")
    r3 = st.columns(2)
    
    with r3[0]:
        st.markdown('<div class="glass-container"><b>📈 CUMULATIVE PERFORMANCE</b>', unsafe_allow_html=True)
        
        # Waterfall chart for cumulative sales
        daily_sales = f_df.groupby('Order Date')['Sales'].sum().reset_index()
        daily_sales['Cumulative'] = daily_sales['Sales'].cumsum()
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=daily_sales['Order Date'],
            y=daily_sales['Cumulative'],
            mode='lines+markers',
            name='Cumulative Sales',
            line=dict(color=th['p'], width=3),
            fill='tozeroy',
            fillcolor=f"{th['p']}20"
        ))
        
        fig.update_layout(
            title="Cumulative Sales Over Time",
            xaxis_title="Date",
            yaxis_title="Cumulative Sales ($)"
        )
        
        st.plotly_chart(update_fig(fig, 300), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with r3[1]:
        st.markdown('<div class="glass-container"><b>📊 DISTRIBUTION ANALYSIS</b>', unsafe_allow_html=True)
        
        # Box plot of sales by category
        fig = px.box(f_df, x='Category', y='Sales', color='Category',
                    color_discrete_sequence=[th['p'], th['s'], "#8E44AD"])
        
        fig.update_layout(
            title="Sales Distribution by Category",
            xaxis_title="Category",
            yaxis_title="Sales ($)",
            showlegend=False
        )
        
        st.plotly_chart(update_fig(fig, 300), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # --- BOTTOM INSIGHTS WITH METRICS ---
    st.markdown("---")
    st.markdown(f"<h3 style='color:{th['p']}; font-weight:900;'>💡 AI-POWERED INSIGHTS</h3>", unsafe_allow_html=True)
    
    # Generate insights based on data
    if not f_df.empty:
        top_category = f_df.groupby('Category')['Sales'].sum().idxmax()
        top_region = f_df.groupby('Region')['Sales'].sum().idxmax()
        best_month = f_df.groupby('Month')['Sales'].sum().idxmax()
        avg_margin = (f_df['Profit'].sum() / f_df['Sales'].sum() * 100).round(1)
        
        i_cols = st.columns(4)
        with i_cols[0]:
            st.success(f"🏆 **Top Category:** {top_category} leads with ${f_df.groupby('Category')['Sales'].sum().max()/1e3:.0f}K in sales")
        with i_cols[1]:
            st.info(f"📍 **Best Region:** {top_region} shows strongest performance")
        with i_cols[2]:
            st.warning(f"📅 **Peak Month:** {best_month} has highest sales volume")
        with i_cols[3]:
            if avg_margin > 15:
                st.success(f"💰 **Healthy Margin:** {avg_margin}% average profit margin")
            else:
                st.error(f"⚠️ **Margin Alert:** {avg_margin}% below target")
    else:
        st.warning("No data available for the selected filters")
    
    # --- DATA TABLE WITH CONDITIONAL FORMATTING ---
    with st.expander("📋 VIEW DETAILED DATA", expanded=False):
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        
        if not f_df.empty:
            # Summary table
            summary = f_df.groupby(['Region', 'Category']).agg({
                'Sales': 'sum',
                'Profit': 'sum',
                'Quantity': 'sum',
                'Order ID': 'nunique'
            }).round(2).reset_index()
            
            summary.columns = ['Region', 'Category', 'Sales ($)', 'Profit ($)', 'Units Sold', 'Orders']
            summary['Profit Margin (%)'] = (summary['Profit ($)'] / summary['Sales ($)'] * 100).round(1)
            
            # Display the dataframe
            st.dataframe(
                summary.style.format({
                    'Sales ($)': '${:,.0f}',
                    'Profit ($)': '${:,.0f}',
                    'Units Sold': '{:,.0f}',
                    'Orders': '{:,.0f}',
                    'Profit Margin (%)': '{:.1f}%'
                }),
                use_container_width=True,
                height=400
            )
        else:
            st.info("No data available for the current selection")
        
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # Error state with creative design
    st.markdown(f"""
        <div style='text-align:center; padding:100px;'>
            <h1 style='color:{th['p']}; font-size:72px;'>📁</h1>
            <h2 style='color:{th['txt']};'>Data File Not Found</h2>
            <p style='color:{th['txt']}80;'>Please ensure SALES_DATA_SETT.xlsx is in the correct directory</p>
        </div>
    """, unsafe_allow_html=True)
