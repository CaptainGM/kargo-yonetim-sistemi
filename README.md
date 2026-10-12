# LogiRoute - Akıllı Kargo Dağıtım ve Rota Optimizasyonu

Türkiye genelinde 81 il ve 350'den fazla lojistik istasyonu arasında kargo dağıtımını simüle eden, güncel akaryakıt ve otoyol maliyetlerini baz alarak TSP (Gezgin Satıcı Problemi) ve Knapsack algoritmalarıyla en uygun rotayı ve araç yüklemesini hesaplayan web tabanlı lojistik yönetim platformu.

Harici ağır web çatıları (Django/Flask) yerine saf Python standart kütüphanesi (`http.server`), MongoDB veritabanı, Leaflet.js haritası ve OSRM açık kaynak yol servisi kullanılarak geliştirilmiştir.

---

## 📸 Ekran Görüntüleri

| Canlı Lojistik Dashboard | 81 İl ve 350+ İstasyon Ağı |
|---|---|
| ![Dashboard](screenshot.png) | ![Harita](harita.png) |
| **6 Sınıflı Araç Filosu** | **Neon Otoyollar & Canlı Simülasyon** |
| ![Araç Filosu](araclar.png) | ![Rota Planlama](rota-planlama.png) |

---

## ✨ Öne Çıkan Özellikler

- **350+ Lojistik İstasyon:** 81 il merkezi ve İç Anadolu başta olmak üzere tüm kritik ilçe, liman ve organize sanayi bölgeleri (OSB) gerçek GPS koordinatlarıyla tanımlıdır.
- **2026 Gerçekçi Akaryakıt & Maliyet Modeli:** Güncel pompa fiyatları (Motorin 92.50 TL/L, Benzin 85.50 TL/L, AdBlue 36.50 TL/L), Osmangazi ve otoyol geçiş ücretleri, şoför yevmiyesi ve karbon salınımı (CO₂) hesabı.
- **6 Farklı Araç Sınıfı:** Moto kuryeden Mega Scania TIR'a kadar farklı kapasite, hacim ve tüketim değerlerine sahip filo.
- **Optimizasyon Algoritmaları:**
  - **Knapsack / Backtracking & Greedy:** Araç kapasitesine en uygun kargo seçimi.
  - **TSP (2-Opt & Nearest Neighbor):** En kısa ve ekonomik güzergah sıralaması.
- **Canlı Komuta Merkezi (Dashboard):** 8 KPI kartı, Chart.js ile bölgesel yük ve maliyet pasta grafiği, canlı kargo takip tablosu.
- **Karizmatik Leaflet Haritası:** Parlayan çok katmanlı neon otoyollar ve rota üzerinde hız göstergesiyle hareket eden tır simülasyonu.

---

## 🚚 Araç Filosu ve Yakıt Tüketimleri

| Araç Sınıfı | Model / Tip | Kapasite | Hacim | Fabrika Tüketimi | km Maliyeti |
|---|---|---|---|---|---|
| Moto Kurye | Honda CBF 150 | 50 kg | 0.3 m³ | 3.5 L Benzin / 100 km | ~2.99 TL/km |
| Panelvan | Fiat Doblo Maxi | 400 kg | 4.2 m³ | 7.8 L Motorin / 100 km | ~7.22 TL/km |
| Kamyonet | Ford Transit 350L | 1.000 kg | 12.5 m³ | 11.5 L Motorin / 100 km | ~10.64 TL/km |
| Bölgesel Kamyon | Isuzu NPR Long | 2.500 kg | 28.0 m³ | 21.0 L Motorin / 100 km | ~19.43 TL/km |
| Ağır Vasıta | Axor 1840 | 6.000 kg | 50.0 m³ | 29.5 L Motorin / 100 km | ~27.29 TL/km |
| Mega Treyler TIR | Scania R450 | 15.000 kg | 95.0 m³ | 33.5 L Mot. + AdBlue | ~31.56 TL/km |

---

## 🛠️ Kullanılan Teknolojiler

- **Backend:** Python 3.9+ (`http.server`, `urllib`, `json`, `math`)
- **Veritabanı:** MongoDB (PyMongo)
- **Frontend:** Vanilla HTML5, CSS3, JavaScript (ES6+), FontAwesome
- **Harita & Rota:** Leaflet.js, OpenStreetMap, CartoDB, OSRM API
- **Grafikler:** Chart.js

---

## 🚀 Kurulum ve Çalıştırma

### 1. Kolay Başlatma (Windows)
MongoDB servisiniz çalışırken klasördeki dosyaya çift tıklayın:
```bat
start.bat
```

### 2. Manuel Başlatma (Terminal)
```bash
# Bağımlılıkları yükleyin
pip install -r requirements.txt

# MongoDB bağlantısı (varsayılan localhost:27017)
python app.py
```

### 3. Docker ile Başlatma
```bash
docker compose up
```

Tarayıcınızdan **`http://localhost:8000`** adresine gidin.

### 🔑 Giriş Bilgileri
- **Yönetici (Admin):** `admin` / `admin123`
- **Kullanıcı:** `user` / `user123`

---

## 📄 Lisans
Bu proje eğitim ve geliştirme amaçlı açık kaynak olarak hazırlanmıştır (MIT Lisansı).
