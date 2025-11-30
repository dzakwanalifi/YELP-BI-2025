# BAB 3: METODOLOGI PENELITIAN

## 3.1 Kerangka dan Pendekatan Penelitian

Penelitian ini menggunakan pendekatan ekonometrika spasial untuk menganalisis dinamika harga beras dengan mempertimbangkan interdependensi spasial antar wilayah. Spatial Durbin Model (SDM) dipilih karena mampu menangkap efek spasial melalui _spatial lag dependent variable_ (ρ) dan _spatial lag independent variables_ (θ) secara simultan, memungkinkan dekomposisi _direct effects_ dan _indirect effects_ (spillover) yang krusial untuk desain kebijakan regional (LeSage & Pace, 2009). SDM lebih fleksibel dibandingkan model SAR atau SEM karena menghasilkan estimasi koefisien yang tidak bias bahkan ketika _data generating process_ sebenarnya adalah SAR atau SEM, menjadikannya _robust_ terhadap _misspecification_ (Rüttenauer, 2019). Alur penelitian terdiri dari lima tahap: Data Preparation, Exploratory Spatial Data Analysis (ESDA), Model Diagnostics, SDM Estimation, dan Policy Simulation.

[Gambar 3.1: Flowchart Metodologi - 5 Tahap]

---

## 3.2 Data dan Variabel Penelitian

Penelitian mengintegrasikan lima sumber data: PIHPS (harga beras harian 2020-2025), OpenMeteo (curah hujan dan suhu harian), TradingEconomics (harga BBM bulanan), BPS Jawa Barat (luas panen tahunan), dan OpenStreetMap (17.344 fasilitas rantai pasok). Data diorganisir dalam _balanced panel_ 12 lokasi × 58 bulan (Januari 2021 - Oktober 2025) menghasilkan 696 observasi. Variabel dependen adalah harga beras (IDR/kg), sedangkan variabel independen meliputi _price_lag1_, _rain_lag1/2/3_, _bbm_lag1_, _temperature_mean_, _luas_panen_, _connectivity_index_, dan _month_dummies_.

Pemilihan _lag structure_ didasarkan pada _biological lag_ siklus tanam padi (90-120 hari) dan _economic lag_ dalam transmisi harga. Naylor et al. (2007) menunjukkan bahwa siklus pertumbuhan padi di Indonesia terdiri dari fase vegetatif (30-60 hari), reproduktif (60-90 hari), dan pematangan (90-120 hari). Xu et al. (2021) menemukan bahwa setiap kenaikan 1°C suhu rata-rata mengurangi hasil padi sekitar 6,2%. Struktur lag BBM mencerminkan _asymmetric price transmission_ dimana kenaikan biaya bahan bakar ditransmisikan lebih cepat (1-2 bulan) dibandingkan penurunan (3-4 bulan) (Bacon, 1991).

Tabel 3.1: Sumber Data dan Karakteristik

| Sumber Data | Variabel | Periode | Frekuensi Awal | Frekuensi Akhir | Jumlah Observasi | Metode Pengumpulan |
|-------------|----------|---------|----------------|-----------------|------------------|-------------------|
| PIHPS | Harga beras medium (IDR/kg) | 2020-2025 | Harian | Bulanan | 696 | Web scraping portal PIHPS |
| OpenMeteo | Curah hujan (mm/hari), Suhu (°C) | 2020-2025 | Harian | Bulanan | 696 | API historical weather |
| TradingEconomics | Harga BBM Pertalite (IDR/liter) | 2020-2025 | Bulanan | Bulanan | 58 | Web scraping database ekonomi |
| BPS Jawa Barat | Luas panen padi (hektar) | 2020-2024 | Tahunan | Bulanan | 696 | Publikasi resmi BPS |
| OpenStreetMap | Fasilitas rantai pasok | 2024 | Cross-section | - | 17.344 | Overpass API query |

Tabel 3.2: Definisi Operasional Variabel

| Variabel | Definisi | Satuan | Sumber | Lag | Justifikasi Lag |
|----------|----------|--------|--------|-----|-----------------|
| price | Harga beras medium di pasar lokal | IDR/kg | PIHPS | - | Variabel dependen |
| price_lag1 | Harga beras bulan sebelumnya | IDR/kg | PIHPS | 1 bulan | Price persistence |
| rain_lag1 | Curah hujan 1 bulan sebelumnya | mm/bulan | OpenMeteo | 1 bulan | Fase vegetatif (30-60 hari) |
| rain_lag2 | Curah hujan 2 bulan sebelumnya | mm/bulan | OpenMeteo | 2 bulan | Fase generatif (60-90 hari) |
| rain_lag3 | Curah hujan 3 bulan sebelumnya | mm/bulan | OpenMeteo | 3 bulan | Fase pematangan (90-120 hari) |
| bbm_lag1 | Harga BBM bulan sebelumnya | IDR/liter | TradingEconomics | 1 bulan | Delayed pass-through |
| temperature_mean | Suhu rata-rata bulanan | °C | OpenMeteo | 0 | Heat stress effect |
| luas_panen | Luas panen padi | Hektar | BPS Jabar | 0 | Supply-side indicator |
| connectivity_index | ln(1 + fasilitas dalam 10km) | Index | OSM | 0 | Efisiensi distribusi |
| month_dummies | Dummy bulan 1-12 | Binary | - | 0 | Pola musiman |

---

## 3.3 Konstruksi Spatial Weights Matrix

Tiga spesifikasi _spatial weights matrix_ dikonstruksi untuk menangkap berbagai dimensi keterkaitan spasial. _Geographic Weights_ (W_geo) menggunakan K-Nearest Neighbors (k=3,5,8) berdasarkan jarak Euclidean untuk menangkap _proximity_ fisik. Anselin (1988) menunjukkan bahwa KNN sesuai untuk unit spasial dengan ukuran tidak seragam karena memastikan setiap lokasi memiliki tepat k tetangga. _Economic Weights_ (W_econ) dikonstruksi menggunakan formula:

w_ij = √(facilities_i × facilities_j) / distance_ij

yang menangkap intensitas koneksi rantai pasok aktual. Conley & Ligon (2002) berargumen bahwa _economic connectivity_ lebih relevan untuk pasar komoditas karena transmisi harga beroperasi melalui jalur perdagangan. _Combined Weights_ (W_combined) merupakan _weighted average_:

W = 0.5×W_geo + 0.5×W_econ

yang mengintegrasikan _proximity_ geografis dan konektivitas ekonomi. Rüttenauer (2019) menunjukkan bahwa SDM _robust_ terhadap _misspecification weights matrix_. Semua matriks di-_row-standardize_ (Σ_j w_ij = 1) untuk interpretabilitas dan konvergensi _spatial multiplier_ (LeSage & Pace, 2009).

---

## 3.4 Spesifikasi Model Spatial Durbin

Model SDM dengan _two-way fixed effects_:

Price_it = ρ(W·Price)_it + X_it β + (W·X_it) θ + α_i + μ_t + ε_it

dimana ρ adalah _spatial autoregressive coefficient_, β adalah _direct effects_, θ adalah _spatial spillover effects_, α_i adalah _location fixed effects_, μ_t adalah _time fixed effects_. Spesifikasi _two-way fixed effects_ dipilih untuk mengontrol heterogenitas spasial _time-invariant_ dan _shock_ temporal _common across regions_ (Elhorst, 2014). Estimasi menggunakan Maximum Likelihood atau GMM dengan _robust standard errors_. Dekomposisi efek mengikuti LeSage & Pace (2009):

∂Price/∂X = (I-ρW)^(-1)(βI_n + Wθ)

menghasilkan _Direct Effects_ (rata-rata diagonal), _Indirect Effects_ (rata-rata _off-diagonal_), dan _Total Effects_ (penjumlahan keduanya). _Spatial multiplier_ (I-ρW)^(-1) mengkuantifikasi bagaimana _shock_ ekonomi menyebar melalui ruang dengan _infinite series expansion_:

(I-ρW)^(-1) = I + ρW + ρ²W² + ρ³W³ + ...

---

## 3.5 Tahapan Analisis

_Exploratory Spatial Data Analysis_ (ESDA) dilakukan menggunakan Global Moran's I untuk deteksi _spatial autocorrelation_ keseluruhan dan Local Moran's I (LISA) untuk identifikasi _spatial clusters_ (High-High, Low-Low) serta _outliers_ (High-Low, Low-High). Anselin (1995) menunjukkan bahwa LISA mendekomposisi _global spatial autocorrelation_ menjadi kontribusi lokal untuk mengidentifikasi _hot spots_.

_Diagnostik Pra-Estimasi_ meliputi ADF test (stasionaritas), VIF (multikolinearitas, threshold <10), Breusch-Pagan (heteroskedastisitas), dan LM-Lag & LM-Error tests (_spatial dependence_). _Model Selection_ dilakukan melalui Robust LM tests (justifikasi SDM vs SAR vs SEM), Hausman test (Fixed vs Random Effects), dan AIC/BIC (perbandingan _model fit_). Anselin et al. (1996) mengembangkan Robust LM tests yang memungkinkan diferensiasi antara _spatial lag_ dan _spatial error dependence_.

_Validasi Pasca-Estimasi_ mencakup Moran's I residual (harus mendekati nol), _robustness checks_ dengan _alternative weights_ (KNN-3/5/8, distance-based, economic-only), dan _out-of-sample forecast validation_ menggunakan _rolling window_ 2021-2023 (training) vs 2024-2025 (testing) dengan metrik MAPE, RMSE, dan _directional accuracy_. Diebold & Mariano (1995) menunjukkan bahwa _out-of-sample forecast evaluation_ memberikan penilaian tidak bias terhadap performa model.

_Policy Simulation_ menggunakan tiga skenario _counterfactual_: BBM shock +15%, Drought -200mm, dan Heat wave +2°C. Dampak dihitung sebagai:

ΔPrice = (I-ρW)^(-1) × (β + W×θ) × ΔX

untuk menghasilkan _spatial impact map_ per wilayah. LeSage & Pace (2009) menekankan bahwa analisis kebijakan spasial memerlukan komputasi _total effects_ yang memperhitungkan _spatial feedback_ melalui _spatial multiplier matrix_.

---

[Total: ~3-4 halaman dengan 2 tabel, 1 gambar]

---

## DAFTAR PUSTAKA

Anselin, L. (1988). _Spatial Econometrics: Methods and Models_. Kluwer Academic Publishers. https://doi.org/10.1007/978-94-015-7799-1

Anselin, L. (1995). Local Indicators of Spatial Association-LISA. _Geographical Analysis_, 27(2), 93-115. https://doi.org/10.1111/j.1538-4632.1995.tb00338.x

Anselin, L., Bera, A.K., Florax, R., & Yoon, M.J. (1996). Simple Diagnostic Tests for Spatial Dependence. _Regional Science and Urban Economics_, 26(1), 77-104. https://doi.org/10.1016/0160-4176(95)02111-6

Bacon, R.W. (1991). Rockets and Feathers: The Asymmetric Speed of Adjustment of UK Retail Gasoline Prices to Cost Changes. _Energy Economics_, 13(3), 211-218. https://doi.org/10.1016/0140-9883(91)90001-E

Baltagi, B.H., Egger, P., & Pfaffermayr, M. (2013). A Generalized Spatial Panel Data Model with Random Effects. _Econometric Reviews_, 32(5-6), 650-685. https://doi.org/10.1080/07474938.2012.740957

Conley, T.G., & Ligon, E. (2002). Economic Distance and Cross-Country Spillovers. _Journal of Economic Growth_, 7(2), 157-187. https://doi.org/10.1023/A:1020823906499

Diebold, F.X., & Mariano, R.S. (1995). Comparing Predictive Accuracy. _Journal of Business & Economic Statistics_, 13(3), 253-263. https://doi.org/10.1080/07350015.1995.10524599

Elhorst, J.P. (2014). Spatial Econometrics: From Cross-Sectional Data to Spatial Panels. _Journal of Geographical Systems_, 16(4), 307-324. https://doi.org/10.1007/s10109-014-0207-x

LeSage, J.P., & Pace, R.K. (2009). _Introduction to Spatial Econometrics_. CRC Press, Boca Raton. https://doi.org/10.1201/9781420064254

Naylor, R.L., Battisti, D.S., Vimont, D.J., Falcon, W.P., & Burke, M.B. (2007). Assessing Risks of Climate Variability and Climate Change for Indonesian Rice Agriculture. _Proceedings of the National Academy of Sciences_, 104(19), 7752-7757. https://doi.org/10.1073/pnas.0701825104

Rüttenauer, T. (2019). Spatial Regression Models: A Systematic Comparison of Different Model Specifications using Monte Carlo Experiments. _Sociological Methods & Research_, 50(3), 1319-1356. https://doi.org/10.1177/0049124119882467

Xu, Y., Chu, C., & Yao, S. (2021). The Impact of High-Temperature Stress on Rice: Challenges and Strategies. _International Journal of Molecular Sciences_, 22(5), 2577. https://doi.org/10.3390/ijms22052577
