# Project Roadmap, RACI, and Risks — Food Demand Intelligence

| Atribut | Nilai |
| --- | --- |
| Status | Siap Ditinjau Tim v0.2 |
| Tanggal | 4 November 2026 |
| Periode | 4–28 November 2026 |
| Project lead | Ismael |
| Approver | Ismael |

## 1. Tujuan pengendalian proyek

Dokumen ini mengubah milestone program menjadi workstream, owner, gate, dan respons risiko. Scope dijaga pada satu vertical slice MVP lokal; fitur baru harus menggantikan scope lain atau dipindahkan setelah pitching.

## 2. Asumsi perencanaan

- Seluruh enam anggota tersedia sesuai workstream; ketersediaan aktual belum dikonfirmasi.
- Anggaran pengembangan belum ditetapkan; gunakan perangkat tim dan software open-source.
- Data PIHPS belum memiliki bukti filter wilayah.
- Pipeline terpadu dan runtime bundle belum tersedia pada 4 November.
- Ketentuan mengenai pekerjaan sebelum HackDay belum ditemukan.
- MVP dapat disiapkan sebelum HackDay sejauh tidak bertentangan dengan klarifikasi panitia.
- Demo harus dapat berjalan lokal dan offline.

## 3. Milestone program

| Tanggal | Milestone | Gate |
| --- | --- | --- |
| 10 Nov | Batas pengumpulan prototyping | Prototipe, narasi, dan bukti alur utama terkirim |
| 13 Nov | Pengumuman seleksi tahap 2 | Keputusan lanjut/stop atau penyesuaian backlog |
| 16 Nov | Bootcamp MVP daring | Feedback dicatat dan scope final dikunci |
| 27 Nov | HackDay 24 Hours | MVP terintegrasi, diuji, dan sesuai aturan panitia |
| 28 Nov | Pitching, exhibition, awarding | Demo offline, pitch, dan evidence siap |

## 4. Roadmap

### Fase 1 — Spesifikasi dan data gate, 4–6 November

| Deliverable | Owner | Done when |
| --- | --- | --- |
| Dokumen 04, 05, dan 07 | Zaky/Rafa | Siap ditinjau tim dan konsisten dengan SRS |
| Klarifikasi wilayah PIHPS | Rafa | Ada bukti filter/re-export atau label unverified diputuskan |
| Artikel domain tambahan | Tim, dikoordinasi Rafa | Referensi primer tersimpan dan relevansinya dicatat |
| Klarifikasi aturan pra-HackDay | Yelsa | Jawaban panitia tertulis atau status unknown terdokumentasi |
| Wireframe satu halaman | Silvana | Alur PRD terlihat pada desktop dan mobile |

### Fase 2 — Prototyping, 7–9 November

| Deliverable | Owner | Done when |
| --- | --- | --- |
| Pipeline baseline BPS/PIHPS | Rafa | Quality gate dan output awal dapat dijalankan ulang |
| Data sintetis tiga skenario | Rafa + Yolanda | Wajar untuk demo dan lolos invariant |
| Forecast/baseline awal | Rafa | Naive/MA/XGBoost menghasilkan laporan awal atau fallback jelas |
| Skeleton frontend | Silvana + Zaky | Satu halaman responsif menampilkan fixture |
| Skeleton backend/optimizer | Zaky + Rafa | Health, dashboard data, dan scenario flow bekerja |
| Prototype rehearsal | Seluruh tim | Alur maksimal lima menit tanpa blocker |

### Gate 1 — Pengumpulan, 10 November

- Bekukan versi prototipe.
- Jalankan smoke test offline.
- Simpan screenshot/video cadangan.
- Pastikan klaim data sesuai status PIHPS.
- Kirim materi sebelum deadline dan simpan bukti pengumpulan.

### Fase 3 — Review dan seleksi, 11–13 November

- Catat defect dan debt dari prototipe tanpa menambah scope.
- Rapikan dokumentasi eksperimen dan backlog.
- Konfirmasi ketersediaan anggota.
- Pada 13 November, lakukan decision gate berdasarkan hasil seleksi.

### Fase 4 — Persiapan bootcamp, 14–16 November

- Siapkan daftar pertanyaan dan keputusan terbuka.
- Ikuti bootcamp 16 November.
- Catat feedback; Ismael menyetujui perubahan scope.
- Bekukan MVP scope setelah bootcamp.

### Fase 5 — Implementasi MVP, 17–20 November

| Workstream | Hasil |
| --- | --- |
| Data/AI | Pipeline final, benchmark rolling-origin, model selection, forecast artifact |
| Synthetic/optimizer | Bundle scenario final, SciPy optimizer, reason code, golden tests |
| Architecture/backend | Pydantic schema, runtime loader, API, static frontend serving |
| Product/UI | Implementasi section dashboard dan state/error flow |

### Fase 6 — Integrasi dan hardening, 21–24 November

- Integrasikan build Vite dengan FastAPI satu origin.
- Selesaikan responsivitas viewport 360px dan desktop.
- Selesaikan keyboard/focus/contrast minimum.
- Jalankan pytest, Vitest, dan satu Playwright flow.
- Verifikasi performa 3s/1s/5s.
- Audit seluruh label sumber, asumsi, synthetic, dan unverified.

### Fase 7 — Freeze dan rehearsal, 25–26 November

- Feature freeze pada 25 November.
- Build bersih dari lockfile pada laptop demo.
- Rehearsal demo, pitching, dan tanya jawab.
- Siapkan backup bundle, build, video, slide, dan salinan offline dependency bila diperbolehkan.
- Simulasikan internet putus dan restart aplikasi.
- Catat baseline sebelum HackDay untuk transparansi kepatuhan.

### Fase 8 — HackDay dan final, 27–28 November

- Ikuti aturan panitia yang tersedia dan catat perubahan selama HackDay.
- Fokus pada perbaikan blocker, integrasi, bukti test, dan kualitas demo.
- Hindari fitur baru setelah alur utama stabil.
- Pada 28 November, jalankan pitch/exhibition dari build yang telah di-smoke-test.

## 5. Work breakdown structure

| WBS | Work package | Primary output |
| --- | --- | --- |
| 1.0 | Governance dan compliance | Scope, keputusan, aturan kompetisi, approval |
| 2.0 | Data acquisition/provenance | Raw, manifest, checksum, coverage status |
| 3.0 | Data pipeline | Processed data, quality report, runtime bundle |
| 4.0 | Forecasting | Benchmark, selected model, metrics, forecast |
| 5.0 | Optimization | Formulation, solver, reason codes, golden scenarios |
| 6.0 | Backend/runtime | Schemas, loader, interfaces, startup |
| 7.0 | Frontend/UX | Dashboard responsive dan accessible |
| 8.0 | Verification | Unit, contract, E2E, performance, offline smoke |
| 9.0 | Business/pitch | Narrative, slides, exhibition, Q&A |
| 10.0 | Release/demo | Build, backup, launcher, rehearsal |

## 6. RACI legend

- **R** — Responsible: mengerjakan.
- **A** — Accountable: satu pemilik hasil/keputusan.
- **C** — Consulted: memberi masukan sebelum keputusan.
- **I** — Informed: menerima perkembangan/hasil.

## 7. RACI matrix

| Workstream/deliverable | Ismael | Yolanda | Zaky | Rafa | Silvana | Yelsa |
| --- | --- | --- | --- | --- | --- | --- |
| Tata kelola, scope, approval | A/R | C | C | I | I | C |
| Validasi domain pangan | C | A/R | I | C | C | I |
| Data provenance dan quality gate | C | C | C | A/R | I | I |
| Artikel/model benchmark | C | C | C | A/R | I | I |
| Arsitektur dan integration contract | C | I | A/R | C | C | I |
| Forecast pipeline | C | C | C | A/R | I | I |
| Synthetic data dan optimizer | C | C | C | A/R | I | I |
| Frontend dan accessibility | I | C | C | I | A/R | I |
| UAT dan rehearsal pengguna | C | C | R | C | A/R | I |
| Test integrasi dan demo lokal | I | I | A/R | R | R | I |
| Compliance aturan kompetisi | A | I | C | I | I | R |
| Bisnis, pitch, exhibition | C | C | C | I | C | A/R |
| Persetujuan final deliverable | A/R | C | C | C | C | C |

## 8. Dependency and critical path

```text
Verifikasi data → pipeline → benchmark → forecast artifact ┐
                                                           ├→ runtime bundle → backend/UI integration → test → demo
Synthetic scenario → optimizer + golden tests ─────────────┘
```

Critical path adalah data gate, runtime bundle, optimizer contract, integrasi frontend/backend, lalu rehearsal. Peta dan fitur stretch tidak boleh mengambil kapasitas dari jalur ini.

## 9. Risk method

Probability dan impact dinilai Low/Medium/High. Level High bila salah satunya High dan yang lain minimal Medium, atau keduanya High. Owner memonitor trigger pada review harian fase aktif.

## 10. Risk register

| ID | Risiko | P | I | Level | Owner | Trigger | Mitigasi | Contingency |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R-01 | Wilayah PIHPS tidak terverifikasi | H | H | High | Rafa | Tidak ada bukti filter/re-export | Verifikasi/re-export; label coverage | Demo sebagai data unverified; batasi klaim |
| R-02 | Pipeline terpadu terlambat | H | H | High | Rafa | Bundle belum terbentuk 9 Nov | Prioritaskan P0; buang BMKG | Gunakan bundle fixture tervalidasi |
| R-03 | Aturan pra-HackDay tidak jelas | M | H | High | Yelsa | Tidak ada jawaban panitia | Minta klarifikasi tertulis | Transparan soal baseline dan log perubahan |
| R-04 | Ketersediaan anggota tidak diketahui | H | H | High | Ismael | PIC tidak konfirmasi jadwal | Konfirmasi dan backup owner | Kurangi scope ke critical path |
| R-05 | Scope creep | H | H | High | Ismael | Fitur baru setelah scope freeze | Change control satu-in-satu | Tolak/pindah ke backlog pasca-MVP |
| R-06 | XGBoost kalah/tidak eligible | M | M | Medium | Rafa | Gate/benchmark gagal | Baseline adalah kandidat sah | Pakai naive/MA terbaik dan laporkan jujur |
| R-07 | Data sintetis dianggap aktual | M | H | High | Yolanda | Label/asumsi tidak terlihat | Label permanen dan review domain | Hentikan klaim; jelaskan saat pitch |
| R-08 | Solver gagal/timeout | M | H | High | Zaky/Rafa | >5 detik atau status error | Problem kecil, golden tests, time limit | Gunakan skenario cadangan yang tervalidasi |
| R-09 | Dependency/build gagal saat demo | M | H | High | Zaky | Clean build/startup gagal | Lockfile, launcher check, rehearsal | Gunakan build dan environment backup |
| R-10 | UI mobile/accessibility terlambat | M | M | Medium | Silvana | P0 belum lulus 24 Nov | Mobile-first, komponen minimum | Pertahankan fungsi; hapus stretch map |
| R-11 | Internet tidak tersedia | M | M | Medium | Zaky | Jaringan venue gagal | Semua aset dan data lokal | Demo offline/video backup |
| R-12 | Artikel domain belum terkumpul | M | L | Medium | Rafa | Tidak ada sumber sebelum baseline doc | Keyword dan PIC sudah dicatat | Gunakan evidence note awal; tandai pending |
| R-13 | Klaim hasil melebihi kualitas data | M | H | High | Ismael | Pitch menyebut permintaan aktual/keputusan resmi | Review narasi dan disclaimer | Koreksi slide/demo sebelum tampil |
| R-14 | Bundle/data antarversi tidak sinkron | M | H | High | Zaky | Hash/schema mismatch | Single atomic bundle + validation | Fail-fast dan rollback bundle sebelumnya |

## 11. Governance cadence

- Review harian singkat selama 4–10 dan 17–28 November: selesai, blocker, keputusan, risiko.
- Owner workstream memperbarui status dan evidence.
- Keputusan scope/claim disetujui Ismael.
- Keputusan arsitektur/integrasi dipimpin Zaky dengan konsultasi Rafa/Silvana.
- Defect blocker demo diprioritaskan di atas fitur baru.

## 12. Change control

Permintaan perubahan setelah scope freeze harus menyebut:

1. requirement atau risiko yang ditangani;
2. owner dan estimasi;
3. item scope yang diganti/dihapus; dan
4. persetujuan Ismael.

Perubahan klaim data/AI juga membutuhkan review Rafa dan Ismael. Perubahan alur pengguna membutuhkan review Silvana.

## 13. Definition of done per deliverable

Deliverable selesai ketika:

- requirement terkait terpenuhi;
- test/evidence proporsional tersedia;
- sumber, asumsi, dan limitation terdokumentasi;
- tidak menambah dependency/runtime yang tidak disetujui;
- owner melakukan review; dan
- approver yang ditetapkan menerima hasil pada gate terkait.

## 14. Keputusan terbuka

| Keputusan | Owner | Due | Dampak bila tertunda |
| --- | --- | --- | --- |
| Bukti cakupan wilayah PIHPS | Rafa | 6 Nov | Klaim Sumbar harus ditahan |
| Aturan pekerjaan pra-HackDay | Yelsa | Sebelum 10 Nov | Risiko compliance/transparansi |
| Ketersediaan seluruh anggota | Ismael | 6 Nov | RACI/estimasi perlu disesuaikan |
| Artikel domain tambahan | Rafa/tim | Sebelum dokumen 04 baseline | Justifikasi domain tetap pending |

## 15. Persetujuan

Setiap owner workstream meninjau bagian terkait. Ismael menyetujui roadmap, perubahan scope, dan penerimaan final.
