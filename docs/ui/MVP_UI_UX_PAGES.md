# Daftar Halaman MVP, Fitur, dan Komponen untuk Desain UI/UX — Food Demand Intelligence

| Atribut | Nilai |
| --- | --- |
| Status | Draf untuk desain UI/UX |
| Tanggal | 7 November 2026 |
| Referensi | `docs/sdlc/02_PRD.md`, `docs/sdlc/03_SRS.md`, `docs/sdlc/05_Software_Architecture.md`, `docs/sdlc/06_Detailed_Design_API_and_Data_Model.md`, `docs/sdlc/10_User_Guide_and_UAT.md`, `../../CONTEXT.md` |

## 1. Kesimpulan penting dari dokumen

PRD §5 "Satu alur" dan SRS UIR-001 **mengunci MVP sebagai satu halaman dashboard tanpa login** — bukan multi-halaman. Yang dibutuhkan bukan daftar halaman, tapi **daftar section + state screen** untuk desain UI/UX. Stretch goal: peta sederhana Sumbar. Won't have: login, upload, riwayat, ekspor, GIS.

## 2. Daftar halaman MVP

| # | Halaman | Sumber requirement |
| --- | --- | --- |
| H1 | **Dashboard utama** (satu-satunya halaman, 7 section berurutan) | UIR-001, PRD §7 |
| H2 | **Peta sederhana Sumbar** — *stretch goal saja*, hanya jika P0 stabil | PRD §6.2 |

Tambahan untuk desain UX — bukan halaman, tapi **state screen yang wajib didesain** (PRD P0 #12, SRS FR-080–084):

- Booting/loading awal.
- `Layanan analisis tidak tersedia` + tombol `Coba Lagi`.
- Optimizer berjalan (loading, tombol nonaktif).
- Timeout (`504`) + `Coba Lagi`.
- Skenario tidak feasible (infeasible + alasan constraint).
- Error inline input (anggaran/kapasitas invalid).

## 3. Fitur dan komponen per section (urutan wajib sesuai UIR-001)

### 3.1 Section 1 — Status & Provenance Data

- **Fitur:** sumber, periode, pembaruan terakhir, asumsi, label sintetis/unverified **selalu terlihat tanpa tooltip** (UIR-002); status kesehatan layanan (FR-001).
- **Komponen:**
  - Banner status layanan (ready/unavailable).
  - Metadata strip (sumber, periode, `bundle_version`, update terakhir).
  - Badge "data sintetis" dan "unverified" (teks/ikon, bukan warna saja — UIR-003).
  - Disclaimer "rekomendasi = bahan tinjauan manusia".

### 3.2 Section 2 — Pemilih Komoditas

- **Fitur:** pilih 1 dari 3 komoditas, default `cabai merah keriting` (FR-003, FR-010). Ganti komoditas → reset skenario ke default dan hapus hasil optimizer (FR-012, FR-013).
- **Komponen:**
  - Tab/toggle group 3 komoditas (keyboard-accessible, fokus terlihat).
  - Label default.

### 3.3 Section 3 — Forecast Harga & Tekanan Pasar

- **Fitur:** harga aktual terakhir, 7 titik forecast Rp/kg (tanggal berurutan, weekend `is_imputed` ditandai), perubahan hari ke-7 %, label `Menurun/Stabil/Waspada/Tinggi` (BR-001), catatan "ambang demo, bukan ambang resmi" (FR-025).
- **Komponen:**
  - Line chart Recharts (aktual + forecast, container responsif).
  - Kartu harga terakhir + badge label tekanan dengan ikon.
  - Marker/tooltip untuk titik imputasi.
  - Footnote ambang demo.

### 3.4 Section 4 — Neraca Wilayah (surplus-defisit)

- **Fitur:** 5 wilayah pilot (Solok, Agam, Tanah Datar, Kota Padang, Bukittinggi), neraca = stok + pasokan − kebutuhan, label estimasi surplus/defisit, disclaimer "estimasi/skenario" (FR-030–033).
- **Komponen:**
  - Tabel (desktop) ↔ kartu wilayah berwarna + ikon (mobile ≤360px) — bukan warna saja.
  - Angka kg bulat.
  - Penjelasan disclaimer.

### 3.5 Section 5 — Input Skenario

- **Fitur:** ubah anggaran (Rp, ≥0) dan kapasitas angkut (kg, ≥1), batas maks dari bundle; error inline untuk kosong/negatif/desimal/over-max; tombol `Jalankan Skenario` nonaktif saat invalid (FR-040–045).
- **Komponen:**
  - 2 number input dengan label + hint batas min/max.
  - Error message inline.
  - Tombol utama `Jalankan Skenario` (disabled state, loading state, mencegah double submit).
  - Spinner/progress saat optimizing.

### 3.6 Section 6 — Rekomendasi Distribusi

- **Fitur:** hasil optimizer — tiap rekomendasi: peringkat, asal, tujuan, komoditas, kg, biaya Rp, status FEFO, sisa defisit. Skenario kosong dibedakan: `no_intervention_needed` vs `constraints_block_intervention` vs infeasible (FR-060–066). Hasil lama dihapus saat gagal/timeout.
- **Komponen:**
  - Tabel rekomendasi ↔ kartu ber-stack (mobile).
  - Empty state 3 varian dengan reason code + penjelasan Bahasa Indonesia.
  - State error infeasible dengan daftar `blocking_constraints`.
  - Disclaimer FEFO (cabai <3 hari prioritas tinggi).

### 3.7 Section 7 — Ringkasan Dampak (sebelum/sesudah)

- **Fitur:** 4 metrik before/after: total defisit kg, kebutuhan terpenuhi %, stok berisiko susut kg, biaya distribusi Rp (FR-070–073).
- **Komponen:**
  - 4 kartu metrik dengan nilai sebelum → sesudah (panah/delta).
  - Ikon + label teks untuk arah perbaikan.

## 4. Catatan desain lintas-section

- Layout bertumpuk di mobile (360px), responsive sampai desktop; Bahasa Indonesia, Rupiah (`Rp`), kilogram (`kg`), tanggal format Indonesia (UIR-004–005).
- Aksesibilitas: semua kontrol keyboard, fokus terlihat, kontras ≥4.5:1, status bukan warna saja (NFR-A11Y).
- Semua state hilang saat refresh — tidak ada navigasi kembali atau histori.
- Backend error contract lengkap di `docs/sdlc/06_Detailed_Design_API_and_Data_Model.md` §5.4 (validasi, timeout, versi bundle basi).

## 5. Risk

ADR stack masih berstatus *proposed* (menunggu approval Ismael) — jika stack berubah, section/komponen UI tetap sama, hanya chart library-nya yang bisa beda.
