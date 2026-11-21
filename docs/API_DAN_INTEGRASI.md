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
| LocalLoop | GET /api/public/events | Daftar acara publik, lokasi dan waktu | Path tercantum di dokumen mitra; URL, respons dan filter belum disepakati |
| LocalLoop | GET /api/events/{id} | Detail acara | Path ada di dokumen mitra; akses belum dikonfirmasi; fungsi klien belum dibuat |
| CourtSlot | GET /api/public/facilities | Daftar fasilitas umum | Path usulan, belum dikonfirmasi |
| CourtSlot | GET /api/public/facilities/{id}/availability | Ketersediaan agregat | Path usulan, belum dikonfirmasi |

Lokasi dan waktu dari mitra dapat dipakai untuk meminta penilaian AERIVA. Katalog fasilitas publik bukan otomatis fasilitas kesehatan. Ketersediaan bukan reservasi, dan informasi cuaca tidak otomatis membatalkan acara/reservasi. Domain contoh .stei.fun/.stei.site belum diverifikasi di Registry.

## Pekerjaan lanjutan

Nanda perlu menentukan sumber prakiraan, menyusun dan memvalidasi aturan/ambang, menangani data parsial, membuat auth/JWT/API key, database sesuai kebutuhan, uji, kontainer dan deployment gateway/tunnel STB. Integrasi mitra berjalan di luar STB dengan timeout, cache sesuai kontrak, status kegagalan dan autentikasi per mitra; jangan menyimpan API key rahasia dalam APK. Mitra harus menyepakati endpoint, filter, respons, limit, dan hak akses. Dua API mitra harus benar-benar dipakai pada fitur aplikasi, bukan hanya dicantumkan dalam daftar.

Rancangan lengkap: salin dokumen `AERIVA_Rancangan_API_Integrasi_Tugas2.md` ke folder docs jika diperlukan dan perbarui bersama mitra. Sertakan README.pdf, dokumentasi API, URL layanan, dan repo sesuai ketentuan Tugas 2 setelah layanan benar-benar siap.
