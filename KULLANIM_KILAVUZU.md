# 📖 Cezaevi Gıda Takip Sistemi - Kullanım Kılavuzu

Bu dokümantasyon, Cezaevi Gıda Takip Sistemi'nin detaylı kullanım kılavuzudur.

## 📋 İçindekiler

1. [İlk Kurulum](#ilk-kurulum)
2. [Ana Ekran](#ana-ekran)
3. [Ürün Yönetimi](#ürün-yönetimi)
4. [Günlük Tabela](#günlük-tabela)
5. [Stok Takibi](#stok-takibi)
6. [Raporlar](#raporlar)
7. [Ayarlar](#ayarlar)
8. [Sık Sorulan Sorular](#sık-sorulan-sorular)

---

## İlk Kurulum

### 1. Uygulamayı Başlatma

```bash
python main.py
```

### 2. İlk Çalıştırma

İlk kez çalıştırdığınızda:

1. **Veritabanı Kontrolü**: Uygulama `data/cezaevi_gida.db` dosyasını arar
2. **MDB İmport İsteği**: Veritabanı yoksa, MDB dosyasından veri aktarmayı sorar
3. **Onay Verme**: "Evet" seçerseniz otomatik import başlar
4. **Veri Aktarımı**: 
   - Cezaevi bilgileri
   - 414 ürün
   - 24,671+ günlük tabela kaydı
   - Firma ve memur bilgileri
5. **Ana Ekran**: Import tamamlandıktan sonra ana ekran açılır

### 3. Manuel Import

Eğer otomatik import yapılmadıysa:

```bash
python mdb_importer.py
```

---

## Ana Ekran

### Dashboard Bileşenleri

#### 1. Cezaevi Bilgileri Kartı

```
┌─────────────────────────────────┐
│   🏛️ Cezaevi Bilgileri          │
├─────────────────────────────────┤
│ Cezaevi: Örnek Cezaevi          │
│ Müdür: [İsim]                    │
│ Ambar Memuru: [İsim]            │
└─────────────────────────────────┘
```

- Cezaevi adı
- Müdür adı
- Ambar memuru adı
- Komisyon üyeleri

#### 2. Günlük Öğün Sayıları

```
┌─────────────────────────────────┐
│   🍽️ Günlük Öğün Sayıları       │
├─────────────────────────────────┤
│ Sabah:  5,773 kişi              │
│ Öğle:   5,773 kişi              │
│ Akşam:  5,773 kişi              │
│ TOPLAM: 17,319 kişi             │
└─────────────────────────────────┘
```

#### 3. Günlük Ekmek Miktarları

```
┌─────────────────────────────────┐
│   🍞 Günlük Ekmek Miktarları    │
├─────────────────────────────────┤
│ Sabah:  5,800 adet              │
│ Öğle:   5,800 adet              │
│ Akşam:  5,800 adet              │
│ TOPLAM: 17,400 adet             │
└─────────────────────────────────┘
```

#### 4. Bugünün Özeti

```
┌─────────────────────────────────┐
│   📊 Bugünün Özeti              │
├─────────────────────────────────┤
│ Toplam Maliyet: 125,450.00 TL   │
│ Toplam Kalori:  2,350 kcal      │
│ Toplam Ürün:    42 adet         │
└─────────────────────────────────┘
```

### Yenileme

- **Manuel Yenileme**: "🔄 Yenile" butonuna tıklayın
- **Otomatik Güncelleme**: Diğer modüllerden ana ekrana döndüğünüzde otomatik yenilenir

---

## Ürün Yönetimi

### Ürün Listesi

Treeview tablosu şu sütunları gösterir:

| Ürün No | Cinsi | Birimi | Fiyatı | Kalorisi | Defter No |
|---------|-------|--------|--------|----------|-----------|
| 1 | GAZOZ | Adet | 13.20 | 150 | 101 |
| 2 | ÇAY | Kg | 85.00 | 0 | 102 |

### Ürün Arama

1. **Arama Kutusu**: Üst kısımdaki arama kutusuna yazın
2. **Canlı Arama**: Yazdıkça sonuçlar filtrelenir
3. **Arama Alanları**: Ürün adı ve birimi içinde arar
4. **Temizle**: "X" işaretine tıklayarak aramayı temizleyin

### Yeni Ürün Ekleme

1. **"➕ Yeni Ürün"** butonuna tıklayın
2. **Form Doldurma**:
   - **Cinsi** (Zorunlu): Ürün adı (örn: "MAKARNA")
   - **Birimi**: Birim (örn: "Kg", "Adet", "Litre")
   - **Fiyatı**: Birim fiyat (örn: "25.50")
   - **Kalorisi**: 100g başına kalori (örn: "350")
   - **Defter No**: Muhasebe defter numarası (opsiyonel)
3. **"💾 Kaydet"** butonuna tıklayın

**Validasyon:**
- Cinsi alanı boş bırakılamaz
- Fiyat pozitif sayı olmalı
- Kalori tam sayı olmalı

### Ürün Düzenleme

1. Tablodan bir ürün seçin
2. **"✏️ Düzenle"** butonuna tıklayın
3. Form açılır, mevcut değerler görünür
4. Değişiklikleri yapın
5. **"💾 Kaydet"** ile kaydedin

### Ürün Silme

1. Tablodan bir veya birden fazla ürün seçin
2. **"🗑️ Sil"** butonuna tıklayın
3. Onay mesajını okuyun
4. **"Evet"** ile onaylayın

**⚠️ Uyarı**: Silme işlemi geri alınamaz!

---

## Günlük Tabela

### Tabela Oluşturma Akışı

#### Adım 1: Tarih Seçimi

```
📅 Tarih: [15.01.2026] 🗓️
```

- Takvim ikonuna tıklayın
- Açılan takvimden tarih seçin
- Seçilen tarih otomatik yazılır

#### Adım 2: Öğün Seçimi

```
🍽️ Öğün: [ÖĞLE ▼]
```

Seçenekler:
- SABAH
- ÖĞLE
- AKŞAM

#### Adım 3: Mevcut Kişi Sayısı

```
👥 Mevcut: [5773]
```

- Öğüne katılacak kişi sayısını girin
- Tüm hesaplamalar bu sayıya göre yapılır

#### Adım 4: Ürün Seçimi

```
📦 Ürün: [GAZOZ ▼]
```

- Dropdown'dan ürün seçin
- Liste veritabanındaki tüm ürünleri içerir
- Alfabetik sıralıdır

#### Adım 5: Miktar Girişi

```
📊 Miktar: [5690]
```

- Kullanılacak miktar (ürünün birimine göre)
- Örnek: 5690 adet, 120 kg, vb.

#### Adım 6: Hesaplama

**"🔢 Hesapla"** butonuna tıklayın

Otomatik hesaplanan değerler:

```
┌────────────────────────────────┐
│ 💰 Tutar:         75,108.00 TL │
│ 👤 Kişi Başı:     13.01 TL     │
│ 📊 Kişi Miktarı:  0.985 adet   │
│ 🔥 Kişi Kalori:   147 kcal     │
└────────────────────────────────┘
```

**Formüller:**
- Tutar = Miktar × Fiyat
- Kişi Başı Tutar = Tutar ÷ Mevcut
- Kişi Başı Miktar = Miktar ÷ Mevcut
- Kişi Başı Kalori = (Miktar × Kalori) ÷ Mevcut

#### Adım 7: Kayıt Ekleme

**"➕ Ekle"** butonuna tıklayın

Kayıt listeye eklenir:

| Ürün | Miktar | Fiyat | Tutar | Kişi Başı |
|------|--------|-------|-------|-----------|
| GAZOZ | 5690 adet | 13.20 | 75,108.00 | 13.01 |

### Kayıt Silme

1. Listeden bir kayıt seçin
2. **"🗑️ Sil"** butonuna tıklayın
3. Onaylayın

### Kayıt Listesi

Alt kısımda seçilen tarih ve öğün için tüm kayıtlar görünür:

```
┌──────────────────────────────────────────────┐
│ 📋 Kayıtlar (15.01.2026 - ÖĞLE)             │
├──────────────────────────────────────────────┤
│ 1. GAZOZ - 5,690 adet - 75,108.00 TL        │
│ 2. ÇAY - 120 kg - 10,200.00 TL              │
│ 3. ŞEKER - 150 kg - 7,500.00 TL             │
├──────────────────────────────────────────────┤
│ TOPLAM: 92,808.00 TL                         │
└──────────────────────────────────────────────┘
```

---

## Stok Takibi

### Stok Görünümü

Treeview tablosu:

| Ürün No | Ürün Adı | Birimi | Stok Miktarı | Durum |
|---------|----------|--------|--------------|-------|
| 1 | GAZOZ | Adet | 5,420 | 🟢 Normal |
| 2 | ÇAY | Kg | 35 | 🟡 Uyarı |
| 3 | MAKARNA | Kg | 8 | 🔴 Kritik |

### Uyarı Seviyeleri

#### 🟢 Normal (>= 50)
- Yeterli stok var
- Yeşil renk

#### 🟡 Uyarı (10-49)
- Stok azalıyor
- Sarı renk
- Yeniden sipariş düşünün

#### 🔴 Kritik (< 10)
- Stok çok düşük
- Kırmızı renk
- **ACİL** sipariş gerekli!

### Stok Yenileme

**"🔄 Yenile"** butonuna tıklayarak güncel stok durumunu görün.

### Stok Hesaplama

Stok miktarı `gunluk_tabela` tablosundaki `stok_mevcudu` sütununun toplamından hesaplanır.

---

## Raporlar

### Rapor Türleri

#### 1. Malzeme Girişleri Raporu

Tarih aralığında depoya giren malzemeleri gösterir:

| Tarih | Ürün | Miktar | Birim | Fiyat | Tutar |
|-------|------|--------|-------|-------|-------|
| 15.01.2026 | GAZOZ | 10,000 | Adet | 13.20 | 132,000.00 |
| 15.01.2026 | ÇAY | 250 | Kg | 85.00 | 21,250.00 |

#### 2. Malzeme Çıkışları Raporu

Tarih aralığında kullanılan malzemeleri gösterir:

| Tarih | Öğün | Ürün | Miktar | Birim | Fiyat | Tutar | Kişi |
|-------|------|------|--------|-------|-------|-------|------|
| 15.01.2026 | ÖĞLE | GAZOZ | 5,690 | Adet | 13.20 | 75,108.00 | 5,773 |
| 15.01.2026 | AKŞAM | ÇAY | 120 | Kg | 85.00 | 10,200.00 | 5,773 |

#### 3. Ürün Bazlı Rapor

Ürünlere göre toplam giriş/çıkış:

| Ürün | Birim | Top. Giriş | Top. Çıkış | Top. Tutar | İşlem |
|------|-------|------------|------------|------------|-------|
| GAZOZ | Adet | 10,000 | 8,450 | 111,540.00 | 125 |
| ÇAY | Kg | 250 | 195 | 16,575.00 | 87 |

#### 4. Günlük Özet Rapor

Seçilen tarihteki tüm işlemler:

| Öğün | Ürün Sayısı | Toplam Tutar | Toplam Kalori | Kişi Sayısı |
|------|-------------|--------------|---------------|-------------|
| SABAH | 15 | 42,350.00 | 1,850 | 5,773 |
| ÖĞLE | 18 | 51,200.00 | 2,100 | 5,773 |
| AKŞAM | 17 | 48,900.00 | 1,975 | 5,773 |

### Rapor Oluşturma

#### Adım 1: Rapor Türü Seçimi

```
📊 Rapor Türü: [Malzeme Çıkışları ▼]
```

#### Adım 2: Tarih Aralığı

```
📅 Başlangıç: [01.01.2026] 🗓️
📅 Bitiş:      [31.01.2026] 🗓️
```

#### Adım 3: Rapor Oluştur

**"📊 Rapor Oluştur"** butonuna tıklayın

Rapor treeview'de gösterilir.

### Excel'e Dışa Aktarma

1. Raporu oluşturun
2. **"📥 Excel'e Aktar"** butonuna tıklayın
3. Dosya konumunu seçin
4. Excel dosyası oluşturulur

**Excel Özellikleri:**
- Başlık satırı kalın ve renkli
- Otomatik sütun genişliği
- Toplam satırı (uygunsa)
- Dosya adı: `rapor_20260115_143022.xlsx`

**Excel Formatı:**

```
┌────────────────────────────────────┐
│ MALZEME ÇIKIŞLARI RAPORU           │  ← Başlık (Kalın, Mavi)
├────────────────────────────────────┤
│ Tarih: 01.01.2026 - 31.01.2026    │
├────┬──────┬────────┬───────┬───────┤
│Tarih│Öğün │Ürün    │Miktar │Tutar  │  ← Başlık (Kalın, Gri)
├────┼──────┼────────┼───────┼───────┤
│15.01│ÖĞLE │GAZOZ   │5,690  │75,108 │
│15.01│AKŞAM│ÇAY     │120    │10,200 │
├────┴──────┴────────┴───────┼───────┤
│                     TOPLAM:│85,308 │  ← Toplam (Kalın)
└────────────────────────────┴───────┘
```

---

## Ayarlar

### Cezaevi Bilgileri

```
🏛️ Cezaevi Adı:        [________________]
👤 Cezaevi Müdürü:     [________________]
📦 Ambar Memuru:       [________________]
👥 Komisyon Üyesi 1:   [________________]
👥 Komisyon Üyesi 2:   [________________]
👥 Komisyon Üyesi 3:   [________________]
```

### Günlük Öğün Sayıları

```
🌅 Sabah:   [5773]
🌞 Öğle:    [5773]
🌙 Akşam:   [5773]
────────────────────
📊 TOPLAM:  17,319  (Otomatik)
```

- Değerleri girin
- Toplam otomatik hesaplanır
- **"💾 Kaydet"** ile kaydedin

### Günlük Ekmek Miktarları

```
🌅 Sabah:   [5800]
🌞 Öğle:    [5800]
🌙 Akşam:   [5800]
────────────────────
🍞 TOPLAM:  17,400  (Otomatik)
```

### Kaydetme

**"💾 Tüm Ayarları Kaydet"** butonuna tıklayın

Başarı mesajı: "✅ Ayarlar başarıyla kaydedildi!"

---

## Sık Sorulan Sorular

### S1: Veritabanı nerede saklanıyor?

**C:** `data/cezaevi_gida.db` dosyasında SQLite formatında.

### S2: MDB dosyasını değiştirdim, nasıl yeniden import yapabilirim?

**C:** 
```bash
# Mevcut veritabanını silin
rm data/cezaevi_gida.db

# Yeniden import yapın
python mdb_importer.py
```

### S3: Excel export çalışmıyor?

**C:** `openpyxl` kütüphanesinin kurulu olduğundan emin olun:
```bash
pip install openpyxl
```

### S4: Tarih seçici çalışmıyor?

**C:** `tkcalendar` kütüphanesini kurun:
```bash
pip install tkcalendar
```

### S5: Ürün silerken hata alıyorum?

**C:** Ürün başka tablolarda kullanılıyor olabilir. Önce o kayıtları silin.

### S6: Stok miktarları yanlış görünüyor?

**C:** Stok hesaplaması `gunluk_tabela` tablosundaki `stok_mevcudu` sütunundan yapılır. Veri tutarsızlığı varsa, veritabanını kontrol edin.

### S7: Hesaplamalar yanlış?

**C:** Hesaplama formülleri `utils/hesaplamalar.py` dosyasında. Eğer sorun varsa bu dosyayı kontrol edin.

### S8: Türkçe karakterler düzgün görünmüyor?

**C:** Tüm dosyalar UTF-8 encoding ile kaydedilmiş olmalı. Editörünüzün encoding ayarını kontrol edin.

### S9: Yedekleme nasıl yapılır?

**C:** `data/cezaevi_gida.db` dosyasını kopyalayın:
```bash
cp data/cezaevi_gida.db data/cezaevi_gida_backup_20260115.db
```

### S10: Eski MDB dosyasına geri dönmek istersem?

**C:** MDB dosyası orijinal haliyle kalır. SQLite sadece bir kopyadır. İstediğiniz zaman MDB'yi kullanmaya devam edebilirsiniz.

---

## 💡 İpuçları ve Püf Noktaları

### 1. Hızlı Ürün Arama
- Ürün yönetiminde arama kutusunu kullanın
- Klavyeden yazmaya başladığınızda otomatik arar

### 2. Toplu Ürün Silme
- Ctrl tuşu ile birden fazla ürün seçebilirsiniz
- Hepsini tek seferde silebilirsiniz

### 3. Excel Raporları
- Excel dosyaları otomatik tarih-saat ile isimlendirilir
- Karışıklığı önler

### 4. Günlük Tabela Hızlı Giriş
- Aynı tarih ve öğün için birden fazla ürün ekleyebilirsiniz
- Her ürün için "Hesapla → Ekle" yapın

### 5. Stok Uyarıları
- Kritik (kırmızı) ürünler için hemen sipariş verin
- Uyarı (sarı) ürünleri listeleyin

### 6. Yedekleme Stratejisi
- Her ayın sonunda veritabanını yedekleyin
- Format: `cezaevi_gida_YYYYMM.db`

### 7. Performans
- Büyük tarih aralıkları için raporlar yavaş olabilir
- Mümkünse aylık veya haftalık raporlar alın

### 8. Veri Girişi
- Fiyatları girerken virgül veya nokta kullanabilirsiniz
- Sistem otomatik dönüştürür

---

## 🔧 Gelişmiş Kullanım

### Veritabanı Sorguları

Özel sorgular için Python'dan:

```python
from database import Database

with Database() as db:
    # Özel sorgu
    result = db.execute_query("""
        SELECT cinsi, SUM(tutar) as toplam
        FROM gunluk_tabela
        WHERE tarih BETWEEN '2026-01-01' AND '2026-01-31'
        GROUP BY cinsi
        ORDER BY toplam DESC
        LIMIT 10
    """)
    
    for row in result:
        print(f"{row['cinsi']}: {row['toplam']:.2f} TL")
```

### Toplu Veri İşleme

```python
from database import Database

with Database() as db:
    # Tüm ürünlerin fiyatını %10 artır
    db.cursor.execute("""
        UPDATE urunler
        SET fiyati = fiyati * 1.10
    """)
    db.conn.commit()
```

---

## 📞 Destek

Sorun yaşarsanız:

1. **Hata Logları**: Konsol çıktısını kontrol edin
2. **GitHub Issues**: [Issue açın](https://github.com/kaansayz/mdb-projesi/issues)
3. **Dokümantasyon**: Bu dosyayı tekrar okuyun

---

**Son Güncelleme**: 15 Ocak 2026
**Versiyon**: 1.0.0
