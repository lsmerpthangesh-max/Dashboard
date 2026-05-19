import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Lingam Supermarket", layout="wide", page_icon="🛒")

st.title("🛒 Lingam Supermarket Analytics")
st.markdown("### Professional Data-Driven Dashboard")

# File Upload
uploaded_file = st.file_uploader("Upload Sales Excel File", type=["xlsx", "xls"], help="Upload your daily sales data")

if uploaded_file:
    with st.spinner("Processing data..."):
        df = pd.read_excel(uploaded_file)
        
        # Auto Data Cleaning
        df.columns = [str(col).strip().lower().replace(" ", "_") for col in df.columns]
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df = df.dropna(subset=['date'])
            df['month'] = df['date'].dt.strftime('%Y-%m')
            df['weekday'] = df['date'].dt.day_name()
        
        numeric_cols = ['quantity', 'price', 'total_amount']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        if 'total_amount' not in df.columns and 'quantity' in df.columns and 'price' in df.columns:
            df['total_amount'] = df['quantity'] * df['price']
        
        df = df.dropna(subset=['total_amount'])
    
    # Filters
    st.sidebar.header("Filters")
    date_range = st.sidebar.date_input("Select Date Range", 
                                       [df['date'].min().date(), df['date'].max().date()])
    
    category_filter = st.sidebar.multiselect("Category", options=sorted(df['category'].dropna().unique())) if 'category' in df.columns else []
    payment_filter = st.sidebar.multiselect("Payment Mode", options=sorted(df['payment_mode'].dropna().unique())) if 'payment_mode' in df.columns else []
    
    # Apply Filters
    mask = (df['date'].dt.date >= date_range[0]) & (df['date'].dt.date <= date_range[1])
    if category_filter:
        mask &= df['category'].isin(category_filter)
    if payment_filter:
        mask &= df['payment_mode'].isin(payment_filter)
    filtered = df[mask].copy()
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("**Total Sales**", f"₹{filtered['total_amount'].sum():,.0f}")
    col2.metric("**Total Quantity**", f"{filtered['quantity'].sum():,.0f}" if 'quantity' in filtered.columns else "N/A")
    col3.metric("**Transactions**", f"{filtered['bill_number'].nunique() if 'bill_number' in filtered.columns else len(filtered):,}")
    col4.metric("**Avg Bill Value**", f"₹{filtered['total_amount'].mean():.2f}")
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Sales Trend", "Product Performance", "Category & Payment", "Customer Insights", "AI Insights"])
    
    with tab1:
        daily = filtered.groupby('date')['total_amount'].sum().reset_index()
        st.plotly_chart(px.line(daily, x='date', y='total_amount', title="Daily Sales Trend"), use_container_width=True)
        
        monthly = filtered.groupby('month')['total_amount'].sum().reset_index()
        st.plotly_chart(px.bar(monthly, x='month', y='total_amount', title="Monthly Sales"), use_container_width=True)
    
    with tab2:
        top10 = filtered.groupby('product_name')['total_amount'].sum().nlargest(10).reset_index()
        st.plotly_chart(px.bar(top10, x='total_amount', y='product_name', orientation='h', title="Top 10 Products"), use_container_width=True)
    
    with tab3:
        c1, c2 = st.columns(2)
        with c1:
            cat_sales = filtered.groupby('category')['total_amount'].sum().reset_index()
            st.plotly_chart(px.bar(cat_sales, x='category', y='total_amount', title="Sales by Category"), use_container_width=True)
        with c2:
            if 'payment_mode' in filtered.columns:
                st.plotly_chart(px.pie(filtered, names='payment_mode', values='total_amount', title="Payment Mode"), use_container_width=True)
    
    with tab4:
        if 'customer_type' in filtered.columns:
            st.plotly_chart(px.pie(filtered, names='customer_type', values='total_amount', title="New vs Regular Customers"), use_container_width=True)
    
    with tab5:
        st.subheader("🤖 Smart Insights & Recommendations")
        top_product = top10.iloc[0]['product_name'] if not top10.empty else ""
        st.success(f"**{top_product}** is your current bestseller!")
        st.info("💡 Recommendation: Review slow-moving items and plan combo offers (Rice + Dal, etc.)")
        st.info("📦 Low stock alert system can be added if you upload inventory data.")
    
    # Download Report
    st.download_button("📥 Download Filtered Report", 
                       data=filtered.to_excel(index=False), 
                       file_name=f"lingam_report_{datetime.now().strftime('%Y%m%d')}.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
else:
    st.info("Please upload your sales Excel file to view the dashboard.")
    st.markdown("**Supported Columns:** Date, Bill Number, Product Name, Category, Quantity, Price, Total Amount, Payment Mode, Customer Type")
