# Panduan Dataset Food Demand Intelligence

Terakhir diperiksa: 2 November 2026.

## Jawaban singkat

Untuk MVP, jangan menunggu satu “dataset lengkap”. Gabungkan empat lapisan data:

1. **harga harian** sebagai sinyal permintaan dan tekanan pasar dari PIHPS Bank Indonesia;
2. **produksi dan konsumsi wilayah** sebagai baseline surplus/defisit dari BPS;
3. **cuaca harian** sebagai fitur eksternal dari BMKG; dan
4. **stok, umur simpan, serta biaya angkut** dari mitra atau template operasional buatan tim.

Lapisan keempat tidak tersedia lengkap sebagai open data. Ia harus diminta dari Dinas Pangan, BUMD/agregator, gudang, atau disimulasikan secara transparan untuk demonstrasi.

## Prioritas sumber

| Prioritas | Data | Sumber dan cara memperoleh | Granularitas/format | Kegunaan | Batasan |
|---|---|---|---|---|---|
| P0 | Harga konsumen tiga komoditas | Buka [PIHPS – Pasar Tradisional, Berdasarkan Daerah](https://www.bi.go.id/hargapangan/TabelHarga/PasarTradisionalDaerah). Pilih Sumatera Barat, kabupaten/kota/pasar yang tersedia, laporan harian, rentang tanggal, lalu **Download**. Ulangi untuk bawang merah, cabai merah keriting, dan cabai rawit merah. | Harian pada hari kerja; provinsi/kabupaten-kota/pasar; hasil ekspor dari UI | Target/proxy utama model deret waktu; volatilitas dan disparitas harga | PIHPS tidak mendokumentasikan API publik pada halaman ini. Jangan bergantung pada endpoint internal. Tidak semua komoditas tersedia di setiap kota sampel. |
| P0 | Produksi hortikultura | Unduh tabel [produksi sayuran menurut kabupaten/kota dan jenis tanaman di Sumatera Barat](https://sumbar.bps.go.id/id/statistics-table/3/ZUhFd1JtZzJWVVpqWTJsV05XTllhVmhRSzFoNFFUMDkjMw==/produksi-tanaman-sayuran-menurut-kabupaten-kota-dan-jenis-tanaman-di-provinsi-sumatera-barat.html?year=2023). Tabel memuat bawang merah, cabai rawit, cabai besar, dan cabai keriting. Publikasi pendamping: [Produksi Tanaman Hortikultura Sumatera Barat 2023](https://sumbar.bps.go.id/id/publication/2024/09/26/3474766909f50d06f360e2b6/horticultural-crop-production-in-sumatera-barat-province-2023.html). | Kabupaten/kota; tahunan; tabel web/unduhan publikasi | Prior kapasitas pasokan dan identifikasi sentra surplus | Terlalu jarang untuk forecast harian; jangan dianggap sebagai stok gudang. Satuan tabel perlu dinormalisasi (umumnya kuintal). |
| P0 | Konsumsi komoditas | Unduh [Pola Konsumsi Makanan Penduduk Provinsi Sumatera Barat 2025](https://sumbar.bps.go.id/en/publication/2026/03/17/07378cc39d6b72a965e75336/food-consumption-patterns-of-the-population-of-sumatera-barat-province-2025.html). Publikasi menggunakan Susenas Maret 2025, mencakup kuantitas 211 komoditas, dan lampirannya menyediakan estimasi kabupaten/kota. | Provinsi dan kabupaten/kota; tahunan; PDF | Baseline kebutuhan: konsumsi per kapita × populasi | Bukan transaksi harian; pecah ke harian hanya sebagai baseline dan beri faktor musiman. |
| P0 | Data operasional mitra | Kirim template CSV kepada Dinas Pangan/BUMD/agregator/gudang untuk diisi. Skema minimum ada di bawah. | Gudang–batch–hari; CSV/XLSX | Input wajib optimasi FEFO, stok, kuota, kapasitas dan biaya | Umumnya tidak terbuka; perlu izin dan definisi data bersama. |
| P1 | Cuaca | Daftar/login di [BMKG Data Online](https://dataonline.bmkg.go.id/dataonline-home), pilih stasiun terdekat, lalu unduh curah hujan, temperatur, kelembapan, penyinaran, dan angin. | Stasiun; harian; unduhan portal | Fitur panen, pasokan, kerusakan, dan keterlambatan distribusi | Unduhan data iklim dibatasi 30 hari per proses; ulangi per bulan. |
| P1 | Harga bulanan pembanding | [Open Data Badan Pangan Nasional – harga konsumen provinsi](https://data.badanpangan.go.id/datasetpublications/g7c/rata-rata-harga-pangan-konsumen-provinsi) menyediakan seri provinsi dan tiga komoditas target. Portal menandai format CSV/JSON/XLSX. | Provinsi; bulanan; CSV/JSON/XLSX | Validasi agregat PIHPS dan fallback demonstrasi | Seri bulanan tidak cukup untuk target forecast 7–14 hari. Sebagian rilis terbaru Bapanas kini berstatus terbatas dan diarahkan ke [SAPA](https://sapa.badanpangan.go.id/). |
| P2 | Konsumsi nasional pembanding | Tabel BPS [rata-rata konsumsi per kapita seminggu 2015–2024](https://www.bps.go.id/id/statistics-table/1/MjMxNiMx/rata-rata-konsumsi-per-kapita-seminggu-beberapa-macam-bahan-makanan-penting--2015-2024.html) memuat bawang merah, cabai merah, dan cabai rawit. | Nasional; tahunan | Sanity check satuan dan tren konsumsi | Bukan data Sumatera Barat dan bukan target utama model. |

## Langkah unduh yang disarankan

### 1. Ambil harga harian PIHPS

1. Masuk ke halaman [Pasar Tradisional – Berdasarkan Daerah](https://www.bi.go.id/hargapangan/TabelHarga/PasarTradisionalDaerah).
2. Pilih `Provinsi = Sumatera Barat`.
3. Mulai dari agregat provinsi. Setelah pipeline berfungsi, ulangi pada kabupaten/kota dan pasar yang tersedia.
4. Pilih `Tipe Laporan = Harian` dan ambil minimal 2–3 tahun jika UI mengizinkan. Bila rentang unduh dibatasi, ekspor per bulan atau per tahun lalu gabungkan.
5. Ulangi untuk nama komoditas resmi PIHPS:
   - bawang merah ukuran sedang/lokal;
   - cabai merah keriting;
   - cabai rawit merah.
6. Simpan file mentah tanpa diedit di `data/raw/pihps/`, lalu buat hasil normalisasi di `data/processed/price_daily.csv`.

PIHPS menyatakan survei pasar tradisional dilakukan pada hari kerja Senin–Jumat. Harga merupakan transaksi eceran, dua pedagang per komoditas per pasar, dan agregat kota/provinsi dibentuk dari sampel yang tersedia. Definisi kualitas tiga komoditas juga dijelaskan di [FAQ resmi PIHPS](https://www.bi.go.id/hargapangan/Informasi/FAQ). Karena itu, akhir pekan/libur sebaiknya dibiarkan sebagai tanggal tanpa observasi atau diimputasi dengan flag; jangan diperlakukan sebagai harga yang benar-benar dicatat.

Skema normalisasi:

```text
date,province_code,regency_code,market_name,commodity,price_rp_per_kg,source,is_imputed
```

### 2. Bentuk baseline permintaan

Gunakan publikasi konsumsi BPS 2025 karena menyediakan kuantitas untuk 211 komoditas dan estimasi kabupaten/kota. Gabungkan dengan jumlah penduduk kabupaten/kota dari tabel BPS pada tahun yang sama.

Rumus awal:

```text
baseline_demand_kg_day = consumption_kg_capita_period
                         × population
                         ÷ days_in_period
```

Pastikan konversi satuan eksplisit: `1 ons = 0,1 kg`; `1 kuintal = 100 kg`. Baseline ini bukan label permintaan riil harian. Untuk MVP, target model yang defensible adalah **forecast harga/tekanan defisit** atau estimasi kebutuhan berbasis baseline konsumsi yang dikalibrasi terhadap data mitra.

### 3. Bentuk baseline pasokan

Dari tabel produksi BPS, ambil kolom:

```text
year,regency_code,commodity,harvest_area_ha,production_kg,productivity_kg_ha
```

Jangan membagi produksi tahunan rata ke 365 hari tanpa flag. Jika jadwal panen bulanan belum tersedia, buat profil musim panen sebagai asumsi skenario dan dokumentasikan bobot bulanannya. Untuk data lebih rinci, ajukan permintaan ke [Pelayanan Statistik Terpadu BPS](https://pst.bps.go.id/) atau konsultasi ke BPS Sumatera Barat; halaman BPS Sumbar juga mencantumkan jalur PST/Silastik dan kontak layanan.

### 4. Ambil cuaca BMKG

Unduh data harian stasiun yang paling mewakili sentra produksi dan wilayah konsumsi. Parameter minimum:

```text
date,station_id,rainfall_mm,temp_avg_c,humidity_avg_pct,wind_speed_avg_ms
```

BMKG menyebut portal menyediakan temperatur, curah hujan, kelembapan, penyinaran, dan angin dengan batas maksimum unduhan 30 hari. [FAQ BMKG](https://dataonline.bmkg.go.id/faq) mengarahkan pengguna ke menu Data Iklim dan menyarankan mengulang unduhan untuk rentang lebih panjang.

### 5. Minta data mitra dengan satu template sederhana

`inventory_batch.csv`

```text
snapshot_date,warehouse_id,batch_id,commodity,quantity_kg,harvest_date,received_date,estimated_expiry_date,storage_type
```

`demand_or_sales.csv`

```text
date,location_id,commodity,quantity_kg,transaction_type
```

`transport_capacity.csv`

```text
date,vehicle_id,origin_id,max_capacity_kg,fixed_cost_rp,cost_rp_per_km
```

`route_cost.csv`

```text
origin_id,destination_id,distance_km,travel_time_min,cost_rp,valid_from
```

Minimal minta 8–12 minggu data harian. Hilangkan nama personal, nomor telepon, dan pengenal sensitif. Buat data dictionary bersama mitra agar arti “stok”, “rusak”, “terjual”, dan “kedaluwarsa” konsisten.

## Dataset minimum untuk demo hackathon

Jika waktu sangat pendek, gunakan paket berikut:

1. PIHPS harga harian Sumatera Barat selama 2023–2026 untuk tiga komoditas;
2. BPS produksi per kabupaten/kota untuk satu atau beberapa tahun terakhir;
3. BPS konsumsi 2025 per kabupaten/kota;
4. BMKG curah hujan dan suhu pada 2–4 stasiun relevan;
5. data operasional sintetis untuk 3 gudang, 6 wilayah tujuan, dan 90 hari—dengan label jelas `synthetic=true`.

Untuk juri, pisahkan klaim:

- **model prediksi** diuji pada data harga publik nyata;
- **baseline kebutuhan** berasal dari konsumsi dan populasi resmi;
- **optimasi distribusi/FEFO** didemonstrasikan pada data operasional mitra atau skenario sintetis;
- **validasi lapangan** menjadi langkah pilot berikutnya.

Pemisahan ini lebih dapat dipertanggungjawabkan daripada menyebut harga sebagai permintaan aktual atau produksi tahunan sebagai stok harian.

## Struktur folder yang disarankan

```text
data/
  raw/
    pihps/
    bps_production/
    bps_consumption/
    bmkg/
    partner/
  processed/
    price_daily.csv
    production_capacity.csv
    demand_baseline.csv
    weather_daily.csv
    inventory_batch.csv
    route_cost.csv
  data_dictionary.md
  sources.md
```

Setiap file olahan sebaiknya memiliki `source_url`, `retrieved_at`, `license_or_terms`, versi transformasi, serta checksum file mentah.

## Akses terprogram dan kehati-hatian

- [WebAPI BPS](https://webapi.bps.go.id/developer/) dapat dipakai setelah pendaftaran aplikasi dan pemberian token. BPS mewajibkan token dirahasiakan dan melarang menaruhnya di repositori publik. Gunakan secret environment/CI, bukan file kode.
- Portal Bapanas menampilkan dataset dalam CSV/JSON/XLSX, tetapi status akses dapat berubah. Sebagai contoh, halaman [harga produsen provinsi](https://data.badanpangan.go.id/datasetpublications/pgs/rata-rata-harga-pangan-bulanan-produsen-provinsi) mengarahkan data lengkap ke SAPA.
- PIHPS menyediakan tombol unduh dari antarmuka web. Karena tidak ada API publik yang terdokumentasi pada halaman sumber, otomasi sebaiknya tetap melalui ekspor resmi atau izin tertulis, bukan mengandalkan endpoint internal yang sewaktu-waktu berubah.

## Kesimpulan keputusan data

Untuk target forecast 7–14 hari, **PIHPS harian adalah tulang punggung**. BPS dan Bapanas menyediakan baseline struktural, bukan label permintaan harian. Agar klaim “optimasi distribusi dan pengurangan susut” sahih, tim tetap memerlukan minimal satu sampel data stok-batch dan biaya angkut dari mitra; jika belum ada, gunakan skenario sintetis yang diberi label dan jangan melaporkannya sebagai hasil lapangan.
