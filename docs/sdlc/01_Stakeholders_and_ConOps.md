# Stakeholders and Concept of Operations — Food Demand Intelligence

| Atribut | Nilai |
| --- | --- |
| Status | Siap Ditinjau Tim v0.2 |
| Tanggal | 3 November 2026 |
| Approver dokumen | Ismael |
| Horizon utama | Target pilot pasca-HackDay |
| Fase awal | MVP lokal untuk pitching/exhibition 28 November 2026 |

## 1. Tujuan ConOps

Dokumen ini menjelaskan siapa yang berkepentingan, bagaimana Food Demand Intelligence digunakan dalam operasi target, batas tanggung jawab manusia dan sistem, serta bagaimana kondisi gagal ditangani. ConOps menggambarkan target pilot agar kebutuhan produk tidak terbatas pada demonstrasi, tetapi membedakan dengan jelas fitur yang benar-benar tersedia pada MVP 24 jam.

## 2. Ringkasan operasi

Food Demand Intelligence membantu Analis Distribusi Pangan meninjau data pangan, melihat forecast harga harian dalam Rp/kg selama tujuh hari beserta label tekanan pasar turunannya, memeriksa estimasi kebutuhan baseline dan potensi surplus-defisit, lalu mencoba alokasi antardaerah. Sistem menyarankan jumlah distribusi dengan mempertimbangkan stok, kapasitas, anggaran, dan usia simpan.

Kebutuhan baseline diturunkan dari konsumsi dan populasi, bukan dari observasi permintaan harian aktual. Surplus-defisit yang ditampilkan MVP adalah estimasi/skenario sesuai data dan asumsi yang terlihat.

Neraca wilayah MVP dihitung sebagai `stok sintetis + estimasi pasokan - kebutuhan baseline`. Nilai positif disebut estimasi surplus dan nilai negatif disebut estimasi defisit.

Sistem tidak melakukan pengadaan, memesan kendaraan, mengirim barang, atau mengambil keputusan resmi. Pejabat penanggung jawab ketersediaan dan distribusi pangan tetap menilai rekomendasi serta menentukan tindakan di luar sistem.

## 3. Stakeholder

### 3.1 Internal

| Stakeholder | Kepentingan | Keterlibatan |
| --- | --- | --- |
| Ismael | Mutu ilmiah, keberhasilan program, dan arah strategis | Ketua tim dan penanggung jawab akhir |
| Yolanda Pagansa Putri | Kesesuaian dengan praktik operasional pangan | Penasihat domain dan penjajakan jejaring |
| Zaky Ramadhan | Sistem terintegrasi dan dapat didemonstrasikan | Koordinator teknis |
| Rafa Maritza Kardinal | Data, model prediksi, dan optimasi valid | AI & Data Engineer |
| Silvana Yulia Damara | Alur mudah dipahami dan sesuai kebutuhan pengguna | Validasi pengguna dan UI/UX |
| Yelsa Pagansa Putri | Nilai bisnis, pitching, dan peluang hilirisasi | Bisnis dan hilirisasi |

### 3.2 Eksternal atau kandidat

| Stakeholder | Peran target | Status saat ini |
| --- | --- | --- |
| Analis Distribusi Pangan tingkat provinsi | Operator utama | Persona target; belum ditetapkan sebagai pengguna resmi |
| Penanggung jawab ketersediaan dan distribusi pangan | Peninjau/pengambil keputusan | Persona target; tidak ada approver resmi untuk MVP |
| Dinas Pangan kabupaten/kota | Penyedia data dan pengguna pendukung | Kandidat stakeholder |
| Pengelola gudang, BUMD, atau agregator | Penyedia data stok dan logistik | Kandidat; belum menjadi mitra resmi |
| Panitia Hackathon Deeptech 2026 | Penilai prototipe dan MVP | Stakeholder program |

Kehadiran anggota tim yang bekerja di bidang pangan tidak berarti instansinya telah menjadi sponsor atau mitra resmi.

## 4. Batas sistem

### Sistem melakukan

- membaca dataset yang telah disiapkan;
- menampilkan provenance dan validitas data;
- menyajikan forecast harga harian dalam Rp/kg selama tujuh hari dan label tekanan pasar turunannya;
- menunjukkan potensi surplus-defisit;
- menerima parameter skenario anggaran dan kapasitas;
- menghitung rekomendasi alokasi dan prioritas FEFO; serta
- menampilkan ringkasan dampak rekomendasi.

### Manusia melakukan

- memastikan konteks dan periode data sesuai;
- menilai apakah asumsi skenario masuk akal;
- meninjau dan menafsirkan rekomendasi;
- menerima, menolak, atau meminta analisis ulang; serta
- menjalankan seluruh proses pengadaan dan distribusi di luar sistem.

## 5. Data dan tanggung jawab

| Data | Sumber target | Tanggung jawab target | Kondisi MVP |
| --- | --- | --- | --- |
| Harga, produksi, konsumsi, dan cuaca | Sumber publik seperti PIHPS, BPS, Bapanas, dan BMKG | Tim teknis menyiapkan dan mencatat provenance | Dataset publik yang telah disiapkan |
| Stok dan usia simpan | Dinas, gudang, BUMD, atau agregator | Pemilik operasional menyediakan dan memvalidasi | Data sintetis berlabel |
| Kapasitas dan biaya distribusi | Pengelola logistik/operasional | Pemilik operasional menyediakan dan memvalidasi | Data sintetis berlabel |

MVP tidak menggunakan data pribadi atau data rahasia mitra. Hasil dari data sintetis hanya layak untuk demonstrasi.

## 6. Ritme operasi target

- Analisis rutin dilakukan satu kali setiap minggu setelah data terbaru tersedia.
- Analisis tambahan dilakukan secara manual saat ada lonjakan harga, risiko defisit, atau stok mendekati kedaluwarsa.
- Penjadwalan dan notifikasi otomatis tidak termasuk MVP.

## 7. Skenario operasi normal target

1. Tim teknis atau pengelola data menyiapkan data publik yang telah dibersihkan.
2. Penyedia data operasional menyerahkan stok, usia simpan, kapasitas, dan biaya.
3. Analis Distribusi Pangan memeriksa periode, provenance, kelengkapan, dan asumsi data.
4. Sistem menampilkan forecast harga harian dalam Rp/kg selama tujuh hari, label tekanan pasar, kebutuhan baseline, dan potensi surplus-defisit.
5. Analis mengatur batas anggaran dan kapasitas untuk skenario yang ingin ditinjau.
6. Optimizer menghasilkan rekomendasi asal, tujuan, komoditas, jumlah, biaya, dan prioritas FEFO.
7. Sistem membandingkan kondisi sebelum dan sesudah rekomendasi.
8. Analis meninjau hasil dan menyampaikannya kepada pejabat penanggung jawab.
9. Pejabat menerima, menolak, atau meminta skenario ulang di luar workflow digital MVP.
10. Tindakan distribusi, bila ada, dilaksanakan melalui proses resmi di luar sistem.

Urutan tujuan optimizer adalah: mengurangi defisit sebanyak mungkin, memprioritaskan stok yang paling dekat kedaluwarsa, lalu menekan biaya distribusi. Semua tujuan tunduk pada batas stok, kapasitas, dan anggaran.

## 8. Skenario demo MVP

1. Presenter membuka dashboard lokal tanpa login.
2. Dataset demo untuk tiga komoditas dan lima wilayah sudah tersedia.
3. Sistem menampilkan forecast harga harian dalam Rp/kg selama tujuh hari, label tekanan pasar, serta tabel/visual estimasi surplus-defisit.
4. Presenter mengubah batas anggaran atau kapasitas.
5. Sistem menjalankan optimizer dan menampilkan rekomendasi feasible dalam kurang dari lima detik.
6. Presenter menunjukkan prioritas FEFO serta perbandingan sebelum-sesudah.
7. Dashboard menampilkan disclaimer bahwa rekomendasi harus ditinjau manusia dan berbasis sebagian data sintetis.

## 9. Kondisi gagal dan respons

| Kondisi | Respons sistem |
| --- | --- |
| Data penting hilang atau kedaluwarsa | Tampilkan peringatan dan jangan hasilkan rekomendasi final |
| Nilai input tidak valid | Tolak input sebelum optimizer berjalan |
| Model forecast gagal | Gunakan baseline sederhana dengan label yang jelas |
| Constraint tidak memiliki solusi | Tampilkan status tidak feasible dan constraint penyebabnya |
| Stok, biaya, atau kapasitas tidak tersedia | Jangan mengarang nilai; minta data atau gunakan skenario sintetis berlabel |

Kegagalan harus terlihat dan dapat dijelaskan. Sistem tidak boleh menampilkan hasil parsial seolah-olah rekomendasi tersebut valid.

## 10. Aturan FEFO MVP

- Semua komoditas diurutkan berdasarkan tanggal kedaluwarsa terdekat.
- Cabai merah keriting dan cabai rawit merah diberi label prioritas tinggi jika sisa usia simpannya kurang dari tiga hari.
- Bawang merah tetap mengikuti urutan FEFO tanpa ambang risiko hari yang belum tervalidasi.
- Tanggal kedaluwarsa pada demo berasal dari data sintetis dan ditampilkan sebagai asumsi.

## 11. Lingkungan operasi

### MVP HackDay

- dijalankan pada perangkat lokal tim;
- tidak memerlukan internet untuk alur utama;
- memakai data publik yang telah disiapkan dan data operasional sintetis;
- tidak menjanjikan availability setelah pitching; dan
- tidak digunakan untuk keputusan distribusi nyata.

### Target pilot

Target pilot mengasumsikan akses data operasional yang tervalidasi, pengguna dari instansi terkait, serta proses tinjauan keputusan yang disepakati. Asumsi tersebut belum terpenuhi dan bukan klaim kondisi saat ini.

## 12. Arah pengembangan di luar MVP

Unggah data, integrasi API, autentikasi dan peran, workflow persetujuan, ekspor, monitoring model, serta deployment produksi hanya dipertimbangkan setelah kebutuhan pilot dan mitra resmi tersedia.

## 13. Persetujuan

Seluruh anggota tim meninjau isi dokumen. Ismael sebagai Ketua Tim memberikan persetujuan akhir sebelum status dokumen diubah dari draft menjadi baseline.

