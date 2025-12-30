import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Konfigurasi Halaman
st.set_page_config(page_title="Mutaqien Care", page_icon="🕌")

st.title("🕌 Mutaqien Care")
st.write("Pembangunan TPQ Al Mutaqien")

# --- KONEKSI JALUR TOL (Gunakan link CSV) ---
# Link ini otomatis mengkonversi Google Sheet Anda jadi data yang siap dibaca
SHEET_ID = "1Sl8mx5MhmunKnm_wEP3Wr8f4ddVFzcjtJY8s_UmgcI0"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Sheet1"

try:
    # Membaca data langsung dari URL
    df = pd.read_csv(URL)
    
    if not df.empty:
        st.success("✅ Data Berhasil Dimuat!")
        
        # Ringkasan Dana
        target = 350000000
        # Pastikan kolom 'Nominal' bersih dari karakter non-angka
        df['Nominal'] = pd.to_numeric(df['Nominal'], errors='coerce').fillna(0)
        total = df['Nominal'].sum()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Dana Terkumpul", f"Rp {total:,.0f}")
        with col2:
            persen = (total/target)*100
            st.metric("Persentase", f"{persen:.1f}%")

        # Pie Chart
        fig, ax = plt.subplots(figsize=(4,4))
        ax.pie([total, max(0, target-total)], 
               labels=['Masuk', 'Sisa'], 
               autopct='%1.1f%%', 
               colors=['#2E7D32', '#eeeeee'])
        st.pyplot(fig)

        # Filter RT
        st.divider()
        list_rt = ["Semua RT"] + sorted(df['RT'].unique().astype(str).tolist())
        pilih_rt = st.selectbox("Cek per RT:", list_rt)
        
        df_tampil = df if pilih_rt == "Semua RT" else df[df['RT'].astype(str) == pilih_rt]
        st.dataframe(df_tampil[['Nama', 'RT', 'Nominal', 'Tanggal']], use_container_width=True, hide_index=True)
        
    else:
        st.warning("Tabel kosong. Silakan isi data di Google Sheets.")

except Exception as e:
    st.error(f"Waduh, ada masalah: {e}")
    st.info("Pastikan nama kolom di Google Sheets adalah: Nama, RT, Nominal, Tanggal")

st.caption("Dikelola oleh Pengurus TPQ Al Mutaqien | Kinara Putri Gemini")
