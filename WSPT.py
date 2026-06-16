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

# ─── Custom CSS (Warna Sidebar & Banner Lebih Muda) ───────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght=300;400;500;600&family=DM+Mono:wght=400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
/* Background utama aplikasi menggunakan warna ungu muda pastel cerah */
.stApp { background: #F3EAFD; } 

/* SIDEBAR: Diubah menjadi warna ungu pastel yang lebih muda, lembut, dan tidak pekat */
[data-testid="stSidebar"] { background: #9B72C4 !important; border-right: 1px solid #B08CD6; }
/* Warna teks di dalam sidebar disesuaikan agar tetap kontras dan terbaca */
[data-testid="stSidebar"] * { color: #2A1A3D !important; }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: #2A1A3D !important; }

/* HERO BANNER / UPPERSIDE: Menggunakan gradasi ungu medium-muda yang cerah */
.hero-banner {
    background: linear-gradient(135deg, #8558B4 0%, #9B72C4 60%, #B28DE0 100%);
    border-radius: 16px; padding: 36px 40px; margin-bottom: 28px;
    box-shadow: 0 4px 12px rgba(133,88,180,0.1);
}
.hero-title { font-size: 28px; font-weight: 600; color: #FFFFFF; margin: 0 0 6px; }
.hero-sub { font-size: 14px; color: #F3EAFD; margin: 0; }

/* Kartu metrik dengan background putih bersih */
.metric-card {
    background: white; border-radius: 12px; padding: 18px 20px;
    border: 1px solid #D9C5EB; box-shadow: 0 2px 8px rgba(133,88,180,0.05);
}
/* Border atas kartu menggunakan variasi warna aksen tema cerah */
.metric-card.purple { border-top: 4px solid #8558B4; }
.metric-card.lavender { border-top: 4px solid #B28DE0; }
.metric-card.coral { border-top: 4px solid #FFD15C; } /* Aksen kuning lembut */

.metric-label { font-size: 11px; font-weight: 600; color: #8558B4; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 6px; }
.metric-value { font-size: 24px; font-weight: 600; color: #2A1A3D; font-family: 'DM Mono', monospace; }
.metric-sub { font-size: 11px; color: #75529C; margin-top: 3px; }

.section-header { display: flex; align-items: center; gap: 10px; margin: 24px 0 14px; }
.section-title { font-size: 16px; font-weight: 600; color: #2A1A3D; }
.info-box { background: #FFFFFF; border-left: 4px solid #9B72C4; border-radius: 0 8px 8px 0; padding: 12px 16px; margin-bottom: 20px; font-size: 13px; color: #523573; box-shadow: 0 1px 4px rgba(0,0,0,0.02); }
hr { border-color: #D9C5EB !important; }

/* Customisasi warna tombol utama agar matching dengan ungu yang lebih muda */
div.stButton > button:first-child {
    background-color: #8558B4 !important;
    color: white !important;
    border: none !important;
}
div.stButton > button:first-child:hover {
    background-color: #7246A0 !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Sidebar Input ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 20px 0 16px'>
        <div style='font-size:22px; font-weight:700; color:#2A1A3D;'>WSPT Scheduler</div>
        <div style='font-size:12px; color:#523573; margin-top:3px'>Weighted Shortest Processing Time</div>
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
        df_display.columns = ["Job", "t_j / W_j", "Bobot", "Waktu", "Flow Time", "Weighted Flow Time"]
        
        st.dataframe(
            df_display.style.format({"t_j / W_j": "{:.1f}"}),
            use_container_width=True
        )
        
        job_order = "-".join([str(name).replace("Job ", "") for name in df_wspt["Job_Name"]])
        st.info(f"**Urutan yang dihasilkan (Berdasarkan nomor Job):** {job_order}")
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # ─── VISUALISASI GANTT CHART ──────────────────────────────────────────
        st.markdown("""<div class="section-header"><div class="section-title">📈 Gantt Chart Timeline (WSPT)</div></div>""", unsafe_allow_html=True)
        
        fig_gantt = go.Figure()
        custom_colors = ['#D1B3E3', '#BFA2DB', '#A27BCA', '#8854C0', '#723CB5', '#5E29A4', '#FF79B4', '#FFD15C']
        
        for idx, row in df_wspt.iterrows():
            fig_gantt.add_trace(go.Bar(
                x=[row["Processing_Time"]],
                y=["Mesin Tunggal"],
                base=[row["Start_Time"]],
                orientation='h',
                name=row["Job_Name"],
                text=f"{row['Job_Name']}",
                textposition='inside',
                marker=dict(color=custom_colors[idx % len(custom_colors)], line=dict(color='white', width=1.5))
            ))
            
        fig_gantt.update_layout(
            barmode='stack',
            height=250,
            plot_bgcolor="rgba(255,255,255,0.5)",
            paper_bgcolor="rgba(0,0,0,0)",
            showlegend=True,
            xaxis=dict(
                title="Waktu Proses", 
                gridcolor="#D2B4E8",
                tickvals=[0] + list(df_wspt["Flow_Time"]),
            ),
            yaxis=dict(showticklabels=False)
        )
        st.plotly_chart(fig_gantt, use_container_width=True)
            
    else:
        st.warning("Silakan masukkan data pekerjaan terlebih dahulu pada tabel.")
