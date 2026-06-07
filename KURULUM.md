# GlobalStock Advisor — Backend Kurulum Kılavuzu

Bu kılavuz, backend'i (1) kendi bilgisayarında test etmeyi ve (2) Render.com'a
ücretsiz deploy etmeyi adım adım anlatır.

---

## 1. KENDİ BİLGİSAYARINDA TEST (opsiyonel ama önerilir)

İlk önce yerelde çalıştırıp gerçek veriyle sonuçları görmek için:

```bash
# 1. Python 3.11+ kurulu olmalı
python --version

# 2. Klasöre gir
cd stockadvisor

# 3. Sanal ortam oluştur (önerilir)
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Bağımlılıkları kur
pip install -r requirements.txt

# 5. (Opsiyonel) FMP API anahtarını ayarla — temel analiz modelleri için
# Windows:
set FMP_API_KEY=senin_anahtarin
# Mac/Linux:
export FMP_API_KEY=senin_anahtarin

# 6. Sunucuyu başlat
uvicorn app.main:app --reload
```

Tarayıcıda aç:
- http://localhost:8000/                → sağlık kontrolü
- http://localhost:8000/markets         → piyasa listesi
- http://localhost:8000/strategies      → model listesi
- http://localhost:8000/scan?market=BIST100&strategy=momentum  → ilk tarama!
- http://localhost:8000/docs            → otomatik API arayüzü (Swagger)

> İlk `/scan` çağrısı 30-60 saniye sürebilir (tüm piyasayı çekiyor).
> İkinci çağrı (aynı piyasa) cache sayesinde anında gelir.

---

## 2. FMP API ANAHTARI ALMA (temel analiz için)

Value, Growth, GARP, Quality modelleri FMP verisi ister.

1. https://site.financialmodelingprep.com/developer/docs adresine git
2. Ücretsiz hesap aç
3. Dashboard'dan API anahtarını kopyala (günde 250 istek ücretsiz)
4. Bu anahtarı Render'da `FMP_API_KEY` ortam değişkenine koyacaksın (aşağıda)

> FMP anahtarı OLMADAN da uygulama çalışır — sadece teknik modeller
> (Momentum, Trend, Relative Strength, Mean Reversion, Low Volatility) aktif olur.

---

## 3. RENDER.COM'A DEPLOY

### 3a. Kodu GitHub'a yükle

1. github.com'da yeni bir repo aç (örn. `globalstock-advisor`)
2. Bu klasördeki tüm dosyaları repoya yükle:

```bash
cd stockadvisor
git init
git add .
git commit -m "İlk backend"
git branch -M main
git remote add origin https://github.com/KULLANICI_ADIN/globalstock-advisor.git
git push -u origin main
```

### 3b. Render'da servis oluştur

1. https://render.com adresine git, ücretsiz hesap aç (GitHub ile giriş kolay)
2. **New +** → **Web Service**
3. GitHub repo'nu seç (`globalstock-advisor`)
4. Ayarlar otomatik gelir (render.yaml sayesinde), yine de kontrol et:
   - **Runtime:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free
5. **Environment** sekmesinde değişken ekle:
   - Key: `FMP_API_KEY`  →  Value: (FMP'den aldığın anahtar)
6. **Create Web Service** → deploy başlar (2-3 dakika)

Bittiğinde sana şuna benzer bir adres verir:
`https://globalstock-advisor-api.onrender.com`

Test et:
`https://globalstock-advisor-api.onrender.com/scan?market=BIST100&strategy=momentum`

---

## 4. UYKU MODUNU ÖNLEME (UptimeRobot)

Render ücretsiz plan 15 dk işlem olmazsa uyur. Çözüm:

1. https://uptimerobot.com → ücretsiz hesap aç
2. **Add New Monitor**
   - Monitor Type: **HTTP(s)**
   - Friendly Name: `StockAdvisor`
   - URL: `https://globalstock-advisor-api.onrender.com/`
   - Monitoring Interval: **5 dakika**
3. Kaydet. Artık her 5 dakikada ping atıp backend'i uyanık tutar.

---

## 5. ENDPOINT ÖZETİ (mobil uygulamanın kullanacağı)

| Endpoint | Açıklama |
|----------|----------|
| `GET /markets` | Piyasa listesi (dropdown) |
| `GET /strategies` | Model listesi (butonlar) |
| `GET /scan?market={id}&strategy={id}&limit=25` | Tarama sonucu |
| `GET /disclaimer` | Yasal uyarı metni |

`/scan` cevabı örneği:
```json
{
  "market": "BIST100",
  "strategy": "momentum",
  "count": 8,
  "results": [
    {
      "symbol": "ASELS.IS",
      "name": "Aselsan",
      "price": 142.5,
      "change_pct": 1.8,
      "score": 34.2,
      "tags": ["6M +34%", "RSI 64"]
    }
  ],
  "disclaimer": "This application provides information for educational..."
}
```

---

## SONRAKİ ADIMLAR

- Eşik değerlerini gerçek sonuçlara göre ince ayar (strategies.py)
- Endeks listelerini otomatik güncelleyen updater.py (sonra eklenecek)
- React Native mobil uygulama (Aşama 5)
