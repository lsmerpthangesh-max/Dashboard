import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import io
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
# PAGE CONFIG & GLOBAL STYLES
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Lingam Supermarket",
    layout="wide",
    page_icon="🛒",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ════════════════════════════════════════
   BASE & MAIN AREA
════════════════════════════════════════ */
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
.main { background: #f0f4f8 !important; }
.block-container { padding: 1.5rem 2rem 2rem 2rem !important; max-width: 1600px; }

/* Force all main-area text to dark so nothing disappears on white */
.main p, .main span, .main div, .main label,
.main h1, .main h2, .main h3, .main h4, .main li { color: #1a2e44 !important; }

/* ════════════════════════════════════════
   SIDEBAR — full dark navy theme
════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a1929 0%, #0d2137 40%, #112d4e 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}

/* Every text element inside sidebar → light */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] small,
[data-testid="stSidebar"] .st-emotion-cache-1629p8f,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] * {
    color: #dce9f7 !important;
}

/* Sidebar section headings */
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em !important;
}

/* Sidebar widget labels */
[data-testid="stSidebar"] .stSelectbox > label,
[data-testid="stSidebar"] .stDateInput  > label,
[data-testid="stSidebar"] .stFileUploader > label {
    color: #90caf9 !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
}

/* Sidebar selectbox/dropdown box */
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stDateInput   > div > div input {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    color: #ffffff !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] .stSelectbox > div > div:hover {
    border-color: #64b5f6 !important;
}
[data-testid="stSidebar"] .stSelectbox svg { color: #90caf9 !important; fill: #90caf9 !important; }

/* Sidebar date input text */
[data-testid="stSidebar"] input[type="text"] {
    color: #ffffff !important;
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
}

/* Sidebar divider */
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.12) !important;
    margin: 1rem 0 !important;
}

/* ── FILE UPLOADER in sidebar ── */
/* Card/box */
[data-testid="stSidebar"] [data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.06) !important;
    border: 1.5px dashed rgba(100,181,246,0.55) !important;
    border-radius: 10px !important;
    padding: 0.5rem !important;
    margin-bottom: 0.6rem !important;
    transition: border-color 0.2s !important;
}
[data-testid="stSidebar"] [data-testid="stFileUploader"]:hover {
    border-color: #64b5f6 !important;
    background: rgba(255,255,255,0.1) !important;
}
/* "Drag and drop" text */
[data-testid="stSidebar"] [data-testid="stFileUploader"] span,
[data-testid="stSidebar"] [data-testid="stFileUploader"] p,
[data-testid="stSidebar"] [data-testid="stFileUploader"] small {
    color: #b0cfe8 !important;
    font-size: 0.78rem !important;
}
/* Browse button inside uploader */
[data-testid="stSidebar"] [data-testid="stFileUploader"] button {
    background: rgba(21,101,192,0.75) !important;
    color: #ffffff !important;
    border: 1px solid rgba(100,181,246,0.5) !important;
    border-radius: 6px !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    padding: 0.3rem 0.8rem !important;
}
[data-testid="stSidebar"] [data-testid="stFileUploader"] button:hover {
    background: rgba(21,101,192,1) !important;
}
/* Uploaded file name chip */
[data-testid="stSidebar"] [data-testid="stFileUploader"] [data-testid="stFileUploaderFile"],
[data-testid="stSidebar"] [data-testid="stFileUploader"] [class*="uploadedFile"] {
    background: rgba(46,125,50,0.25) !important;
    border: 1px solid rgba(102,187,106,0.5) !important;
    border-radius: 6px !important;
    color: #a5d6a7 !important;
}
/* ✕ delete button on uploaded chip */
[data-testid="stSidebar"] [data-testid="stFileUploader"] [data-testid="stFileUploaderDeleteBtn"] button {
    background: transparent !important;
    border: none !important;
    color: #ef9a9a !important;
}

/* ════════════════════════════════════════
   HERO BANNER
════════════════════════════════════════ */
.hero-banner {
    background: linear-gradient(135deg, #0a1929 0%, #0d2137 35%, #1565c0 100%);
    border-radius: 18px; padding: 2rem 2.5rem; margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(13,33,55,0.35);
    position: relative; overflow: hidden;
}
.hero-banner::before {
    content: "🛒"; position: absolute; right: 2.5rem; top: 50%;
    transform: translateY(-50%); font-size: 6rem; opacity: 0.08;
}
.hero-banner::after {
    content: ""; position: absolute; top: -40%; right: 15%;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(100,181,246,0.15) 0%, transparent 70%);
    pointer-events: none;
}
.hero-banner h1 { color: #fff !important; margin: 0; font-size: 2.1rem; font-weight: 800; letter-spacing: -0.02em; }
.hero-banner p  { color: #90caf9 !important; margin: 0.3rem 0 0 0; font-size: 1rem; font-weight: 400; }
.hero-tag {
    display: inline-block; background: rgba(255,255,255,0.12);
    color: #e3f2fd !important; border-radius: 20px; padding: 3px 14px;
    font-size: 0.75rem; font-weight: 600; margin-top: 0.6rem;
    border: 1px solid rgba(255,255,255,0.2);
    backdrop-filter: blur(6px);
}

/* ════════════════════════════════════════
   KPI CARDS
════════════════════════════════════════ */
.kpi-card {
    background: #ffffff !important;
    border-radius: 14px; padding: 1.2rem 1.4rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    border-left: 5px solid #1565c0;
    transition: transform 0.2s, box-shadow 0.2s;
}
.kpi-card:hover { transform: translateY(-3px); box-shadow: 0 6px 24px rgba(0,0,0,0.13); }
.kpi-label { color: #5c7491 !important; font-size: 0.73rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.07em; margin-bottom: 0.35rem; }
.kpi-value { color: #0d2137 !important; font-size: 1.6rem; font-weight: 800; line-height: 1.1; }
.kpi-sub   { color: #6fa86f !important; font-size: 0.76rem; margin-top: 0.35rem; font-weight: 500; }
.kpi-card.green  { border-left-color: #2e7d32; }
.kpi-card.orange { border-left-color: #e65100; }
.kpi-card.purple { border-left-color: #6a1b9a; }
.kpi-card.teal   { border-left-color: #00695c; }
.kpi-card.red    { border-left-color: #c62828; }

/* ════════════════════════════════════════
   SECTION TITLES
════════════════════════════════════════ */
.section-title {
    font-size: 1.05rem; font-weight: 700; color: #0d2137 !important;
    border-left: 4px solid #1565c0; padding-left: 0.75rem;
    margin: 1.5rem 0 0.75rem 0;
}

/* ════════════════════════════════════════
   TABS
════════════════════════════════════════ */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap: 0.3rem; background: #dde5ef; border-radius: 12px; padding: 5px;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    border-radius: 8px; font-weight: 600; font-size: 0.82rem;
    color: #3a5068 !important; padding: 0.45rem 0.9rem;
    background: transparent !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: #1565c0 !important;
    color: #ffffff !important;
    box-shadow: 0 2px 8px rgba(21,101,192,0.35) !important;
}

/* ════════════════════════════════════════
   ALERT BADGES
════════════════════════════════════════ */
.alert-danger { background: #fdecea !important; border: 1px solid #f5c6cb; border-radius: 10px; padding: 0.7rem 1rem; color: #b71c1c !important; font-size: 0.87rem; font-weight: 500; }
.alert-warn   { background: #fff8e1 !important; border: 1px solid #ffe082; border-radius: 10px; padding: 0.7rem 1rem; color: #bf360c !important; font-size: 0.87rem; font-weight: 500; }
.alert-ok     { background: #e8f5e9 !important; border: 1px solid #a5d6a7; border-radius: 10px; padding: 0.7rem 1rem; color: #1b5e20 !important; font-size: 0.87rem; font-weight: 500; }

/* ════════════════════════════════════════
   CHARTS & DATAFRAMES
════════════════════════════════════════ */
.stPlotlyChart { border-radius: 14px; overflow: hidden; box-shadow: 0 2px 12px rgba(0,0,0,0.07); background: #fff; }
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; box-shadow: 0 1px 8px rgba(0,0,0,0.06); }

/* ════════════════════════════════════════
   st.info / st.warning / st.success
════════════════════════════════════════ */
[data-testid="stAlert"] { border-radius: 10px !important; }
[data-testid="stAlert"] p { color: inherit !important; }

/* ════════════════════════════════════════
   DOWNLOAD BUTTONS
════════════════════════════════════════ */
[data-testid="stDownloadButton"] button {
    background: linear-gradient(135deg, #1565c0, #1a237e) !important;
    color: #fff !important; border-radius: 10px !important;
    font-weight: 600 !important; padding: 0.6rem 1.4rem !important;
    border: none !important;
    box-shadow: 0 3px 10px rgba(21,101,192,0.4) !important;
    transition: all 0.2s !important;
}
[data-testid="stDownloadButton"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 18px rgba(21,101,192,0.5) !important;
}

/* ════════════════════════════════════════
   SPINNER
════════════════════════════════════════ */
[data-testid="stSpinner"] p { color: #1565c0 !important; font-weight: 500 !important; }

/* ════════════════════════════════════════
   SELECTBOX & INPUTS (main area)
════════════════════════════════════════ */
.stSelectbox label { color: #3a5068 !important; font-weight: 600 !important; font-size: 0.85rem !important; }

/* ════════════════════════════════════════
   FOOTER
════════════════════════════════════════ */
.footer {
    text-align: center; color: #7a9ab0 !important;
    font-size: 0.75rem; margin-top: 2rem; padding: 1rem;
    border-top: 1px solid #d4dde8;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# COLOUR PALETTE FOR CHARTS
# ─────────────────────────────────────────────
PALETTE   = ["#1565c0","#2e7d32","#e65100","#6a1b9a","#00695c","#c62828","#f9a825","#0277bd","#4a148c","#1b5e20"]
CHART_TPL = dict(
    plot_bgcolor="#ffffff", paper_bgcolor="#ffffff",
    font=dict(family="Inter", color="#0d2137"),
    margin=dict(l=20, r=20, t=40, b=20),
    xaxis=dict(gridcolor="#eef2f7", showline=True, linecolor="#ccd6e0"),
    yaxis=dict(gridcolor="#eef2f7", showline=True, linecolor="#ccd6e0"),
)

def apply_template(fig, title=""):
    fig.update_layout(**CHART_TPL, title=dict(text=title, font=dict(size=15, weight=700, color="#0d2137")))
    return fig

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def to_excel_bytes(df_dict):
    out = io.BytesIO()
    with pd.ExcelWriter(out, engine='openpyxl') as w:
        for sheet, df in df_dict.items():
            df.to_excel(w, sheet_name=sheet[:31], index=False)
    out.seek(0)
    return out

def kpi(label, value, sub="", colour=""):
    return f"""<div class="kpi-card {colour}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {"<div class='kpi-sub'>"+sub+"</div>" if sub else ""}
    </div>"""

# ─────────────────────────────────────────────
# HERO BANNER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
  <h1>🛒 Lingam Supermarket</h1>
  <p>Complete Analytics & Business Intelligence Dashboard</p>
  <span class="hero-tag">📍 Professional Retail Analytics</span>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FILE UPLOADS  (sidebar)
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:1.2rem 0.5rem 0.8rem 0.5rem;">
      <div style="font-size:2rem;margin-bottom:0.3rem;">🛒</div>
      <div style="color:#ffffff;font-size:1.05rem;font-weight:800;letter-spacing:0.03em;">Lingam Supermarket</div>
      <div style="color:#64b5f6;font-size:0.72rem;font-weight:500;margin-top:2px;">Analytics Dashboard</div>
    </div>
    <hr style="border-color:rgba(255,255,255,0.1);margin:0 0 1rem 0;">
    <div style="color:#90caf9;font-size:0.7rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.6rem;padding-left:0.2rem;">
      📂 Data Upload
    </div>
    """, unsafe_allow_html=True)

    sales_file     = st.file_uploader("📊 Sales Data  ★ Required",  type=["xlsx","xls"], key="sales",     help="Upload your daily sales transactions file")
    purchase_file  = st.file_uploader("📦 Purchase / Stock-In",      type=["xlsx","xls"], key="purchase",  help="Upload supplier purchase orders")
    inventory_file = st.file_uploader("🏪 Inventory Master",          type=["xlsx","xls"], key="inventory", help="Upload your product inventory list")
    customer_file  = st.file_uploader("👥 Customer Master",           type=["xlsx","xls"], key="customer",  help="Upload your customer database")
    overall_file   = st.file_uploader("📋 Overall Report Data",       type=["xlsx","xls"], key="overall",   help="Upload merged_data / overall_report_data.xlsx")

    st.markdown("""
    <hr style="border-color:rgba(255,255,255,0.1);margin:0.8rem 0;">
    <div style="color:#90caf9;font-size:0.7rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.4rem;padding-left:0.2rem;">
      🔍 Filters
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
def load_df(f, date_cols=None, num_cols=None):
    df = pd.read_excel(f)
    df.columns = [str(c).strip().lower().replace(" ","_") for c in df.columns]
    if date_cols:
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
    if num_cols:
        for col in num_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

sales_df     = None
purchase_df  = None
inventory_df = None
customer_df  = None

if sales_file:
    with st.spinner("Loading Sales Data…"):
        sales_df = load_df(sales_file, date_cols=['date'],
                           num_cols=['quantity','price','total_amount','discount_%'])
        if 'total_amount' not in sales_df.columns and 'quantity' in sales_df.columns and 'price' in sales_df.columns:
            disc = sales_df.get('discount_%', pd.Series(0, index=sales_df.index)).fillna(0)
            sales_df['total_amount'] = sales_df['quantity'] * sales_df['price'] * (1 - disc/100)
        sales_df = sales_df.dropna(subset=['total_amount','date']).copy()

if purchase_file:
    purchase_df = load_df(purchase_file, date_cols=['date'],
                          num_cols=['stock_in','purchase_rate','purchase_amount'])

if inventory_file:
    inventory_df = load_df(inventory_file, num_cols=['opening_stock','min_stock_level','selling_price','purchase_rate'])

if customer_file:
    customer_df = load_df(customer_file, date_cols=['join_date'])

# ── Overall Report data ──────────────────────────────────────────────────────
overall_inv_df  = None
overall_inv2_df = None

if overall_file:
    try:
        xl_or = pd.ExcelFile(overall_file)
        if "Inventory_Monthly" in xl_or.sheet_names:
            overall_inv_df = pd.read_excel(overall_file, sheet_name="Inventory_Monthly")
            overall_inv_df.columns = [str(c).strip() for c in overall_inv_df.columns]
            for nc in ['INWARD QTY','INWARD PRICE','RETAIL SALES QTY','RETAIL SALES VALUE','RETAIL PROFIT',
                       'WHOLESALE SALES QTY','WHOLESALE VALUE','WHOLESALE PROFIT',
                       'WHOLESALE_2 SALES QTY','WHOLESALE_2 VALUE','WHOLESALE_2 PROFIT',
                       'CUSTOM SALES QTY','CUSTOM SALES VALUE','CUSTOM PROFIT',
                       'REMAINING STOCK QTY','REMAINING STOCK VALUE',
                       'PURCHASE STOCK VALUE','SALES VALUE','CURRENT PROFIT','FINAL PROFIT']:
                if nc in overall_inv_df.columns:
                    overall_inv_df[nc] = pd.to_numeric(overall_inv_df[nc], errors='coerce')
        if "Invoice_Monthly" in xl_or.sheet_names:
            overall_inv2_df = pd.read_excel(overall_file, sheet_name="Invoice_Monthly")
            overall_inv2_df.columns = [str(c).strip() for c in overall_inv2_df.columns]
            for nc in ['Quantity','Unit Price','Discount','Tax Percent','Total Amount']:
                if nc in overall_inv2_df.columns:
                    overall_inv2_df[nc] = pd.to_numeric(overall_inv2_df[nc], errors='coerce')
            if 'Bill Date' in overall_inv2_df.columns:
                overall_inv2_df['Bill Date'] = pd.to_datetime(overall_inv2_df['Bill Date'], errors='coerce')
    except Exception as e:
        st.sidebar.warning(f"Overall file issue: {e}")

# ─────────────────────────────────────────────
# SIDEBAR FILTERS (after data loaded)
# ─────────────────────────────────────────────
filtered_sales = sales_df.copy() if sales_df is not None else None

if sales_df is not None:
    with st.sidebar:
        min_d = sales_df['date'].min().date()
        max_d = sales_df['date'].max().date()
        date_range = st.date_input("📅 Date Range", [min_d, max_d])
        if len(date_range) == 2:
            filtered_sales = sales_df[
                (sales_df['date'].dt.date >= date_range[0]) &
                (sales_df['date'].dt.date <= date_range[1])
            ].copy()

        if 'category' in sales_df.columns:
            cats = ["All Categories"] + sorted(sales_df['category'].dropna().unique().tolist())
            sel_cat = st.selectbox("🏷️ Category", cats)
            if sel_cat != "All Categories":
                filtered_sales = filtered_sales[filtered_sales['category'] == sel_cat]

        if 'payment_mode' in sales_df.columns:
            pms = ["All Payment Modes"] + sorted(sales_df['payment_mode'].dropna().unique().tolist())
            sel_pm = st.selectbox("💳 Payment Mode", pms)
            if sel_pm != "All Payment Modes":
                filtered_sales = filtered_sales[filtered_sales['payment_mode'] == sel_pm]

        st.markdown("""
        <div style="margin-top:1.4rem;padding:0.8rem;background:rgba(255,255,255,0.05);
                    border-radius:10px;border:1px solid rgba(255,255,255,0.08);">
          <div style="color:#64b5f6;font-size:0.68rem;font-weight:700;text-transform:uppercase;
                      letter-spacing:0.08em;margin-bottom:0.4rem;">ℹ️ Quick Guide</div>
          <div style="color:#b0cfe8;font-size:0.71rem;line-height:1.6;">
            ★ Sales file is required.<br>
            Other files unlock extra tabs.<br>
            Filters apply to all charts.
          </div>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# NO DATA STATE
# ─────────────────────────────────────────────
if sales_df is None:
    st.markdown("""
    <div style="background:#ffffff;border-radius:20px;padding:3rem 2.5rem;text-align:center;
                box-shadow:0 6px 28px rgba(0,0,0,0.09);margin-top:0.5rem;
                border:1px solid #e2ecf7;">
      <div style="font-size:4rem;margin-bottom:0.8rem;">📤</div>
      <h2 style="color:#0d2137 !important;font-size:1.6rem;font-weight:800;margin-bottom:0.5rem;">
        Upload Your Data to Get Started
      </h2>
      <p style="color:#4a6680 !important;max-width:520px;margin:0 auto 2rem auto;font-size:0.95rem;line-height:1.6;">
        Use the <strong style="color:#1565c0;">left sidebar</strong> to upload your Excel files.
        Only <strong style="color:#1565c0;">Sales Data</strong> is required — the rest unlock extra analytics.
      </p>
      <div style="display:flex;justify-content:center;gap:1rem;flex-wrap:wrap;margin-bottom:2rem;">
        <div style="background:#f0f7ff;border:1px solid #bbdefb;border-radius:12px;padding:0.9rem 1.4rem;min-width:130px;">
          <div style="font-size:1.4rem;">📊</div>
          <div style="color:#1565c0 !important;font-weight:700;font-size:0.82rem;margin-top:0.3rem;">Sales Data</div>
          <div style="color:#5c7491 !important;font-size:0.72rem;">★ Required</div>
        </div>
        <div style="background:#f1f8e9;border:1px solid #c5e1a5;border-radius:12px;padding:0.9rem 1.4rem;min-width:130px;">
          <div style="font-size:1.4rem;">📦</div>
          <div style="color:#2e7d32 !important;font-weight:700;font-size:0.82rem;margin-top:0.3rem;">Purchase Data</div>
          <div style="color:#5c7491 !important;font-size:0.72rem;">Optional</div>
        </div>
        <div style="background:#fff3e0;border:1px solid #ffcc80;border-radius:12px;padding:0.9rem 1.4rem;min-width:130px;">
          <div style="font-size:1.4rem;">🏪</div>
          <div style="color:#e65100 !important;font-weight:700;font-size:0.82rem;margin-top:0.3rem;">Inventory</div>
          <div style="color:#5c7491 !important;font-size:0.72rem;">Optional</div>
        </div>
        <div style="background:#f3e5f5;border:1px solid #ce93d8;border-radius:12px;padding:0.9rem 1.4rem;min-width:130px;">
          <div style="font-size:1.4rem;">👥</div>
          <div style="color:#6a1b9a !important;font-weight:700;font-size:0.82rem;margin-top:0.3rem;">Customers</div>
          <div style="color:#5c7491 !important;font-size:0.72rem;">Optional</div>
        </div>
      </div>
      <div style="background:#e8f0fe;border-radius:10px;padding:0.8rem 1.2rem;
                  display:inline-block;color:#1a237e !important;font-size:0.85rem;font-weight:600;">
        💡 Use the template Excel files provided to test the dashboard instantly
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ─────────────────────────────────────────────
# COMPUTE KPIs
# ─────────────────────────────────────────────
fs = filtered_sales
total_sales   = fs['total_amount'].sum()
total_qty     = fs['quantity'].sum() if 'quantity' in fs.columns else 0
total_bills   = len(fs)
avg_bill      = total_sales / total_bills if total_bills > 0 else 0
unique_prods  = fs['product_name'].nunique() if 'product_name' in fs.columns else 0
unique_custs  = fs['customer_id'].nunique() if 'customer_id' in fs.columns else 0

# MoM comparison
if 'date' in fs.columns and len(fs):
    latest_month = fs['date'].dt.to_period('M').max()
    prev_month   = latest_month - 1
    this_m = fs[fs['date'].dt.to_period('M') == latest_month]['total_amount'].sum()
    prev_m = fs[fs['date'].dt.to_period('M') == prev_month]['total_amount'].sum()
    mom_pct = ((this_m - prev_m)/prev_m*100) if prev_m else 0
    mom_str = f"{'▲' if mom_pct>=0 else '▼'} {abs(mom_pct):.1f}% vs prev month"
else:
    mom_str = ""

# ─────────────────────────────────────────────
# KPI ROW
# ─────────────────────────────────────────────
k1,k2,k3,k4,k5,k6 = st.columns(6)
k1.markdown(kpi("💰 Total Revenue",   f"₹{total_sales:,.0f}",  mom_str), unsafe_allow_html=True)
k2.markdown(kpi("📦 Units Sold",      f"{total_qty:,.0f}",     "", "green"), unsafe_allow_html=True)
k3.markdown(kpi("🧾 Invoices",        f"{total_bills:,}",      "", "orange"), unsafe_allow_html=True)
k4.markdown(kpi("📈 Avg Invoice",     f"₹{avg_bill:,.0f}",     "", "purple"), unsafe_allow_html=True)
k5.markdown(kpi("🏷️ Products Active", f"{unique_prods}",       "", "teal"), unsafe_allow_html=True)
k6.markdown(kpi("👥 Customers",       f"{unique_custs}",       "", "red"), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tabs = st.tabs([
    "📈 Sales Trend",
    "🏆 Top Products",
    "🏷️ Category & Payment",
    "📦 Stock Movement",
    "☠️ Dead Stock",
    "👥 Customer Insights",
    "📅 Monthly Report",
    "📆 Yearly Report",
    "🚨 Alerts",
    "📥 Download Reports",
    "📋 Overall Report"
])

# ────────────────────────────────────
# TAB 1: SALES TREND
# ────────────────────────────────────
with tabs[0]:
    st.markdown('<div class="section-title">Daily & Monthly Sales Trend</div>', unsafe_allow_html=True)

    daily = fs.groupby('date')['total_amount'].sum().reset_index()
    fig_daily = px.line(daily, x='date', y='total_amount', color_discrete_sequence=[PALETTE[0]])
    fig_daily.add_scatter(x=daily['date'], y=daily['total_amount'].rolling(7).mean(),
                          mode='lines', name='7-Day Avg', line=dict(dash='dash', color=PALETTE[2], width=2))
    apply_template(fig_daily, "Daily Revenue with 7-Day Moving Average")
    fig_daily.update_traces(selector=dict(mode='lines'), line_width=1.5)
    st.plotly_chart(fig_daily, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        monthly = fs.groupby(fs['date'].dt.to_period('M'))['total_amount'].sum().reset_index()
        monthly['date'] = monthly['date'].astype(str)
        fig_m = px.bar(monthly, x='date', y='total_amount', color_discrete_sequence=[PALETTE[0]])
        apply_template(fig_m, "Monthly Revenue")
        st.plotly_chart(fig_m, use_container_width=True)
    with c2:
        weekly = fs.groupby(fs['date'].dt.day_name())['total_amount'].mean().reindex(
            ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']).reset_index()
        weekly.columns = ['Day', 'Avg_Sales']
        fig_w = px.bar(weekly, x='Day', y='Avg_Sales', color_discrete_sequence=[PALETTE[4]])
        apply_template(fig_w, "Avg Sales by Day of Week")
        st.plotly_chart(fig_w, use_container_width=True)

    if 'quantity' in fs.columns:
        hourly_note = "Tip: If your sales data has an 'hour' column, hourly heatmaps will appear here."
        st.info(hourly_note)

# ────────────────────────────────────
# TAB 2: TOP PRODUCTS
# ────────────────────────────────────
with tabs[1]:
    st.markdown('<div class="section-title">Product Performance</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        top_rev = fs.groupby('product_name')['total_amount'].sum().nlargest(15).reset_index()
        fig = px.bar(top_rev, x='total_amount', y='product_name', orientation='h',
                     color='total_amount', color_continuous_scale='Blues')
        apply_template(fig, "Top 15 Products by Revenue (₹)")
        fig.update_layout(yaxis=dict(autorange='reversed'), coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        if 'quantity' in fs.columns:
            top_qty = fs.groupby('product_name')['quantity'].sum().nlargest(15).reset_index()
            fig2 = px.bar(top_qty, x='quantity', y='product_name', orientation='h',
                          color='quantity', color_continuous_scale='Greens')
            apply_template(fig2, "Top 15 Products by Quantity Sold")
            fig2.update_layout(yaxis=dict(autorange='reversed'), coloraxis_showscale=False)
            st.plotly_chart(fig2, use_container_width=True)

    # Revenue contribution
    st.markdown('<div class="section-title">Revenue Concentration (Pareto)</div>', unsafe_allow_html=True)
    prod_rev = fs.groupby('product_name')['total_amount'].sum().sort_values(ascending=False).reset_index()
    prod_rev['cumulative_%'] = (prod_rev['total_amount'].cumsum() / prod_rev['total_amount'].sum() * 100).round(1)
    fig_p = make_subplots(specs=[[{"secondary_y": True}]])
    fig_p.add_trace(go.Bar(x=prod_rev['product_name'][:20], y=prod_rev['total_amount'][:20],
                           name='Revenue', marker_color=PALETTE[0]), secondary_y=False)
    fig_p.add_trace(go.Scatter(x=prod_rev['product_name'][:20], y=prod_rev['cumulative_%'][:20],
                               mode='lines+markers', name='Cumulative %', line=dict(color=PALETTE[2], width=2)),
                    secondary_y=True)
    fig_p.update_layout(**CHART_TPL, title=dict(text="Pareto – Top 20 Products", font=dict(size=15,weight=700)))
    fig_p.update_yaxes(title_text="Revenue ₹", secondary_y=False)
    fig_p.update_yaxes(title_text="Cumulative %", secondary_y=True, range=[0,110])
    st.plotly_chart(fig_p, use_container_width=True)

# ────────────────────────────────────
# TAB 3: CATEGORY & PAYMENT
# ────────────────────────────────────
with tabs[2]:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-title">Revenue by Category</div>', unsafe_allow_html=True)
        if 'category' in fs.columns:
            cat_df = fs.groupby('category')['total_amount'].sum().reset_index().sort_values('total_amount', ascending=False)
            fig = px.bar(cat_df, x='category', y='total_amount', color='total_amount',
                         color_continuous_scale='Blues', text_auto='.2s')
            apply_template(fig, "")
            fig.update_layout(coloraxis_showscale=False, xaxis_tickangle=-30)
            st.plotly_chart(fig, use_container_width=True)

            if 'quantity' in fs.columns:
                cat_qty = fs.groupby('category')['quantity'].sum().reset_index()
                fig2 = px.pie(cat_qty, names='category', values='quantity',
                              color_discrete_sequence=PALETTE, hole=0.4)
                apply_template(fig2, "Quantity Share by Category")
                st.plotly_chart(fig2, use_container_width=True)

    with c2:
        st.markdown('<div class="section-title">Payment Mode Analysis</div>', unsafe_allow_html=True)
        if 'payment_mode' in fs.columns:
            pm_df = fs.groupby('payment_mode')['total_amount'].sum().reset_index()
            fig3 = px.pie(pm_df, names='payment_mode', values='total_amount',
                          color_discrete_sequence=PALETTE, hole=0.45)
            apply_template(fig3, "Sales Split by Payment Mode")
            st.plotly_chart(fig3, use_container_width=True)

            pm_cnt = fs.groupby('payment_mode')['total_amount'].count().reset_index()
            pm_cnt.columns = ['Payment Mode','Transaction Count']
            pm_avg = fs.groupby('payment_mode')['total_amount'].mean().reset_index()
            pm_avg.columns = ['Payment Mode','Avg Transaction ₹']
            pm_merged = pm_cnt.merge(pm_avg, on='Payment Mode')
            pm_merged['Avg Transaction ₹'] = pm_merged['Avg Transaction ₹'].map('₹{:,.0f}'.format)
            st.dataframe(pm_merged, use_container_width=True, hide_index=True)

            # Cash vs Digital split
            if 'payment_mode' in fs.columns:
                fs_pm = fs.copy()
                fs_pm['mode_type'] = fs_pm['payment_mode'].apply(
                    lambda x: 'Cash' if str(x).lower()=='cash' else 'Digital')
                mode_summary = fs_pm.groupby('mode_type')['total_amount'].sum().reset_index()
                fig4 = px.pie(mode_summary, names='mode_type', values='total_amount',
                              color_discrete_sequence=['#1565c0','#2e7d32'], hole=0.5)
                apply_template(fig4, "Cash vs Digital Payments")
                st.plotly_chart(fig4, use_container_width=True)

# ────────────────────────────────────
# TAB 4: STOCK MOVEMENT
# ────────────────────────────────────
with tabs[3]:
    st.markdown('<div class="section-title">Stock-In vs Stock-Out Movement</div>', unsafe_allow_html=True)

    stock_out = fs.groupby('date')['quantity'].sum().reset_index().rename(columns={'quantity':'Stock_Out'}) if 'quantity' in fs.columns else None

    if purchase_df is not None and 'stock_in' in purchase_df.columns:
        stock_in = purchase_df.groupby('date')['stock_in'].sum().reset_index().rename(columns={'stock_in':'Stock_In'})
        if stock_out is not None:
            movement = pd.merge(stock_out, stock_in, on='date', how='outer').fillna(0).sort_values('date')
            fig = go.Figure()
            fig.add_bar(x=movement['date'], y=movement['Stock_In'],  name='Stock In',  marker_color=PALETTE[1])
            fig.add_bar(x=movement['date'], y=movement['Stock_Out'], name='Stock Out', marker_color=PALETTE[2])
            apply_template(fig, "Daily Stock Movement – In vs Out")
            fig.update_layout(barmode='group')
            st.plotly_chart(fig, use_container_width=True)

            movement['Net_Stock'] = movement['Stock_In'] - movement['Stock_Out']
            fig2 = px.area(movement, x='date', y='Net_Stock', color_discrete_sequence=[PALETTE[0]])
            apply_template(fig2, "Net Stock Position Over Time")
            st.plotly_chart(fig2, use_container_width=True)

            st.dataframe(movement.tail(30), use_container_width=True, hide_index=True)

        # Supplier analysis
        if 'supplier_name' in purchase_df.columns and 'purchase_amount' in purchase_df.columns:
            st.markdown('<div class="section-title">Supplier Analysis</div>', unsafe_allow_html=True)
            sup_df = purchase_df.groupby('supplier_name')['purchase_amount'].sum().reset_index().sort_values('purchase_amount', ascending=False)
            fig3 = px.bar(sup_df, x='supplier_name', y='purchase_amount',
                          color='purchase_amount', color_continuous_scale='Greens', text_auto='.2s')
            apply_template(fig3, "Purchase Value by Supplier")
            fig3.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig3, use_container_width=True)
    else:
        if stock_out is not None:
            fig = px.bar(stock_out, x='date', y='Stock_Out', color_discrete_sequence=[PALETTE[2]])
            apply_template(fig, "Daily Stock-Out (Sales Quantity)")
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="alert-warn">⚠️ Upload Purchase / Stock-In file for full In vs Out analysis.</div>', unsafe_allow_html=True)

# ────────────────────────────────────
# TAB 5: DEAD STOCK
# ────────────────────────────────────
with tabs[4]:
    st.markdown('<div class="section-title">☠️ Dead & Slow-Moving Stock Analysis</div>', unsafe_allow_html=True)

    if 'quantity' in fs.columns and 'product_name' in fs.columns:
        prod_sales = fs.groupby('product_name').agg(
            Total_Qty=('quantity','sum'),
            Total_Revenue=('total_amount','sum'),
            Last_Sale=('date','max'),
            Transactions=('total_amount','count')
        ).reset_index()

        today = pd.Timestamp.today()
        prod_sales['Days_Since_Last_Sale'] = (today - prod_sales['Last_Sale']).dt.days

        dead   = prod_sales[prod_sales['Total_Qty'] <= 5].sort_values('Total_Qty')
        slow   = prod_sales[(prod_sales['Total_Qty'] > 5) & (prod_sales['Total_Qty'] <= 20)].sort_values('Total_Qty')
        stale  = prod_sales[prod_sales['Days_Since_Last_Sale'] > 30].sort_values('Days_Since_Last_Sale', ascending=False)

        d1, d2, d3 = st.columns(3)
        d1.markdown(kpi("☠️ Dead Stock",       f"{len(dead)}",  "≤ 5 units sold", "red"),   unsafe_allow_html=True)
        d2.markdown(kpi("🐌 Slow Moving",      f"{len(slow)}",  "5-20 units",     "orange"), unsafe_allow_html=True)
        d3.markdown(kpi("📅 Not Sold 30+ Days",f"{len(stale)}", "Check reorder",  "purple"), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if not dead.empty:
                st.markdown('<div class="alert-danger">🚨 Dead Stock – Take Immediate Action</div>', unsafe_allow_html=True)
                st.dataframe(dead[['product_name','Total_Qty','Total_Revenue','Days_Since_Last_Sale']].head(20),
                             use_container_width=True, hide_index=True)
            else:
                st.markdown('<div class="alert-ok">✅ No dead stock found in this period.</div>', unsafe_allow_html=True)
        with c2:
            if not slow.empty:
                st.markdown('<div class="alert-warn">⚠️ Slow-Moving Products</div>', unsafe_allow_html=True)
                st.dataframe(slow[['product_name','Total_Qty','Total_Revenue','Days_Since_Last_Sale']].head(20),
                             use_container_width=True, hide_index=True)

        # Bubble chart: qty vs revenue
        fig = px.scatter(prod_sales.head(30), x='Total_Qty', y='Total_Revenue',
                         size='Transactions', color='Days_Since_Last_Sale',
                         hover_name='product_name', color_continuous_scale='RdYlGn_r',
                         size_max=40)
        apply_template(fig, "Product Matrix: Qty vs Revenue (bubble = transactions, color = days since last sale)")
        st.plotly_chart(fig, use_container_width=True)

# ────────────────────────────────────
# TAB 6: CUSTOMER INSIGHTS
# ────────────────────────────────────
with tabs[5]:
    st.markdown('<div class="section-title">👥 Customer Analytics</div>', unsafe_allow_html=True)

    if 'customer_id' in fs.columns:
        cust_stats = fs.groupby('customer_id').agg(
            Total_Spent=('total_amount','sum'),
            Visits=('total_amount','count'),
            Last_Visit=('date','max'),
            First_Visit=('date','min')
        ).reset_index()
        cust_stats['Avg_Per_Visit']  = cust_stats['Total_Spent'] / cust_stats['Visits']
        cust_stats['Days_Since_Visit'] = (pd.Timestamp.today() - cust_stats['Last_Visit']).dt.days

        # RFM-lite segmentation
        def segment(row):
            if row['Visits'] >= 10 and row['Total_Spent'] >= cust_stats['Total_Spent'].quantile(0.75):
                return "🌟 VIP"
            elif row['Visits'] >= 5:
                return "🔄 Regular"
            elif row['Days_Since_Visit'] > 60:
                return "💤 Dormant"
            else:
                return "🆕 New"
        cust_stats['Segment'] = cust_stats.apply(segment, axis=1)

        seg_summary = cust_stats.groupby('Segment').agg(
            Count=('customer_id','count'),
            Total_Spent=('Total_Spent','sum'),
            Avg_Visits=('Visits','mean')
        ).reset_index()

        c1, c2 = st.columns(2)
        with c1:
            fig = px.pie(seg_summary, names='Segment', values='Count',
                         color_discrete_sequence=PALETTE, hole=0.45)
            apply_template(fig, "Customer Segments")
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig2 = px.bar(seg_summary, x='Segment', y='Total_Spent',
                          color='Segment', color_discrete_sequence=PALETTE, text_auto='.2s')
            apply_template(fig2, "Revenue by Customer Segment")
            fig2.update_layout(showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)

        # New vs Returning customers over time (if join_date available)
        st.markdown('<div class="section-title">New vs Returning Customer Trend</div>', unsafe_allow_html=True)
        monthly_visits = fs.groupby([fs['date'].dt.to_period('M'), 'customer_id'])['total_amount'].count().reset_index()
        monthly_visits.columns = ['Month','customer_id','visits']
        first_month = monthly_visits.groupby('customer_id')['Month'].min().reset_index()
        first_month.columns = ['customer_id','First_Month']
        monthly_visits = monthly_visits.merge(first_month, on='customer_id')
        monthly_visits['Type'] = monthly_visits.apply(lambda r: 'New' if r['Month']==r['First_Month'] else 'Returning', axis=1)
        nv = monthly_visits.groupby(['Month','Type'])['customer_id'].nunique().reset_index()
        nv['Month'] = nv['Month'].astype(str)
        fig3 = px.bar(nv, x='Month', y='customer_id', color='Type',
                      color_discrete_map={'New':PALETTE[1],'Returning':PALETTE[0]}, barmode='stack')
        apply_template(fig3, "New vs Returning Customers Monthly")
        fig3.update_layout(xaxis_tickangle=-30)
        st.plotly_chart(fig3, use_container_width=True)

        st.markdown('<div class="section-title">Top Customers by Revenue</div>', unsafe_allow_html=True)
        top_custs = cust_stats.sort_values('Total_Spent', ascending=False).head(20)
        top_custs['Total_Spent']    = top_custs['Total_Spent'].map('₹{:,.0f}'.format)
        top_custs['Avg_Per_Visit']  = top_custs['Avg_Per_Visit'].map('₹{:,.0f}'.format)
        st.dataframe(top_custs[['customer_id','Segment','Total_Spent','Visits','Avg_Per_Visit','Days_Since_Visit']],
                     use_container_width=True, hide_index=True)

        if customer_df is not None and 'customer_name' in customer_df.columns:
            st.markdown('<div class="section-title">Customer Master Details</div>', unsafe_allow_html=True)
            if 'customer_type' in customer_df.columns:
                ct = customer_df.groupby('customer_type').size().reset_index(name='Count')
                fig4 = px.pie(ct, names='customer_type', values='Count',
                              color_discrete_sequence=PALETTE, hole=0.4)
                apply_template(fig4, "Customer Types from Master Data")
                st.plotly_chart(fig4, use_container_width=True)
    else:
        st.info("Add a 'Customer_ID' column in your Sales file to unlock Customer Analytics.")

# ────────────────────────────────────
# TAB 7: MONTHLY REPORT
# ────────────────────────────────────
with tabs[6]:
    st.markdown('<div class="section-title">📅 Monthly Performance Report</div>', unsafe_allow_html=True)

    if 'date' in fs.columns:
        fs_m = fs.copy()
        fs_m['Month']     = fs_m['date'].dt.to_period('M')
        fs_m['MonthStr']  = fs_m['date'].dt.strftime('%b %Y')

        monthly_summary = fs_m.groupby(['Month','MonthStr']).agg(
            Revenue=('total_amount','sum'),
            Units=('quantity','sum') if 'quantity' in fs_m.columns else ('total_amount','count'),
            Invoices=('total_amount','count'),
            Avg_Invoice=('total_amount','mean'),
            Customers=('customer_id','nunique') if 'customer_id' in fs_m.columns else ('total_amount','count')
        ).reset_index().sort_values('Month')

        monthly_summary['MoM_Growth'] = monthly_summary['Revenue'].pct_change() * 100

        # Month selector
        months_avail = monthly_summary['MonthStr'].tolist()
        sel_month = st.selectbox("Select Month to Drill Down", months_avail, index=len(months_avail)-1)
        sel_data  = fs_m[fs_m['MonthStr'] == sel_month]

        st.markdown("---")
        m1,m2,m3,m4 = st.columns(4)
        m_rev    = sel_data['total_amount'].sum()
        m_inv    = len(sel_data)
        m_units  = sel_data['quantity'].sum() if 'quantity' in sel_data.columns else 0
        m_avg    = m_rev/m_inv if m_inv else 0
        m1.markdown(kpi("Revenue", f"₹{m_rev:,.0f}", sel_month), unsafe_allow_html=True)
        m2.markdown(kpi("Invoices", f"{m_inv:,}", "", "green"), unsafe_allow_html=True)
        m3.markdown(kpi("Units Sold", f"{m_units:,.0f}", "", "orange"), unsafe_allow_html=True)
        m4.markdown(kpi("Avg Invoice", f"₹{m_avg:,.0f}", "", "purple"), unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            # Top products this month
            tp = sel_data.groupby('product_name')['total_amount'].sum().nlargest(10).reset_index()
            fig = px.bar(tp, x='total_amount', y='product_name', orientation='h',
                         color_discrete_sequence=[PALETTE[0]])
            apply_template(fig, f"Top Products – {sel_month}")
            fig.update_layout(yaxis=dict(autorange='reversed'))
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            # Category split this month
            if 'category' in sel_data.columns:
                cat_m = sel_data.groupby('category')['total_amount'].sum().reset_index()
                fig2 = px.pie(cat_m, names='category', values='total_amount',
                              color_discrete_sequence=PALETTE, hole=0.4)
                apply_template(fig2, f"Category Mix – {sel_month}")
                st.plotly_chart(fig2, use_container_width=True)

        # Full monthly trend table
        st.markdown('<div class="section-title">All Months Summary</div>', unsafe_allow_html=True)
        display_cols = ['MonthStr','Revenue','Units','Invoices','Avg_Invoice','MoM_Growth']
        display_cols = [c for c in display_cols if c in monthly_summary.columns]
        ms_disp = monthly_summary[display_cols].copy()
        for col in ['Revenue','Avg_Invoice']:
            if col in ms_disp.columns:
                ms_disp[col] = ms_disp[col].map('₹{:,.0f}'.format)
        if 'MoM_Growth' in ms_disp.columns:
            ms_disp['MoM_Growth'] = ms_disp['MoM_Growth'].map(lambda x: f"{'▲' if x>=0 else '▼'} {abs(x):.1f}%" if pd.notna(x) else '-')
        st.dataframe(ms_disp, use_container_width=True, hide_index=True)

# ────────────────────────────────────
# TAB 8: YEARLY REPORT
# ────────────────────────────────────
with tabs[7]:
    st.markdown('<div class="section-title">📆 Yearly Business Performance</div>', unsafe_allow_html=True)

    if 'date' in fs.columns:
        fs_y = fs.copy()
        fs_y['Year'] = fs_y['date'].dt.year

        yearly = fs_y.groupby('Year').agg(
            Revenue=('total_amount','sum'),
            Units=('quantity','sum') if 'quantity' in fs_y.columns else ('total_amount','count'),
            Invoices=('total_amount','count'),
            Avg_Invoice=('total_amount','mean'),
            Customers=('customer_id','nunique') if 'customer_id' in fs_y.columns else ('total_amount','count'),
            Products=('product_name','nunique') if 'product_name' in fs_y.columns else ('total_amount','count')
        ).reset_index()

        # Yearly KPIs
        y1,y2,y3 = st.columns(3)
        for i, row in yearly.iterrows():
            if i == 0:
                y1.markdown(kpi(f"📆 {row['Year']} Revenue", f"₹{row['Revenue']:,.0f}", f"{row['Invoices']:,} invoices"), unsafe_allow_html=True)
            elif i == 1:
                y2.markdown(kpi(f"📆 {row['Year']} Revenue", f"₹{row['Revenue']:,.0f}", f"{row['Invoices']:,} invoices", "green"), unsafe_allow_html=True)
            else:
                y3.markdown(kpi(f"📆 {row['Year']} Revenue", f"₹{row['Revenue']:,.0f}", f"{row['Invoices']:,} invoices", "orange"), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            fig = px.bar(yearly, x='Year', y='Revenue', color_discrete_sequence=[PALETTE[0]],
                         text_auto='.2s')
            apply_template(fig, "Annual Revenue")
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig2 = px.bar(yearly, x='Year', y='Invoices', color_discrete_sequence=[PALETTE[1]],
                          text_auto=True)
            apply_template(fig2, "Annual Invoice Count")
            st.plotly_chart(fig2, use_container_width=True)

        # YoY Top Products
        st.markdown('<div class="section-title">Top 10 Products – All Time</div>', unsafe_allow_html=True)
        all_top = fs_y.groupby(['Year','product_name'])['total_amount'].sum().reset_index()
        top_prods_all = all_top.groupby('product_name')['total_amount'].sum().nlargest(10).index.tolist()
        all_top_filt  = all_top[all_top['product_name'].isin(top_prods_all)]
        all_top_filt['Year'] = all_top_filt['Year'].astype(str)
        fig3 = px.bar(all_top_filt, x='product_name', y='total_amount', color='Year',
                      barmode='group', color_discrete_sequence=PALETTE)
        apply_template(fig3, "Top 10 Products Revenue by Year")
        fig3.update_layout(xaxis_tickangle=-30)
        st.plotly_chart(fig3, use_container_width=True)

        # Annual summary table
        st.markdown('<div class="section-title">Annual Summary Table</div>', unsafe_allow_html=True)
        yr_disp = yearly.copy()
        yr_disp['Revenue']    = yr_disp['Revenue'].map('₹{:,.0f}'.format)
        yr_disp['Avg_Invoice']= yr_disp['Avg_Invoice'].map('₹{:,.0f}'.format)
        st.dataframe(yr_disp, use_container_width=True, hide_index=True)

# ────────────────────────────────────
# TAB 9: ALERTS & RECOMMENDATIONS
# ────────────────────────────────────
with tabs[8]:
    st.markdown('<div class="section-title">🚨 Smart Alerts & Business Recommendations</div>', unsafe_allow_html=True)

    alerts = []

    if 'quantity' in fs.columns and 'product_name' in fs.columns:
        prod_qty  = fs.groupby('product_name')['quantity'].sum()
        dead_count = (prod_qty <= 5).sum()
        if dead_count > 0:
            alerts.append(("danger", f"☠️ {dead_count} products have ≤5 units sold — review for clearance or discontinuation."))

    if len(fs):
        latest_7  = fs[fs['date'] >= fs['date'].max() - pd.Timedelta(days=7)]['total_amount'].sum()
        prev_7    = fs[(fs['date'] >= fs['date'].max() - pd.Timedelta(days=14)) &
                       (fs['date'] < fs['date'].max() - pd.Timedelta(days=7))]['total_amount'].sum()
        if prev_7 > 0 and latest_7 < prev_7 * 0.9:
            pct = (prev_7-latest_7)/prev_7*100
            alerts.append(("danger", f"📉 Sales dropped {pct:.1f}% in the last 7 days vs the previous 7 days. Investigate!"))
        elif prev_7 > 0 and latest_7 > prev_7 * 1.1:
            pct = (latest_7-prev_7)/prev_7*100
            alerts.append(("ok", f"📈 Sales are up {pct:.1f}% in the last 7 days vs the previous 7 days. Great momentum!"))

    if 'payment_mode' in fs.columns:
        digital_pct = fs[fs['payment_mode'].str.lower()!='cash']['total_amount'].sum() / fs['total_amount'].sum() * 100
        if digital_pct < 20:
            alerts.append(("warn", f"💳 Only {digital_pct:.0f}% digital payments. Consider GPay/PhonePe promotions to improve tracking."))
        else:
            alerts.append(("ok", f"💳 {digital_pct:.0f}% digital payment adoption. Good for audit trails!"))

    if 'customer_id' in fs.columns:
        cust_freq = fs.groupby('customer_id').size()
        single_visit = (cust_freq == 1).sum()
        if single_visit > len(cust_freq) * 0.5:
            alerts.append(("warn", f"👥 {single_visit} customers ({single_visit/len(cust_freq)*100:.0f}%) visited only once. Launch a loyalty programme!"))

    if inventory_df is not None and 'min_stock_level' in inventory_df.columns and 'opening_stock' in inventory_df.columns:
        low_stock = inventory_df[inventory_df['opening_stock'] <= inventory_df['min_stock_level']]
        if not low_stock.empty:
            alerts.append(("danger", f"📦 {len(low_stock)} products are at or below minimum stock level. Reorder immediately!"))

    if not alerts:
        alerts.append(("ok", "✅ No critical alerts found for the selected period. Business looks healthy!"))

    type_map = {"danger":"alert-danger","warn":"alert-warn","ok":"alert-ok"}
    for atype, msg in alerts:
        st.markdown(f'<div class="{type_map[atype]}" style="margin-bottom:0.6rem;">{msg}</div>', unsafe_allow_html=True)

    # Recommendations
    st.markdown('<div class="section-title">💡 Recommendations</div>', unsafe_allow_html=True)
    recs = [
        ("🔄","Run monthly dead-stock clearance sales to free up shelf space and cash flow."),
        ("📱","Send WhatsApp offers to dormant customers (not visited in 30+ days)."),
        ("⭐","Reward top 20% VIP customers (highest spend) with exclusive discounts."),
        ("📊","Review product categories with declining revenue and negotiate better supplier rates."),
        ("💰","Offer 2% cashback on GPay/PhonePe to shift cash customers to digital (easier reconciliation)."),
        ("📦","Set up automatic reorder alerts when inventory touches min-stock levels."),
        ("🕐","Identify peak sales hours and schedule extra staff accordingly."),
        ("🧾","Bundle slow-moving items with fast-moving ones to clear dead stock faster."),
    ]
    for icon, rec in recs:
        st.markdown(f"""
        <div style="background:#fff;border-radius:10px;padding:0.7rem 1rem;margin-bottom:0.5rem;
                    box-shadow:0 1px 6px rgba(0,0,0,0.07);display:flex;gap:0.8rem;align-items:flex-start;">
          <span style="font-size:1.3rem;">{icon}</span>
          <span style="color:#2d3a47;font-size:0.9rem;">{rec}</span>
        </div>
        """, unsafe_allow_html=True)

# ────────────────────────────────────
# TAB 10: DOWNLOAD REPORTS
# ────────────────────────────────────
with tabs[9]:
    st.markdown('<div class="section-title">📥 Download Reports</div>', unsafe_allow_html=True)
    st.markdown("Export ready-to-use Excel reports for sharing, printing, or archiving.")
    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### 📊 Sales Report")
        excel_sales = to_excel_bytes({'Sales_Data': filtered_sales})
        st.download_button("📥 Download Filtered Sales", data=excel_sales,
                           file_name=f"lingam_sales_{datetime.now().strftime('%Y%m%d')}.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           use_container_width=True)

    with c2:
        st.markdown("#### 🏆 Product Summary")
        prod_summary = fs.groupby('product_name').agg(
            Total_Revenue=('total_amount','sum'),
            Units_Sold=('quantity','sum') if 'quantity' in fs.columns else ('total_amount','count'),
            Transactions=('total_amount','count'),
            Avg_Price=('total_amount','mean')
        ).reset_index().sort_values('Total_Revenue', ascending=False)
        excel_prod = to_excel_bytes({'Product_Summary': prod_summary})
        st.download_button("📥 Download Product Report", data=excel_prod,
                           file_name=f"lingam_products_{datetime.now().strftime('%Y%m%d')}.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           use_container_width=True)

    with c3:
        st.markdown("#### 📅 Monthly Summary")
        fs_dl = fs.copy()
        fs_dl['Month'] = fs_dl['date'].dt.strftime('%b %Y')
        monthly_dl = fs_dl.groupby('Month').agg(
            Revenue=('total_amount','sum'),
            Invoices=('total_amount','count'),
        ).reset_index()
        excel_monthly = to_excel_bytes({'Monthly_Summary': monthly_dl})
        st.download_button("📥 Download Monthly Report", data=excel_monthly,
                           file_name=f"lingam_monthly_{datetime.now().strftime('%Y%m%d')}.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           use_container_width=True)

    if 'customer_id' in fs.columns:
        st.markdown("<br>", unsafe_allow_html=True)
        c4, c5, _ = st.columns(3)
        with c4:
            st.markdown("#### 👥 Customer Report")
            cust_dl = fs.groupby('customer_id').agg(
                Total_Spent=('total_amount','sum'),
                Visits=('total_amount','count'),
                Last_Visit=('date','max')
            ).reset_index().sort_values('Total_Spent', ascending=False)
            excel_cust = to_excel_bytes({'Customer_Report': cust_dl})
            st.download_button("📥 Download Customer Report", data=excel_cust,
                               file_name=f"lingam_customers_{datetime.now().strftime('%Y%m%d')}.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                               use_container_width=True)
        with c5:
            if 'quantity' in fs.columns:
                st.markdown("#### ☠️ Dead Stock Report")
                dead_dl = fs.groupby('product_name')['quantity'].sum().reset_index()
                dead_dl = dead_dl[dead_dl['quantity'] <= 5].sort_values('quantity')
                excel_dead = to_excel_bytes({'Dead_Stock': dead_dl})
                st.download_button("📥 Download Dead Stock Report", data=excel_dead,
                                   file_name=f"lingam_deadstock_{datetime.now().strftime('%Y%m%d')}.xlsx",
                                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                   use_container_width=True)

# ────────────────────────────────────
# TAB 11: OVERALL REPORT
# ────────────────────────────────────
with tabs[10]:
    st.markdown('<div class="section-title">📋 Overall Report — Inventory & Invoice Analytics</div>', unsafe_allow_html=True)

    if overall_inv_df is None and overall_inv2_df is None:
        st.markdown("""
        <div style="background:#fff;border-radius:16px;padding:3rem 2rem;text-align:center;
                    box-shadow:0 4px 20px rgba(0,0,0,0.07);border:1px solid #e2ecf7;">
          <div style="font-size:3.5rem;margin-bottom:0.8rem;">📋</div>
          <h3 style="color:#0d2137 !important;font-weight:800;margin-bottom:0.5rem;">Upload Overall Report Data</h3>
          <p style="color:#4a6680 !important;max-width:480px;margin:0 auto 1rem auto;font-size:0.92rem;line-height:1.6;">
            Upload the <strong>overall_report_data.xlsx</strong> file (or your merged_data file)
            using the <strong>📋 Overall Report Data</strong> uploader in the sidebar.<br><br>
            The file must have sheets: <code>Inventory_Monthly</code> and <code>Invoice_Monthly</code>.
          </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # ── MONTH SELECTOR ────────────────────────────────────────────────────
        all_months = []
        if overall_inv_df is not None and 'Month' in overall_inv_df.columns:
            all_months = sorted(overall_inv_df['Month'].dropna().unique().tolist())
        elif overall_inv2_df is not None and 'Month' in overall_inv2_df.columns:
            all_months = sorted(overall_inv2_df['Month'].dropna().unique().tolist())

        month_labels = {m: pd.Timestamp(m+"-01").strftime("%B %Y") for m in all_months}
        label_to_key = {v: k for k, v in month_labels.items()}

        col_sel, col_all = st.columns([3, 1])
        with col_sel:
            view_mode = st.radio("View Mode", ["Single Month", "All Months (Full Year)"], horizontal=True, label_visibility="collapsed")
        with col_all:
            if all_months:
                selected_label = st.selectbox("Select Month", list(month_labels.values()),
                                               index=len(month_labels)-1,
                                               disabled=(view_mode=="All Months (Full Year)"))
                selected_month = label_to_key.get(selected_label, all_months[-1]) if all_months else None

        # Filter by month
        def filt_month(df, col='Month'):
            if df is None or col not in df.columns: return df
            if view_mode == "All Months (Full Year)": return df
            return df[df[col] == selected_month].copy()

        inv_f  = filt_month(overall_inv_df)
        inv2_f = filt_month(overall_inv2_df)

        period_label = selected_label if view_mode == "Single Month" else "Full Year 2024"
        st.markdown(f"<div style='background:#e8f0fe;border-radius:8px;padding:0.5rem 1rem;"
                    f"color:#1a237e !important;font-size:0.85rem;font-weight:600;margin-bottom:1rem;display:inline-block;'>"
                    f"📅 Showing: {period_label}</div>", unsafe_allow_html=True)

        # ── TOP KPIs ──────────────────────────────────────────────────────────
        if inv_f is not None and len(inv_f):
            tot_inward_val   = inv_f['PURCHASE STOCK VALUE'].sum() if 'PURCHASE STOCK VALUE' in inv_f.columns else 0
            tot_sales_val    = inv_f['SALES VALUE'].sum() if 'SALES VALUE' in inv_f.columns else 0
            tot_profit       = inv_f['FINAL PROFIT'].sum() if 'FINAL PROFIT' in inv_f.columns else 0
            tot_remain_val   = inv_f['REMAINING STOCK VALUE'].sum() if 'REMAINING STOCK VALUE' in inv_f.columns else 0
            tot_remain_qty   = inv_f['REMAINING STOCK QTY'].sum() if 'REMAINING STOCK QTY' in inv_f.columns else 0
            profit_pct       = (tot_profit/tot_sales_val*100) if tot_sales_val else 0

            k1,k2,k3,k4,k5,k6 = st.columns(6)
            k1.markdown(kpi("🏭 Purchase Value",  f"₹{tot_inward_val:,.0f}", period_label), unsafe_allow_html=True)
            k2.markdown(kpi("💰 Sales Value",     f"₹{tot_sales_val:,.0f}", "", "green"), unsafe_allow_html=True)
            k3.markdown(kpi("📈 Gross Profit",    f"₹{tot_profit:,.0f}", "", "teal"), unsafe_allow_html=True)
            k4.markdown(kpi("📊 Profit Margin",   f"{profit_pct:.1f}%", "", "purple"), unsafe_allow_html=True)
            k5.markdown(kpi("📦 Remaining Stock", f"₹{tot_remain_val:,.0f}", "", "orange"), unsafe_allow_html=True)
            k6.markdown(kpi("🔢 Remaining Qty",   f"{tot_remain_qty:,.0f}", "units", "red"), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── SECTION A: INVENTORY ANALYTICS ───────────────────────────────────
        if inv_f is not None and len(inv_f):
            st.markdown('<div class="section-title">📦 Inventory Performance</div>', unsafe_allow_html=True)

            # 1. Sales Value vs Purchase Value by Product
            c1, c2 = st.columns(2)
            with c1:
                prod_grp = inv_f.groupby('PRODUCT NAME').agg(
                    Purchase_Value=('PURCHASE STOCK VALUE','sum'),
                    Sales_Value=('SALES VALUE','sum'),
                    Profit=('FINAL PROFIT','sum')
                ).reset_index().sort_values('Sales_Value', ascending=False).head(15)

                fig = go.Figure()
                fig.add_bar(x=prod_grp['PRODUCT NAME'], y=prod_grp['Purchase_Value'],
                            name='Purchase Value', marker_color='#90caf9')
                fig.add_bar(x=prod_grp['PRODUCT NAME'], y=prod_grp['Sales_Value'],
                            name='Sales Value', marker_color='#1565c0')
                apply_template(fig, "Purchase vs Sales Value — Top 15 Products")
                fig.update_layout(barmode='group', xaxis_tickangle=-40, legend=dict(
                    orientation='h', y=1.1, bgcolor='rgba(0,0,0,0)'))
                st.plotly_chart(fig, use_container_width=True)

            with c2:
                # Profit by product (top 15)
                prod_profit = inv_f.groupby('PRODUCT NAME')['FINAL PROFIT'].sum().reset_index()
                prod_profit = prod_profit[prod_profit['FINAL PROFIT'] > 0].sort_values('FINAL PROFIT', ascending=False).head(15)
                fig2 = px.bar(prod_profit, x='PRODUCT NAME', y='FINAL PROFIT',
                              color='FINAL PROFIT', color_continuous_scale='Greens', text_auto='.2s')
                apply_template(fig2, "Gross Profit by Product")
                fig2.update_layout(coloraxis_showscale=False, xaxis_tickangle=-40)
                st.plotly_chart(fig2, use_container_width=True)

            # 2. Sales Channel breakdown — Retail / Wholesale / Custom
            st.markdown('<div class="section-title">🔀 Sales Channel Breakdown</div>', unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)

            with c1:
                channel_vals = {
                    'Retail':    inv_f['RETAIL SALES VALUE'].sum()    if 'RETAIL SALES VALUE'    in inv_f.columns else 0,
                    'Wholesale': inv_f['WHOLESALE VALUE'].sum()       if 'WHOLESALE VALUE'       in inv_f.columns else 0,
                    'Wholesale2':inv_f['WHOLESALE_2 VALUE'].sum()     if 'WHOLESALE_2 VALUE'     in inv_f.columns else 0,
                    'Custom':    inv_f['CUSTOM SALES VALUE'].sum()    if 'CUSTOM SALES VALUE'    in inv_f.columns else 0,
                }
                ch_df = pd.DataFrame({'Channel': list(channel_vals.keys()), 'Value': list(channel_vals.values())})
                ch_df = ch_df[ch_df['Value'] > 0]
                fig3 = px.pie(ch_df, names='Channel', values='Value', hole=0.45,
                              color_discrete_sequence=PALETTE)
                apply_template(fig3, "Revenue by Sales Channel")
                st.plotly_chart(fig3, use_container_width=True)

            with c2:
                channel_profit = {
                    'Retail':    inv_f['RETAIL PROFIT'].sum()    if 'RETAIL PROFIT'    in inv_f.columns else 0,
                    'Wholesale': inv_f['WHOLESALE PROFIT'].sum() if 'WHOLESALE PROFIT' in inv_f.columns else 0,
                    'Wholesale2':inv_f['WHOLESALE_2 PROFIT'].sum() if 'WHOLESALE_2 PROFIT' in inv_f.columns else 0,
                    'Custom':    inv_f['CUSTOM PROFIT'].sum()    if 'CUSTOM PROFIT'    in inv_f.columns else 0,
                }
                cp_df = pd.DataFrame({'Channel': list(channel_profit.keys()), 'Profit': list(channel_profit.values())})
                cp_df = cp_df[cp_df['Profit'] > 0]
                fig4 = px.bar(cp_df, x='Channel', y='Profit', color='Channel',
                              color_discrete_sequence=PALETTE, text_auto='.2s')
                apply_template(fig4, "Profit by Sales Channel")
                fig4.update_layout(showlegend=False)
                st.plotly_chart(fig4, use_container_width=True)

            with c3:
                # Channel qty
                channel_qty = {
                    'Retail':    inv_f['RETAIL SALES QTY'].sum()    if 'RETAIL SALES QTY'    in inv_f.columns else 0,
                    'Wholesale': inv_f['WHOLESALE SALES QTY'].sum() if 'WHOLESALE SALES QTY' in inv_f.columns else 0,
                    'Wholesale2':inv_f['WHOLESALE_2 SALES QTY'].sum() if 'WHOLESALE_2 SALES QTY' in inv_f.columns else 0,
                    'Custom':    inv_f['CUSTOM SALES QTY'].sum()    if 'CUSTOM SALES QTY'    in inv_f.columns else 0,
                }
                cq_df = pd.DataFrame({'Channel': list(channel_qty.keys()), 'Qty': list(channel_qty.values())})
                cq_df = cq_df[cq_df['Qty'] > 0]
                fig5 = px.pie(cq_df, names='Channel', values='Qty', hole=0.45,
                              color_discrete_sequence=[PALETTE[i] for i in [1,4,2,5]])
                apply_template(fig5, "Quantity by Sales Channel")
                st.plotly_chart(fig5, use_container_width=True)

            # 3. Category-wise summary
            if 'Category' in inv_f.columns:
                st.markdown('<div class="section-title">🏷️ Category Analysis</div>', unsafe_allow_html=True)
                cat_grp = inv_f.groupby('Category').agg(
                    Purchase_Value=('PURCHASE STOCK VALUE','sum'),
                    Sales_Value=('SALES VALUE','sum'),
                    Profit=('FINAL PROFIT','sum'),
                    Products=('PRODUCT NAME','nunique'),
                    Inward_Qty=('INWARD QTY','sum')
                ).reset_index()
                c1, c2 = st.columns(2)
                with c1:
                    fig6 = px.bar(cat_grp, x='Category', y=['Purchase_Value','Sales_Value'],
                                  barmode='group', color_discrete_sequence=[PALETTE[0], PALETTE[1]],
                                  text_auto='.2s')
                    apply_template(fig6, "Category: Purchase vs Sales Value")
                    fig6.update_layout(legend=dict(orientation='h', y=1.1, bgcolor='rgba(0,0,0,0)'))
                    st.plotly_chart(fig6, use_container_width=True)
                with c2:
                    fig7 = px.treemap(cat_grp, path=['Category'], values='Sales_Value',
                                      color='Profit', color_continuous_scale='RdYlGn',
                                      hover_data=['Products','Inward_Qty'])
                    apply_template(fig7, "Category Treemap — Sales Value (color = Profit)")
                    st.plotly_chart(fig7, use_container_width=True)

            # 4. Remaining stock risk
            st.markdown('<div class="section-title">🏗️ Remaining Stock Overview</div>', unsafe_allow_html=True)
            if 'REMAINING STOCK QTY' in inv_f.columns:
                rem_df = inv_f.groupby('PRODUCT NAME').agg(
                    Remaining_Qty=('REMAINING STOCK QTY','sum'),
                    Remaining_Value=('REMAINING STOCK VALUE','sum'),
                    Inward_Qty=('INWARD QTY','sum')
                ).reset_index()
                rem_df['Stock_Utilisation_%'] = ((rem_df['Inward_Qty'] - rem_df['Remaining_Qty'])
                                                  / rem_df['Inward_Qty'] * 100).clip(0,100).round(1)
                rem_df = rem_df.sort_values('Remaining_Value', ascending=False).head(20)

                c1, c2 = st.columns(2)
                with c1:
                    fig8 = px.bar(rem_df.head(15), x='PRODUCT NAME', y='Remaining_Value',
                                  color='Remaining_Value', color_continuous_scale='Oranges', text_auto='.2s')
                    apply_template(fig8, "Remaining Stock Value (Top 15)")
                    fig8.update_layout(coloraxis_showscale=False, xaxis_tickangle=-40)
                    st.plotly_chart(fig8, use_container_width=True)
                with c2:
                    fig9 = px.bar(rem_df.head(15), x='PRODUCT NAME', y='Stock_Utilisation_%',
                                  color='Stock_Utilisation_%', color_continuous_scale='RdYlGn',
                                  text_auto='.1f')
                    apply_template(fig9, "Stock Utilisation % (100% = fully sold)")
                    fig9.update_layout(coloraxis_showscale=False, xaxis_tickangle=-40, yaxis_range=[0,110])
                    st.plotly_chart(fig9, use_container_width=True)

            # 5. Monthly trend (only in All Months view)
            if view_mode == "All Months (Full Year)" and 'Month' in overall_inv_df.columns:
                st.markdown('<div class="section-title">📆 Monthly Inventory Trends</div>', unsafe_allow_html=True)
                mon_trend = overall_inv_df.groupby('Month').agg(
                    Purchase_Value=('PURCHASE STOCK VALUE','sum'),
                    Sales_Value=('SALES VALUE','sum'),
                    Profit=('FINAL PROFIT','sum'),
                    Remaining_Value=('REMAINING STOCK VALUE','sum')
                ).reset_index().sort_values('Month')
                mon_trend['Month_Label'] = mon_trend['Month'].apply(
                    lambda m: pd.Timestamp(m+"-01").strftime("%b %Y"))

                fig10 = go.Figure()
                fig10.add_trace(go.Scatter(x=mon_trend['Month_Label'], y=mon_trend['Purchase_Value'],
                                           name='Purchase Value', line=dict(color='#90caf9', width=2.5), mode='lines+markers'))
                fig10.add_trace(go.Scatter(x=mon_trend['Month_Label'], y=mon_trend['Sales_Value'],
                                           name='Sales Value', line=dict(color='#1565c0', width=2.5), mode='lines+markers'))
                fig10.add_trace(go.Scatter(x=mon_trend['Month_Label'], y=mon_trend['Profit'],
                                           name='Profit', line=dict(color='#2e7d32', width=2, dash='dash'), mode='lines+markers'))
                apply_template(fig10, "Monthly: Purchase Value vs Sales Value vs Profit")
                fig10.update_layout(legend=dict(orientation='h', y=1.1, bgcolor='rgba(0,0,0,0)'))
                st.plotly_chart(fig10, use_container_width=True)

                # Profit margin monthly
                mon_trend['Profit_Margin_%'] = (mon_trend['Profit'] / mon_trend['Sales_Value'] * 100).round(2)
                fig11 = px.bar(mon_trend, x='Month_Label', y='Profit_Margin_%',
                               color='Profit_Margin_%', color_continuous_scale='RdYlGn', text_auto='.1f')
                apply_template(fig11, "Monthly Profit Margin %")
                fig11.update_layout(coloraxis_showscale=False)
                st.plotly_chart(fig11, use_container_width=True)

            # 6. Summary table
            st.markdown('<div class="section-title">📊 Detailed Inventory Table</div>', unsafe_allow_html=True)
            show_cols = [c for c in ['PRODUCT NAME','Category','INWARD QTY','INWARD PRICE',
                          'RETAIL SALES QTY','RETAIL SALES VALUE','RETAIL PROFIT',
                          'WHOLESALE VALUE','WHOLESALE PROFIT',
                          'REMAINING STOCK QTY','REMAINING STOCK VALUE',
                          'PURCHASE STOCK VALUE','SALES VALUE','FINAL PROFIT'] if c in inv_f.columns]
            inv_table = inv_f[show_cols].copy()
            for mc in ['RETAIL SALES VALUE','RETAIL PROFIT','WHOLESALE VALUE','WHOLESALE PROFIT',
                       'REMAINING STOCK VALUE','PURCHASE STOCK VALUE','SALES VALUE','FINAL PROFIT']:
                if mc in inv_table.columns:
                    inv_table[mc] = inv_table[mc].apply(lambda x: f"₹{x:,.0f}" if pd.notna(x) else '-')
            st.dataframe(inv_table, use_container_width=True, hide_index=True)

        # ── SECTION B: INVOICE ANALYTICS ─────────────────────────────────────
        if inv2_f is not None and len(inv2_f):
            st.markdown('<div class="section-title">🧾 Invoice & Sales Analytics</div>', unsafe_allow_html=True)

            iv_rev    = inv2_f['Total Amount'].sum() if 'Total Amount' in inv2_f.columns else 0
            iv_bills  = inv2_f['Invoice No.'].nunique() if 'Invoice No.' in inv2_f.columns else len(inv2_f)
            iv_qty    = inv2_f['Quantity'].sum() if 'Quantity' in inv2_f.columns else 0
            iv_avg    = iv_rev / iv_bills if iv_bills else 0

            k1, k2, k3, k4 = st.columns(4)
            k1.markdown(kpi("💰 Invoice Revenue",  f"₹{iv_rev:,.0f}",  period_label), unsafe_allow_html=True)
            k2.markdown(kpi("🧾 Invoices Raised",  f"{iv_bills:,}",    "", "green"),   unsafe_allow_html=True)
            k3.markdown(kpi("📦 Units Invoiced",   f"{iv_qty:,.0f}",   "", "orange"),  unsafe_allow_html=True)
            k4.markdown(kpi("📈 Avg Invoice Value",f"₹{iv_avg:,.0f}",  "", "purple"),  unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)

            with c1:
                # Top products by invoice value
                if 'Item Name' in inv2_f.columns and 'Total Amount' in inv2_f.columns:
                    top_inv = inv2_f.groupby('Item Name')['Total Amount'].sum().nlargest(15).reset_index()
                    fig12 = px.bar(top_inv, x='Total Amount', y='Item Name', orientation='h',
                                   color='Total Amount', color_continuous_scale='Blues')
                    apply_template(fig12, "Top 15 Products by Invoice Value")
                    fig12.update_layout(yaxis=dict(autorange='reversed'), coloraxis_showscale=False)
                    st.plotly_chart(fig12, use_container_width=True)

            with c2:
                # Customer breakdown
                if 'Customer Name' in inv2_f.columns and 'Total Amount' in inv2_f.columns:
                    cust_inv = inv2_f.groupby('Customer Name')['Total Amount'].sum().reset_index().sort_values('Total Amount', ascending=False)
                    fig13 = px.pie(cust_inv.head(10), names='Customer Name', values='Total Amount',
                                   hole=0.4, color_discrete_sequence=PALETTE)
                    apply_template(fig13, "Invoice Revenue by Customer")
                    st.plotly_chart(fig13, use_container_width=True)

            # Monthly invoice trend (Full Year view)
            if view_mode == "All Months (Full Year)" and 'Month' in overall_inv2_df.columns:
                mon_inv = overall_inv2_df.groupby('Month').agg(
                    Revenue=('Total Amount','sum'),
                    Invoices=('Invoice No.','nunique'),
                    Qty=('Quantity','sum')
                ).reset_index().sort_values('Month')
                mon_inv['Month_Label'] = mon_inv['Month'].apply(
                    lambda m: pd.Timestamp(str(m)+"-01").strftime("%b %Y"))
                mon_inv['Avg_Invoice'] = mon_inv['Revenue'] / mon_inv['Invoices']

                c1, c2 = st.columns(2)
                with c1:
                    fig14 = px.bar(mon_inv, x='Month_Label', y='Revenue',
                                   color_discrete_sequence=[PALETTE[0]], text_auto='.2s')
                    apply_template(fig14, "Monthly Invoice Revenue")
                    st.plotly_chart(fig14, use_container_width=True)
                with c2:
                    fig15 = go.Figure()
                    fig15.add_bar(x=mon_inv['Month_Label'], y=mon_inv['Invoices'],
                                  name='Invoices', marker_color=PALETTE[1], yaxis='y')
                    fig15.add_scatter(x=mon_inv['Month_Label'], y=mon_inv['Avg_Invoice'],
                                      name='Avg Invoice ₹', mode='lines+markers',
                                      line=dict(color=PALETTE[2], width=2.5), yaxis='y2')
                    apply_template(fig15, "Invoice Count & Avg Invoice Value")
                    fig15.update_layout(
                        yaxis=dict(title='Invoice Count'),
                        yaxis2=dict(title='Avg Invoice ₹', overlaying='y', side='right'),
                        legend=dict(orientation='h', y=1.1, bgcolor='rgba(0,0,0,0)')
                    )
                    st.plotly_chart(fig15, use_container_width=True)

            # Category mix from invoices
            if 'Category' in inv2_f.columns and 'Total Amount' in inv2_f.columns:
                st.markdown('<div class="section-title">🏷️ Invoice Category Mix</div>', unsafe_allow_html=True)
                cat_inv = inv2_f.groupby('Category').agg(
                    Revenue=('Total Amount','sum'),
                    Qty=('Quantity','sum'),
                    Count=('Invoice No.','count')
                ).reset_index()
                c1, c2 = st.columns(2)
                with c1:
                    fig16 = px.pie(cat_inv, names='Category', values='Revenue', hole=0.4,
                                   color_discrete_sequence=PALETTE)
                    apply_template(fig16, "Invoice Revenue by Category")
                    st.plotly_chart(fig16, use_container_width=True)
                with c2:
                    fig17 = px.bar(cat_inv, x='Category', y='Qty',
                                   color='Category', color_discrete_sequence=PALETTE, text_auto=True)
                    apply_template(fig17, "Units Invoiced by Category")
                    fig17.update_layout(showlegend=False)
                    st.plotly_chart(fig17, use_container_width=True)

            # Invoice data table
            st.markdown('<div class="section-title">📋 Invoice Details Table</div>', unsafe_allow_html=True)
            show_inv2 = [c for c in ['Invoice No.','Bill Date','Customer Name','Item Name',
                          'Category','Quantity','Unit Price','Discount','Tax Percent','Total Amount']
                          if c in inv2_f.columns]
            inv2_table = inv2_f[show_inv2].copy().head(200)
            if 'Total Amount' in inv2_table.columns:
                inv2_table['Total Amount'] = inv2_table['Total Amount'].apply(
                    lambda x: f"₹{x:,.2f}" if pd.notna(x) else '-')
            st.dataframe(inv2_table, use_container_width=True, hide_index=True)

        # ── DOWNLOAD ──────────────────────────────────────────────────────────
        if inv_f is not None or inv2_f is not None:
            st.markdown('<div class="section-title">📥 Export Overall Report</div>', unsafe_allow_html=True)
            dl_sheets = {}
            if inv_f is not None:  dl_sheets['Inventory'] = inv_f
            if inv2_f is not None: dl_sheets['Invoices']  = inv2_f
            excel_or = to_excel_bytes(dl_sheets)
            st.download_button("📥 Download Overall Report Excel",
                               data=excel_or,
                               file_name=f"lingam_overall_report_{datetime.now().strftime('%Y%m%d')}.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# ────────────────────────────────────
# FOOTER
# ────────────────────────────────────
st.markdown(f"""
<div class="footer">
  🛒 <strong>Lingam Supermarket Analytics</strong> &nbsp;|&nbsp;
  Powered by Streamlit &nbsp;|&nbsp;
  Last Updated: {datetime.now().strftime('%d %b %Y, %I:%M %p')}
</div>
""", unsafe_allow_html=True)
