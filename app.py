import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. Konfigurasi Dasar
st.set_page_config(page_title="Mutaqien Care", page_icon="🕌", layout="wide")

# 2. Database & Fungsi Koneksi
SHEET_ID = "1Sl8mx5MhmunKnm_wEP3Wr8f4ddVFzcjtJY8s_UmgcI0"

def get_url(sheet_name):
    return f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

def fix_drive_link(url):
    """Mengubah link share Google Drive menjadi link gambar langsung"""
    try:
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
        return url

# 3. Load Data
try:
    df_masuk = pd.read_csv(get_url("Sheet1"))
    df_progres = pd.read_csv(get_url("Sheet2"))
    df_keluar = pd.read_csv(get_url("Sheet3"))
    df_galeri = pd.read_csv(get_url("Sheet4"))
except Exception as e:
    st.error(f"Gagal memuat data. Pastikan nama Sheet1-4 benar. Error: {e}")
    st.stop()

# 4. Header Aplikasi
st.title("🕌 Mutaqien Care")
st.caption("Dashboard Transparansi Pembangunan TPQ Al Mutaqien")
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
        st.write(f"**Target:** Rp {target_dana:,.0f}")
        st.progress(min(persen/100, 1.0))
        
        # Grafik Pie
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie([total_m, max(0, target_dana-total_m)], labels=['Terkumpul', 'Sisa'], 
               autopct='%1.1f%%', colors=['#2E7D32', '#FFCDD2'], startangle=90)
        st.pyplot(fig)

    with col_m2:
        st.subheader("🏗️ Status Pembangunan")
        for _, row in df_progres.iterrows():
            icon = "✅" if str(row['Status']).lower() == "selesai" else "⏳"
            st.write(f"{icon} **{row['Aktivitas']}** ({row['Status']})")

    st.divider()
    st.subheader("🔍 Filter Data Iuran Warga")
    rt_list = ["Semua RT"] + sorted(df_masuk['RT'].unique().astype(str).tolist())
    pilih_rt = st.selectbox("Pilih RT Anda:", rt_list)
    df_f = df_masuk if pilih_rt == "Semua RT" else df_masuk[df_masuk['RT'].astype(str) == pilih_rt]
    st.dataframe(df_f[['Nama', 'RT', 'Nominal', 'Tanggal']], use_container_width=True, hide_index=True)

# --- TAB 2: KEUANGAN ---
with tab2:
    df_keluar['Nominal'] = pd.to_numeric(df_keluar['Nominal'], errors='coerce').fillna(0)
    total_k = df_keluar['Nominal'].sum()
    saldo = total_m - total_k

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Masuk", f"Rp {total_m:,.0f}")
    c2.metric("Total Keluar", f"Rp {total_k:,.0f}", delta_color="inverse")
    c3.metric("Saldo Kas", f"Rp {saldo:,.0f}")

    st.subheader("📋 Rincian Pengeluaran")
    st.table(df_keluar)

# --- TAB 3: GALERI ---
with tab3:
    st.subheader("📸 Dokumentasi Pekerjaan Lapangan")
    if not df_galeri.empty:
        cols = st.columns(3)
        for i, row in df_galeri.iterrows():
            with cols[i % 3]:
                img_url = fix_drive_link(str(row['Link_Foto']))
                st.markdown(f"**📅 {row['Tanggal']}**")
                try:
                    st.image(img_url, use_container_width=True)
                    st.caption(f"📌 {row['Aktivitas']}")
                except:
                    st.error("Gagal memuat gambar.")
                st.markdown("---")
    else:
        st.info("Belum ada foto dokumentasi.")

st.caption("Aplikasi dikelola secara mandiri | Dikembangkan oleh GesitNet")
