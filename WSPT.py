import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="WSPT Scheduler · Cute Edition",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS (Cute Style, Layout Clean, & Custom Palette) ─────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

/* Mengubah font menjadi Quicksand agar memberikan impresi lebih lucu dan bulat */
html, body, [class*="css"] { font-family: 'Quicksand', sans-serif; }

/* Base background aplikasi diubah menjadi putih bersih */
.stApp { background: #FFFFFF; } 

/* SIDEBAR: Menggunakan kombinasi warna pastel lembut #accad7 */
[data-testid="stSidebar"] { background: #accad7 !important; border-right: 2px rounded #1e7796; }
[data-testid="stSidebar"] * { color: #124d61 !important; }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: #124d61 !important; font-weight: 700; }

/* HERO BANNER: Menggunakan warna utama #124d61 dan #1e7796 dengan gaya rounded imut */
.hero-banner {
    background: linear-gradient(135deg, #124d61 0%, #1e7796 100%);
    border-radius: 24px; padding: 30px 35px; margin-bottom: 28px;
    box-shadow: 0 8px 20px rgba(30,119,150,0.15);
}
.hero-title { font-size: 26px; font-weight: 700; color: #FFFFFF; margin: 0 0 6px; }
.hero-sub { font-size: 13px; color: #accad7; margin: 0; }

/* CARD SECTION: Lembar Per Section yang Bikin Tampilan Terpisah Rapi */
.section-sheet {
    background: #F4F8FA; border-radius: 20px; padding: 25px; margin-bottom: 25px;
    border: 2px solid #accad7; box-shadow: 0 4px 10px rgba(172,202,215,0.2);
}

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

/* CUTE TITLE FORMAT */
.section-title { font-size: 18px; font-weight: 700; color: #124d61; margin-bottom: 15px; display: flex; align-items: center; gap: 8px; }

/* CUSTOM BUTTON */
div.stButton > button:first-child {
    background: linear-gradient(135deg, #1e7796 0%, #124d61 100%) !important;
    color: white !important; font-weight: 600 !important;
    border-radius: 12px !important; border: none !important;
    padding: 10px 24px !important; box-shadow: 0 4px 10px rgba(18,77,97,0.2);
}
div.stButton > button:first-child:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 14px rgba(18,77,97,0.3);
}
</style>
""", unsafe_allow_html=True)

# ─── Sidebar Input ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 10px 0 10px'>
        <div style='font-size:24px; font-weight:700; color:#124d61;'>✨ WSPT Scheduler</div>
        <div style='font-size:12px; color:#124d61; opacity:0.8; margin-top:3px'>Weighted Shortest Processing Time</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border-color: #124d61;'>", unsafe_allow_html=True)
    st.markdown("### ⏱️ Aturan WSPT")
    st.write("Pekerjaan diurutkan berdasarkan rasio Waktu Proses dibagi Bobot ($t_j / W_j$) dari yang terkecil untuk meminimalkan waktu alir tertimbang.")

# ─── Hero Banner ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">✨ Weighted Shortest Processing Time (WSPT) Dashboard</div>
    <div class="hero-sub">Optimasi urutan penjadwalan dengan pembobotan job tunggal secara otomatis dan menggemaskan!</div>
</div>
""", unsafe_allow_html=True)

# ─── Section 1: Cara Penggunaan ───────────────────────────────────────────────
st.markdown('<div class="section-sheet">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📘 Cara Penggunaan Aplikasi</div>', unsafe_allow_html=True)
st.markdown("""
1. **Isi Data Pekerjaan:** Pada tabel di bawah, masukkan nama pekerjaan, nilai Waktu Proses ($t_j$), dan Bobot ($W_j$) masing-masing job.
2. **Tambah/Hapus Baris:** Anda bisa menambah baris baru dengan menekan tombol **`+`** di bagian bawah tabel data editor.
3. **Mulai Optimasi:** Klik tombol **`▶️ Hitung Penjadwalan WSPT`** yang berwarna biru di bawah tabel.
4. **Lihat Hasil:** Hasil perhitungan, metrik performa rata-rata, beserta visualisasi bagan urutan (*Gantt Chart*) akan langsung muncul dalam lembar terpisah.
""")
st.markdown('</div>', unsafe_allow_html=True)

# ─── Section 2: Input Data Job (Lembar Persection) ───────────────────────────
st.markdown('<div class="section-sheet">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📂 Lembar Input Data Job</div>', unsafe_allow_html=True)

# Default data sesuai gambar soal user
init_data = pd.DataFrame([
    {"Job_Name": "Job 1", "Processing_Time": 5, "Weight": 1},
    {"Job_Name": "Job 2", "Processing_Time": 8, "Weight": 2},
    {"Job_Name": "Job 3", "Processing_Time": 6, "Weight": 3},
    {"Job_Name": "Job 4", "Processing_Time": 3, "Weight": 1},
    {"Job_Name": "Job 5", "Processing_Time": 10, "Weight": 2},
    {"Job_Name": "Job 6", "Processing_Time": 14, "Weight": 3},
    {"Job_Name": "Job 7", "Processing_Time": 7, "Weight": 2},
    {"Job_Name": "Job 8", "Processing_Time": 3, "Weight": 1},
])

edited_df = st.data_editor(
    init_data,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "Job_Name": st.column_config.TextColumn("Nama Job / Pekerjaan", required=True),
        "Processing_Time": st.column_config.NumberColumn("Waktu Proses ($t_j$)", min_value=1, step=1, format="%d"),
        "Weight": st.column_config.NumberColumn("Bobot ($W_j$)", min_value=1, step=1, format="%d")
    }
)
st.markdown('</div>', unsafe_allow_html=True)

# ─── Tombol Proses ────────────────────────────────────────────────────────────
if st.button("▶️ Hitung Penjadwalan WSPT", type="primary"):
    if edited_df is not None and len(edited_df) > 0:
        df_jobs = edited_df.dropna().copy()
        
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
        
        # ─── Section 3: Metrik Performa (Lembar Persection) ─────────────────────
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
        
        # ─── Section 4: Tabel Urutan Hasil (Lembar Persection) ──────────────────
        st.markdown('<div class="section-sheet">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📋 Lembar Hasil Urutan Optimasi</div>', unsafe_allow_html=True)
        
        df_wspt["Sequence"] = [f"Urutan {i+1}" for i in range(len(df_wspt))]
        df_display = df_wspt.set_index("Sequence")[["Job_Name", "Rasio_tj_Wj", "Weight", "Processing_Time", "Flow_Time", "Weighted_Flow_Time"]]
        df_display.columns = ["Job", "t_j / W_j", "Bobot", "Waktu", "Flow Time", "Weighted Flow Time"]
        
        st.dataframe(
            df_display.style.format({"t_j / W_j": "{:.1f}"}),
            use_container_width=True
        )
        
        job_order = "-".join([str(name).replace("Job ", "") for name in df_wspt["Job_Name"]])
        st.success(f"📌 **Urutan Akhir yang Terbentuk:** {job_order}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # ─── Section 5: Visualisasi Gantt Chart (Lembar Persection) ───────────
        st.markdown('<div class="section-sheet">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📈 Lembar Visualisasi Timeline Gantt Chart</div>', unsafe_allow_html=True)
        
        fig_gantt = go.Figure()
        
        # Skema warna cerah menggemaskan berbasis palet biru-hijau pastel ceria
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
            barmode='stack',
            height=220,
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="rgba(0,0,0,0)",
            showlegend=True,
            margin=dict(l=10, r=10, t=20, b=20),
            xaxis=dict(
                title="Sumbu Linimasa Waktu", 
                gridcolor="#F0F4F6",
                tickvals=[0] + list(df_wspt["Flow_Time"]),
            ),
            yaxis=dict(showticklabels=False)
        )
        st.plotly_chart(fig_gantt, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
            
    else:
        st.warning("Silakan masukkan data pekerjaan terlebih dahulu pada tabel.")
