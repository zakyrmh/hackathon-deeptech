# Dataset Produksi dan Konsumsi Sumatera Barat

Dataset ini disiapkan untuk MVP **Food Demand Intelligence** dan mencakup seluruh 19 kabupaten/kota di Sumatera Barat.

## File

- `raw/bps_production/production_sumbar_2024_source_snapshot.csv`: salinan baris relevan dari tabel statistik resmi BPS, mempertahankan label dan format angka sumber.
- `raw/bps_consumption/consumption_sumbar_2025_appendix4_source_snapshot.csv`: transkripsi tabel Lampiran 4 publikasi resmi BPS, termasuk total provinsi.
- `raw/bps_population/population_sumbar_2025_source_snapshot.csv`: salinan tabel kependudukan resmi BPS, mempertahankan seluruh kolom tabel sumber.
- `raw/pihps_bank_indonesia/*.xlsx`: tiga ekspor harga harian PIHPS untuk bawang merah ukuran sedang, cabai merah keriting, dan cabai rawit.
- `raw/bmkg/DataIklimBulanan_2024-11_2026-09.xlsx`: data iklim bulanan dari dua stasiun BMKG, November 2024–September 2026.
- `processed/`: sengaja dikosongkan. Data olahan harus dibuat melalui pipeline Python/notebook yang dapat diaudit.

## Sumber resmi

1. Produksi: [BPS Sumatera Barat — Produksi Tanaman Sayuran dan Buah-Buahan Semusim 2024](https://sumbar.bps.go.id/id/statistics-table/3/ZUhFd1JtZzJWVVpqWTJsV05XTllhVmhRSzFoNFFUMDkjMw==/produksi-tanaman-sayuran-dan-buah-buahan-semusim-menurut-kabupaten-kota-dan-jenis-tanaman---di-provinsi-sumatera-barat--2024.html?year=2024).
2. Konsumsi: [BPS Sumatera Barat — Pola Konsumsi Makanan Penduduk 2025](https://sumbar.bps.go.id/id/publication/2026/03/17/07378cc39d6b72a965e75336/pola-konsumsi-makanan-penduduk-provinsi-sumatera-barat-2025.html), Lampiran 4 halaman PDF 111–112 (halaman file 128–129).
3. Populasi: [BPS Sumatera Barat — Penduduk Menurut Kabupaten/Kota 2025](https://sumbar.bps.go.id/id/statistics-table/3/V1ZSbFRUY3lTbFpEYTNsVWNGcDZjek53YkhsNFFUMDkjMw==/jumlah-penduduk--laju-pertumbuhan-penduduk--distribusi-persentase-penduduk--kepadatan-penduduk--rasio-jenis-kelamin-penduduk-menurut-kabupaten-kota-di-provinsi-sumatera-barat--2025.html?year=2025).
4. Harga: [PIHPS Bank Indonesia — Tabel Harga Pasar Tradisional Berdasarkan Daerah](https://www.bi.go.id/hargapangan/TabelHarga/PasarTradisionalDaerah).
5. Iklim: [BMKG Data Online — Data Bulanan](https://dataonline.bmkg.go.id/data-bulanan).

Dokumentasi manusia-baca terdapat di [`raw/SUMBER_DATA_RAW.md`](raw/SUMBER_DATA_RAW.md). Detail terstruktur mengenai penerbit, periode, tanggal pengambilan, URL, metode akuisisi, file turunan, dan SHA-256 dicatat di [`MANIFEST.csv`](MANIFEST.csv). Integritas seluruh file dapat diperiksa dengan:

```bash
cd data
sha256sum --check CHECKSUMS.sha256
```

## Raw, snapshot, dan reproduksi

File BPS di `raw/` adalah **snapshot tabel sumber resmi**, bukan file PDF/XLSX asli yang diunduh dari BPS. Nilai, label wilayah, format desimal Indonesia, tanda `-`, dan baris total provinsi dipertahankan agar jejak transformasinya terlihat. Status ini dicatat secara eksplisit sebagai `is_original_download=false` di manifest. File PIHPS adalah XLSX lokal yang dinyatakan berasal dari halaman PIHPS; status unduhan aslinya dicatat sebagai `unverified` karena tidak diunduh ulang pada proses ini.

Skrip lama untuk membangun baseline BPS tersedia di `scripts/build_processed.py`, tetapi belum mencakup PIHPS dan BMKG. Skrip tersebut tidak dijalankan otomatis. Jika dijalankan, ia akan membuat ulang empat CSV baseline BPS:

```bash
python3 data/scripts/build_processed.py
```

Skrip memvalidasi jumlah wilayah, jumlah baris, serta total produksi provinsi sebelum menulis hasil. Pipeline terpadu BPS–PIHPS–BMKG masih perlu disusun sebelum folder `processed/` diisi kembali.

## Rumus baseline

```text
estimated_demand_kg_day = consumption_kg_capita_week × population / 7
estimated_demand_kg_year = consumption_kg_capita_week × population × 52
structural_balance_kg = production_kg_year_2024 - estimated_demand_kg_year_2025
```

`structural_balance_kg` hanya indikator struktural lintas tahun, bukan stok aktual atau neraca pangan resmi.

## Validasi

Jumlah produksi kabupaten/kota cocok dengan total provinsi pada tabel BPS:

| Komoditas | Total produksi 2024 (kuintal) |
| --- | ---: |
| Bawang merah | 2.307.184,11 |
| Cabai merah keriting | 1.141.695,55 |
| Cabai rawit | 277.163,69 |

Jumlah penduduk kabupaten/kota dari angka satu desimal adalah 5.914.200 orang, sedangkan total provinsi yang ditampilkan BPS adalah 5.914.300. Selisih 100 orang berasal dari pembulatan publikasi.

## Batasan penting

- Produksi 2024 adalah angka tetap dan dipakai sebagai kapasitas struktural, bukan stok harian.
- Konsumsi 2025 berasal dari Susenas Maret dan merupakan rata-rata per kapita per minggu, bukan transaksi harian.
- BPS mencatat konsumsi `Cabe merah` dan `Cabe rawit`, tidak memisahkan varietas/warna. Dataset menandainya sebagai proxy untuk `cabai_merah_keriting` dan `cabai_rawit_merah`.
- Nilai `-` pada produksi berarti tidak ada atau nol dan dinormalisasi menjadi `0`.
- XLSX PIHPS tidak menyimpan filter provinsi, kabupaten/kota, atau pasar yang dipilih ketika ekspor. Cakupan wilayah harus dikonfirmasi sebelum dipakai sebagai data Sumatera Barat.
- Untuk optimasi nyata, tetap diperlukan data stok batch, umur simpan, penjualan, kapasitas kendaraan, serta biaya angkut dari mitra.
