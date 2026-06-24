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

# ─── Custom CSS (Cute Style, Layout Clean, & Custom Palette) ─────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght=400;500;600;700&family=DM+Mono:wght=400;500&display=swap');

html, body, [class*="css"] { font-family: 'Quicksand', sans-serif; }
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

/* CARD SECTION (KOTAK-KOTAK PEMBAHASAN) */
.section-sheet {
    background: #F4F8FA; border-radius: 20px; padding: 25px; margin-bottom: 25px;
    border: 2px solid #accad7; box-shadow: 0 4px 10px rgba(172,202,215,0.2);
}
.section-title { font-size: 18px; font-weight: 700; color: #124d61; margin-bottom: 15px; display: flex; align-items: center; gap: 8px; }

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
}
</style>
""", unsafe_allow_html=True)

# ─── Navigation via Session State & Sidebar ──────────────────────────────────
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "📖 Lembar 1: Panduan"

with st.sidebar:
    st.markdown("""
    <div style='padding: 10px 0 10px'>
        <div style='font-size:24px; font-weight:700; color:#124d61;'>✨ WSPT Menu</div>
        <div style='font-size:12px; color:#124d61; opacity:0.8; margin-top:3px'>Pilih Lembar Kerja Anda:</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<hr style='border-color: #124d61;'>", unsafe_allow_html=True)
    
    # Radio button sebagai tombol navigasi instan di kiri
    chosen_tab = st.radio(
        "Pindah ke Halaman:",
        ["📖 Lembar 1: Panduan", "📂 Lembar 2: Input Data", "📊 Lembar 3: Hasil Perhitungan"],
        key="sidebar_nav"
    )
    st.session_state.active_tab = chosen_tab

# ─── Hero Banner ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">✨ Weighted Shortest Processing Time (WSPT) Dashboard</div>
    <div class="hero-sub">Sistem Manajemen Penjadwalan Kerja Interaktif Lembar demi Lembar</div>
</div>
""", unsafe_allow_html=True)

# Sinkronisasi tab atas dengan pilihan menu di sidebar
tabs_list = ["📖 Lembar 1: Panduan", "📂 Lembar 2: Input Data", "📊 Lembar 3: Hasil Perhitungan"]
active_index = tabs_list.index(st.session_state.active_tab)
tab1, tab2, tab3 = st.tabs(tabs_list)

# Inisialisasi default dataframe di Session State agar data tidak hilang saat pindah tab
if 'df_input_data' not in st.session_state:
    st.session_state.df_input_data = pd.DataFrame([
        {"Job_Name": "Job 1", "Processing_Time": 5, "Weight": 1},
        {"Job_Name": "Job 2", "Processing_Time": 8, "Weight": 2},
        {"Job_Name": "Job 3", "Processing_Time": 6, "Weight": 3},
        {"Job_Name": "Job 4", "Processing_Time": 3, "Weight": 1},
        {"Job_Name": "Job 5", "Processing_Time": 10, "Weight": 2},
        {"Job_Name": "Job 6", "Processing_Time": 14, "Weight": 3},
        {"Job_Name": "Job 7", "Processing_Time": 7, "Weight": 2},
        {"Job_Name": "Job 8", "Processing_Time": 3, "Weight": 1},
    ])

# ─── LEMBAR 1: PANDUAN & ATURAN ───────────────────────────────────────────────
with tab1:
    if active_index == 0:
        st.markdown('<div class="section-sheet">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📘 Cara Penggunaan Aplikasi</div>', unsafe_allow_html=True)
        st.markdown("""
        1. **Pilih Lembar Input Data:** Buka **Lembar 2** melalui menu di atas atau menu navigasi di sidebar kiri.
        2. **Pilih Metode Input:** Anda dapat mengetik data secara manual di tabel langsung atau mengunggah file `.csv`.
        3. **Proses Jadwal:** Tekan tombol **`▶️ Hitung Penjadwalan WSPT`** yang disediakan untuk memproses urutan pekerjaan.
        4. **Analisis Hasil & Unduh:** Pindah ke **Lembar 3** untuk melihat grafik *Gantt Chart*, urutan otomatis, serta mengunduh berkas Excel/CSV hasil optimasi.
        """)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-sheet">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">⏱️ Landasan Teori Aturan WSPT</div>', unsafe_allow_html=True)
        st.markdown("""
        Metode **WSPT (Weighted Shortest Processing Time)** digunakan untuk mengoptimalkan urutan pengerjaan tugas pada satu mesin tunggal (*Single Machine Scheduling*).
        Aturan utama dari metode ini adalah mengurutkan pekerjaan berdasarkan rasio nilai **Waktu Proses dibagi dengan Bobot Kepentingan** ($\\'\\\\frac{t_j}{W_j}\\'$) dari urutan yang **paling kecil hingga terbesar**. 
        Metode ini terbukti secara matematis dapat meminimalkan **Total Weighted Flow Time** (Waktu alir total tertimbang).
        """)
        st.markdown('</div>', unsafe_allow_html=True)

# ─── LEMBAR 2: INPUT DATA (MANUAL & OTOMATIS) ──────────────────────────────────
with tab2:
    if active_index == 1:
        st.markdown('<div class="section-sheet">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">⚙️ Pilih Metode Memasukkan Data</div>', unsafe_allow_html=True)
        
        input_method = st.radio(
            "Metode Input:",
            ["Manual Input (Ketik di Tabel)", "Otomatis (Upload File CSV)"],
            horizontal=True,
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-sheet">', unsafe_allow_html=True)
        if "Manual Input" in input_method:
            st.markdown('<div class="section-title">✍️ Manual Input Data Pekerjaan</div>', unsafe_allow_html=True)
            edited_df = st.data_editor(
                st.session_state.df_input_data,
                num_rows="dynamic",
                use_container_width=True,
                column_config={
                    "Job_Name": st.column_config.TextColumn("Nama Job / Pekerjaan", required=True),
                    "Processing_Time": st.column_config.NumberColumn("Waktu Proses ($t_j$)", min_value=1, step=1, format="%d"),
                    "Weight": st.column_config.NumberColumn("Bobot ($W_j$)", min_value=1, step=1, format="%d")
                }
            )
            st.session_state.df_input_data = edited_df
        else:
            st.markdown('<div class="section-title">📤 Upload File CSV Data Pekerjaan</div>', unsafe_allow_html=True)
            uploaded_file = st.file_uploader("Pilih file CSV Anda (Pastikan berisi kolom: Job_Name, Processing_Time, Weight)", type=["csv"])
            if uploaded_file is not None:
                try:
                    uploaded_df = pd.read_csv(uploaded_file)
                    st.session_state.df_input_data = uploaded_df
                    st.success("✅ File CSV Berhasil Dimuat!")
                    st.dataframe(uploaded_df, use_container_width=True)
                except Exception as e:
                    st.error(f"Format dokumen salah atau rusak: {e}")
                    
        st.write("Setelah memastikan data sudah benar, silakan klik tombol di bawah untuk memproses:")
        trigger_calc = st.button("▶️ Hitung Penjadwalan WSPT", type="primary")
        if trigger_calc:
            st.success("Perhitungan selesai! Silakan buka Lembar 3 via sidebar/menu tab di atas untuk melihat hasilnya.")
        st.markdown('</div>', unsafe_allow_html=True)

# ─── LEMBAR 3: HASIL PERHITUNGAN & DOWNLOAD ──────────────────────────────────
with tab3:
    if active_index == 2:
        df_jobs = st.session_state.df_input_data.dropna().copy()
        
        if df_jobs is not None and len(df_jobs) > 0:
            # ─── WSPT Calculation Logic (TIDAK BERUBAH) ───────────────────────
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
            
            # ─── Box 1: Metrik Performa ───────────────────────────────────────
            st.markdown('<div class="section-sheet">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">📊 Lembar Ringkasan Performa Perhitungan</div>', unsafe_allow_html=True)
            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown(f"""<div class="metric-card primary"><div class="metric-label">Total Flow Time</div><div class="metric-value">{total_flow_time}</div><div class="metric-sub">Jumlah total waktu alir</div></div>""", unsafe_allow_html=True)
            with m2:
                st.markdown(f"""<div class="metric-card secondary"><div class="metric-label">Rata-rata Flow Time</div><div class="metric-value">{mean_flow_time:.2f}</div><div class="metric-sub">{total_flow_time} / {num_jobs} (Total Job)</div></div>""", unsafe_allow_html=True)
            with m3:
                st.markdown(f"""<div class="metric-card accent"><div class="metric-label">Rata-rata Flow Time Tertimbang</div><div class="metric-value">{mean_weighted_flow_time:.5f}</div><div class="metric-sub">{total_weighted_flow_time} / {total_weight} (Total Bobot)</div></div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # ─── Box 2: Tabel Hasil Urutan & Tombol Download ──────────────────
            st.markdown('<div class="section-sheet">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">📋 Lembar Hasil Urutan Optimasi</div>', unsafe_allow_html=True)
            
            df_wspt["Sequence"] = [f"Urutan {i+1}" for i in range(len(df_wspt))]
            df_display = df_wspt.set_index("Sequence")[["Job_Name", "Rasio_tj_Wj", "Weight", "Processing_Time", "Flow_Time", "Weighted_Flow_Time"]]
            df_display.columns = ["Job", "t_j / W_j", "Bobot", "Waktu", "Flow Time", "Weighted Flow Time"]
            
            st.dataframe(df_display.style.format({"t_j / W_j": "{:.1f}"}), use_container_width=True)
            
            job_order = "-".join([str(name).replace("Job ", "") for name in df_wspt["Job_Name"]])
            st.success(f"📌 **Urutan Akhir yang Terbentuk:** {job_order}")
            
            # Fitur Download File Hasil Perhitungan
            csv_buffer = BytesIO()
            df_display.to_csv(csv_buffer, index=True)
            st.download_button(
                label="📥 Unduh Hasil Penjadwalan (.CSV)",
                data=csv_buffer.getvalue(),
                file_name="hasil_penjadwalan_wspt.csv",
                mime="text/csv"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # ─── Box 3: Gantt Chart ───────────────────────────────────────────
            st.markdown('<div class="section-sheet">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">📈 Lembar Visualisasi Timeline Gantt Chart</div>', unsafe_allow_html=True)
            
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
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("Silakan isi data pekerjaan di Lembar 2 terlebih dahulu.")
