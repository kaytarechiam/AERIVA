# AERIVA — Rancangan API dan Integrasi untuk Tugas 2

**Diperbarui:** 21 November 2026  
**Status:** draf untuk diskusi dengan Nanda, LocalLoop, dan CourtSlot. Belum merupakan kontrak yang disepakati, bukti endpoint berjalan, atau bukti deployment. Semua contoh data di bawah adalah data fiktif.

**Kelas:** AERIVA adalah **K02**, sedangkan LocalLoop dan CourtSlot adalah **K01**, berdasarkan informasi Kayta. Integrasi lintas kelas ini perlu menggunakan URL dan kontrak masing-masing kelompok yang terdaftar; kepastian alamat final tetap perlu dikonfirmasi kepada tiap tim.

## 1. Hasil pembacaan dan keputusan awal

- **Nama aplikasi dan usulan nama tim/domain: AERIVA (`aeriva`).** Mudah diingat, sesuai nama produk, lima huruf kecil, memenuhi pola 3–20 karakter. Ketersediaan di API Registry belum dicek. Alternatif bila sudah terpakai: `aeriva-itb` atau `aeriva-app`, tetap perlu dicek.
- Satu **AERIVA Core API** di STB cukup untuk aturan inti, dengan gateway, auth, database bila diperlukan, dan tunnel. Bounded context dapat berupa modul; tidak harus membuat satu kontainer per fungsi.
- **LocalLoop** berpotensi memberi katalog acara luar ruangan; **CourtSlot** memberi katalog fasilitas publik termasuk taman atau lapangan. Keduanya dapat memakai penilaian AERIVA untuk kondisi di lokasi dan waktu kegiatan/kunjungan.
- Hindari mengubah fitur AERIVA menjadi aplikasi pemesanan acara atau fasilitas. Sebagai pengembangan yang perlu disetujui bersama, tampilkan kegiatan/fasilitas relevan dalam alur memilih aktivitas atau lokasi, lalu hubungkan ke ringkasan kondisi AERIVA.
- CourtSlot menyediakan fasilitas publik umum, **bukan otomatis daftar rumah sakit/puskesmas**. Fitur faskes AERIVA tetap membutuhkan sumber yang sesuai; jangan menyamakan taman/lapangan dengan fasilitas kesehatan.
- Integrasi dua mitra harus benar-benar digunakan dalam fitur aplikasi. Penggunaan AERIVA oleh mitra saja tidak membuktikan AERIVA sudah mengonsumsi dua API kelompok lain.

## 2. Dasar sumber dan tingkat kepastian

| Sumber | Hal yang tertulis | Hal yang belum dibuktikan |
|---|---|---|
| LocalLoop — `partner-catalog.md` yang diberikan tim | Endpoint katalog publik dan detail sudah diimplementasikan. Kontrak filter, JSON, dan autentikasi dijelaskan pada Bagian 6. | Base URL publik dan API key belum diberikan, layanan publik belum diuji. |
| [CourtSlot — perancangan layanan](https://docs.google.com/document/d/1Fgm12ReclZc7yq63S0ahkqHrTMGmvLtHLJgX-lE4xlc/edit) | API baca untuk katalog fasilitas dan ketersediaan agregat tanpa identitas warga; meminta lokasi, periode, indikator hujan dari AERIVA. | Path, parameter, skema JSON, URL dasar dan ketersediaan layanan belum dinyatakan secara rinci dalam bagian yang terbaca. |
| [Makalah AERIVA](https://docs.google.com/document/d/1QkyMAnuDl0LFiPvORDHqcHvoiWIRFNT2xJDaPQkVULQ/edit?tab=t.kyfi5wo9uem8) | Inti: penilaian lingkungan, penjelasan, rekomendasi waktu; sumber, periode dan satuan harus jelas. | Aturan numerik dan ambang akhir belum disepakati/diuji. |
| PDF Tugas Besar, hlm. 14–17 dan 20–23 | Tugas 2: API inti di STB dengan Docker dan HTTPS, dokumentasi serta contoh request; integrasi minimal dua kelompok di Tugas 3. | Status Registry, hostname, API key, implementasi dan deployment kelompok sekarang belum diperiksa. |

Catatan audit makalah: pada 2.4 tertulis indikator yang belum tersedia dianggap `Good`, sementara 2.5 menyatakan harus dibedakan. Ini bertentangan dan penting diperbaiki dalam dokumen bila diminta; rancangan API ini memakai status `unavailable`, tidak menganggap data hilang sebagai baik.

## 3. Gambaran hubungan layanan

```text
Pengguna → Aplikasi AERIVA
             ├─→ AERIVA Core API (gateway + tunnel → STB)
             ├─→ LocalLoop API (katalog acara)
             └─→ CourtSlot API (fasilitas/ketersediaan)

LocalLoop/CourtSlot → AERIVA Core API (informasi lingkungan)
```

Penggabungan hasil dari ketiga API berjalan **di aplikasi atau layanan integrasi di luar STB**, sesuai rancangan tugas. Layanan inti AERIVA tetap di STB. Konsumsi langsung dari aplikasi atau melalui integrasi harus disepakati, terutama karena API key antarkelompok tidak boleh ditanam sebagai rahasia tetap di aplikasi mobile. Integrator server-side di luar STB dapat menyimpan key di lingkungan server; jangan menganggap key di bundle Expo aman.

## 4. Nama dan URL

| Hal | Usulan / status |
|---|---|
| Nama sistem/tim | AERIVA / `aeriva` — usulan, pengguna dan Nanda menentukan bersama |
| AERIVA — K02 | `https://aeriva.stei.site` — usulan jika nama `aeriva` tersedia di Registry; belum terdaftar/terverifikasi |
| LocalLoop — K01 | Base URL HTTPS akan diberikan oleh tim LocalLoop setelah deployment dan pengujian. |
| CourtSlot — K01 | `https://courtslot.stei.fun` — pola contoh; hostname sebenarnya perlu diminta ke tim |
| Base API | `https://<nama-terdaftar>.<domain-kelas>/api/v1` — **placeholder, belum hidup** |
| Endpoint health | `GET /api/v1/health` — usulan, cek konfigurasi gateway |
| Integrasi opsional | `https://<nama-terdaftar>-int.<domain-kelas>` — opsional, hanya bila disepakati |

Kelas sudah diketahui: **AERIVA K02**, **LocalLoop dan CourtSlot K01**. Cek ketersediaan dan reservasi nama AERIVA di API Registry, lalu Nanda membuat tunnel/hostname sesuai petunjuk kelas. Tunnel memberi alamat publik ke gateway, **bukan otomatis membuat endpoint**: path harus cocok dengan aplikasi, routing Nginx, dan kontrak yang didokumentasikan. Jangan memakai `api.aeriva.stei.site` dalam pola tugas; jangan menempel token tunnel ke repo.

## 5. Kontrak AERIVA yang diusulkan untuk mitra

Semua path di bagian ini **usulan**, belum disepakati atau diuji. Base URL digabung dengan path persis sekali. Gunakan JSON, UTF-8, waktu ISO 8601 dengan offset atau UTC, koordinat WGS84. `start` inklusif, `end` eksklusif; kedua waktu harus memiliki offset. Validasi lintang -90..90, bujur -180..180, `start < end`. Batas cakupan mengikuti data yang benar-benar tersedia, tidak dijanjikan selalu 48 jam.

| Endpoint | Tujuan | Masukan | Pengguna |
|---|---|---|---|
| `GET /health` | Memeriksa layanan | Tidak ada | Nanda/monitoring |
| `GET /environment/assessment` | Kewaspadaan dan indikator per periode pada lokasi | `lat`, `lon`, `start`, `end` | LocalLoop, CourtSlot, AERIVA |
| `GET /environment/recommendations` | Membandingkan periode tersedia dalam jendela | `lat`, `lon`, `start`, `end` | LocalLoop, AERIVA; CourtSlot jika dibutuhkan |
| `POST /auth/register` | Membuat akun aplikasi AERIVA | nama, email, password dalam body HTTPS | Mobile AERIVA |
| `POST /auth/login` | Mendapat sesi | email, password dalam body HTTPS | Mobile AERIVA |

Auth pengguna: Bearer JWT; akses server mitra: `X-API-Key` per kelompok. Detail path auth dan kebijakan endpoint publik adalah **rancangan** untuk diputuskan Nanda. Jangan mengirim data sensitivitas pribadi mitra dan jangan simpan rahasia dalam contoh.

### 5.1 GET /environment/assessment

Contoh request hipotetis:

```http
GET /api/v1/environment/assessment?lat=-6.9175&lon=107.6191&start=2026-12-01T06%3A00%3A00%2B07%3A00&end=2026-12-01T12%3A00%3A00%2B07%3A00 HTTP/1.1
Host: <nama-terdaftar>.<domain-kelas>
X-API-Key: <API_KEY_MITRA>
```

Contoh respons **fiktif**, tidak menyiratkan prakiraan tersedia untuk tanggal tersebut:

```json
{
  "location": {"lat": -6.9175, "lon": 107.6191},
  "timezone": "Asia/Jakarta",
  "generated_at": "2026-11-30T18:00:00+07:00",
  "data_status": "partial",
  "periods": [
    {
      "start": "2026-12-01T06:00:00+07:00",
      "end": "2026-12-01T09:00:00+07:00",
      "caution_level": null,
      "assessment_status": "insufficient_data",
      "indicators": [
        {"type": "temperature", "value": 24, "unit": "°C", "status": "available", "source": "contoh", "updated_at": "2026-11-30T17:00:00+07:00"},
        {"type": "precipitation_probability", "value": 40, "unit": "%", "status": "available", "source": "contoh", "updated_at": "2026-11-30T17:00:00+07:00"},
        {"type": "uv_index", "value": null, "unit": "index", "status": "unavailable", "source": null, "updated_at": null}
      ]
    }
  ]
}
```

Hujan dapat berupa probabilitas (%) dan/atau jumlah (mm): definisi dan ketersediaan harus disepakati, jangan menukar satuan. Status tiap indikator serta alasan data tidak memadai harus jelas. Kategori `good`, `moderate`, `caution`, `high_caution` hanya boleh dikeluarkan setelah aturan/ambang bersumber dan data memadai. Pengguna memahami itu tingkat lingkungan, bukan diagnosis atau jaminan acara aman.

### 5.2 GET /environment/recommendations

Query sama: `lat`, `lon`, `start`, `end`. Misalnya mitra mengirim jendela acara pukul 06.00–12.00 dan menerima salah satu periode yang relatif lebih mendukung, jika data mencukupi. Tidak mengirim sensitivitas atau identitas peserta.

```json
{
  "location": {"lat": -6.9175, "lon": 107.6191},
  "window": {"start": "2026-12-01T06:00:00+07:00", "end": "2026-12-01T12:00:00+07:00"},
  "status": "insufficient_data",
  "recommended_period": null,
  "reasons": [],
  "message": "Data belum cukup untuk menentukan waktu yang disarankan.",
  "generated_at": "2026-11-30T18:00:00+07:00"
}
```

Jika tersedia, `recommended_period` berisi `start`, `end`, `caution_level`; `reasons` menjelaskan indikator dan perbandingan aktual. Aturan minimum data, tie dan trade-off harus ditetapkan bersama sebelum hasil dinyatakan valid.

### 5.3 Kesalahan dan perilaku khusus

| HTTP | Contoh | Makna/aksi |
|---|---|---|
| 400 | `INVALID_TIME_RANGE` | Parameter format/satuan salah atau rentang terbalik |
| 401 | `UNAUTHENTICATED` | Token atau API key tidak valid/tidak ada |
| 403 | `FORBIDDEN` | Key/akun tidak berhak |
| 422 | `OUT_OF_FORECAST_RANGE` | Usulan: jendela di luar cakupan; tanggapan perlu disepakati |
| 429 | `RATE_LIMITED` | Batasi panggilan dan sediakan `Retry-After` bila mungkin |
| 503 | `SOURCE_UNAVAILABLE` | Sumber data tidak dapat diakses |

Contoh format error usulan: `{"error":{"code":"SOURCE_UNAVAILABLE","message":"Data lingkungan sementara tidak tersedia."}}`. Data parsial dapat `200` dengan status parsial; jendela di luar cakupan diusulkan `422`. Bedakan kedua keadaan dan sepakati dengan mitra. Mitra boleh tetap menjalankan registrasi/reservasi saat AERIVA gagal; advis tidak otomatis membatalkan kegiatan.

## 6. API LocalLoop yang dibutuhkan AERIVA

Berdasarkan `partner-catalog.md` dari LocalLoop, endpoint katalog sudah diimplementasikan. Base URL HTTPS publik dan API key untuk AERIVA akan diberikan LocalLoop setelah deployment dan pengujian. Katalog hanya berisi acara berstatus published dan aksesnya read-only dengan header `X-API-Key`.

| Method | Path | Kegunaan |
|---|---|---|
| GET | `/api/public/events` | Daftar acara publik, diurutkan berdasarkan ID menaik |
| GET | `/api/public/events/{event_id}` | Detail satu acara publik berdasarkan ID bilangan bulat positif |

Filter opsional daftar adalah `q`, `category`, `event_format`, `location`, `starts_from`, dan `starts_before`. Rentang waktu memakai batas awal inklusif dan akhir eksklusif, serta membutuhkan waktu ISO 8601 dengan zona waktu. Filter digabungkan dengan AND. Endpoint MVP tidak menyediakan pagination. `event_format=in_person` berarti acara luring dan tidak menjamin kegiatan di luar ruangan.

Respons daftar berbentuk `{"items": [...]}`; jika kosong, `{"items": []}`. Detail mengembalikan satu objek acara tanpa pembungkus `items`. Field yang selalu ada adalah `id`, `title`, `capacity`, `waitlist_enabled`, dan `status`. Field lain seperti `category`, `description`, `event_format`, `starts_at`, `ends_at`, `location`, `registration_opens_at`, dan `registration_closes_at` bersifat opsional dan dapat tidak disertakan. Waktu dikembalikan dalam UTC. `capacity` adalah kapasitas total, bukan jumlah kursi tersisa.

Contoh respons dari panduan LocalLoop berikut menggunakan data ilustrasi:

```json
{"items":[{"id":7,"title":"Community Sports Day","capacity":40,"waitlist_enabled":true,"status":"published","category":"Sports","description":"Outdoor activities with local communities","event_format":"in_person","starts_at":"2026-12-05T02:00:00Z","ends_at":"2026-12-05T05:00:00Z","location":"Bandung, West Java","registration_opens_at":"2026-11-25T00:00:00Z","registration_closes_at":"2026-12-04T16:00:00Z"}]}
```

Lokasi berupa teks dan tidak menyertakan koordinat. AERIVA perlu mendapatkan koordinat melalui mekanisme yang disepakati dengan LocalLoop sebelum meminta penilaian lingkungan. Acara online atau acara yang waktu/lokasinya tidak tersedia perlu ditangani sesuai data yang ada. API ini tidak menyediakan prakiraan, skor lingkungan, data peserta, registrasi individual, atau data kehadiran.

Error dari LocalLoop mencakup `401 INVALID_API_KEY`, `404 EVENT_NOT_FOUND`, `422` validasi FastAPI, dan `503 PARTNER_AUTH_UNAVAILABLE`. Error 401, 404, dan 503 berbentuk objek dengan field `code` dan `message` pada tingkat teratas. Kunci API diberikan secara privat, dipakai di header, dan disimpan pada layanan integrasi di luar STB, bukan di aplikasi mobile.

## 7. API CourtSlot yang dibutuhkan AERIVA

Dokumen CourtSlot menyebut API baca fasilitas dan ketersediaan agregat, tetapi **tidak menetapkan path spesifik yang terverifikasi**. Dua path di bawah adalah usulan untuk didiskusikan, bukan endpoint CourtSlot yang sudah ada:

| Usulan method dan path | Dicari berdasarkan | Hasil minimal |
|---|---|---|
| `GET /api/public/facilities` | koordinat/radius atau kota, jenis, halaman | ID, nama, jenis, lokasi, koordinat, status, detail |
| `GET /api/public/facilities/{id}/availability` | ID fasilitas, tanggal atau start/end | unit, periode, status tersedia/tertutup, kapasitas agregat jika diizinkan |

Contoh respons **fiktif usulan**:

```json
{"facility":{"id":"fac-demo-01","name":"Taman contoh","type":"park","location":{"lat":-6.9175,"lon":107.6191}},"slots":[{"start":"2026-12-01T07:00:00+07:00","end":"2026-12-01T08:00:00+07:00","status":"available","remaining_capacity":10}],"updated_at":"2026-11-30T18:00:00+07:00"}
```

Pengguna memilih fasilitas dan slot → AERIVA menampilkan ringkasan lingkungan untuk koordinat/periode → bila ingin memesan, pengguna mengikuti mekanisme resmi CourtSlot. Ketersediaan agregat bukan konfirmasi reservasi; cuaca tidak otomatis mengubah reservasi. Kesesuaian fitur ini dengan prioritas MVP AERIVA perlu disetujui kelompok sebelum dibuat.

## 8. Yang perlu ditanyakan kepada kedua mitra

1. Base URL HTTPS, dokumentasi OpenAPI/Postman dan status live; path, method, contoh respons dan error.
2. Query/filter yang didukung, format koordinat, zona waktu, format tanggal, pagination, cakupan lokasi, laju pembaruan dan limit.
3. Cara mendapatkan API key masing-masing, masa berlaku, akun uji bila relevan dan kontak teknis.
4. LocalLoop: minta base URL HTTPS, API key privat, dan sepakati mekanisme mendapatkan koordinat dari lokasi teks. Kontrak katalog dan detail publik sudah dijelaskan dalam panduan mitra.
5. CourtSlot: API katalog dan ketersediaan agregat, skema fasilitas/unit/slot dan penutupan, serta cakupan kota/data uji.
6. Apakah kedua mitra menerima desain AERIVA assessment/recommendations, kebutuhan indikator hujan, rentang waktu dan definisi status parsial.
7. Tulis kesepakatan pada README kedua pihak setelah disetujui, lalu uji nyata dan simpan bukti. Status calon/perencanaan saat ini bukan bukti integrasi.

## 9. Tugas 2: pembagian kerja dan kriteria selesai

| Pekerjaan | Penanggung jawab yang disarankan | Bukti |
|---|---|---|
| Memetakan kebutuhan dan menyusun kontrak/draf | Kayta bersama Nanda dan mitra | Dokumen API yang telah disepakati, contoh request/response |
| Aturan inti, validasi dan implementasi API | Nanda | source code, pengujian, daftar endpoint aktual |
| Hak akses, JWT, key, data uji | Nanda; koordinasi bersama | dokumentasi akses, akun uji, tanpa rahasia dalam repo |
| Docker, gateway, limit CPU/memori, tunnel/STB | Nanda | compose, log, `docker stats`, endpoint HTTPS aktif |
| Penyusunan dokumentasi | Kayta dan Nanda | OpenAPI/Postman, contoh, README.pdf sesuai output Tugas 2 |
| Registrasi nama/domain/API | kelompok, sesuai hak akses | nama unik, URL dan dokumentasi di API Registry |
| Integrasi mitra dan aplikasi | bersama, tahap Tugas 3/PWAM | panggilan nyata dari fitur, README kedua pihak, bukti uji |

Tugas 2 mengumpulkan URL microservice, URL repo, dokumentasi dan README.pdf. Repo/draf saja belum menyelesaikan deployment dan HTTPS. Contoh resource limit pada slide bukan angka wajib; tentukan sesuai STB. Setiap kontainer sesuai ketentuan memerlukan limit CPU/memori dan restart policy. Jangan menaruh data rahasia di GitHub.

## 10. Bisa dikerjakan melalui GitHub?

**Bisa untuk menulis dan membagikan desain:** file Markdown ini, OpenAPI YAML/JSON, contoh request/response fiktif, README dan daftar kebutuhan dapat ditaruh di repo yang disepakati. File dapat diedit melalui browser GitHub atau VS Code dan dibagikan ke Nanda. GitHub menyimpan file; **GitHub sendiri tidak menjalankan tunnel atau mendeploy core pada STB**.

Jika repo AERIVA belum ada atau belum diketahui, tentukan repo bersama Nanda; jangan menganggap repo praktikum KatalogKu adalah repo AERIVA. Buat draf lokal dahulu, tinjau bersama, lalu Kayta melakukan commit/push manual sesuai preferensi. Jangan taruh `.env`, API key, token tunnel, password, database pribadi atau data peserta ke repo. Repo privat dan hak akses mitra diputuskan pemilik repo.

## 11. Langkah berikutnya

1. Sepakati dengan Nanda nama tim `aeriva`, ruang lingkup endpoint, stack dan lokasi repo; kelas AERIVA sudah diketahui K02.
2. Periksa Registry untuk ketersediaan nama dan alamat mitra; dapatkan dokumentasi yang sebenarnya.
3. Kirim kebutuhan pada Bagian 8 melalui kanal yang dipilih sendiri; catat koreksi mitra, query dan skema final.
4. Perbarui spesifikasi ini menjadi kontrak OpenAPI/Postman yang konsisten dengan implementasi yang disepakati; tandai nilai contoh.
5. Nanda membuat dan menguji layanan inti di laptop/STB, menyiapkan resource limits dan mengaktifkan tunnel sesuai kelas.
6. Periksa HTTPS health dan setiap endpoint nyata dari jaringan luar, autentikasi, error, sumber dan data hilang; catat hasil tanpa memalsukan bukti.
7. Siapkan README.pdf dan link repo/dokumentasi untuk Tugas 2; integrasikan kedua layanan pada fitur nyata untuk Tugas 3.

Tenggat dalam dokumen: akhir M14 untuk URL/dokumentasi Registry; final 13 Desember 2026 pukul 23.59 WIB. Periksa pengumuman terbaru pengajar bila ada perubahan.

## 12. Kontrak acuan bersama

Gunakan Bagian 13 sebagai **satu usulan kontrak yang tetap** untuk LocalLoop, CourtSlot, dan AERIVA. Base URL LocalLoop akan diberikan oleh tim mereka. Nama host CourtSlot `courtslot.stei.fun` dan AERIVA `aeriva.stei.site` adalah usulan yang masih harus tersedia di Registry dan dipakai pada tunnel masing-masing tim. Dokumen ini tidak dapat menetapkan nama Registry atau implementasi untuk kelompok lain; apabila satu nama tidak tersedia atau tim mitra menggunakan kontrak berbeda, atur alamat dan penerjemahan data pada lapisan integrasi agar antarmuka yang digunakan layar AERIVA dapat tetap sama.

## 13. Daftar alamat endpoint dua arah untuk kesepakatan

Bagian ini adalah daftar yang bisa dipakai ketiga tim untuk menyamakan kontrak. **Baris bertanda “usulan” belum boleh dianggap sebagai alamat nyata yang sudah disepakati atau aktif.** Nama hostname di antara `<...>` harus diganti setelah tim pemiliknya memberikan alamat Registry yang benar. Jangan gunakan contoh respons atau link placeholder sebagai bukti pengujian.

### 13.1 LocalLoop → diambil oleh AERIVA

| Informasi | Method | Endpoint | Status |
|---|---|---|---|
| Daftar acara publik | GET | `{LOCALLOOP_BASE_URL}/api/public/events` | Diimplementasikan menurut panduan mitra. Base URL dan API key AERIVA belum diberikan. |
| Detail acara publik | GET | `{LOCALLOOP_BASE_URL}/api/public/events/{event_id}` | Diimplementasikan menurut panduan mitra. ID berupa bilangan bulat positif. |

Semua request memakai header `X-API-Key`. Field acara, filter yang didukung, dan bentuk respons dijelaskan dalam Bagian 6 dan 14.1. Lokasi adalah teks tanpa koordinat, sehingga mekanisme memperoleh koordinat masih perlu disepakati.

### 13.2 CourtSlot → diambil oleh AERIVA

Dokumen CourtSlot menyatakan ada rencana API baca fasilitas dan ketersediaan agregat, tetapi **tidak memberikan path pastinya**. Nama berikut adalah rancangan yang diajukan AERIVA untuk disepakati, bukan alamat yang sudah ditetapkan CourtSlot.

| Nama informasi | Method usulan | Alamat endpoint usulan | Status dan informasi yang diambil |
|---|---|---|---|
| Daftar fasilitas publik | GET | `https://courtslot.stei.fun/api/public/facilities` | **Usulan.** Konfirmasi path, filter kota/koordinat/jenis, ID, nama, alamat dan koordinat. |
| Ketersediaan fasilitas | GET | `https://courtslot.stei.fun/api/public/facilities/{id}/availability` | **Usulan.** Konfirmasi path, ID fasilitas/unit, rentang waktu, status slot dan kapasitas agregat. |

Contoh kebutuhan: AERIVA mengambil fasilitas yang relevan serta, bila tersedia dan disepakati, informasi slot. AERIVA memakai koordinat dan waktu pilihan untuk menampilkan penilaian lingkungan. CourtSlot tetap menjadi pemilik data dan keputusan reservasi; ketersediaan yang dibaca AERIVA bukan konfirmasi pemesanan.

### 13.3 AERIVA → diambil oleh LocalLoop dan CourtSlot

Karena AERIVA berada di K02, alamat dasar yang diusulkan adalah `https://aeriva.stei.site`. **Nama `aeriva` belum diverifikasi di Registry dan endpoint berikut belum dibuktikan telah diimplementasikan.** Jika nama Registry berubah, seluruh URL di bawah menyesuaikan hostname yang terdaftar.

| Nama informasi | Method | Alamat endpoint usulan | Dipakai oleh | Parameter dan kegunaan |
|---|---|---|---|---|
| Kondisi dan penilaian lingkungan per periode | GET | `https://aeriva.stei.site/api/v1/environment/assessment` | LocalLoop dan CourtSlot | `lat`, `lon`, `start`, `end`. Menghasilkan periode, indikator yang tersedia, sumber/pembaruan dan status penilaian. CourtSlot dapat memetakan informasi hujan ke waktu slot jika data dan kontraknya tersedia. |
| Perbandingan waktu aktivitas | GET | `https://aeriva.stei.site/api/v1/environment/recommendations` | LocalLoop jika disepakati; CourtSlot bila diperlukan | `lat`, `lon`, `start`, `end`. Memberikan periode relatif lebih mendukung dan alasan ketika data memadai. Kebutuhan mitra perlu dikonfirmasi. |
| Kesehatan layanan | GET | `https://aeriva.stei.site/api/v1/health` | Tim AERIVA dan mitra bila disepakati | Memeriksa status layanan; isi respons final ditentukan implementasi. |

**Contoh susunan URL usulan**, dengan nilai fiktif dan placeholder akses:

```http
GET https://aeriva.stei.site/api/v1/environment/assessment?lat=-6.9175&lon=107.6191&start=2026-12-01T06%3A00%3A00%2B07%3A00&end=2026-12-01T09%3A00%3A00%2B07%3A00
X-API-Key: <API_KEY_YANG_DIBERIKAN_AERIVA>
```

Respons contoh dan keadaan `insufficient_data` ada pada Bagian 5. Jangan memberikan kategori `Good` untuk data yang tidak tersedia, dan jangan menjanjikan rekomendasi untuk tanggal di luar cakupan prakiraan. LocalLoop dan CourtSlot tetap menangani keputusan partisipasi/reservasi pada sistem masing-masing.

### 13.4 Kesimpulan alamat yang perlu dikonfirmasi

1. **AERIVA:** cek nama `aeriva` di Registry K02, lalu konfirmasi apakah base URL benar `https://aeriva.stei.site` dan path assessment/recommendations disetujui serta diimplementasikan Nanda.
2. **LocalLoop:** minta base URL HTTPS dan API key privat yang akan diberikan setelah deployment, lalu uji `/api/public/events` dan `/api/public/events/{event_id}`. Sepakati cara memperoleh koordinat dari lokasi teks.
3. **CourtSlot:** minta hostname K01 persis serta path, parameter dan respons final untuk fasilitas dan ketersediaan. Kedua path di 13.2 masih usulan.
4. Setelah ketiga kelompok menyepakati kontrak dan mendaftarkan URL, ganti placeholder, tambahkan contoh respons nyata yang aman, dan catat versi serta tanggal konfirmasi. Pengujian nyata tetap diperlukan untuk membuktikan integrasi.


## 14. Kontrak acuan tetap untuk implementasi

Ketiga tim diharapkan memakai bentuk berikut sebagai acuan bersama. **Bagian ini ditetapkan sebagai rancangan AERIVA, bukan klaim bahwa tim lain sudah menyetujui, mendaftarkan domain, atau mengimplementasikannya.** Perubahan di luar kendali tim tetap mungkin; konfigurasi URL dan adapter memungkinkan antarmuka aplikasi tetap stabil. Semua contoh fiktif.

### 14.1 LocalLoop — katalog publik

**GET `{LOCALLOOP_BASE_URL}/api/public/events`**

| Parameter | Tipe | Ketentuan |
|---|---|---|
| `q` | string, maks. 100 karakter | Pencarian judul atau deskripsi tanpa membedakan kapital |
| `category` | string, maks. 64 karakter | Kategori teks dengan kecocokan penuh tanpa membedakan kapital |
| `event_format` | `in_person` atau `online` | Kecocokan format acara |
| `location` | string, maks. 100 karakter | Pencarian sebagian teks lokasi tanpa membedakan kapital |
| `starts_from` | datetime ISO 8601 dengan zona waktu | Waktu mulai acara pada atau setelah nilai ini |
| `starts_before` | datetime ISO 8601 dengan zona waktu | Waktu mulai acara sebelum nilai ini |

Semua parameter opsional dan digabungkan dengan AND. Server membandingkan waktu sebagai UTC. Tidak ada pagination, pencarian koordinat/radius, atau filter indoor/outdoor dalam kontrak MVP. Detail memakai **GET `{LOCALLOOP_BASE_URL}/api/public/events/{event_id}`** dan mengembalikan satu objek, bukan daftar. Header `X-API-Key` wajib untuk kedua endpoint. Lihat contoh respons dan field pada Bagian 6.

Base URL dan API key masih menunggu LocalLoop. Kontrak ini tidak memuat koordinat sehingga penilaian lingkungan berdasarkan lokasi acara memerlukan mekanisme penyelesaian lokasi yang disepakati.

### 14.2 CourtSlot — fasilitas dan slot publik

**GET `https://courtslot.stei.fun/api/public/facilities`**

| Parameter | Tipe | Ketentuan acuan |
|---|---|---|
| `lat`, `lon`, `radius_km` | number | Opsional; koordinat bersama dan radius dalam km |
| `city`, `type` | string | Opsional; wilayah dan jenis fasilitas |
| `limit`, `cursor` | integer, string | Opsional; ukuran dan penanda halaman |

Respons acuan:

```json
{"items":[{"id":"fac-demo-01","name":"Taman contoh","type":"park","address":"Alamat contoh","location":{"lat":-6.9175,"lon":107.6191},"status":"open","detail_url":null,"updated_at":"2026-11-30T18:00:00+07:00"}],"next_cursor":null}
```

**GET `https://courtslot.stei.fun/api/public/facilities/{id}/availability?start=...&end=...`** menggunakan ID dari katalog dan waktu ISO 8601 ber-offset, dengan `start` inklusif dan `end` eksklusif. Respons acuan:

```json
{"facility_id":"fac-demo-01","slots":[{"unit_id":"unit-demo-01","start":"2026-12-01T07:00:00+07:00","end":"2026-12-01T08:00:00+07:00","status":"available","remaining_capacity":10}],"updated_at":"2026-11-30T18:00:00+07:00"}
```

Kedua path CourtSlot adalah **usulan baru**. Data agregat bersifat informasi saat diperbarui dan bukan bukti reservasi. Tidak meminta identitas warga. Waktu, struktur unit, arti status dan sisa kapasitas perlu persetujuan CourtSlot.

### 14.3 AERIVA — digunakan kedua mitra

**GET `https://aeriva.stei.site/api/v1/environment/assessment?lat=...&lon=...&start=...&end=...`** menyediakan data per periode dan status ketersediaan. **GET `https://aeriva.stei.site/api/v1/environment/recommendations?lat=...&lon=...&start=...&end=...`** menyediakan perbandingan periode jika data mencukupi. Contoh JSON, status dan batas klaim ada pada Bagian 5. Auth mitra dirancang memakai `X-API-Key` yang diberikan terpisah untuk setiap kelompok; mekanisme final harus disetujui dan diterapkan oleh backend.

### 14.4 Pengaturan AERIVA agar kode layar tetap konsisten

Simpan `LOCALLOOP_BASE_URL`, `COURTSLOT_BASE_URL`, dan `AERIVA_BASE_URL` dalam konfigurasi lingkungan layanan integrasi di luar STB. Kode layar hanya menggunakan bentuk data yang didefinisikan di atas melalui adapter, sedangkan URL dan perbedaan format ditangani di integrator. Jangan memasukkan API key mitra ke aplikasi Expo yang didistribusikan. Pada tahap ini belum ada kode, registrasi domain, atau panggilan API yang dibuat oleh dokumen ini.
