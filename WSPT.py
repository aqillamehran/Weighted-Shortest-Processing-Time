import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

st.set_page_config(
    page_title="WSPT Scheduler · Cute Edition",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS (Cute Style, Clean Base, & Custom Palette) ─────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght=400;500;600;700&family=DM+Mono:wght=400;500&display=swap');

html, body, [class*="css"] { font-family: 'Quicksand', sans-serif; scroll-behavior: smooth; }
.stApp { background: #FFFFFF; } 

/* SIDEBAR STYLE */
[data-testid="stSidebar"] { background: #accad7 !important; border-right: 2px solid #1e7796; }
[data-testid="stSidebar"] * { color: #124d61 !important; }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: #124d61 !important; font-weight: 700; }

/* HERO BANNER */
.hero-banner {
    background: linear-gradient(135deg, #124d61 0%, #1e7796 100%);
    border-radius: 24px; padding: 30px 35px; margin-bottom: 25px;
    box-shadow: 0 8px 20px rgba(30,119,150,0.15);
}
.hero-title { font-size: 26px; font-weight: 700; color: #FFFFFF; margin: 0 0 6px; }
.hero-sub { font-size: 13px; color: #accad7; margin: 0; }

/* CARD SECTION (KOTAK-KOTAK LEMBAR PEMBAHASAN) */
.section-sheet {
    background: #F4F8FA; border-radius: 20px; padding: 25px; margin-bottom: 35px;
    border: 2px solid #accad7; box-shadow: 0 4px 10px rgba(172,202,215,0.2);
}
.section-title { font-size: 20px; font-weight: 700; color: #124d61; margin-bottom: 15px; display: flex; align-items: center; gap: 8px; }

/* METRIC CARD STYLE */
.metric-card {
    background: white; border-radius: 16px; padding: 18px 20px;
    border: 2px solid #accad7; box-shadow: 0 4px 8px rgba(0,0,0,0.02);
    text-align: center;
}
.metric-card.primary { border-top: 5px solid #124d61; }
.metric-card.secondary { border-top: 5px solid #1e7796; }
.metric-card.accent { border-top: 5px solid #accad7; }

.metric-label { font-size: 11px; font-weight: 700; color: #1e7796; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 6px; }
.metric-value { font-size: 24px; font-weight: 700; color: #124d61; font-family: 'DM Mono', monospace; }
.metric-sub { font-size: 11px; color: #6b8894; margin-top: 3px; }

/* BUTTON STYLE */
div.stButton > button:first-child {
    background: linear-gradient(135deg, #1e7796 0%, #124d61 100%) !important;
    color: white !important; font-weight: 600 !important;
    border-radius: 12px !important; border: none !important;
    padding: 10px 24px !important; box-shadow: 0 4px 10px rgba(18,77,97,0.2);
    width: 100%;
}

/* LINK NAVIGATION SIDEBAR */
.nav-link {
    display: block; padding: 12px 15px; margin: 8px 0;
    background-color: #ffffff; color: #124d61 !important;
    text-decoration: none !important; font-weight: 600;
    border-radius: 10px; border: 1px solid #1e7796;
    transition: all 0.2s ease; text-align: center;
}
.nav-link:hover {
    background-color: #1e7796; color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

# ─── SIDEBAR: Navigasi Otomatis (Scroll ke Bawah) ────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 10px 0 10px'>
        <div style='font-size:24px; font-weight:700; color:#124d61;'>✨ WSPT Menu</div>
        <div style='font-size:12px; color:#124d61; opacity:0.8; margin-top:3px'>Klik untuk langsung meluncur ke lembar kerja:</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<hr style='border-color: #124d61;'>", unsafe_allow_html=True)
    
    # Membuat tombol navigasi HTML Anchor yang jika diklik otomatis
