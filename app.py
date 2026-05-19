import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import io

st.set_page_config(page_title="Lingam Supermarket", layout="wide", page_icon="🛒")

st.title("🛒 Lingam Supermarket Analytics Dashboard")
st.markdown("### Professional Sales & Inventory Intelligence")

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
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📈 Sales Trend", 
        "🏆 Product Performance", 
        "📊 Category & Payment", 
        "📦 Inventory Insights",
        "☠️ Dead Stock",
        "📦 Stock Movement"
    ])

    with tab1:
        if 'date' in filtered_df.columns:
            daily = filtered_df.groupby('date')['total_amount'].sum().reset_index()
            st.plotly_chart(px.line(daily, x='date', y='total_amount', title="Daily Sales Trend"), use_container_width=True)

    with tab2:  # Product Performance
        st.subheader("Highest Revenue Products")
        top_revenue = filtered_df.groupby('product_name')['total_amount'].sum().nlargest(15).reset_index()
        st.plotly_chart(px.bar(top_revenue, x='total_amount', y='product_name', orientation='h', 
                              title="Highest Revenue Products"), use_container_width=True)

        st.subheader("Most Sold by Quantity")
        top_qty = filtered_df.groupby('product_name')['quantity'].sum().nlargest(10).reset_index()
        st.plotly_chart(px.bar(top_qty, x='quantity', y='product_name', orientation='h', 
                              title="Top Products by Quantity Sold"), use_container_width=True)

    with tab3:
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
        product_summary = filtered_df.groupby('product_name').agg({
            'quantity': 'sum',
            'total_amount': 'sum'
        }).reset_index().rename(columns={'quantity': 'Total_Sold'})
        
        st.dataframe(product_summary.sort_values('Total_Sold', ascending=False), use_container_width=True)

    with tab5:  # Dead Stock
        st.subheader("☠️ Dead Stock Analysis")
        all_products = filtered_df.groupby('product_name').agg({
            'quantity': 'sum',
            'total_amount': 'sum',
            'date': 'max'
        }).reset_index()
        
        # Products with very low or zero sales (Dead Stock)
        dead_stock = all_products[all_products['quantity'] <= 2]  # Adjust threshold as needed
        
        if not dead_stock.empty:
            st.warning(f"⚠️ Found {len(dead_stock)} Dead / Slow Moving Products")
            st.dataframe(dead_stock.sort_values('quantity'), use_container_width=True)
        else:
            st.success("No dead stock detected in selected period.")

    with tab6:  # Stock Movement
        st.subheader("📦 Stock Movement (In vs Out)")
        st.info("💡 For accurate Stock Movement, upload a file with both Sales + Purchase/Inward data.")
        
        # Current simulation based on sales (Out)
        movement = filtered_df.groupby('date').agg({
            'quantity': 'sum',
            'total_amount': 'sum'
        }).reset_index()
        movement = movement.rename(columns={'quantity': 'Quantity_Sold_Out'})
        
        st.plotly_chart(px.bar(movement, x='date', y='Quantity_Sold_Out', 
                              title="Daily Stock Out (Sales)"), use_container_width=True)
        
        st.warning("Note: Stock In (Purchase) data is not available in current upload. Add it for full In vs Out comparison.")

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
    st.info("👆 Please upload your sales Excel file to see the complete professional dashboard")
