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
    padding: 12px 24px !important; box-shadow: 0 4px 10px rgba(18,77,97,0.2);
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
    
    st.markdown('<a class="nav-link" href="#lembar-1-panduan">📖 Lembar 1: Panduan</a>', unsafe_allow_html=True)
    st.markdown('<a class="nav-link" href="#lembar-2-input-data">📂 Lembar 2: Input Data</a>', unsafe_allow_html=True)
    st.markdown('<a class="nav-link" href="#lembar-3-hasil-perhitungan">📊 Lembar 3: Hasil & Grafik</a>', unsafe_allow_html=True)

# ─── Hero Banner ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">✨ Weighted Shortest Processing Time (WSPT) Dashboard</div>
    <div class="hero-sub">Sistem Optimasi Urutan Penjadwalan Kerja dalam Lembar Terkotak Nyaman</div>
</div>
""", unsafe_allow_html=True)

# Inisialisasi Session State untuk pemicu kalkulasi agar tidak otomatis terhitung di awal
if 'calculated' not in st.session_state:
    st.session_state.calculated = False

# Inisialisasi awal tabel kosong agar diisi mandiri oleh pengguna
if 'df_input_data' not in st.session_state:
    st.session_state.df_input_data = pd.DataFrame([
        {"Job_Name": "", "Processing_Time": None, "Weight": None}
    ])

# ─── LEMBAR 1: PANDUAN & ATURAN ───────────────────────────────────────────────
st.markdown('<div id="lembar-1-panduan"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-sheet">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📖 Lembar 1: Aturan WSPT & Petunjuk Penggunaan</div>', unsafe_allow_html=True)
st.markdown("""
**⏱️ Landasan Teori Aturan WSPT:**
Metode **WSPT (Weighted Shortest Processing Time)** digunakan untuk mengoptimalkan urutan pengerjaan tugas pada satu mesin tunggal (*Single Machine Scheduling*). Aturan utamanya adalah mengurutkan pekerjaan berdasarkan rasio nilai **Waktu Proses dibagi dengan Bobot Kepentingan** ($t_j / W_j$) dari urutan yang **paling kecil hingga terbesar**. Metode ini terbukti meminimalkan *Total Weighted Flow Time*.

**📘 Cara Penggunaan Aplikasi:**
1. Gulir ke bawah ke **Lembar 2** atau klik menu di sidebar kiri.
2. Masukkan data secara manual di komponen tabel editor (gunakan tombol `+` di bawah tabel untuk menambah baris baru) atau pilih metode upload berkas `.csv`.
3. Tekan tombol **▶️ Hitung Penjadwalan WSPT**.
4. Hasil pengurutan detail, ringkasan nilai, dan chart linimasa pengerjaan akan langsung tersaji lengkap pada **Lembar 3**.
""")
st.markdown('</div>', unsafe_allow_html=True)

# ─── LEMBAR 2: INPUT DATA (MANUAL & OTOMATIS) ──────────────────────────────────
st.markdown('<div id="lembar-2-input-data"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-sheet">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📂 Lembar 2: Input Data Job (Pekerjaan)</div>', unsafe_allow_html=True)

input_method = st.radio(
    "Pilih Metode Memasukkan Data:",
    ["Manual Input (Ketik di Tabel)", "Otomatis (Upload File CSV)"],
    horizontal=True
)

st.markdown("<br>", unsafe_allow_html=True)

if "Manual Input" in input_method:
    edited_df = st.data_editor(
        st.session_state.df_input_data,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Job_Name": st.column_config.TextColumn("Nama Job / Pekerjaan", required=True, placeholder="contoh: Job 1"),
            "Processing_Time": st.column_config.NumberColumn("Waktu Proses ($t_j$)", min_value=1, step=1, format="%d"),
            "Weight": st.column_config.NumberColumn("Bobot ($W_j$)", min_value=1, step=1, format="%d")
        }
    )
    # Filter baris kosong yang belum diisi oleh pengguna agar tidak memicu error sistem
    st.session_state.df_input_data = edited_df
else:
    uploaded_file = st.file_uploader("Unggah file CSV Anda di sini (Pastikan judul kolom: Job_Name, Processing_Time, Weight)", type=["csv"])
    if uploaded_file is not None:
        try:
            uploaded_df = pd.read_csv(uploaded_file)
            st.session_state.df_input_data = uploaded_df
            st.success("✅ File CSV Berhasil Dimuat!")
            st.dataframe(uploaded_df, use_container_width=True)
        except Exception as e:
            st.error(f"Gagal membaca file CSV, pastikan formatnya benar. Error: {e}")

st.markdown("<br>", unsafe_allow_html=True)
if st.button("▶️ Hitung Penjadwalan WSPT", type="primary"):
    st.session_state.calculated = True
st.markdown('</div>', unsafe_allow_html=True)

# ─── LEMBAR 3: HASIL PERHITUNGAN & DOWNLOAD ──────────────────────────────────
st.markdown('<div id="lembar-3-hasil-perhitungan"></div>', unsafe_allow_html=True)

# Lakukan penyaringan data masukan pengguna
df_clean = st.session_state.df_input_data.copy()
df_clean = df_clean.dropna(subset=["Processing_Time", "Weight"])
df_clean = df_clean[df_clean["Job_Name"].str.strip() != ""]

# Tampilkan halaman Lembar 3 dalam keadaan terkotak rapi
st.markdown('<div class="section-sheet">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📊 Lembar 3: Hasil Perhitungan & Grafik Linimasa</div>', unsafe_allow_html=True)

if st.session_state.calculated and len(df_clean) > 0:
    # ─── WSPT Calculation Logic (TIDAK BERUBAH) ───────────────────────────
    df_clean["Rasio_tj_Wj"] = df_clean["Processing_Time"] / df_clean["Weight"]
    df_wspt = df_clean.sort_values(by=["Rasio_tj_Wj", "Processing_Time"], ascending=[True, True]).reset_index(drop=True)
    
    start_times = []
    flow_times = []
    current_time = 0
    
    for idx, row in df_wspt.iterrows():
        start_times.append(current_time)
        current_time += int(row["Processing_Time"])
        flow_times.append(current_time)
        
    df_wspt["Start_Time"] = start_times
    df_wspt["Flow_Time"] = flow_times
    df_wspt["Weighted_Flow_Time"] = df_wspt["Weight"] * df_wspt["Flow_Time"]
    
    total_flow_time = df_wspt["Flow_Time"].sum()
    total_weighted_flow_time = df_wspt["Weighted_Flow_Time"].sum()
    total_weight = df_wspt["Weight"].sum()
    num_jobs = len(df_wspt)
    
    mean_flow_time = total_flow_time / num_jobs
    mean_weighted_flow_time = total_weighted_flow_time / total_weight

    # 1. Ringkasan Metrik Angka
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""<div class="metric-card primary"><div class="metric-label">Total Flow Time</div><div class="metric-value">{total_flow_time}</div><div class="metric-sub">Jumlah total waktu alir</div></div>""", unsafe_allow_html=True)
    with m2:
        st.markdown(f"""<div class="metric-card secondary"><div class="metric-label">Rata-rata Flow Time</div><div class="metric-value">{mean_flow_time:.2f}</div><div class="metric-sub">{total_flow_time} / {num_jobs} (Total Job)</div></div>""", unsafe_allow_html=True)
    with m3:
        st.markdown(f"""<div class="metric-card accent"><div class="metric-label">Rata-rata Flow Time Tertimbang</div><div class="metric-value">{mean_weighted_flow_time:.5f}</div><div class="metric-sub">{total_weighted_flow_time} / {total_weight} (Total Bobot)</div></div>""", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("**Tabel Perhitungan Urutan Hasil Optimasi WSPT (Dijabarkan):**")
    
    # 2. Tabel Penjabaran Detail
    df_wspt["Sequence"] = [f"Urutan {i+1}" for i in range(len(df_wspt))]
    df_display = df_wspt.set_index("Sequence")[["Job_Name", "Rasio_tj_Wj", "Weight", "Processing_Time", "Flow_Time", "Weighted_Flow_Time"]]
    df_display.columns = ["Job", "t_j / W_j", "Bobot", "Waktu", "Flow Time", "Weighted Flow Time"]
    
    st.dataframe(df_display.style.format({"t_j / W_j": "{:.1f}"}), use_container_width=True)
    
    job_order = "-".join([str(name).replace("Job ", "") for name in df_wspt["Job_Name"]])
    st.success(f"📌 **Urutan Akhir yang Terbentuk:** {job_order}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**Visualisasi Timeline Gantt Chart:**")
    
    # 3. Visualisasi Gantt Chart (Plotly menyediakan tombol unduh gambar bawaan)
    fig_gantt = go.Figure()
    custom_colors = ['#accad7', '#87BDD8', '#5B9AA0', '#4F8A8B', '#1e7796', '#124d61', '#3A6073', '#709FB0']
    
    for idx, row in df_wspt.iterrows():
        fig_gantt.add_trace(go.Bar(
            x=[row["Processing_Time"]],
            y=["Mesin Tunggal"],
            base=[row["Start_Time"]],
            orientation='h',
            name=row["Job_Name"],
            text=f"{row['Job_Name']}",
            textposition='inside',
            marker=dict(color=custom_colors[idx % len(custom_colors)], line=dict(color='white', width=2))
        ))
        
    fig_gantt.update_layout(
        barmode='stack', height=220, plot_bgcolor="#FFFFFF", paper_bgcolor="rgba(0,0,0,0)",
        showlegend=True, margin=dict(l=10, r=10, t=20, b=20),
        xaxis=dict(title="Sumbu Linimasa Waktu", gridcolor="#F0F4F6", tickvals=[0] + list(df_wspt["Flow_Time"])),
        yaxis=dict(showticklabels=False)
    )
    st.plotly_chart(fig_gantt, use_container_width=True)
    
    st.markdown("""
    💡 *Tip: Untuk menyimpan Gantt Chart menjadi gambar (.png), arahkan kursor Anda ke area kanan atas grafik tersebut, lalu klik ikon kamera (**"Download plot as a png"**).*
    """)
    
    # 4. Tombol Download Tabel Hasil
    csv_buffer = BytesIO()
    df_display.to_csv(csv_buffer, index=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.download_button(
        label="📥 Unduh Hasil Tabel Penjadwalan (.CSV)",
        data=csv_buffer.getvalue(),
        file_name="hasil_penjadwalan_wspt.csv",
        mime="text/csv"
    )
else:
    st.info("Waiting for Data... Silakan isi data pekerjaan di Lembar 2, lalu klik tombol 'Hitung Penjadwalan WSPT' untuk menampilkan hasil analisa di sini.")

st.markdown('</div>', unsafe_allow_html=True)
