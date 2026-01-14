# MDB Projesi - Access Veritabanı Analiz Aracı

Bu proje, Microsoft Access veritabanı (.mdb) dosyalarını analiz eden bir Python scripti içerir. Script, veritabanı yapısını, tabloları, sütunları, ilişkileri ve sorguları otomatik olarak analiz eder ve detaylı bir rapor üretir.

## 📋 Özellikler

- ✅ Tüm tabloları listeler
- ✅ Her tablo için sütun adları ve veri tiplerini gösterir
- ✅ Tablolardaki kayıt sayılarını hesaplar
- ✅ Her tablodan ilk 5 satır örnek veri gösterir
- ✅ Tablolar arası ilişkileri (foreign keys) listeler
- ✅ Veritabanındaki sorguları (queries/views) listeler
- ✅ Sonuçları hem ekrana yazdırır hem de dosyaya kaydeder
- ✅ Türkçe karakter desteği (UTF-8)
- ✅ Detaylı hata yönetimi

## 🔧 Gereksinimler

### Yazılım Gereksinimleri

- Python 3.8 veya üzeri
- Windows işletim sistemi (Microsoft Access Driver için)
- Microsoft Access Database Engine (ODBC Driver)

### Python Kütüphaneleri

- `pyodbc` - ODBC veritabanı bağlantısı için
- `pandas` - Veri analizi ve tablo gösterimi için

## 📥 Kurulum

### 1. Python Kütüphanelerini Yükleyin

```bash
pip install -r requirements.txt
```

### 2. Microsoft Access Database Engine'i Yükleyin (Gerekiyorsa)

Eğer sisteminizde Microsoft Access kurulu değilse, Access Database Engine ODBC sürücüsünü yüklemeniz gerekir:

**Adımlar:**

1. [Microsoft Access Database Engine 2016 Redistributable](https://www.microsoft.com/en-us/download/details.aspx?id=54920) sayfasına gidin
2. Sisteminize uygun sürümü indirin:
   - 32-bit Python kullanıyorsanız: **AccessDatabaseEngine.exe**
   - 64-bit Python kullanıyorsanız: **AccessDatabaseEngine_X64.exe**
3. İndirdiğiniz dosyayı çalıştırın ve kurulumu tamamlayın

**Not:** Python sürümünüzü kontrol etmek için:
```bash
python --version
python -c "import struct; print(struct.calcsize('P') * 8, 'bit')"
```

### 3. Kullanılan Python Sürümünü Kontrol Edin

Script Python 3.8+ ile uyumludur. Eğer sisteminizde birden fazla Python sürümü varsa, doğru sürümü kullandığınızdan emin olun:

```bash
python --version
# veya
python3 --version
```

## 🚀 Kullanım

### Temel Kullanım

Script, aynı dizindeki `04.08.2025 İTİBAREN.mdb` dosyasını otomatik olarak analiz eder:

```bash
python mdb_analiz.py
```

### Farklı Bir MDB Dosyasını Analiz Etme

Komut satırından farklı bir dosya belirtebilirsiniz:

```bash
python mdb_analiz.py "C:\yol\dosya.mdb"
```

### Çıktı

Script çalıştığında:
1. Analiz sonuçları **ekrana** yazdırılır
2. Aynı içerik **RAPOR.txt** dosyasına kaydedilir

## 📊 Örnek Çıktı

```
🔍 MDB DOSYASI ANALİZ RAPORU
==================================================

📁 Dosya: 04.08.2025 İTİBAREN.mdb
📅 Analiz Tarihi: 14.01.2026 16:30:45
📊 Toplam Tablo Sayısı: 3

──────────────────────────────────────────────────
📋 TABLO: Musteriler
──────────────────────────────────────────────────
📝 Kayıt Sayısı: 125
📌 Sütunlar:
  - MusteriID (INTEGER)
  - Ad (VARCHAR)
  - Soyad (VARCHAR)
  - Telefon (VARCHAR)
  
💾 Örnek Veriler (İlk 5 satır):
  MusteriID      Ad    Soyad      Telefon
          1    Ahmet   Yılmaz  05321234567
          2   Mehmet    Demir  05421234567
  ...

──────────────────────────────────────────────────
🔗 İLİŞKİLER
──────────────────────────────────────────────────
  Siparisler.MusteriID -> Musteriler.MusteriID

──────────────────────────────────────────────────
📜 SORGULAR
──────────────────────────────────────────────────
  - AktifMusteriler
  - ToplamSiparisler

──────────────────────────────────────────────────
⚙️ VBA MODÜLLERİ
──────────────────────────────────────────────────
  Not: VBA modüllerinin okunması ODBC sürücüsü ile 
  desteklenmemektedir.

==================================================
✅ Analiz tamamlandı!

💾 Rapor kaydedildi: RAPOR.txt
```

## 🐛 Hata Giderme

### "Microsoft Access Driver bulunamadı" Hatası

**Çözüm:** Microsoft Access Database Engine'i yükleyin (bkz. Kurulum bölümü)

### "Dosya bulunamadı" Hatası

**Çözüm:** 
- MDB dosyasının doğru konumda olduğundan emin olun
- Dosya yolunu tam yol olarak belirtin
- Dosya adında Türkçe karakter varsa, dosya yolunu tırnak içinde verin

### Python Sürüm Uyumsuzluğu

**Çözüm:** Python 3.8 veya daha yeni bir sürüm kullanın:
```bash
python3 --version
```

### 32-bit vs 64-bit Uyumsuzluğu

**Çözüm:** Python versiyonunuz ile Access Database Engine versiyonunun (32-bit veya 64-bit) aynı olması gerekir.

## 📁 Proje Yapısı

```
mdb-projesi/
│
├── 04.08.2025 İTİBAREN.mdb    # Analiz edilecek veritabanı
├── mdb_analiz.py               # Ana analiz scripti
├── requirements.txt            # Python bağımlılıkları
├── .gitignore                  # Git ignore dosyası
├── README.md                   # Bu dosya
└── RAPOR.txt                   # Üretilen rapor (script çalıştırıldığında)
```

## 🔒 Güvenlik Notları

- Script, veritabanından sadece okuma yapar, hiçbir değişiklik yapmaz
- RAPOR.txt dosyası hassas veriler içerebilir, paylaşırken dikkatli olun
- Güvenlik nedeniyle RAPOR.txt dosyası `.gitignore` ile Git'e eklenmemiştir

## 📝 Lisans

Bu proje açık kaynaklıdır.

## 🤝 Katkıda Bulunma

Hata raporları ve öneriler için lütfen GitHub Issues bölümünü kullanın.

## ✨ Notlar

- VBA modüllerinin okunması ODBC sürücüsü ile mümkün değildir
- Çok büyük tablolar için örnek veri gösterimi zaman alabilir
- Script Windows işletim sisteminde test edilmiştir
