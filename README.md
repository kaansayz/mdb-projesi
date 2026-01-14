# MDB Dosyası Analiz Programı

Bu program Microsoft Access (.mdb) veritabanı dosyalarını okuyup analiz eder ve detaylı bir rapor oluşturur.

## 📋 Program Ne Yapar?

- ✅ MDB dosyasındaki tüm tabloları listeler
- ✅ Her tablonun sütunlarını ve veri tiplerini gösterir
- ✅ Kayıt sayılarını hesaplar
- ✅ Her tablodan örnek veriler gösterir (ilk 5 satır)
- ✅ Veritabanındaki sorguları (queries) listeler
- ✅ Tablo ilişkilerini gösterir
- ✅ Sonuçları hem ekrana yazdırır hem de `RAPOR.txt` dosyasına kaydeder

## 🚀 Kurulum

### Adım 1: Python Yükleme

Eğer bilgisayarınızda Python yoksa:

1. [Python indirme sayfasına](https://www.python.org/downloads/) gidin
2. Python 3.8 veya daha yeni bir sürüm indirin
3. Kurulum sırasında **"Add Python to PATH"** seçeneğini işaretleyin

### Adım 2: Microsoft Access Driver Kurulumu

MDB dosyalarını okuyabilmek için Access Driver gereklidir:

**Hangi sürümü indirmeliyim?**

Komut satırında şunu çalıştırarak Python sürümünüzü öğrenin:
```bash
python --version
```

Ardından Python'un kaç bit olduğunu öğrenin:
```bash
python -c "import struct; print(struct.calcsize('P') * 8, 'bit')"
```

**İndirme linkleri:**

- **32-bit Python için:** [Microsoft Access Database Engine 2010 (32-bit)](https://www.microsoft.com/en-us/download/details.aspx?id=13255)
- **64-bit Python için:** [Microsoft Access Database Engine 2016 (64-bit)](https://www.microsoft.com/en-us/download/details.aspx?id=54920)

**Önemli Not:** Eğer Microsoft Office yüklüyse, aynı bit sürümünde (32 veya 64-bit) driver indirmelisiniz.

### Adım 3: Gerekli Python Kütüphanelerini Yükleme

1. Komut satırını (CMD veya PowerShell) açın
2. Bu projenin klasörüne gidin:
   ```bash
   cd C:\yol\mdb-projesi
   ```
3. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Kullanım

### Basit Kullanım

**Yöntem 1: Varsayılan dosya ile**

1. Komut satırını (CMD veya PowerShell) açın
2. Proje klasörüne gidin (MDB dosyası ile aynı klasör olmalı)
3. Programı çalıştırın:
   ```bash
   python mdb_analiz.py
   ```

**Yöntem 2: Farklı bir MDB dosyası ile**

Başka bir MDB dosyasını analiz etmek için dosya adını parametre olarak verin:

```bash
python mdb_analiz.py "başka_dosya.mdb"
```

veya tam yol ile:

```bash
python mdb_analiz.py "C:\Belgeler\veritabanı.mdb"
```

Program çalışmaya başlayacak ve:
- Ekrana analiz sonuçlarını yazdıracak
- `RAPOR.txt` adında bir dosya oluşturacak

### Örnek Çıktı

```
🔍 MDB DOSYASI ANALİZ RAPORU
================================

📁 Dosya: 04.08.2025 İTİBAREN.mdb
📊 Toplam Tablo Sayısı: 3

──────────────────────────────────────────────────
📋 TABLO: Musteriler
──────────────────────────────────────────────────
📌 Sütunlar (4 adet):
  • ID (COUNTER)
  • Ad (VARCHAR)
  • Soyad (VARCHAR)
  • Telefon (VARCHAR)

📝 Kayıt Sayısı: 150

💾 Örnek Veriler (İlk 5 satır):
  ID | Ad | Soyad | Telefon
  --------------------------
  1 | Ahmet | Yılmaz | 555-1234
  2 | Ayşe | Kaya | 555-5678
  ...
```

## 📁 Dosya Yapısı

```
mdb-projesi/
│
├── 04.08.2025 İTİBAREN.mdb    # Access veritabanı dosyası
├── mdb_analiz.py               # Ana program
├── requirements.txt            # Gerekli kütüphaneler
├── README.md                   # Bu dosya
├── .gitignore                  # Git için görmezden gelinecek dosyalar
└── RAPOR.txt                   # Program çıktısı (otomatik oluşturulur)
```

## ❓ Sık Karşılaşılan Sorunlar

### "pyodbc modülü bulunamadı" hatası

**Çözüm:**
```bash
pip install pyodbc pandas
```

### "Microsoft Access Driver bulunamadı" hatası

**Çözüm:**
1. Python'unuzun 32-bit mi 64-bit mi olduğunu kontrol edin
2. Uygun Access Driver'ı indirip kurun (yukarıdaki linklere bakın)
3. Bilgisayarı yeniden başlatın
4. Programı tekrar çalıştırın

### "Dosya bulunamadı" hatası

**Çözüm:**
- Programı MDB dosyası ile aynı klasörde çalıştırdığınızdan emin olun
- Komut satırında `dir` (Windows) veya `ls` (Linux/Mac) komutu ile dosyaları kontrol edin

### Türkçe karakterler düzgün görünmüyor

**Çözüm:**
- RAPOR.txt dosyasını UTF-8 destekleyen bir editörde açın (Notepad++, VS Code, vb.)
- Windows Notepad'de açarken "Encoding" olarak "UTF-8" seçin

## 🛠️ Geliştirme

Bu program Python 3.8+ ile uyumludur ve şu kütüphaneleri kullanır:

- **pyodbc**: ODBC veritabanı bağlantısı için
- **pandas**: Veri analizi için (opsiyonel, gelişmiş özellikler için)

## 📝 Notlar

- Program sadece veri okur, MDB dosyasında hiçbir değişiklik yapmaz
- VBA modüllerini okumak için Microsoft Access uygulaması gerekir (ODBC ile erişilemez)
- Şifreli MDB dosyaları için ek yapılandırma gerekebilir

## 📞 Destek

Sorun yaşarsanız:
1. Önce "Sık Karşılaşılan Sorunlar" bölümüne bakın
2. `RAPOR.txt` dosyasındaki hata mesajlarını kontrol edin
3. GitHub'da issue açabilirsiniz

## 📄 Lisans

Bu proje eğitim amaçlı geliştirilmiştir.
