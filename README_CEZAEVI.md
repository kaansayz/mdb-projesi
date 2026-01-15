# 🏛️ Cezaevi Gıda Takip Sistemi

Modern ve kullanıcı dostu **Python GUI uygulaması** ile cezaevi gıda ihtiyaçlarını takip edin!

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)

## 📋 İçindekiler

- [Genel Bakış](#-genel-bakış)
- [Özellikler](#-özellikler)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [Modüller](#-modüller)
- [Veritabanı](#-veritabanı)
- [Katkıda Bulunma](#-katkıda-bulunma)

## 🎯 Genel Bakış

**Cezaevi Gıda Takip Sistemi**, cezaevlerinin günlük gıda ihtiyaçlarını, stok durumunu ve maliyetleri takip etmek için geliştirilmiş modern bir masaüstü uygulamasıdır. Access MDB dosyasındaki mevcut verileri SQLite veritabanına aktararak daha hızlı ve güvenilir bir çözüm sunar.

### 🌟 Ana Özellikler

- ✅ **Modern GUI Arayüzü** - Temiz ve kullanıcı dostu tkinter tabanlı arayüz
- ✅ **Ürün Yönetimi** - Ekle, düzenle, sil, ara
- ✅ **Günlük Tabela** - Öğün bazlı gıda kayıtları ve otomatik hesaplamalar
- ✅ **Stok Takibi** - Renkli uyarı sistemi ile stok kontrolü
- ✅ **Raporlama** - Excel'e dışa aktarma ile detaylı raporlar
- ✅ **Ayarlar** - Cezaevi ve personel bilgileri yönetimi
- ✅ **MDB İmport** - Access veritabanından otomatik veri aktarımı

## ✨ Özellikler

### 🏠 Ana Ekran (Dashboard)

- Cezaevi genel bilgileri
- Günlük öğün sayıları (Sabah/Öğle/Akşam)
- Günlük ekmek miktarları
- Bugünün özeti (toplam maliyet, kalori, ürün sayısı)
- Renkli istatistik kartları

### 📦 Ürün Yönetimi

- Tüm ürünleri listele (tablo görünümü)
- Ürün ara (isim, birim bazlı)
- Yeni ürün ekle
- Ürün bilgilerini düzenle
- Ürün sil (onay ile)
- Sütunlar: Ürün No, Cinsi, Birimi, Fiyatı, Kalorisi, Defter No

### 📋 Günlük Tabela

- Tarih seçimi (takvim widget)
- Öğün seçimi (Sabah/Öğle/Akşam)
- Mevcut kişi sayısı
- Ürün seçimi ve miktar girişi
- **Otomatik Hesaplama:**
  - Toplam tutar
  - Kişi başı tutar
  - Kişi başı miktar
  - Kişi başı kalori
- Kayıtları listele ve sil

### 📊 Stok Takibi

- Ürün bazında stok görünümü
- Renkli uyarı sistemi:
  - 🔴 Kırmızı: Stok < 10 (Kritik)
  - 🟡 Sarı: Stok < 50 (Uyarı)
  - 🟢 Yeşil: Stok >= 50 (Normal)
- Anlık stok yenileme

### 📈 Raporlar

4 farklı rapor türü:

1. **Malzeme Girişleri** - Tarih aralığında giriş yapılan ürünler
2. **Malzeme Çıkışları** - Tarih aralığında kullanılan ürünler
3. **Ürün Bazlı** - Ürünlere göre toplam giriş/çıkış
4. **Günlük Özet** - Seçilen tarihteki tüm işlemler

**Excel Dışa Aktarma:**
- Başlık satırı (kalın, renkli)
- Otomatik sütun genişliği
- Toplam satırı
- Dosya adı: `rapor_YYYYMMDD_HHMMSS.xlsx`

### ⚙️ Ayarlar

- Cezaevi bilgileri düzenleme
- Personel bilgileri:
  - Cezaevi Müdürü
  - Ambar Memuru
  - Komisyon Üyeleri (1, 2, 3)
- Günlük öğün sayıları (otomatik toplam)
- Günlük ekmek miktarları (otomatik toplam)

## 🔧 Kurulum

### Gereksinimler

- **Python 3.8** veya üzeri
- **Windows** işletim sistemi (Access driver için)
- **Microsoft Access Database Engine** (MDB import için)

### Adım 1: Repository'yi Klonlayın

```bash
git clone https://github.com/kaansayz/mdb-projesi.git
cd mdb-projesi
```

### Adım 2: Gerekli Kütüphaneleri Yükleyin

```bash
pip install -r requirements.txt
```

Kurulacak kütüphaneler:
- `pyodbc>=4.0.35` - Access veritabanı bağlantısı
- `pandas>=1.5.0` - Veri işleme
- `ttkthemes>=3.2.2` - Modern temalar
- `openpyxl>=3.0.10` - Excel export
- `pillow>=9.0.0` - Görsel işleme
- `tkcalendar>=1.6.1` - Tarih seçici widget

### Adım 3: Access Database Engine Yükleyin

**Windows için gerekli!** (MDB import için)

1. [Microsoft Access Database Engine 2016 Redistributable](https://www.microsoft.com/en-us/download/details.aspx?id=54920) indirin
2. Sisteminize uygun versiyonu yükleyin:
   - **64-bit Python**: `AccessDatabaseEngine_X64.exe`
   - **32-bit Python**: `AccessDatabaseEngine.exe`

Python bit sürümünü kontrol:
```bash
python -c "import struct; print(struct.calcsize('P') * 8, 'bit')"
```

## 🚀 Kullanım

### İlk Çalıştırma

```bash
python main.py
```

**İlk çalıştırmada:**
1. Uygulama veritabanının varlığını kontrol eder
2. Veritabanı yoksa MDB import için onay ister
3. Onay verilirse `04.08.2025 İTİBAREN.mdb` dosyasından veri aktarır
4. Ana ekran açılır

### Manuel Veri İmport

```bash
python mdb_importer.py
```

Bu komut MDB dosyasındaki tüm verileri SQLite'a aktarır:
- Cezaevi bilgileri
- Ürünler (414 kayıt)
- Günlük tabela (24,671+ kayıt)
- Firmalar
- Memurlar

### Veritabanını Sıfırdan Oluşturma

```bash
python database.py
```

Bu komut boş bir SQLite veritabanı oluşturur.

## 📖 Modüller

### Ana Uygulama (`main.py`)

- 900x700 piksel minimum pencere boyutu
- Sol navigasyon menüsü
- Sağ içerik alanı
- Dinamik modül yükleme
- Veritabanı bağlantı yönetimi

### GUI Modülleri

```
gui/
├── __init__.py
├── ana_ekran.py       # Dashboard
├── urun_yonetimi.py   # Ürün CRUD
├── gunluk_tabela.py   # Öğün kaydı
├── stok_takibi.py     # Stok görünümü
├── raporlar.py        # Raporlama
└── ayarlar.py         # Ayarlar
```

### Yardımcı Modüller

```
utils/
├── __init__.py
├── hesaplamalar.py    # Maliyet/kalori hesaplamaları
└── validasyon.py      # Veri doğrulama
```

### Veritabanı

- `database.py` - SQLite işlemleri
- `mdb_importer.py` - MDB -> SQLite dönüştürücü
- `data/cezaevi_gida.db` - SQLite veritabanı dosyası

## 💾 Veritabanı

### Tablolar

1. **cezaevi_bilgileri** - Cezaevi ve personel bilgileri
2. **urunler** - Ürün kataloğu
3. **gunluk_tabela** - Günlük öğün kayıtları
4. **firmalar** - Tedarikçi firmaları
5. **memurlar** - Memur listesi
6. **raporlar** - Rapor tanımları

### Schema

```sql
-- Örnek: Ürünler tablosu
CREATE TABLE urunler (
    urun_no INTEGER PRIMARY KEY AUTOINCREMENT,
    cinsi TEXT NOT NULL,
    defter_no INTEGER,
    kalorisi INTEGER DEFAULT 0,
    birimi TEXT,
    fiyati REAL DEFAULT 0
);
```

Detaylı schema için `database.py` dosyasına bakın.

## 🎨 Ekran Görüntüleri

### Ana Ekran
![Ana Ekran](docs/screenshots/dashboard.png)

### Ürün Yönetimi
![Ürün Yönetimi](docs/screenshots/urun_yonetimi.png)

### Günlük Tabela
![Günlük Tabela](docs/screenshots/gunluk_tabela.png)

### Raporlar
![Raporlar](docs/screenshots/raporlar.png)

## 🐛 Sorun Giderme

### "pyodbc modülü bulunamadı"
```bash
pip install pyodbc
```

### "Microsoft Access Driver bulunamadı"
1. Access Database Engine indirin ve kurun
2. Python bit sürümü ile driver bit sürümü aynı olmalı
3. Bilgisayarı yeniden başlatın

### "tkinter modülü bulunamadı" (Linux)
```bash
sudo apt-get install python3-tk
```

### "Veritabanı bulunamadı"
İlk çalıştırmada otomatik oluşturulur. Manuel oluşturmak için:
```bash
python database.py
```

### MDB Import Başarısız
1. MDB dosyasının proje dizininde olduğundan emin olun
2. Access Database Engine kurulu olmalı
3. MDB dosyası başka bir program tarafından açık olmamalı

## 📚 Dokümantasyon

- **GUI_KULLANIM.md** - Detaylı kullanım kılavuzu
- **README_GUI.md** - Proje genel bakış
- **database.py** - API dokümantasyonu (docstrings)

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/yeni-ozellik`)
3. Commit yapın (`git commit -m 'feat: Yeni özellik ekle'`)
4. Push yapın (`git push origin feature/yeni-ozellik`)
5. Pull Request açın

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 👨‍💻 Geliştirici

**Kaan Sayz**

- GitHub: [@kaansayz](https://github.com/kaansayz)

## 🙏 Teşekkürler

- Python topluluğu
- tkinter ve ttkthemes geliştiricileri
- pyodbc kütüphanesi geliştiricileri
- openpyxl kütüphanesi geliştiricileri

## 📞 İletişim

Sorularınız veya önerileriniz için:
- **Issue** açın: [GitHub Issues](https://github.com/kaansayz/mdb-projesi/issues)

---

## 🔥 Hızlı Başlangıç

```bash
# 1. Klonla
git clone https://github.com/kaansayz/mdb-projesi.git
cd mdb-projesi

# 2. Kütüphaneleri kur
pip install -r requirements.txt

# 3. Uygulamayı başlat
python main.py
```

---

⭐ Projeyi beğendiyseniz yıldız vermeyi unutmayın!
