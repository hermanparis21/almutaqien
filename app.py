import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import matplotlib.pyplot as plt

# Konfigurasi Tampilan
st.set_page_config(page_title="Mutaqien Care", page_icon="🕌", layout="wide")

# Gaya CSS Custom agar lebih cantik di HP
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_index=True)

# Judul Utama
st.title("🕌 Mutaqien Care")
st.subheader("Pembangunan TPQ Al Mutaqien Sidakangen")

# --- KONEKSI GOOGLE SHEETS ---
# Masukkan URL Google Sheets Anda di sini
URL_SHEETS = "https://docs.google.com/spreadsheets/d/1Sl8mx5MhmunKnm_wEP3Wr8f4ddVFzcjtJY8s_UmgcI0/edit?usp=sharing"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=URL_SHEETS, worksheet="Sheet1")
    df_progress = conn.read(spreadsheet=URL_SHEETS, worksheet="Sheet2")
except:
    st.error("Gagal memuat data. Pastikan URL Sheets benar dan aksesnya 'Anyone with the link'.")
    st.stop()

# --- LOGIKA PERHITUNGAN ---
TARGET_DANA = 350000000
total_terkumpul = df["Nominal"].sum()
persentase = (total_terkumpul / TARGET_DANA) * 100
sisa_dana = TARGET_DANA - total_terkumpul

# --- DASHBOARD UTAMA (WARGA) ---
col1, col2 = st.columns([1, 1])

with col1:
    st.metric("Total Dana Terkumpul", f"Rp {total_terkumpul:,.0f}", f"{persentase:.1f}%")
    
    # Pie Chart
    fig, ax = plt.subplots(figsize=(5, 5))
    colors = ['#2E7D32', '#FFCDD2']
    ax.pie([total_terkumpul, max(0, sisa_dana)], 
           labels=['Terkumpul', 'Sisa'], 
           autopct='%1.1f%%', startangle=90, colors=colors, wedgeprops={'edgecolor': 'white'})
    ax.set_title("Persentase Target Dana")
    st.pyplot(fig)

with col2:
    st.info("📢 **Progress Fisik Pembangunan**")
    for index, row in df_progress.iterrows():
        status_icon = "✅" if row['Status'] == "Selesai" else "🏗️"
        st.write(f"{status_icon} {row['Aktivitas']}")

st.divider()

# --- FILTER & TABEL DATA ---
st.subheader("🔍 Cek Data Pembayaran")
pilihan_rt = st.selectbox("Pilih RT untuk melihat daftar warga:", ["Semua RT"] + sorted(df["RT"].unique().tolist()))

if pilihan_rt == "Semua RT":
    tampilan_df = df
else:
    tampilan_df = df[df["RT"] == pilihan_rt]

# Menampilkan Tabel yang Responsif
st.dataframe(tampilan_df[["Nama", "RT", "Nominal", "Tanggal"]].sort_values(by="Tanggal", ascending=False), 
             use_container_width=True, hide_index=True)

# --- FOOTER ---
st.divider()
st.caption(f"Aplikasi dikelola oleh Pengurus TPQ Al Mutaqien Sidakangen | Supported by GesitNet")
