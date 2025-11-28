# BPS Jakarta Data - Pola Konsumsi & Potensi Kelurahan 2024

Dataset ini berisi data terstruktur dari dokumen BPS Jakarta:
- **Pola Konsumsi Penduduk Provinsi DKI Jakarta 2024**
- **Statistik Potensi Kelurahan Provinsi DKI Jakarta 2024**

## 📁 Daftar File CSV

### 1. `pengeluaran_per_kapita_wilayah.csv`
**Deskripsi:** Rata-rata pengeluaran per kapita sebulan menurut kabupaten/kota (2023-2024)
**Kolom:**
- `kabupaten_kota`: Nama wilayah
- `pengeluaran_2023_rp`: Pengeluaran tahun 2023 (Rupiah)
- `pengeluaran_2024_rp`: Pengeluaran tahun 2024 (Rupiah)

### 2. `proporsi_pengeluaran_makanan.csv`
**Deskripsi:** Proporsi pengeluaran makanan vs bukan makanan menurut golongan pengeluaran (2024)
**Kolom:**
- `golongan_pengeluaran_rp`: Rentang pengeluaran per kapita sebulan
- `makanan_persen`: Persentase pengeluaran untuk makanan
- `bukan_makanan_persen`: Persentase pengeluaran untuk bukan makanan

### 3. `konsumsi_komoditas_utama.csv`
**Deskripsi:** Rata-rata konsumsi dan pengeluaran komoditas makanan utama (2024)
**Kolom:**
- `komoditas`: Nama komoditas makanan
- `satuan`: Satuan pengukuran (Kg, Ons, Liter, Butir, dll)
- `rata_rata_konsumsi`: Rata-rata banyaknya konsumsi
- `rata_rata_pengeluaran_rp`: Rata-rata nilai pengeluaran (Rupiah)

### 4. `pengeluaran_komoditas_per_wilayah.csv`
**Deskripsi:** Rata-rata pengeluaran per kapita menurut kelompok komoditas pangan per wilayah (2024)
**Kolom:**
- `kelompok_komoditas`: Kategori komoditas pangan
- `kepulauan_seribu`: Pengeluaran di Kepulauan Seribu (Rp)
- `jakarta_selatan`: Pengeluaran di Jakarta Selatan (Rp)
- `jakarta_timur`: Pengeluaran di Jakarta Timur (Rp)
- `jakarta_pusat`: Pengeluaran di Jakarta Pusat (Rp)
- `jakarta_barat`: Pengeluaran di Jakarta Barat (Rp)
- `jakarta_utara`: Pengeluaran di Jakarta Utara (Rp)

### 5. `sarana_ekonomi_kelurahan.csv`
**Deskripsi:** Ketersediaan sarana ekonomi (pasar dan toko) di tingkat kelurahan (2024)
**Kolom:**
- `kabupaten_kota`: Nama wilayah
- `kelompok_pertokoan`: Jumlah kelurahan yang memiliki kelompok pertokoan
- `pasar_permanen`: Jumlah kelurahan dengan pasar bangunan permanen
- `pasar_semi_permanen`: Jumlah kelurahan dengan pasar bangunan semi permanen
- `toko_warung_kelontong`: Jumlah kelurahan dengan toko/warung kelontong

### 6. `penerima_sktm_kelurahan.csv`
**Deskripsi:** Indikator kemiskinan - warga penerima Surat Keterangan Tidak Mampu (SKTM) per wilayah (2023)
**Kolom:**
- `kabupaten_kota`: Nama wilayah
- `kelurahan_ada_penerima_sktm`: Jumlah kelurahan yang ada warga penerima SKTM
- `kelurahan_tidak_ada_penerima_sktm`: Jumlah kelurahan tanpa warga penerima SKTM
- `total_kelurahan`: Total kelurahan di wilayah tersebut

### 7. `profil_penghasilan_utama.csv`
**Deskripsi:** Profil sumber penghasilan utama penduduk per wilayah (2024)
**Kolom:**
- `kabupaten_kota`: Nama wilayah
- `pertanian_perikanan`: Jumlah kelurahan dengan mayoritas penghasilan dari pertanian/perikanan
- `industri_pengolahan`: Jumlah kelurahan dengan mayoritas penghasilan dari industri pengolahan
- `perdagangan_reparasi`: Jumlah kelurahan dengan mayoritas penghasilan dari perdagangan & reparasi
- `akomodasi_makan_minum`: Jumlah kelurahan dengan mayoritas penghasilan dari akomodasi & makan minum

## 📊 Penggunaan Data

Data ini dapat digunakan untuk:
- Analisis pola konsumsi pangan Jakarta
- Analisis daya beli per wilayah
- Mapping infrastruktur pasar dan aksesibilitas pangan
- Analisis korelasi kemiskinan dengan harga pangan
- Segmentasi wilayah berdasarkan karakteristik ekonomi

## 📝 Catatan

- Semua data pengeluaran dalam satuan **Rupiah (Rp)**
- Data tahun **2024** (kecuali SKTM yang tahun 2023)
- Sumber: **Badan Pusat Statistik (BPS) Provinsi DKI Jakarta**
