import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import io

st.set_page_config(page_title="Lingam Supermarket", layout="wide", page_icon="🛒")

st.title("🛒 Lingam Supermarket Analytics Dashboard")
st.markdown("### Professional Sales & Inventory Report")

# ====================== FILE UPLOAD ======================
uploaded_file = st.file_uploader("📤 Upload Your Sales Excel File", type=["xlsx", "xls"])

if uploaded_file:
    with st.spinner("Processing your data..."):
        df = pd.read_excel(uploaded_file)
        
        # Data Cleaning
        df.columns = [str(col).strip().lower().replace(" ", "_") for col in df.columns]
        
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df = df.dropna(subset=['date'])
        
        for col in ['quantity', 'price', 'total_amount']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        if 'total_amount' not in df.columns and 'quantity' in df.columns and 'price' in df.columns:
            df['total_amount'] = df['quantity'] * df['price']
        
        df = df.dropna(subset=['total_amount']).copy()
    
    st.success(f"✅ Data Loaded Successfully! ({len(df)} records)")

    # ====================== FILTERS ======================
    st.sidebar.header("🔍 Filters")
    if 'date' in df.columns:
        min_date = df['date'].min().date()
        max_date = df['date'].max().date()
        date_range = st.sidebar.date_input("Date Range", [min_date, max_date])
        filtered_df = df[(df['date'].dt.date >= date_range[0]) & (df['date'].dt.date <= date_range[1])]
    else:
        filtered_df = df

    # ====================== KPI CARDS ======================
    col1, col2, col3, col4 = st.columns(4)
    total_sales = filtered_df['total_amount'].sum()
    total_qty = filtered_df.get('quantity', pd.Series(0)).sum()
    total_bills = len(filtered_df)
    avg_bill = total_sales / total_bills if total_bills > 0 else 0

    col1.metric("💰 Total Sales", f"₹{total_sales:,.0f}")
    col2.metric("📦 Quantity Sold", f"{total_qty:,.0f}")
    col3.metric("🧾 Total Bills", f"{total_bills:,}")
    col4.metric("📈 Avg Bill", f"₹{avg_bill:.2f}")

    # ====================== TABS ======================
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Sales Trend", "🏆 Product Performance", "📊 Category & Payment", "📦 Inventory Insights"])

    with tab1:
        if 'date' in filtered_df.columns:
            daily = filtered_df.groupby('date')['total_amount'].sum().reset_index()
            st.plotly_chart(px.line(daily, x='date', y='total_amount', title="Daily Sales Trend"), use_container_width=True)

    with tab2:  # Product Performance
        st.subheader("Top & Least Selling Products")
        col_a, col_b = st.columns(2)
        
        with col_a:
            top10 = filtered_df.groupby('product_name')['total_amount'].sum().nlargest(10).reset_index()
            st.plotly_chart(px.bar(top10, x='total_amount', y='product_name', orientation='h', 
                                  title="Highest Revenue Products (Top 10)"), use_container_width=True)
        
        with col_b:
            least10 = filtered_df.groupby('product_name')['total_amount'].sum().nsmallest(10).reset_index()
            st.plotly_chart(px.bar(least10, x='total_amount', y='product_name', orientation='h', 
                                  title="Least Selling Products"), use_container_width=True)
        
        st.subheader("Most Sold by Quantity")
        top_qty = filtered_df.groupby('product_name')['quantity'].sum().nlargest(10).reset_index()
        st.plotly_chart(px.bar(top_qty, x='quantity', y='product_name', orientation='h', 
                              title="Top 10 Products by Quantity Sold"), use_container_width=True)

    with tab3:  # Category & Payment
        c1, c2 = st.columns(2)
        with c1:
            if 'category' in filtered_df.columns:
                cat = filtered_df.groupby('category')['total_amount'].sum().reset_index()
                st.plotly_chart(px.bar(cat, x='category', y='total_amount', title="Sales by Category"), use_container_width=True)
        with c2:
            if 'payment_mode' in filtered_df.columns:
                st.plotly_chart(px.pie(filtered_df, names='payment_mode', values='total_amount', 
                                     title="Payment Mode Distribution"), use_container_width=True)

    with tab4:  # Inventory Insights
        st.subheader("📦 Inventory Insights")
        
        # For demo - assuming you will add inventory data later
        if 'product_name' in filtered_df.columns:
            stock_summary = filtered_df.groupby('product_name').agg({
                'quantity': 'sum',
                'total_amount': 'sum'
            }).reset_index()
            stock_summary = stock_summary.rename(columns={'quantity': 'Total_Sold'})
            
            st.dataframe(stock_summary, use_container_width=True)
            
            # Low Stock Alert (Demo)
            st.subheader("⚠️ Low Stock Alert")
            low_stock = stock_summary[stock_summary['Total_Sold'] > 50]  # Example threshold
            if not low_stock.empty:
                st.warning("Following products have high movement - Consider restocking:")
                st.dataframe(low_stock)
            else:
                st.info("No critical low stock detected in this period.")
        
        st.info("💡 Tip: Upload a separate Inventory sheet with Current Stock for better alerts.")

    # ====================== DOWNLOAD REPORT ======================
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        filtered_df.to_excel(writer, index=False, sheet_name='Sales_Report')
    output.seek(0)

    st.download_button(
        label="📥 Download Full Report (Excel)",
        data=output,
        file_name=f"lingam_full_report_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

else:
    st.info("👆 Please upload your sales Excel file to see the complete dashboard")
