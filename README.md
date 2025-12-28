# 🕌 Mutaqien Care - Aplikasi Penggalangan Dana TPQ Al Mutaqien

Aplikasi mobile-responsive sederhana yang dirancang untuk transparansi dana pembangunan TPQ Al Mutaqien. Aplikasi ini memudahkan jamaah/warga untuk memantau progres donasi dan pembangunan secara real-time.

## 🚀 Fitur Utama

### 1. Dashboard Warga (Transparansi)
* **Visualisasi Target Dana**: Menampilkan persentase dana terkumpul vs target (Rp 350.000.000) dalam bentuk **Pie Chart**.
* **Daftar Donatur**: Informasi nama warga, nominal setoran, dan tanggal bayar.
* **Filter Per RT**: Memudahkan warga melihat kontribusi per lingkungannya (RT 01 - RT 05).
* **Progress Pembangunan**: Update berkala mengenai tahap pekerjaan pembangunan fisik TPQ.

### 2. Dashboard Pengurus (Via Google Sheets)
* **Input Mudah**: Pengurus (Ketua, Sekretaris, Bendahara) cukup menginput data melalui Google Sheets.
* **Real-Time Update**: Setiap perubahan data di Google Sheets akan langsung tercermin di aplikasi jamaah.

---

## 🛠️ Teknologi yang Digunakan

* **Bahasa Pemrograman**: [Python](https://www.python.org/)
* **Framework Dashboard**: [Streamlit](https://streamlit.io/)
* **Database**: [Google Sheets API](https://docs.google.com/spreadsheets/)
* **Visualisasi**: [Matplotlib](https://matplotlib.org/)

---

## 📋 Cara Instalasi & Penggunaan

### 1. Persiapan Database
1. Buat Google Sheets dengan dua tab (sheet):
   - **Sheet1**: Kolom `Nama`, `RT`, `Nominal`, `Tanggal`.
   - **Sheet2**: Kolom `Aktivitas`, `Status`.
2. Pastikan akses Google Sheets diatur ke **"Anyone with the link"** sebagai **Viewer**.

### 2. Instalasi Lokal
Jika ingin menjalankan di komputer sendiri:
```bash
# Clone repository ini
git clone (https://github.com/hermanparis21/almutaqien)

# Masuk ke direktori
cd tpq-mutaqien

# Install library yang dibutuhkan
pip install -r requirements.txt

# Jalankan aplikasi
streamlit run app.py
