# 📖 Kullanım Örnekleri ve Sık Sorulan Sorular

Bu dosya, MDB Dosya Analiz Programı'nın kullanımı ile ilgili örnekler ve sık sorulan soruları içerir.

## 🚀 Hızlı Başlangıç

### 1. Kurulum

```bash
# Repository'yi klonlayın
git clone https://github.com/kaansayz/mdb-projesi.git
cd mdb-projesi

# Gerekli kütüphaneleri yükleyin
pip install -r requirements.txt

# Programı başlatın
python mdb_gui.py
```

### 2. İlk Analiz

1. Program açıldığında **"📁 MDB Dosyası Seç"** butonuna tıklayın
2. `.mdb` veya `.accdb` dosyanızı seçin
3. **"🔍 Analiz Et"** butonuna tıklayın
4. Sonuçları bekleyin (birkaç saniye)
5. **"📄 Rapor Kaydet"** ile sonuçları kaydedin

## 📋 Detaylı Kullanım Senaryoları

### Senaryo 1: Basit Tablo Analizi

**Amaç:** MDB dosyasındaki tüm tabloları ve içeriklerini görmek

**Adımlar:**
1. Programı başlatın: `python mdb_gui.py`
2. MDB dosyasını seçin
3. "Analiz Et" butonuna tıklayın
4. Sonuç penceresinde:
   - Tablo sayısını görün
   - Her tablonun sütunlarını inceleyin
   - Kayıt sayılarını kontrol edin
   - Örnek verileri görün

**Örnek Çıktı:**
```
📊 TOPLAM 5 TABLO BULUNDU
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 TABLO 1: Musteriler
   📌 Sütun Sayısı: 8
   📊 Kayıt Sayısı: 150
```

### Senaryo 2: Rapor Oluşturma

**Amaç:** Analiz sonuçlarını dosyaya kaydetmek

**Adımlar:**
1. Analizi tamamlayın (Senaryo 1)
2. "📄 Rapor Kaydet" butonuna tıklayın
3. Dosya adı ve konumu seçin
4. Kaydet butonuna tıklayın
5. Başarı mesajını bekleyin

**Rapor Formatı:**
- **TXT:** Düz metin, tüm editörlerde açılır
- **CSV:** Excel'de açılabilir (yakında)
- **XLSX:** Excel formatı (yakında)

### Senaryo 3: Birden Fazla Dosya Analizi

**Amaç:** Farklı MDB dosyalarını sırayla analiz etmek

**Adımlar:**
1. İlk dosyayı analiz edin
2. "📄 Rapor Kaydet" ile sonuçları kaydedin
3. "🗑️ Temizle" butonuna tıklayın
4. Yeni dosya seçin ve 2. adımdan devam edin

### Senaryo 4: Koyu Tema ile Çalışma

**Amaç:** Göz yormayan karanlık modda çalışmak

**Adımlar:**
1. Programı başlatın
2. Sağ üstteki **🌙** butonuna tıklayın
3. Tema değişecektir
4. Tekrar tıklayarak açık temaya dönebilirsiniz

## 🎯 İpuçları ve Püf Noktaları

### 💡 İpucu 1: Hızlı Analiz

Eğer sadece tablo listesini görmek istiyorsanız:
- Analiz sonuçlarının üst kısmında tablo sayısı ve isimleri gösterilir
- Detaylı bilgi için aşağı kaydırın

### 💡 İpucu 2: Büyük Dosyaları Analiz Etme

Büyük MDB dosyaları için:
- İlerleme çubuğu işlem durumunu gösterir
- Threading sayesinde arayüz donmaz
- Sabırlı olun, büyük dosyalar birkaç dakika alabilir

### 💡 İpucu 3: Hata Durumunda

Eğer analiz başarısız olursa:
1. Hata mesajını okuyun (genellikle çözümü içerir)
2. MDB dosyasının bozuk olmadığından emin olun
3. Başka program tarafından açık olmadığını kontrol edin
4. Access Database Engine driver'ını kontrol edin

### 💡 İpucu 4: Rapor Organizasyonu

Raporlarınızı organize etmek için:
- Otomatik tarih-saat etiketli dosya isimleri kullanılır
- Örnek: `mdb_analiz_20260114_143000.txt`
- Kendi klasör yapınızı oluşturun

### 💡 İpucu 5: Klavye Kısayolları

- **ESC tuşu:** Programdan çıkış
- Daha fazla kısayol yakında eklenecek!

## ❓ Sık Sorulan Sorular (SSS)

### S1: "Microsoft Access Driver bulunamadı" hatası alıyorum

**Cevap:** 
Access Database Engine yüklü değil. Şu adımları izleyin:

1. [Bu linkten](https://www.microsoft.com/en-us/download/details.aspx?id=54920) indirin
2. Python bit sürümünüzü kontrol edin:
   ```bash
   python -c "import struct; print(struct.calcsize('P') * 8, 'bit')"
   ```
3. Uygun versiyonu yükleyin:
   - 64-bit Python → AccessDatabaseEngine_X64.exe
   - 32-bit Python → AccessDatabaseEngine.exe
4. Bilgisayarı yeniden başlatın

### S2: Program yavaş çalışıyor

**Cevap:**
- MDB dosyasının boyutuna bağlıdır
- Büyük dosyalar (>100 MB) daha uzun sürer
- Threading sayesinde arayüz donmaz
- İlerleme çubuğu işlemi gösterir

### S3: Türkçe karakterler bozuk görünüyor

**Cevap:**
- UTF-8 encoding kullanılıyor
- Python 3.8+ kullandığınızdan emin olun
- Windows'ta sorun olmaz
- Linux'ta locale ayarlarını kontrol edin:
  ```bash
  export LANG=tr_TR.UTF-8
  ```

### S4: Analiz sırasında bazı tablolar hata veriyor

**Cevap:**
Olası nedenler:
1. **Sistem tabloları:** MSys* ile başlayan tablolar otomatik atlanır
2. **Bozuk tablo:** Bazı tablolar corrupt olabilir
3. **İzin sorunu:** Bazı tablolar şifreli olabilir
4. **Uyumluluk:** Eski Access sürümleri sorun çıkarabilir

Çözüm: Hata mesajını okuyun, sorunlu tabloyu not alın

### S5: .exe dosyası oluşturamıyorum

**Cevap:**
```bash
# PyInstaller'ı yükleyin
pip install pyinstaller

# build_exe.py scriptini kullanın
python build_exe.py

# veya manuel olarak
pyinstaller --onefile --windowed --name="MDB-Analiz" mdb_gui.py
```

Detaylı talimatlar için `build_instructions.md` dosyasına bakın.

### S6: CSV veya Excel export çalışmıyor

**Cevap:**
Bu özellikler henüz geliştirilme aşamasında. Şu an sadece TXT format destekleniyor.

Gelecek güncellemelerde:
- CSV export
- Excel export
- PDF export

### S7: Linux'ta çalıştıramıyorum

**Cevap:**
Linux'ta tkinter yüklü olmalı:

```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora/RHEL
sudo dnf install python3-tkinter

# Arch Linux
sudo pacman -S tk
```

**Not:** Access Database Engine sadece Windows'ta çalışır. Linux'ta:
- Wine kullanabilirsiniz (karmaşık)
- mdbtools kullanabilirsiniz (alternatif)
- Docker ile Windows container (gelişmiş)

### S8: Program başlamıyor, hiçbir şey olmuyor

**Cevap:**
1. Komut satırından çalıştırın:
   ```bash
   python mdb_gui.py
   ```
2. Hata mesajlarını okuyun
3. Gerekli kütüphaneleri kontrol edin:
   ```bash
   pip install -r requirements.txt
   ```
4. Python versiyonunu kontrol edin:
   ```bash
   python --version  # 3.8 veya üzeri olmalı
   ```

### S9: Antivirüs programım .exe dosyasını engelliyor

**Cevap:**
Bu normal bir durumdur (false positive):

1. .exe dosyasını antivirüs beyaz listesine ekleyin
2. Windows Defender'da istisna oluşturun:
   - Ayarlar → Güvenlik → Virüs ve tehdit koruması
   - İstisnalar yönet → İstisna ekle
   - Dosya seçin: MDB-Analiz.exe

Güvenlik: .exe dosyası sadece Python scriptlerinden oluşturulmuştur, zararlı değildir.

### S10: Birden fazla MDB dosyasını aynı anda analiz edebilir miyim?

**Cevap:**
Şu an tek dosya analizi destekleniyor. Birden fazla dosya için:

1. İlk dosyayı analiz edin
2. Raporu kaydedin
3. "Temizle" butonuna tıklayın
4. Yeni dosya seçin

**Gelecek özellik:** Toplu analiz modu planlanıyor!

## 🔧 Sorun Giderme

### Sorun: "pyodbc modülü bulunamadı"

**Çözüm:**
```bash
pip install pyodbc
```

### Sorun: "tkinter modülü bulunamadı"

**Çözüm (Linux):**
```bash
sudo apt-get install python3-tk
```

### Sorun: Program donuyor

**Çözüm:**
- Threading kullanıldığı için donmamalı
- Eğer donuyorsa, Ctrl+C ile durdurun
- Bug raporu açın: GitHub Issues

### Sorun: Rapor kaydedilemiyor

**Çözüm:**
1. Yazma izniniz olduğundan emin olun
2. Disk alanı kontrolü yapın
3. Farklı bir konum deneyin
4. Dosya adında özel karakter kullanmayın

## 📊 Performans İpuçları

### Büyük Dosyalar İçin

- **Sabırlı olun:** 100 MB+ dosyalar 5-10 dakika alabilir
- **RAM kontrolü:** En az 4 GB RAM önerilir
- **SSD kullanın:** HDD'ye göre 3-4x daha hızlı

### Optimizasyon

- Gereksiz programları kapatın
- Antivirüs'ü geçici olarak durdurun (analiz sırasında)
- Ağ bağlantısı gerekmez (offline çalışır)

## 🎓 İleri Seviye Kullanım

### Python API Olarak Kullanma

MDB GUI'yi kendi scriptinizde kullanabilirsiniz:

```python
# Örnek: API kullanımı (gelecekte eklenecek)
from mdb_gui import MDBAnalyzer

analyzer = MDBAnalyzer("mydatabase.mdb")
results = analyzer.analyze()
print(results)
```

### Komut Satırı Arayüzü

```bash
# Gelecek özellik: CLI modu
python mdb_gui.py --cli --file="mydatabase.mdb" --output="report.txt"
```

## 📞 Destek ve İletişim

### Hata Bildirimi

GitHub Issues kullanın:
https://github.com/kaansayz/mdb-projesi/issues

**Hata raporu şablonu:**
```
**Hata Açıklaması:**
[Hatanın kısa açıklaması]

**Adımlar:**
1. [Birinci adım]
2. [İkinci adım]
3. [Hata oluşuyor]

**Beklenen Davranış:**
[Ne olmasını bekliyordunuz]

**Ekran Görüntüleri:**
[Varsa ekleyin]

**Sistem Bilgisi:**
- OS: [Windows 10, Ubuntu 20.04, vb.]
- Python: [3.8, 3.9, 3.10, vb.]
- Program Versiyonu: [v1.0.0]
```

### Özellik İsteği

GitHub Issues'da "enhancement" etiketi ile açın.

### Katkıda Bulunma

Pull Request'lerinizi bekliyoruz! 🎉

## 🔄 Güncellemeler

### Nasıl Güncellenir

```bash
cd mdb-projesi
git pull origin main
pip install -r requirements.txt --upgrade
```

### Changelog

**v1.0.0 (Ocak 2026)**
- ✅ İlk sürüm
- ✅ GUI arayüzü
- ✅ Tablo analizi
- ✅ TXT rapor
- ✅ Tema desteği

**Planlar (v1.1.0)**
- 🔜 CSV export
- 🔜 Excel export
- 🔜 Toplu analiz
- 🔜 Grafik gösterim
- 🔜 İlişki diyagramı

## 📚 Ek Kaynaklar

- **GitHub:** https://github.com/kaansayz/mdb-projesi
- **Python:** https://www.python.org/
- **pyodbc:** https://github.com/mkleehammer/pyodbc
- **tkinter:** https://docs.python.org/3/library/tkinter.html

---

**Son güncelleme:** 14 Ocak 2026

Başka sorularınız için GitHub Issues kullanın! 💬
