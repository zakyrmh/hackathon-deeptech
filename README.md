# Food Demand Intelligence

MVP sistem pendukung keputusan untuk membaca forecast harga pangan, estimasi surplus-defisit, dan rekomendasi skenario distribusi antardaerah. Sistem dirancang sebagai demo lokal dan offline untuk tiga komoditas serta lima wilayah pilot di Sumatera Barat.

> Rekomendasi adalah bahan tinjauan manusia, bukan keputusan atau instruksi distribusi resmi. Data stok, usia simpan, rute, biaya, dan kapasitas pada MVP bersifat sintetis.

## Status

Repository saat ini berada pada tahap persiapan dan spesifikasi SDLC. Implementasi aplikasi, benchmark model, test execution, dan UAT belum selesai.

Milestone utama:

- 10 November 2026 — batas pengumpulan prototyping;
- 13 November 2026 — pengumuman seleksi tahap prototyping;
- 16 November 2026 — bootcamp MVP daring;
- 27 November 2026 — HackDay 24 Hours;
- 28 November 2026 — pitching, exhibition, dan awarding.

## Dokumentasi

- [Daftar dokumen SDLC](docs/sdlc/SDLC_DOCUMENT_CHECKLIST.md)
- [Project Charter](docs/sdlc/00_Project_Charter.md)
- [Product Requirements](docs/sdlc/02_PRD.md)
- [Software Requirements](docs/sdlc/03_SRS.md)
- [Data and AI Specification](docs/sdlc/04_Data_and_AI_Specification.md)
- [Software Architecture](docs/sdlc/05_Software_Architecture.md)
- [Test Plan and Traceability](docs/sdlc/08_Test_Plan_and_Traceability.md)
- [Model Card and Evaluation Report](docs/sdlc/11_Model_Card_and_Evaluation_Report.md)
- [Domain glossary](CONTEXT.md)
- [Architecture decisions](docs/adr/)
- [Research notes](docs/research/)
- [Dataset guide](docs/data/DATASET_GUIDE.md)

## Struktur repository

```text
.
├── data/                 # raw public data, manifest, checksums, pipeline script
├── docs/
│   ├── adr/              # architecture decision records
│   ├── data/             # human-readable dataset guidance
│   ├── reports/          # project/data status reports
│   ├── research/         # research notes and evidence
│   ├── sdlc/             # documents 00–11 and SDLC checklist
│   └── private/          # local proposal source; ignored by Git
├── AGENTS.md             # project instructions for coding agents
├── CONTEXT.md            # domain glossary
└── README.md
```

## Data

Raw data yang disertakan berasal dari sumber publik BPS, PIHPS Bank Indonesia, dan BMKG. Provenance dan keterbatasan dicatat pada [data/README.md](data/README.md), [data/MANIFEST.csv](data/MANIFEST.csv), dan [data/raw/SUMBER_DATA_RAW.md](data/raw/SUMBER_DATA_RAW.md).

Verifikasi checksum:

```bash
cd data
sha256sum --check CHECKSUMS.sha256
```

File PIHPS belum menyimpan bukti filter wilayah yang digunakan saat ekspor. Jangan mengklaim seri tersebut sebagai representasi Sumatera Barat sebelum cakupannya diverifikasi.

## Target stack MVP

- React, TypeScript, Vite, Tailwind CSS, dan Recharts;
- FastAPI dan Pydantic;
- pandas, scikit-learn, XGBoost, dan SciPy HiGHS;
- satu `runtime_bundle.json` read-only;
- satu proses lokal pada `127.0.0.1:8000`.

Stack masih mengikuti ADR berstatus proposed dan menunggu persetujuan tim.

## Privasi repository

Proposal asli, foto, dan nomor identitas anggota disimpan lokal di `docs/private/` dan dikecualikan melalui `.gitignore`. Periksa kembali `git status` sebelum push agar tidak ada data pribadi, secret, log, atau artefak lokal yang ikut terunggah.

