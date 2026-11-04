# Laporan Singkat Progres Dataset

**Tanggal:** 3 November 2026  
**Proyek:** Food Demand Intelligence

## Hasil malam ini

- Proposal sudah tersedia dalam format Markdown agar mudah dibaca dan diproses oleh agent.
- Data raw BPS Sumatera Barat sudah tersedia untuk produksi 2024, konsumsi 2025, dan jumlah penduduk 2025.
- Tiga file harga harian PIHPS sudah tersimpan untuk bawang merah, cabai merah keriting, dan cabai rawit, dengan periode 25 Oktober 2024–2 November 2026.
- Data iklim bulanan BMKG sudah tersedia untuk Stasiun Padang Panjang dan Teluk Bayur, periode November 2024–September 2026.
- Sumber, checksum, dan keterbatasan data sudah dicatat dalam manifest dan dokumentasi raw.
- Seluruh data olahan sebelumnya sudah dihapus. Folder `data/processed/` sengaja dikosongkan agar hasil berikutnya hanya dibuat melalui pipeline Python/notebook yang transparan.

## Temuan penting

- File PIHPS tidak menyimpan metadata daerah. Belum dapat dipastikan apakah datanya merupakan agregat Sumatera Barat, Kota Padang, atau nasional.
- Data BMKG masih bulanan dan terlalu agregat untuk menjadi fitur utama forecast harian 7–14 hari. Beberapa periode awal Padang Panjang juga tidak memiliki pengukuran.
- Data BPS cocok sebagai baseline struktural produksi dan konsumsi, bukan sebagai stok atau permintaan harian.

## Langkah selanjutnya

1. Memastikan wilayah dan tingkat agregasi data PIHPS atau melakukan ekspor ulang dengan metadata filter yang lengkap.
2. Mengajukan data cuaca harian melalui PTSP/UPT BMKG Sumatera Barat.
3. Memperbarui `../data/DATASET_GUIDE.md` sesuai kondisi dataset terbaru.
4. Membuat satu pipeline Python/notebook untuk membersihkan, memvalidasi, dan menggabungkan BPS, PIHPS, serta BMKG.
5. Menjalankan EDA dan baseline forecast setelah validasi wilayah PIHPS selesai.

**Status saat ini:** data raw dan provenance sudah tertata, tetapi dataset belum siap digunakan untuk klaim forecast regional sebelum metadata PIHPS dan granularitas cuaca diselesaikan.
