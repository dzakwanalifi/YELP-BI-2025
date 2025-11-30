# BAB IV: HASIL DAN DISKUSI

Bab ini menguraikan temuan empiris dari analisis spasial-temporal terintegrasi terhadap ekosistem rantai pasok pangan di wilayah Jawa Barat dan DKI Jakarta. Melalui pendekatan metodologi hibrida yang menggabungkan *Spatial Econometrics* (MGWR), *Network Science* (VAR), dan *Non-linear Time Series Analysis* (NARDL), penelitian ini berupaya membedah anatomi inflasi pangan bukan sekadar sebagai fenomena moneter agregat, melainkan sebagai konsekuensi dari inefisiensi struktural dalam jaringan logistik. Diskusi difokuskan pada tiga dimensi utama: heterogenitas spasial, dinamika transmisi guncangan, dan asimetri perilaku harga.

## 4.1. Heterogenitas Spasial Sensitivitas Harga: Bukti Empiris dari Model MGWR

> **[GAMBAR 1]**  
> **File:** `final_paper_assets/Fig1_MGWR_Coefficient_Map.png`  
> **Caption:** Gambar 1. Peta Variasi Spasial Koefisien Pengaruh Jarak Distribusi terhadap Harga (MGWR). Gradasi warna menunjukkan sensitivitas harga di setiap lokasi: merah pekat = sensitivitas tinggi (Jakarta), biru muda = sensitivitas rendah (Cirebon).

Penerapan *Multiscale Geographically Weighted Regression* (MGWR) menyingkap pola heterogenitas yang mencolok dalam elastisitas harga terhadap faktor logistik di seluruh wilayah studi. Berbeda dengan regresi global (OLS) yang mengasumsikan hubungan seragam (*stationarity*), hasil MGWR membuktikan bahwa sensitivitas harga bersifat *spatially non-stationary*. Sebagaimana divisualisasikan pada **Gambar 1**, gradasi warna pada peta menunjukkan variasi intensitas sensitivitas harga terhadap jarak distribusi di setiap lokasi.

Secara spesifik, model mengestimasi tingkat sensitivitas (*sensitivity magnitude*) harga terhadap jarak distribusi di Jakarta Pusat mencapai **0.354**. Secara statistik, angka ini mengindikasikan bahwa Jakarta memiliki eksposur risiko logistik tertinggi dibandingkan wilayah lainnya. Sebagai wilayah *net-importer* absolut, struktur pembentukan harga di Jakarta sangat rentan terhadap friksi distribusi; setiap peningkatan hambatan logistik—baik berupa biaya transportasi, pungutan liar, maupun kemacetan fisik—akan tertransmisikan secara signifikan ke harga konsumen akhir. Temuan ini menggarisbawahi bahwa bagi Jakarta, efisiensi jaringan distribusi adalah determinan biaya yang dominan.

Kondisi ini bertolak belakang dengan temuan di Cirebon, yang mencatat tingkat sensitivitas yang jauh lebih rendah (**0.072**). Rendahnya sensitivitas ini menegaskan peran Cirebon sebagai *Natural Hub*.

> **[TABEL 1]**  
> **File:** `final_paper_assets/mgwr_results.csv`  
> **Caption:** Tabel 1. Hasil Estimasi MGWR: Koefisien Sensitivitas Spasial untuk Setiap Lokasi. Kolom menunjukkan koefisien jarak produksi, jarak distribusi, dan curah hujan terhadap harga. 

Kedekatan geografis Cirebon dengan sentra produksi bawang dan cabai di sekitarnya menciptakan efisiensi alamiah yang mengisolasi pasar lokal dari volatilitas biaya logistik eksternal. Divergensi statistik antara Jakarta dan Cirebon ini memberikan bukti empiris yang kuat bahwa inflasi pangan di Jawa Barat bukanlah fenomena tunggal, melainkan masalah struktural yang berakar pada topologi jaringan distribusi. Implikasi teoretisnya adalah kebijakan subsidi biaya angkut (*transport subsidy*) akan memiliki *marginal utility* yang tinggi di Jakarta, namun akan menjadi inefisiensi alokasi sumber daya jika diterapkan di Cirebon yang masalah utamanya bukan pada akses fisik, melainkan pada kapasitas manajemen stok dan penyimpanan.

## 4.2. Analisis Dinamis Transmisi Guncangan Pasokan (*Supply Shock Propagation*)

> **[GAMBAR 2]**  
> **File:** `final_paper_assets/Fig2_Shock_Propagation_IRF.png`  
> **Caption:** Gambar 2. Impulse Response Function (IRF): Respon Harga Jakarta Pusat terhadap Guncangan Pasokan di Bandung. Grafik menunjukkan puncak dampak terjadi pada minggu ke-2 dengan nilai respon -0.310.

Analisis statis saja tidak cukup untuk memahami perilaku harga yang dinamis. Oleh karena itu, penelitian ini menggunakan model *Vector Autoregression* (VAR) untuk mensimulasikan bagaimana guncangan pasokan (*supply shock*) di hulu merambat ke pasar konsumen di hilir. Simulasi *Impulse Response Function* (IRF) yang disajikan pada **Gambar 2** mematahkan asumsi klasik bahwa pasar merespon informasi secara instan (*efficient market hypothesis*).

Grafik respon impuls menunjukkan bahwa guncangan pasokan sebesar satu standar deviasi di sentra produksi Bandung tidak langsung memuncak di Jakarta pada periode yang sama. Puncak dampak (*peak impact*) deflasi atau inflasi baru tercatat secara signifikan pada **Minggu ke-2** (dengan nilai respon -0.310). Fenomena jeda waktu (*time lag*) selama 14 hari ini merefleksikan kompleksitas rantai pasok fisik yang berlapis. Komoditas harus melewati serangkaian proses konsolidasi di tingkat pengepul (*middlemen*), transportasi antar-kota, hingga distribusi di pasar induk sebelum akhirnya membentuk harga di tingkat eceran. Friksi dalam setiap lapisan inilah yang menunda transmisi sinyal pasar.

Dari perspektif kebijakan, temuan "Jeda 2 Minggu" ini menawarkan jendela peluang (*window of opportunity*) yang krusial bagi Bank Indonesia.

> **[TABEL 2]**  
> **File:** `final_paper_assets/johansen_cointegration_test.csv`  
> **Caption:** Tabel 2. Hasil Uji Kointegrasi Johansen: Validasi Hubungan Jangka Panjang antar Pasar.

> **[TABEL 3]**  
> **File:** `final_paper_assets/granger_causality.txt`  
> **Caption:** Tabel 3. Hasil Uji Kausalitas Granger (Bandung → Jakarta Pusat). P-value < 0.05 mengindikasikan Bandung secara statistik "menyebabkan" perubahan harga di Jakarta. Selama ini, respon pengendalian inflasi seringkali bersifat reaktif—dilakukan setelah harga konsumen melonjak. Data ini menyarankan perlunya pergeseran paradigma menuju intervensi *pre-emptive*. Dengan membangun sistem peringatan dini (*Early Warning System*) yang memantau volatilitas harga di pasar hulu (Bandung/Garut), otoritas moneter memiliki waktu emas selama dua minggu untuk melakukan antisipasi—seperti mobilisasi pasokan antar-daerah (KAD) atau operasi pasar—sebelum guncangan tersebut teramplifikasi menjadi lonjakan IHK di Jakarta.

## 4.3. Asimetri Transmisi Harga dan Paradoks Komoditas *Perishable*

> **[GAMBAR 3]**  
> **File:** `final_paper_assets/Fig3_Price_Asymmetry.png`  
> **Caption:** Gambar 3. Asimetri Transmisi Harga: Perbandingan Kecepatan Transmisi Kenaikan vs Penurunan Harga. Bar chart menunjukkan koefisien penurunan harga (0.286) lebih tinggi dari kenaikan harga (0.258), mengindikasikan fenomena "Panic Selling".

Salah satu temuan paling menarik dari penelitian ini adalah perilaku asimetri harga yang terungkap melalui model *Non-linear Autoregressive Distributed Lag* (NARDL). Teori ekonomi umum sering merujuk pada fenomena *Rockets and Feathers*, di mana harga cenderung naik cepat seperti roket saat terjadi guncangan biaya, namun turun lambat seperti bulu saat biaya normal kembali. Namun, hasil empiris pada komoditas cabai rawit di wilayah studi ini justru **menolak hipotesis tersebut**.

Hasil estimasi menunjukkan bahwa koefisien transmisi untuk penurunan harga (*price decrease*) adalah sebesar **0.286**, yang secara statistik lebih tinggi dibandingkan koefisien kenaikan harga (*price increase*) sebesar **0.258**. Anomali ini dapat dijelaskan melalui karakteristik intrinsik komoditas hortikultura yang mudah rusak (*perishable*) dan ketiadaan infrastruktur penyimpanan (*cold chain*). Dalam literatur ekonomi pertanian, fenomena ini dikenal sebagai dampak dari **"Perishability Risk"** dan **"Liquidity Constraint"**.

Ketika terjadi panen raya (surplus pasokan), petani dan pengepul menghadapi tekanan ganda: risiko komoditas membusuk dan kebutuhan likuiditas tunai. Tanpa fasilitas *Cold Storage* untuk menahan stok, mereka dipaksa melakukan aksi jual cepat (*panic selling*) untuk meminimalisir kerugian total, sehingga penurunan harga di tingkat produsen tertransmisikan dengan sangat cepat dan agresif ke pasar konsumen. Sebaliknya, ketika terjadi kelangkaan (kenaikan harga), transmisi berjalan lebih lambat karena adanya upaya penahanan stok (*hoarding*) di berbagai titik rantai pasok untuk memaksimalkan margin. Temuan ini secara empiris memvalidasi bahwa absennya infrastruktur pasca-panen (*Cold Storage*) adalah akar penyebab volatilitas ekstrem yang merugikan petani (saat panen raya) sekaligus konsumen (saat paceklik).

## 4.4. Sintesis Kebijakan: Menuju Pengendalian Inflasi Presisi

Integrasi dari ketiga analisis di atas mengarah pada satu kesimpulan fundamental: pengendalian inflasi pangan di Jawa Barat dan Jakarta memerlukan transformasi dari pendekatan makro-agregat menjadi pendekatan mikro-struktural yang presisi. Peta jalan kebijakan yang diusulkan meliputi:

1.  **Zonasi Intervensi Berbasis Data:** Mengganti kebijakan subsidi "pukul rata" dengan alokasi asimetris. Fokuskan subsidi logistik dan perbaikan akses fisik pada "Zona Rentan Friksi" seperti Jakarta dan Depok. Sementara itu, alihkan anggaran untuk pembangunan infrastruktur penyimpanan publik pada "Zona Hub Produksi" seperti Cirebon dan Tasikmalaya.
2.  **Pemanfaatan Jendela Waktu Intervensi:** Menggeser kurva intervensi TPID ke kiri (*shift-left*), memanfaatkan jeda transmisi 2 minggu untuk meredam ekspektasi inflasi sebelum terealisasi pada data BPS.
3.  **Investasi Struktural *Cold Chain*:** Menjadikan pengadaan *Cold Storage* sebagai prioritas infrastruktur pengendali inflasi, bukan sekadar pelengkap. Ini adalah solusi struktural untuk memutus siklus *panic selling* dan menstabilkan asimetri transmisi harga.

Melalui strategi ini, Bank Indonesia dapat memperkuat perannya bukan hanya sebagai penjaga stabilitas moneter, tetapi juga sebagai orkestrator efisiensi ekonomi riil yang berbasis pada kecerdasan data spasial (*Spatial Intelligence*).
