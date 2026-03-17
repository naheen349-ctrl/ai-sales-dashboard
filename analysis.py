import pandas as pd
import numpy as np

def load_data():
    """Load and prepare the dataset"""
    # Load the Excel file
    df = pd.read_excel('SALES_DATA_SETT.xlsx')
    
    # Convert date columns
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d-%m-%Y')
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d-%m-%Y')
    
    # Create useful columns for analysis
    df['Order Month'] = df['Order Date'].dt.strftime('%Y-%m')
    df['Order Year'] = df['Order Date'].dt.year
    df['Order Quarter'] = df['Order Date'].dt.quarter
    df['Year-Month'] = df['Order Date'].dt.strftime('%Y-%m')
    
    return df

def get_kpi_metrics(df):
    """Calculate all KPI metrics"""
    metrics = {
        'total_sales': df['Sales'].sum(),
        'total_profit': df['Profit'].sum(),
        'total_orders': df['Order ID'].nunique(),
        'avg_profit_margin': df['profit margin'].mean(),
        'loss_count': len(df[df['Profit'] < 0])
    }
    return metrics

def get_profit_by_subcategory(df):
    """Calculate profit by sub-category"""
    return df.groupby('Sub-Category')['Profit'].sum().reset_index().sort_values('Profit')

def get_sales_by_category(df):
    """Calculate sales by category"""
    return df.groupby('Category')['Sales'].sum().reset_index()

def get_top_products(df, n=5):
    """Get top N products by sales with profit info"""
    return df.groupby('Product Name').agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).sort_values('Sales', ascending=False).head(n).reset_index()

def get_profit_vs_sales(df):
    """Get profit vs sales scatter data"""
    return df.groupby('Product Name').agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()

def get_monthly_sales_trend(df):
    """Get monthly sales trend"""
    monthly = df.groupby('Year-Month')['Sales'].sum().reset_index()
    return monthly.sort_values('Year-Month')

def get_shipping_delay_by_mode(df):
    """Get average shipping delay by ship mode"""
    return df.groupby('Ship Mode')['shipping_delay_days'].mean().reset_index()

def apply_filters(df, categories, regions, ship_modes, profit_filter):
    """Apply all filters to dataframe"""
    filtered_df = df.copy()
    
    # Apply category filter
    if categories and len(categories) > 0:
        filtered_df = filtered_df[filtered_df['Category'].isin(categories)]
    
    # Apply region filter
    if regions and len(regions) > 0:
        filtered_df = filtered_df[filtered_df['Region'].isin(regions)]
    
    # Apply ship mode filter
    if ship_modes and len(ship_modes) > 0:
        filtered_df = filtered_df[filtered_df['Ship Mode'].isin(ship_modes)]
    
    # Apply profit filter
    if profit_filter == "Loss Making":
        filtered_df = filtered_df[filtered_df['Profit'] < 0]
    elif profit_filter == "Profitable":
        filtered_df = filtered_df[filtered_df['Profit'] > 0]
    
    return filtered_df
