# Changelog

Bu dosya projedeki tüm önemli değişiklikleri içerir.

Format [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) standardına dayanır,
ve bu proje [Semantic Versioning](https://semver.org/spec/v2.0.0.html) kullanır.

## [Unreleased]

### Planlanıyor
- CSV export desteği
- Excel export desteği
- Toplu dosya analizi
- Grafik ve chart gösterimi
- İlişki diyagramları
- Tablo filtreleme
- Veri arama özelliği
- PDF rapor export

## [1.0.0] - 2026-01-14

### Eklendi
- 🎨 Modern GUI arayüzü (tkinter)
- 📁 Dosya seçim dialogu (.mdb, .accdb)
- 🔍 MDB dosya analizi
- 📊 Tablo listeleme ve detaylı analiz
- 📋 Sütun bilgileri (ad, tip, boyut)
- 📈 Kayıt sayısı gösterimi
- 📝 İlk 5 örnek veri görüntüleme
- 🔎 Sorgu ve görünüm listeleme
- 💾 TXT formatında rapor kaydetme
- ⏱️ İşlem süresi göstergesi
- 📊 İlerleme çubuğu (progress bar)
- 🌙 Açık/Koyu tema desteği
- 🎨 Renkli sonuç gösterimi
- 🧵 Threading ile donmama önleme
- 🛡️ Kapsamlı hata yönetimi
- 📱 Responsive tasarım
- 🌍 Türkçe karakter tam desteği (UTF-8)
- ⌨️ ESC tuşu ile çıkış
- 🗑️ Sonuçları temizleme özelliği
- 📄 Durum çubuğu (status bar)
- 💾 Dışa aktarma menüsü
- 📚 Kapsamlı README.md
- 📖 Detaylı build talimatları
- 🏗️ PyInstaller build scripti
- 🧪 Kod validasyon scripti
- 🎭 Demo/gösterim scripti
- 📖 Kullanım örnekleri dokümantasyonu
- 📜 MIT Lisansı
- 📦 requirements.txt

### Teknik Detaylar
- Python 3.8+ uyumlu
- pyodbc ile veritabanı bağlantısı
- tkinter GUI framework
- Threading ile async işlemler
- UTF-8 encoding
- Cross-platform kod yapısı (Windows öncelikli)

### Dokümantasyon
- README.md - Genel kullanım kılavuzu
- build_instructions.md - .exe oluşturma talimatları
- USAGE.md - Detaylı kullanım örnekleri ve SSS
- demo.py - Uygulama özelliklerinin gösterimi
- test_code.py - Kod validasyon aracı

### Bilinen Sınırlamalar
- CSV export henüz çalışmıyor (placeholder)
- Excel export henüz çalışmıyor (placeholder)
- Linux'ta Access Database Engine gerekli
- Tek dosya analizi (toplu analiz yok)
- VBA modül detayları gösterilmiyor

### Gelecek Versiyonlar İçin Planlar

#### v1.1.0 (Planlanıyor)
- CSV export implementasyonu
- Excel export implementasyonu
- Gelişmiş filtreleme
- Arama özelliği

#### v1.2.0 (Planlanıyor)
- Toplu dosya analizi
- Karşılaştırma modu
- Grafik gösterimler

#### v1.3.0 (Planlanıyor)
- İlişki diyagramları
- VBA kod görüntüleme
- PDF export

#### v2.0.0 (Uzun Vadeli)
- Web-based arayüz
- API endpoint'leri
- Veritabanı editör
- SQL sorgu çalıştırma

## Versiyon Notları

### Semantic Versioning

Format: `MAJOR.MINOR.PATCH`

- **MAJOR:** API'de geriye dönük uyumsuz değişiklikler
- **MINOR:** Geriye dönük uyumlu yeni özellikler
- **PATCH:** Geriye dönük uyumlu hata düzeltmeleri

### Destek Politikası

- **Aktif Geliştirme:** Son major versiyon
- **Güvenlik Güncellemeleri:** Son 2 major versiyon
- **Bug Düzeltmeleri:** Son major versiyon

### Bağımlılık Versiyonları

#### v1.0.0
```
pyodbc >= 4.0.35
pandas >= 1.5.0
ttkthemes >= 3.2.2
openpyxl >= 3.0.10
pillow >= 9.0.0
```

## Katkıda Bulunanlar

- **Kaan Sayz** - Initial work - [@kaansayz](https://github.com/kaansayz)

## Teşekkürler

- Python topluluğuna
- tkinter geliştiricilerine
- pyodbc kütüphanesi geliştiricilerine
- Tüm katkıda bulunanlara

---

[Unreleased]: https://github.com/kaansayz/mdb-projesi/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/kaansayz/mdb-projesi/releases/tag/v1.0.0
