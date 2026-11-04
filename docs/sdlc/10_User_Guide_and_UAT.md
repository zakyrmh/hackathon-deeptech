# User Guide and UAT — Food Demand Intelligence

| Atribut | Nilai |
| --- | --- |
| Status | Siap Ditinjau Tim v0.2 — UAT belum dijalankan |
| Tanggal | 4 November 2026 |
| Pemilik panduan/UAT | Silvana |
| Reviewer domain | Yolanda |
| Approver | Ismael |

## 1. Untuk siapa panduan ini

Panduan ditujukan kepada Analis Distribusi Pangan yang mengeksplorasi estimasi kondisi pangan dan rekomendasi skenario. Sistem tidak mengirim barang, tidak membuat keputusan resmi, dan tidak menggantikan verifikasi lapangan atau persetujuan penanggung jawab.

## 2. Sebelum mulai

- Operator teknis telah menjalankan aplikasi sesuai dokumen 09.
- Buka URL lokal yang diberikan, biasanya `http://127.0.0.1:8000`.
- Pastikan banner status layanan menyatakan siap.
- Periksa sumber, periode, waktu pembaruan, asumsi, label sintetis, dan status cakupan data.
- Bila cakupan PIHPS masih belum terverifikasi, jangan menyebut harga sebagai representasi resmi Sumatera Barat.

## 3. Mengenali halaman

Urutan satu halaman:

1. status dan provenance data;
2. pemilih komoditas;
3. harga aktual, forecast tujuh hari, dan tekanan pasar;
4. estimasi neraca lima wilayah;
5. input anggaran dan kapasitas;
6. rekomendasi distribusi;
7. ringkasan dampak.

Semua angka stok, usia simpan, rute, biaya, dan kapasitas pada MVP adalah data operasional sintetis. Forecast adalah prediksi harga, bukan prediksi permintaan harian aktual.

## 4. Menjalankan alur utama

### 4.1 Pilih komoditas

Pilih bawang merah, cabai merah keriting, atau cabai rawit merah. Cabai merah keriting adalah default. Pergantian komoditas memperbarui forecast, tekanan, neraca, dan nilai default; hasil optimasi sebelumnya dihapus.

### 4.2 Baca forecast dan tekanan pasar

- Harga aktual terakhir dan forecast ditampilkan dalam Rp/kg.
- Forecast mencakup tujuh hari kalender sesudah observasi terakhir.
- Akhir pekan membawa nilai hari kerja terakhir dan ditandai sebagai imputasi.
- Tekanan pasar membandingkan forecast hari ke-7 dengan harga aktual terakhir:
  - `< -5%`: Menurun;
  - `-5%` sampai `+5%`: Stabil;
  - `>5%` sampai `10%`: Waspada;
  - `>10%`: Tinggi.

Ambang ini untuk demo, bukan ambang resmi pemerintah.

### 4.3 Baca estimasi neraca

Lima wilayah pilot adalah Kabupaten Solok, Agam, Tanah Datar, Kota Padang, dan Bukittinggi. Neraca dihitung sebagai:

`stok sintetis + estimasi pasokan tujuh hari - kebutuhan baseline tujuh hari`.

Nilai positif berarti estimasi surplus; nilai negatif berarti estimasi defisit. Keduanya adalah skenario analitis, bukan status operasional resmi.

### 4.4 Isi skenario

- Anggaran: Rupiah bulat, minimum `0`, maksimum sesuai batas yang tampil.
- Kapasitas: kilogram bulat, minimum `1`, maksimum sesuai batas yang tampil.
- Nilai kosong, negatif, desimal, atau melebihi maksimum menghasilkan error inline dan tombol nonaktif.

### 4.5 Jalankan dan baca hasil

Tekan `Jalankan Skenario` sekali. Saat proses berjalan, tunggu indikator selesai. Setiap rekomendasi memuat peringkat, asal, tujuan, komoditas, jumlah, biaya, status FEFO, dan sisa defisit.

Interpretasi hasil:

| Hasil | Arti | Tindakan pengguna |
| --- | --- | --- |
| Rekomendasi tersedia | Ada alokasi feasible | Tinjau asumsi, rute, FEFO, sisa defisit, dan dampak |
| Tidak diperlukan intervensi | Tidak ada defisit pada skenario | Jangan memaksakan distribusi; catat konteks |
| Constraint menghalangi | Ada defisit tetapi anggaran/kapasitas/rute/stok menghalangi seluruh alokasi | Ubah parameter secara wajar atau laporkan keterbatasan |
| Infeasible | Model/constraint kontradiktif | Jangan gunakan hasil; minta pemeriksaan teknis |
| Timeout/error | Proses gagal | Hasil lama harus hilang; pilih `Coba Lagi` sekali |

FEFO memprioritaskan batch paling dekat kedaluwarsa. Cabai dengan sisa usia simpan kurang dari tiga hari diberi prioritas tinggi. Bawang merah belum memiliki ambang hari sampai tervalidasi.

### 4.6 Baca dampak

Bandingkan sebelum dan sesudah untuk estimasi defisit, kebutuhan terpenuhi, stok berisiko susut, serta biaya distribusi. Perubahan ini adalah hasil model skenario dan tidak menjamin dampak lapangan.

## 5. Aturan penggunaan yang aman

- Selalu tampilkan sumber, periode, asumsi, dan limitation saat presentasi.
- Jangan menyebut data sintetis sebagai data operasional aktual.
- Jangan menganggap rekomendasi sebagai perintah pengiriman.
- Jangan menyimpulkan kausalitas atau keberhasilan kebijakan dari demo.
- Jangan memasukkan data pribadi atau rahasia mitra.
- Validasi di luar sistem diperlukan sebelum keputusan resmi.

## 6. Accessibility dan perangkat

Semua kontrol inti harus dapat dijangkau dengan `Tab`, memiliki fokus terlihat, dan dapat diaktifkan dengan keyboard. Status memiliki teks/ikon, bukan warna saja. Pada layar kecil mulai 360px, bagian bertumpuk; tabel dapat berubah menjadi kartu atau scroll horizontal. Chrome/Edge Chromium adalah browser wajib MVP.

## 7. Troubleshooting pengguna

| Masalah | Tindakan |
| --- | --- |
| `Layanan analisis tidak tersedia` | pilih `Coba Lagi`; jika tetap, hubungi operator teknis |
| Tombol nonaktif | periksa error anggaran/kapasitas dan batas maksimum |
| Data tampak tidak berubah | tunggu pemuatan; ganti komoditas kembali atau refresh |
| Hasil hilang setelah refresh | perilaku benar; MVP tidak menyimpan skenario |
| Timeout | coba sekali lagi; bila berulang hentikan penggunaan hasil |
| Angka tampak dibulatkan | tampilan dibulatkan; perhitungan internal memakai presisi penuh |

## 8. Tujuan UAT

UAT menilai apakah pengguna representatif dapat memahami dan menyelesaikan alur utama, bukan membuktikan akurasi model atau dampak kebijakan. Karena sponsor/mitra formal belum ada, tahap awal adalah UAT internal; jangan menyebutnya penerimaan instansi eksternal.

## 9. Peserta dan peran UAT

- Minimum tiga peserta internal bila tersedia.
- Yolanda menjadi reviewer domain/pengguna representatif.
- Silvana memfasilitasi dan mencatat observasi.
- Minimal satu peserta bukan implementer utama alur yang diuji.
- Zaky menangani defect teknis; Rafa menjawab data/model; Ismael menyetujui penerimaan.

Identitas, ketersediaan, dan jadwal peserta belum dikonfirmasi. UAT eksternal dengan instansi/mitra ditunda sampai pihak tersebut ada.

## 10. Prasyarat UAT

- Release candidate dan bundle/hash telah dibekukan.
- Smoke test, test P0, dan offline mode lulus.
- Label sintetis/unverified dan disclaimer terlihat.
- Moderator memiliki skenario dan lembar observasi.
- Peserta menerima konteks singkat, bukan panduan langkah demi langkah.
- Sesi direkam hanya dengan persetujuan; tanpa data pribadi di artefak publik.

## 11. Skenario UAT

| ID | Tugas peserta | Kriteria penerimaan |
| --- | --- | --- |
| UAT-01 | Verifikasi status/sumber/periode/label data | Menemukan dan menjelaskan mana data publik vs sintetis |
| UAT-02 | Pilih satu komoditas dan jelaskan forecast | Menjelaskan 7 hari, Rp/kg, tekanan, dan ambang demo |
| UAT-03 | Identifikasi wilayah defisit terbesar | Memahami tanda neraca dan disclaimer estimasi |
| UAT-04 | Isi budget/capacity valid lalu jalankan | Selesai tanpa bantuan kritis dan tanpa double submit |
| UAT-05 | Jelaskan satu rekomendasi dan FEFO | Menyebut asal, tujuan, kg, biaya, sisa defisit, limitation |
| UAT-06 | Bandingkan dampak before/after | Membaca empat metrik dengan benar |
| UAT-07 | Tangani no-intervention dan constraint-block | Membedakan kedua keadaan dan tindakan yang aman |
| UAT-08 | Selesaikan alur pada viewport kecil/keyboard | Fitur inti dapat dipakai mulai 360px dan keyboard |
| UAT-09 | Hadapi timeout/service unavailable | Tidak memakai hasil lama; menemukan retry |

Alur inti UAT-01 sampai UAT-06 ditargetkan selesai maksimal lima menit.

## 12. Pertanyaan pascaskenario

Gunakan skala 1 (sangat tidak setuju) sampai 5 (sangat setuju):

1. Saya memahami status dan batas data yang ditampilkan.
2. Saya dapat membedakan forecast harga, neraca estimasi, dan rekomendasi.
3. Input anggaran/kapasitas dan error mudah dipahami.
4. Alasan ketika tidak ada rekomendasi cukup jelas.
5. Saya dapat menjelaskan hasil tanpa menganggapnya keputusan resmi.
6. Tampilan dapat dibaca dan digunakan pada perangkat yang diuji.

Pertanyaan terbuka: bagian paling membingungkan; informasi yang kurang; istilah yang perlu diubah; dan risiko salah tafsir yang masih terlihat. SUS formal dapat dilakukan pada pilot, tetapi bukan gate MVP tanpa peserta representatif yang memadai.

## 13. Form hasil UAT

| Field | Isi |
| --- | --- |
| Session/date/release/bundle | diisi saat eksekusi |
| Participant role/device/browser | diisi tanpa PII yang tidak perlu |
| Task result | Pass / Pass with help / Fail / Not Run |
| Completion time | menit:detik |
| Critical assistance | ya/tidak + catatan |
| Misinterpretation | data/model/rekomendasi/disclaimer |
| Defect/feedback ID | tautan defect log/backlog |
| Participant comments | ringkasan |

## 14. Kriteria penerimaan UAT

- seluruh peserta menyelesaikan UAT-01–06;
- minimal dua dari tiga selesai tanpa bantuan kritis;
- median alur inti maksimal lima menit;
- tidak ada salah tafsir Critical tentang data sintetis, cakupan, atau rekomendasi sebagai keputusan resmi;
- UAT-07 dan UAT-09 tidak meninggalkan hasil basi;
- seluruh temuan Major ke atas diperbaiki atau mendapat waiver Ismael.

Jika peserta aktual kurang dari tiga, hasil dilaporkan sebagai usability dry run, bukan UAT final.

## 15. Status dan sign-off

UAT belum dijalankan per 4 November 2026. Sign-off akhir memuat release/hash, ringkasan hasil, defect terbuka, waiver, rekomendasi Silvana/Yolanda, dan keputusan Ismael: `Accepted`, `Accepted with conditions`, atau `Rejected`.

