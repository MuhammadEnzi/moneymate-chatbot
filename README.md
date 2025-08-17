🤖 MoneyMate: Asisten Keuangan Pribadi Berbasis AI
MoneyMate adalah aplikasi chatbot keuangan cerdas yang dirancang untuk membantu Anda mengelola keuangan pribadi dengan cara yang modern, intuitif, dan menyenangkan. Ditenagai oleh Google Gemini API dan dibangun dengan Streamlit, MoneyMate berfungsi sebagai pelatih keuangan pribadi Anda yang selalu siap membantu.

(Tips: Ganti URL di atas dengan screenshot aplikasi Anda setelah di-deploy)

✨ Fitur Utama
📝 Pencatatan Transaksi Cerdas: Catat pemasukan dan pengeluaran dengan mudah melalui antarmuka yang bersih.

💬 Chatbot AI Interaktif: Dapatkan saran keuangan, hitung target tabungan, dan analisis pengeluaran Anda hanya dengan mengobrol.

📊 Dasbor Visual: Pahami kondisi keuangan Anda dalam sekejap melalui ringkasan saldo, metrik pemasukan/pengeluaran, dan grafik alokasi dana.

🎯 Pelacakan Target: Tetapkan tujuan finansial (seperti dana darurat atau liburan) dan pantau progresnya secara visual.

📄 Ekspor Laporan: Unduh riwayat transaksi Anda dalam format CSV untuk analisis lebih lanjut.

🎨 Desain Modern & Futuristik: Nikmati pengalaman pengguna yang memukau dengan tema glassmorphism, latar belakang gradien animasi, dan efek neon yang responsif di semua perangkat.

🛠️ Teknologi yang Digunakan
Frontend: Streamlit

AI & Language Model: Google Gemini API

Data Handling: Pandas

Visualisasi: Plotly Express

Bahasa: Python

🚀 Cara Menjalankan Proyek
Ikuti langkah-langkah berikut untuk menjalankan MoneyMate di komputer Anda.

1. Persiapan
Pastikan Anda memiliki Python 3.8+ dan Git terinstal.

Salin (clone) repositori ini ke komputer Anda:

git clone https://github.com/username/moneymate-chatbot.git
cd moneymate-chatbot

(Ganti username/moneymate-chatbot dengan URL repositori Anda)

2. Setup Lingkungan
Buat dan aktifkan virtual environment:

# Windows
python -m venv venv
venv\Scripts\activate

# MacOS/Linux
python3 -m venv venv
source venv/bin/activate

3. Instalasi Dependensi
Instal semua library yang dibutuhkan dari file requirements.txt:

pip install -r requirements.txt

4. Konfigurasi API Key
Dapatkan Google Gemini API Key Anda dari Google AI Studio.

Buat folder baru bernama .streamlit di dalam direktori proyek.

Di dalam folder .streamlit, buat file baru bernama secrets.toml.

Tambahkan API key Anda ke dalam file secrets.toml dengan format:

GEMINI_API_KEY = "MASUKKAN_API_KEY_ANDA_DI_SINI"

5. Jalankan Aplikasi
Jalankan aplikasi Streamlit dari terminal Anda:

streamlit run app.py

Aplikasi akan otomatis terbuka di browser Anda!

☁️ Deploy ke Streamlit Cloud
Unggah proyek Anda ke repositori GitHub (pastikan file .streamlit/secrets.toml sudah ada di dalam .gitignore).

Kunjungi share.streamlit.io.

Klik "New app" dan pilih repositori GitHub Anda.

Buka "Advanced settings..." dan tambahkan API key Anda di bagian "Secrets".

Klik "Deploy!" dan tunggu hingga proses selesai.

