# Deployment and Operations — Food Demand Intelligence

| Atribut | Nilai |
| --- | --- |
| Status | Siap Ditinjau Tim v0.2 — command dikonfirmasi saat implementasi |
| Tanggal | 4 November 2026 |
| Pemilik operasi | Zaky |
| Approver | Ismael |

## 1. Sasaran operasi

MVP dijalankan lokal, offline, dan dapat dipulihkan cepat pada laptop demo. Deployment bukan layanan produksi: tidak ada cloud, container, database, daemon, login, telemetry, atau akses dari perangkat lain. FastAPI menyajikan API dan build frontend melalui satu proses di `http://127.0.0.1:8000`.

## 2. Platform dan prasyarat

- Platform utama: Linux pada laptop demo tim; Windows/macOS best effort sampai diuji.
- Python target: 3.12 atau versi tepat yang dibekukan di lock/dependency manifest.
- Node target: versi LTS yang memenuhi Vite/Vitest dan dibekukan di repository.
- Browser: Chrome/Chromium atau Edge Chromium terbaru yang telah diuji.
- Port lokal `8000` tersedia.
- Dependency sudah terinstal sebelum mode offline.
- `data/runtime/runtime_bundle.json` dan build frontend tersedia serta tervalidasi.

Versi aktual, bukan target di atas, dicatat dalam release manifest dan laporan test.

## 3. Artefak rilis

| Artefak | Kegunaan |
| --- | --- |
| source commit/tag | identitas kode |
| dependency lock/manifest Python dan Node | reproduksi environment |
| `frontend/dist/` | aset statis yang disajikan FastAPI |
| `data/runtime/runtime_bundle.json` | data runtime immutable |
| `artifacts/` | laporan benchmark/model dan provenance |
| test report + UAT evidence | bukti penerimaan |
| release manifest | commit, versi, hash bundle, dependency, waktu build |
| backup demo/video/slides | contingency exhibition |

Bundle, laporan model, dan build harus berasal dari release candidate yang sama. Hash mismatch adalah kondisi fail-fast, bukan warning yang boleh diabaikan.

## 4. Konfigurasi minimum

| Variabel | Default aman | Aturan |
| --- | --- | --- |
| `FDI_HOST` | `127.0.0.1` | nilai lain ditolak untuk MVP |
| `FDI_PORT` | `8000` | port lokal bebas konflik |
| `FDI_BUNDLE_PATH` | `data/runtime/runtime_bundle.json` | path file read-only |
| `FDI_LOG_LEVEL` | `INFO` | jangan tampilkan payload/stack trace ke UI |

Tidak ada secret atau kredensial. File `.env` tidak diperlukan untuk rilis MVP.

## 5. Build bersih

Command berikut adalah kontrak target dan wajib disesuaikan dengan file implementasi/lockfile sebelum diberi status operasional:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
npm --prefix frontend ci
npm --prefix frontend run build
.venv/bin/python -m pytest
npm --prefix frontend run test -- --run
```

Build final dilakukan dari commit bersih. Jangan mengandalkan cache internet pada hari demo. Simpan wheel/npm cache offline hanya jika sesuai aturan kompetisi.

## 6. Startup dan shutdown

Target launcher akhir adalah `scripts/run_demo.sh`, yang harus:

1. memeriksa Python environment, frontend build, bundle, dan port;
2. memvalidasi schema/hash bundle;
3. bind hanya ke `127.0.0.1`;
4. menampilkan URL lokal dan versi bundle; dan
5. keluar non-zero jika prerequisite gagal.

Command manual fallback:

```bash
.venv/bin/python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

Buka `http://127.0.0.1:8000`. Hentikan dengan `Ctrl+C`; pastikan proses berhenti dan port dilepas. Nama modul/launcher masih harus dicocokkan dengan implementasi aktual.

## 7. Startup validation

Sebelum aplikasi berstatus ready:

- frontend build ada;
- bundle dapat dibaca dan schema version dikenali;
- metadata, tiga komoditas, lima wilayah, forecast, scenario, batch, dan route lengkap;
- referensi dan invariant valid;
- bundle version/hash dicatat;
- bind address aman;
- port tersedia.

Kegagalan menampilkan pesan lokal yang dapat ditindaklanjuti dan membuat `/api/health` tidak ready. Runtime tidak boleh menambal data hilang secara otomatis.

## 8. Smoke test deployment

Jalankan setelah setiap build, restart, restore, atau perpindahan laptop:

1. start dari launcher dan pastikan tidak ada error;
2. `GET /api/health` mengembalikan `ready` dan bundle version benar;
3. buka dashboard, pastikan cabai merah keriting tampil sebagai default;
4. ganti ketiga komoditas;
5. jalankan skenario default dan periksa rekomendasi/impact;
6. jalankan fixture no-intervention dan constraint-block bila release menyediakan selector test;
7. refresh dan pastikan state reset;
8. cek keyboard dan viewport 360px;
9. putus internet, restart proses, dan ulangi alur utama;
10. catat commit, hash bundle, browser, durasi, dan hasil.

Tidak perlu mengekspos fixture/test selector pada UI pitching jika meningkatkan risiko; fixture boleh diverifikasi lewat suite otomatis.

## 9. Logging dan observability

Log lokal minimum:

- timestamp Asia/Jakarta dan level;
- startup/shutdown;
- commit/release dan bundle version/hash;
- method/path, status, dan durasi request;
- durasi/status optimizer dan reason code;
- error code aman.

Jangan mencatat isi bundle penuh, payload penuh, path sensitif, secret, atau stack trace ke browser. Karena tidak ada telemetry eksternal, pemantauan dilakukan dari terminal, health endpoint, dan checklist operator.

## 10. Runbook insiden

| Gejala | Diagnosis | Tindakan |
| --- | --- | --- |
| Port 8000 terpakai | periksa proses lokal | hentikan proses lama yang teridentifikasi atau pilih port lokal yang dicatat |
| Health 503 | baca error startup dan validasi bundle | gunakan bundle rilis tervalidasi; jangan membuat angka baru |
| Halaman kosong/aset 404 | build `frontend/dist` hilang atau path salah | restore/rebuild aset lalu restart |
| Versi data mismatch | UI/cache lama terhadap proses baru | hard refresh/restart browser; pastikan satu release |
| Optimizer timeout | cek fixture, ukuran problem, log durasi | retry sekali; bila berulang gunakan release backup tervalidasi/video |
| Hasil tampak basi | state/error handling gagal | hentikan demo hasil tersebut; restart dan catat defect Critical |
| Browser bermasalah | cek browser/version/cache | gunakan browser cadangan yang sudah smoke-test |
| Laptop gagal | perangkat utama tidak tersedia | pindah ke laptop cadangan dengan release yang sama dan ulang smoke test |

Target recovery demo adalah kurang dari 10 menit; ini sasaran operasional dan harus dibuktikan saat rehearsal, bukan SLA produksi.

## 11. Backup dan rollback

Simpan minimal dua salinan offline dari:

- repository/release archive yang telah diuji;
- Python/Node dependency yang diperlukan bila diizinkan;
- frontend build;
- bundle dan hash;
- artifacts/model report;
- slides, screenshot, dan video alur utama.

Rollback berarti menghentikan proses, memilih satu release lengkap sebelumnya (kode + build + bundle + manifest), memulai ulang, lalu menjalankan smoke test. Jangan mencampur bundle lama dengan kode baru. Release lama tidak dihapus sampai pitching selesai.

## 12. Rehearsal dan hari demo

Sebelum 10, 27, dan 28 November:

- lakukan clean build dan full test sesuai 08;
- lakukan smoke offline dan cold restart;
- ukur performa pada laptop utama dan cadangan;
- isi daya, nonaktifkan update/notifikasi yang mengganggu, dan siapkan charger;
- verifikasi resolusi layar/projector serta zoom browser;
- pastikan label synthetic/unverified dan disclaimer terlihat;
- simpan bukti versi yang didemokan;
- dokumentasikan baseline/perubahan sesuai aturan HackDay yang akhirnya diklarifikasi.

## 13. Keamanan dan privasi operasi

- Bind hanya localhost, bukan `0.0.0.0`.
- Tidak membuka firewall/router atau tunnel.
- Tidak ada data pribadi/rahasia mitra.
- Tidak mengirim request runtime ke internet.
- Aset pihak ketiga harus dibundel lokal dan lisensinya diperiksa.
- Rekomendasi tetap bahan tinjauan manusia, bukan instruksi distribusi.

## 14. Batasan

- Tidak ada high availability, autoscaling, backup database, audit trail, atau remote monitoring.
- Pembaruan data membutuhkan pipeline/build bundle baru dan restart.
- Windows/macOS, Firefox, dan Safari bukan gate sampai ada hasil test.
- Command final bergantung pada struktur implementasi yang belum tersedia per 4 November 2026.

## 15. Checklist Go/No-Go

`Go` hanya bila build, health, E2E utama, offline smoke, performa, bundle/hash, backup, dan rehearsal lulus; tidak ada Blocker/Critical; serta klaim data/model sesuai bukti. Ismael memutuskan Go/No-Go berdasarkan rekomendasi test lead dan owner workstream.

