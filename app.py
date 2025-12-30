import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. Konfigurasi Dasar
st.set_page_config(page_title="Muttaqin Care", page_icon="🕌", layout="wide")

# 2. Database & Fungsi Koneksi
SHEET_ID = "1Sl8mx5MhmunKnm_wEP3Wr8f4ddVFzcjtJY8s_UmgcI0"

def get_url(sheet_name):
    return f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

def fix_drive_link(url):
    """Mengubah link share Google Drive menjadi link gambar langsung"""
    try:
        if pd.isna(url) or not isinstance(url, str):
            return ""
        if 'drive.google.com' in url:
            if '/file/d/' in url:
                file_id = url.split('/file/d/')[1].split('/')[0]
            elif 'id=' in url:
                file_id = url.split('id=')[1].split('&')[0]
            else:
                return url
            return f"https://thumbnail.googleusercontent.com/ds/{file_id}"
        return url
    except:
        return ""

# 3. Load Data dengan Proteksi Error
@st.cache_data(ttl=600) # Simpan cache 10 menit agar hemat kuota
def load_data():
    try:
        d1 = pd.read_csv(get_url("Sheet1"))
        d2 = pd.read_csv(get_url("Sheet2"))
        d3 = pd.read_csv(get_url("Sheet3"))
        d4 = pd.read_csv(get_url("Sheet4"))
        return d1, d2, d3, d4
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return None, None, None, None

df_masuk, df_progres, df_keluar, df_galeri = load_data()

if df_masuk is None:
    st.stop()

# 4. Header Aplikasi
st.title("🕌 Muttaqien Care")
st.caption("Dashboard Transparansi Pembangunan TPQ Al Muttaqin | Dikembangkan oleh GesitNet")
st.markdown("---")

# 5. Navigasi Tab
tab1, tab2, tab3 = st.tabs(["📊 Donasi & Progres", "💸 Laporan Keuangan", "📸 Galeri Foto"])

# --- TAB 1: DONASI ---
with tab1:
    target_dana = 350000000
    df_masuk['Nominal'] = pd.to_numeric(df_masuk['Nominal'], errors='coerce').fillna(0)
    total_m = df_masuk['Nominal'].sum()
    persen = (total_m / target_dana) * 100

    col_m1, col_m2 = st.columns([1, 1])
    with col_m1:
        st.metric("Dana Terkumpul", f"Rp {total_m:,.0f}", f"{persen:.1f}%")
        st.progress(min(persen/100, 1.0))
        
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie([total_m, max(0, target_dana-total_m)], labels=['Terkumpul', 'Sisa'], 
               autopct='%1.1f%%', colors=['#2E7D32', '#FFCDD2'], startangle=90)
        st.pyplot(fig)

    with col_m2:
        st.subheader("🏗️ Status Pembangunan")
        for _, row in df_progres.iterrows():
            icon = "✅" if str(row['Status']).lower() == "selesai" else "⏳"
            st.write(f"{icon} **{row['Aktivitas']}**")

    st.divider()
    st.subheader("🔍 Filter Data Iuran Warga")
    rt_list = ["Semua RT"] + sorted(df_masuk['RT'].unique().astype(str).tolist())
    pilih_rt = st.selectbox("Pilih RT:", rt_list)
    df_f = df_masuk if pilih_rt == "Semua RT" else df_masuk[df_masuk['RT'].astype(str) == pilih_rt]
    # Menggunakan width='stretch' untuk mengganti use_container_width
    st.dataframe(df_f[['Nama', 'RT', 'Nominal', 'Tanggal']], width='stretch', hide_index=True)

# --- TAB 2: KEUANGAN ---
with tab2:
    df_keluar['Nominal'] = pd.to_numeric(df_keluar['Nominal'], errors='coerce').fillna(0)
    total_k = df_keluar['Nominal'].sum()
    
    c1, c2 = st.columns(2)
    c1.metric("Total Pengeluaran", f"Rp {total_k:,.0f}")
    c2.metric("Saldo Kas", f"Rp {total_m - total_k:,.0f}")
    st.table(df_keluar)

# --- TAB 3: GALERI ---
with tab3:
    st.subheader("📸 Dokumentasi Pekerjaan")
    if not df_galeri.empty:
        # Menghapus baris yang link fotonya kosong agar tidak error
        df_galeri = df_galeri.dropna(subset=['Link_Foto'])
        cols = st.columns(3)
        for i, row in df_galeri.iterrows():
            with cols[i % 3]:
                img_url = fix_drive_link(str(row['Link_Foto']))
                if img_url:
                    st.markdown(f"**📅 {row['Tanggal']}**")
                    try:
                        # Menggunakan width='stretch' di sini juga
                        st.image(img_url, width='stretch')
                        st.caption(f"📌 {row['Aktivitas']}")
                    except:
                        st.write("🖼️ (Gambar tidak dapat dimuat)")
                st.markdown("---")
    else:
        st.info("Belum ada foto dokumentasi.")
