# MDB Analiz Programı - Kullanım Kılavuzu

## İçindekiler
1. [Kurulum](#kurulum)
2. [İlk Çalıştırma](#ilk-çalıştırma)
3. [Temel Kullanım](#temel-kullanım)
4. [İleri Özellikler](#ileri-özellikler)
5. [Sorun Giderme](#sorun-giderme)

## Kurulum

### Adım 1: Python Kurulumu

1. [Python'un resmi sitesine](https://www.python.org/downloads/) gidin
2. Python 3.8 veya üzeri bir sürüm indirin
3. Kurulum sırasında **"Add Python to PATH"** seçeneğini işaretleyin
4. Kurulumu tamamlayın

Python'un doğru kurulduğunu kontrol edin:
```bash
python --version
```

### Adım 2: Gerekli Kütüphanelerin Kurulumu

Komut satırını (CMD veya PowerShell) açın ve proje klasörüne gidin:
```bash
cd C:\path\to\mdb-projesi
```

Kütüphaneleri yükleyin:
```bash
pip install -r requirements.txt
```

### Adım 3: Access Driver Kurulumu (Windows)

**ÖNEMLİ:** Python versiyonunuzla uyumlu driver yüklemelisiniz!

#### Python bit sürümünüzü kontrol edin:
```bash
python -c "import struct; print(struct.calcsize('P') * 8, 'bit')"
```

#### Driver İndirme:
- [Microsoft Access Database Engine 2016 (32-bit)](https://www.microsoft.com/en-us/download/details.aspx?id=54920)
- [Microsoft Access Database Engine 2016 (64-bit)](https://www.microsoft.com/en-us/download/details.aspx?id=54920)

**Not:** Eğer Office yüklüyse, Office'in bit sürümü ile aynı driver'ı yükleyin.

## İlk Çalıştırma

### Windows'ta:

#### Yöntem 1: Batch Dosyası
`calistir.bat` dosyasına çift tıklayın.

#### Yöntem 2: Komut Satırı
```bash
python mdb_uygulama.py
```

### macOS/Linux'ta:
```bash
python3 mdb_uygulama.py
```

## Temel Kullanım

### 1. Dosya Seçme

1. Uygulama açıldığında "📁 Dosya Seç" butonuna tıklayın
2. Açılan pencerede `.mdb` veya `.accdb` dosyanızı bulun
3. Dosyayı seçin ve "Aç" butonuna tıklayın
4. Seçilen dosya yolu üst kısımda görünecektir

### 2. Veritabanını Analiz Etme

1. "🔍 Analiz Et" butonuna tıklayın
2. Program veritabanını analiz etmeye başlayacak:
   - Tablolar bulunacak
   - Her tablonun yapısı incelenecek
   - Örnek veriler alınacak
3. İşlem bittiğinde bir bilgi mesajı görüntülenecek
4. Sol panelde tablo listesi belirecek

### 3. Tablo İnceleme

1. Sol panelden bir tablo adına tıklayın
2. Sağ panelde şunlar görünecek:
   - Tablo adı
   - Toplam kayıt sayısı
   - Sütun sayısı
   - Sütun isimleri ve veri tipleri
   - İlk 5 satırdan örnek veriler

### 4. Rapor Kaydetme

1. "💾 Rapor Kaydet (.txt)" butonuna tıklayın
2. Dosya adı ve konum seçin
3. "Kaydet" butonuna tıklayın
4. Rapor metin dosyası olarak kaydedilecek

**Rapor içeriği:**
- Dosya bilgileri
- Tüm tabloların listesi
- Her tablo için:
  - Kayıt sayısı
  - Sütun listesi (isim, tip, boyut)
  - Örnek veriler

### 5. Excel'e Aktarma

1. "📊 Excel'e Aktar (.xlsx)" butonuna tıklayın
2. Seçim yapın:
   - **Evet:** Tüm tablolar Excel'e aktarılır
   - **Hayır:** Sadece seçili tablo aktarılır
   - **İptal:** İşlem iptal edilir
3. Excel dosya adı ve konum seçin
4. "Kaydet" butonuna tıklayın

**Excel dosyası yapısı:**
- Her tablo ayrı bir sheet'te
- İlk satır sütun başlıkları
- Tüm veriler tablolar halinde

## İleri Özellikler

### Klavye Kısayolları

- **Yukarı/Aşağı Ok:** Tablo listesinde gezinme
- **Enter:** Seçili tabloyu görüntüleme
- **Ctrl+O:** Dosya seç (eğer focus üst kısımdaysa)

### Çoklu Tablo İşleme

Tüm tabloları Excel'e aktarırken her tablo otomatik olarak ayrı bir sheet'e yerleştirilir. Sheet isimleri Excel'in 31 karakter limitine göre kısaltılır.

### Progress Bar

Analiz ve Excel aktarma işlemleri sırasında alt kısımda bir progress bar animasyonu görünür. Bu, programın çalıştığını gösterir.

### Threading

Program arkaplanda threading kullanır, bu sayede:
- Analiz sırasında pencere donmaz
- İşlemi iptal edebilirsiniz (pencereyi kapatarak)
- Durum çubuğunda gerçek zamanlı güncellemeler görürsünüz

## Sorun Giderme

### "Access Driver bulunamadı" Hatası

**Neden:** Microsoft Access Database Engine yüklü değil veya yanlış bit sürümü yüklü.

**Çözüm:**
1. Python bit sürümünüzü kontrol edin:
   ```bash
   python -c "import struct; print(struct.calcsize('P') * 8, 'bit')"
   ```
2. Aynı bit sürümünde driver yükleyin
3. Bilgisayarı yeniden başlatın
4. Uygulamayı tekrar çalıştırın

### "Veritabanına bağlanılamadı" Hatası

**Olası nedenler ve çözümler:**

1. **Dosya hasarlı:**
   - Dosyayı Access'te açmayı deneyin
   - Yedek kopyadan geri yükleyin

2. **Dosya başka programda açık:**
   - Tüm Access pencerelerini kapatın
   - Başka programları kontrol edin

3. **Dosya yolu Türkçe karakter içeriyor:**
   - Dosyayı İngilizce isimli bir klasöre taşıyın
   - Tekrar deneyin

### "Excel oluşturulamadı" Hatası

**Çözüm:**
1. Pandas ve openpyxl yüklü mü kontrol edin:
   ```bash
   pip list | findstr pandas
   pip list | findstr openpyxl
   ```
2. Eksikse yükleyin:
   ```bash
   pip install pandas openpyxl
   ```
3. Hedef klasörde yazma izniniz olduğunu kontrol edin

### Program Çok Yavaş Çalışıyor

**Çözümler:**
1. Çok büyük tablolar varsa, program yavaşlayabilir
2. Sadece ihtiyacınız olan tabloyu Excel'e aktarın
3. Rapor kaydetme Excel'den daha hızlıdır

### Türkçe Karakterler Bozuk Görünüyor

**Windows CMD için:**
```bash
chcp 65001
python mdb_uygulama.py
```

**Rapor dosyasında bozuk karakterler:**
- Dosyayı UTF-8 destekleyen bir editörde açın (Notepad++, VS Code)
- Windows Notepad'de "Encoding > UTF-8" seçin

### Program Açılmıyor

1. **Python yüklü mü?**
   ```bash
   python --version
   ```

2. **Tkinter yüklü mü?**
   ```bash
   python -m tkinter
   ```
   Bir pencere açılmalı.

3. **Kütüphaneler yüklü mü?**
   ```bash
   pip install -r requirements.txt
   ```

## İpuçları

### Hızlı İş Akışı
1. Dosyayı bir kez seçin
2. Analiz edin
3. İlginç tabloları not edin
4. Sadece ihtiyacınız olanları Excel'e aktarın

### Büyük Veritabanları İçin
- İlk önce rapor kaydedin (hızlı)
- Raporu inceleyip hangi tabloları istediğinize karar verin
- Sadece o tabloları Excel'e aktarın

### Yedekleme
- Analiz işlemi veritabanını değiştirmez (sadece okur)
- Ancak yine de yedek almak iyi bir uygulamadır

## EXE Dosyası Oluşturma

Uygulamayı Python yüklü olmayan bilgisayarlarda çalıştırmak için:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="MDB-Analiz" mdb_uygulama.py
```

EXE dosyası `dist/` klasöründe oluşur.

**Not:** EXE dosyasının çalışması için hedef bilgisayarda hala Access Driver gereklidir!

## Destek

Sorun yaşıyorsanız:
1. Bu kılavuzdaki "Sorun Giderme" bölümünü kontrol edin
2. README.md dosyasını okuyun
3. GitHub'da issue açın: https://github.com/kaansayz/mdb-projesi/issues

## Lisans

Bu proje eğitim amaçlıdır ve herkes tarafından kullanılabilir.
