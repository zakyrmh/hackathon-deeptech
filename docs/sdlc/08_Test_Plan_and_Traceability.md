# Test Plan and Traceability — Food Demand Intelligence

| Atribut | Nilai |
| --- | --- |
| Status | Siap Ditinjau Tim v0.2 — eksekusi test belum dimulai |
| Tanggal | 4 November 2026 |
| Test lead | Zaky |
| Kontributor | Rafa, Silvana, Yolanda |
| Approver | Ismael |

## 1. Tujuan

Rencana ini menentukan bagaimana MVP diverifikasi terhadap PRD, SRS, spesifikasi data/AI, dan desain. Dokumen tidak mengklaim test telah lulus: kolom hasil tetap `Not Run` sampai ada command, tanggal, environment, dan evidence nyata.

## 2. Scope

Termasuk:

- pipeline, quality gate, bundle schema, dan reproducibility;
- forecast, business rules, optimizer, dan reason code;
- kontrak tiga endpoint;
- state, format, aksesibilitas, dan responsivitas frontend;
- performa lokal, offline, startup, recovery, dan alur E2E;
- UAT internal untuk alur keputusan.

Tidak termasuk: produksi/cloud, multiuser, auth, database, integrasi data live, keamanan jaringan publik, Firefox/Safari sebagai release gate, dan validasi dampak distribusi dunia nyata.

## 3. Strategi dan level test

| Level | Tool target | Fokus | Owner |
| --- | --- | --- | --- |
| Unit pipeline/backend | pytest | transformasi, formula, invariant, pressure, FEFO, impact | Rafa/Zaky |
| Golden optimizer | pytest | tiga skenario deterministik dan constraint | Zaky/Rafa |
| Bundle/schema | pytest + Pydantic | schema, referensi, hash, metadata, fail-fast | Rafa/Zaky |
| HTTP contract | pytest/FastAPI test client | payload, code, status, error | Zaky |
| Frontend unit | Vitest | validasi input, formatter, reducer/state, rendering | Silvana/Zaky |
| E2E | Playwright Chromium | alur desktop dan mobile 360px | Silvana/Zaky |
| Manual | checklist/browser | keyboard, focus, contrast, label, offline, rehearsal | Silvana |
| Data/model evaluation | pipeline report | rolling-origin, WAPE/MAE, selection gate | Rafa |
| UAT | skenario §10 dan dokumen 10 | pemahaman dan kegunaan alur | Silvana/Yolanda |

## 4. Test environment

- Primary: laptop demo lokal, OS Linux yang dipakai tim, Python dan Node dari lockfile.
- Browser wajib: Chrome/Chromium dan Edge Chromium terbaru yang tersedia saat test; satu viewport desktop dan minimal `360x800`.
- Firefox/Safari: best effort, bukan release gate.
- Network mode: online untuk instalasi saja; alur penerimaan dijalankan dengan internet dinonaktifkan.
- Data: bundle kandidat rilis dengan hash tercatat dan tiga fixture skenario deterministik.

Environment aktual wajib direkam saat test: OS, CPU/RAM, browser/version, Python, Node, commit, bundle version/hash, tanggal, dan tester.

## 5. Entry dan exit criteria

Entry:

- kontrak 06 disetujui untuk implementasi;
- bundle/fixture lolos schema dasar;
- build frontend dan backend dapat dimulai;
- test data tiga skenario tersedia.

Exit MVP:

- semua test P0 lulus;
- tidak ada defect Blocker/Critical terbuka;
- seluruh requirement SRS memiliki test/evidence atau waiver disetujui Ismael;
- performa 3s/1s/5s terbukti pada laptop demo;
- alur offline, viewport 360px, dan keyboard lulus;
- hasil model dilaporkan jujur, termasuk bila baseline menang;
- smoke test final lulus setelah clean build/restart.

## 6. Severity dan disposition

| Severity | Definisi | Gate |
| --- | --- | --- |
| Blocker | aplikasi tidak start, alur demo tidak dapat selesai, data/hasil menyesatkan | wajib diperbaiki |
| Critical | constraint/angka salah, hasil basi tampil sebagai baru, klaim data salah | wajib diperbaiki |
| Major | fungsi P0 terganggu tetapi ada workaround aman | perbaiki atau waiver Ismael |
| Minor | kosmetik/tidak menghalangi alur | boleh backlog |

Defect log minimal memuat ID, test ID, requirement, severity, environment, langkah reproduksi, expected/actual, evidence, owner, status, dan commit perbaikan.

## 7. Test data

| Fixture | Kondisi | Expected |
| --- | --- | --- |
| `scenario_recommendations` | Ada surplus, defisit, rute, anggaran, kapasitas | feasible + rekomendasi |
| `scenario_no_intervention` | Tidak ada defisit | feasible + `no_intervention_needed` + kosong |
| `scenario_constraints_block` | Ada defisit tetapi semua pengiriman terhalang | feasible + `constraints_block_intervention` + kosong |
| `bundle_invalid_*` | metadata/referensi/tanggal/nilai wajib salah | health 503, optimizer nonaktif |
| `request_invalid_*` | kosong, negatif, desimal, melebihi maksimum | error inline/422; tidak ada eksekusi |

Semua fixture sintetis harus berlabel dan memakai seed/config tetap. Expected golden result disimpan dengan presisi yang memungkinkan post-validation; UI snapshot bukan sumber kebenaran numerik.

## 8. Katalog test case

| ID | Pri | Test | Expected | Otomasi |
| --- | --- | --- | --- | --- |
| T-START-01 | P0 | Start dengan bundle valid | health ready, default cabai keriting, forecast/balance tampil | API/E2E |
| T-START-02 | P0 | Bundle hilang/rusak/metadata kurang | fail-fast, 503, optimizer nonaktif, tanpa angka buatan | Unit/API/E2E |
| T-COMM-01 | P0 | Ganti ketiga komoditas | data terkait berubah, default reset, hasil lama hilang ≤1s | Unit/E2E |
| T-FCST-01 | P0 | Periksa actual + 7 tanggal | 7 hari kalender berurutan; weekend imputed berlabel | Unit/E2E |
| T-PRESS-01 | P0 | Nilai tepat di sekitar -5%, +5%, +10% | label mengikuti BR-001 dan ambang demo terlihat | Unit |
| T-BAL-01 | P0 | Hitung lima wilayah | formula BR-002, label estimasi, disclaimer terlihat | Unit/E2E |
| T-INPUT-01 | P0 | Nilai valid termasuk batas | tombol aktif; payload integer benar | Unit/E2E |
| T-INPUT-02 | P0 | kosong/negatif/desimal/lebih maksimum | error inline; tombol nonaktif | Unit/E2E |
| T-OPT-01 | P0 | Fixture rekomendasi | semua constraint, tujuan, FEFO, urutan, impact benar | Golden/API/E2E |
| T-OPT-02 | P0 | Tidak ada defisit | feasible, reason no-intervention, kosong | Golden/API |
| T-OPT-03 | P0 | Constraint memblokir | feasible, reason blocked, batas dijelaskan | Golden/API |
| T-OPT-04 | P0 | Model kontradiktif/infeasible | infeasible, tanpa rekomendasi | Unit/API |
| T-OPT-05 | P0 | Request identik berulang | output dan order identik | Golden/API |
| T-OPT-06 | P0 | Double click dan timeout | satu request; timeout ≤5s; hasil lama bersih; retry ada | Unit/E2E |
| T-IMPACT-01 | P0 | Hitung before/after | deficit, fulfilled, at-risk, cost konsisten | Unit/API |
| T-PREC-01 | P0 | Angka pecahan internal | constraint memakai presisi penuh; UI saja dibulatkan | Unit |
| T-DATA-01 | P0 | Bundle schema/referential integrity | tiga komoditas, lima wilayah, metadata/hash valid | Unit |
| T-DATA-02 | P0 | Audit sumber dan synthetic | sumber/periode/update/asumsi/label terlihat | Unit/E2E |
| T-API-01 | P0 | Kontrak tiga endpoint | schema, HTTP, error code sesuai 06 | Contract |
| T-STATE-01 | P0 | Error setelah result sukses | rekomendasi lama tidak terlihat | Unit/E2E |
| T-RESET-01 | P0 | Refresh | kembali ke initial state, tanpa persistence | E2E |
| T-RESP-01 | P0 | 360px, tablet, desktop | fungsi inti usable; stack/card/scroll aman | E2E/manual |
| T-A11Y-01 | P0 | Keyboard/focus/label/status | seluruh kontrol usable, focus visible, bukan color-only | E2E/manual |
| T-A11Y-02 | P0 | Contrast teks utama | minimal 4.5:1 | Manual/tool |
| T-LOCAL-01 | P0 | Inspect bind/network | hanya localhost; tanpa telemetry/request eksternal | Manual |
| T-OFFLINE-01 | P0 | Putus internet lalu restart/alur | alur utama selesai | E2E/manual |
| T-PERF-01 | P0 | Cold start dashboard | ready ≤3s | Measurement |
| T-PERF-02 | P0 | Pergantian komoditas | update ≤1s | Measurement |
| T-PERF-03 | P0 | Optimizer | hasil atau timeout ≤5s | Measurement |
| T-MODEL-01 | P0 | Rolling-origin semua kandidat | 8 fold, horizon 5 hari kerja, WAPE/MAE | Pipeline |
| T-MODEL-02 | P0 | Selection rule | XGBoost hanya menang bila seluruh gate terpenuhi | Pipeline |
| T-MODEL-03 | P0 | Leakage/reproducibility | feature hanya masa lalu; seed/hash/param tercatat | Pipeline/review |
| T-UAT-01 | P0 | Alur pengguna ≤5 menit | peserta memahami input, output, limitation | UAT |

## 9. Requirement Traceability Matrix

| Requirement | Test ID | Evidence target |
| --- | --- | --- |
| FR-001–005 | T-START-01, T-START-02 | API/E2E report |
| FR-010–013 | T-COMM-01, T-STATE-01 | Vitest/Playwright |
| FR-020–025 | T-FCST-01, T-PRESS-01, T-DATA-02 | pytest/E2E |
| FR-030–033 | T-BAL-01, T-DATA-02 | pytest/E2E |
| FR-040–045 | T-INPUT-01, T-INPUT-02 | Vitest/Playwright/API |
| FR-050–058 | T-OPT-01, T-OPT-05, T-OPT-06 | golden/API/E2E |
| FR-060–066 | T-OPT-01–04, T-STATE-01 | golden/API/E2E |
| FR-070–073 | T-IMPACT-01 | pytest/API/E2E |
| FR-080–084 | T-START-02, T-STATE-01 | API/E2E |
| FR-090–091 | T-RESET-01 | Playwright |
| BR-001 | T-PRESS-01 | parameterized unit report |
| BR-002 | T-BAL-01 | unit report |
| BR-003–005 | T-OPT-01–05, T-PREC-01 | golden/post-validation |
| BR-006 | T-DATA-02, T-UAT-01 | screenshot/UAT |
| DR-001–008 | T-DATA-01, T-DATA-02, T-START-02, T-LOCAL-01 | schema/audit |
| UIR-001–006 | T-DATA-02, T-PREC-01, T-RESP-01, T-A11Y-01 | E2E/manual |
| IR-001–004 | T-API-01 | contract report |
| NFR-PERF-001–003 | T-PERF-01–03 | timing log |
| NFR-SEC-001–004 | T-LOCAL-01, T-DATA-01 | network/data audit |
| NFR-UX-001 | T-UAT-01 | timed UAT |
| NFR-A11Y-001–004 | T-A11Y-01–02 | evidence checklist |
| NFR-RESP-001–002 | T-RESP-01 | viewport screenshots/report |
| NFR-COMP-001–002 | T-RESP-01 | browser matrix |
| NFR-REL-001–003 | T-OPT-05, T-STATE-01, T-OFFLINE-01 | automated/manual report |

## 10. Acceptance/UAT scenarios

UAT detail berada di dokumen 10. Minimum internal dry run:

1. peserta memilih komoditas dan menjelaskan forecast/tekanan;
2. peserta mengidentifikasi wilayah estimasi defisit;
3. peserta mengubah budget/capacity dan menjalankan skenario;
4. peserta menjelaskan rekomendasi, FEFO, impact, dan limitation;
5. peserta menghadapi skenario no-intervention dan constraints-block;
6. peserta menyelesaikan alur utama maksimal lima menit tanpa bantuan kritis.

## 11. Model evaluation evidence

Laporan wajib memuat per komoditas dan kandidat: eligibility, fold dates, WAPE/MAE tiap fold, mean, win count, improvement terhadap naive, model terpilih, alasan, seed, features, parameter, data hash, dan runtime. Weekend imputation tidak ikut metrik. Hasil tersebut belum tersedia per 4 November 2026 dan tidak boleh dipalsukan.

## 12. Performa, accessibility, dan offline protocol

- Jalankan minimal lima kali setelah satu warm-up; laporkan median dan nilai terburuk.
- Ukur dari aksi pengguna sampai state siap/selesai, bukan hanya waktu solver.
- Accessibility manual meliputi urutan Tab, Enter/Space, focus ring, label input, heading, teks status, dan zoom 200% bila memungkinkan.
- Offline smoke dijalankan setelah dependency, build, dan bundle tersedia; network request yang gagal tidak boleh dibutuhkan alur inti.

## 13. Hasil eksekusi

| Suite | Status | Tanggal | Evidence |
| --- | --- | --- | --- |
| pytest | Not Run | — | — |
| Vitest | Not Run | — | — |
| Playwright desktop | Not Run | — | — |
| Playwright mobile 360px | Not Run | — | — |
| Performance | Not Run | — | — |
| Offline smoke | Not Run | — | — |
| Accessibility manual | Not Run | — | — |
| Model evaluation | Not Run | — | — |
| UAT | Not Run | — | — |

## 14. Release recommendation

Test lead memberi rekomendasi `Go`, `Conditional Go`, atau `No-Go` berdasarkan exit criteria dan defect. Hanya Ismael yang menyetujui waiver. Status dokumen “Siap Ditinjau” bukan bukti bahwa produk atau model telah lulus test.

