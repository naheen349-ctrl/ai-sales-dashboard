import streamlit as st
import pandas as pd
from analysis import *
from dashboard import *

# Page config for laptop screen
st.set_page_config(
    page_title="Superstore Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ultra-compact CSS to maximize space
st.markdown("""
    <style>
        /* Reduce all padding and margins */
        .block-container {
            padding-top: 0.5rem;
            padding-bottom: 0rem;
            padding-left: 1rem;
            padding-right: 1rem;
            max-width: 100%;
        }
        div[data-testid="column"] {
            padding: 0 3px;
        }
        div[data-testid="stHorizontalBlock"] {
            gap: 0.5rem;
        }
        .stMetric {
            background-color: #f0f2f6;
            padding: 8px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stMetric label {
            font-size: 0.8rem !important;
            font-weight: 600 !important;
        }
        .stMetric div {
            font-size: 1.3rem !important;
            font-weight: 700 !important;
        }
        h1 {
            font-size: 1.8rem !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        h3 {
            font-size: 1rem !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        .element-container {
            margin: 0 !important;
        }
        hr {
            margin: 0.3rem 0 !important;
        }
        div[data-testid="stMarkdownContainer"] {
            font-size: 0.9rem;
        }
        .stRadio div {
            gap: 0.2rem !important;
        }
        .stMultiSelect div {
            font-size: 0.8rem;
        }
        .stButton button {
            font-size: 0.8rem;
            padding: 0.2rem 0.5rem;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("# 📊 SUPERSTORE SALES DASHBOARD")

# Load data
@st.cache_data
def load_data_cached():
    return load_data()

try:
    df = load_data_cached()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# === TOP ROW: 5 KPIs ===
st.markdown("### 📈 Key Metrics")
kpi_cols = st.columns(5)

# Get KPI metrics
metrics = get_kpi_metrics(df)

with kpi_cols[0]:
    st.metric("Total Sales", f"${metrics['total_sales']:,.0f}")

with kpi_cols[1]:
    delta_color = "inverse" if metrics['total_profit'] < 0 else "normal"
    st.metric("Total Profit", f"${metrics['total_profit']:,.0f}", 
              delta=f"{metrics['total_profit']:,.0f}", 
              delta_color=delta_color)

with kpi_cols[2]:
    st.metric("Total Orders", f"{metrics['total_orders']}")

with kpi_cols[3]:
    st.metric("Avg Margin", f"{metrics['avg_profit_margin']:.1f}%")

with kpi_cols[4]:
    st.metric("Loss Making", f"{metrics['loss_count']} products", 
              delta="⚠️" if metrics['loss_count'] > 0 else "✅", 
              delta_color="inverse")

st.markdown("---")

# === MAIN GRID: 3 columns for filters + 4 visuals ===
col1, col2, col3 = st.columns([1.2, 1.4, 1.4])

# Column 1: FILTERS PANEL
with col1:
    st.markdown("### 🔍 Filters")
    
    # Initialize session state for filters if not exists
    if 'apply_filter' not in st.session_state:
        st.session_state.apply_filter = False
    
    # Category filter
    selected_categories = st.multiselect(
        "Category",
        options=df['Category'].unique(),
        default=list(df['Category'].unique()),
        key="cat_filter"
    )
    
    # Profit status filter
    profit_filter = st.radio(
        "Profit Status",
        options=["All", "Loss Making", "Profitable"],
        horizontal=True,
        key="profit_filter"
    )
    
    # Region filter
    selected_regions = st.multiselect(
        "Region",
        options=df['Region'].unique(),
        default=list(df['Region'].unique()),
        key="region_filter"
    )
    
    # Ship mode filter
    selected_ship_modes = st.multiselect(
        "Ship Mode",
        options=df['Ship Mode'].unique(),
        default=list(df['Ship Mode'].unique()),
        key="ship_filter"
    )
    
    # Apply filters button
    if st.button("🔄 Apply Filters", use_container_width=True):
        st.session_state.apply_filter = True
    
    # Show filter summary
    st.markdown("---")
    st.markdown(f"**📊 Data Summary**")
    st.markdown(f"Total rows: {len(df)}")
    
    # Reset filters button
    if st.button("🗑️ Reset All Filters", use_container_width=True):
        for key in ['cat_filter', 'region_filter', 'ship_filter']:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.profit_filter = "All"
        st.rerun()

# Apply filters
filtered_df = apply_filters(
    df, 
    selected_categories, 
    selected_regions, 
    selected_ship_modes, 
    profit_filter
)

# Column 2: VISUAL 1 and VISUAL 3
with col2:
    # VISUAL 1: Profit by Sub-Category
    st.markdown("### 📊 Profit by Sub-Category")
    try:
        profit_data = get_profit_by_subcategory(filtered_df)
        if not profit_data.empty:
            fig1 = create_profit_subcategory_chart(profit_data)
            st.plotly_chart(fig1, use_container_width=True, key="viz1")
            
            # Show alert if there are losses
            if any(profit_data['Profit'] < 0):
                loss_value = profit_data[profit_data['Profit'] < 0]['Profit'].sum()
                st.error(f"⚠️ Total Losses: ${abs(loss_value):,.0f}")
        else:
            st.info("No data available for selected filters")
    except Exception as e:
        st.error(f"Error creating chart: {e}")
    
    # VISUAL 3: Top 5 Products
    st.markdown("### 🏆 Top 5 Products")
    try:
        top_products_data = get_top_products(filtered_df, 5)
        if not top_products_data.empty:
            top_products_html = display_top_products(top_products_data)
            st.markdown(top_products_html, unsafe_allow_html=True)
        else:
            st.info("No product data available")
    except Exception as e:
        st.error(f"Error displaying products: {e}")

# Column 3: VISUAL 2 and VISUAL 4
with col3:
    # VISUAL 2: Sales by Category
    st.markdown("### 🥧 Sales by Category")
    try:
        cat_data = get_sales_by_category(filtered_df)
        if not cat_data.empty:
            fig2 = create_sales_category_chart(cat_data)
            st.plotly_chart(fig2, use_container_width=True, key="viz2")
        else:
            st.info("No category data available")
    except Exception as e:
        st.error(f"Error creating chart: {e}")
    
    # VISUAL 4: Profit vs Sales Scatter
    st.markdown("### 📈 Profit vs Sales")
    try:
        scatter_data = get_profit_vs_sales(filtered_df)
        if not scatter_data.empty:
            fig4 = create_profit_vs_sales_scatter(scatter_data)
            st.plotly_chart(fig4, use_container_width=True, key="viz4")
        else:
            st.info("No scatter data available")
    except Exception as e:
        st.error(f"Error creating chart: {e}")

# === BOTTOM ROW: 2 visuals ===
st.markdown("---")
bot_col1, bot_col2 = st.columns(2)

with bot_col1:
    # VISUAL 5: Monthly Sales Trend
    st.markdown("### 📅 Monthly Sales Trend")
    try:
        monthly_data = get_monthly_sales_trend(filtered_df)
        if not monthly_data.empty:
            fig5 = create_monthly_trend_chart(monthly_data)
            st.plotly_chart(fig5, use_container_width=True, key="viz5")
        else:
            st.info("No monthly data available")
    except Exception as e:
        st.error(f"Error creating chart: {e}")

with bot_col2:
    # VISUAL 6: Shipping Delay by Ship Mode
    st.markdown("### 🚚 Shipping Delay by Mode")
    try:
        delay_data = get_shipping_delay_by_mode(filtered_df)
        if not delay_data.empty:
            fig6 = create_shipping_delay_chart(delay_data)
            st.plotly_chart(fig6, use_container_width=True, key="viz6")
        else:
            st.info("No shipping data available")
    except Exception as e:
        st.error(f"Error creating chart: {e}")

# Footer with filter info
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.caption(f"📊 Showing {len(filtered_df)} of {len(df)} rows")
with col2:
    if not filtered_df.empty:
        st.caption(f"💰 Sales: ${filtered_df['Sales'].sum():,.0f} | Profit: ${filtered_df['Profit'].sum():,.0f}")
with col3:
    st.caption("🔄 Filters active" if len(filtered_df) < len(df) else "📋 No filters active")

# Debug section (commented out - remove in production)
# with st.expander("🔧 Debug Info"):
#     st.write("Selected Categories:", selected_categories)
#     st.write("Selected Regions:", selected_regions)
#     st.write("Selected Ship Modes:", selected_ship_modes)
#     st.write("Profit Filter:", profit_filter)
#     st.write("Original df shape:", df.shape)
#     st.write("Filtered df shape:", filtered_df.shape)
