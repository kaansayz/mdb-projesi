# -*- coding: utf-8 -*-
"""
Cezaevi Gıda Takip Sistemi GUI - Kullanım Kılavuzu
"""

# GUI Kullanım Kılavuzu

## 🚀 Başlangıç

### Gereksinimler
```bash
pip install -r requirements.txt
```

### Uygulamayı Başlatma
```bash
python main.py
```

## 📱 Ana Özellikler

### 1. 🏠 Ana Sayfa (Dashboard)
Ana ekran şunları gösterir:
- **Cezaevi Bilgileri**: Cezaevi adı, müdür, ambar memuru
- **İstatistikler**: 
  - Günlük kişi sayıları (Sabah, Öğle, Akşam öğünleri)
  - Ekmek sayıları (Sabah, Öğle, Akşam)
- **Bugünün Özeti**:
  - Toplam maliyet
  - Toplam kalori
  - Ürün çeşidi
  - İşlem sayısı

**Özellikler**:
- Otomatik veri yenileme
- Renkli istatistik kartları
- Yenile butonu

---

### 2. 📦 Ürün Yönetimi
Ürünleri ekleyin, düzenleyin ve silin.

**Sol Panel - Ürün Listesi**:
- Tüm ürünleri görüntüleme
- Arama çubuğu (ürün adı veya birime göre)
- Treeview tablosu:
  - Ürün No
  - Ürün Adı
  - Birim
  - Fiyat (TL)
  - Kalori
  - Defter No

**Sağ Panel - Ürün Formu**:
- Ürün Adı (zorunlu)
- Birim (kg, adet, litre, vb.)
- Fiyat (TL)
- Kalori (kcal/100g)
- Defter No

**Butonlar**:
- ➕ **Yeni**: Yeni ürün ekle
- 📝 **Düzenle**: Seçili ürünü düzenle
- 🗑️ **Sil**: Seçili ürünü sil
- 💾 **Kaydet/Güncelle**: Değişiklikleri kaydet
- ↩️ **İptal**: Formu temizle

**Kullanım**:
1. Yeni ürün eklemek için "Yeni" butonuna tıklayın
2. Form alanlarını doldurun
3. "Kaydet" butonuna tıklayın
4. Ürün düzenlemek için listeden seçin ve "Düzenle" tıklayın
5. Değişiklikleri yapın ve "Güncelle" tıklayın

---

### 3. 📋 Günlük Tabela
Günlük yemek planlaması ve kayıt işlemleri.

**Üst Panel - Yeni Kayıt Formu**:

**Sol Taraf - Temel Bilgiler**:
- **Tarih**: Takvim seçici (dd.mm.yyyy)
- **Öğün**: SABAH / ÖĞLE / AKŞAM
- **Mevcut Kişi Sayısı**: O öğündeki toplam kişi sayısı

**Sağ Taraf - Ürün Bilgileri**:
- **Ürün**: Açılır listeden ürün seçimi
- **Verilen Miktar**: Dağıtılan miktar
- **Otomatik Hesaplamalar**:
  - Toplam Tutar
  - Kişi Başı Tutar
  - Kişi Başı Kalori

**Alt Panel - Günlük Kayıtlar**:
- Seçili tarih ve öğün için kayıtları gösterir
- Kolonlar:
  - Sıra No
  - Tarih
  - Öğün
  - Kişi Sayısı
  - Ürün
  - Verilen Miktar
  - Toplam Tutar
  - Kişi Başı Tutar
  - Kişi Başı Miktar
  - Kişi Başı Kalori

**Butonlar**:
- ➕ **Ekle**: Yeni kayıt ekle
- 🔄 **Yenile**: Kayıtları yenile
- 🗑️ **Sil**: Seçili kaydı sil

**Kullanım**:
1. Tarihi seçin
2. Öğünü seçin (SABAH/ÖĞLE/AKŞAM)
3. Mevcut kişi sayısını girin
4. Ürünü seçin
5. Verilen miktarı girin
6. Hesaplamaları kontrol edin
7. "Ekle" butonuna tıklayın

**Önemli Notlar**:
- Kişi başı değerler otomatik hesaplanır
- Ürün fiyatı ve kalorisi ürün tablosundan otomatik gelir
- Yanlış kayıt için "Sil" butonunu kullanın

---

### 4. 📊 Stok Takibi
Ürün bazlı stok durumu ve uyarı sistemi.

**Stok Durumu Göstergeleri**:
- 🔴 **KRİTİK** (≤10): Kırmızı arka plan - Acil sipariş gerekli
- 🟡 **UYARI** (≤50): Sarı arka plan - Stok azalıyor
- 🟢 **NORMAL** (>50): Yeşil arka plan - Stok yeterli

**Tablo Kolonları**:
- Ürün No
- Ürün Adı
- Birim
- Stok Miktarı
- Durum

**Özellikler**:
- Renkli uyarı sistemi
- Otomatik stok hesaplama
- Yenile butonu

**Kullanım**:
1. Stok durumunu kontrol edin
2. Kırmızı ve sarı uyarılara dikkat edin
3. Gerekli siparişleri verin
4. "Yenile" ile güncel durumu görün

**Not**: Stok miktarı, günlük tabela kayıtlarından otomatik hesaplanır.

---

### 5. 📈 Raporlar
Çeşitli raporlar oluşturun ve Excel'e aktarın.

**Üst Panel - Rapor Ayarları**:

**Rapor Tipleri**:
1. **Malzeme Giriş Raporu**:
   - Tarih, Ürün, Giriş Miktarı, Birim, Fiyat, Tutar

2. **Malzeme Çıkış Raporu**:
   - Tarih, Öğün, Ürün, Çıkış Miktarı, Birim, Fiyat, Tutar, Kişi Sayısı

3. **Ürün Bazlı Rapor**:
   - Ürün, Birim, Toplam Giriş, Toplam Çıkış, Toplam Tutar, İşlem Sayısı

4. **Günlük Özet Rapor**:
   - Tarih, Öğün, Ürün Sayısı, Toplam Miktar, Toplam Tutar, Ort. Kişi Tutar, Toplam Kalori

**Tarih Aralığı**:
- **Başlangıç Tarihi**: Raporun başlangıç tarihi
- **Bitiş Tarihi**: Raporun bitiş tarihi

**Alt Panel - Rapor Sonuçları**:
- Tablo formatında rapor görüntüleme
- Yatay ve dikey kaydırma

**Butonlar**:
- 📊 **Rapor Oluştur**: Seçili raporu oluştur
- 📥 **Excel'e Aktar**: Raporu Excel dosyasına kaydet

**Kullanım**:
1. Rapor tipini seçin
2. Başlangıç ve bitiş tarihlerini seçin
3. "Rapor Oluştur" butonuna tıklayın
4. Sonuçları inceleyin
5. "Excel'e Aktar" ile .xlsx dosyası olarak kaydedin

**Excel Özellikleri**:
- Otomatik kolon genişliği ayarı
- Başlık satırı formatlaması (mavi arka plan, beyaz yazı)
- Tarihli dosya adı (örn: Malzeme_Cikis_20250201.xlsx)

---

### 6. ⚙️ Ayarlar
Sistem ayarları ve cezaevi bilgilerini yönetin.

**Cezaevi Bilgileri**:
- Cezaevi Adı

**Personel Bilgileri**:
- Cezaevi Müdürü
- Ambar Memuru
- Komisyon Üye 1
- Komisyon Üye 2
- Komisyon Üye 3

**Günlük Öğün Kişi Sayıları**:
- Sabah Öğünü Kişi Sayısı
- Öğle Öğünü Kişi Sayısı
- Akşam Öğünü Kişi Sayısı
- Toplam Kişi Sayısı (otomatik hesaplanır)

**Günlük Ekmek Sayıları**:
- Sabah Ekmeği
- Öğle Ekmeği
- Akşam Ekmeği
- Toplam Ekmek (otomatik hesaplanır)

**Özellikler**:
- Otomatik toplam hesaplama
- Scrollable form (uzun formlar için)
- Tek tıkla kaydetme

**Kullanım**:
1. Bilgileri girin veya güncelleyin
2. Öğün ve ekmek sayıları girerken toplamlar otomatik hesaplanır
3. "Ayarları Kaydet" butonuna tıklayın
4. Ana sayfada güncel bilgileri görün

**Not**: Bu ayarlar ana sayfada ve raporlarda kullanılır.

---

## 🎨 Renk Kodları

Sistem genelinde kullanılan renkler:
- **Başarı** (#4CAF50): Yeşil - Olumlu durumlar
- **Hata** (#f44336): Kırmızı - Hatalar, kritik durumlar
- **Uyarı** (#ff9800): Turuncu - Dikkat gerektiren durumlar
- **Bilgi** (#2196F3): Mavi - Bilgilendirme, butonlar
- **Arka Plan** (#f0f0f0): Açık gri - Genel arka plan
- **Sidebar** (#2c3e50): Koyu mavi - Navigasyon menüsü

---

## 🔑 Kısayollar ve İpuçları

### Genel İpuçlar
1. **Navigasyon**: Sol menüden istediğiniz modüle geçiş yapın
2. **Arama**: Ürün Yönetimi'nde gerçek zamanlı arama yapın
3. **Seçim**: Treeview'lerde tek tıklama ile seçim yapın
4. **Tarih**: DateEntry ile kolayca tarih seçin

### Validasyon
- Boş alanlar kabul edilmez (zorunlu alanlar)
- Sayısal alanlar kontrol edilir
- Negatif değerler kabul edilmez
- Türkçe virgül (,) ve nokta (.) desteklenir

### Hesaplamalar
- Kişi başı değerler otomatik hesaplanır
- Toplam tutar = Verilen Miktar × Fiyat
- Kişi başı tutar = Toplam Tutar / Kişi Sayısı
- Kişi başı kalori = (Verilen Miktar × Kalori) / Kişi Sayısı

### Veritabanı
- SQLite veritabanı kullanılır
- Veritabanı: `data/cezaevi_gida.db`
- İlk çalıştırmada otomatik oluşturulur
- MDB dosyasından veri aktarımı yapılabilir

---

## ❗ Sorun Giderme

### Veritabanı Bulunamadı
**Sorun**: "Veritabanı dosyası bulunamadı" hatası
**Çözüm**: 
1. MDB dosyasını proje dizinine koyun
2. Evet'e tıklayarak import işlemini başlatın
3. Veya boş veritabanı ile devam edin

### Modül Bulunamadı
**Sorun**: ImportError veya ModuleNotFoundError
**Çözüm**:
```bash
pip install -r requirements.txt
```

### PyODBC Hatası
**Sorun**: MDB import sırasında pyodbc hatası
**Çözüm**:
1. Windows'ta: Microsoft Access Database Engine yükleyin
2. Linux'ta: mdbtools yükleyin
3. Veya CSV export/import kullanın

### Türkçe Karakter Sorunu
**Sorun**: Türkçe karakterler düzgün görünmüyor
**Çözüm**: Tüm dosyalar UTF-8 encoding kullanır, sistem ayarlarınızı kontrol edin

### Excel Export Hatası
**Sorun**: Excel'e aktarma başarısız
**Çözüm**:
```bash
pip install openpyxl
```

---

## 🔧 Teknik Detaylar

### Mimari
```
main.py                 # Ana uygulama ve navigasyon
├── gui/
│   ├── ana_ekran.py       # Dashboard
│   ├── urun_yonetimi.py   # Ürün CRUD
│   ├── gunluk_tabela.py   # Günlük planlama
│   ├── stok_takibi.py     # Stok görüntüleme
│   ├── raporlar.py        # Raporlama
│   └── ayarlar.py         # Ayarlar
├── database.py         # Veritabanı işlemleri
└── utils/
    ├── hesaplamalar.py # Hesaplama fonksiyonları
    └── validasyon.py   # Validasyon fonksiyonları
```

### Kullanılan Kütüphaneler
- **tkinter**: GUI framework
- **ttkthemes**: Modern tema desteği
- **tkcalendar**: Tarih seçici
- **sqlite3**: Veritabanı
- **openpyxl**: Excel export
- **pyodbc**: MDB import (opsiyonel)

### Veritabanı Şeması
- **cezaevi_bilgileri**: Cezaevi ve personel bilgileri
- **urunler**: Ürün listesi
- **gunluk_tabela**: Günlük yemek kayıtları
- **firmalar**: Firma listesi (opsiyonel)
- **memurlar**: Memur listesi (opsiyonel)
- **raporlar**: Rapor tanımları (opsiyonel)

---

## 📞 Destek

Sorun yaşarsanız:
1. Hata mesajını okuyun
2. Log dosyalarını kontrol edin
3. GitHub Issues'da arama yapın
4. Yeni issue açın (varsa)

---

## 📝 Notlar

- Tüm veriler yerel SQLite veritabanında saklanır
- Düzenli yedekleme yapmanız önerilir
- Veritabanı dosyası: `data/cezaevi_gida.db`
- Excel raporları otomatik tarihle kaydedilir
- Sistem UTF-8 encoding kullanır (Türkçe karakter desteği)

---

**Geliştirici**: Cezaevi Gıda Takip Sistemi v1.0.0
**Tarih**: 2025
**Lisans**: Proje lisansına bakınız
