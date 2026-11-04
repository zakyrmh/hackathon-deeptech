# Model Card and Evaluation Report — Food Demand Intelligence

| Atribut | Nilai |
| --- | --- |
| Status | Siap Ditinjau Tim v0.2 — benchmark belum dijalankan |
| Tanggal | 4 November 2026 |
| Model/data owner | Rafa |
| Reviewer domain | Yolanda |
| Integration reviewer | Zaky |
| Approver | Ismael |

## 1. Ringkasan

Artefak AI MVP memprediksi harga harian Rp/kg untuk tiga komoditas selama tujuh hari kalender. Model dipilih per komoditas dari naive-last-value, moving average lima hari kerja, dan XGBoost melalui evaluasi rolling-origin. Model card ini juga mencatat bahwa rekomendasi distribusi berasal dari optimizer deterministik SciPy HiGHS, bukan dari model generatif.

Per 4 November 2026, benchmark belum dijalankan dan tidak ada model pemenang atau angka WAPE/MAE yang sah. Tabel hasil sengaja berstatus `Pending`.

## 2. Identitas artefak

| Field | Nilai |
| --- | --- |
| Nama sistem | Food Demand Intelligence |
| Task model | Univariate/tabular price forecasting per komoditas |
| Komoditas | bawang merah; cabai merah keriting; cabai rawit merah |
| Horizon evaluasi | 5 hari kerja terobservasi |
| Horizon tampilan | 7 hari kalender |
| Runtime AI | forecast dibentuk offline dan disimpan dalam bundle |
| Runtime optimizer | linear programming deterministik saat pengguna menjalankan skenario |
| Seed | 42 |
| Lisensi/dependency | mengikuti manifest/lockfile final; pending |

## 3. Intended use

- Mendukung demo eksplorasi perubahan harga dan skenario alokasi lima wilayah pilot.
- Membandingkan kandidat model secara transparan dan memakai baseline jika lebih baik.
- Menjadi bahan tinjauan manusia untuk pitching/prototype, bukan keputusan resmi.

Out of scope:

- prediksi permintaan harian aktual;
- peringatan harga resmi atau rekomendasi kebijakan otomatis;
- trading, pengadaan, atau pengiriman otomatis;
- generalisasi nasional/produksi tanpa validasi baru;
- causal inference, estimasi dampak kebijakan, atau jaminan ketersediaan pangan;
- penggunaan data pribadi/rahasia.

## 4. Data

| Dataset | Fungsi | Status/batas |
| --- | --- | --- |
| PIHPS harga harian XLSX | target historis forecast | cakupan wilayah belum terverifikasi; klaim Sumbar ditahan |
| BPS produksi 2024 | estimasi pasokan mingguan | tahunan/52, non-seasonal assumption |
| BPS konsumsi 2025 | kebutuhan per kapita mingguan | bukan observasi permintaan transaksi |
| BPS populasi 2025 | skala kebutuhan wilayah | periode harus terlihat |
| Data operasional sintetis | stok, batch, expiry, route, cost, capacity | bukan data aktual; seed/config tetap |

BMKG bulanan tidak digunakan sebagai feature forecast harian MVP karena granularitas dan alignment belum memadai.

Data manifest harus merekam sumber, URL/referensi, tanggal unduh, periode, checksum, license/terms bila tersedia, coverage, dan status verifikasi. Tidak ada data pribadi atau rahasia mitra.

## 5. Preprocessing dan quality gate

- Normalisasi nama komoditas, tanggal, satuan Rp/kg, wilayah, dan missing value.
- Deduplikasi key harga; urut waktu; pemeriksaan nilai finite/nonnegatif dan outlier terdokumentasi.
- Train/evaluation hanya pada observasi hari kerja valid.
- XGBoost eligible bila minimal 250 observasi hari kerja valid dan missing rate hari kerja ≤10%.
- Transformasi/feature pada tiap fold hanya boleh memakai data sebelum origin untuk mencegah leakage.
- Jika quality gate gagal, kandidat XGBoost dikeluarkan dan baseline terbaik dipakai serta dilabeli.

## 6. Kandidat model

### 6.1 Naive last value

Prediksi seluruh horizon memakai harga hari kerja valid terakhir. Baseline sederhana dan kuat untuk series yang persisten.

### 6.2 Moving average 5 hari kerja

Prediksi memakai rata-rata lima observasi hari kerja terakhir sesuai implementasi recursive/direct yang dibekukan sebelum benchmark. Detail ini wajib tercatat dalam artifact config.

### 6.3 XGBoost regressor

Feature yang diizinkan:

- lag 1, 2, 5, dan 10 observasi;
- rolling mean 5, 10, dan 20 observasi;
- rolling standard deviation 5, 10, dan 20 observasi;
- day-of-week dan month.

Hyperparameter search harus kecil dan dibekukan agar realistis untuk hackathon. Parameter final, versi library, seed, dan runtime dicatat; XGBoost adalah kandidat, bukan pemenang default.

## 7. Evaluation protocol

- Expanding-window rolling-origin.
- Initial training window: 12 bulan.
- Delapan fold terbaru yang tidak overlap.
- Horizon tiap fold: lima hari kerja terobservasi.
- Metrik utama: WAPE.
- Metrik sekunder: MAE Rp/kg dan improvement terhadap naive.
- Weekend carry-forward tidak dimasukkan ke metrik.
- Evaluasi dilakukan terpisah per komoditas.

Formula:

`WAPE = sum(|y - y_hat|) / sum(|y|) × 100%`.

`MAE = mean(|y - y_hat|)`.

Fold dengan denominator WAPE nol harus ditandai dan ditangani eksplisit, bukan disamarkan. Harga yang valid diharapkan positif, tetapi guard tetap diperlukan.

## 8. Selection rule

XGBoost dipilih hanya bila:

1. lolos eligibility data;
2. mean WAPE lebih rendah daripada naive dan moving average; dan
3. menang minimal lima dari delapan fold.

Jika tidak, baseline dengan mean WAPE terendah dipilih. Tie ditentukan secara deterministik dengan memilih model yang lebih sederhana, lalu MAE yang lebih rendah jika masih diperlukan. Sasaran improvement 15% pada proposal adalah aspirasi, bukan syarat penerimaan.

## 9. Hasil benchmark

### 9.1 Ringkasan per komoditas

| Komoditas | Eligibility XGBoost | Naive WAPE/MAE | MA5 WAPE/MAE | XGBoost WAPE/MAE | Win folds XGB | Model terpilih | Alasan |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Bawang merah | Pending | Pending | Pending | Pending | Pending | Not evaluated | Benchmark belum dijalankan |
| Cabai merah keriting | Pending | Pending | Pending | Pending | Pending | Not evaluated | Benchmark belum dijalankan |
| Cabai rawit merah | Pending | Pending | Pending | Pending | Pending | Not evaluated | Benchmark belum dijalankan |

### 9.2 Detail fold

Detail tanggal train/test, jumlah observasi, missing rate, WAPE, MAE, runtime, dan error per fold disimpan dalam `artifacts/` dan ditautkan ke versi dokumen setelah eksekusi. Tidak ada nilai yang diisi dari perkiraan manual.

### 9.3 Status penerimaan

`Not evaluated`. Dokumen ini belum dapat menyatakan model memenuhi akurasi tertentu. Forecast runtime tidak boleh dipakai untuk pitch sebagai hasil tervalidasi sebelum §9 terisi dari pipeline yang dapat direproduksi.

## 10. Forecast calendar handling

Setelah model terpilih menghasilkan prediksi hari kerja, sistem membentuk tujuh tanggal kalender sesudah observasi terakhir. Sabtu/Minggu membawa nilai prediksi hari kerja terakhir dan `is_imputed=true`. Nilai imputasi harus terlihat sebagai asumsi dan tidak dianggap observasi/model output baru dalam evaluasi.

## 11. Optimizer evaluation

Optimizer bukan model ML. Evaluasinya melalui golden tests dan invariant:

- seluruh constraint stok, surplus/defisit, budget, capacity, route, dan FEFO terpenuhi;
- urutan tujuan: kurangi defisit, expiry terdekat, biaya lebih rendah;
- input/bundle identik menghasilkan hasil dan order identik;
- tiga reason scenario berfungsi;
- post-validation tidak menemukan pelanggaran di luar toleransi;
- hasil/timeout maksimal lima detik pada laptop demo.

Status saat ini: `Not tested`; evidence akan dicatat dalam dokumen 08.

## 12. Limitations dan risiko

- Cakupan wilayah harga PIHPS belum terbukti mewakili Sumatera Barat.
- Harga historis saja tidak menangkap cuaca, hari besar, gangguan distribusi, atau kebijakan secara kausal.
- Data produksi tahunan dibagi 52 dan mengabaikan musim/panen.
- Konsumsi/populasi adalah baseline agregat, bukan demand real-time.
- Lima wilayah dan tiga komoditas tidak mendukung generalisasi luas.
- Data operasi sintetis dapat menghasilkan rekomendasi yang realistis secara matematis tetapi tidak faktual secara operasional.
- Delapan fold memberi evidence terbatas; regime shift dapat menurunkan performa.
- WAPE agregat dapat menyembunyikan error besar pada tanggal tertentu.
- Akurasi harga tidak otomatis berarti rekomendasi distribusi tepat di lapangan.

## 13. Responsible AI dan safeguards

- Human review wajib; sistem tidak mengeksekusi keputusan.
- Label synthetic, sumber, periode, cakupan, asumsi, dan limitation selalu terlihat.
- Baseline tidak disembunyikan ketika mengalahkan XGBoost.
- Tidak memakai PII, data rahasia, atau model generatif untuk mencipta angka yang hilang.
- Klaim pitch harus mengikuti evidence hasil, bukan target proposal.
- Validasi domain Yolanda diperlukan untuk kewajaran scenario; approval final Ismael.

## 14. Reproducibility dan provenance

Setiap run benchmark menyimpan:

- commit dan versi pipeline;
- input manifest/checksum dan processed-data hash;
- filter/quality report;
- fold definition dan timestamp Asia/Jakarta;
- feature list, parameter, seed 42, dependency lock;
- metric per fold dan agregat;
- selected model serta machine-readable selection reason;
- serialized model/forecast bila diperlukan;
- runtime dan environment;
- `runtime_bundle.json` version/hash yang dihasilkan.

Pipeline menulis bundle secara atomik setelah seluruh validasi lulus.

## 15. Monitoring dan update

Untuk MVP offline, monitoring berarti pemeriksaan sebelum release: data freshness, schema/hash, missing/outlier, benchmark, dan smoke. Tidak ada live drift monitoring. Pada pilot, pertimbangkan monitoring error aktual vs forecast, drift distribusi, coverage, data freshness, override pengguna, dan audit keputusan—setelah data aktual dan governance tersedia.

Pemicu retrain/re-evaluate:

- data baru atau koreksi sumber;
- perubahan definisi komoditas/wilayah;
- quality gate gagal;
- error meningkat terhadap baseline;
- perubahan metode feature/model;
- kebutuhan penggunaan di luar demo.

## 16. Riset yang masih perlu dilakukan

Artikel primer tetap diperlukan untuk menguatkan pilihan model dan asumsi domain. Kata kunci pencarian:

- `food commodity price forecasting rolling origin evaluation`;
- `chili price forecasting Indonesia XGBoost`;
- `shallot price forecasting Indonesia machine learning`;
- `agricultural price forecasting naive baseline WAPE MAE`;
- `perishable food distribution optimization FEFO linear programming`;
- `food redistribution surplus deficit optimization Indonesia`.

Prioritaskan jurnal/proceeding primer, metode dan dataset yang jelas, split temporal, baseline sederhana, serta konteks Indonesia/komoditas sejenis. Catat DOI, data, horizon, leakage risk, metrik, dan relevansi—jangan memilih model hanya karena satu artikel melaporkan skor tinggi.

## 17. Checklist sebelum sign-off

- [ ] Cakupan PIHPS diverifikasi atau limitation final disetujui.
- [ ] Quality gate dan delapan fold dijalankan per komoditas.
- [ ] Tabel §9 terisi otomatis dari artifact, bukan manual.
- [ ] Selection rule dapat direproduksi.
- [ ] Runtime bundle/hash sesuai model report.
- [ ] Golden test optimizer dan performa lulus.
- [ ] Yolanda meninjau kewajaran domain.
- [ ] Zaky meninjau kontrak integrasi.
- [ ] Ismael menyetujui klaim final.

## 18. Persetujuan

Model card baru dapat diberi status hasil final setelah benchmark/evaluation evidence tersedia. Jika baseline menang atau XGBoost tidak eligible, hasil tersebut tetap sah dan harus dilaporkan apa adanya.

