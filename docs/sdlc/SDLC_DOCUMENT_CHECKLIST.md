# SDLC Document Checklist — Food Demand Intelligence

Dokumen ini adalah daftar persiapan pengembangan software yang disesuaikan untuk MVP Hackathon 24 jam. Artefak digabung agar tetap mencakup kebutuhan SDLC tanpa menghasilkan dokumentasi berlebihan.

Status:

- `Siap Ditinjau Tim`: isi awal sudah tersedia dan menunggu review tim.
- `Belum dibuat`: belum disusun sebagai dokumen tersendiri.
- `Sebagian tersedia`: bahan sumber tersedia, tetapi belum menjadi dokumen SDLC yang lengkap.

## Dokumen inti

| No. | Dokumen | Cakupan | Prioritas | Status |
| --- | --- | --- | --- | --- |
| 00 | `00_Project_Charter.md` | Latar belakang, tujuan, scope, deliverable, milestone, tim, constraint, risiko, dan kriteria sukses | P0 | Siap Ditinjau Tim v0.2 |
| 01 | `01_Stakeholders_and_ConOps.md` | Stakeholder, aktor, batas sistem, alur operasi, data, kondisi gagal, dan skenario demo | P0 | Siap Ditinjau Tim v0.2 |
| 02 | `02_PRD.md` | Masalah pengguna, persona, outcome, fitur, prioritas, user journey, dan acceptance criteria produk | P0 | Siap Ditinjau Tim v0.2 |
| 03 | `03_SRS.md` | Functional requirements, non-functional requirements, business rules, antarmuka, constraint, dan requirement ID | P0 | Siap Ditinjau Tim v0.2 |
| 04 | `04_Data_and_AI_Specification.md` | Sumber dan skema data, provenance, kualitas data, target forecast, feature engineering, baseline, evaluasi, asumsi, dan batas AI | P0 | Siap Ditinjau Tim v0.2 |
| 05 | `05_Software_Architecture.md` | Konteks sistem, komponen, aliran data, deployment lokal, keputusan teknologi, dan quality scenarios | P0 | Siap Ditinjau Tim v0.2 |
| 06 | `06_Detailed_Design_API_and_Data_Model.md` | Kontrak modul/API, model data, optimizer, error states, dan integrasi frontend-backend | P1 | Siap Ditinjau Tim v0.2 |
| 07 | `07_Project_Roadmap_RACI_and_Risks.md` | WBS, roadmap sampai pitching, pembagian kerja, dependency, risk register, dan mitigasi | P0 | Siap Ditinjau Tim v0.2 |
| 08 | `08_Test_Plan_and_Traceability.md` | Strategi test, test case, test data, acceptance test, RTM, hasil test, dan defect log | P0 | Siap Ditinjau Tim v0.2; eksekusi pending |
| 09 | `09_Deployment_and_Operations.md` | Setup lokal, build/run, konfigurasi, smoke test, logging, troubleshooting, backup demo, dan rollback | P1 | Siap Ditinjau Tim v0.2; command pending implementasi |
| 10 | `10_User_Guide_and_UAT.md` | Panduan demo/operator, skenario UAT, kuesioner, hasil validasi, dan persetujuan pengguna | P1 | Siap Ditinjau Tim v0.2; UAT pending |
| 11 | `11_Model_Card_and_Evaluation_Report.md` | Identitas model, dataset, metrik, hasil benchmark, limitation, ethical use, serta monitoring lanjutan | P1 | Siap Ditinjau Tim v0.2; benchmark pending |

## Artefak pendukung

| Artefak | Fungsi | Status |
| --- | --- | --- |
| `../../CONTEXT.md` | Glossary istilah domain | Tersedia |
| `../adr/` | Keputusan arsitektur yang sulit dibalik dan memiliki trade-off nyata | Dibuat hanya jika diperlukan |
| `../private/proposal/Proposal_PLAYIT_FoodDemandIntelligence_referensi_terbaru.md` | Sumber lokal privat; memuat identitas/foto dan tidak ikut Git | Tersedia lokal, diabaikan Git |
| `../data/DATASET_GUIDE.md` | Sumber dan panduan awal dataset | Tersedia |
| `../reports/LAPORAN_SINGKAT_2026-11-03.md` | Status dan temuan dataset | Tersedia |

## Urutan pengerjaan yang disarankan

1. `02_PRD.md`
2. `03_SRS.md`
3. `04_Data_and_AI_Specification.md`
4. `05_Software_Architecture.md`
5. `07_Project_Roadmap_RACI_and_Risks.md`
6. `08_Test_Plan_and_Traceability.md`
7. `06_Detailed_Design_API_and_Data_Model.md`
8. `09_Deployment_and_Operations.md`
9. `10_User_Guide_and_UAT.md`
10. `11_Model_Card_and_Evaluation_Report.md`

Untuk prototyping tanggal 10 November, minimum yang perlu matang adalah dokumen 00–05 serta bagian pembagian kerja dari dokumen 07. Dokumen 08–11 dapat diselesaikan bertahap menjelang HackDay dan pitching.
