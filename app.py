import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import matplotlib.pyplot as plt

# Konfigurasi Halaman
st.set_page_config(page_title="Mutaqien Care", page_icon="🕌", layout="wide")

# Gaya CSS
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🕌 Mutaqien Care")
st.subheader("Pembangunan TPQ Al Mutaqien")

# --- KONEKSI GOOGLE SHEETS ---
try:
    # Mengambil koneksi otomatis dari Secrets
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Membaca data
    df = conn.read(worksheet="Sheet1")
    df_progress = conn.read(worksheet="Sheet2")

    if df is None or df.empty:
        st.warning("Data di Google Sheets (Sheet1) kosong atau tidak terbaca.")
        st.stop()

except Exception as e:
    st.error(f"⚠️ Koneksi Gagal: {e}")
    st.info("Pastikan link Google Sheets sudah dimasukkan di menu Settings -> Secrets di Dashboard Streamlit.")
    st.stop()

# --- LOGIKA PERHITUNGAN ---
TARGET_DANA = 350000000
total_terkumpul = pd.to_numeric(df["Nominal"]).sum()
persentase = (total_terkumpul / TARGET_DANA) * 100
sisa_dana = TARGET_DANA - total_terkumpul

# --- TAMPILAN DASHBOARD ---
col1, col2 = st.columns([1, 1])

with col1:
    st.metric("Total Dana Terkumpul", f"Rp {total_terkumpul:,.0f}", f"{persentase:.1f}%")
    
    # Pie Chart
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie([total_terkumpul, max(0, sisa_dana)], 
           labels=['Terkumpul', 'Sisa'], 
           autopct='%1.1f%%', startangle=90, colors=['#2E7D32', '#FFCDD2'])
    st.pyplot(fig)

with col2:
    st.info("📢 **Progress Fisik Pembangunan**")
    for index, row in df_progress.iterrows():
        st.write(f"✅ {row['Aktivitas']} - *{row['Status']}*")

st.divider()
st.subheader("🔍 Daftar Pembayaran Warga")
rt_pilihan = st.selectbox("Filter RT:", ["Semua RT"] + sorted(df["RT"].unique().astype(str).tolist()))

df_tampil = df if rt_pilihan == "Semua RT" else df[df["RT"] == rt_pilihan]
st.dataframe(df_tampil, use_container_width=True, hide_index=True)

st.caption("Aplikasi dikelola oleh Pengurus TPQ Al Mutaqien | Supported by GesitNet")
