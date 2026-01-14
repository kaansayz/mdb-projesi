#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MDB Dosyası Analiz Programı
Bu program Microsoft Access (.mdb) dosyalarını okur ve içeriğini analiz eder.
"""

import sys
import os
from datetime import datetime

def print_and_log(message, file_handle=None):
    """Mesajı hem ekrana hem dosyaya yaz"""
    print(message)
    if file_handle:
        file_handle.write(message + '\n')

def analyze_mdb_file(mdb_path, output_file='RAPOR.txt'):
    """MDB dosyasını analiz et ve rapor oluştur"""
    
    # Çıktı dosyasını aç
    with open(output_file, 'w', encoding='utf-8') as f:
        
        # Başlık
        header = """
🔍 MDB DOSYASI ANALİZ RAPORU
================================
"""
        print_and_log(header, f)
        print_and_log(f"📁 Dosya: {os.path.basename(mdb_path)}", f)
        print_and_log(f"📅 Analiz Tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}", f)
        print_and_log(f"📍 Dosya Yolu: {os.path.abspath(mdb_path)}", f)
        print_and_log(f"💾 Dosya Boyutu: {os.path.getsize(mdb_path) / (1024*1024):.2f} MB", f)
        print_and_log("", f)
        
        try:
            import pyodbc
            
            # Access Driver'ı bul
            drivers = [driver for driver in pyodbc.drivers() if 'Access' in driver or 'access' in driver.lower()]
            
            if not drivers:
                error_msg = """
❌ HATA: Microsoft Access Driver bulunamadı!

Windows'ta Access Driver kurulumu için:
1. 32-bit Python kullanıyorsanız: Microsoft Access Database Engine 2010 (32-bit)
2. 64-bit Python kullanıyorsanız: Microsoft Access Database Engine 2016 (64-bit)

İndirme linkleri:
- 32-bit: https://www.microsoft.com/en-us/download/details.aspx?id=13255
- 64-bit: https://www.microsoft.com/en-us/download/details.aspx?id=54920

Kurulum sonrası programı tekrar çalıştırın.
"""
                print_and_log(error_msg, f)
                return False
            
            driver = drivers[0]
            print_and_log(f"✅ Kullanılan Driver: {driver}", f)
            print_and_log("", f)
            
            # MDB dosyasına bağlan
            conn_str = f'DRIVER={{{driver}}};DBQ={mdb_path};'
            print_and_log("🔌 Veritabanına bağlanılıyor...", f)
            
            try:
                conn = pyodbc.connect(conn_str)
                cursor = conn.cursor()
                print_and_log("✅ Bağlantı başarılı!", f)
                print_and_log("", f)
                
                # Tabloları listele (sistem tablolarını hariç tut)
                tables = []
                for table_info in cursor.tables(tableType='TABLE'):
                    table_name = table_info.table_name
                    # MSys ile başlayan sistem tablolarını atla
                    if not table_name.startswith('MSys'):
                        tables.append(table_name)
                
                print_and_log(f"📊 Toplam Tablo Sayısı: {len(tables)}", f)
                print_and_log("", f)
                
                # Her tablo için detaylı bilgi
                for table_name in tables:
                    print_and_log("─" * 50, f)
                    print_and_log(f"📋 TABLO: {table_name}", f)
                    print_and_log("─" * 50, f)
                    
                    try:
                        # Sütun bilgilerini al
                        columns = []
                        for column in cursor.columns(table=table_name):
                            col_name = column.column_name
                            col_type = column.type_name
                            columns.append((col_name, col_type))
                        
                        print_and_log(f"📌 Sütunlar ({len(columns)} adet):", f)
                        for col_name, col_type in columns:
                            print_and_log(f"  • {col_name} ({col_type})", f)
                        print_and_log("", f)
                        
                        # Kayıt sayısını al
                        try:
                            cursor.execute(f"SELECT COUNT(*) FROM [{table_name}]")
                            count = cursor.fetchone()[0]
                            print_and_log(f"📝 Kayıt Sayısı: {count}", f)
                        except Exception as e:
                            print_and_log(f"⚠️  Kayıt sayısı alınamadı: {str(e)}", f)
                            count = 0
                        
                        # İlk 5 satırı göster (eğer veri varsa)
                        if count > 0:
                            print_and_log("", f)
                            print_and_log("💾 Örnek Veriler (İlk 5 satır):", f)
                            try:
                                cursor.execute(f"SELECT TOP 5 * FROM [{table_name}]")
                                rows = cursor.fetchall()
                                
                                if rows:
                                    # Sütun isimlerini yazdır
                                    col_names = [desc[0] for desc in cursor.description]
                                    print_and_log("  " + " | ".join(col_names), f)
                                    print_and_log("  " + "-" * (len(" | ".join(col_names))), f)
                                    
                                    # Satırları yazdır
                                    for row in rows:
                                        row_str = " | ".join([str(val) if val is not None else "NULL" for val in row])
                                        print_and_log(f"  {row_str}", f)
                            except Exception as e:
                                print_and_log(f"⚠️  Örnek veriler alınamadı: {str(e)}", f)
                        
                        print_and_log("", f)
                        
                    except Exception as e:
                        print_and_log(f"❌ Tablo bilgisi alınırken hata: {str(e)}", f)
                        print_and_log("", f)
                
                # Sorguları listele
                print_and_log("─" * 50, f)
                print_and_log("📜 SORGULAR (QUERIES):", f)
                print_and_log("─" * 50, f)
                
                queries = []
                for table_info in cursor.tables(tableType='VIEW'):
                    query_name = table_info.table_name
                    if not query_name.startswith('MSys'):
                        queries.append(query_name)
                
                if queries:
                    for query_name in queries:
                        print_and_log(f"  • {query_name}", f)
                else:
                    print_and_log("  (Sorgu bulunamadı)", f)
                
                print_and_log("", f)
                
                # VBA modülleri hakkında not
                print_and_log("─" * 50, f)
                print_and_log("⚙️  VBA MODÜLLERİ:", f)
                print_and_log("─" * 50, f)
                print_and_log("ℹ️  VBA modüllerini okumak için Microsoft Access uygulaması gerekir.", f)
                print_and_log("   ODBC bağlantısı ile VBA kodlarına erişim mümkün değildir.", f)
                print_and_log("", f)
                
                # İlişkiler hakkında not
                print_and_log("─" * 50, f)
                print_and_log("🔗 İLİŞKİLER (RELATIONSHIPS):", f)
                print_and_log("─" * 50, f)
                
                try:
                    # Foreign key bilgilerini almaya çalış
                    relationships_found = False
                    for table_name in tables:
                        try:
                            fks = cursor.foreignKeys(table=table_name)
                            fk_list = list(fks)
                            if fk_list:
                                relationships_found = True
                                print_and_log(f"  Tablo: {table_name}", f)
                                for fk in fk_list:
                                    print_and_log(f"    • {fk.fk_column_name} -> {fk.pktable_name}.{fk.pk_column_name}", f)
                        except:
                            pass
                    
                    if not relationships_found:
                        print_and_log("  (İlişki bulunamadı veya erişilemiyor)", f)
                except Exception as e:
                    print_and_log(f"  ℹ️  İlişki bilgisi alınamadı: {str(e)}", f)
                
                print_and_log("", f)
                print_and_log("=" * 50, f)
                print_and_log("✅ Analiz tamamlandı!", f)
                print_and_log(f"📄 Rapor dosyası: {output_file}", f)
                print_and_log("=" * 50, f)
                
                conn.close()
                return True
                
            except pyodbc.Error as e:
                error_msg = f"""
❌ Veritabanı bağlantı hatası:
{str(e)}

Olası nedenler:
1. MDB dosyası bozuk veya şifreli olabilir
2. Access Driver düzgün kurulmamış olabilir
3. Dosya başka bir program tarafından kullanılıyor olabilir
"""
                print_and_log(error_msg, f)
                return False
                
        except ImportError:
            error_msg = """
❌ HATA: pyodbc modülü bulunamadı!

Kurulum için şu komutu çalıştırın:
    pip install -r requirements.txt

veya

    pip install pyodbc pandas
"""
            print_and_log(error_msg, f)
            return False

def main():
    """Ana program"""
    print("=" * 50)
    print("  MDB DOSYASI ANALİZ PROGRAMI")
    print("=" * 50)
    print()
    
    # MDB dosyasını belirle (komut satırı argümanı veya varsayılan)
    if len(sys.argv) > 1:
        mdb_file = sys.argv[1]
    else:
        mdb_file = "04.08.2025 İTİBAREN.mdb"
    
    # Dosya mevcut mu kontrol et
    if not os.path.exists(mdb_file):
        print(f"❌ HATA: '{mdb_file}' dosyası bulunamadı!")
        print(f"📍 Aranan konum: {os.path.abspath(mdb_file)}")
        print()
        print("Kullanım:")
        print(f"  python mdb_analiz.py [dosya_adı.mdb]")
        print()
        print("Örnek:")
        print(f"  python mdb_analiz.py \"04.08.2025 İTİBAREN.mdb\"")
        sys.exit(1)
    
    print(f"✅ MDB dosyası bulundu: {mdb_file}")
    print()
    
    # Analizi başlat
    success = analyze_mdb_file(mdb_file)
    
    if success:
        print()
        print("✨ İşlem başarıyla tamamlandı!")
        print(f"📄 Detaylı rapor için RAPOR.txt dosyasını kontrol edin.")
    else:
        print()
        print("⚠️  İşlem tamamlanamadı. Lütfen yukarıdaki hataları kontrol edin.")
        sys.exit(1)

if __name__ == "__main__":
    main()
