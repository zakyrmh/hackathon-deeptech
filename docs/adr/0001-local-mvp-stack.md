# ADR-0001: Stack MVP Lokal Satu Proses

- Status: Proposed for team review
- Date: 2026-11-04
- Decision owner: Zaky Ramadhan
- Approver: Ismael

## Context

Proposal awal menyebut Next.js, FastAPI, PostgreSQL/Supabase, dan PuLP/SciPy. Requirement final adalah dashboard lokal satu halaman, tanpa login atau persistensi, dengan pipeline AI offline dan optimizer runtime. MVP harus responsif, dapat berjalan tanpa internet, dan selesai dalam HackDay 24 jam.

## Decision

Gunakan React/TypeScript/Vite untuk frontend, FastAPI/Pydantic untuk backend yang juga menyajikan build frontend, SciPy HiGHS untuk optimizer, dan satu JSON tervalidasi untuk storage runtime. Jalankan melalui satu proses lokal pada `127.0.0.1`. Jangan gunakan database, Next.js, Supabase, Docker, atau PuLP/CBC pada MVP.

## Alternatives

### Next.js + FastAPI

Ditolak untuk MVP karena dashboard tidak membutuhkan SSR atau server routing Next.js. Optimizer Python tetap memerlukan backend, sehingga Next.js menambah runtime tanpa menghilangkan FastAPI.

### Streamlit

Ditolak karena kontrol atas layout pitching, responsivitas, state, dan aksesibilitas lebih terbatas dibanding React.

### PostgreSQL/Supabase

Ditolak karena tidak ada write, histori, auth, upload, multiuser, atau audit pada MVP.

### PuLP + CBC

Ditolak karena menambah dependency solver eksternal, sedangkan problem linear MVP dapat diselesaikan melalui SciPy HiGHS.

## Consequences

Positif:

- satu proses runtime dan satu origin;
- UI tetap fleksibel dan Python tetap menangani optimasi;
- tidak ada koneksi database atau cloud yang dapat gagal saat demo; dan
- interface runtime kecil serta mudah diuji.

Negatif:

- membutuhkan build Node sebelum FastAPI dijalankan;
- data tidak dapat diperbarui atau disimpan dari UI; dan
- fitur pilot seperti auth, histori, serta upload memerlukan evolusi arsitektur.

## Revisit triggers

Tinjau ulang saat ada kebutuhan menyimpan skenario, upload data, multiuser, audit/approval, deployment publik, atau integrasi sumber data produksi.
