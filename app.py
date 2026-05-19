import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Lingam Supermarket", layout="wide", page_icon="🛒")

st.title("🛒 Lingam Supermarket Analytics Dashboard")
st.markdown("### Professional Sales Report Generator")

# File Upload
uploaded_file = st.file_uploader("📁 Upload Your Sales Excel File", type=["xlsx", "xls"])

if uploaded_file is not None:
    with st.spinner("🔄 Processing your sales data..."):
        try:
            # Read the Excel file
            df = pd.read_excel(uploaded_file)
            
            # Clean column names
            df.columns = [str(col).strip().lower().replace(" ", "_").replace(".", "") for col in df.columns]
            
            # Handle Date
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'], errors='coerce')
                df = df.dropna(subset=['date'])
                df['month'] = df['date'].dt.strftime('%Y-%m')
            
            # Convert numeric columns
            for col in ['quantity', 'price', 'total_amount']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Create Total Amount if missing
            if 'total_amount' not in df.columns and 'quantity' in df.columns and 'price' in df.columns:
                df['total_amount'] = df['quantity'] * df['price']
            
            df = df.dropna(subset=['total_amount'])
            
            st.success("✅ Data Loaded Successfully!")
            
        except Exception as e:
            st.error(f"Error reading file: {e}")
            st.stop()
    
    # ==================== SIDEBAR FILTERS ====================
    st.sidebar.header("🔍 Filters")
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])
    
    # Apply Date Filter
    filtered_df = df[(df['date'].dt.date >= date_range[0]) & (df['date'].dt.date <= date_range[1])]
    
    # ==================== KPI CARDS ====================
    st.subheader("📊 Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    total_sales = filtered_df['total_amount'].sum()
    total_qty = filtered_df['quantity'].sum() if 'quantity' in filtered_df.columns else 0
    total_bills = len(filtered_df)
    avg_bill = total_sales / total_bills if total_bills > 0 else 0
    
    col1.metric("💰 Total Sales", f"₹{total_sales:,.0f}")
    col2.metric("📦 Quantity Sold", f"{total_qty:,.0f}")
    col3.metric("🧾 Total Bills", f"{total_bills:,}")
    col4.metric("📈 Avg Bill Value", f"₹{avg_bill:.2f}")
    
    # ==================== CHARTS ====================
    tab1, tab2, tab3 = st.tabs(["📈 Sales Trend", "🏆 Top Products", "📊 Category Analysis"])
    
    with tab1:
        daily_sales = filtered_df.groupby('date')['total_amount'].sum().reset_index()
        fig1 = px.line(daily_sales, x='date', y='total_amount', title="Daily Sales Trend")
        st.plotly_chart(fig1, use_container_width=True)
    
    with tab2:
        top_products = filtered_df.groupby('product_name')['total_amount'].sum().nlargest(10).reset_index()
        fig2 = px.bar(top_products, x='total_amount', y='product_name', 
                     orientation='h', title="Top 10 Selling Products")
        st.plotly_chart(fig2, use_container_width=True)
    
    with tab3:
        if 'category' in filtered_df.columns:
            category_sales = filtered_df.groupby('category')['total_amount'].sum().reset_index()
            fig3 = px.bar(category_sales, x='category', y='total_amount', title="Sales by Category")
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("Category column not found in your data")
    
    # ==================== DOWNLOAD REPORT ====================
    st.subheader("📥 Download Report")
    excel_data = filtered_df.to_excel(index=False)
    st.download_button(
        label="📥 Download Complete Sales Report (Excel)",
        data=excel_data,
        file_name=f"lingam_supermarket_report_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

else:
    st.info("👆 Please upload your sales Excel file to generate the dashboard.")
    st.markdown("""
    **Expected Columns:**  
    `Date, Bill Number, Product Name, Category, Quantity, Price, Total Amount, Payment Mode, Customer Type`
    """)
