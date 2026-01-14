#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MDB Dosya Analiz Programı
Microsoft Access (.mdb/.accdb) dosyalarını analiz eden pencereli masaüstü uygulaması.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pyodbc
import pandas as pd
import threading
import os
import sys


class MDBAnalyzer:
    """MDB dosya analiz sınıfı"""
    
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.tables = []
        self.table_data = {}
    
    def connect(self, db_path):
        """MDB dosyasına bağlan"""
        try:
            # Access driver'larını dene
            drivers = [
                'Microsoft Access Driver (*.mdb, *.accdb)',
                'Driver do Microsoft Access (*.mdb)',
                'Microsoft Access Driver (*.mdb)',
            ]
            
            connection_string = None
            for driver in drivers:
                try:
                    connection_string = f'Driver={{{driver}}};DBQ={db_path};'
                    self.connection = pyodbc.connect(connection_string)
                    self.cursor = self.connection.cursor()
                    return True
                except pyodbc.Error:
                    continue
            
            # Hiçbir driver çalışmadıysa
            raise Exception("Access driver bulunamadı!")
            
        except Exception as e:
            raise Exception(f"Veritabanına bağlanılamadı: {str(e)}")
    
    def get_tables(self):
        """Tüm tabloları listele"""
        try:
            self.tables = []
            for table_info in self.cursor.tables(tableType='TABLE'):
                table_name = table_info.table_name
                # Sistem tablolarını filtrele
                if not table_name.startswith('MSys') and not table_name.startswith('~'):
                    self.tables.append(table_name)
            return self.tables
        except Exception as e:
            raise Exception(f"Tablolar alınamadı: {str(e)}")
    
    def analyze_table(self, table_name):
        """Belirtilen tabloyu analiz et"""
        try:
            # Sütun bilgileri
            columns = []
            for column in self.cursor.columns(table=table_name):
                columns.append({
                    'name': column.column_name,
                    'type': column.type_name,
                    'size': column.column_size
                })
            
            # Kayıt sayısı
            self.cursor.execute(f'SELECT COUNT(*) FROM [{table_name}]')
            row_count = self.cursor.fetchone()[0]
            
            # İlk 5 satır
            self.cursor.execute(f'SELECT TOP 5 * FROM [{table_name}]')
            sample_rows = self.cursor.fetchall()
            sample_data = [list(row) for row in sample_rows]
            
            return {
                'columns': columns,
                'row_count': row_count,
                'sample_data': sample_data
            }
        except Exception as e:
            raise Exception(f"Tablo analiz edilemedi: {str(e)}")
    
    def export_to_excel(self, output_path, table_name=None):
        """Excel'e aktar"""
        try:
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                if table_name:
                    # Tek tablo
                    query = f'SELECT * FROM [{table_name}]'
                    df = pd.read_sql(query, self.connection)
                    df.to_excel(writer, sheet_name=table_name[:31], index=False)
                else:
                    # Tüm tablolar
                    for table in self.tables:
                        try:
                            query = f'SELECT * FROM [{table}]'
                            df = pd.read_sql(query, self.connection)
                            # Excel sheet ismi max 31 karakter
                            sheet_name = table[:31]
                            df.to_excel(writer, sheet_name=sheet_name, index=False)
                        except:
                            continue
            return True
        except Exception as e:
            raise Exception(f"Excel'e aktarılamadı: {str(e)}")
    
    def close(self):
        """Bağlantıyı kapat"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()


class MDBAnalyzerGUI:
    """MDB Analiz Programı GUI"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("📊 MDB Dosya Analiz Programı")
        self.root.geometry("1000x700")
        
        # Pencereyi ortala
        self.center_window()
        
        # Değişkenler
        self.db_path = tk.StringVar()
        self.analyzer = None
        self.current_table_data = {}
        
        # GUI oluştur
        self.create_widgets()
        
        # Durum
        self.update_status("Hazır")
    
    def center_window(self):
        """Pencereyi ekranın ortasına yerleştir"""
        self.root.update_idletasks()
        width = 1000
        height = 700
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """GUI bileşenlerini oluştur"""
        
        # Ana konteyner
        main_container = ttk.Frame(self.root, padding="10")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Üst kısım
        self.create_header(main_container)
        
        # Orta kısım (Ana ekran)
        self.create_main_area(main_container)
        
        # Alt kısım
        self.create_footer(main_container)
        
        # Grid ağırlıkları
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(1, weight=1)
    
    def create_header(self, parent):
        """Üst kısım - Başlık ve butonlar"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        header_frame.columnconfigure(1, weight=1)
        
        # Başlık
        title_label = ttk.Label(
            header_frame,
            text="📊 MDB Dosya Analiz Programı",
            font=('Arial', 18, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Dosya yolu
        ttk.Label(header_frame, text="Dosya:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5))
        path_entry = ttk.Entry(header_frame, textvariable=self.db_path, state='readonly')
        path_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        
        # Dosya seç butonu
        select_btn = tk.Button(
            header_frame,
            text="📁 Dosya Seç",
            command=self.select_file,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=15,
            pady=5,
            cursor='hand2'
        )
        select_btn.grid(row=1, column=2, padx=(0, 5))
        
        # Analiz et butonu
        self.analyze_btn = tk.Button(
            header_frame,
            text="🔍 Analiz Et",
            command=self.analyze_database,
            bg='#2196F3',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=15,
            pady=5,
            cursor='hand2',
            state='disabled'
        )
        self.analyze_btn.grid(row=1, column=3)
    
    def create_main_area(self, parent):
        """Orta kısım - Ana ekran"""
        main_frame = ttk.Frame(parent)
        main_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=3)
        main_frame.rowconfigure(0, weight=1)
        
        # Sol panel - Tablo listesi
        self.create_table_list(main_frame)
        
        # Sağ panel - Tablo detayları
        self.create_table_details(main_frame)
    
    def create_table_list(self, parent):
        """Sol panel - Tablo listesi"""
        left_frame = ttk.LabelFrame(parent, text="📋 Tablolar", padding="5")
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(0, weight=1)
        
        # Listbox ve scrollbar
        scrollbar = ttk.Scrollbar(left_frame)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.table_listbox = tk.Listbox(
            left_frame,
            yscrollcommand=scrollbar.set,
            font=('Arial', 10),
            selectmode=tk.SINGLE
        )
        self.table_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.config(command=self.table_listbox.yview)
        
        # Tablo seçim eventi
        self.table_listbox.bind('<<ListboxSelect>>', self.on_table_select)
    
    def create_table_details(self, parent):
        """Sağ panel - Tablo detayları"""
        right_frame = ttk.LabelFrame(parent, text="📊 Tablo Detayları", padding="5")
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)
        
        # Bilgi çerçevesi
        info_frame = ttk.Frame(right_frame)
        info_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.info_label = ttk.Label(
            info_frame,
            text="Lütfen sol panelden bir tablo seçin",
            font=('Arial', 10)
        )
        self.info_label.grid(row=0, column=0, sticky=tk.W)
        
        # Treeview için container
        tree_frame = ttk.Frame(right_frame)
        tree_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        # Scrollbarlar
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        # Treeview
        self.details_tree = ttk.Treeview(
            tree_frame,
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )
        
        vsb.config(command=self.details_tree.yview)
        hsb.config(command=self.details_tree.xview)
        
        self.details_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        hsb.grid(row=1, column=0, sticky=(tk.W, tk.E))
    
    def create_footer(self, parent):
        """Alt kısım - Butonlar ve durum çubuğu"""
        footer_frame = ttk.Frame(parent)
        footer_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        footer_frame.columnconfigure(1, weight=1)
        
        # Butonlar
        button_frame = ttk.Frame(footer_frame)
        button_frame.grid(row=0, column=0, sticky=tk.W)
        
        self.save_report_btn = tk.Button(
            button_frame,
            text="💾 Rapor Kaydet (.txt)",
            command=self.save_report,
            bg='#FF9800',
            fg='white',
            font=('Arial', 9, 'bold'),
            padx=10,
            pady=3,
            cursor='hand2',
            state='disabled'
        )
        self.save_report_btn.grid(row=0, column=0, padx=(0, 5))
        
        self.export_excel_btn = tk.Button(
            button_frame,
            text="📊 Excel'e Aktar (.xlsx)",
            command=self.export_to_excel,
            bg='#009688',
            fg='white',
            font=('Arial', 9, 'bold'),
            padx=10,
            pady=3,
            cursor='hand2',
            state='disabled'
        )
        self.export_excel_btn.grid(row=0, column=1)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            footer_frame,
            mode='indeterminate',
            length=200
        )
        self.progress.grid(row=0, column=1, padx=10)
        
        # Durum çubuğu
        self.status_label = ttk.Label(
            footer_frame,
            text="Hazır",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_label.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
    
    def select_file(self):
        """Dosya seç"""
        filename = filedialog.askopenfilename(
            title="MDB Dosyası Seçin",
            filetypes=[
                ("Access Veritabanı", "*.mdb *.accdb"),
                ("Tüm Dosyalar", "*.*")
            ]
        )
        
        if filename:
            self.db_path.set(filename)
            self.analyze_btn.config(state='normal')
            self.update_status(f"Dosya seçildi: {os.path.basename(filename)}")
    
    def analyze_database(self):
        """Veritabanını analiz et"""
        if not self.db_path.get():
            messagebox.showwarning("Uyarı", "Lütfen önce bir dosya seçin!")
            return
        
        # Thread'de çalıştır
        thread = threading.Thread(target=self._analyze_worker)
        thread.daemon = True
        thread.start()
    
    def _analyze_worker(self):
        """Analiz worker thread"""
        try:
            # Progress başlat
            self.root.after(0, self.progress.start)
            self.root.after(0, lambda: self.update_status("Analiz ediliyor..."))
            self.root.after(0, lambda: self.analyze_btn.config(state='disabled'))
            
            # Analyzer oluştur
            self.analyzer = MDBAnalyzer()
            
            # Bağlan
            self.root.after(0, lambda: self.update_status("Veritabanına bağlanılıyor..."))
            self.analyzer.connect(self.db_path.get())
            
            # Tabloları al
            self.root.after(0, lambda: self.update_status("Tablolar alınıyor..."))
            tables = self.analyzer.get_tables()
            
            if not tables:
                self.root.after(0, lambda: messagebox.showinfo(
                    "Bilgi",
                    "Veritabanında kullanıcı tablosu bulunamadı!"
                ))
                return
            
            # Listbox'ı güncelle
            self.root.after(0, self._update_table_list, tables)
            
            # Her tabloyu analiz et
            for i, table in enumerate(tables):
                self.root.after(0, lambda t=table: self.update_status(f"Analiz ediliyor: {t}..."))
                table_info = self.analyzer.analyze_table(table)
                self.current_table_data[table] = table_info
            
            # Başarılı
            self.root.after(0, lambda: self.update_status(
                f"Analiz tamamlandı! {len(tables)} tablo bulundu."
            ))
            self.root.after(0, lambda: messagebox.showinfo(
                "Başarılı",
                f"Analiz tamamlandı!\n\n{len(tables)} tablo bulundu."
            ))
            
            # Butonları aktif et
            self.root.after(0, lambda: self.save_report_btn.config(state='normal'))
            self.root.after(0, lambda: self.export_excel_btn.config(state='normal'))
            
        except Exception as e:
            error_msg = str(e)
            
            # Driver hatası özel mesaj
            if "driver" in error_msg.lower():
                error_msg = (
                    "Access Driver bulunamadı!\n\n"
                    "Microsoft Access Database Engine yüklemek için:\n"
                    "https://www.microsoft.com/en-us/download/details.aspx?id=54920\n\n"
                    "Not: 64-bit Python kullanıyorsanız 64-bit driver,\n"
                    "32-bit Python kullanıyorsanız 32-bit driver yükleyin."
                )
            
            self.root.after(0, lambda: messagebox.showerror("Hata", error_msg))
            self.root.after(0, lambda: self.update_status(f"Hata: {str(e)}"))
        
        finally:
            # Progress durdur
            self.root.after(0, self.progress.stop)
            self.root.after(0, lambda: self.analyze_btn.config(state='normal'))
    
    def _update_table_list(self, tables):
        """Tablo listesini güncelle"""
        self.table_listbox.delete(0, tk.END)
        for table in tables:
            self.table_listbox.insert(tk.END, table)
    
    def on_table_select(self, event):
        """Tablo seçildiğinde"""
        selection = self.table_listbox.curselection()
        if not selection:
            return
        
        table_name = self.table_listbox.get(selection[0])
        if table_name not in self.current_table_data:
            return
        
        self.display_table_details(table_name)
    
    def display_table_details(self, table_name):
        """Tablo detaylarını göster"""
        table_info = self.current_table_data[table_name]
        
        # Bilgi etiketini güncelle
        info_text = (
            f"Tablo: {table_name}  |  "
            f"Kayıt Sayısı: {table_info['row_count']}  |  "
            f"Sütun Sayısı: {len(table_info['columns'])}"
        )
        self.info_label.config(text=info_text)
        
        # Treeview'i temizle
        self.details_tree.delete(*self.details_tree.get_children())
        
        # Sütunları ayarla
        columns = table_info['columns']
        column_ids = [f"col_{i}" for i in range(len(columns))]
        self.details_tree['columns'] = column_ids
        
        # Sütun başlıklarını ayarla
        self.details_tree.heading('#0', text='#')
        self.details_tree.column('#0', width=50, stretch=False)
        
        for i, col in enumerate(columns):
            col_id = column_ids[i]
            col_header = f"{col['name']}\n({col['type']})"
            self.details_tree.heading(col_id, text=col_header)
            self.details_tree.column(col_id, width=150)
        
        # Örnek verileri ekle
        sample_data = table_info['sample_data']
        for idx, row in enumerate(sample_data, 1):
            # None değerlerini düzenle
            row_values = [str(v) if v is not None else '' for v in row]
            self.details_tree.insert('', tk.END, text=str(idx), values=row_values)
        
        self.update_status(f"Tablo gösteriliyor: {table_name}")
    
    def save_report(self):
        """Rapor kaydet"""
        if not self.current_table_data:
            messagebox.showwarning("Uyarı", "Önce veritabanını analiz edin!")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Rapor Kaydet",
            defaultextension=".txt",
            filetypes=[("Metin Dosyası", "*.txt"), ("Tüm Dosyalar", "*.*")]
        )
        
        if not filename:
            return
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("MDB DOSYA ANALİZ RAPORU\n")
                f.write("=" * 80 + "\n\n")
                f.write(f"Dosya: {self.db_path.get()}\n")
                f.write(f"Toplam Tablo Sayısı: {len(self.current_table_data)}\n\n")
                
                for table_name, table_info in self.current_table_data.items():
                    f.write("-" * 80 + "\n")
                    f.write(f"TABLO: {table_name}\n")
                    f.write("-" * 80 + "\n")
                    f.write(f"Kayıt Sayısı: {table_info['row_count']}\n\n")
                    
                    f.write("SÜTUNLAR:\n")
                    for col in table_info['columns']:
                        f.write(f"  - {col['name']} ({col['type']}, {col['size']})\n")
                    
                    f.write("\nÖRNEK VERİLER (İlk 5 satır):\n")
                    col_names = [col['name'] for col in table_info['columns']]
                    f.write("  " + " | ".join(col_names) + "\n")
                    f.write("  " + "-" * 60 + "\n")
                    
                    for row in table_info['sample_data']:
                        row_str = " | ".join([str(v) if v is not None else '' for v in row])
                        f.write("  " + row_str + "\n")
                    
                    f.write("\n")
            
            messagebox.showinfo("Başarılı", f"Rapor kaydedildi:\n{filename}")
            self.update_status(f"Rapor kaydedildi: {os.path.basename(filename)}")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Rapor kaydedilemedi:\n{str(e)}")
    
    def export_to_excel(self):
        """Excel'e aktar"""
        if not self.analyzer:
            messagebox.showwarning("Uyarı", "Önce veritabanını analiz edin!")
            return
        
        # Seçim diyalogu
        choice = messagebox.askyesnocancel(
            "Excel'e Aktar",
            "Tüm tabloları Excel'e aktarmak ister misiniz?\n\n"
            "Evet: Tüm tablolar\n"
            "Hayır: Sadece seçili tablo\n"
            "İptal: İşlemi iptal et"
        )
        
        if choice is None:  # Cancel
            return
        
        # Dosya adı sor
        filename = filedialog.asksaveasfilename(
            title="Excel Dosyası Kaydet",
            defaultextension=".xlsx",
            filetypes=[("Excel Dosyası", "*.xlsx"), ("Tüm Dosyalar", "*.*")]
        )
        
        if not filename:
            return
        
        try:
            self.update_status("Excel'e aktarılıyor...")
            self.progress.start()
            
            if choice:  # Tüm tablolar
                self.analyzer.export_to_excel(filename)
            else:  # Seçili tablo
                selection = self.table_listbox.curselection()
                if not selection:
                    messagebox.showwarning("Uyarı", "Lütfen bir tablo seçin!")
                    return
                table_name = self.table_listbox.get(selection[0])
                self.analyzer.export_to_excel(filename, table_name)
            
            self.progress.stop()
            messagebox.showinfo("Başarılı", f"Excel dosyası oluşturuldu:\n{filename}")
            self.update_status(f"Excel oluşturuldu: {os.path.basename(filename)}")
            
        except Exception as e:
            self.progress.stop()
            messagebox.showerror("Hata", f"Excel oluşturulamadı:\n{str(e)}")
            self.update_status("Hata: Excel oluşturulamadı")
    
    def update_status(self, message):
        """Durum çubuğunu güncelle"""
        self.status_label.config(text=message)


def main():
    """Ana fonksiyon"""
    root = tk.Tk()
    app = MDBAnalyzerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
