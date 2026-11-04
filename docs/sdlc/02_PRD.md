# Product Requirements Document — Food Demand Intelligence

| Atribut | Nilai |
| --- | --- |
| Status | Siap Ditinjau Tim v0.2 |
| Tanggal | 3 November 2026 |
| Fase | MVP HackDay 24 jam |
| Pemilik inisiatif | Tim Food Demand Intelligence |
| Approver | Ismael |
| Referensi | `00_Project_Charter.md`, `01_Stakeholders_and_ConOps.md`, `../../CONTEXT.md` |

## 1. Ringkasan produk

Food Demand Intelligence adalah dashboard *decision support* yang membantu Analis Distribusi Pangan memahami tekanan harga, mengidentifikasi estimasi surplus-defisit, dan mencoba skenario alokasi antardaerah. Dalam maksimal lima menit, pengguna harus dapat menentukan:

- komoditas dan wilayah yang memerlukan intervensi;
- wilayah sumber pasokan;
- jumlah alokasi yang direkomendasikan; dan
- estimasi biaya distribusi.

Rekomendasi harus ditinjau manusia. Sistem tidak mengeksekusi pengadaan atau pengiriman.

## 2. Masalah pengguna

Data harga, produksi, konsumsi, stok, usia simpan, kapasitas, dan biaya tersebar di sumber yang berbeda. Pengguna harus menggabungkan konteks tersebut untuk menilai risiko dan merancang intervensi. Kondisi ini membuat proses lambat, sulit dibandingkan, dan rentan mengabaikan stok yang mendekati kedaluwarsa.

MVP tidak mengklaim menyelesaikan integrasi data produksi. MVP membuktikan bahwa satu alur keputusan dapat disajikan secara terpadu dengan data publik yang telah disiapkan dan data operasional sintetis.

## 3. Outcome dan prioritas nilai

Urutan nilai produk adalah:

1. mendeteksi risiko tekanan harga atau defisit lebih awal;
2. mengurangi estimasi defisit melalui rekomendasi alokasi;
3. mengurangi risiko susut melalui FEFO; dan
4. menekan estimasi biaya distribusi.

## 4. Persona

### Persona aktif: Analis Distribusi Pangan

Analis menjalankan dashboard, memeriksa konteks data, memilih komoditas, meninjau forecast dan neraca wilayah, mengatur skenario, serta membaca rekomendasi.

### Stakeholder nonaktif di dalam MVP

Pejabat penanggung jawab ketersediaan dan distribusi pangan menerima ringkasan dari analis dan menentukan tindak lanjut di luar sistem. MVP tidak menyediakan akun, layar, atau workflow persetujuan untuk pejabat tersebut.

## 5. Prinsip produk

- **Satu alur:** seluruh demo inti tersedia dalam satu halaman dashboard.
- **Transparan:** data aktual, olahan, dan sintetis dapat dibedakan dengan jelas.
- **Human-in-the-loop:** rekomendasi tidak dipresentasikan sebagai keputusan resmi.
- **Fail visibly:** data atau skenario yang tidak valid tidak menghasilkan rekomendasi yang tampak sah.
- **Demo lokal:** alur inti tidak bergantung pada internet atau layanan cloud.
- **Scope 24 jam:** fitur yang tidak mendukung alur keputusan utama ditunda.

## 6. Scope dan prioritas

### 6.1 Must have — P0

1. Dashboard satu halaman tanpa login.
2. Data demo untuk tiga komoditas dan lima wilayah pilot.
3. Pemilihan komoditas.
4. Forecast harga harian Rp/kg selama tujuh hari.
5. Label tekanan pasar berdasarkan perubahan forecast hari ke-7 terhadap harga aktual terakhir.
6. Tabel/kartu estimasi surplus-defisit.
7. Input total anggaran dan total kapasitas angkut.
8. Tombol `Jalankan Skenario`.
9. Rekomendasi alokasi yang feasible dan berurutan.
10. Ringkasan sebelum dan sesudah optimasi.
11. Provenance, periode, pembaruan terakhir, asumsi, dan label data sintetis yang selalu terlihat.
12. Kondisi kosong, tidak valid, model gagal, dan skenario tidak feasible yang dapat dijelaskan.
13. Tampilan responsif dari lebar 360px hingga desktop.

### 6.2 Stretch goal

- peta sederhana Sumatera Barat jika alur P0 telah stabil.

### 6.3 Won't have pada MVP

- login, RBAC, atau persetujuan digital;
- unggah data dan integrasi API;
- penyimpanan serta riwayat skenario;
- retraining atau data real-time;
- GIS kompleks atau rute jalan;
- ekspor laporan;
- transaksi, pembayaran, pengadaan, armada, GPS, ERP, atau IoT;
- multi-tenant, billing, dan deployment produksi; serta
- aplikasi mobile native.

## 7. Alur pengguna utama

1. Pengguna membuka dashboard lokal; forecast dan kondisi awal langsung tampil.
2. Pengguna memeriksa sumber, periode, pembaruan terakhir, asumsi, dan status data sintetis.
3. Pengguna memilih salah satu dari tiga komoditas.
4. Pengguna melihat forecast harga tujuh hari dan label tekanan pasar.
5. Pengguna melihat estimasi neraca lima wilayah dalam tabel/kartu berwarna.
6. Pengguna mengubah total anggaran dan/atau total kapasitas angkut.
7. Pengguna menekan `Jalankan Skenario`.
8. Sistem memvalidasi input dan menjalankan optimizer.
9. Pengguna meninjau rekomendasi alokasi serta metrik sebelum-sesudah.
10. Pengguna menyampaikan hasil untuk ditinjau pejabat di luar sistem.

Refresh halaman mengembalikan data dan parameter default. MVP tidak menyimpan skenario secara permanen.

## 8. Kebutuhan fitur

### 8.1 Forecast dan tekanan pasar

- Tampilkan harga aktual terakhir dan forecast harian dalam Rp/kg untuk tujuh hari.
- Bandingkan forecast hari ke-7 dengan harga aktual terakhir.
- Gunakan label demo berikut:
  - `Menurun`: perubahan kurang dari `-5%`;
  - `Stabil`: perubahan `-5%` sampai `+5%`;
  - `Waspada`: perubahan di atas `5%` sampai `10%`;
  - `Tinggi`: perubahan di atas `10%`.
- Nyatakan bahwa ambang tersebut adalah aturan demo, bukan ambang resmi pemerintah.

### 8.2 Estimasi surplus-defisit

- Hitung neraca wilayah sebagai `stok sintetis + estimasi pasokan - kebutuhan baseline`.
- Nilai positif adalah estimasi surplus dan nilai negatif adalah estimasi defisit.
- Tampilkan hasil sebagai estimasi/skenario, bukan kondisi operasional resmi.
- Tabel/kartu adalah visual utama. Peta bukan syarat penerimaan MVP.

### 8.3 Input skenario

- Pengguna hanya mengubah total anggaran distribusi dan total kapasitas angkut.
- Nilai per kendaraan, rute, atau gudang berasal dari dataset demo dan tidak diedit di UI.
- Optimizer berjalan hanya setelah pengguna menekan `Jalankan Skenario`.

### 8.4 Rekomendasi optimizer

Setiap rekomendasi menampilkan:

- peringkat prioritas;
- wilayah asal;
- wilayah tujuan;
- komoditas;
- jumlah alokasi dalam kg;
- estimasi biaya;
- status FEFO; dan
- sisa estimasi defisit setelah alokasi.

Urutan tujuan optimizer adalah mengurangi defisit, memprioritaskan stok yang paling dekat kedaluwarsa, lalu menekan biaya. Semua rekomendasi tunduk pada batas stok, kapasitas, dan anggaran.

### 8.5 Ringkasan dampak

Tampilkan perbandingan sebelum dan sesudah untuk:

- total estimasi defisit dalam kg;
- kebutuhan yang terpenuhi dalam persen;
- stok berisiko susut dalam kg; dan
- estimasi biaya distribusi dalam Rupiah.

### 8.6 FEFO

- Semua komoditas diurutkan berdasarkan tanggal kedaluwarsa terdekat.
- Cabai merah keriting dan cabai rawit merah diberi prioritas tinggi jika sisa usia simpan kurang dari tiga hari.
- Bawang merah mengikuti urutan FEFO tanpa ambang risiko hari yang belum tervalidasi.
- Tanggal kedaluwarsa pada MVP berasal dari data sintetis dan harus diberi label.

## 9. User stories dan acceptance outcome

| ID | User story | Acceptance outcome |
| --- | --- | --- |
| PRD-US-01 | Sebagai analis, saya ingin mengetahui sumber dan status data agar tidak salah menafsirkan hasil | Provenance, periode, pembaruan terakhir, dan label sintetis terlihat tanpa membuka halaman lain |
| PRD-US-02 | Sebagai analis, saya ingin memilih komoditas agar analisis fokus | Dashboard memperbarui forecast, neraca, dan skenario untuk komoditas terpilih |
| PRD-US-03 | Sebagai analis, saya ingin melihat forecast harga agar dapat mengenali tekanan pasar | Harga aktual, tujuh titik forecast, persentase perubahan, dan label tekanan tampil |
| PRD-US-04 | Sebagai analis, saya ingin melihat neraca wilayah agar mengetahui kandidat sumber dan tujuan | Lima wilayah menampilkan nilai neraca dan status estimasi surplus/defisit |
| PRD-US-05 | Sebagai analis, saya ingin mengubah batas anggaran dan kapasitas agar dapat membandingkan skenario | Nilai valid dapat diubah dan nilai tidak valid ditolak dengan pesan yang jelas |
| PRD-US-06 | Sebagai analis, saya ingin menjalankan optimizer agar memperoleh opsi intervensi | Skenario feasible menghasilkan rekomendasi terurut dalam kurang dari lima detik |
| PRD-US-07 | Sebagai analis, saya ingin mengetahui alasan prioritas agar hasil dapat dijelaskan | Rekomendasi memperlihatkan jumlah, biaya, FEFO, dan sisa defisit |
| PRD-US-08 | Sebagai analis, saya ingin membandingkan dampak agar dapat menilai manfaat skenario | Empat metrik sebelum-sesudah tampil setelah optimasi |
| PRD-US-09 | Sebagai analis, saya ingin kegagalan terlihat agar tidak memakai hasil yang tidak valid | Data/model/input/solver yang gagal menampilkan status yang sesuai dan tidak menyamarkan hasil |

Jika daftar rekomendasi kosong, sistem harus membedakan kondisi `no_intervention_needed` karena tidak ada defisit dari `constraints_block_intervention` karena anggaran, kapasitas, stok, atau rute menghalangi pengiriman.

## 10. Responsivitas dan lokalisasi

- Fitur inti dapat digunakan pada lebar viewport mulai 360px hingga desktop.
- Layout bertumpuk pada layar kecil.
- Tabel dapat berubah menjadi kartu atau menggunakan scroll horizontal.
- Targetnya fungsional dan terbaca, bukan *pixel-perfect* pada setiap perangkat.
- UI menggunakan Bahasa Indonesia, Rupiah (`Rp`), kilogram (`kg`), dan format tanggal Indonesia.

## 11. Indikator penerimaan produk

- Pengguna dapat menyelesaikan alur utama dalam maksimal lima menit.
- Alur demo P0 berjalan tanpa error yang menghalangi presentasi.
- Skenario demo menghasilkan rekomendasi feasible kurang dari lima detik.
- Seluruh sumber, asumsi, dan data sintetis dapat dikenali pengguna.
- Hasil dapat dijelaskan tanpa mengklaim permintaan aktual atau keputusan resmi.

WAPE di bawah 15%, peningkatan terhadap baseline, dan SUS di atas 75 tetap menjadi target validasi lanjutan, bukan gerbang MVP HackDay.

## 12. Dependency dan risiko

| Dependency/risiko | Respons produk |
| --- | --- |
| Dataset dan artefak forecast belum siap | Siapkan dan validasi sebelum HackDay; sediakan baseline berlabel |
| Metadata data publik lemah | Tampilkan provenance dan batasi klaim |
| Data operasional hanya sintetis | Beri label permanen dan batasi penggunaan untuk demo |
| Skenario tidak feasible | Tampilkan status dan constraint penyebab tanpa rekomendasi palsu |
| Scope bertambah | Fitur baru menggantikan scope lain atau masuk pasca-MVP |

## 13. Persetujuan

Seluruh anggota tim meninjau dokumen. Ismael memberikan persetujuan akhir sebelum status diubah menjadi baseline.
