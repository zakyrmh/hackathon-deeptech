# Data and AI Specification — Food Demand Intelligence

| Atribut | Nilai |
| --- | --- |
| Status | Siap Ditinjau Tim v0.2 |
| Tanggal | 4 November 2026 |
| Fase | MVP HackDay 24 jam |
| Approver | Ismael |
| Referensi | `02_PRD.md`, `03_SRS.md`, `../data/DATASET_GUIDE.md`, `../../data/MANIFEST.csv`, `../research/model_selection_price_forecast.md` |

## 1. Tujuan

Dokumen ini menetapkan sumber, transformasi, quality gate, metode benchmark, artefak, dan batas klaim data/AI. MVP mem-forecast harga harian Rp/kg selama tujuh hari, menghitung kebutuhan dan pasokan baseline tujuh hari, lalu menghasilkan `runtime_bundle.json` untuk dashboard dan optimizer.

Model tidak memprediksi permintaan harian aktual. Data operasional stok, usia simpan, rute, kapasitas, dan biaya bersifat sintetis.

## 2. Inventaris sumber

| Data | Sumber/periode | Penggunaan MVP | Status/gotcha |
| --- | --- | --- | --- |
| Produksi hortikultura | BPS Sumbar 2024 | Estimasi pasokan struktural | Tahunan; bukan stok atau panen mingguan aktual |
| Konsumsi | BPS Sumbar 2025 | Kebutuhan baseline | Rata-rata kg/kapita/minggu; bukan transaksi harian |
| Populasi | BPS Sumbar 2025 | Pengali kebutuhan baseline | Terdapat selisih pembulatan 100 orang pada total publikasi |
| Harga | PIHPS, 25 Okt 2024–2 Nov 2026 | Training dan evaluasi forecast | Filter wilayah tidak tertanam di XLSX dan belum terverifikasi |
| Iklim | BMKG bulanan, Nov 2024–Sep 2026 | Dokumentasi sumber potensial | Tidak digunakan pada model harian MVP |
| Operasional | Sintetis | Optimizer dan demo FEFO | Bukan data mitra atau kondisi nyata |

Detail provenance, URL, checksum, metode akuisisi, dan status original download tetap mengacu pada `data/MANIFEST.csv` serta `data/CHECKSUMS.sha256`.

## 3. Aturan kelayakan klaim

- Data PIHPS hanya boleh mendukung klaim forecast Sumatera Barat setelah cakupan wilayah diverifikasi atau data diekspor ulang dengan bukti filter.
- Sebelum verifikasi, seluruh hasil harga harus menampilkan label `cakupan wilayah belum terverifikasi`.
- Hasil dari data operasional sintetis hanya boleh disebut skenario demo.
- Estimasi pasokan mingguan dari produksi tahunan tidak boleh disebut stok atau jadwal panen aktual.
- Estimasi kebutuhan tidak boleh disebut permintaan transaksi harian.

## 4. Pembagian fungsi data

| Kelompok | Fungsi |
| --- | --- |
| PIHPS | Forecast harga dan label tekanan pasar |
| Produksi, konsumsi, populasi BPS | Kebutuhan baseline dan estimasi pasokan struktural |
| Data operasional sintetis | Stok batch, expiry, rute, biaya, kapasitas, dan skenario optimizer |
| BMKG bulanan | Tidak digunakan pada model MVP; kandidat riset setelah tersedia data harian yang sejajar |

## 5. Entitas data kanonik

### 5.1 PriceObservation

| Field | Tipe/aturan |
| --- | --- |
| `date` | Tanggal `Asia/Jakarta`, unik per komoditas |
| `commodity` | `bawang_merah`, `cabai_merah_keriting`, atau `cabai_rawit_merah` |
| `price_rp_per_kg` | Angka positif |
| `source` | Identitas sumber PIHPS |
| `coverage_status` | `verified` atau `unverified` |
| `is_observed` | `true` hanya untuk nilai PIHPS aktual |
| `is_imputed` | `true` untuk nilai akhir pekan hasil carry-forward |

### 5.2 RegionBaseline

| Field | Tipe/aturan |
| --- | --- |
| `region_code` | Kode BPS empat digit |
| `region_name` | Nama kanonik wilayah |
| `commodity` | Komoditas kanonik |
| `population_people` | Populasi 2025 |
| `consumption_kg_capita_week` | Konsumsi BPS 2025 |
| `production_kg_year` | Produksi BPS 2024 |
| `baseline_need_kg_7d` | Konsumsi × populasi |
| `estimated_supply_kg_7d` | Produksi tahunan ÷ 52 |

### 5.3 InventoryBatch sintetis

| Field | Tipe/aturan |
| --- | --- |
| `batch_id` | ID unik dan stabil |
| `region_code` | Salah satu dari lima wilayah pilot |
| `commodity` | Komoditas kanonik |
| `quantity_kg` | Bilangan positif |
| `expiry_date` | Tanggal sintetis setelah snapshot |
| `is_synthetic` | Selalu `true` pada MVP |

### 5.4 Route sintetis

| Field | Tipe/aturan |
| --- | --- |
| `origin_code` / `destination_code` | Berbeda dan termasuk wilayah pilot |
| `commodity` | Komoditas yang diizinkan pada rute |
| `cost_rp_per_kg` | Bilangan positif |
| `max_capacity_kg` | Bilangan positif |
| `is_synthetic` | Selalu `true` |

### 5.5 ForecastPoint

| Field | Tipe/aturan |
| --- | --- |
| `date` | Satu dari tujuh hari kalender setelah observasi terakhir |
| `price_rp_per_kg` | Forecast harga |
| `is_imputed` | `true` pada akhir pekan hasil carry-forward |
| `model_id` | Identitas model/baseline pemenang |

## 6. Transformasi baseline tujuh hari

```text
baseline_need_kg_7d = consumption_kg_capita_week × population_people
estimated_supply_kg_7d = production_kg_year ÷ 52
balance_kg_7d = synthetic_stock_kg + estimated_supply_kg_7d - baseline_need_kg_7d
```

Nilai `balance_kg_7d > 0` adalah estimasi surplus dan nilai `< 0` adalah estimasi defisit. Pembagian produksi tahunan dengan 52 adalah asumsi tanpa musim panen dan harus terlihat dalam metadata runtime.

## 7. Pipeline data dan AI

1. Verifikasi checksum dan manifest raw.
2. Parse format angka/tanggal sumber tanpa mengubah file raw.
3. Normalisasi kode wilayah, komoditas, satuan kg, dan zona waktu.
4. Jalankan quality gate dan hasilkan laporan validasi.
5. Bentuk baseline BPS tujuh hari untuk lima wilayah pilot.
6. Bentuk seri harga per komoditas dan tandai observasi versus imputasi.
7. Bangun fitur time-series tanpa memakai informasi masa depan.
8. Jalankan benchmark rolling-origin untuk tiga kandidat.
9. Pilih pemenang sesuai aturan seleksi dan buat forecast tujuh hari.
10. Gabungkan forecast, baseline, dan data operasional sintetis.
11. Validasi lalu tulis satu `runtime_bundle.json` secara atomik.

Folder `data/raw/` tidak ditulis ulang. Seluruh hasil turunan harus dapat dibuat ulang oleh pipeline.

## 8. Quality gate

### 8.1 Harga

- tanggal dapat diparse dan unik per komoditas;
- harga aktual lebih besar dari nol;
- urutan waktu monoton;
- observasi dan imputasi dapat dibedakan;
- XGBoost hanya eligible jika tersedia minimal 250 observasi hari kerja valid dan missing rate hari kerja maksimal 10%; dan
- jika gate XGBoost gagal, gunakan baseline terbaik dengan label fallback.

### 8.2 BPS

- terdapat 19 wilayah dan 57 kombinasi wilayah-komoditas pada hasil normalisasi penuh;
- tiga komoditas tersedia untuk lima wilayah pilot;
- konversi kuintal ke kg menggunakan faktor 100;
- total produksi per komoditas harus cocok dengan kontrol pada `data/README.md`; dan
- nilai sumber `-` dinormalisasi menjadi nol serta dicatat sebagai transformasi.

### 8.3 Runtime bundle

- schema valid;
- versi, hash input, waktu pembuatan, periode, sumber, dan asumsi tersedia;
- tiga komoditas dan lima wilayah pilot tersedia;
- semua data sintetis ditandai;
- seluruh rute merujuk wilayah/komoditas yang valid; dan
- minimal tersedia skenario `recommendations_available`, `no_intervention_needed`, dan `constraints_block_intervention`.

Jika gate wajib gagal, pipeline tidak boleh menerbitkan bundle baru.

## 9. Kandidat model

Benchmark dilakukan terpisah per komoditas:

1. `naive_last_value` — harga observasi terakhir;
2. `moving_average_5` — rata-rata lima observasi hari kerja terakhir; dan
3. `xgboost_regressor` — gradient-boosted trees dengan fitur time-series.

XGBoost adalah kandidat, bukan pemenang awal. LightGBM dan deep learning tidak masuk MVP.

## 10. Fitur XGBoost

- lag harga pada 1, 2, 5, dan 10 observasi hari kerja;
- rolling mean pada 5, 10, dan 20 observasi;
- rolling standard deviation pada 5, 10, dan 20 observasi;
- hari dalam minggu; dan
- bulan.

Setiap fitur pada tanggal target hanya boleh memakai data sebelum tanggal tersebut. Transformasi dan tuning hanya boleh belajar dari bagian training pada fold terkait.

## 11. Evaluasi

- Metode: expanding-window rolling-origin.
- Minimum data awal: 12 bulan.
- Fold: delapan origin terbaru yang tidak tumpang tindih.
- Horizon fold: lima observasi hari kerja.
- Metrik utama: WAPE.
- Metrik pendamping: MAE dalam Rp/kg dan improvement terhadap naive.
- Evaluasi hanya menggunakan harga yang benar-benar terobservasi; nilai akhir pekan hasil carry-forward dikeluarkan.
- Laporkan metrik per fold, rata-rata, dan variasi; jangan hanya satu skor agregat.

## 12. Aturan pemilihan model

XGBoost dipilih hanya jika:

1. WAPE rata-ratanya lebih rendah dari naive dan moving average; dan
2. menang setidaknya pada lima dari delapan fold.

Jika tidak, baseline dengan WAPE rata-rata terbaik menjadi model runtime. Target improvement 15% merupakan sasaran proposal, bukan syarat penerimaan MVP.

## 13. Forecast tujuh hari

- Model menghasilkan prediksi untuk observasi hari kerja.
- Sabtu/Minggu menggunakan nilai hari kerja terakhir dan diberi `is_imputed=true`.
- Horizon runtime tetap tujuh hari kalender berturut-turut.
- Label tekanan pasar mengikuti BR-001 pada SRS.
- Forecast runtime dibekukan sebelum demo dan tidak dihitung ulang melalui dashboard.

## 14. Reproduksibilitas dan artefak

Setiap eksperimen/final run menyimpan:

- versi dan hash dataset;
- konfigurasi fitur;
- parameter kandidat;
- random seed `42`;
- definisi fold;
- metrik per fold dan agregat;
- model pemenang serta alasan pemilihan;
- forecast runtime; dan
- versi software/dependency lock.

Artefak final disimpan di `artifacts/`; bundle konsumsi aplikasi disimpan di `data/runtime/runtime_bundle.json`.

## 15. Data sintetis

Data operasional dibuat sekali dengan seed/config tetap dan tidak diacak saat aplikasi berjalan. Skenario harus memuat batch stok, tanggal kedaluwarsa, rute, biaya Rp/kg, dan kapasitas. Nilainya harus ditinjau Yolanda untuk kewajaran demonstrasi dan divalidasi Rafa/Zaky terhadap constraint solver.

## 16. Responsible AI dan batas penggunaan

- Tampilkan sumber, cakupan wilayah, periode, model, metrik, serta fallback.
- Bedakan observasi, imputasi, estimasi, dan data sintetis.
- Jangan mengklaim hubungan kausal antara forecast harga dan defisit.
- Jangan gunakan hasil sebagai instruksi distribusi resmi.
- Jangan menyembunyikan baseline jika baseline mengalahkan XGBoost.
- Jangan memakai data pribadi atau rahasia mitra.

## 17. Tindak lanjut riset artikel

Artikel domain tambahan masih perlu dicari sebelum dokumen menjadi baseline. Keyword dan sumber awal tercatat di `../research/model_selection_price_forecast.md`. Artikel digunakan untuk justifikasi fitur, kandidat, evaluasi, dan batas klaim; hasil benchmark proyek tetap menentukan model utama.

## 18. Acceptance criteria

- Pipeline dapat membangun ulang seluruh output dari raw yang tercatat.
- Quality gate gagal secara eksplisit pada input invalid.
- Benchmark ketiga kandidat menghasilkan metrik delapan fold per komoditas.
- Pemilihan model dapat dijelaskan dari bukti metrik.
- Weekend imputation tidak masuk metrik evaluasi.
- `runtime_bundle.json` lolos schema validation dan memuat metadata wajib.
- Tidak ada klaim Sumatera Barat sebelum coverage PIHPS terverifikasi.

## 19. Persetujuan

Rafa bertanggung jawab atas isi teknis data/AI, Yolanda dikonsultasikan untuk kewajaran domain, Zaky meninjau kontrak runtime/integrasi, dan Ismael memberikan persetujuan akhir.
