import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Lingam Supermarket", layout="wide", page_icon="🛒")

st.title("🛒 Lingam Supermarket Analytics Dashboard")

uploaded_file = st.file_uploader("Upload Sales Excel File", type=["xlsx", "xls"])

if uploaded_file:
    with st.spinner("Processing data..."):
        df = pd.read_excel(uploaded_file)
        
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
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Sales", f"₹{df['total_amount'].sum():,.0f}")
    col2.metric("Quantity Sold", f"{df.get('quantity', pd.Series(0)).sum():,.0f}")
    col3.metric("Transactions", f"{len(df):,}")
    col4.metric("Avg Bill", f"₹{df['total_amount'].mean():.2f}")
    
    # Charts
    st.subheader("Daily Sales Trend")
    daily = df.groupby('date')['total_amount'].sum().reset_index()
    st.plotly_chart(px.line(daily, x='date', y='total_amount'), use_container_width=True)
    
    st.subheader("Top 10 Products")
    top10 = df.groupby('product_name')['total_amount'].sum().nlargest(10).reset_index()
    st.plotly_chart(px.bar(top10, x='total_amount', y='product_name', orientation='h'), use_container_width=True)

    st.download_button("Download Report", data=df.to_excel(index=False), file_name="report.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

else:
    st.info("Upload your Excel file")
