#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MDB Dosyası Analiz Scripti
Bu script, Microsoft Access veritabanı (.mdb) dosyalarını analiz eder
ve içeriği hakkında detaylı rapor üretir.
"""

import os
import sys
import pyodbc
import pandas as pd
from datetime import datetime


class MDBAnalyzer:
    """Microsoft Access veritabanı analiz sınıfı"""
    
    def __init__(self, mdb_file):
        """
        MDB analiz sınıfını başlat
        
        Args:
            mdb_file (str): Analiz edilecek MDB dosyasının yolu
        """
        self.mdb_file = mdb_file
        self.conn = None
        self.output_lines = []
        
    def connect(self):
        """MDB dosyasına bağlan"""
        if not os.path.exists(self.mdb_file):
            raise FileNotFoundError(f"MDB dosyası bulunamadı: {self.mdb_file}")
        
        # Microsoft Access Driver bul
        drivers = [x for x in pyodbc.drivers() if 'Access' in x or 'access' in x]
        if not drivers:
            raise Exception(
                "Microsoft Access Driver bulunamadı!\n"
                "Lütfen Microsoft Access Database Engine'i yükleyin:\n"
                "https://www.microsoft.com/en-us/download/details.aspx?id=54920"
            )
        
        driver = drivers[0]
        conn_str = f'DRIVER={{{driver}}};DBQ={self.mdb_file};'
        
        try:
            self.conn = pyodbc.connect(conn_str)
            return True
        except Exception as e:
            raise Exception(f"Veritabanına bağlanırken hata: {str(e)}")
    
    def log(self, message):
        """Mesajı hem ekrana yazdır hem de çıktı listesine ekle"""
        print(message)
        self.output_lines.append(message)
    
    def get_tables(self):
        """Veritabanındaki kullanıcı tablolarını listele"""
        cursor = self.conn.cursor()
        tables = []
        
        for table_info in cursor.tables(tableType='TABLE'):
            table_name = table_info.table_name
            # Sistem tablolarını filtrele
            if not table_name.startswith('MSys'):
                tables.append(table_name)
        
        return sorted(tables)
    
    def get_table_info(self, table_name):
        """
        Belirtilen tablo hakkında detaylı bilgi al
        
        Args:
            table_name (str): Tablo adı
            
        Returns:
            dict: Tablo bilgileri
        """
        cursor = self.conn.cursor()
        
        # Sütun bilgilerini al
        columns = []
        for column in cursor.columns(table=table_name):
            col_name = column.column_name
            col_type = column.type_name
            columns.append((col_name, col_type))
        
        # Kayıt sayısını al
        try:
            cursor.execute(f"SELECT COUNT(*) FROM [{table_name}]")
            record_count = cursor.fetchone()[0]
        except:
            record_count = 0
        
        # İlk 5 satırı al
        sample_data = None
        try:
            query = f"SELECT TOP 5 * FROM [{table_name}]"
            sample_data = pd.read_sql(query, self.conn)
        except Exception as e:
            sample_data = None
        
        return {
            'name': table_name,
            'columns': columns,
            'record_count': record_count,
            'sample_data': sample_data
        }
    
    def get_queries(self):
        """Veritabanındaki sorguları listele"""
        cursor = self.conn.cursor()
        queries = []
        
        try:
            for table_info in cursor.tables(tableType='VIEW'):
                queries.append(table_info.table_name)
        except:
            pass
        
        return sorted(queries)
    
    def get_relationships(self):
        """Tablolar arasındaki ilişkileri listele"""
        cursor = self.conn.cursor()
        relationships = []
        
        try:
            # Tüm tablolar için foreign key ilişkilerini kontrol et
            tables = self.get_tables()
            for table in tables:
                try:
                    for fk in cursor.foreignKeys(table=table):
                        relationships.append({
                            'fk_table': fk.fktable_name,
                            'fk_column': fk.fkcolumn_name,
                            'pk_table': fk.pktable_name,
                            'pk_column': fk.pkcolumn_name
                        })
                except:
                    continue
        except:
            pass
        
        return relationships
    
    def analyze(self):
        """Tam analiz yap ve rapor üret"""
        try:
            self.connect()
            
            # Başlık
            self.log("🔍 MDB DOSYASI ANALİZ RAPORU")
            self.log("=" * 50)
            self.log("")
            self.log(f"📁 Dosya: {os.path.basename(self.mdb_file)}")
            self.log(f"📅 Analiz Tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
            
            # Tabloları al
            tables = self.get_tables()
            self.log(f"📊 Toplam Tablo Sayısı: {len(tables)}")
            self.log("")
            
            # Her tablo için detaylı analiz
            for table_name in tables:
                self.log("─" * 50)
                self.log(f"📋 TABLO: {table_name}")
                self.log("─" * 50)
                
                table_info = self.get_table_info(table_name)
                
                self.log(f"📝 Kayıt Sayısı: {table_info['record_count']}")
                self.log("")
                self.log("📌 Sütunlar:")
                for col_name, col_type in table_info['columns']:
                    self.log(f"  - {col_name} ({col_type})")
                self.log("")
                
                # Örnek verileri göster
                if table_info['sample_data'] is not None and not table_info['sample_data'].empty:
                    self.log("💾 Örnek Veriler (İlk 5 satır):")
                    # DataFrame'i string'e çevir
                    sample_str = table_info['sample_data'].to_string(index=False)
                    for line in sample_str.split('\n'):
                        self.log(f"  {line}")
                else:
                    self.log("💾 Örnek Veriler: Veri bulunamadı veya okunamadı")
                
                self.log("")
            
            # İlişkileri göster
            self.log("─" * 50)
            self.log("🔗 İLİŞKİLER")
            self.log("─" * 50)
            relationships = self.get_relationships()
            if relationships:
                for rel in relationships:
                    self.log(f"  {rel['fk_table']}.{rel['fk_column']} -> "
                           f"{rel['pk_table']}.{rel['pk_column']}")
            else:
                self.log("  İlişki bulunamadı")
            self.log("")
            
            # Sorguları listele
            self.log("─" * 50)
            self.log("📜 SORGULAR")
            self.log("─" * 50)
            queries = self.get_queries()
            if queries:
                for query in queries:
                    self.log(f"  - {query}")
            else:
                self.log("  Sorgu bulunamadı")
            self.log("")
            
            # VBA modülleri için not
            self.log("─" * 50)
            self.log("⚙️ VBA MODÜLLERİ")
            self.log("─" * 50)
            self.log("  Not: VBA modüllerinin okunması ODBC sürücüsü ile desteklenmemektedir.")
            self.log("  VBA modüllerini görmek için Microsoft Access uygulamasını kullanın.")
            self.log("")
            
            self.log("=" * 50)
            self.log("✅ Analiz tamamlandı!")
            
        except Exception as e:
            self.log(f"\n❌ HATA: {str(e)}")
            raise
        finally:
            if self.conn:
                self.conn.close()
    
    def save_report(self, output_file="RAPOR.txt"):
        """Raporu dosyaya kaydet"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(self.output_lines))
            print(f"\n💾 Rapor kaydedildi: {output_file}")
            return True
        except Exception as e:
            print(f"\n❌ Rapor kaydedilirken hata: {str(e)}")
            return False


def main():
    """Ana fonksiyon"""
    # MDB dosyasının yolu
    script_dir = os.path.dirname(os.path.abspath(__file__))
    mdb_file = os.path.join(script_dir, "04.08.2025 İTİBAREN.mdb")
    
    # Komut satırından dosya adı alınabilir
    if len(sys.argv) > 1:
        mdb_file = sys.argv[1]
    
    print("=" * 50)
    print("MDB DOSYASI ANALİZ ARACI")
    print("=" * 50)
    print()
    
    try:
        # Analiz yap
        analyzer = MDBAnalyzer(mdb_file)
        analyzer.analyze()
        
        # Raporu kaydet
        analyzer.save_report("RAPOR.txt")
        
    except Exception as e:
        print(f"\n❌ Program hatası: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
