# Evidence Note: Pemilihan Model Forecast Harga untuk MVP

Tanggal: 4 November 2026  
Konteks: Food Demand Intelligence, tiga seri harga harian PIHPS, sekitar dua tahun observasi hari kerja, horizon tampilan tujuh hari kalender.

## Kesimpulan

Studi literatur ringkas diperlukan untuk membenarkan **cara membandingkan model**, bukan untuk memilih pemenang sebelum eksperimen. XGBoost layak menjadi kandidat, tetapi tidak boleh ditetapkan sebagai model utama hanya karena populer atau berhasil pada domain lain. Model utama harus menjadi model yang paling baik pada evaluasi *out-of-sample* berurutan di data proyek, dengan baseline sederhana tetap dipertahankan sebagai kandidat sah.

Kompetisi forecasting berskala besar menunjukkan tidak ada keluarga model yang selalu unggul. Pada M4, metode ML murni yang diajukan tidak mendominasi dan metode kombinasi berada di posisi teratas; pada M5, gradient-boosted trees sangat berhasil pada data penjualan yang kaya, berpola hierarkis, dan memiliki banyak seri serta variabel penjelas. Dua hasil tersebut mendukung benchmarking sesuai karakter data, bukan pemilihan berdasarkan reputasi algoritma. [M4 results](https://doi.org/10.1016/j.ijforecast.2019.04.014), [M5 Accuracy results](https://doi.org/10.1016/j.ijforecast.2021.11.013)

## Bukti yang relevan

1. **Urutan waktu harus dipertahankan.** Studi evaluasi empiris Cerqueira, Torgo, dan Mozetič menemukan bahwa pada seri dunia nyata dengan non-stasioneritas, estimasi performa paling akurat berasal dari metode *out-of-sample* yang mempertahankan urutan temporal. [Paper dan artefak eksperimen](https://github.com/vcerqueira/experiments-performance_estimation)
2. **Rolling origin lebih tepat daripada satu holdout.** Tashman menjelaskan bahwa reliabilitas pengujian *out-of-sample* dapat ditingkatkan dengan rolling-origin, kalibrasi ulang, dan beberapa periode uji. [Original research article](https://doi.org/10.1016/S0169-2070(00)00065-0)
3. **Panjang data memengaruhi posisi ML.** Eksperimen Cerqueira, Torgo, dan Soares menunjukkan performa relatif ML membaik seiring bertambahnya sampel dan tidak ada ambang universal yang menjamin ML unggul. Ini memperkuat kebutuhan membandingkan XGBoost dengan metode sederhana pada panjang data aktual. [Paper](https://arxiv.org/abs/1909.13316), [kode eksperimen penulis](https://github.com/vcerqueira/experiments-sizematters)
4. **Gradient boosting tetap berisiko leakage dan overfit pada time series.** Paper solusi pemenang M5 Uncertainty membahas kekuatan gradient-boosted trees sekaligus risiko overfitting, leakage, dan kegagalan generalisasi pada target non-stasioner. [Original research article](https://doi.org/10.1016/j.ijforecast.2021.12.003)
5. **Paper algoritma bukan bukti kesesuaian domain.** Paper XGBoost dan LightGBM membuktikan desain serta efisiensi sistem boosting, tetapi tidak membuktikan keduanya paling akurat untuk seri harga pangan proyek ini. [XGBoost paper](https://doi.org/10.1145/2939672.2939785), [LightGBM paper](https://proceedings.neurips.cc/paper_files/paper/2017/hash/6449f44a102fde848669bdd9eb6b76fa-Abstract.html)
6. **Split temporal mencegah pelatihan pada masa depan.** Dokumentasi resmi `TimeSeriesSplit` menjelaskan bahwa split berurutan digunakan ketika split biasa akan melatih pada masa depan dan mengevaluasi pada masa lalu. [scikit-learn documentation](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html)

## Protokol seleksi yang disarankan

### 1. Data gate

- Verifikasi cakupan wilayah ekspor PIHPS sebelum membuat klaim Sumatera Barat.
- Jika belum terverifikasi, hasil hanya boleh diberi status demo dengan label `cakupan wilayah belum terverifikasi`.
- Evaluasi hanya menggunakan harga yang benar-benar terobservasi. Nilai akhir pekan hasil carry-forward tidak masuk perhitungan metrik.

### 2. Kandidat minimum

Bandingkan per komoditas:

1. **Naive:** harga observasi terakhir.
2. **Moving average:** rata-rata lima observasi hari kerja terakhir.
3. **XGBoost regression:** fitur lag, rolling statistics, dan kalender yang hanya dibentuk dari informasi yang tersedia sebelum titik forecast.

XGBoost adalah kandidat utama ML, bukan pemenang awal. LightGBM dan deep learning tidak perlu ditambahkan pada MVP kecuali tiga kandidat di atas sudah selesai dan teruji.

### 3. Evaluasi

- Gunakan expanding-window rolling-origin dengan beberapa origin pada bagian akhir seri.
- Setiap fold mengevaluasi horizon yang sama; evaluasi hanya pada hari dengan observasi PIHPS.
- Tuning hanya boleh memakai bagian training pada setiap origin; test fold tidak boleh memengaruhi fitur, imputasi, atau hyperparameter.
- Laporkan metrik per fold dan agregat, bukan satu angka tanpa variasi.
- Gunakan WAPE sebagai metrik utama agar selaras dengan proposal, MAE dalam Rp/kg sebagai metrik yang mudah dijelaskan, dan improvement terhadap naive sebagai pembanding.

### 4. Aturan pemilihan

- Pilih model dengan WAPE rolling-origin terendah yang performanya tidak bergantung pada satu fold saja.
- Gunakan XGBoost hanya jika peningkatannya terhadap baseline konsisten dan cukup material; target aspiratif proposal adalah 15%, bukan hasil yang boleh diasumsikan.
- Jika XGBoost tidak menang konsisten, gunakan baseline terbaik sebagai model MVP dan laporkan hasil secara jujur.
- Bekukan random seed, konfigurasi, versi dataset, dan artefak forecast untuk demo.

## Cuaca bulanan

Data BMKG yang tersedia bulanan (November 2024–September 2026) sebaiknya tidak menjadi fitur model harian MVP. Ini adalah inferensi proyek: seri cuaca memiliki granularitas jauh lebih kasar, hanya sekitar dua lusin titik bulanan, dan tidak memberi variasi harian yang sepadan dengan target. Mengulang nilai bulanan ke setiap hari dapat memberi kesan jumlah sampel yang lebih besar tanpa menambah informasi temporal baru.

Cuaca tetap dicatat sebagai sumber potensial. Ia baru layak diuji setelah tersedia data harian yang sejajar berdasarkan tanggal dan stasiun, serta nilainya tersedia pada saat forecast dibuat.

## Keputusan yang direkomendasikan untuk spesifikasi

- Lakukan literature review terbatas ini; tidak perlu systematic literature review untuk MVP 24 jam.
- Tetapkan protokol benchmark, bukan XGBoost, sebagai keputusan metodologis utama.
- Tulis XGBoost sebagai **candidate model** sampai hasil rolling-origin tersedia.
- Jadikan baseline sebagai fallback runtime dan kandidat pemenang yang sah.

## Tindak lanjut artikel domain

**PIC:** pengguna/tim Food Demand Intelligence  
**Status:** belum dilakukan; ingatkan kembali sebelum `../sdlc/04_Data_and_AI_Specification.md` dinaikkan menjadi baseline.

Cari artikel ilmiah primer yang membahas forecast harga komoditas hortikultura, evaluasi time-series, dan integrasi forecast dengan optimasi distribusi. Artikel dipakai untuk memperkuat feature rationale, kandidat model, metrik, serta batas klaim; model pemenang tetap ditentukan melalui benchmark data proyek.

Kueri pencarian yang disarankan:

- `daily agricultural commodity price forecasting XGBoost rolling origin evaluation`
- `food price forecasting gradient boosting versus ARIMA naive baseline`
- `horticultural commodity price forecasting machine learning Indonesia`
- `chili price forecasting Indonesia XGBoost`
- `shallot price forecasting Indonesia machine learning`
- `cabai forecasting harga machine learning time series`
- `bawang merah peramalan harga XGBoost ARIMA`
- `rolling origin cross validation commodity price forecasting`
- `weather variables agricultural price forecasting daily data`
- `predictive prescriptive analytics food supply chain optimization`
- `perishable food distribution FEFO linear programming`
- `surplus deficit food distribution optimization linear programming`
