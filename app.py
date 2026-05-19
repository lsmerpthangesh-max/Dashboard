import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Lingam Supermarket", layout="wide", page_icon="🛒")

st.title("🛒 Lingam Supermarket - Analytics Dashboard")
st.markdown("### Upload Excel → Get Professional Report")

# File Upload
uploaded_file = st.file_uploader("Upload Your Sales Excel File", type=["xlsx", "xls"])

if uploaded_file:
    with st.spinner("Processing your data... Please wait"):
        # Read Excel
        df = pd.read_excel(uploaded_file)
        
        # Data Cleaning
        df.columns = [str(col).strip().lower().replace(" ", "_") for col in df.columns]
        
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df = df.dropna(subset=['date'])
            df['month'] = df['date'].dt.strftime('%Y-%m')
        
        # Convert numeric columns
        for col in ['quantity', 'price', 'total_amount']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        if 'total_amount' not in df.columns and 'quantity' in df.columns and 'price' in df.columns:
            df['total_amount'] = df['quantity'] * df['price']
        
        df = df.dropna(subset=['total_amount'])
    
    # ==================== FILTERS ====================
    st.sidebar.header("🔍 Filters")
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    date_range = st.sidebar.date_input("Date Range", [min_date, max_date])
    
    category_filter = st.sidebar.multiselect("Category", 
                        options=df['category'].dropna().unique()) if 'category' in df.columns else []
    
    # Apply Filters
    mask = (df['date'].dt.date >= date_range[0]) & (df['date'].dt.date <= date_range[1])
    if category_filter:
        mask = mask & df['category'].isin(category_filter)
    filtered_df = df[mask].copy()
    
    # ==================== KPI CARDS ====================
    st.subheader("📊 Key Performance Indicators")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Sales", f"₹{filtered_df['total_amount'].sum():,.0f}")
    c2.metric("Total Quantity", f"{filtered_df['quantity'].sum():,.0f}" if 'quantity' in filtered_df.columns else "N/A")
    c3.metric("Total Bills", f"{filtered_df.shape[0]:,}")
    c4.metric("Avg Bill Value", f"₹{filtered_df['total_amount'].mean():.2f}")
    
    # ==================== CHARTS ====================
    tab1, tab2, tab3 = st.tabs(["Sales Trend", "Top Products", "Category Analysis"])
    
    with tab1:
        daily = filtered_df.groupby('date')['total_amount'].sum().reset_index()
        st.plotly_chart(px.line(daily, x='date', y='total_amount', title="Daily Sales Trend"), use_container_width=True)
    
    with tab2:
        top10 = filtered_df.groupby('product_name')['total_amount'].sum().nlargest(10).reset_index()
        st.plotly_chart(px.bar(top10, x='total_amount', y='product_name', 
                              orientation='h', title="Top 10 Selling Products"), use_container_width=True)
    
    with tab3:
        if 'category' in filtered_df.columns:
            cat = filtered_df.groupby('category')['total_amount'].sum().reset_index()
            st.plotly_chart(px.bar(cat, x='category', y='total_amount', title="Sales by Category"), use_container_width=True)
    
    # ==================== DOWNLOAD REPORT ====================
    st.success("✅ Dashboard Ready!")
    csv = filtered_df.to_excel(index=False)
    st.download_button(
        label="📥 Download Full Report (Excel)",
        data=csv,
        file_name=f"lingam_sales_report_{datetime.now().strftime('%Y%m%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

else:
    st.info("👆 Please upload your sales Excel file to generate the dashboard.")
