# 📊 MDB Dosya Analiz Programı

Microsoft Access (.mdb/.accdb) dosyalarını analiz eden pencereli masaüstü uygulaması.

## 🎯 Özellikler

- ✅ Grafik arayüz (GUI)
- 📁 Dosya seçici
- 🔍 Otomatik tablo analizi
- 📊 Sütun ve veri tiplerini gösterme
- 💾 Rapor kaydetme
- 📈 Excel'e aktarma

## 🚀 Kurulum

### 1. Python Kurulumu
[Python 3.8+](https://www.python.org/downloads/) indir ve kur

### 2. Gerekli Kütüphaneler
```bash
pip install -r requirements.txt
```

### 3. Access Driver (Windows)
[Microsoft Access Database Engine](https://www.microsoft.com/en-us/download/details.aspx?id=54920) indir ve kur

**Önemli Not:** 
- 64-bit Python kullanıyorsanız 64-bit driver yükleyin
- 32-bit Python kullanıyorsanız 32-bit driver yükleyin

Python versiyonunuzu kontrol etmek için:
```bash
python --version
python -c "import struct; print(struct.calcsize('P') * 8, 'bit')"
```

## 💻 Kullanım

### Windows:
```bash
python mdb_uygulama.py
```

veya `calistir.bat` dosyasını çift tıklayın.

### macOS/Linux:
```bash
python3 mdb_uygulama.py
```

### Adım Adım Kullanım:

1. **Dosya Seç** butonuna tıklayın
2. .mdb dosyanızı seçin (örnek: `04.08.2025 İTİBAREN.mdb`)
3. **Analiz Et** butonuna basın
4. Sol panelden tabloları inceleyin
5. Bir tabloya tıklayarak detaylarını görün
6. İsterseniz rapor kaydedin veya Excel'e aktarın

## 📦 .EXE Dosyası Oluşturma

Uygulamayı bağımsız .exe dosyası olarak dağıtmak için:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="MDB-Analiz" mdb_uygulama.py
```

Oluşan .exe dosyası `dist/` klasöründe olacak.

## 🖼️ Ekran Görünümü

Uygulama aşağıdaki bileşenleri içerir:

- **Üst Kısım:** Dosya seçme ve analiz butonları
- **Sol Panel:** Veritabanındaki tablo listesi
- **Sağ Panel:** Seçilen tablonun sütunları, veri tipleri ve örnek veriler
- **Alt Kısım:** Rapor kaydetme, Excel'e aktarma butonları ve durum çubuğu

## 📁 Dosya Yapısı

```
mdb-projesi/
├── 04.08.2025 İTİBAREN.mdb    # Örnek Access veritabanı
├── mdb_uygulama.py             # Ana uygulama
├── requirements.txt            # Python bağımlılıkları
├── calistir.bat               # Windows başlatıcı
├── README.md                  # Bu dosya
└── .gitignore                # Git ignore kuralları
```

## 🛠️ Teknik Detaylar

- **Python:** 3.8+
- **GUI Framework:** Tkinter
- **Veritabanı:** pyodbc
- **Excel:** pandas, openpyxl
- **Threading:** UI donmasını önlemek için

## 📝 Notlar

- Windows için tasarlanmıştır (macOS/Linux'ta alternatif driver gerekebilir)
- Access Driver gereklidir
- Türkçe karakter desteği vardır (UTF-8)
- Sistem tabloları (MSys*, ~*) otomatik filtrelenir

## 🔧 Sorun Giderme

### "Access Driver bulunamadı" hatası:
- Microsoft Access Database Engine yükleyin
- Python ve Driver bit sürümlerinin aynı olduğundan emin olun (32-bit veya 64-bit)

### "Veritabanına bağlanılamadı" hatası:
- Dosya yolunun doğru olduğundan emin olun
- Dosyanın hasarlı olmadığını kontrol edin
- Dosyanın başka bir program tarafından açık olmadığından emin olun

### "Excel oluşturulamadı" hatası:
- pandas ve openpyxl kütüphanelerinin yüklü olduğundan emin olun
- Hedef klasörde yazma izniniz olduğunu kontrol edin

## 📄 Lisans

Bu proje eğitim amaçlıdır.

## 👨‍💻 Geliştirici

GitHub: [@kaansayz](https://github.com/kaansayz)
