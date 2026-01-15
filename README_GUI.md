# Cezaevi Gıda Takip Sistemi - GUI Uygulaması

Modern, kullanıcı dostu bir cezaevi gıda takip ve yönetim sistemi.

## 🎯 Özellikler

### Ana Modüller

1. **📊 Ana Sayfa (Dashboard)**
   - Cezaevi bilgileri
   - Günlük öğün ve ekmek sayıları
   - Bugünün maliyet ve kalori özeti
   - Renkli istatistik kartları

2. **📦 Ürün Yönetimi**
   - Ürün ekleme, düzenleme, silme (CRUD)
   - Gerçek zamanlı arama
   - Ürün listesi (Ad, Birim, Fiyat, Kalori, Defter No)

3. **📋 Günlük Tabela**
   - Tarih ve öğün seçimi
   - Ürün seçimi ve miktar girişi
   - Otomatik hesaplamalar (tutar, kişi başı değerler)
   - Günlük kayıt listeleme

4. **📊 Stok Takibi**
   - Ürün bazlı stok görüntüleme
   - Renkli uyarı sistemi:
     - 🔴 Kritik (≤10)
     - 🟡 Uyarı (≤50)
     - 🟢 Normal (>50)

5. **📈 Raporlar**
   - Malzeme Giriş Raporu
   - Malzeme Çıkış Raporu
   - Ürün Bazlı Rapor
   - Günlük Özet Rapor
   - Excel'e aktarma (xlsx)

6. **⚙️ Ayarlar**
   - Cezaevi bilgileri
   - Personel bilgileri (Müdür, Memur, Komisyon Üyeleri)
   - Günlük öğün kişi sayıları
   - Günlük ekmek sayıları

## 🚀 Kurulum

### Gereksinimler

```bash
Python 3.8+
```

### Bağımlılıkları Yükleme

```bash
pip install -r requirements.txt
```

Gerekli paketler:
- tkinter (Python ile birlikte gelir)
- tkcalendar (Tarih seçici)
- openpyxl (Excel export)
- pyodbc (MDB import - opsiyonel)

## 📖 Kullanım

### Uygulamayı Başlatma

```bash
python main.py
```

### İlk Çalıştırma

1. Uygulama başlatıldığında veritabanı kontrolü yapılır
2. Veritabanı yoksa:
   - MDB dosyasından import yapabilirsiniz
   - Veya boş veritabanı ile devam edebilirsiniz
3. Ana ekran açılır ve kullanıma hazır olur

### Temel İşlemler

#### Ürün Ekleme
1. Sol menüden "Ürün Yönetimi"ne tıklayın
2. "Yeni" butonuna basın
3. Form alanlarını doldurun
4. "Kaydet" butonuna tıklayın

#### Günlük Tabela Oluşturma
1. Sol menüden "Günlük Tabela"ya tıklayın
2. Tarih seçin
3. Öğün seçin (SABAH/ÖĞLE/AKŞAM)
4. Mevcut kişi sayısını girin
5. Ürün seçin
6. Verilen miktarı girin
7. "Ekle" butonuna tıklayın

#### Rapor Oluşturma
1. Sol menüden "Raporlar"a tıklayın
2. Rapor tipini seçin
3. Tarih aralığını belirleyin
4. "Rapor Oluştur" butonuna tıklayın
5. Excel'e aktarmak için "Excel'e Aktar" butonunu kullanın

## 🎨 Tasarım

### Renkler

- **Başarı**: #4CAF50 (Yeşil)
- **Hata**: #f44336 (Kırmızı)
- **Uyarı**: #ff9800 (Turuncu)
- **Bilgi**: #2196F3 (Mavi)
- **Arka Plan**: #f0f0f0 (Açık Gri)
- **Sidebar**: #2c3e50 (Koyu Mavi)

### Pencere Boyutları

- **Minimum**: 900x700 piksel
- **Varsayılan**: 1200x750 piksel
- **Yeniden boyutlandırılabilir**: Evet

## 📁 Dosya Yapısı

```
mdb-projesi/
├── main.py                 # Ana uygulama
├── database.py             # Veritabanı işlemleri
├── mdb_importer.py         # MDB import
├── requirements.txt        # Bağımlılıklar
├── GUI_KULLANIM.md        # Detaylı kullanım kılavuzu
├── README_GUI.md          # Bu dosya
├── gui/
│   ├── __init__.py
│   ├── ana_ekran.py       # Dashboard modülü
│   ├── urun_yonetimi.py   # Ürün yönetimi
│   ├── gunluk_tabela.py   # Günlük planlama
│   ├── stok_takibi.py     # Stok takibi
│   ├── raporlar.py        # Raporlar
│   └── ayarlar.py         # Ayarlar
├── utils/
│   ├── hesaplamalar.py    # Hesaplama fonksiyonları
│   └── validasyon.py      # Validasyon fonksiyonları
└── data/
    └── cezaevi_gida.db    # SQLite veritabanı
```

## 🔧 Teknik Detaylar

### Veritabanı

- **Tip**: SQLite
- **Dosya**: `data/cezaevi_gida.db`
- **Encoding**: UTF-8

### Tablolar

1. **cezaevi_bilgileri**: Cezaevi ve personel bilgileri
2. **urunler**: Ürün listesi
3. **gunluk_tabela**: Günlük yemek kayıtları
4. **firmalar**: Firma listesi (opsiyonel)
5. **memurlar**: Memur listesi (opsiyonel)

### Hesaplamalar

```python
# Toplam tutar
tutar = verilen_miktar × fiyat

# Kişi başı tutar
sahis_tutar = tutar / mevcut_kisi

# Kişi başı miktar
sahis_miktar = verilen_miktar / mevcut_kisi

# Kişi başı kalori
sahis_kalori = (verilen_miktar × kalori) / mevcut_kisi
```

## 🛡️ Güvenlik

- ✅ Input validasyonu yapılır
- ✅ SQL injection koruması (parametreli sorgular)
- ✅ XSS koruması (string sanitization)
- ✅ Hata yönetimi (try-except)
- ✅ CodeQL güvenlik taraması geçti

## 🐛 Sorun Giderme

### Veritabanı Bulunamadı
```
Çözüm: İlk açılışta MDB dosyasını import edin veya boş DB ile devam edin
```

### Modül Bulunamadı
```bash
pip install -r requirements.txt
```

### Türkçe Karakter Sorunu
```
Tüm dosyalar UTF-8 encoding kullanır
```

### Excel Export Hatası
```bash
pip install openpyxl
```

## 📚 Dokümantasyon

Detaylı kullanım kılavuzu için:
```
GUI_KULLANIM.md dosyasına bakın
```

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun
3. Değişikliklerinizi commit edin
4. Branch'i push edin
5. Pull Request açın

## 📝 Lisans

Proje lisansına bakınız.

## 📞 Destek

- GitHub Issues: Sorun bildirimi
- Dokümantasyon: GUI_KULLANIM.md

## 🎉 Özellikler

- ✅ Modern ve temiz arayüz
- ✅ Türkçe dil desteği
- ✅ Kolay kullanım
- ✅ Hızlı performans
- ✅ Renkli istatistikler
- ✅ Excel export
- ✅ Otomatik hesaplamalar
- ✅ Validasyon ve hata yönetimi
- ✅ Responsive tasarım

## 🔄 Güncelleme Geçmişi

### v1.0.0 (2025)
- İlk sürüm
- Tüm temel modüller eklendi
- Modern GUI tasarımı
- Excel export özelliği
- Stok takibi ve uyarı sistemi
- Otomatik hesaplamalar
- Türkçe dil desteği

---

**Geliştirici**: Cezaevi Gıda Takip Sistemi  
**Versiyon**: 1.0.0  
**Yıl**: 2025
