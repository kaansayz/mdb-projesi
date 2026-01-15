# -*- coding: utf-8 -*-
"""
Veritabanı İşlemleri
SQLite veritabanı bağlantı ve CRUD işlemleri
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple, Any

DB_PATH = "data/cezaevi_gida.db"


class Database:
    """SQLite veritabanı yönetim sınıfı"""
    
    def __init__(self, db_path: str = DB_PATH):
        """Veritabanı bağlantısını başlat"""
        self.db_path = db_path
        self.ensure_data_dir()
        self.conn = None
        self.cursor = None
    
    def ensure_data_dir(self):
        """Data dizininin var olduğundan emin ol"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def connect(self):
        """Veritabanına bağlan"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Dict-like access
        self.cursor = self.conn.cursor()
        return self.conn
    
    def disconnect(self):
        """Veritabanı bağlantısını kapat"""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
    
    def __enter__(self):
        """Context manager enter"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()
    
    def create_tables(self):
        """Tüm tabloları oluştur"""
        self.connect()
        
        # Cezaevi bilgileri tablosu
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS cezaevi_bilgileri (
                id INTEGER PRIMARY KEY,
                cezaevi TEXT,
                mudur TEXT,
                ambar_memuru TEXT,
                uye1 TEXT,
                uye2 TEXT,
                uye3 TEXT,
                sabah_miktar REAL DEFAULT 0,
                ogle_miktar REAL DEFAULT 0,
                aksam_miktar REAL DEFAULT 0,
                toplam_miktar REAL DEFAULT 0,
                sabah_ekmek INTEGER DEFAULT 0,
                ogle_ekmek INTEGER DEFAULT 0,
                aksam_ekmek INTEGER DEFAULT 0,
                toplam_ekmek INTEGER DEFAULT 0
            )
        """)
        
        # Ürünler tablosu
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS urunler (
                urun_no INTEGER PRIMARY KEY AUTOINCREMENT,
                cinsi TEXT NOT NULL,
                defter_no INTEGER,
                kalorisi INTEGER DEFAULT 0,
                birimi TEXT,
                fiyati REAL DEFAULT 0
            )
        """)
        
        # Günlük tabela tablosu
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS gunluk_tabela (
                sira_no INTEGER PRIMARY KEY AUTOINCREMENT,
                tabela_no INTEGER,
                tarih DATE,
                mevcut INTEGER,
                ogun TEXT CHECK(ogun IN ('SABAH', 'ÖĞLE', 'AKŞAM')),
                urun_no INTEGER,
                cinsi TEXT,
                stok_mevcudu REAL DEFAULT 0,
                verilen REAL DEFAULT 0,
                fiyati REAL DEFAULT 0,
                kalorisi INTEGER DEFAULT 0,
                defter_no INTEGER,
                tutar REAL DEFAULT 0,
                sahis_tutar REAL DEFAULT 0,
                sahis_miktar REAL DEFAULT 0,
                sahis_kalori REAL DEFAULT 0,
                FOREIGN KEY (urun_no) REFERENCES urunler(urun_no)
            )
        """)
        
        # Firmalar tablosu
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS firmalar (
                firma_no INTEGER PRIMARY KEY AUTOINCREMENT,
                firma_adi TEXT NOT NULL
            )
        """)
        
        # Memurlar tablosu
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS memurlar (
                kayit_no INTEGER PRIMARY KEY AUTOINCREMENT,
                memur TEXT,
                unvan TEXT
            )
        """)
        
        # Raporlar tablosu
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS raporlar (
                rapor_no INTEGER PRIMARY KEY,
                rapor_etiketi TEXT,
                rapor_adi TEXT
            )
        """)
        
        self.conn.commit()
    
    # CEZAEVI BİLGİLERİ İŞLEMLERİ
    
    def get_cezaevi_bilgileri(self) -> Optional[Dict]:
        """Cezaevi bilgilerini getir"""
        self.cursor.execute("SELECT * FROM cezaevi_bilgileri WHERE id = 1")
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def update_cezaevi_bilgileri(self, data: Dict):
        """Cezaevi bilgilerini güncelle"""
        # İlk kayıt yoksa oluştur
        existing = self.get_cezaevi_bilgileri()
        if not existing:
            self.cursor.execute("""
                INSERT INTO cezaevi_bilgileri (id, cezaevi, mudur, ambar_memuru,
                    uye1, uye2, uye3, sabah_miktar, ogle_miktar, aksam_miktar,
                    toplam_miktar, sabah_ekmek, ogle_ekmek, aksam_ekmek, toplam_ekmek)
                VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data.get('cezaevi', ''),
                data.get('mudur', ''),
                data.get('ambar_memuru', ''),
                data.get('uye1', ''),
                data.get('uye2', ''),
                data.get('uye3', ''),
                data.get('sabah_miktar', 0),
                data.get('ogle_miktar', 0),
                data.get('aksam_miktar', 0),
                data.get('toplam_miktar', 0),
                data.get('sabah_ekmek', 0),
                data.get('ogle_ekmek', 0),
                data.get('aksam_ekmek', 0),
                data.get('toplam_ekmek', 0)
            ))
        else:
            self.cursor.execute("""
                UPDATE cezaevi_bilgileri SET
                    cezaevi = ?, mudur = ?, ambar_memuru = ?,
                    uye1 = ?, uye2 = ?, uye3 = ?,
                    sabah_miktar = ?, ogle_miktar = ?, aksam_miktar = ?,
                    toplam_miktar = ?, sabah_ekmek = ?, ogle_ekmek = ?,
                    aksam_ekmek = ?, toplam_ekmek = ?
                WHERE id = 1
            """, (
                data.get('cezaevi', ''),
                data.get('mudur', ''),
                data.get('ambar_memuru', ''),
                data.get('uye1', ''),
                data.get('uye2', ''),
                data.get('uye3', ''),
                data.get('sabah_miktar', 0),
                data.get('ogle_miktar', 0),
                data.get('aksam_miktar', 0),
                data.get('toplam_miktar', 0),
                data.get('sabah_ekmek', 0),
                data.get('ogle_ekmek', 0),
                data.get('aksam_ekmek', 0),
                data.get('toplam_ekmek', 0)
            ))
        self.conn.commit()
    
    # ÜRÜN İŞLEMLERİ
    
    def get_all_urunler(self) -> List[Dict]:
        """Tüm ürünleri getir"""
        self.cursor.execute("""
            SELECT * FROM urunler ORDER BY cinsi
        """)
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_urun(self, urun_no: int) -> Optional[Dict]:
        """Belirli bir ürünü getir"""
        self.cursor.execute("SELECT * FROM urunler WHERE urun_no = ?", (urun_no,))
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def add_urun(self, cinsi: str, defter_no: int = None, kalorisi: int = 0,
                 birimi: str = '', fiyati: float = 0) -> int:
        """Yeni ürün ekle"""
        self.cursor.execute("""
            INSERT INTO urunler (cinsi, defter_no, kalorisi, birimi, fiyati)
            VALUES (?, ?, ?, ?, ?)
        """, (cinsi, defter_no, kalorisi, birimi, fiyati))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def update_urun(self, urun_no: int, cinsi: str, defter_no: int = None,
                    kalorisi: int = 0, birimi: str = '', fiyati: float = 0):
        """Ürün bilgilerini güncelle"""
        self.cursor.execute("""
            UPDATE urunler SET
                cinsi = ?, defter_no = ?, kalorisi = ?, birimi = ?, fiyati = ?
            WHERE urun_no = ?
        """, (cinsi, defter_no, kalorisi, birimi, fiyati, urun_no))
        self.conn.commit()
    
    def delete_urun(self, urun_no: int):
        """Ürünü sil"""
        self.cursor.execute("DELETE FROM urunler WHERE urun_no = ?", (urun_no,))
        self.conn.commit()
    
    def search_urunler(self, search_term: str) -> List[Dict]:
        """Ürünlerde arama yap"""
        self.cursor.execute("""
            SELECT * FROM urunler 
            WHERE cinsi LIKE ? OR birimi LIKE ?
            ORDER BY cinsi
        """, (f'%{search_term}%', f'%{search_term}%'))
        return [dict(row) for row in self.cursor.fetchall()]
    
    # GÜNLÜK TABELA İŞLEMLERİ
    
    def get_tabela_by_date_and_ogun(self, tarih: str, ogun: str) -> List[Dict]:
        """Belirli tarih ve öğün için tabela kayıtlarını getir"""
        self.cursor.execute("""
            SELECT * FROM gunluk_tabela
            WHERE tarih = ? AND ogun = ?
            ORDER BY sira_no
        """, (tarih, ogun))
        return [dict(row) for row in self.cursor.fetchall()]
    
    def add_tabela_kayit(self, data: Dict) -> int:
        """Yeni tabela kaydı ekle"""
        self.cursor.execute("""
            INSERT INTO gunluk_tabela (
                tabela_no, tarih, mevcut, ogun, urun_no, cinsi,
                stok_mevcudu, verilen, fiyati, kalorisi, defter_no,
                tutar, sahis_tutar, sahis_miktar, sahis_kalori
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get('tabela_no', 0),
            data.get('tarih'),
            data.get('mevcut', 0),
            data.get('ogun'),
            data.get('urun_no'),
            data.get('cinsi', ''),
            data.get('stok_mevcudu', 0),
            data.get('verilen', 0),
            data.get('fiyati', 0),
            data.get('kalorisi', 0),
            data.get('defter_no'),
            data.get('tutar', 0),
            data.get('sahis_tutar', 0),
            data.get('sahis_miktar', 0),
            data.get('sahis_kalori', 0)
        ))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def delete_tabela_kayit(self, sira_no: int):
        """Tabela kaydını sil"""
        self.cursor.execute("DELETE FROM gunluk_tabela WHERE sira_no = ?", (sira_no,))
        self.conn.commit()
    
    def get_tabela_by_date_range(self, start_date: str, end_date: str) -> List[Dict]:
        """Tarih aralığına göre tabela kayıtlarını getir"""
        self.cursor.execute("""
            SELECT * FROM gunluk_tabela
            WHERE tarih BETWEEN ? AND ?
            ORDER BY tarih, ogun, sira_no
        """, (start_date, end_date))
        return [dict(row) for row in self.cursor.fetchall()]
    
    # STOK İŞLEMLERİ
    
    def get_stok_durumu(self) -> List[Dict]:
        """Tüm ürünlerin stok durumunu getir"""
        self.cursor.execute("""
            SELECT 
                u.urun_no,
                u.cinsi,
                u.birimi,
                COALESCE(SUM(gt.stok_mevcudu), 0) as toplam_stok
            FROM urunler u
            LEFT JOIN gunluk_tabela gt ON u.urun_no = gt.urun_no
            GROUP BY u.urun_no, u.cinsi, u.birimi
            ORDER BY u.cinsi
        """)
        return [dict(row) for row in self.cursor.fetchall()]
    
    # RAPOR İŞLEMLERİ
    
    def get_malzeme_giris_raporu(self, start_date: str, end_date: str) -> List[Dict]:
        """Malzeme giriş raporunu getir"""
        # Bu örnekte tabela verileri kullanılıyor
        # Gerçek uygulamada ayrı bir giriş tablosu olabilir
        self.cursor.execute("""
            SELECT 
                tarih, cinsi, stok_mevcudu as giris_miktari,
                birimi, fiyati, tutar
            FROM gunluk_tabela gt
            JOIN urunler u ON gt.urun_no = u.urun_no
            WHERE tarih BETWEEN ? AND ? AND stok_mevcudu > 0
            ORDER BY tarih, cinsi
        """, (start_date, end_date))
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_malzeme_cikis_raporu(self, start_date: str, end_date: str) -> List[Dict]:
        """Malzeme çıkış raporunu getir"""
        self.cursor.execute("""
            SELECT 
                tarih, ogun, cinsi, verilen as cikis_miktari,
                birimi, fiyati, tutar, mevcut
            FROM gunluk_tabela gt
            JOIN urunler u ON gt.urun_no = u.urun_no
            WHERE tarih BETWEEN ? AND ? AND verilen > 0
            ORDER BY tarih, ogun, cinsi
        """, (start_date, end_date))
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_urun_bazli_rapor(self, start_date: str, end_date: str) -> List[Dict]:
        """Ürünlere göre giriş/çıkış raporu"""
        self.cursor.execute("""
            SELECT 
                cinsi,
                birimi,
                SUM(stok_mevcudu) as toplam_giris,
                SUM(verilen) as toplam_cikis,
                SUM(tutar) as toplam_tutar,
                COUNT(*) as islem_sayisi
            FROM gunluk_tabela gt
            JOIN urunler u ON gt.urun_no = u.urun_no
            WHERE tarih BETWEEN ? AND ?
            GROUP BY cinsi, birimi
            ORDER BY toplam_tutar DESC
        """, (start_date, end_date))
        return [dict(row) for row in self.cursor.fetchall()]
    
    # YARDIMCI FONKSİYONLAR
    
    def execute_query(self, query: str, params: Tuple = ()) -> List[Dict]:
        """Özel sorgu çalıştır"""
        self.cursor.execute(query, params)
        return [dict(row) for row in self.cursor.fetchall()]
    
    def init_default_data(self):
        """Varsayılan verileri ekle"""
        # Cezaevi bilgileri
        existing = self.get_cezaevi_bilgileri()
        if not existing:
            self.update_cezaevi_bilgileri({
                'cezaevi': 'Örnek Cezaevi',
                'mudur': '',
                'ambar_memuru': '',
                'uye1': '',
                'uye2': '',
                'uye3': '',
                'sabah_miktar': 0,
                'ogle_miktar': 0,
                'aksam_miktar': 0,
                'toplam_miktar': 0,
                'sabah_ekmek': 0,
                'ogle_ekmek': 0,
                'aksam_ekmek': 0,
                'toplam_ekmek': 0
            })


def init_database():
    """Veritabanını başlat"""
    with Database() as db:
        db.create_tables()
        db.init_default_data()
    print("✅ Veritabanı başarıyla oluşturuldu!")


if __name__ == "__main__":
    init_database()
