#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MDB Dosya Analiz Programı - GUI Uygulaması
Modern ve kullanıcı dostu pencereli uygulama
"""

import os
import sys
import time
import threading
from datetime import datetime
from pathlib import Path
import traceback

# GUI imports
try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox, scrolledtext
    from tkinter.font import Font
except ImportError:
    print("HATA: tkinter modülü bulunamadı!")
    print("Linux'ta şu komutu çalıştırın: sudo apt-get install python3-tk")
    sys.exit(1)

# Database imports
try:
    import pyodbc
except ImportError:
    pyodbc = None

try:
    import pandas as pd
except ImportError:
    pd = None

try:
    from ttkthemes import ThemedTk
    THEMED_TK_AVAILABLE = True
except ImportError:
    THEMED_TK_AVAILABLE = False

try:
    import openpyxl
    EXCEL_AVAILABLE = True
except ImportError:
    EXCEL_AVAILABLE = False


# Renk Paleti
class Colors:
    BG_COLOR = "#f0f0f0"
    BG_DARK = "#2b2b2b"
    BUTTON_COLOR = "#4CAF50"
    BUTTON_HOVER = "#45a049"
    BUTTON_DANGER = "#f44336"
    TEXT_BG = "#ffffff"
    TEXT_BG_DARK = "#1e1e1e"
    TEXT_FG = "#000000"
    TEXT_FG_DARK = "#e0e0e0"
    TITLE_COLOR = "#2196F3"
    STATUS_BG = "#e3f2fd"
    STATUS_BG_DARK = "#1a237e"
    HEADER_COLOR = "#1976D2"
    SUCCESS_COLOR = "#4CAF50"
    ERROR_COLOR = "#f44336"
    WARNING_COLOR = "#ff9800"


class MDBAnalyzerGUI:
    """MDB Dosya Analiz GUI Uygulaması"""
    
    # Window configuration constants
    WINDOW_WIDTH = 950
    WINDOW_HEIGHT = 750
    MIN_WIDTH = 800
    MIN_HEIGHT = 600
    
    def __init__(self, root):
        self.root = root
        self.setup_window()
        
        # Variables
        self.selected_file = tk.StringVar()
        self.status_text = tk.StringVar(value="Hazır")
        self.is_analyzing = False
        self.analysis_results = ""
        self.dark_mode = False
        
        # Checkboxes for table selection
        self.table_vars = {}
        self.all_tables = []
        
        # Create UI
        self.create_widgets()
        self.apply_theme()
        
    def setup_window(self):
        """Pencere ayarlarını yapılandır"""
        self.root.title("🗂️ MDB Dosya Analiz Programı")
        self.root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        self.root.minsize(self.MIN_WIDTH, self.MIN_HEIGHT)
        
        # Center window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_widgets(self):
        """Tüm GUI bileşenlerini oluştur"""
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Header
        self.create_header(main_frame)
        
        # File selection section
        self.create_file_section(main_frame)
        
        # Action buttons section
        self.create_buttons_section(main_frame)
        
        # Results section
        self.create_results_section(main_frame)
        
        # Status bar
        self.create_status_bar(main_frame)
        
    def create_header(self, parent):
        """Başlık bölümünü oluştur"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        header_frame.columnconfigure(0, weight=1)
        
        title_label = ttk.Label(
            header_frame,
            text="🗂️ MDB Dosya Analiz Programı",
            font=('Segoe UI', 18, 'bold')
        )
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        # Theme toggle button
        theme_btn = ttk.Button(
            header_frame,
            text="🌙",
            width=3,
            command=self.toggle_theme
        )
        theme_btn.grid(row=0, column=1, padx=5)
        
    def create_file_section(self, parent):
        """Dosya seçim bölümünü oluştur"""
        file_frame = ttk.LabelFrame(parent, text="📁 Dosya Seçimi", padding="10")
        file_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        select_btn = ttk.Button(
            file_frame,
            text="📁 MDB Dosyası Seç",
            command=self.select_file
        )
        select_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.file_label = ttk.Label(
            file_frame,
            textvariable=self.selected_file,
            relief=tk.SUNKEN,
            padding=5
        )
        self.file_label.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
    def create_buttons_section(self, parent):
        """Aksiyon butonları bölümünü oluştur"""
        btn_frame = ttk.Frame(parent)
        btn_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Analyze button
        self.analyze_btn = ttk.Button(
            btn_frame,
            text="🔍 Analiz Et",
            command=self.start_analysis,
            style="Accent.TButton"
        )
        self.analyze_btn.pack(side=tk.LEFT, padx=5)
        
        # Save report button
        self.save_btn = ttk.Button(
            btn_frame,
            text="📄 Rapor Kaydet",
            command=self.save_report,
            state=tk.DISABLED
        )
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        # Export options menu
        export_menu = ttk.Menubutton(btn_frame, text="💾 Dışa Aktar")
        export_menu.pack(side=tk.LEFT, padx=5)
        
        menu = tk.Menu(export_menu, tearoff=0)
        menu.add_command(label="TXT Olarak Kaydet", command=lambda: self.export_report('txt'))
        menu.add_command(label="CSV Olarak Kaydet", command=lambda: self.export_report('csv'))
        if EXCEL_AVAILABLE:
            menu.add_command(label="Excel Olarak Kaydet", command=lambda: self.export_report('xlsx'))
        export_menu['menu'] = menu
        
        # Clear button
        self.clear_btn = ttk.Button(
            btn_frame,
            text="🗑️ Temizle",
            command=self.clear_results
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            btn_frame,
            mode='indeterminate',
            length=200
        )
        self.progress.pack(side=tk.RIGHT, padx=5)
        
    def create_results_section(self, parent):
        """Sonuç gösterim bölümünü oluştur"""
        results_frame = ttk.LabelFrame(parent, text="📊 Analiz Sonuçları", padding="10")
        results_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Text widget with scrollbar
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            wrap=tk.WORD,
            font=('Courier New', 10),
            height=20
        )
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure text tags for colors
        self.results_text.tag_configure("header", foreground=Colors.HEADER_COLOR, font=('Courier New', 11, 'bold'))
        self.results_text.tag_configure("success", foreground=Colors.SUCCESS_COLOR, font=('Courier New', 10, 'bold'))
        self.results_text.tag_configure("error", foreground=Colors.ERROR_COLOR, font=('Courier New', 10, 'bold'))
        self.results_text.tag_configure("warning", foreground=Colors.WARNING_COLOR)
        self.results_text.tag_configure("info", foreground=Colors.TITLE_COLOR)
        
    def create_status_bar(self, parent):
        """Durum çubuğunu oluştur"""
        status_frame = ttk.Frame(parent, relief=tk.SUNKEN)
        status_frame.grid(row=4, column=0, sticky=(tk.W, tk.E))
        status_frame.columnconfigure(0, weight=1)
        
        self.status_label = ttk.Label(
            status_frame,
            textvariable=self.status_text,
            padding=5
        )
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.time_label = ttk.Label(status_frame, text="", padding=5)
        self.time_label.pack(side=tk.RIGHT)
        
    def select_file(self):
        """Dosya seçim dialogunu aç"""
        filetypes = (
            ('Microsoft Access Database', '*.mdb'),
            ('Access Database', '*.accdb'),
            ('Tüm Dosyalar', '*.*')
        )
        
        filename = filedialog.askopenfilename(
            title='MDB Dosyası Seç',
            filetypes=filetypes
        )
        
        if filename:
            self.selected_file.set(filename)
            self.update_status(f"Dosya seçildi: {os.path.basename(filename)}")
            
    def start_analysis(self):
        """Analizi başlat (thread ile)"""
        if not self.selected_file.get():
            messagebox.showwarning(
                "Uyarı",
                "Lütfen önce bir MDB dosyası seçin!"
            )
            return
        
        if self.is_analyzing:
            messagebox.showinfo("Bilgi", "Analiz zaten devam ediyor...")
            return
        
        # Check if file exists
        if not os.path.exists(self.selected_file.get()):
            messagebox.showerror(
                "Hata",
                f"Dosya bulunamadı:\n{self.selected_file.get()}"
            )
            return
        
        # Check if pyodbc is available
        if pyodbc is None:
            messagebox.showerror(
                "Hata",
                "pyodbc modülü bulunamadı!\n\n"
                "Lütfen şu komutu çalıştırın:\n"
                "pip install pyodbc\n\n"
                "Not: Windows'ta Microsoft Access Database Engine driver'ı gereklidir."
            )
            return
        
        # Start analysis in thread
        self.is_analyzing = True
        self.analyze_btn.config(state=tk.DISABLED)
        self.progress.start()
        
        thread = threading.Thread(target=self.analyze_file, daemon=True)
        thread.start()
        
    def analyze_file(self):
        """MDB dosyasını analiz et"""
        start_time = time.time()
        
        try:
            self.update_status("Analiz başlatılıyor...")
            
            # Clear previous results
            self.root.after(0, self.results_text.delete, 1.0, tk.END)
            
            filepath = self.selected_file.get()
            
            # Show initial info
            self.append_result("=" * 60 + "\n", "header")
            self.append_result("🗂️  MDB DOSYA ANALİZ RAPORU\n", "header")
            self.append_result("=" * 60 + "\n\n", "header")
            
            self.append_result(f"📄 Dosya: {os.path.basename(filepath)}\n")
            self.append_result(f"📁 Konum: {os.path.dirname(filepath)}\n")
            self.append_result(f"📊 Boyut: {os.path.getsize(filepath) / 1024 / 1024:.2f} MB\n")
            self.append_result(f"🕐 Analiz Zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Try to connect
            self.update_status("Veritabanına bağlanılıyor...")
            
            try:
                # Try different connection strings
                conn_str = self.get_connection_string(filepath)
                conn = pyodbc.connect(conn_str)
                cursor = conn.cursor()
                
                self.append_result("✅ Veritabanı bağlantısı başarılı!\n\n", "success")
                
                # Get all tables
                self.update_status("Tablolar taranıyor...")
                tables = []
                for row in cursor.tables(tableType='TABLE'):
                    if not row.table_name.startswith('MSys'):
                        tables.append(row.table_name)
                
                self.all_tables = tables
                
                self.append_result("=" * 60 + "\n", "info")
                self.append_result(f"📊 TOPLAM {len(tables)} TABLO BULUNDU\n", "info")
                self.append_result("=" * 60 + "\n\n", "info")
                
                # Analyze each table
                for i, table in enumerate(tables, 1):
                    self.update_status(f"Tablo analiz ediliyor: {table} ({i}/{len(tables)})")
                    
                    self.append_result("━" * 60 + "\n", "header")
                    self.append_result(f"📋 TABLO {i}: {table}\n", "header")
                    self.append_result("━" * 60 + "\n\n", "header")
                    
                    try:
                        # Get column info
                        columns = []
                        for col in cursor.columns(table=table):
                            columns.append({
                                'name': col.column_name,
                                'type': col.type_name,
                                'size': col.column_size
                            })
                        
                        self.append_result(f"   📌 Sütun Sayısı: {len(columns)}\n")
                        self.append_result("   📌 Sütunlar:\n")
                        for col in columns:
                            self.append_result(f"      • {col['name']}: {col['type']}", "info")
                            if col['size']:
                                self.append_result(f" ({col['size']})\n")
                            else:
                                self.append_result("\n")
                        
                        # Get row count
                        try:
                            cursor.execute(f"SELECT COUNT(*) FROM [{table}]")
                            count = cursor.fetchone()[0]
                            self.append_result(f"\n   📊 Kayıt Sayısı: {count}\n", "success")
                        except Exception as e:
                            self.append_result(f"\n   ⚠️  Kayıt sayısı alınamadı: {str(e)}\n", "warning")
                        
                        # Get sample data (first 5 rows)
                        try:
                            cursor.execute(f"SELECT TOP 5 * FROM [{table}]")
                            rows = cursor.fetchall()
                            
                            if rows:
                                self.append_result("\n   📝 İlk 5 Örnek Veri:\n")
                                for idx, row in enumerate(rows, 1):
                                    self.append_result(f"      {idx}. ", "info")
                                    row_data = []
                                    for col_idx, value in enumerate(row):
                                        col_name = columns[col_idx]['name'] if col_idx < len(columns) else f"Col{col_idx}"
                                        if value is not None:
                                            val_str = str(value)
                                            if len(val_str) > 50:
                                                val_str = val_str[:50] + "..."
                                            row_data.append(f"{col_name}={val_str}")
                                    self.append_result(", ".join(row_data) + "\n")
                            else:
                                self.append_result("\n   ℹ️  Tabloda veri yok\n", "info")
                        except Exception as e:
                            self.append_result(f"\n   ⚠️  Örnek veri alınamadı: {str(e)}\n", "warning")
                        
                        self.append_result("\n")
                        
                    except Exception as e:
                        self.append_result(f"   ❌ Tablo analiz hatası: {str(e)}\n\n", "error")
                
                # Try to get queries/views
                self.update_status("Sorgular taranıyor...")
                try:
                    queries = []
                    for row in cursor.tables(tableType='VIEW'):
                        queries.append(row.table_name)
                    
                    if queries:
                        self.append_result("=" * 60 + "\n", "info")
                        self.append_result(f"🔍 SORGULAR VE GÖRÜNÜMLERİ ({len(queries)})\n", "info")
                        self.append_result("=" * 60 + "\n\n", "info")
                        for query in queries:
                            self.append_result(f"   • {query}\n")
                        self.append_result("\n")
                except Exception as e:
                    self.append_result(f"⚠️  Sorgu listesi alınamadı: {str(e)}\n\n", "warning")
                
                # Close connection
                cursor.close()
                conn.close()
                
                # Summary
                elapsed = time.time() - start_time
                self.append_result("=" * 60 + "\n", "success")
                self.append_result("✅ ANALİZ TAMAMLANDI\n", "success")
                self.append_result("=" * 60 + "\n", "success")
                self.append_result(f"⏱️  Toplam Süre: {elapsed:.2f} saniye\n", "success")
                self.append_result(f"📊 Analiz Edilen Tablo: {len(tables)}\n", "success")
                
                # Save results to variable
                self.analysis_results = self.results_text.get(1.0, tk.END)
                
                self.root.after(0, self.save_btn.config, {'state': tk.NORMAL})
                self.update_status(f"✅ İşlem tamamlandı ({elapsed:.2f} saniye)")
                self.root.after(0, self.time_label.config, {'text': f"⏱️ {elapsed:.2f}s"})
                
            except pyodbc.Error as e:
                error_msg = str(e)
                self.append_result("❌ VERİTABANI BAĞLANTI HATASI\n", "error")
                self.append_result("=" * 60 + "\n\n", "error")
                
                if "IM002" in error_msg or "Data source name not found" in error_msg:
                    self.append_result(
                        "Microsoft Access Database Engine driver bulunamadı!\n\n",
                        "error"
                    )
                    self.append_result(
                        "Çözüm:\n"
                        "1. Microsoft Access Database Engine 2016 Redistributable indirin:\n"
                        "   https://www.microsoft.com/en-us/download/details.aspx?id=54920\n\n"
                        "2. Sisteminize uygun sürümü yükleyin:\n"
                        "   - 64-bit Python için: AccessDatabaseEngine_X64.exe\n"
                        "   - 32-bit Python için: AccessDatabaseEngine.exe\n\n"
                    )
                else:
                    self.append_result(f"Hata Detayı: {error_msg}\n\n", "error")
                
                self.update_status("❌ Bağlantı hatası")
                
        except Exception as e:
            self.append_result(f"❌ BEKLENMEYEN HATA\n", "error")
            self.append_result("=" * 60 + "\n\n", "error")
            self.append_result(f"{str(e)}\n\n", "error")
            self.append_result(f"Detay:\n{traceback.format_exc()}\n", "warning")
            self.update_status("❌ Hata oluştu")
            
        finally:
            self.is_analyzing = False
            self.root.after(0, self.analyze_btn.config, {'state': tk.NORMAL})
            self.root.after(0, self.progress.stop)
    
    def get_connection_string(self, filepath):
        """Get appropriate connection string for the MDB file"""
        # Try different drivers
        drivers = [
            'Microsoft Access Driver (*.mdb, *.accdb)',
            'Microsoft Access Driver (*.mdb)',
            'Driver do Microsoft Access (*.mdb)',
        ]
        
        for driver in drivers:
            try:
                # Check if driver is available
                if driver in [d for d in pyodbc.drivers()]:
                    return f'DRIVER={{{driver}}};DBQ={filepath};'
            except:
                pass
        
        # Default connection string
        return f'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={filepath};'
    
    def append_result(self, text, tag=None):
        """Sonuç metnine ekle"""
        def _append():
            if tag:
                self.results_text.insert(tk.END, text, tag)
            else:
                self.results_text.insert(tk.END, text)
            self.results_text.see(tk.END)
        
        self.root.after(0, _append)
    
    def update_status(self, text):
        """Durum çubuğunu güncelle"""
        self.root.after(0, self.status_text.set, text)
    
    def save_report(self):
        """Raporu kaydet"""
        if not self.analysis_results:
            messagebox.showwarning("Uyarı", "Kaydedilecek rapor yok!")
            return
        
        filetypes = (
            ('Text files', '*.txt'),
            ('All files', '*.*')
        )
        
        filename = filedialog.asksaveasfilename(
            title='Raporu Kaydet',
            defaultextension='.txt',
            filetypes=filetypes,
            initialfile=f"mdb_analiz_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.analysis_results)
                messagebox.showinfo(
                    "Başarılı",
                    f"Rapor kaydedildi:\n{filename}"
                )
                self.update_status(f"✅ Rapor kaydedildi: {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror(
                    "Hata",
                    f"Rapor kaydedilemedi:\n{str(e)}"
                )
    
    def export_report(self, format_type):
        """Export report in different formats"""
        if not self.analysis_results:
            messagebox.showwarning("Uyarı", "Dışa aktarılacak veri yok!")
            return
        
        if format_type == 'txt':
            self.save_report()
        elif format_type == 'csv':
            self.export_csv()
        elif format_type == 'xlsx':
            self.export_excel()
    
    def export_csv(self):
        """Export to CSV format"""
        if not pd:
            messagebox.showerror("Hata", "pandas modülü gerekli!")
            return
        
        messagebox.showinfo("Bilgi", "CSV export özelliği yakında eklenecek!")
    
    def export_excel(self):
        """Export to Excel format"""
        if not EXCEL_AVAILABLE:
            messagebox.showerror("Hata", "openpyxl modülü gerekli!")
            return
        
        messagebox.showinfo("Bilgi", "Excel export özelliği yakında eklenecek!")
    
    def clear_results(self):
        """Sonuçları temizle"""
        self.results_text.delete(1.0, tk.END)
        self.analysis_results = ""
        self.save_btn.config(state=tk.DISABLED)
        self.status_text.set("Hazır")
        self.time_label.config(text="")
        self.update_status("🗑️ Sonuçlar temizlendi")
    
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        self.dark_mode = not self.dark_mode
        self.apply_theme()
    
    def apply_theme(self):
        """Apply current theme colors"""
        if self.dark_mode:
            bg = Colors.BG_DARK
            fg = Colors.TEXT_FG_DARK
            text_bg = Colors.TEXT_BG_DARK
            status_bg = Colors.STATUS_BG_DARK
        else:
            bg = Colors.BG_COLOR
            fg = Colors.TEXT_FG
            text_bg = Colors.TEXT_BG
            status_bg = Colors.STATUS_BG
        
        # Apply to text widget
        try:
            self.results_text.config(bg=text_bg, fg=fg, insertbackground=fg)
        except:
            pass


def check_dependencies():
    """Check and report missing dependencies"""
    missing = []
    
    if pyodbc is None:
        missing.append("pyodbc")
    if pd is None:
        missing.append("pandas")
    if not EXCEL_AVAILABLE:
        missing.append("openpyxl")
    
    if missing:
        msg = "Eksik modüller:\n\n"
        msg += "\n".join(f"  • {m}" for m in missing)
        msg += "\n\nKurmak için:\n"
        msg += f"pip install {' '.join(missing)}"
        
        print("=" * 60)
        print("UYARI: Bazı modüller eksik!")
        print("=" * 60)
        print(msg)
        print("=" * 60)
        print()


def main():
    """Ana program"""
    print("=" * 60)
    print("🗂️  MDB Dosya Analiz Programı")
    print("=" * 60)
    print()
    
    # Check dependencies
    check_dependencies()
    
    # Create GUI
    try:
        if THEMED_TK_AVAILABLE:
            root = ThemedTk(theme="arc")
        else:
            root = tk.Tk()
        
        app = MDBAnalyzerGUI(root)
        
        print("✅ GUI başlatıldı!")
        print("Pencereyi kapatmak için X'e tıklayın veya ESC tuşuna basın.")
        print()
        
        # Bind ESC to quit
        root.bind('<Escape>', lambda e: root.quit())
        
        root.mainloop()
        
    except Exception as e:
        print(f"❌ HATA: {str(e)}")
        print()
        print(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
