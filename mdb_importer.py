# -*- coding: utf-8 -*-
"""
MDB -> SQLite Dönüştürücü
Access veritabanından SQLite'a veri aktarımı
"""

import os
import sys
from datetime import datetime

try:
    import pyodbc
except ImportError:
    print("❌ HATA: pyodbc modülü bulunamadı!")
    print("Kurulum: pip install pyodbc")
    sys.exit(1)

from database import Database, init_database

MDB_FILE = "04.08.2025 İTİBAREN.mdb"


class MDBImporter:
    """MDB dosyasından SQLite'a veri aktarımı"""
    
    def __init__(self, mdb_path: str):
        self.mdb_path = mdb_path
        self.db = None
        self.mdb_conn = None
        
    def connect_mdb(self):
        """MDB dosyasına bağlan"""
        if not os.path.exists(self.mdb_path):
            raise FileNotFoundError(f"MDB dosyası bulunamadı: {self.mdb_path}")
        
        # Driver'ları dene
        drivers = [
            'Microsoft Access Driver (*.mdb, *.accdb)',
            'Microsoft Access Driver (*.mdb)',
            'Driver do Microsoft Access (*.mdb)',
        ]
        
        conn_str = None
        for driver in drivers:
            try:
                if driver in pyodbc.drivers():
                    conn_str = f'DRIVER={{{driver}}};DBQ={self.mdb_path};'
                    break
            except:
                continue
        
        if not conn_str:
            conn_str = f'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={self.mdb_path};'
        
        print(f"🔌 MDB'ye bağlanılıyor: {os.path.basename(self.mdb_path)}")
        self.mdb_conn = pyodbc.connect(conn_str)
        print("✅ Bağlantı başarılı!")
        return self.mdb_conn
    
    def get_mdb_tables(self) -> list:
        """MDB dosyasındaki tabloları listele"""
        cursor = self.mdb_conn.cursor()
        tables = []
        for row in cursor.tables(tableType='TABLE'):
            if not row.table_name.startswith('MSys'):
                tables.append(row.table_name)
        return tables
    
    def import_gerekli_bilgiler(self):
        """Gerekli Bilgiler tablosunu aktar"""
        print("\n📋 Gerekli Bilgiler tablosu aktarılıyor...")
        
        cursor = self.mdb_conn.cursor()
        try:
            cursor.execute("SELECT * FROM [Gerekli Bilgiler]")
            row = cursor.fetchone()
            
            if row:
                columns = [column[0] for column in cursor.description]
                data = dict(zip(columns, row))
                
                # Veriyi SQLite formatına dönüştür
                cezaevi_data = {
                    'cezaevi': data.get('Cezaevi', ''),
                    'mudur': data.get('CezaeviMüdürü', ''),
                    'ambar_memuru': data.get('AmbarMemuru', ''),
                    'uye1': data.get('Üye1', ''),
                    'uye2': data.get('Üye2', ''),
                    'uye3': data.get('Üye3', ''),
                    'sabah_miktar': float(data.get('SabahMiktar', 0) or 0),
                    'ogle_miktar': float(data.get('ÖyleMiktar', 0) or 0),
                    'aksam_miktar': float(data.get('AkşamMiktar', 0) or 0),
                    'toplam_miktar': float(data.get('ToplamMiktar', 0) or 0),
                    'sabah_ekmek': int(data.get('SabahEkmeği', 0) or 0),
                    'ogle_ekmek': int(data.get('ÖğlenEkmeği', 0) or 0),
                    'aksam_ekmek': int(data.get('AkşamEkmeği', 0) or 0),
                    'toplam_ekmek': int(data.get('ToplamEkmek', 0) or 0)
                }
                
                self.db.update_cezaevi_bilgileri(cezaevi_data)
                print(f"   ✅ 1 kayıt aktarıldı")
            else:
                print("   ⚠️ Kayıt bulunamadı")
        except Exception as e:
            print(f"   ❌ Hata: {e}")
    
    def import_urunler(self):
        """Ürünler tablosunu aktar"""
        print("\n📦 Ürünler tablosu aktarılıyor...")
        
        cursor = self.mdb_conn.cursor()
        try:
            cursor.execute("SELECT * FROM [Ürünler]")
            count = 0
            
            for row in cursor.fetchall():
                columns = [column[0] for column in cursor.description]
                data = dict(zip(columns, row))
                
                # Veriyi ekle
                self.db.cursor.execute("""
                    INSERT INTO urunler (urun_no, cinsi, defter_no, kalorisi, birimi, fiyati)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    data.get('ÜrünNo'),
                    data.get('Cinsi', ''),
                    data.get('DefterNo'),
                    int(data.get('Kalorisi', 0) or 0),
                    data.get('Birimi', ''),
                    float(data.get('Fiatı', 0) or 0)
                ))
                count += 1
            
            self.db.conn.commit()
            print(f"   ✅ {count} kayıt aktarıldı")
        except Exception as e:
            print(f"   ❌ Hata: {e}")
    
    def import_tabela_alt(self):
        """Tabela Alt tablosunu aktar"""
        print("\n📊 Tabela Alt tablosu aktarılıyor...")
        
        cursor = self.mdb_conn.cursor()
        try:
            cursor.execute("SELECT * FROM [Tabela Alt]")
            count = 0
            
            for row in cursor.fetchall():
                columns = [column[0] for column in cursor.description]
                data = dict(zip(columns, row))
                
                # Tarih dönüştürme
                tarih = data.get('Tarih')
                if tarih and isinstance(tarih, datetime):
                    tarih = tarih.strftime('%Y-%m-%d')
                elif tarih:
                    tarih = str(tarih)
                
                # Veriyi ekle
                self.db.cursor.execute("""
                    INSERT INTO gunluk_tabela (
                        sira_no, tabela_no, tarih, mevcut, ogun,
                        urun_no, cinsi, stok_mevcudu, verilen, fiyati,
                        kalorisi, defter_no, tutar, sahis_tutar, sahis_miktar, sahis_kalori
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    data.get('SıraNo'),
                    data.get('TabelaNo'),
                    tarih,
                    int(data.get('Mevcut', 0) or 0),
                    data.get('Öğün', ''),
                    data.get('ÜrünNo'),
                    data.get('Cinsi', ''),
                    float(data.get('StokMevcudu', 0) or 0),
                    float(data.get('Verilen', 0) or 0),
                    float(data.get('Fiyatı', 0) or 0),
                    int(data.get('Kalorisi', 0) or 0) if 'Kalorisi' in data else 0,
                    data.get('DefterNo') if 'DefterNo' in data else None,
                    float(data.get('Tutar', 0) or 0),
                    float(data.get('ŞahısTutar', 0) or 0),
                    float(data.get('ŞahısMiktar', 0) or 0),
                    float(data.get('ŞahısKalori', 0) or 0)
                ))
                count += 1
                
                # Her 1000 kayıtta bir commit
                if count % 1000 == 0:
                    self.db.conn.commit()
                    print(f"   📝 {count} kayıt işlendi...")
            
            self.db.conn.commit()
            print(f"   ✅ Toplam {count} kayıt aktarıldı")
        except Exception as e:
            print(f"   ❌ Hata: {e}")
            import traceback
            traceback.print_exc()
    
    def import_firmalar(self):
        """Firma Adları tablosunu aktar"""
        print("\n🏢 Firma Adları tablosu aktarılıyor...")
        
        cursor = self.mdb_conn.cursor()
        try:
            cursor.execute("SELECT * FROM [Firma Adları]")
            count = 0
            
            for row in cursor.fetchall():
                columns = [column[0] for column in cursor.description]
                data = dict(zip(columns, row))
                
                self.db.cursor.execute("""
                    INSERT INTO firmalar (firma_adi)
                    VALUES (?)
                """, (data.get('FirmaAdı', data.get('Firma', '')),))
                count += 1
            
            self.db.conn.commit()
            print(f"   ✅ {count} kayıt aktarıldı")
        except Exception as e:
            print(f"   ⚠️ Tablo bulunamadı veya hata: {e}")
    
    def import_memurlar(self):
        """Memur tablosunu aktar"""
        print("\n👤 Memur tablosu aktarılıyor...")
        
        cursor = self.mdb_conn.cursor()
        try:
            cursor.execute("SELECT * FROM [Memur]")
            count = 0
            
            for row in cursor.fetchall():
                columns = [column[0] for column in cursor.description]
                data = dict(zip(columns, row))
                
                self.db.cursor.execute("""
                    INSERT INTO memurlar (memur, unvan)
                    VALUES (?, ?)
                """, (data.get('Memur', ''), data.get('Ünvan', '')))
                count += 1
            
            self.db.conn.commit()
            print(f"   ✅ {count} kayıt aktarıldı")
        except Exception as e:
            print(f"   ⚠️ Tablo bulunamadı veya hata: {e}")
    
    def import_all(self):
        """Tüm verileri aktar"""
        print("=" * 60)
        print("🗂️  MDB -> SQLite Veri Aktarımı")
        print("=" * 60)
        
        try:
            # MDB'ye bağlan
            self.connect_mdb()
            
            # Tabloları listele
            tables = self.get_mdb_tables()
            print(f"\n📊 Bulunan tablolar: {', '.join(tables)}")
            
            # SQLite veritabanını hazırla
            print(f"\n💾 SQLite veritabanı hazırlanıyor...")
            init_database()
            
            # Veritabanına bağlan
            self.db = Database()
            self.db.connect()
            
            # Tabloları aktar
            self.import_gerekli_bilgiler()
            self.import_urunler()
            self.import_tabela_alt()
            self.import_firmalar()
            self.import_memurlar()
            
            # İstatistikler
            print("\n" + "=" * 60)
            print("📊 AKTARIM İSTATİSTİKLERİ")
            print("=" * 60)
            
            # Kayıt sayılarını göster
            stats = [
                ("Cezaevi Bilgileri", "SELECT COUNT(*) FROM cezaevi_bilgileri"),
                ("Ürünler", "SELECT COUNT(*) FROM urunler"),
                ("Günlük Tabela", "SELECT COUNT(*) FROM gunluk_tabela"),
                ("Firmalar", "SELECT COUNT(*) FROM firmalar"),
                ("Memurlar", "SELECT COUNT(*) FROM memurlar")
            ]
            
            for name, query in stats:
                self.db.cursor.execute(query)
                count = self.db.cursor.fetchone()[0]
                print(f"   • {name}: {count} kayıt")
            
            print("\n✅ Tüm veriler başarıyla aktarıldı!")
            print(f"📁 Veritabanı: {self.db.db_path}")
            
        except Exception as e:
            print(f"\n❌ HATA: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            if self.db:
                self.db.disconnect()
            if self.mdb_conn:
                self.mdb_conn.close()
        
        return True


def main():
    """Ana fonksiyon"""
    if not os.path.exists(MDB_FILE):
        print(f"❌ MDB dosyası bulunamadı: {MDB_FILE}")
        print("Lütfen MDB dosyasını proje dizinine koyun.")
        return
    
    importer = MDBImporter(MDB_FILE)
    success = importer.import_all()
    
    if success:
        print("\n🎉 İşlem tamamlandı!")
        print("Şimdi uygulamayı başlatabilirsiniz: python main.py")
    else:
        print("\n❌ İşlem başarısız oldu!")


if __name__ == "__main__":
    main()
