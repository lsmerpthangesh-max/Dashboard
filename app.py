import streamlit as st
import pandas as pd
from datetime import datetime
import io

st.set_page_config(page_title="Lingam Supermarket", layout="wide", page_icon="🛒")

st.title("🛒 Lingam Supermarket Analytics Dashboard")

uploaded_file = st.file_uploader("Upload Sales Excel File", type=["xlsx", "xls"])

if uploaded_file:
    with st.spinner("Processing data..."):
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
        
        df = df.dropna(subset=['total_amount'])
    
    st.success(f"✅ Loaded {len(df)} records successfully!")
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Total Sales", f"₹{df['total_amount'].sum():,.0f}")
    col2.metric("📦 Quantity Sold", f"{df.get('quantity', pd.Series(0)).sum():,.0f}")
    col3.metric("🧾 Transactions", f"{len(df):,}")
    col4.metric("📈 Avg Bill", f"₹{df['total_amount'].mean():.2f}")
    
    # Preview
    st.subheader("Data Preview")
    st.dataframe(df.head(10))
    
    # Download Button - FIXED
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sales_Report')
    output.seek(0)
    
    st.download_button(
        label="📥 Download Full Report (Excel)",
        data=output,
        file_name=f"lingam_sales_report_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

else:
    st.info("👆 Please upload your sales Excel file")
