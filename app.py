import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Mutaqien Care", page_icon="🕌")

st.title("🕌 Mutaqien Care")
st.write("Pembangunan TPQ Al Mutaqien")

# --- KONEKSI ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # Membaca data tanpa menentukan worksheet terlebih dahulu untuk tes
    df = conn.read()
    
    if df is not None:
        st.success("✅ Koneksi Berhasil!")
        st.write("Data terbaru:")
        st.dataframe(df.head())
        
        # Hitung Total
        target = 350000000
        total = pd.to_numeric(df["Nominal"]).sum()
        st.metric("Dana Terkumpul", f"Rp {total:,.0f}")
        
        # Pie Chart Sederhana
        fig, ax = plt.subplots()
        ax.pie([total, max(0, target-total)], labels=['Masuk', 'Sisa'], autopct='%1.1f%%', colors=['green', 'red'])
        st.pyplot(fig)
        
    else:
        st.error("Data tidak ditemukan. Cek Google Sheets Anda.")

except Exception as e:
    st.error(f"Terjadi Masalah: {e}")
    st.info("Buka Settings > Secrets di Streamlit Cloud dan pastikan URL sudah benar.")
