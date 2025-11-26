# InfoPangan Jakarta - API Documentation

Dokumentasi lengkap API endpoints yang ditemukan dari website InfoPangan Jakarta.

## Base URL
```
https://infopangan.jakarta.go.id/api2
```

---

## 📌 Endpoints

### 1. Get All Markets

**Endpoint:** `GET /v1/master-data/market`

**Deskripsi:** Mengambil daftar semua pasar yang tersedia di Jakarta

**Parameters:** None

**Response:**
```json
{
  "data": [
    {
      "city_id": "2",
      "city_name": "Jakarta Pusat",
      "market_id": "3",
      "market_name": "Pasar Senen Blok III - VI",
      "market_short_name": "Senen",
      "market_address": "Jl. Pasar Senen Raya Kel. Senen, Kec. Senen",
      "market_latitude": "-6.176417",
      "market_longitude": "106.840836",
      "market_phone": "+62 21 4210411 / 42881877",
      "market_level": "eceran"
    }
  ],
  "total": 50
}
```

**Contoh cURL:**
```bash
curl -X GET "https://infopangan.jakarta.go.id/api2/v1/master-data/market"
```

---

### 2. Search Markets

**Endpoint:** `GET /v1/master-data/market`

**Deskripsi:** Mencari pasar berdasarkan keyword (autocomplete)

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| search_text | string | Yes | Keyword pencarian pasar |

**Response:**
```json
{
  "data": [
    {
      "city_id": "2",
      "city_name": "Jakarta Pusat",
      "market_id": "21",
      "market_name": "Pasar Tanah Abang Blok A-G",
      "market_short_name": "Tanah Abang",
      "market_address": "Jl. K.H. Fachrudin Kel.Kampung Bali Kec.Tanah Abang",
      "market_latitude": "-6.187407",
      "market_longitude": "106.814136",
      "market_phone": "",
      "market_level": "eceran"
    }
  ],
  "total": 1
}
```

**Contoh cURL:**
```bash
curl -X GET "https://infopangan.jakarta.go.id/api2/v1/master-data/market?search_text=Tanah%20Abang"
```

**Contoh Python:**
```python
import requests

response = requests.get(
    "https://infopangan.jakarta.go.id/api2/v1/master-data/market",
    params={"search_text": "Tanah Abang"}
)
print(response.json())
```

---

### 3. Get Commodity Prices by Market

**Endpoint:** `GET /v2/public/master-data/commodity/markets/{market_id}`

**Deskripsi:** Mengambil data harga komoditas untuk pasar tertentu

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| market_id | integer | Yes | ID pasar (0 untuk semua pasar) |

**Headers:**
```
app-client-id: 6d608776a6b399ac767db6b0df8b864a18b1c1e9
```

**Response:**
```json
{
  "status": 200,
  "message": "Success",
  "data": {
    "selected_price_date": "2025-11-26",
    "data": [
      {
        "commodity_id": 1,
        "name": "Beras IR. I (IR 64)",
        "unit": "kg",
        "image_path": "https://infopangan.jakarta.go.id/api2/v1/file?name=IR_I_(IR_64).png",
        "newest_price": 14000,
        "prev_price": 14000,
        "highest_price": 14000,
        "lowest_price": 14000,
        "avg_price": 14000,
        "percentage_price_increase_warning": 50.32,
        "latest_new_price_date": "2025-11-26",
        "gap_min_price": 999999,
        "gap_max_price": 999999,
        "status": "stagnant"
      }
    ]
  }
}
```

**Status Values:**
- `stagnant`: Harga tidak berubah
- `rise`: Harga naik

**Contoh cURL:**
```bash
curl -X GET "https://infopangan.jakarta.go.id/api2/v2/public/master-data/commodity/markets/21" \
  -H "app-client-id: 6d608776a6b399ac767db6b0df8b864a18b1c1e9"
```

**Contoh Python:**
```python
import requests

headers = {
    'app-client-id': '6d608776a6b399ac767db6b0df8b864a18b1c1e9'
}

response = requests.get(
    "https://infopangan.jakarta.go.id/api2/v2/public/master-data/commodity/markets/21",
    headers=headers
)
print(response.json())
```

---

### 4. Get Content/Links

**Endpoint:** `GET /v1/public/content`

**Deskripsi:** Mengambil konten atau link dari website

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| search_text | string | Yes | Keyword pencarian konten |

**Contoh cURL:**
```bash
curl -X GET "https://infopangan.jakarta.go.id/api2/v1/public/content?search_text=link"
```

---

### 5. Auth Session

**Endpoint:** `GET /api/auth/session`

**Deskripsi:** Mendapatkan session info (tidak wajib untuk public API)

**Base URL:** `https://infopangan.jakarta.go.id/api`

---

## 📊 Market ID Reference

Berikut adalah daftar market_id yang populer:

### Jakarta Pusat
| Market ID | Nama Pasar |
|-----------|------------|
| 3 | Pasar Senen Blok III - VI |
| 21 | Pasar Tanah Abang Blok A-G |
| 22 | Pasar Petojo Ilir |
| 23 | Pasar Gondangdia |
| 24 | Pasar Paseban |
| 25 | Pasar Cempaka Putih |
| 26 | Pasar Johar Baru |
| 27 | Pasar Baru Metro Atom |

### Jakarta Selatan
| Market ID | Nama Pasar |
|-----------|------------|
| 9 | Pasar Minggu |
| 10 | Pasar Mayestik |
| 28 | Pasar Kebayoran Lama |
| 29 | Pasar Cipete |
| 30 | Pasar Pesanggrahan |
| 31 | Pasar Pondok Labu |
| 32 | Pasar Lenteng Agung |
| 33 | Pasar Mampang Prapatan |

### Jakarta Timur
| Market ID | Nama Pasar |
|-----------|------------|
| 11 | Pasar Pramuka |
| 12 | Pasar Kramat Jati |
| 13 | Pasar Jatinegara |
| 14 | Pasar Perumnas Klender |
| 15 | Pasar Pulo Gadung |
| 16 | Pasar Pal Meriam |
| 17 | Pasar Ciplak |
| 18 | Pasar Cijantung |

### Jakarta Barat
| Market ID | Nama Pasar |
|-----------|------------|
| 7 | Pasar Grogol |
| 8 | Pasar Glodok |

### Jakarta Utara
| Market ID | Nama Pasar |
|-----------|------------|
| 5 | Pasar Sunter Podomoro |
| 6 | Pasar Rawa Badak |

---

## 🔐 Authentication

API ini bersifat **public** dan tidak memerlukan authentication. Namun untuk beberapa endpoint, disarankan menggunakan header:

```
app-client-id: 6d608776a6b399ac767db6b0df8b864a18b1c1e9
```

---

## ⚡ Rate Limiting

Tidak ada dokumentasi resmi tentang rate limit, namun disarankan:
- Berikan delay minimal **1 detik** antar request
- Hindari parallel request dalam jumlah besar
- Gunakan cache untuk data yang tidak sering berubah

---

## 🚨 Error Handling

### HTTP Status Codes
- `200`: Success
- `304`: Not Modified (cached)
- `400`: Bad Request
- `500`: Internal Server Error

### Example Error Response
```json
{
  "status": 400,
  "message": "Bad Request",
  "data": null
}
```

---

## 💡 Best Practices

1. **Gunakan Cache**
   - Data harga biasanya update sekali sehari
   - Cache response untuk mengurangi beban server

2. **Handle Network Errors**
   - Implementasikan retry mechanism
   - Timeout yang wajar (10-30 detik)

3. **Respect Server Resources**
   - Jangan scrape terlalu agresif
   - Gunakan delay antar request
   - Scrape di jam-jam off-peak

4. **Data Validation**
   - Validasi data sebelum disimpan
   - Handle null/empty values
   - Check `status` field di response

---

## 📝 Changelog

### 2025-11-26
- Initial API documentation
- Discovered all public endpoints
- Documented market IDs
- Added usage examples

---

## 📞 Support

Untuk informasi lebih lanjut, kunjungi:
- Website: https://infopangan.jakarta.go.id
- Contact: https://infopangan.jakarta.go.id/contact-us

---

**Note:** Dokumentasi ini dibuat berdasarkan reverse engineering website InfoPangan Jakarta dan bukan merupakan dokumentasi resmi. Gunakan dengan bijak dan bertanggung jawab.
