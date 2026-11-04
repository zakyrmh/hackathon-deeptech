# Detailed Design, API, and Data Model — Food Demand Intelligence

| Atribut | Nilai |
| --- | --- |
| Status | Siap Ditinjau Tim v0.2 |
| Tanggal | 4 November 2026 |
| Pemilik | Zaky |
| Reviewer | Rafa, Silvana |
| Approver | Ismael |

## 1. Tujuan dan batas desain

Dokumen ini menetapkan interface modul, kontrak HTTP, model data runtime, aturan optimizer, dan state integrasi frontend-backend untuk MVP lokal. Desain mengikuti SRS dan ADR-0001: satu proses FastAPI pada `127.0.0.1:8000`, frontend React/Vite dari origin yang sama, satu bundle JSON read-only, dan tanpa database, autentikasi, CRUD, atau koneksi cloud.

API pada judul dokumen berarti kontrak HTTP. Dalam desain kode, istilah yang dipakai adalah **Module**, **Interface**, **Implementation**, **Seam**, dan **Adapter**.

## 2. Prinsip desain

- Hanya tiga kemampuan eksternal: health, dashboard per komoditas, dan optimasi skenario.
- Kompleksitas parsing bundle dan formulasi linear disembunyikan di balik interface modul yang kecil.
- Pydantic memvalidasi bentuk data; invariant domain divalidasi kembali oleh Implementation.
- Semua perhitungan memakai presisi penuh. Pembulatan hanya dilakukan oleh frontend.
- Input dan bundle identik harus menghasilkan hasil dan urutan identik.
- Runtime bersifat read-only dan stateless; refresh mengembalikan kondisi awal.
- Tidak dibuat service layer, repository, atau Adapter database hipotetis.

## 3. Modul dan seam

| Module | Interface | Tanggung jawab Implementation |
| --- | --- | --- |
| `runtime_data` | `load_bundle(path) -> RuntimeBundle`; `get_dashboard(commodity) -> DashboardData` | Baca sekali saat startup, validasi schema/invariant/hash, indeks komoditas, fallback forecast yang sudah dibundel |
| `optimizer` | `optimize(input, bundle) -> OptimizationResult` | Bangun variabel/matriks, solve leksikografis, FEFO, tie-break, post-validation, reason code, impact |
| `api` | tiga endpoint HTTP pada §5 | Translasi HTTP/Pydantic ke dua Module; tidak memuat aturan bisnis |
| `frontend` | state dan view satu halaman | Validasi input cepat, format lokal, request cancellation, rendering status/error/accessibility |

Seam nyata berada di kontrak `RuntimeBundle` antara pipeline dan runtime serta kontrak HTTP antara frontend dan backend. Karena hanya ada satu storage, tidak dibuat seam storage tambahan.

## 4. Konvensi kontrak HTTP

- Base path: `/api/v1`, kecuali health check.
- Media type: `application/json; charset=utf-8`.
- Field JSON: `snake_case` agar sama dengan model Python dan bundle.
- Tanggal: `YYYY-MM-DD`; timestamp: ISO 8601 dengan offset `+07:00`.
- Enum komoditas: `bawang_merah`, `cabai_merah_keriting`, `cabai_rawit_merah`.
- Nilai uang dalam Rupiah dan kuantitas dalam kilogram; angka respons tidak dibulatkan oleh backend.
- Endpoint runtime tidak menyediakan CORS karena frontend dan backend satu origin.
- HTTP `200` juga digunakan untuk hasil bisnis `infeasible`; status tersebut bukan kegagalan transport.

## 5. Endpoint

### 5.1 `GET /api/health`

Memeriksa kesiapan proses dan bundle.

Respons `200`:

```json
{
  "status": "ready",
  "bundle_version": "2026-11-04-demo.1",
  "generated_at": "2026-11-04T18:00:00+07:00"
}
```

Jika bundle tidak dapat dipakai, respons `503` dengan error `BUNDLE_NOT_READY`. Endpoint tidak menampilkan path lokal atau stack trace.

### 5.2 `GET /api/v1/dashboard/{commodity}`

Mengembalikan seluruh data yang diperlukan untuk mengganti komoditas tanpa optimizer.

Respons `200` berbentuk `DashboardData` (§7.2). Komoditas tidak dikenal menghasilkan `404 COMMODITY_NOT_FOUND`; bundle tidak siap menghasilkan `503 BUNDLE_NOT_READY`.

### 5.3 `POST /api/v1/scenarios/optimize`

Request:

```json
{
  "commodity": "cabai_merah_keriting",
  "budget_rp": 5000000,
  "capacity_kg": 2500,
  "bundle_version": "2026-11-04-demo.1"
}
```

Aturan:

- `budget_rp` bilangan bulat, minimum `0`, maksimum mengikuti konfigurasi komoditas;
- `capacity_kg` bilangan bulat, minimum `1`, maksimum mengikuti konfigurasi komoditas;
- `bundle_version` wajib sama dengan bundle aktif untuk mencegah hasil dari data UI yang basi;
- hanya satu request aktif dicegah pada frontend; backend tetap stateless.

Respons `200` berbentuk `OptimizationResult` (§7.3). Validasi request menghasilkan `422 VALIDATION_ERROR`; versi basi menghasilkan `409 BUNDLE_VERSION_MISMATCH`; waktu proses melebihi batas menghasilkan `504 OPTIMIZER_TIMEOUT` dan tanpa hasil lama.

### 5.4 Bentuk error

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Anggaran harus berupa bilangan bulat dalam batas skenario.",
    "fields": {"budget_rp": "Nilai maksimum 10000000."}
  }
}
```

| HTTP | Code | Kondisi |
| --- | --- | --- |
| 404 | `COMMODITY_NOT_FOUND` | Komoditas di luar tiga enum |
| 409 | `BUNDLE_VERSION_MISMATCH` | UI memakai versi data lama |
| 422 | `VALIDATION_ERROR` | Bentuk, tipe, atau batas input salah |
| 503 | `BUNDLE_NOT_READY` | Bundle hilang/tidak valid |
| 504 | `OPTIMIZER_TIMEOUT` | Batas waktu optimasi terlampaui |
| 500 | `INTERNAL_ERROR` | Kegagalan tak terduga; detail teknis hanya di log lokal |

## 6. State frontend

```text
booting -> ready | unavailable
ready --ganti komoditas--> loading_dashboard -> ready | dashboard_error
ready --input invalid--> ready (error inline, tombol nonaktif)
ready --jalankan--> optimizing -> result | optimize_error
result --ganti komoditas/invalid/timeout/error--> hasil lama dibersihkan
unavailable/dashboard_error/optimize_error --coba lagi--> state pemuatan terkait
```

Frontend menyimpan hanya state sesi di memori. Request dashboard lama dibatalkan/diabaikan jika pengguna mengganti komoditas lagi. Selama `optimizing`, tombol dinonaktifkan untuk mencegah double submit.

## 7. Model data runtime

### 7.1 `RuntimeBundle`

| Field | Tipe | Aturan |
| --- | --- | --- |
| `schema_version` | string | Versi schema, wajib dan dikenali runtime |
| `bundle_version` | string | Identitas immutable untuk satu build data |
| `generated_at` | datetime | Offset Asia/Jakarta |
| `timezone` | literal | `Asia/Jakarta` |
| `dataset_hash` | string | SHA-256 input/manifest yang relevan |
| `sources` | `DataSource[]` | Nama, periode, URL/referensi, cakupan, status verifikasi |
| `warnings` | string[] | Termasuk cakupan PIHPS belum terverifikasi bila masih berlaku |
| `commodities` | map enum → `CommodityData` | Tepat tiga komoditas |
| `regions` | `Region[]` | Tepat lima wilayah pilot dengan kode stabil |
| `inventory_batches` | `InventoryBatch[]` | Data operasional sintetis, tanggal kedaluwarsa wajib |
| `routes` | `Route[]` | Rute sintetis yang diizinkan dan biaya per kg |
| `scenarios` | map enum → `ScenarioConfig` | Default dan batas input per komoditas |

### 7.2 `DashboardData`

| Field | Tipe | Isi |
| --- | --- | --- |
| `bundle_version` | string | Versi untuk optimistic consistency |
| `commodity` | enum | Komoditas aktif |
| `metadata` | object | sumber, periode, update, asumsi, label sintetis/unverified |
| `last_actual` | `{date, price_rp_per_kg}` | Observasi valid terakhir |
| `forecast` | `ForecastPoint[7]` | Tujuh hari kalender berturut-turut |
| `market_pressure` | object | perubahan %, label, keterangan ambang demo |
| `balances` | `RegionBalance[5]` | Komponen dan neraca wilayah |
| `scenario` | `ScenarioConfig` | default/minimum/maksimum anggaran dan kapasitas |
| `warnings` | string[] | Batas klaim yang harus terlihat |

`ForecastPoint` memuat `date`, `price_rp_per_kg`, `is_imputed`, dan `model_name`. Hari akhir pekan membawa nilai hari kerja terakhir dan diberi `is_imputed=true`.

`RegionBalance` memuat `region_code`, `region_name`, `synthetic_stock_kg`, `estimated_supply_7d_kg`, `baseline_need_7d_kg`, dan `balance_kg`. Invariant: `balance_kg = synthetic_stock_kg + estimated_supply_7d_kg - baseline_need_7d_kg` dalam toleransi numerik.

### 7.3 `OptimizationResult`

| Field | Tipe | Aturan |
| --- | --- | --- |
| `status` | `feasible \| infeasible` | Status bisnis |
| `reason_code` | enum | Lihat tabel di bawah |
| `bundle_version` | string | Versi yang dihitung |
| `recommendations` | `Recommendation[]` | Kosong untuk no-action, blocked, atau infeasible |
| `impact` | `ImpactMetrics \| null` | Ada untuk hasil feasible |
| `explanation` | string | Bahasa Indonesia, aman ditampilkan |
| `blocking_constraints` | string[] | Diisi untuk constraints-block atau infeasible |
| `warnings` | string[] | Asumsi dan limitation relevan |

| Reason code | Status | Makna |
| --- | --- | --- |
| `recommendations_available` | feasible | Minimal satu pengiriman memenuhi constraint |
| `no_intervention_needed` | feasible | Tidak ada defisit; daftar kosong |
| `constraints_block_intervention` | feasible | Ada defisit, tetapi anggaran/kapasitas/rute/stok menghalangi seluruh pengiriman |
| `model_infeasible` | infeasible | Constraint kontradiktif atau solver menyatakan infeasible |

`Recommendation` memuat `rank`, `origin_code/name`, `destination_code/name`, `commodity`, `quantity_kg`, `estimated_cost_rp`, `inventory_batch_ids`, `fefo_status`, dan `remaining_deficit_kg`.

`ImpactMetrics` memuat nilai sebelum/sesudah untuk `total_deficit_kg`, `need_fulfilled_pct`, `at_risk_stock_kg`, serta `distribution_cost_rp`.

### 7.4 Entitas optimizer

| Entitas | Field utama | Invariant |
| --- | --- | --- |
| `InventoryBatch` | id, region, commodity, quantity, expiry_date, synthetic | quantity ≥ 0; synthetic selalu true pada MVP |
| `Route` | origin, destination, cost_rp_per_kg, allowed | origin ≠ destination; biaya ≥ 0 |
| `ScenarioConfig` | default/min/max budget dan capacity | default berada dalam batas |
| `Region` | code, name | kode unik dan stabil |

Tidak ada entitas User, Session, Approval, atau Shipment aktual karena sistem tidak mengeksekusi distribusi maupun menyimpan histori.

## 8. Desain optimizer

Decision variable kontinu menyatakan kilogram dari batch asal ke tujuan melalui rute yang diizinkan. Nilai internal tidak dibulatkan.

Constraint wajib:

1. seluruh alokasi nonnegatif;
2. asal berbeda dari tujuan;
3. outbound tidak melebihi stok/surplus tersedia;
4. inbound tidak melebihi defisit tujuan;
5. total kuantitas tidak melebihi kapasitas;
6. total biaya tidak melebihi anggaran;
7. hanya rute `allowed=true`;
8. batch mengikuti FEFO.

Tujuan diselesaikan berurutan: maksimalkan pengurangan defisit; dengan optimum pertama dikunci, maksimalkan pemakaian batch terdekat kedaluwarsa; dengan keduanya dikunci, minimalkan biaya. Implementasi dapat memakai solve bertahap dengan toleransi numerik terdokumentasi. Hasil setara diurutkan stabil berdasarkan kode asal, tujuan, lalu komoditas.

Post-validation menghitung ulang setiap constraint dari solusi. Pelanggaran di atas toleransi tidak boleh dikirim sebagai `feasible`. Time limit solver ditetapkan di bawah lima detik agar serialisasi dan respons tetap memenuhi SRS.

## 9. Validasi startup bundle

Urutan fail-fast:

1. file ada dan JSON dapat dibaca;
2. schema/version dikenali;
3. metadata, timezone, hash, tiga komoditas, dan lima wilayah lengkap;
4. tanggal forecast tepat tujuh dan berurutan;
5. referensi region/commodity/batch/route valid;
6. nilai numerik finite dan memenuhi invariant;
7. default input berada dalam batas;
8. label sintetis dan status verifikasi sumber tersedia.

Kegagalan membuat health `503`, menonaktifkan optimizer, dan tidak diatasi dengan menciptakan nilai fallback baru. Baseline forecast hanya boleh digunakan jika sudah dihasilkan pipeline dan dilabeli di bundle.

## 10. Integrasi dan sequence

```text
Browser -> GET /api/health
Browser -> GET /api/v1/dashboard/cabai_merah_keriting
Backend -> runtime_data.get_dashboard(...)
Browser <- metadata + forecast + balance + defaults
User -> ubah budget/capacity -> validasi lokal
Browser -> POST /api/v1/scenarios/optimize
Backend -> optimizer.optimize(input, immutable bundle)
Backend <- validated result
Browser <- result -> recommendation + impact
```

## 11. Keamanan, observability, dan performa

- Bind eksplisit `127.0.0.1`; tidak menerima traffic LAN.
- Tidak ada secret, cookie, login, telemetry, atau request eksternal.
- Log lokal mencatat startup, versi bundle, endpoint, status, durasi, dan code error; tidak mencatat payload penuh.
- Dashboard target ≤3 detik, pergantian komoditas ≤1 detik, optimizer/timeout ≤5 detik.
- Bundle dimuat sekali dan immutable selama proses untuk mengurangi I/O dan mencegah perbedaan antarrequest.

## 12. Traceability desain

| Desain | Requirement utama |
| --- | --- |
| Health dan fail-fast | FR-001, FR-080–084, DR-006 |
| Dashboard endpoint | FR-002–005, FR-010–033, DR-001–007 |
| Optimize endpoint/result | FR-040–073, BR-003–006, IR-001–004 |
| State frontend | FR-013, FR-044–054, FR-066, FR-090–091 |
| Same-origin/local stateless runtime | NFR-SEC-001–004, NFR-REL-001–003 |
| Presisi dan format | UIR-004–006 |

## 13. Keputusan yang masih perlu dikonfirmasi

- Nilai final maksimum anggaran/kapasitas berasal dari bundle yang ditinjau Yolanda.
- Toleransi numerik solver ditetapkan saat golden test, lalu dicatat di kode dan laporan test.
- Nama versi dependency final mengikuti lockfile implementasi.
- ADR-0001 masih menunggu persetujuan Ismael; perubahan stack harus memperbarui dokumen ini.

## 14. Kriteria selesai desain

- Pydantic schema merepresentasikan seluruh kontrak di dokumen ini.
- Contract test mencakup tiga endpoint dan seluruh error code.
- Golden test mencakup tiga skenario: rekomendasi tersedia, tidak perlu intervensi, dan constraint menghalangi.
- Tidak ada endpoint CRUD/admin atau persistence tersembunyi.
- Rafa, Silvana, dan Ismael meninjau bagian sesuai peran.

