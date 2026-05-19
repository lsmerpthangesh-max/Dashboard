import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import io

st.set_page_config(page_title="Lingam Supermarket", layout="wide", page_icon="🛒")

st.title("🛒 Lingam Supermarket Analytics Dashboard")
st.markdown("### Upload Excel → View Full Report")

# File Upload
uploaded_file = st.file_uploader("📤 Upload Your Sales Excel File", type=["xlsx", "xls"])

if uploaded_file:
    with st.spinner("Processing your data..."):
        df = pd.read_excel(uploaded_file)
        
        # Data Cleaning
        df.columns = [str(col).strip().lower().replace(" ", "_") for col in df.columns]
        
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df = df.dropna(subset=['date'])
        
        # Convert numeric columns
        for col in ['quantity', 'price', 'total_amount']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        if 'total_amount' not in df.columns and 'quantity' in df.columns and 'price' in df.columns:
            df['total_amount'] = df['quantity'] * df['price']
        
        df = df.dropna(subset=['total_amount']).copy()
    
    st.success(f"✅ Data Loaded Successfully! ({len(df)} records)")

    # ==================== FILTERS ====================
    st.sidebar.header("🔍 Filters")
    if 'date' in df.columns:
        min_date = df['date'].min().date()
        max_date = df['date'].max().date()
        date_range = st.sidebar.date_input("Date Range", [min_date, max_date])
        filtered_df = df[(df['date'].dt.date >= date_range[0]) & (df['date'].dt.date <= date_range[1])]
    else:
        filtered_df = df

    # ==================== KPI CARDS ====================
    col1, col2, col3, col4 = st.columns(4)
    total_sales = filtered_df['total_amount'].sum()
    total_qty = filtered_df.get('quantity', pd.Series(0)).sum()
    total_bills = len(filtered_df)
    avg_bill = total_sales / total_bills if total_bills > 0 else 0

    col1.metric("💰 Total Sales", f"₹{total_sales:,.0f}")
    col2.metric("📦 Quantity Sold", f"{total_qty:,.0f}")
    col3.metric("🧾 Total Bills", f"{total_bills:,}")
    col4.metric("📈 Avg Bill Value", f"₹{avg_bill:.2f}")

    # ==================== TOP SALES & CHARTS ====================
    tab1, tab2, tab3 = st.tabs(["📈 Sales Trend", "🏆 Top Products", "📊 Category Analysis"])

    with tab1:
        if 'date' in filtered_df.columns:
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
        if 'payment_mode' in filtered_df.columns:
            st.plotly_chart(px.pie(filtered_df, names='payment_mode', values='total_amount', title="Payment Mode"), use_container_width=True)

    # ==================== DOWNLOAD REPORT ====================
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        filtered_df.to_excel(writer, index=False, sheet_name='Sales_Report')
    output.seek(0)

    st.download_button(
        label="📥 Download Full Report (Excel)",
        data=output,
        file_name=f"lingam_sales_report_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

else:
    st.info("👆 Please upload your sales Excel file to see the full dashboard")
    st.markdown("**Tip:** Use the sample file I gave you earlier.")
