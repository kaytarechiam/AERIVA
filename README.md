# AERIVA — rancangan API lokal

AERIVA membantu pengguna merencanakan kegiatan luar ruangan berdasarkan kondisi lingkungan. Layanan inti menerima lokasi dan rentang waktu, lalu menyediakan penilaian lingkungan dan rekomendasi ketika data serta aturan tervalidasi tersedia. LocalLoop menyediakan acara publik; CourtSlot menyediakan fasilitas dan ketersediaan. Penggabungan API mitra direncanakan berjalan di luar STB. Kedua mitra dan AERIVA memiliki API masing-masing.

## Struktur

```text
backend/
  app.py                API inti lokal: health, assessment, recommendations
  requirements.txt      Dependensi untuk menjalankan API
integration/
  clients.py            Klien baca LocalLoop, CourtSlot, dan AERIVA
  api_catalog.json      Daftar alamat, fungsi, parameter, status rancangan
docs/
  API_DAN_INTEGRASI.md  Kontrak rinci dan penjelasan
.env.example            Contoh konfigurasi tanpa kunci rahasia
.gitignore
```

## Menjalankan API inti di laptop

Di PowerShell, dari folder proyek:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend/requirements.txt
python -m uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000
```

Buka http://127.0.0.1:8000/docs untuk dokumentasi dan uji interaktif. Bila aktivasi PowerShell dibatasi, gunakan `.\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt` dan `.\.venv\Scripts\python.exe -m uvicorn backend.app:app --host 127.0.0.1 --port 8000` tanpa aktivasi.

API saat ini menyediakan kerangka respons dengan status **insufficient_data**, tanpa data prakiraan atau skor palsu. Belum ada autentikasi/JWT/API key, database, penyedia cuaca, aturan penilaian teruji, endpoint akun, limit permintaan, Docker, tunnel, atau deployment. Karena itu jangan dipublikasikan sebagai API produksi dan belum memenuhi Tugas 2. Klien integrasi juga belum dihubungkan ke layar mobile atau API mitra nyata.

## GitHub

Repository tujuan: https://github.com/kaytarechiam/AERIVA.git. Pengguna sendiri melakukan commit dan push. Sebelum menghubungkan, periksa `git status`, `git remote -v`, dan isi repo online. Jika repo remote sudah berisi README atau commit, jangan membuat riwayat terpisah lalu memaksa push; clone atau gabungkan riwayat dengan hati-hati setelah memeriksa isinya.
