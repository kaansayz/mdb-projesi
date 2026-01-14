# 🗂️ MDB Dosya Analiz Programı

Modern ve kullanıcı dostu **pencereli (GUI) masaüstü uygulaması** ile Microsoft Access (.mdb) veritabanı dosyalarını analiz edin!

![Build Status](https://github.com/kaansayz/mdb-projesi/actions/workflows/build-exe.yml/badge.svg)
![GitHub release](https://img.shields.io/github/v/release/kaansayz/mdb-projesi)
![Downloads](https://img.shields.io/github/downloads/kaansayz/mdb-projesi/total)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)

## 📋 İçindekiler

- [Hızlı Kurulum - EXE İndir](#-hızlı-kurulum---exe-i̇ndir-python-gerektirmez)
- [Özellikler](#-özellikler)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [Ekran Görüntüleri](#-ekran-görüntüleri)
- [Gereksinimler](#-gereksinimler)
- [Sorun Giderme](#-sorun-giderme)

## 📦 Hızlı Kurulum - EXE İndir (Python Gerektirmez!)

### Windows Kullanıcıları İçin En Kolay Yol:

1. **[Releases](https://github.com/kaansayz/mdb-projesi/releases/latest)** sayfasına gidin
2. En son **MDB-Analiz.exe** dosyasını indirin
3. Çift tıklayarak çalıştırın! 🚀

> ⚠️ Windows Defender uyarısı alırsanız: "More info" → "Run anyway" seçin

### Gereksinimler:
- ✅ Windows 10 veya 11
- ✅ [Microsoft Access Database Engine](https://www.microsoft.com/en-us/download/details.aspx?id=54920) (yoksa program uyarı verecek)

---

## ✨ Özellikler

### 🎨 Modern GUI Arayüzü
- **Pencereli uygulama** ile kolay kullanım
- Türkçe karakter tam desteği (UTF-8)
- Açık/Koyu tema seçeneği
- Responsive ve modern tasarım

### 🔍 Güçlü Analiz
- **Tüm tabloları** listeler
- Her tablo için:
  - ✅ Sütun adları ve veri tipleri
  - ✅ Kayıt sayısı
  - ✅ İlk 5 örnek veri
- Sorgu ve görünümleri listeler
- VBA modüllerini tespit eder

### 💾 Esnek Raporlama
- **TXT formatında** rapor kaydetme
- CSV export (yakında)
- Excel export (yakında)
- Otomatik tarih-saat etiketli dosya isimleri

### ⚡ Performans
- **Threading ile** arayüz donmaması
- İlerleme çubuğu ile işlem takibi
- İşlem süresi göstergesi
- Hızlı ve verimli analiz

### 🛡️ Hata Yönetimi
- Kullanıcı dostu hata mesajları
- Detaylı hata logları
- Driver eksikliği uyarıları
- Dosya bulunamadı kontrolü

## 📦 Kurulum

### 🎯 Hızlı Kullanıcılar İçin (EXE - Önerilir)

Python kurmadan direkt kullanmak istiyorsanız, yukarıdaki [Hızlı Kurulum](#-hızlı-kurulum---exe-i̇ndir-python-gerektirmez) bölümüne bakın.

---

## 💻 Geliştiriciler İçin - Python ile Çalıştırma

Eğer Python kuruluysa veya geliştirme yapmak istiyorsanız:

### Gereksinimler

- **Python 3.8** veya üzeri
- **Windows işletim sistemi** (Access driver için)
- **Microsoft Access Database Engine** driver

### Adım 1: Repository'yi Klonlayın

```bash
git clone https://github.com/kaansayz/mdb-projesi.git
cd mdb-projesi
```

### Adım 2: Gerekli Kütüphaneleri Yükleyin

```bash
pip install -r requirements.txt
```

veya manuel olarak:

```bash
pip install pyodbc pandas ttkthemes openpyxl pillow
```

### Adım 3: Access Database Engine Yükleyin

**Windows için gerekli!**

1. [Microsoft Access Database Engine 2016 Redistributable](https://www.microsoft.com/en-us/download/details.aspx?id=54920) indirin
2. Sisteminize uygun versiyonu yükleyin:
   - **64-bit Python** kullanıyorsanız: `AccessDatabaseEngine_X64.exe`
   - **32-bit Python** kullanıyorsanız: `AccessDatabaseEngine.exe`

Python bit sürümünüzü kontrol etmek için:
```bash
python -c "import struct; print(struct.calcsize('P') * 8, 'bit')"
```

## 🚀 Kullanım

### GUI Uygulamasını Başlatma

```bash
python mdb_gui.py
```

### Kullanım Adımları

1. **📁 MDB Dosyası Seç** butonuna tıklayın
2. Analiz etmek istediğiniz `.mdb` veya `.accdb` dosyasını seçin
3. **🔍 Analiz Et** butonuna tıklayın
4. Sonuçlar ekranda gösterilecektir
5. **📄 Rapor Kaydet** ile sonuçları dosyaya kaydedin

### Arayüz Özellikleri

```
┌─────────────────────────────────────────────────────┐
│   🗂️ MDB Dosya Analiz Programı              [🌙]   │
├─────────────────────────────────────────────────────┤
│  📁 Dosya Seçimi                                    │
│  [📁 MDB Dosyası Seç] [Seçilen dosya yolu...]     │
├─────────────────────────────────────────────────────┤
│  [🔍 Analiz Et] [📄 Rapor Kaydet] [💾▾] [🗑️]     │
│  [■■■■■■■■░░░░] İşlem devam ediyor...              │
├─────────────────────────────────────────────────────┤
│  📊 Analiz Sonuçları                                │
│  ┌───────────────────────────────────────────────┐ │
│  │ ============================================  │ │
│  │ 🗂️  MDB DOSYA ANALİZ RAPORU                 │ │
│  │ ============================================  │ │
│  │                                              │ │
│  │ 📄 Dosya: 04.08.2025 İTİBAREN.mdb          │ │
│  │ 📊 Toplam 5 tablo bulundu                   │ │
│  │                                              │ │
│  │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │ │
│  │ 📋 TABLO 1: Musteriler                      │ │
│  │    📌 Sütun Sayısı: 8                       │ │
│  │    📊 Kayıt Sayısı: 150                     │ │
│  │    ...                                       │ │
│  └───────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────┤
│  ⚡ İşlem tamamlandı (2.5 saniye)        ⏱️ 2.5s │
└─────────────────────────────────────────────────────┘
```

### Klavye Kısayolları

- **ESC**: Programı kapat
- **🌙 Butonu**: Açık/Koyu tema değiştir

## 📸 Ekran Görüntüleri

### Ana Pencere
![Ana Pencere](docs/screenshots/main_window.png)

### Analiz Sonuçları
![Analiz Sonuçları](docs/screenshots/analysis_results.png)

### Rapor Kaydetme
![Rapor Kaydetme](docs/screenshots/save_report.png)

## 🔧 Gereksinimler

### Python Kütüphaneleri

```
pyodbc>=4.0.35        # ODBC veritabanı bağlantısı
pandas>=1.5.0         # Veri işleme
ttkthemes>=3.2.2      # Modern temalar
openpyxl>=3.0.10      # Excel export
pillow>=9.0.0         # Görsel işleme
```

### Sistem Gereksinimleri

- **İşletim Sistemi**: Windows 7/8/10/11
- **Python**: 3.8 veya üzeri
- **RAM**: En az 2 GB
- **Disk**: En az 100 MB boş alan
- **Access Driver**: Microsoft Access Database Engine

## 🐛 Sorun Giderme

### "pyodbc modülü bulunamadı"

```bash
pip install pyodbc
```

### "Microsoft Access Driver bulunamadı"

1. [Access Database Engine](https://www.microsoft.com/en-us/download/details.aspx?id=54920) indirin
2. Python bit sürümünüze uygun versiyonu yükleyin
3. Bilgisayarı yeniden başlatın

### "tkinter modülü bulunamadı" (Linux)

```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora/RHEL
sudo dnf install python3-tkinter
```

### Dosya Seçilemiyor

- Dosya yolunda **Türkçe karakter** varsa sorun olabilir
- Dosyanın **salt okunur** olmadığından emin olun
- **Yönetici** olarak çalıştırmayı deneyin

### Analiz Çalışmıyor

1. MDB dosyasının **bozuk olmadığını** kontrol edin
2. Dosyanın başka bir program tarafından **açık olmadığını** kontrol edin
3. **Access Database Engine** driver'ının yüklü olduğundan emin olun

## 🏗️ Geliştirme

### 🔨 Kendiniz EXE Oluşturma

Kendi bilgisayarınızda .exe dosyası oluşturmak için:

```bash
pip install pyinstaller
python build_exe.py
```

veya doğrudan:

```bash
pyinstaller --onefile --windowed --name="MDB-Analiz" mdb_gui.py
```

.exe dosyası `dist/` klasöründe oluşacak.

Detaylı talimatlar için [build_instructions.md](build_instructions.md) dosyasına bakın.

## 📝 Örnek MDB Dosyası

Repository'de **04.08.2025 İTİBAREN.mdb** adında örnek bir Access veritabanı bulunmaktadır. Bu dosyayı kullanarak uygulamayı test edebilirsiniz.

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'feat: Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 👨‍💻 Geliştirici

**Kaan Sayz**

- GitHub: [@kaansayz](https://github.com/kaansayz)

## 🙏 Teşekkürler

- Python topluluğu
- tkinter ve ttkthemes geliştiricileri
- pyodbc kütüphanesi geliştiricileri

## 📞 İletişim

Sorularınız veya önerileriniz için:
- **Issue** açın: [GitHub Issues](https://github.com/kaansayz/mdb-projesi/issues)

---

⭐ Projeyi beğendiyseniz yıldız vermeyi unutmayın!
