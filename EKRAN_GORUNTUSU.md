# MDB Analiz Programı - Ekran Görüntüsü Açıklaması

Bu dosya, uygulamanın görsel yapısını ve kullanıcı arayüzünü açıklar.

## Ana Pencere Yapısı

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 📊 MDB Dosya Analiz Programı                                    [─][□][×]│
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│                   📊 MDB Dosya Analiz Programı                           │
│                                                                           │
│  Dosya: [C:\...\04.08.2025 İTİBAREN.mdb          ] [📁 Dosya Seç] [🔍 Analiz Et] │
│                                                                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌────────────────────┬───────────────────────────────────────────────┐ │
│  │   📋 Tablolar      │        📊 Tablo Detayları                     │ │
│  ├────────────────────┼───────────────────────────────────────────────┤ │
│  │                    │ Tablo: Customers | Kayıt Sayısı: 1250 |     │ │
│  │ ▸ Customers        │ Sütun Sayısı: 8                              │ │
│  │ ▸ Orders           ├───────────────────────────────────────────────┤ │
│  │ ▸ Products         │ #  │ ID       │ Name      │ Email    │ ...   │ │
│  │ ▸ Categories       │────┼──────────┼───────────┼──────────┼───────┤ │
│  │ ▸ Suppliers        │ 1  │ 1001     │ Ali Yılmaz│ ali@...  │       │ │
│  │ ▸ Employees        │ 2  │ 1002     │ Ayşe Kaya │ ayse@... │       │ │
│  │ ▸ Invoices         │ 3  │ 1003     │ Mehmet Can│ mehmet@..│       │ │
│  │                    │ 4  │ 1004     │ Zeynep K. │ zeynep@..│       │ │
│  │                    │ 5  │ 1005     │ Ahmet Öz  │ ahmet@.. │       │ │
│  │                    │    │          │           │          │       │ │
│  │                    │                                               │ │
│  │       [↕]          │                                       [↕][↔] │ │
│  └────────────────────┴───────────────────────────────────────────────┘ │
│                                                                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  [💾 Rapor Kaydet (.txt)]  [📊 Excel'e Aktar (.xlsx)]   [========]      │
│                                                                           │
│  Durum: Analiz tamamlandı! 7 tablo bulundu.                             │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────┘
```

## Renk Şeması

- **Yeşil Buton (📁 Dosya Seç):** #4CAF50
- **Mavi Buton (🔍 Analiz Et):** #2196F3
- **Turuncu Buton (💾 Rapor Kaydet):** #FF9800
- **Teal Buton (📊 Excel'e Aktar):** #009688

## Kullanıcı Akışı

### 1. Başlangıç Ekranı
- Pencere 1000x700 px boyutunda açılır
- Ekranın ortasında konumlanır
- "Analiz Et" butonu devre dışı (disabled)

### 2. Dosya Seçimi
- Kullanıcı "📁 Dosya Seç" butonuna tıklar
- Dosya seçim diyalogu açılır (sadece .mdb ve .accdb dosyaları görünür)
- Dosya seçildikten sonra:
  - Dosya yolu üst kısımda görünür
  - "Analiz Et" butonu aktif hale gelir
  - Durum çubuğu: "Dosya seçildi: 04.08.2025 İTİBAREN.mdb"

### 3. Analiz İşlemi
- Kullanıcı "🔍 Analiz Et" butonuna tıklar
- Progress bar animasyonu başlar (alt kısımda)
- Durum çubuğu sırayla:
  - "Veritabanına bağlanılıyor..."
  - "Tablolar alınıyor..."
  - "Analiz ediliyor: Customers..."
  - "Analiz ediliyor: Orders..."
  - ...
- Sol panelde tablolar listelenir
- Başarılı mesaj kutusu: "Analiz tamamlandı! X tablo bulundu."
- "Rapor Kaydet" ve "Excel'e Aktar" butonları aktif olur

### 4. Tablo İnceleme
- Kullanıcı sol panelden bir tabloya tıklar
- Sağ panelde tablo detayları gösterilir:
  - Üst kısım: Tablo adı, kayıt sayısı, sütun sayısı
  - Ana kısım: Sütun isimleri ve veri tipleri başlıklarda
  - İlk 5 satır örnek veri tablo formatında
- Kaydırma çubukları ile veri görüntülenebilir

### 5. Rapor Kaydetme
- Kullanıcı "💾 Rapor Kaydet (.txt)" butonuna tıklar
- Dosya kaydetme diyalogu açılır
- Kaydedildikten sonra başarı mesajı gösterilir
- Durum çubuğu: "Rapor kaydedildi: RAPOR.txt"

### 6. Excel'e Aktarma
- Kullanıcı "📊 Excel'e Aktar (.xlsx)" butonuna tıklar
- Seçim diyalogu: "Tüm tablolar / Sadece seçili tablo"
- Dosya kaydetme diyalogu açılır
- Progress bar animasyonu
- Başarı mesajı: "Excel dosyası oluşturuldu"

## Hata Durumları

### Driver Bulunamadı
```
╔══════════════════════════════════════╗
║             Hata                     ║
╠══════════════════════════════════════╣
║ Access Driver bulunamadı!            ║
║                                      ║
║ Microsoft Access Database Engine    ║
║ yüklemek için:                       ║
║ https://www.microsoft.com/...        ║
║                                      ║
║ Not: 64-bit Python kullanıyorsanız  ║
║ 64-bit driver yükleyin.              ║
║                                      ║
║              [ Tamam ]               ║
╚══════════════════════════════════════╝
```

### Bağlantı Hatası
```
╔══════════════════════════════════════╗
║             Hata                     ║
╠══════════════════════════════════════╣
║ Veritabanına bağlanılamadı:          ║
║ [Hata mesajı detayı]                 ║
║                                      ║
║              [ Tamam ]               ║
╚══════════════════════════════════════╝
```

## Özellikler

✅ Modern ve temiz tasarım
✅ Türkçe karakter desteği (UTF-8)
✅ Responsive layout (paneller orantılı genişler)
✅ Kaydırma çubukları (çok veri olduğunda)
✅ Progress bar (işlem sırasında)
✅ Threading (UI donması yok)
✅ Kullanıcı dostu hata mesajları
✅ İkonlar ve emojiler
✅ Durum çubuğu (sürekli bilgilendirme)
✅ Klavye kısayolları (Enter ile seçim)

## Teknik Detaylar

- **Framework:** tkinter
- **Bileşenler:**
  - tk.Button (renkli butonlar)
  - ttk.LabelFrame (paneller)
  - tk.Listbox (tablo listesi)
  - ttk.Treeview (tablo detayları)
  - ttk.Scrollbar (kaydırma)
  - ttk.Progressbar (animasyon)
  - ttk.Label (durum çubuğu)
  - filedialog (dosya seç/kaydet)
  - messagebox (uyarı/bilgi mesajları)
- **Threading:** UI donmasını önler
- **Encoding:** UTF-8 (Türkçe karakterler)
