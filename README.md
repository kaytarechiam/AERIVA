# AERIVA

**Know your environment. Plan your day.**

AERIVA adalah aplikasi mobile yang membantu pengguna memahami kondisi lingkungan dan merencanakan aktivitas di luar ruangan. Melalui informasi kualitas udara, suhu dan panas, indeks ultraviolet (UV), serta cuaca, AERIVA menyajikan gambaran kondisi di lokasi yang dipilih dan membantu pengguna mempertimbangkan waktu beraktivitas.

Informasi disajikan sebagai pendukung perencanaan sehari-hari. AERIVA tidak digunakan untuk memberikan diagnosis atau memastikan keamanan aktivitas secara medis.

## Fitur yang direncanakan

- **Daily Outlook** — ringkasan kondisi lingkungan dan tingkat kewaspadaan harian.
- **Personalized Insights** — penjelasan yang disesuaikan dengan preferensi pengguna.
- **Forecast Timeline** — prakiraan kondisi lingkungan berdasarkan waktu.
- **Best Time to Go Out** — perbandingan waktu aktivitas dengan alasan pemilihannya, apabila data memadai.
- **Fasilitas kesehatan dan edukasi** — informasi pendukung untuk membantu pengguna memahami kondisi di sekitarnya.

## Gambaran sistem

AERIVA direncanakan terdiri atas aplikasi mobile, layanan inti, dan integrasi dengan layanan lain. Aplikasi mobile menampilkan informasi kepada pengguna. Layanan inti mengelola aturan penilaian lingkungan serta rekomendasi waktu aktivitas, sedangkan integrasi menghubungkan informasi dari layanan mitra sesuai kebutuhan aplikasi.

| Bagian | Peran | Status |
|---|---|---|
| Aplikasi mobile | Menyajikan informasi, preferensi, dan fitur AERIVA | Direncanakan |
| Layanan inti AERIVA | Menyediakan API untuk penilaian lingkungan dan rekomendasi | Kerangka awal lokal |
| Integrasi LocalLoop | Mengambil informasi kegiatan publik | Klien awal; kontrak dan alamat menunggu konfirmasi |
| Integrasi CourtSlot | Mengambil informasi fasilitas publik dan ketersediaan | Klien awal; kontrak dan alamat menunggu konfirmasi |

Layanan inti direncanakan berjalan pada STB. Penggabungan data dari layanan lain direncanakan berjalan di luar STB. Alamat dan endpoint mitra masih perlu disepakati serta diuji bersama sebelum dipakai pada aplikasi.

## Struktur repository

Struktur berikut menunjukkan berkas yang sudah ada. Aplikasi mobile dan konfigurasi deployment dapat ditambahkan ketika mulai dikerjakan.

```text
AERIVA/
├── backend/                               # Kerangka layanan inti AERIVA
│   ├── __init__.py
│   ├── app.py                             # Endpoint API inti
│   └── requirements.txt                   # Dependensi layanan inti
├── integration/                           # Klien layanan mitra
│   ├── __init__.py
│   ├── api_catalog.json                   # Daftar layanan dan endpoint
│   └── clients.py                         # Pengambilan data mitra
├── docs/                                  # Dokumentasi dan rancangan
│   ├── API_DAN_INTEGRASI.md
│   └── AERIVA_Rancangan_API_Integrasi_Tugas2.md
├── .env.example                           # Contoh konfigurasi tanpa rahasia
├── .gitignore
└── README.md
```

## Menjalankan layanan inti secara lokal

Jalankan perintah berikut melalui PowerShell dari folder utama repository:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend/requirements.txt
python -m uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000
```

Setelah server berjalan, buka [dokumentasi API lokal](http://127.0.0.1:8000/docs) untuk melihat dan mencoba endpoint. Alamat tersebut hanya dapat diakses ketika server lokal aktif.

Jika aktivasi PowerShell dibatasi, gunakan Python dari folder virtual environment tanpa aktivasi:

```powershell
.\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt
.\.venv\Scripts\python.exe -m uvicorn backend.app:app --host 127.0.0.1 --port 8000
```

## Status pengembangan

Repository saat ini berisi kerangka awal layanan inti, klien integrasi, dan dokumentasi rancangan. Sumber prakiraan, aturan penilaian tervalidasi, autentikasi, database, pembatasan permintaan, serta konfigurasi Docker dan tunnel masih perlu dikerjakan. Endpoint penilaian dan rekomendasi saat ini memberikan status data belum tersedia karena sumber prakiraan belum terhubung.

## Dokumentasi

- [API dan integrasi](docs/API_DAN_INTEGRASI.md)
- [Rancangan API dan integrasi Tugas 2](docs/AERIVA_Rancangan_API_Integrasi_Tugas2.md)

## Tim pengembang

- **Kayta Rechia Mazaya** — 18224022
- **R. Athalla Ananda P.** — 18224060

Tugas besar II3160 Teknologi Sistem Terintegrasi × II3140 Pengembangan Aplikasi Web & Mobile.
