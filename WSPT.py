import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Production Scheduling · WSPT Optimizer",
    page_icon="⏱️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS (Matching Style) ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght=300;400;500;600&family=DM+Mono:wght=400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #FDF6F9; }
[data-testid="stSidebar"] { background: #2A1A3D !important; border-right: 1px solid #452A5C; }
[data-testid="stSidebar"] * { color: #E8D6F5 !important; }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: #F5E8FD !important; }

.hero-banner {
    background: linear-gradient(135deg, #2A1A3D 0%, #53357B 55%, #C278E8 100%);
    border-radius: 16px; padding: 36px 40px; margin-bottom: 28px;
}
.hero-title { font-size: 28px; font-weight: 600; color: #F5E8FD; margin: 0 0 6px; }
.hero-sub { font-size: 14px; color: #DCC2F5; margin: 0; }

.metric-card {
    background: white; border-radius: 12px; padding: 18px 20px;
    border: 1px solid #E8D6F5; box-shadow: 0 1px 6px rgba(130,80,180,0.07);
}
.metric-card.purple { border-top: 3px solid #C278E8; }
.metric-card.lavender { border-top: 3px solid #A070D4; }
.metric-card.coral { border-top: 3px solid #E878A0; }

.metric-label { font-size: 11px; font-weight: 600; color: #A084C0; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 6px; }
.metric-value { font-size: 24px; font-weight: 600; color: #2A1A3D; font-family: 'DM Mono', monospace; }
.metric-sub { font-size: 11px; color: #A084C0; margin-top: 3px; }

.section-header { display: flex; align-items: center; gap: 10px; margin: 24px 0 14px; }
.section-title { font-size: 16px; font-weight: 600; color: #2A1A3D; }
.info-box { background: #F7F0FF; border-left: 4px solid #C278E8; border-radius: 0 8px 8px 0; padding: 12px 16px; margin-bottom: 20px; font-size: 13px; color: #53357B; }
hr { border-color: #E8D6F5 !important; }
</style>
""", unsafe_allow_html=True)

# ─── Sidebar Input ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 20px 0 16px'>
        <div style='font-size:22px; font-weight:700; color:#F5E8FD;'>WSPT Scheduler</div>
        <div style='font-size:12px; color:#A084C0; margin-top:3px'>Weighted Shortest Processing Time</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.write("⏱️ **Aturan WSPT:** Pekerjaan diurutkan berdasarkan rasio Waktu Proses dibagi Bobot ($t_j / W_j$) dari yang terkecil untuk meminimalkan *Total Weighted Flow Time*.")

# ─── Hero Banner ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">⏱️ Weighted Shortest Processing Time (WSPT) Dashboard</div>
    <div class="hero-sub">Optimasi urutan penjadwalan dengan pembobotan job tunggal (Single Machine Scheduling)</div>
</div>
""", unsafe_allow_html=True)

# ─── Data Input Section ───────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-title">📂 Input Data Job (Pekerjaan)</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    💡 <b>Petunjuk:</b> Isikan daftar pekerjaan, waktu proses (Processing Time), dan Bobot (Weight). 
    Data default di bawah disesuaikan dengan contoh soal pada gambar Anda (8 Jobs).
</div>
""", unsafe_allow_html=True)

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

if st.button("▶️ Hitung Penjadwalan WSPT", type="primary"):
    if edited_df is not None and len(edited_df) > 0:
        df_jobs = edited_df.dropna().copy()
        
        # ─── WSPT Calculation Logic ────────────────────────────────────────────
        # 1. Hitung rasio tj / Wj
        df_jobs["Rasio_tj_Wj"] = df_jobs["Processing_Time"] / df_jobs["Weight"]
        
        # 2. Urutkan berdasarkan rasio terkecil ke terbesar
        # Jika rasio sama, diurutkan berdasarkan Processing_Time terkecil (Aturan Tambahan)
        df_wspt = df_jobs.sort_values(by=["Rasio_tj_Wj", "Processing_Time"], ascending=[True, True]).reset_index(drop=True)
        
        # 3. Hitung Flow Time & Weighted Flow Time
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
        
        # ─── Hitung Metrik Performa (Sesuai Rumus Gambar) ─────────────────────
        total_flow_time = df_wspt["Flow_Time"].sum()
        total_weighted_flow_time = df_wspt["Weighted_Flow_Time"].sum()
        total_weight = df_wspt["Weight"].sum()
        num_jobs = len(df_wspt)
        
        mean_flow_time = total_flow_time / num_jobs
        mean_weighted_flow_time = total_weighted_flow_time / total_weight
        
        # ─── METRIC CARDS ─────────────────────────────────────────────────────
        st.markdown("""<div class="section-header"><div class="section-title">📊 Performa Penjadwalan WSPT</div></div>""", unsafe_allow_html=True)
        
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"""<div class="metric-card purple"><div class="metric-label">Total Flow Time</div><div class="metric-value">{total_flow_time}</div><div class="metric-sub">Jumlah total waktu alir</div></div>""", unsafe_allow_html=True)
        with m2:
            st.markdown(f"""<div class="metric-card lavender"><div class="metric-label">Rata-rata Flow Time</div><div class="metric-value">{mean_flow_time:.2f}</div><div class="metric-sub">{total_flow_time} / {num_jobs} (Total Job)</div></div>""", unsafe_allow_html=True)
        with m3:
            st.markdown(f"""<div class="metric-card coral"><div class="metric-label">Rata-rata Flow Time Tertimbang</div><div class="metric-value">{mean_weighted_flow_time:.5f}</div><div class="metric-sub">{total_weighted_flow_time} / {total_weight} (Total Bobot)</div></div>""", unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ─── TABEL HASIL URUTAN WSPT ───────────────────────────────────────────
        st.markdown("**Tabel Perhitungan Urutan Hasil Optimasi WSPT**")
        
        df_wspt["Sequence"] = [f"Urutan {i+1}" for i in range(len(df_wspt))]
        df_display = df_wspt.set_index("Sequence")[["Job_Name", "Rasio_tj_Wj", "Weight", "Processing_Time", "Flow_Time", "Weighted_Flow_Time"]]
        
        # Rename kolom agar presisi seperti di gambar tugas
        df_display.columns = ["Job", "t_j / W_j", "Bobot", "Waktu", "Flow Time", "Weighted Flow Time"]
        
        # Membaca style agar rapi
        st.dataframe(
            df_display.style.format({"t_j / W_j": "{:.1f}"}),
            use_container_width=True
        )
        
        # Menampilkan string urutan text seperti di gambar (contoh: 3-4-8...)
        job_order = "-".join([str(name).replace("Job ", "") for name in df_wspt["Job_Name"]])
        st.info(f"**Urutan yang dihasilkan (Berdasarkan nomor Job):** {job_order}")
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # ─── VISUALISASI GANTT CHART ──────────────────────────────────────────
        st.markdown("""<div class="section-header"><div class="section-title">📈 Gantt Chart Timeline (WSPT)</div></div>""", unsafe_allow_html=True)
        
        fig_gantt = go.Figure()
        colors = px.colors.qualitative.Pastel
        
        for idx, row in df_wspt.iterrows():
            fig_gantt.add_trace(go.Bar(
                x=[row["Processing_Time"]],
                y=["Mesin Tunggal"],
                base=[row["Start_Time"]],
                orientation='h',
                name=row["Job_Name"],
                text=f"{row['Job_Name']}",
                textposition='inside',
                marker=dict(color=colors[idx % len(colors)], line=dict(color='white', width=1.5))
            ))
            
        fig_gantt.update_layout(
            barmode='stack',
            height=250,
            plot_bgcolor="white",
            showlegend=True,
            xaxis=dict(
                title="Waktu Proses", 
                gridcolor="#F0E8F5",
                tickvals=[0] + list(df_wspt["Flow_Time"]), # Membuat penanda angka di chart presisi sesuai akumulasi waktu selesai
            ),
            yaxis=dict(showticklabels=False)
        )
        st.plotly_chart(fig_gantt, use_container_width=True)
            
    else:
        st.warning("Silakan masukkan data pekerjaan terlebih dahulu pada tabel.")
