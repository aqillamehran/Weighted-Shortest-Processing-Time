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

/* KOTAK BASE PEMBAHASAN (Melengkung, Background Putih, Border Tipis dengan Header Menyatu) */
.custom-base-box {
    background-color: #FFFFFF;
    border: 1px solid #accad7;
    border-top: 4px solid #1e7796;
    border-radius: 16px;
    padding: 30px;
    margin-bottom: 35px;
    box-shadow: 0 4px 12px rgba(172, 202, 215, 0.2);
}

/* JUDUL DI DALAM KOTAK */
.box-title-text {
    font-size: 20px;
    font-weight: 700;
    color: #124d61;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 10px;
}

/* HERO BANNER */
.hero-banner {
    background: linear-gradient(135deg, #124d61 0%, #1e7796 100%);
    border-radius: 24px; padding: 30px 35px; margin-bottom: 25px;
    box-shadow: 0 8px 20px rgba(30,119,150,0.15);
}
.hero-title { font-size: 26px; font-weight: 700; color: #FFFFFF; margin: 0 0 6px; }
.hero-sub { font-size: 13px; color: #accad7; margin: 0; }

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

# ─── INISIALISASI DATA KOSONG (Fix Bug Baris & Auto Clear) ───────────────────
if 'df_input_data' not in st.session_state:
    st.session_state.df_input_data = pd.DataFrame([{"Job_Name": "", "Processing_Time": None, "Weight": None}])

if 'calculated' not in st.session_state:
    st.session_state.calculated = False

# ─── SIDEBAR: Navigasi Tanpa Label Angka (Scroll ke Bawah) ────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 10px 0 10px'>
        <div style='font-size:24px; font-weight:700; color:#124d61;'>✨ WSPT Menu</div>
        <div style='font-size:12px; color:#124d61; opacity:0.8; margin-top:3px'>Klik untuk berpindah halaman:</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<hr style='border-color: #124d61;'>", unsafe_allow_html=True)
    
    st.markdown('<a class="nav-link" href="#aturan-wspt-panduan">📖 Aturan WSPT & Petunjuk Penggunaan</a>', unsafe_allow_html=True)
    st.markdown('<a class="nav-link" href="#input-data-job">📂 Input Data Job</a>', unsafe_allow_html=True)
    st.markdown('<a class="nav-link" href="#hasil-perhitungan-grafik">📊 Hasil Perhitungan & Grafik Linimasa</a>', unsafe_allow_html=True)

# ─── Hero Banner ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">✨ Weighted Shortest Processing Time (WSPT) Dashboard</div>
    <div class="hero-sub">Sistem Optimasi Urutan Penjadwalan Kerja dalam Lembar Terkotak Nyaman</div>
</div>
""", unsafe_allow_html=True)

# ─── KOTAK 1: ATURAN WSPT & PETUNJUK PENGGUNAAN ──────────────────────────────
st.markdown('<div id="aturan-wspt-panduan"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="custom-base-box">
    <div class="box-title-text">📖 Aturan WSPT & Petunjuk Penggunaan</div>
    <p><b>⚙️ Aturan WSPT:</b><br>
    Metode <b>WSPT (Weighted Shortest Processing Time)</b> digunakan untuk mengoptimalkan urutan pengerjaan tugas pada satu mesin tunggal (<i>Single Machine Scheduling</i>). Aturan utamanya adalah mengurutkan pekerjaan berdasarkan rasio nilai <b>Waktu Proses dibagi dengan Bobot Kepentingan</b> ($t_j / W_j$) dari urutan yang <b>paling kecil hingga terbesar</b>. Metode ini terbukti meminimalkan <i>Total Weighted Flow Time</i>.</p>
    <br>
    <p><b>📘 Cara Penggunaan Aplikasi:</b><br>
    1. Gulir ke bawah ke lembar <b>Input Data Job</b> atau klik tombol pintasan di sidebar kiri.<br>
    2. Masukkan data secara manual di tabel editor atau pilih metode upload dari file berkas Excel atau CSV.<br>
    3. Tekan tombol <b>▶️ Hitung Penjadwalan WSPT</b>.<br>
    4. Hasil pengurutan detail, ringkasan nilai, dan chart linimasa pengerjaan akan langsung tersaji lengkap pada lembar <b>Hasil Perhitungan & Grafik Linimasa</b>.</p>
</div>
""", unsafe_allow_html=True)

# ─── KOTAK 2: INPUT DATA JOB (KOSONG DAN BISA DITAMBAH SEPUASNYA) ─────────────
st.markdown('<div id="input-data-job"></div>', unsafe_allow_html=True)
st.markdown('<div class="custom-base-box">', unsafe_allow_html=True)
st.markdown('<div class="box-title-text">📂 Input Data Job (Pekerjaan)</div>', unsafe_allow_html=True)

input_method = st.radio(
    "Pilih Metode Memasukkan Data:",
    ["Manual Input (Ketik di Tabel)", "Otomatis (Upload File Excel / CSV)"],
    horizontal=True
)

st.markdown("<br>", unsafe_allow_html=True)

if "Manual Input" in input_method:
    edited_df = st.data_editor(
        st.session_state.df_input_data,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Job_Name": st.column_config.TextColumn("Nama Job / Pekerjaan", required=True),
            "Processing_Time": st.column_config.NumberColumn("Waktu Proses ($t_j$)", min_value=1, step=1, format="%d"),
            "Weight": st.column_config.NumberColumn("Bobot ($W_j$)", min_value=1, step=1, format="%d")
        },
        key="editor_grid"
    )
    st.session_state.df_input_data = edited_df
else:
    uploaded_file = st.file_uploader("Unggah file Excel (.xlsx) atau CSV Anda di sini (Pastikan judul kolom: Job_Name, Processing_Time, Weight)", type=["csv", "xlsx"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                uploaded_df = pd.read_csv(uploaded_file)
            else:
                uploaded_df = pd.read_excel(uploaded_file)
            st.session_state.df_input_data = uploaded_df
            st.success("✅ File Berhasil Dimuat!")
            st.dataframe(uploaded_df, use_container_width=True)
        except Exception as e:
            st.error(f"Gagal membaca file berkas, pastikan format kolom benar. Error: {e}")

st.markdown("<br>", unsafe_allow_html=True)
if st.button("▶️ Hitung Penjadwalan WSPT", type="primary"):
    valid_data = st.session_state.df_input_data.dropna(subset=["Job_Name", "Processing_Time", "Weight"])
    if len(valid_data) > 0:
        st.session_state.calculated = True
        st.success("🎉 Berhasil dihitung! Silakan gulir ke bawah untuk melihat hasil pengerjaan.")
    else:
        st.warning("Mohon masukkan setidaknya satu data pengerjaan job secara lengkap terlebih dahulu!")
st.markdown('</div>', unsafe_allow_html=True)

# ─── KOTAK 3: HASIL PERHITUNGAN & GRAFIK (HANYA MUNCUL JIKA SUDAH DIKLIK) ────
st.markdown('<div id="hasil-perhitungan-grafik"></div>', unsafe_allow_html=True)

# Bersihkan baris-baris kosong sebelum menjalankan formula pengerjaan
df_jobs = st.session_state.df_input_data.dropna(subset=["Job_Name", "Processing_Time", "Weight"]).copy()

if st.session_state.calculated and len(df_jobs) > 0:
    # ─── WSPT Calculation Logic (TIDAK BERUBAH) ───────────────────────────
    df_jobs["Rasio_tj_Wj"] = df_jobs["Processing_Time"] / df_jobs["Weight"]
    df_wspt = df_jobs.sort_values(by=["Rasio_tj_Wj", "Processing_Time"], ascending=[True, True]).reset_index(drop=True)
    
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

    st.markdown('<div class="custom-base-box">', unsafe_allow_html=True)
    st.markdown('<div class="box-title-text">📊 Hasil Perhitungan & Grafik Linimasa</div>', unsafe_allow_html=True)
    
    # 1. Tampilan Ringkasan Metrik
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""<div class="metric-card primary"><div class="metric-label">Total Flow Time</div><div class="metric-value">{total_flow_time}</div><div class="metric-sub">Jumlah total waktu alir</div></div>""", unsafe_allow_html=True)
    with m2:
        st.markdown(f"""<div class="metric-card secondary"><div class="metric-label">Rata-rata Flow Time</div><div class="metric-value">{mean_flow_time:.2f}</div><div class="metric-sub">{total_flow_time} / {num_jobs} Job</div></div>""", unsafe_allow_html=True)
    with m3:
        st.markdown(f"""<div class="metric-card accent"><div class="metric-label">Rata-rata Flow Time Tertimbang</div><div class="metric-value">{mean_weighted_flow_time:.5f}</div><div class="metric-sub">{total_weighted_flow_time} / {total_weight} Total Bobot</div></div>""", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("**Tabel Perhitungan Urutan Hasil Optimasi WSPT (Dijabarkan):**")
    
    # 2. Tabel Detail Hasil Penjadwalan
    df_wspt["Sequence"] = [f"Urutan {i+1}" for i in range(len(df_wspt))]
    df_display = df_wspt.set_index("Sequence")[["Job_Name", "Rasio_tj_Wj", "Weight", "Processing_Time", "Flow_Time", "Weighted_Flow_Time"]]
    df_display.columns = ["Job", "t_j / W_j", "Bobot", "Waktu", "Flow Time", "Weighted Flow Time"]
    
    st.dataframe(df_display.style.format({"t_j / W_j": "{:.1f}"}), use_container_width=True)
    
    job_order = "-".join([str(name).replace("Job ", "") for name in df_wspt["Job_Name"]])
    st.success(f"📌 **Urutan Akhir yang Terbentuk:** {job_order}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**Visualisasi Timeline Gantt Chart:**")
    
    # 3. Gantt Chart Interaktif (Plotly)
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
    
    # 4. Petunjuk Download Grafik Gantt Chart sebagai Gambar (.png)
    st.markdown("""
    <div style="background-color: #EBF3F5; border-left: 4px solid #1e7796; padding: 16px; border-radius: 8px; margin-top: 10px;">
        📸 <b>Tombol Download Gambar Gantt Chart Bawaan:</b><br>
        Untuk mengunduh grafik Gantt Chart di atas menjadi file gambar png, silakan gerakkan kursor mouse Anda ke area grafik batang di atas. Menu toolbar kecil akan muncul di <b>pojok kanan atas grafik</b>, silakan klik ikon berlambang <b>Kamera (Download plot as a png)</b> untuk mengunduhnya secara instan.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="custom-base-box" style="text-align: center; color: #6b8894; padding: 45px 20px;">', unsafe_allow_html=True)
    st.markdown('<div class="box-title-text" style="justify-content: center;">📊 Hasil Perhitungan & Grafik Linimasa</div>', unsafe_allow_html=True)
    st.write("Belum ada data pengerjaan yang diproses. Isikan data Anda pada tabel isian di atas dan tekan tombol hitung untuk memunculkan visualisasi pengerjaan di sini.")
    st.markdown('</div>', unsafe_allow_html=True)
