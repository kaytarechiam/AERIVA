# API dan integrasi AERIVA

## Yang disediakan AERIVA

| Method dan path | Masukan | Hasil saat ini |
|---|---|---|
| GET /api/v1/health | - | Status API, provider belum terhubung |
| GET /api/v1/environment/assessment | lat, lon, start, end | Status data tidak tersedia, daftar periode kosong |
| GET /api/v1/environment/recommendations | lat, lon, start, end | Status data belum cukup, tanpa rekomendasi palsu |

Masukkan waktu ISO 8601 beserta offset, misalnya `2026-12-01T06:00:00+07:00` (tanda `+` harus di-encode sebagai `%2B` dalam query). Koordinat WGS84; validasi lat -90..90 dan lon -180..180, start harus lebih awal dari end. Hasil API lokal ini adalah kerangka, bukan prakiraan nyata.

## Yang diambil AERIVA

| Layanan | Endpoint | Kegunaan | Status |
|---|---|---|---|
| LocalLoop | GET /api/public/events | Daftar acara publik, lokasi teks dan waktu | Sudah diimplementasikan menurut panduan mitra; URL publik dan API key belum diberikan |
| LocalLoop | GET /api/public/events/{event_id} | Detail acara publik | Sudah diimplementasikan menurut panduan mitra; fungsi klien AERIVA belum dibuat |
| CourtSlot | GET /api/public/facilities | Daftar fasilitas umum | Kontrak target AERIVA; implementasi belum diverifikasi |
| CourtSlot | GET /api/public/facilities/{facility_id} | Detail fasilitas umum | Kontrak target AERIVA; klien belum dibuat |
| CourtSlot | GET /api/public/facilities/{facility_id}/availability | Ketersediaan agregat | Kontrak target AERIVA; implementasi belum diverifikasi |

LocalLoop menyediakan lokasi sebagai teks, tanpa koordinat. Pengguna memilih koordinat yang sesuai sebelum lokasi dan waktu acara dipakai untuk meminta penilaian AERIVA. Katalog fasilitas publik bukan otomatis fasilitas kesehatan. Ketersediaan bukan reservasi, dan informasi cuaca tidak otomatis membatalkan acara/reservasi. Base URL dan API key LocalLoop akan diberikan setelah deployment. Kedua endpoint LocalLoop memakai header X-API-Key dan berjalan read-only.

## Pekerjaan lanjutan

Nanda perlu menentukan sumber prakiraan, menyusun dan memvalidasi aturan/ambang, menangani data parsial, membuat auth/JWT/API key, database sesuai kebutuhan, uji, kontainer dan deployment gateway/tunnel STB. Integrasi mitra berjalan di luar STB dengan timeout, cache sesuai kontrak, status kegagalan dan autentikasi per mitra; jangan menyimpan API key rahasia dalam APK. Endpoint, filter, respons, limit, dan hak akses ditetapkan dalam dokumen kontrak dan perlu diimplementasikan serta diuji. Dua API mitra harus benar-benar dipakai pada fitur aplikasi, bukan hanya dicantumkan dalam daftar.

Kontrak lengkap tersedia di `AERIVA_Rancangan_API_Integrasi_Tugas2.md` dalam folder ini. Sertakan README.pdf, dokumentasi API, URL layanan, dan repo sesuai ketentuan Tugas 2 setelah layanan benar-benar siap.
