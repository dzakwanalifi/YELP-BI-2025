# Framework Paper YELP BI 2025: "Spatial Intelligence for Inflation Control"

## 1. Judul & Abstrak
**Judul:**
**"Beyond Price: Membangun Ketahanan Pangan Jakarta Melalui Analisis Jejaring Rantai Pasok Berbasis Graph Theory dan Big Data Geospasial"**

**Abstrak (Draft):**
Inflasi pangan (*volatile food*) di Jakarta seringkali diasumsikan sebagai akibat dari guncangan pasokan (*supply shock*) atau iklim. Namun, studi ini menawarkan perspektif baru dengan membedah struktur mikro rantai pasok menggunakan pendekatan *Network Science* dan *Spatial Intelligence*. Mengintegrasikan data 17.344 fasilitas logistik (OpenStreetMap), harga harian 5 tahun (PIHPS), dan data iklim (Open-Meteo), penelitian ini membangun "Digital Twin" sistem distribusi pangan Jabar-Jakarta. Hasil analisis *Graph Theory* mengungkap adanya 10 *Critical Hubs* yang menjadi *single point of failure*, sementara pemodelan *Random Forest* (R²=0.85) membuktikan bahwa **Konektivitas Logistik** berkontribusi 58.4% terhadap volatilitas harga, jauh melampaui faktor risiko iklim (30.2%). Temuan ini merekomendasikan transformasi peran Bank Indonesia dari sekadar penjaga stabilitas moneter menjadi "Arsitek Ketahanan Jaringan", dengan strategi intervensi presisi berbasis klaster wilayah untuk optimalisasi GNPIP dan PSBI.

---

## 2. Struktur & Konten Paper

### I. Pendahuluan
*(Paragraf 1: Latar Belakang)*
Jakarta sebagai barometer inflasi nasional menghadapi tantangan struktural: ketergantungan pasokan pangan dari luar daerah mencapai 98%. Selama ini, lonjakan harga sering direspon dengan kebijakan agregat (operasi pasar umum) yang seringkali kurang efektif karena tidak menyentuh akar masalah inefisiensi distribusi di level mikro.

*(Paragraf 2: Masalah & Gap)*
Belum adanya peta komprehensif yang memvisualisasikan "jalur tikus" distribusi pangan membuat pembuat kebijakan buta terhadap lokasi *bottleneck* yang sebenarnya. Apakah harga mahal di Jakarta Selatan disebabkan oleh jarak fisik ke produsen, atau karena struktur pasar yang oligopolistik?

*(Paragraf 3: Solusi & Novelty)*
Paper ini mengisi kekosongan tersebut dengan pendekatan *Spatial Intelligence*. Kebaruan studi ini terletak pada penggunaan **Graph Theory** untuk memetakan topologi jaringan logistik secara granular, yang dipadukan dengan **Machine Learning** untuk mengisolasi dampak logistik vs iklim terhadap harga.

### II. Tinjauan Pustaka
*   **Network Resilience:** Konsep ketahanan jaringan (Barabási) dalam konteks rantai pasok pangan.
*   **Spatial Price Transmission:** Teori transmisi harga spasial dan *Law of One Price*.
*   **Peran Bank Sentral:** Evolusi mandat BI dalam pengendalian inflasi daerah (TPID/GNPIP).

### III. Metodologi
*(Paragraf Data)*
Studi ini menggunakan *High-Frequency Spatial Data*:
1.  **Infrastruktur:** 17.344 titik fasilitas (Produsen, Distributor, Ritel) dari OpenStreetMap.
2.  **Harga:** Data harian PIHPS (2020-2025) untuk komoditas strategis (Cabai Rawit Merah).
3.  **Lingkungan:** Data curah hujan historis dari Open-Meteo API.

*(Paragraf Metode)*
Analisis dilakukan dalam tiga tahap:
1.  **Network Construction:** Membangun graf berarah untuk menghitung metrik sentralitas (*Betweenness Centrality*).
2.  **Integrated Modeling:** Menggunakan *Random Forest Regressor* untuk mengukur *Feature Importance*.
3.  **Spatial Clustering:** Mengelompokkan wilayah berdasarkan karakteristik masalah (Struktural vs Inefisiensi).

### IV. Hasil dan Diskusi

#### 4.1. The Spatial Heterogeneity: Peta Diagnosa Presisi (MGWR)
Analisis *Multiscale Geographically Weighted Regression* (MGWR) mengungkap bahwa pengaruh logistik terhadap harga tidak seragam (*spatially non-stationary*). Peta koefisien pada **Gambar 1** menunjukkan divergensi yang tajam antara wilayah konsumen dan hub distribusi.

> **[INSERT FIGURE 1 HERE]**
> *   **File:** `final_paper_assets/Fig1_MGWR_Coefficient_Map.png`
> *   **Caption:** Gambar 1. Peta Variasi Spasial Koefisien Pengaruh Logistik terhadap Harga (MGWR).
> *   **Interpretasi:**
>     *   **Jakarta Pusat (Sink Node):** Memiliki sensitivitas negatif yang kuat terhadap jarak produksi (Koefisien: **-0.427**). Artinya, setiap penambahan jarak fisik dari sentra produksi berdampak signifikan pada struktur harga. Ini mengkonfirmasi bahwa Jakarta masih terkendala oleh "Friksi Fisik".
>     *   **Cirebon (Hub Node):** Sebaliknya, Cirebon menunjukkan sensitivitas yang sangat rendah terhadap jarak distribusi (Koefisien: **0.072**), jauh di bawah Bogor (0.398). Ini membuktikan status Cirebon sebagai *Natural Hub* yang memiliki akses pasar superior, sehingga jarak tidak lagi menjadi kendala biaya.
>     *   **Implikasi:** Kebijakan subsidi ongkos angkut akan sangat efektif untuk Jakarta, namun sia-sia untuk Cirebon. Cirebon lebih membutuhkan infrastruktur penyimpanan (*Cold Storage*) untuk mengelola volume, bukan subsidi jarak.

#### 4.2. The Transmission Mechanism: Melacak Jejak 'Tsunami' Harga (Network Stress Test)
Simulasi *Impulse Response Function* (IRF) dari model VAR mematahkan asumsi transmisi instan. Hasil simulasi guncangan pasokan dari Bandung ke Jakarta menunjukkan adanya jeda waktu (*time lag*) yang signifikan.

> **[INSERT FIGURE 2 HERE]**
> *   **File:** `final_paper_assets/Fig2_Shock_Propagation_IRF.png`
> *   **Caption:** Gambar 2. Respon Impuls Harga Jakarta terhadap Guncangan Supply di Sentra Produksi (Bandung).
> *   **Interpretasi:**
>     *   **The 2-Week Lag:** Dampak guncangan harga di Bandung tidak langsung memuncak di Jakarta pada hari yang sama. Data menunjukkan puncak dampak (*peak impact*) baru terjadi pada **Minggu ke-2** (Nilai respon: -0.309).
>     *   **Jendela Intervensi:** Temuan ini memberikan "Waktu Emas" (*Golden Time*) selama 14 hari bagi Bank Indonesia. Saat ini, respon kebijakan seringkali terlambat (reaktif). Dengan dashboard *Early Warning System* yang memantau harga di hulu (Bandung), BI dapat melakukan intervensi pre-emptive pada Minggu ke-0 atau ke-1, mencegah "tsunami" harga mencapai puncaknya di Jakarta.

#### 4.3. The Structural Bottleneck: Asimetri Harga & The Perishability Paradox
Analisis *Asymmetric Price Transmission* mengungkap fenomena menarik yang spesifik pada komoditas mudah rusak (*perishable*).

> **[INSERT FIGURE 3 HERE]**
> *   **File:** `final_paper_assets/Fig3_Price_Asymmetry.png`
> *   **Caption:** Gambar 3. Asimetri Transmisi Harga: Perbandingan Fase Kenaikan vs Penurunan.
> *   **Interpretasi:**
>     *   **The Perishability Paradox:** Berbeda dengan teori *Rockets and Feathers* klasik (naik cepat, turun lambat), data menunjukkan bahwa transmisi penurunan harga justru lebih kuat (Koefisien: **0.286**) dibandingkan kenaikan harga (Koefisien: **0.258**).
>     *   **Panic Selling:** Fenomena ini mengindikasikan perilaku *Panic Selling* di tingkat produsen. Tanpa fasilitas *Cold Storage*, petani/pengepul dipaksa segera melepas stok saat panen raya (harga turun) agar tidak membusuk, sehingga transmisi ke Jakarta sangat cepat. Sebaliknya, saat harga naik (kelangkaan), transmisi sedikit tertahan.
>     *   **Solusi Struktural:** Ini memvalidasi urgensi pengadaan *Cold Storage* di titik *Critical Hubs*. Fasilitas ini akan memberikan opsi "tahan stok" bagi petani, menstabilkan laju transmisi harga, dan melindungi petani dari kejatuhan harga yang ekstrim.

### V. Kesimpulan dan Rekomendasi Kebijakan
*(Paragraf Kesimpulan)*
Studi ini menyimpulkan bahwa inflasi pangan Jakarta adalah masalah logistik struktural, bukan sekadar fenomena moneter atau cuaca sesaat. Sistem distribusi yang bertumpu pada sedikit *Critical Hubs* menciptakan kerentanan tinggi.

*(Paragraf Rekomendasi - "The BI Way")*
1.  **Transformasi GNPIP:** Beralih dari operasi pasar "pukul rata" menjadi intervensi berbasis zona (Merah/Oranye) sesuai Peta Klaster (Gambar 3).
2.  **Penguatan PSBI:** Alokasi bantuan *Cold Storage* difokuskan wajib pada 10 *Critical Hubs* (Tabel 1) untuk membangun redundansi sistem.
3.  **Digitalisasi Rantai Pasok:** Implementasi QRIS dan pencatatan stok digital di *Critical Hubs* sebagai sistem peringatan dini (*Early Warning System*) inflasi.

---

## 3. Checklist Lampiran (Attachments)
*   [ ] **Lampiran A:** Statistik Deskriptif Data (`final_paper_assets/Table1_Descriptive_Stats.csv`).
*   [ ] **Lampiran B:** Evaluasi Akurasi Model ML (`final_paper_assets/Table3_Model_Evaluation.txt`).
*   [ ] **Lampiran C:** Matriks Korelasi (`final_paper_assets/Fig4_Correlation_Matrix.png`).
