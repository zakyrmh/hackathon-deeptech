# Software Requirements Specification — Food Demand Intelligence

| Atribut | Nilai |
| --- | --- |
| Status | Siap Ditinjau Tim v0.2 |
| Tanggal | 4 November 2026 |
| Fase | MVP HackDay 24 jam |
| Approver | Ismael |
| Referensi | `00_Project_Charter.md`, `01_Stakeholders_and_ConOps.md`, `02_PRD.md`, `../../CONTEXT.md` |

## 1. Tujuan dan ruang lingkup

Dokumen ini menetapkan requirement software yang dapat diuji untuk MVP Food Demand Intelligence. Sistem adalah dashboard lokal tanpa login yang menampilkan forecast harga tujuh hari, estimasi neraca wilayah, simulasi anggaran/kapasitas, dan rekomendasi alokasi antardaerah.

Sistem tidak memprediksi permintaan harian aktual, tidak mengeksekusi distribusi, dan tidak digunakan sebagai keputusan resmi.

## 2. Konvensi requirement

| Prefix | Jenis |
| --- | --- |
| `FR` | Functional requirement |
| `DR` | Data requirement |
| `UIR` | User-interface requirement |
| `IR` | Interface requirement |
| `NFR` | Non-functional requirement |
| `BR` | Business rule |

Kata **harus** menunjukkan requirement wajib MVP. Semua requirement wajib dapat ditelusuri ke kebutuhan produk atau aturan domain.

## 3. Aktor dan lingkungan operasi

### 3.1 Aktor

Satu-satunya aktor langsung adalah Analis Distribusi Pangan. Pejabat penanggung jawab menerima hasil di luar sistem dan tidak memiliki akun atau antarmuka tersendiri.

### 3.2 Lingkungan

- Aplikasi berjalan pada laptop tim dan diakses melalui browser.
- Runtime utama harus berfungsi tanpa koneksi internet.
- Aplikasi hanya mendengarkan pada `localhost`.
- Runtime menggunakan data publik yang telah diproses dan data operasional sintetis.
- Forecast telah dibuat dan divalidasi sebelum demo; optimizer berjalan saat diminta pengguna.

## 4. Functional requirements

### 4.1 Startup dan kondisi awal

| ID | Requirement |
| --- | --- |
| FR-001 | Saat dashboard dibuka, sistem harus memeriksa kesehatan layanan analisis. |
| FR-002 | Sistem harus memuat metadata, forecast, neraca, dan parameter default dari paket data runtime lokal. |
| FR-003 | Komoditas default harus `cabai merah keriting`. |
| FR-004 | Anggaran dan kapasitas default harus berasal dari skenario demo tervalidasi yang feasible. |
| FR-005 | Forecast dan kondisi awal harus tampil tanpa menjalankan optimizer. |

### 4.2 Pemilihan komoditas

| ID | Requirement |
| --- | --- |
| FR-010 | Pengguna harus dapat memilih bawang merah, cabai merah keriting, atau cabai rawit merah. |
| FR-011 | Saat komoditas berubah, sistem harus memperbarui forecast, label tekanan pasar, dan neraca wilayah. |
| FR-012 | Saat komoditas berubah, sistem harus mengembalikan anggaran dan kapasitas ke nilai default komoditas tersebut. |
| FR-013 | Saat komoditas berubah, sistem harus menghapus hasil optimizer sebelumnya. |

### 4.3 Forecast harga dan tekanan pasar

| ID | Requirement |
| --- | --- |
| FR-020 | Sistem harus menampilkan harga aktual terakhir dalam Rp/kg. |
| FR-021 | Sistem harus menampilkan tujuh nilai forecast harga harian dalam Rp/kg. |
| FR-022 | Tujuh tanggal forecast harus merupakan tujuh hari kalender berturut-turut setelah observasi harga terakhir. |
| FR-023 | Sistem harus menghitung persentase perubahan forecast hari ke-7 terhadap harga aktual terakhir. |
| FR-024 | Sistem harus menampilkan label tekanan pasar berdasarkan BR-001. |
| FR-025 | Sistem harus menyatakan bahwa label tekanan pasar menggunakan ambang demo, bukan ambang resmi pemerintah. |

### 4.4 Neraca wilayah

| ID | Requirement |
| --- | --- |
| FR-030 | Sistem harus menampilkan neraca untuk Kabupaten Solok, Agam, Tanah Datar, Kota Padang, dan Bukittinggi. |
| FR-031 | Sistem harus menghitung neraca wilayah sesuai BR-002. |
| FR-032 | Sistem harus memberi label estimasi surplus pada nilai positif dan estimasi defisit pada nilai negatif. |
| FR-033 | Sistem harus menyatakan bahwa neraca merupakan estimasi/skenario, bukan status operasional resmi. |

### 4.5 Input skenario

| ID | Requirement |
| --- | --- |
| FR-040 | Pengguna harus dapat mengubah total anggaran distribusi dalam Rupiah. |
| FR-041 | Pengguna harus dapat mengubah total kapasitas angkut dalam kilogram. |
| FR-042 | Anggaran harus berupa bilangan bulat dengan nilai minimum `0` dan maksimum dari konfigurasi skenario. |
| FR-043 | Kapasitas harus berupa bilangan bulat dengan nilai minimum `1` dan maksimum dari konfigurasi skenario. |
| FR-044 | Sistem harus menampilkan error inline untuk nilai kosong, negatif, desimal, atau melebihi maksimum. |
| FR-045 | Tombol `Jalankan Skenario` harus nonaktif selama input tidak valid. |

### 4.6 Eksekusi optimizer

| ID | Requirement |
| --- | --- |
| FR-050 | Optimizer hanya boleh berjalan setelah pengguna menekan `Jalankan Skenario`. |
| FR-051 | Saat optimizer berjalan, sistem harus menampilkan indikator proses dan menonaktifkan tombol eksekusi. |
| FR-052 | Sistem harus mencegah pengiriman skenario ganda selama satu proses masih berjalan. |
| FR-053 | Sistem harus menghentikan atau menganggap gagal proses yang melebihi lima detik. |
| FR-054 | Saat timeout, sistem harus menghapus hasil lama, menampilkan pesan kegagalan, dan menyediakan aksi `Coba Lagi`. |
| FR-055 | Optimizer harus menerapkan seluruh constraint pada BR-003. |
| FR-056 | Optimizer harus menerapkan urutan tujuan pada BR-004. |
| FR-057 | Input dan dataset yang sama harus menghasilkan rekomendasi dan urutan yang sama. |
| FR-058 | Solusi yang tetap setara harus diurutkan berdasarkan kode asal, kode tujuan, lalu kode komoditas secara alfabetis. |

### 4.7 Hasil optimizer

| ID | Requirement |
| --- | --- |
| FR-060 | Hasil bisnis optimizer harus berstatus `feasible` atau `infeasible`. |
| FR-061 | Status `feasible` harus menampilkan rekomendasi yang memenuhi seluruh constraint, walaupun masih terdapat sisa defisit. |
| FR-062 | Setiap rekomendasi harus memuat peringkat, asal, tujuan, komoditas, jumlah kg, estimasi biaya, status FEFO, dan sisa defisit. |
| FR-063 | Jika tidak ada defisit, sistem harus mengembalikan `feasible`, daftar kosong, reason code `no_intervention_needed`, dan pesan `Tidak diperlukan intervensi distribusi untuk skenario ini`. |
| FR-064 | Jika terdapat defisit tetapi constraint menghalangi seluruh pengiriman, sistem harus mengembalikan `feasible`, daftar kosong, reason code `constraints_block_intervention`, dan penjelasan batas yang menghalangi. |
| FR-065 | Status `infeasible` hanya digunakan ketika constraint model kontradiktif atau solver menyatakan model tidak feasible; hasil harus menampilkan alasan dan tidak memuat rekomendasi. |
| FR-066 | Hasil invalid, gagal, timeout, atau `infeasible` harus menghapus rekomendasi lama. |

### 4.8 Ringkasan dampak

| ID | Requirement |
| --- | --- |
| FR-070 | Setelah hasil `feasible`, sistem harus menampilkan total estimasi defisit sebelum dan sesudah dalam kg. |
| FR-071 | Sistem harus menampilkan persentase kebutuhan terpenuhi sebelum dan sesudah. |
| FR-072 | Sistem harus menampilkan stok berisiko susut sebelum dan sesudah dalam kg. |
| FR-073 | Sistem harus menampilkan estimasi biaya distribusi dalam Rupiah. |

### 4.9 Kegagalan dan fallback

| ID | Requirement |
| --- | --- |
| FR-080 | Jika layanan analisis tidak tersedia, sistem harus menampilkan banner `Layanan analisis tidak tersedia`. |
| FR-081 | Saat layanan analisis tidak tersedia, optimizer harus nonaktif dan sistem harus menyediakan aksi `Coba Lagi`. |
| FR-082 | Informasi statis dan provenance yang berhasil dimuat tetap boleh ditampilkan saat backend tidak tersedia. |
| FR-083 | Jika artefak forecast gagal dimuat, sistem harus menggunakan baseline yang telah disiapkan dan melabelinya secara jelas. |
| FR-084 | Sistem tidak boleh membuat nilai stok, biaya, kapasitas, atau forecast yang tidak tersedia. |

### 4.10 Reset dan persistensi

| ID | Requirement |
| --- | --- |
| FR-090 | MVP tidak boleh menyimpan parameter atau hasil skenario secara permanen. |
| FR-091 | Refresh halaman harus mengembalikan komoditas, parameter, dan hasil ke kondisi awal. |

## 5. Business rules

| ID | Aturan |
| --- | --- |
| BR-001 | Label tekanan pasar membandingkan forecast hari ke-7 dengan harga aktual terakhir: `Menurun` untuk `< -5%`; `Stabil` untuk `-5%` sampai `+5%`; `Waspada` untuk `> 5%` sampai `10%`; dan `Tinggi` untuk `> 10%`. |
| BR-002 | Neraca wilayah = `stok sintetis + estimasi pasokan - kebutuhan baseline`; nilai positif adalah estimasi surplus dan nilai negatif adalah estimasi defisit. |
| BR-003 | Alokasi harus tidak negatif; asal dan tujuan berbeda; pengiriman tidak melebihi surplus/stok tersedia; penerimaan tidak melebihi defisit; total kiriman tidak melebihi kapasitas; total biaya tidak melebihi anggaran; hanya rute dalam dataset yang boleh digunakan; dan batch mengikuti FEFO. |
| BR-004 | Optimizer memprioritaskan pengurangan defisit, kemudian stok terdekat kedaluwarsa, lalu biaya distribusi yang lebih rendah. |
| BR-005 | Semua komoditas mengikuti FEFO. Cabai merah keriting dan cabai rawit merah berprioritas tinggi jika sisa usia simpan kurang dari tiga hari. Bawang merah tidak memiliki ambang hari sampai tervalidasi. |
| BR-006 | Rekomendasi adalah bahan tinjauan manusia, bukan keputusan atau instruksi distribusi resmi. |

## 6. Data requirements

| ID | Requirement |
| --- | --- |
| DR-001 | Pipeline harus menghasilkan paket JSON tervalidasi untuk runtime dashboard. |
| DR-002 | Dashboard tidak boleh membaca data raw CSV secara langsung. |
| DR-003 | Paket runtime harus memuat versi dataset, waktu pembuatan, periode data, daftar sumber, dan penanda data sintetis. |
| DR-004 | Paket runtime harus memuat tiga komoditas dan lima wilayah pilot. |
| DR-005 | Paket runtime harus memuat harga aktual terakhir, tujuh nilai forecast, komponen neraca, parameter default, batas input, batch stok, rute, dan biaya. |
| DR-006 | Jika metadata wajib hilang, sistem harus menandai data tidak valid dan menonaktifkan optimizer. |
| DR-007 | Semua tanggal dan waktu harus menggunakan zona `Asia/Jakarta`. |
| DR-008 | Data pribadi dan data rahasia mitra tidak boleh dimasukkan ke paket runtime MVP. |

## 7. Interface requirements

### 7.1 User interface

| ID | Requirement |
| --- | --- |
| UIR-001 | Dashboard harus menggunakan satu halaman dengan urutan: status data, pemilih komoditas, forecast, neraca, input skenario, rekomendasi, dan dampak. |
| UIR-002 | Sumber, periode, pembaruan terakhir, asumsi, dan label sintetis harus terlihat tanpa membuka halaman lain atau tooltip. |
| UIR-003 | Status tidak boleh disampaikan melalui warna saja; harus ada teks atau ikon yang berlabel. |
| UIR-004 | UI harus menggunakan Bahasa Indonesia, Rupiah, kilogram, dan format tanggal Indonesia. |
| UIR-005 | Harga dan biaya ditampilkan sebagai Rupiah bulat, kuantitas sebagai kg bulat, dan persentase dengan satu angka desimal. |
| UIR-006 | Pembulatan hanya dilakukan saat menampilkan; perhitungan internal harus mempertahankan presisi sumbernya. |

### 7.2 Application interfaces

| ID | Requirement |
| --- | --- |
| IR-001 | Backend MVP hanya harus menyediakan fungsi pemeriksaan kesehatan, pengambilan data dashboard per komoditas, dan eksekusi skenario optimasi. |
| IR-002 | MVP tidak boleh menyediakan API CRUD atau endpoint administratif. |
| IR-003 | Kontrak optimizer harus menerima komoditas, anggaran, dan kapasitas, lalu mengembalikan status, reason code, rekomendasi/alasan, dan metrik dampak. |
| IR-004 | Bentuk payload dan path endpoint ditetapkan dalam dokumen desain, bukan SRS. |

## 8. Non-functional requirements

### 8.1 Performa

| ID | Requirement |
| --- | --- |
| NFR-PERF-001 | Pada laptop demo, dashboard harus siap digunakan maksimal tiga detik setelah dibuka. |
| NFR-PERF-002 | Pergantian komoditas harus memperbarui tampilan maksimal satu detik. |
| NFR-PERF-003 | Optimizer harus mengembalikan hasil atau timeout maksimal lima detik. |

### 8.2 Keamanan dan privasi

| ID | Requirement |
| --- | --- |
| NFR-SEC-001 | Aplikasi hanya boleh mendengarkan pada `localhost` untuk MVP. |
| NFR-SEC-002 | Aplikasi tidak boleh menyimpan secret atau kredensial. |
| NFR-SEC-003 | Aplikasi tidak boleh mengirim data atau telemetry keluar perangkat. |
| NFR-SEC-004 | Runtime tidak boleh memuat data pribadi atau rahasia mitra. |

### 8.3 Usability dan aksesibilitas

| ID | Requirement |
| --- | --- |
| NFR-UX-001 | Pengguna harus dapat menyelesaikan alur utama maksimal lima menit. |
| NFR-A11Y-001 | Semua kontrol harus dapat digunakan dengan keyboard. |
| NFR-A11Y-002 | Semua kontrol harus memiliki label dan indikator fokus yang terlihat. |
| NFR-A11Y-003 | Informasi status harus menggunakan teks/ikon selain warna. |
| NFR-A11Y-004 | Teks utama harus memenuhi rasio kontras minimal `4.5:1`. |

### 8.4 Responsivitas dan kompatibilitas

| ID | Requirement |
| --- | --- |
| NFR-RESP-001 | Fitur inti harus dapat digunakan pada viewport mulai 360px hingga desktop. |
| NFR-RESP-002 | Layout harus bertumpuk pada layar kecil; tabel boleh menjadi kartu atau scroll horizontal. |
| NFR-COMP-001 | Google Chrome dan Microsoft Edge berbasis Chromium terbaru pada desktop dan mobile adalah browser wajib. |
| NFR-COMP-002 | Firefox dan Safari bersifat best effort dan bukan gerbang penerimaan MVP. |

### 8.5 Reliabilitas dan portabilitas demo

| ID | Requirement |
| --- | --- |
| NFR-REL-001 | Input dan dataset identik harus menghasilkan hasil identik. |
| NFR-REL-002 | Alur utama harus berfungsi tanpa internet setelah dependensi dan artefak tersedia. |
| NFR-REL-003 | Kegagalan tidak boleh meninggalkan rekomendasi lama yang tampak sebagai hasil terbaru. |

## 9. Traceability ke PRD

| User story | Requirement utama |
| --- | --- |
| PRD-US-01 | DR-003, DR-006, UIR-002, UIR-003 |
| PRD-US-02 | FR-010–FR-013 |
| PRD-US-03 | FR-020–FR-025, BR-001 |
| PRD-US-04 | FR-030–FR-033, BR-002 |
| PRD-US-05 | FR-040–FR-045 |
| PRD-US-06 | FR-050–FR-066, BR-003, BR-004 |
| PRD-US-07 | FR-057, FR-058, FR-062, BR-005 |
| PRD-US-08 | FR-070–FR-073 |
| PRD-US-09 | FR-053, FR-054, FR-063–FR-066, FR-080–FR-084 |

## 10. Acceptance test minimum

1. Dashboard dapat dibuka secara lokal tanpa internet.
2. Metadata lengkap menampilkan kondisi awal cabai merah keriting.
3. Ketiga komoditas dapat dipilih dan mereset skenario dengan benar.
4. Label tekanan pasar benar pada setiap batas nilai BR-001.
5. Input invalid menampilkan error dan mencegah optimizer berjalan.
6. Skenario feasible memenuhi setiap constraint BR-003 dan selesai maksimal lima detik.
7. Skenario tanpa defisit menghasilkan `feasible` dengan reason code `no_intervention_needed` dan daftar kosong.
8. Skenario dengan defisit tetapi terhalang constraint menghasilkan `feasible` dengan reason code `constraints_block_intervention` dan daftar kosong.
9. Skenario infeasible menampilkan alasan tanpa rekomendasi lama.
10. Hasil deterministik untuk input dan dataset yang sama.
11. Alur utama dapat digunakan pada viewport 360px dan desktop Chromium.
12. Kontrol utama dapat dioperasikan dengan keyboard dan memiliki fokus terlihat.
13. Tidak ada request data/telemetry ke jaringan eksternal selama demo.

Test case rinci dan RTM requirement-ke-test disusun dalam `08_Test_Plan_and_Traceability.md`.

## 11. Detail yang ditunda ke desain

- framework dan pembagian komponen;
- path endpoint dan bentuk payload lengkap;
- skema JSON runtime;
- formulasi matematis, bobot, dan implementasi solver;
- struktur file dan proses build/run; serta
- gaya visual dan komponen UI.

## 12. Persetujuan

Seluruh anggota tim meninjau dokumen. Ismael memberikan persetujuan akhir sebelum status diubah menjadi baseline.

