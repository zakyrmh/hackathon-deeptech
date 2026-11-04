# Sumber Data Raw

Dokumen ini mencatat asal, cakupan, integritas, dan keterbatasan setiap data mentah yang digunakan dalam proyek **Food Demand Intelligence**.

Tanggal pencatatan: **3 November 2026**.

## 1. Harga pangan PIHPS Bank Indonesia

- **Penerbit/sistem:** Bank Indonesia — Pusat Informasi Harga Pangan Strategis Nasional (PIHPS Nasional)
- **Halaman sumber:** [Tabel Harga Pasar Tradisional Berdasarkan Daerah](https://www.bi.go.id/hargapangan/TabelHarga/PasarTradisionalDaerah)
- **Jenis data:** perkembangan harga pangan harian, satuan rupiah
- **Rentang tanggal dalam file:** 25 Oktober 2024–2 November 2026
- **Jumlah tanggal:** 527 tanggal per seri
- **Format asli yang tersedia:** XLSX
- **Status provenance:** file lokal yang telah tersedia dan dinyatakan berasal dari halaman PIHPS di atas; unduhan ulang tidak dilakukan pada pemindahan ini.

| File raw | Seri di dalam file | SHA-256 |
| --- | --- | --- |
| [`pihps_bank_indonesia/bawang_merah_ukuran_sedang.xlsx`](pihps_bank_indonesia/bawang_merah_ukuran_sedang.xlsx) | Bawang Merah; Bawang Merah Ukuran Sedang | `e571d2b4ff41d645cd3b00de05fd0b115a3e880b6d6825a2bb19dc01862f40f8` |
| [`pihps_bank_indonesia/cabai_merah_keriting.xlsx`](pihps_bank_indonesia/cabai_merah_keriting.xlsx) | Cabai Merah; Cabai Merah Keriting | `ddb831c0de5d46112f42822a9d501328d3819389b2690264b4ca512fcfad0a97` |
| [`pihps_bank_indonesia/cabai_rawit_merah.xlsx`](pihps_bank_indonesia/cabai_rawit_merah.xlsx) | Cabai Rawit | `0fd142c2111dcab8711d434f3e90ae3ac6e09c2e6812ece03132ed31aacc10a6` |

### Batasan provenance PIHPS

Halaman PIHPS menyediakan filter **komoditas, provinsi, kabupaten/kota, pasar, tipe laporan, tanggal mulai, dan tanggal selesai**. Akan tetapi, ketiga file XLSX tidak menyimpan nilai filter wilayah/pasar tersebut. Karena itu:

- komoditas dan rentang waktu dapat diverifikasi langsung dari isi file;
- provinsi, kabupaten/kota, pasar, dan tipe laporan yang dipilih saat ekspor belum dapat diverifikasi hanya dari file;
- file tidak boleh diberi label “Sumatera Barat” atau wilayah tertentu sebelum parameter ekspornya dikonfirmasi;
- tanda `-` adalah nilai yang tidak tersedia pada sumber dan tidak boleh otomatis dianggap nol.

## 2. Iklim bulanan BMKG

- **Penerbit:** Badan Meteorologi, Klimatologi, dan Geofisika (BMKG)
- **Sumber:** [BMKG Data Online — Data Bulanan](https://dataonline.bmkg.go.id/data-bulanan)
- **File raw:** [`bmkg/DataIklimBulanan_2024-11_2026-09.xlsx`](bmkg/DataIklimBulanan_2024-11_2026-09.xlsx)
- **Periode:** November 2024–September 2026
- **Stasiun:** WMO 96165 Stasiun Geofisika Padang Panjang dan WMO 96161 Stasiun Meteorologi Maritim Teluk Bayur
- **Variabel:** curah hujan bulanan (`rainfall`, mm), kecepatan angin rata-rata (`wind_avg`, m/s), kelembapan rata-rata (`hum_avg`, %), dan temperatur rata-rata (`temp_avg`, °C)
- **SHA-256:** `e7f7919b0ef59e5a2bf70899629901df862201efe48f6bbed141e99b6fda5bb9`

### Batasan BMKG

- Portal membatasi pengambilan data; file ini adalah satu-satunya ekspor BMKG yang tersedia dalam proyek.
- Tanda `-` dan kode `9999` berarti tidak ada data/tidak dilakukan pengukuran, bukan nilai nol.
- Jangan melakukan interpolasi atau imputasi sebelum metode dan alasannya ditetapkan dalam pipeline pemrosesan.

## 3. Produksi hortikultura BPS Sumatera Barat

- **Penerbit:** Badan Pusat Statistik Provinsi Sumatera Barat
- **Sumber:** [Produksi Tanaman Sayuran dan Buah-buahan Semusim Menurut Kabupaten/Kota dan Jenis Tanaman, 2024](https://sumbar.bps.go.id/id/statistics-table/3/ZUhFd1JtZzJWVVpqWTJsV05XTllhVmhRSzFoNFFUMDkjMw==/produksi-tanaman-sayuran-dan-buah-buahan-semusim-menurut-kabupaten-kota-dan-jenis-tanaman---di-provinsi-sumatera-barat--2024.html?year=2024)
- **File raw:** [`bps_production/production_sumbar_2024_source_snapshot.csv`](bps_production/production_sumbar_2024_source_snapshot.csv)
- **Periode:** 2024
- **Status:** snapshot tabel web resmi, bukan unduhan asli BPS
- **SHA-256:** `acc0241f30d15de34933292351bec5f9eaaa473cf706bda856f7011797c1eb48`

## 4. Konsumsi pangan BPS Sumatera Barat

- **Penerbit:** Badan Pusat Statistik Provinsi Sumatera Barat
- **Sumber:** [Pola Konsumsi Makanan Penduduk Provinsi Sumatera Barat 2025](https://sumbar.bps.go.id/id/publication/2026/03/17/07378cc39d6b72a965e75336/pola-konsumsi-makanan-penduduk-provinsi-sumatera-barat-2025.html)
- **Tabel:** Lampiran 4, halaman cetak 111–112 / halaman PDF 128–129
- **File raw:** [`bps_consumption/consumption_sumbar_2025_appendix4_source_snapshot.csv`](bps_consumption/consumption_sumbar_2025_appendix4_source_snapshot.csv)
- **Periode:** Susenas Maret 2025
- **Status:** snapshot tabel publikasi resmi, bukan PDF asli BPS
- **SHA-256:** `8849fff8214c1d20f9846288052fbaabb8953c905b1a4197226b0ca91de78c18`

## 5. Penduduk BPS Sumatera Barat

- **Penerbit:** Badan Pusat Statistik Provinsi Sumatera Barat
- **Sumber:** [Jumlah Penduduk dan Indikator Kependudukan Menurut Kabupaten/Kota, 2025](https://sumbar.bps.go.id/id/statistics-table/3/V1ZSbFRUY3lTbFpEYTNsVWNGcDZjek53YkhsNFFUMDkjMw==/jumlah-penduduk--laju-pertumbuhan-penduduk--distribusi-persentase-penduduk--kepadatan-penduduk--rasio-jenis-kelamin-penduduk-menurut-kabupaten-kota-di-provinsi-sumatera-barat--2025.html?year=2025)
- **File raw:** [`bps_population/population_sumbar_2025_source_snapshot.csv`](bps_population/population_sumbar_2025_source_snapshot.csv)
- **Periode:** 2025
- **Status:** snapshot tabel web resmi, bukan unduhan asli BPS
- **SHA-256:** `e0978216d43b040d49389229a6b476da260edaf37123ae5f834064c2f867455b`

## Verifikasi integritas

Jalankan dari direktori `data`:

```bash
sha256sum --check CHECKSUMS.sha256
```

Metadata terstruktur seluruh sumber juga tersedia di [`../MANIFEST.csv`](../MANIFEST.csv).
