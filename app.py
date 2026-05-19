import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import io

st.set_page_config(page_title="Lingam Supermarket", layout="wide", page_icon="🛒")

st.title("🛒 Lingam Supermarket Analytics Dashboard")
st.markdown("### Professional Sales & Inventory System")

# ====================== FILE UPLOADS ======================
col1, col2 = st.columns(2)

with col1:
    sales_file = st.file_uploader("📤 Upload Sales Data", type=["xlsx", "xls"], key="sales")

with col2:
    purchase_file = st.file_uploader("📥 Upload Stock In / Purchases Data (Optional)", 
                                    type=["xlsx", "xls"], key="purchase")

# ====================== PROCESS SALES DATA ======================
if sales_file:
    with st.spinner("Processing Sales Data..."):
        sales_df = pd.read_excel(sales_file)
        sales_df.columns = [str(col).strip().lower().replace(" ", "_") for col in sales_df.columns]
        
        if 'date' in sales_df.columns:
            sales_df['date'] = pd.to_datetime(sales_df['date'], errors='coerce')
            sales_df = sales_df.dropna(subset=['date'])
        
        for col in ['quantity', 'price', 'total_amount']:
            if col in sales_df.columns:
                sales_df[col] = pd.to_numeric(sales_df[col], errors='coerce')
        
        if 'total_amount' not in sales_df.columns and 'quantity' in sales_df.columns and 'price' in sales_df.columns:
            sales_df['total_amount'] = sales_df['quantity'] * sales_df['price']
        
        sales_df = sales_df.dropna(subset=['total_amount']).copy()

    st.success(f"✅ Sales Data Loaded: {len(sales_df)} records")

    # Filters
    st.sidebar.header("🔍 Filters")
    min_date = sales_df['date'].min().date()
    max_date = sales_df['date'].max().date()
    date_range = st.sidebar.date_input("Date Range", [min_date, max_date])
    filtered_sales = sales_df[(sales_df['date'].dt.date >= date_range[0]) & 
                             (sales_df['date'].dt.date <= date_range[1])]

    # KPI Cards
    c1, c2, c3, c4 = st.columns(4)
    total_sales = filtered_sales['total_amount'].sum()
    total_qty = filtered_sales.get('quantity', pd.Series(0)).sum()
    total_bills = len(filtered_sales)
    avg_bill = total_sales / total_bills if total_bills > 0 else 0

    c1.metric("💰 Total Sales", f"₹{total_sales:,.0f}")
    c2.metric("📦 Quantity Sold", f"{total_qty:,.0f}")
    c3.metric("🧾 Total Bills", f"{total_bills:,}")
    c4.metric("📈 Avg Bill", f"₹{avg_bill:.2f}")

    # ====================== TABS ======================
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📈 Sales Trend", "🏆 Product Performance", "📊 Category & Payment", 
        "📦 Inventory Insights", "☠️ Dead Stock", "📦 Stock Movement (In vs Out)"
    ])

    with tab1:
        daily = filtered_sales.groupby('date')['total_amount'].sum().reset_index()
        st.plotly_chart(px.line(daily, x='date', y='total_amount', title="Daily Sales Trend"), use_container_width=True)

    with tab2:
        top_rev = filtered_sales.groupby('product_name')['total_amount'].sum().nlargest(10).reset_index()
        st.plotly_chart(px.bar(top_rev, x='total_amount', y='product_name', orientation='h', 
                              title="Highest Revenue Products"), use_container_width=True)

    with tab3:
        c1, c2 = st.columns(2)
        with c1:
            if 'category' in filtered_sales.columns:
                cat = filtered_sales.groupby('category')['total_amount'].sum().reset_index()
                st.plotly_chart(px.bar(cat, x='category', y='total_amount', title="Sales by Category"), use_container_width=True)
        with c2:
            if 'payment_mode' in filtered_sales.columns:
                st.plotly_chart(px.pie(filtered_sales, names='payment_mode', values='total_amount', title="Payment Mode"), use_container_width=True)

    with tab4:
        st.subheader("Inventory Insights")
        st.info("Upload Inventory file for better stock analysis (future enhancement)")

    with tab5:  # Dead Stock
        st.subheader("☠️ Dead Stock Analysis")
        product_sales = filtered_sales.groupby('product_name')['quantity'].sum().reset_index()
        dead_stock = product_sales[product_sales['quantity'] <= 3]
        if not dead_stock.empty:
            st.warning(f"Found {len(dead_stock)} Dead/Slow Moving Products")
            st.dataframe(dead_stock, use_container_width=True)
        else:
            st.success("No dead stock in selected period.")

    with tab6:  # Stock Movement
        st.subheader("📦 Stock Movement (In vs Out)")
        
        if purchase_file:
            with st.spinner("Processing Purchase Data..."):
                purchase_df = pd.read_excel(purchase_file)
                purchase_df.columns = [str(col).strip().lower().replace(" ", "_") for col in purchase_df.columns]
                if 'date' in purchase_df.columns:
                    purchase_df['date'] = pd.to_datetime(purchase_df['date'], errors='coerce')
                
                # Daily Stock In
                stock_in = purchase_df.groupby('date')['stock_in'].sum().reset_index() if 'stock_in' in purchase_df.columns else None
                
                # Daily Stock Out
                stock_out = filtered_sales.groupby('date')['quantity'].sum().reset_index()
                stock_out = stock_out.rename(columns={'quantity': 'stock_out'})
                
                # Merge In vs Out
                movement = pd.merge(stock_out, stock_in, on='date', how='outer').fillna(0)
                movement = movement.rename(columns={'stock_in': 'Stock_In'})
                
                st.plotly_chart(px.bar(movement, x='date', y=['Stock_In', 'stock_out'], 
                                      title="Stock Movement - In vs Out", barmode='group'), use_container_width=True)
                
                st.dataframe(movement, use_container_width=True)
        else:
            st.warning("⚠️ Please upload Stock In / Purchases file for accurate In vs Out analysis.")
            st.info("Expected columns in Purchase file: Date, Product Name, Stock In, Purchase Amount")

    # ====================== DOWNLOAD ======================
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        filtered_sales.to_excel(writer, index=False, sheet_name='Sales_Report')
    output.seek(0)

    st.download_button(
        label="📥 Download Sales Report",
        data=output,
        file_name=f"lingam_sales_report_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

else:
    st.info("👆 Please upload **Sales Data** file to start analysis.")
