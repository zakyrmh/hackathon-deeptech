# Alternatif Resmi Mendapatkan Data BMKG

Tanggal verifikasi: **3 November 2026**

## Ringkasan keputusan

Untuk proyek ini, jalur paling tepat adalah:

1. pertahankan XLSX bulanan yang sudah diperoleh sebagai data observasi historis awal;
2. ajukan **data observasi harian** untuk stasiun dan periode yang dibutuhkan melalui **PTSP BMKG** atau UPT BMKG Sumatera Barat;
3. gunakan **API Prakiraan Cuaca Terbuka BMKG** hanya untuk fitur ke depan, bukan untuk mengganti histori observasi;
4. hindari mengambil endpoint internal portal secara otomatis karena BMKG sudah menyediakan jalur API/kerja sama resmi untuk akses terprogram.

Tidak ditemukan API publik resmi yang terdokumentasi untuk mengunduh bebas seluruh histori observasi stasiun seperti isi Data Online. API publik terbuka yang dokumentasinya jelas saat ini terutama menyediakan **prakiraan**, bukan arsip observasi historis.

## Mengapa Data Online membatasi unduhan

FAQ resmi Data Online menyatakan bahwa data bulanan hanya dapat diakses untuk **dua tahun terakhir**, dengan **kuota awal 24 bulan**; setelah kuota habis, pengguna harus menunggu **30 hari** untuk dapat mengunduh lagi. Portal utama juga menyatakan data yang tersedia di Data Online adalah data level 2 beresolusi bulanan, sedangkan permintaan resolusi yang lebih kecil dari bulanan diarahkan ke PTSP BMKG. Sumber: [FAQ Data Online BMKG](https://dataonline.bmkg.go.id/faq) dan [halaman utama Data Online](https://dataonline.bmkg.go.id/dataonline-home).

Artinya, keterbatasan yang dialami pengguna merupakan kebijakan portal, bukan kesalahan pada file atau akun proyek.

## Pilihan resmi

### 1. PTSP BMKG — pilihan utama untuk data historis harian

Gunakan [PTSP BMKG](https://ptsp.bmkg.go.id/) untuk meminta data pada resolusi harian atau kebutuhan khusus. Pemberitahuan resmi Data Online secara eksplisit mengarahkan permintaan data beresolusi lebih kecil dari bulanan ke PTSP. Standar pelayanan BMKG menjelaskan pola pengajuan melalui akun PTSP, pemilihan produk pada katalog, unggah surat permohonan, proses tarif/e-billing bila berlaku, lalu unduh hasil. Sumber: [Data Online BMKG](https://dataonline.bmkg.go.id/dataonline-home) dan [Standar Pelayanan dan Jasa MKG melalui PTSP 2026](https://jdih.bmkg.go.id/storage/common/dokumen/KEP.1_SU_I_2026%20TTG%20STANDAR%20PELAYANAN%20DAN%20JASA%20MKG%20MELALUI%20PTSP.pdf).

Permintaan yang disarankan untuk hackathon:

- stasiun: WMO 96165 Padang Panjang, WMO 96161 Teluk Bayur, dan bila tersedia Stasiun Klimatologi Sumatera Barat;
- periode: samakan dengan histori harga PIHPS, misalnya 25 Oktober 2024–2 November 2026;
- resolusi: harian;
- parameter: curah hujan, temperatur rata-rata/minimum/maksimum, kelembapan rata-rata, kecepatan angin rata-rata/maksimum, dan lama penyinaran;
- tujuan: pendidikan/riset nonkomersial untuk hackathon dan pengembangan prototipe.

Tarif nol rupiah dapat berlaku untuk kategori kegiatan tertentu, termasuk pendidikan dan penelitian nonkomersial, tetapi tetap memerlukan persyaratan dan persetujuan BMKG; jangan menganggap otomatis gratis. Contoh prosedur resmi UPT BMKG mencantumkan surat pengantar penelitian, surat pernyataan, surat permohonan tarif nol rupiah, proposal, dan identitas pemohon. Sumber: [layanan permintaan data UPT BMKG](https://staklim-lampung.bmkg.go.id/form-data.php) dan [Peraturan BMKG Nomor 12 Tahun 2019 melalui halaman layanan BMKG](https://staklim-aceh.bmkg.go.id/permintaan-data/).

### 2. Hubungi UPT BMKG Sumatera Barat

Daftar resmi PPID BMKG mencantumkan lima UPT di Sumatera Barat. Kontak yang paling relevan untuk proyek ini:

- **Stasiun Klimatologi Kelas II Sumatera Barat** — `staklim.sumbar@bmkg.go.id`, telepon `(0751) 676848` / `(0751) 675100`;
- **Stasiun Geofisika Kelas I Padang Panjang** — `stageof.padangpanjang@bmkg.go.id`, telepon `(0752) 484236` / `(0752) 82236`;
- **Stasiun Meteorologi Maritim Kelas III Teluk Bayur** — `stamar.tlb@bmkg.go.id`;
- **Stasiun Meteorologi Kelas II Minangkabau** — `stamet.minangkabau@bmkg.go.id`, telepon `(0751) 819105`.

Sumber kontak: [Daftar Balai/UPT PPID BMKG](https://ppid.bmkg.go.id/profil/balai-upt).

Kirim surat singkat yang menyebutkan parameter, resolusi, periode, stasiun, format yang diinginkan, dan tujuan penggunaan. Tanyakan apakah permohonan harus diteruskan melalui PTSP pusat atau dapat dilayani UPT.

### 3. API Prakiraan Cuaca Terbuka — untuk variabel masa depan

[API Prakiraan Cuaca Terbuka BMKG](https://data.bmkg.go.id/prakiraan-cuaca/) menyediakan prakiraan tingkat kelurahan/desa untuk tiga hari, delapan titik waktu per hari (setiap tiga jam), diperbarui dua kali sehari dalam JSON. Batas akses yang didokumentasikan adalah 60 permintaan per menit per IP dan atribusi BMKG wajib ditampilkan.

Contoh endpoint resmi:

```text
https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4={kode_wilayah_tingkat_iv}
```

Data ini cocok untuk fitur cuaca ke depan pada forecast harga 1–3 hari, tetapi **bukan histori observasi** dan tidak dapat digunakan untuk mengisi ulang data iklim stasiun yang hilang. Contoh pemrosesan resmi tersedia pada [repositori GitHub BMKG](https://github.com/infoBMKG/data-cuaca).

### 4. API AWS Center BMKG — observasi otomatis, tetapi memerlukan token

Dokumentasi resmi [API Pertukaran Data AWS Center](https://apiaws.bmkg.go.id/) menyebut akses data AWS dalam JSON melalui endpoint `getdata`, dengan parameter token, filter, tanggal mulai, dan tanggal selesai. Token diperoleh melalui proses permintaan/login. Parameter dapat mencakup curah hujan, temperatur, kelembapan, dan tekanan sesuai alat.

Opsi ini layak ditanyakan kepada BMKG bila tim membutuhkan data observasi otomatis. Namun, jangan menganggap token tersedia bebas atau bahwa semua stasiun/periode historis tercakup. Konfirmasi cakupan, hak akses, rate limit, dan izin penggunaan langsung kepada BMKG sebelum menjadikannya ketergantungan pipeline.

### 5. Satu Peta MKG — data API real-time, cakupan perlu diverifikasi

[Portal Data API Satu Peta MKG](https://gis.bmkg.go.id/portal/dataapi) menyatakan menyediakan data real-time meteorologi, klimatologi, dan geofisika seperti suhu, curah hujan, arah angin, dan aktivitas seismik. Portal ini dapat menjadi sumber tambahan untuk monitoring atau prototipe.

Dokumentasi publik yang terindeks belum cukup untuk memastikan ketersediaan histori stasiun, mekanisme autentikasi, dan batas akses bagi kebutuhan proyek ini. Perlakukan sebagai kandidat yang perlu diuji/ditanyakan, bukan pengganti pasti Data Online.

### 6. Produk analisis dan prediksi iklim publik — fitur kategori atau validasi

BMKG menerbitkan [analisis curah dan sifat hujan bulanan](https://www.bmkg.go.id/iklim/analisis-hujan) dan dashboard monitoring/prediksi regional. Produk ini berguna untuk validasi pola musim atau fitur kategori wilayah ketika observasi stasiun terbatas.

Untuk Data Variabilitas Iklim, BMKG menyatakan akses data real-time penuh terbatas bagi lembaga/organisasi yang memiliki kerja sama resmi, serta mengimbau agar nilai numerik tidak ditampilkan ulang secara langsung dan lebih memilih kelas kategori. Sumber: [Akses Data Variabilitas Iklim BMKG](https://iklim.bmkg.go.id/id/clivardb/). Karena itu, jangan melakukan ekstraksi massal dari dashboard atau menganggap visualisasi sebagai dataset numerik bebas.

## Yang tidak disarankan

- Jangan mengotomasi endpoint internal yang ditemukan dari DevTools bila endpoint itu tidak didokumentasikan sebagai API publik.
- Jangan menyamakan prakiraan 3 hari dengan observasi historis.
- Jangan mengisi `-` atau `9999` menjadi nol; keduanya menandakan data tidak tersedia/tidak dilakukan pengukuran pada ekspor BMKG yang ada.
- Jangan menggabungkan stasiun berbeda tanpa mempertahankan `station_id`, koordinat, elevasi, dan flag sumber.
- Jangan menggunakan dataset cuaca pihak ketiga dengan label “BMKG” kecuali provenance-nya benar-benar dapat dibuktikan.

## Rekomendasi praktis untuk hackathon

Jika PTSP belum memberikan data sebelum tenggat:

1. gunakan XLSX bulanan yang sudah tersedia sebagai fitur iklim bulanan;
2. gunakan API Prakiraan Cuaca Terbuka untuk fitur masa depan tiga hari;
3. tandai seluruh bulan/stasiun yang kosong dengan missing flag, tanpa imputasi diam-diam;
4. batasi klaim model: cuaca bulanan adalah konteks musiman, bukan pemicu harian;
5. dokumentasikan permohonan PTSP sebagai rencana peningkatan data setelah hackathon.

Pendekatan ini mempertahankan sumber resmi BMKG dan menghindari klaim bahwa proyek memiliki histori harian yang sebenarnya belum tersedia.
