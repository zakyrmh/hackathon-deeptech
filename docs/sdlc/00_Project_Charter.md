# Project Charter — Food Demand Intelligence

| Atribut | Nilai |
| --- | --- |
| Status | Siap Ditinjau Tim v0.2 |
| Tanggal | 3 November 2026 |
| Pemilik inisiatif | Tim Food Demand Intelligence |
| Ketua tim | Ismael |
| Approver dokumen | Ismael |
| Batas MVP | Pitching dan exhibition, 28 November 2026 |
| Sponsor eksternal | Belum ada |
| Product Owner | Belum ditetapkan |
| Mitra resmi/pilot | Belum ada; masih berupa kandidat/penjajakan |

## 1. Latar belakang

Keputusan distribusi pangan daerah masih menghadapi data harga, produksi, konsumsi, stok, dan logistik yang terfragmentasi. Portal publik umumnya bersifat deskriptif, sedangkan perencanaan distribusi perlu melihat potensi surplus-defisit, usia simpan, kapasitas angkut, dan biaya secara bersamaan.

Food Demand Intelligence adalah purwarupa *decision support system* berbasis web. Sistem membantu pengguna meninjau prediksi jangka pendek dan mencoba skenario alokasi distribusi. Hasil sistem adalah rekomendasi untuk ditinjau manusia, bukan keputusan atau instruksi distribusi otomatis.

## 2. Tujuan proyek

Membangun satu *vertical slice* MVP yang dapat didemonstrasikan dalam HackDay 24 jam untuk:

1. menampilkan forecast harga harian dalam Rp/kg selama tujuh hari dari model atau baseline yang telah disiapkan, beserta label tekanan pasar turunannya;
2. menunjukkan estimasi kebutuhan baseline serta potensi surplus atau defisit untuk tiga komoditas;
3. menghasilkan rekomendasi alokasi antardaerah yang memenuhi batas stok, kapasitas, anggaran, dan prioritas FEFO;
4. memperlihatkan dampak skenario sebelum dan sesudah optimasi; dan
5. menyajikan sumber, asumsi, dan keterbatasan data secara transparan.

## 3. Komoditas dan wilayah MVP

Komoditas:

- bawang merah;
- cabai merah keriting; dan
- cabai rawit merah.

Cakupan analisis dapat menampilkan seluruh kabupaten/kota Sumatera Barat jika data publik memadai. Skenario optimasi demo dibatasi pada:

- Kabupaten Solok;
- Kabupaten Agam;
- Kabupaten Tanah Datar;
- Kota Padang; dan
- Kota Bukittinggi.

Wilayah tersebut adalah simpul skenario. Sistem tidak boleh mengklaim suatu wilayah selalu surplus atau defisit; status harus berasal dari data dan periode yang digunakan.

Untuk MVP, neraca wilayah dihitung sebagai `stok sintetis + estimasi pasokan - kebutuhan baseline`. Nilai positif adalah estimasi surplus dan nilai negatif adalah estimasi defisit.

Optimizer memprioritaskan pengurangan defisit, kemudian stok yang paling dekat kedaluwarsa, lalu biaya distribusi yang lebih rendah. Seluruh tujuan tetap tunduk pada batas stok, kapasitas, dan anggaran.

## 4. Scope MVP 24 jam

### 4.1 Termasuk

1. Satu dashboard web responsif yang berjalan lokal tanpa login.
2. Dataset demo yang telah disiapkan untuk lima wilayah dan tiga komoditas.
3. Forecast harga harian dalam Rp/kg selama tujuh hari menggunakan model atau baseline yang telah dilatih/disiapkan sebelumnya, beserta label tekanan pasar turunannya.
4. Tabel atau visual sederhana surplus-defisit.
5. Satu formulir simulasi untuk batas anggaran dan kapasitas angkut.
6. Rekomendasi asal, tujuan, komoditas, jumlah, estimasi biaya, dan prioritas FEFO.
7. Ringkasan kondisi sebelum dan sesudah optimasi.
8. Penanda bahwa rekomendasi harus ditinjau manusia.

### 4.2 Tidak termasuk

- login, RBAC, atau alur persetujuan digital;
- unggah CSV atau integrasi API eksternal;
- pelatihan ulang dan prediksi secara real-time;
- GIS kompleks atau optimasi rute jalan *turn-by-turn*;
- ekspor laporan;
- transaksi, pembayaran, pengadaan, armada, GPS, ERP, atau IoT;
- multi-tenant, billing, MLOps, high availability, dan infrastruktur produksi; serta
- eksekusi keputusan distribusi secara otomatis; dan
- aplikasi mobile native.

## 5. Deliverable

1. Dashboard MVP lokal yang dapat didemonstrasikan.
2. Dataset demo beserta sumber, asumsi, dan penanda data sintetis.
3. Artefak model/baseline forecast yang digunakan dalam demo.
4. Model optimasi dan skenario demo yang feasible.
5. Ringkasan hasil pengujian alur demo.
6. Materi pitching dan exhibition.

## 6. Milestone

| Tanggal | Milestone | Hasil yang diharapkan |
| --- | --- | --- |
| 10 November 2026 | Batas pengumpulan prototyping | Prototipe tahap seleksi terkirim |
| 13 November 2026 | Pengumuman seleksi tahap 2 | Status kelulusan prototyping diketahui |
| 16 November 2026 | Bootcamp MVP daring | Arah MVP dan persiapan HackDay dipertajam |
| 27 November 2026 | HackDay 24 Hours | *Vertical slice* MVP dibangun dan diuji |
| 28 November 2026 | Pitching, exhibition, dan awarding | MVP didemonstrasikan dan dipresentasikan |

## 7. Kriteria keberhasilan MVP

- Dashboard menyelesaikan satu alur demo tanpa error yang menghalangi presentasi.
- Forecast harga harian dalam Rp/kg selama tujuh hari tampil dari artefak model/baseline yang telah disiapkan, beserta label tekanan pasar turunannya.
- Sumber, periode, asumsi, dan keterbatasan data terlihat jelas.
- Semua rekomendasi optimizer memenuhi stok, kapasitas, anggaran, dan aturan FEFO.
- Solver selesai kurang dari lima detik untuk skenario demo.
- Perubahan parameter menghasilkan rekomendasi yang konsisten dan dapat dijelaskan.
- Ringkasan sebelum-sesudah dapat dipahami saat pitching.
- Sistem tidak mengklaim hasil sebagai keputusan distribusi resmi.

Target WAPE di bawah 15%, peningkatan terhadap baseline, dan SUS di atas 75 tetap merupakan target validasi lanjutan. Target tersebut bukan gerbang penerimaan MVP HackDay sebelum metadata data dan UAT mitra tervalidasi.

## 8. Tim dan kewenangan

| Nama | Peran | Kewenangan/tanggung jawab utama |
| --- | --- | --- |
| Ismael | Ketua Tim dan Mentor Ilmiah | Penanggung jawab akhir tim, metodologi, mutu, dan keputusan strategis |
| Yolanda Pagansa Putri | Profesional/domain pangan | Masukan praktik operasional pangan dan penjajakan jejaring/pilot; bukan perwakilan mitra resmi |
| Zaky Ramadhan | Koordinator Teknis | Keputusan teknis, integrasi MVP, repositori, deployment lokal, dan pengujian integrasi |
| Rafa Maritza Kardinal | AI & Data Engineer | Akuisisi dan pengolahan data, model prediksi, optimasi, serta logika FEFO |
| Silvana Yulia Damara | Koordinator Validasi Pengguna dan UI/UX | Kebutuhan pengguna, rancangan dashboard, skenario penggunaan, dan validasi pengguna |
| Yelsa Pagansa Putri | Koordinator Bisnis dan Hilirisasi | Model bisnis, hilirisasi, kemitraan, materi pitching, dan serah terima |

Tim merupakan pemilik inisiatif secara kolektif. Ismael memegang keputusan akhir strategis dan Zaky memegang keputusan teknis. Sponsor eksternal, Product Owner, serta mitra resmi belum ditetapkan.

## 9. Batas sumber daya dan asumsi

- Anggaran pengembangan belum ditetapkan.
- Pengembangan memprioritaskan perangkat tim, software open-source, dan layanan gratis.
- MVP harus dapat berjalan lokal dan tidak bergantung pada deployment publik.
- Masa operasi MVP yang dijanjikan berakhir pada demo 28 November 2026.
- Data MVP terdiri dari data publik dan data operasional sintetis; tidak menggunakan data pribadi atau rahasia mitra.
- Tim memiliki akses ke dataset dan artefak model yang diperlukan sebelum HackDay dimulai.
- Kebutuhan baseline dihitung dari data konsumsi dan populasi; ia bukan observasi permintaan harian aktual.
- Label surplus-defisit pada MVP merupakan estimasi/skenario sesuai data dan asumsi yang ditampilkan.
- FEFO mengurutkan semua komoditas berdasarkan tanggal kedaluwarsa terdekat. Stok cabai merah keriting dan cabai rawit merah diberi label prioritas tinggi jika sisa usia simpannya kurang dari tiga hari. Bawang merah tetap mengikuti urutan FEFO tanpa ambang risiko hari yang belum tervalidasi.
- Pilot, integrasi produksi, dan SaaS adalah arah pengembangan pasca-HackDay, bukan deliverable MVP.

## 10. Risiko utama

| Risiko | Dampak | Respons |
| --- | --- | --- |
| Metadata atau granularitas data publik tidak memadai | Klaim prediksi regional tidak valid | Tampilkan provenance dan batasan; gunakan klaim yang sesuai dengan data |
| Data operasional nyata belum tersedia | Optimasi tidak merepresentasikan operasi nyata | Gunakan data sintetis yang diberi label jelas |
| Scope tidak selesai dalam 24 jam | Demo gagal terintegrasi | Pertahankan satu *vertical slice* dan data yang telah disiapkan |
| Optimizer tidak menemukan solusi | Tidak ada rekomendasi demo | Siapkan skenario feasible dan tampilkan penyebab jika constraint tidak feasible |
| Model forecast gagal | Alur demo terhenti | Gunakan baseline sederhana yang diberi label |
| Hasil dipersepsikan sebagai keputusan resmi | Risiko salah penggunaan | Tampilkan disclaimer dan pertahankan tinjauan manusia |
| Ketergantungan internet/cloud | Demo terganggu | Pastikan alur utama berjalan lokal |

## 11. Persetujuan kerja

Dokumen ini adalah baseline kerja tim, bukan kontrak sponsor atau mitra. Perubahan scope yang mengancam batas 24 jam harus ditolak atau menggantikan scope lain secara eksplisit.

Seluruh anggota tim meninjau isi dokumen. Ismael sebagai Ketua Tim memberikan persetujuan akhir sebelum status dokumen diubah dari draft menjadi baseline.

