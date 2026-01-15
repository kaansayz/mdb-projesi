# -*- coding: utf-8 -*-
"""
Cezaevi Gıda Takip Sistemi - Ana Uygulama
Modern Tkinter GUI
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
import traceback
from pathlib import Path

# Uygulama renkler
COLORS = {
    'success': '#4CAF50',
    'error': '#f44336',
    'warning': '#ff9800',
    'info': '#2196F3',
    'background': '#f0f0f0',
    'sidebar': '#2c3e50',
    'sidebar_hover': '#34495e',
    'content': '#ffffff',
    'text': '#2c3e50',
    'text_light': '#7f8c8d',
    'border': '#bdc3c7'
}


class CezaeviGidaApp:
    """Ana uygulama sınıfı"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cezaevi Gıda Takip Sistemi")
        self.root.geometry("1200x750")
        self.root.minsize(900, 700)
        
        # Veritabanı kontrolü
        self.check_database()
        
        # Ana container
        self.main_container = tk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Modüller
        self.current_module = None
        self.modules = {}
        
        # UI oluştur
        self.create_ui()
        
        # Ana ekranı göster
        self.show_module("ana_ekran")
    
    def check_database(self):
        """Veritabanı kontrolü ve gerekirse import"""
        db_path = Path("data/cezaevi_gida.db")
        
        if not db_path.exists():
            response = messagebox.askyesno(
                "Veritabanı Bulunamadı",
                "Veritabanı dosyası bulunamadı.\n\n"
                "MDB dosyasından veritabanını oluşturmak ister misiniz?\n"
                "(Bu işlem birkaç dakika sürebilir)"
            )
            
            if response:
                self.import_from_mdb()
            else:
                # Boş veritabanı oluştur
                from database import init_database
                init_database()
                messagebox.showinfo(
                    "Veritabanı Oluşturuldu",
                    "Boş bir veritabanı oluşturuldu.\n"
                    "Ayarlar bölümünden cezaevi bilgilerini girebilirsiniz."
                )
    
    def import_from_mdb(self):
        """MDB dosyasından veri aktar"""
        try:
            from mdb_importer import MDBImporter, MDB_FILE
            
            if not os.path.exists(MDB_FILE):
                messagebox.showerror(
                    "Hata",
                    f"MDB dosyası bulunamadı: {MDB_FILE}\n\n"
                    "Lütfen MDB dosyasını proje dizinine koyun."
                )
                # Boş veritabanı oluştur
                from database import init_database
                init_database()
                return
            
            # İlerleme penceresi göster
            progress_window = tk.Toplevel(self.root)
            progress_window.title("Veri Aktarımı")
            progress_window.geometry("400x150")
            progress_window.transient(self.root)
            progress_window.grab_set()
            
            label = tk.Label(
                progress_window,
                text="MDB dosyasından veriler aktarılıyor...\nLütfen bekleyin.",
                font=("Segoe UI", 10),
                pady=20
            )
            label.pack()
            
            progress = ttk.Progressbar(
                progress_window,
                mode='indeterminate'
            )
            progress.pack(pady=10, padx=20, fill=tk.X)
            progress.start(10)
            
            self.root.update()
            
            # Import işlemini başlat
            importer = MDBImporter(MDB_FILE)
            success = importer.import_all()
            
            progress.stop()
            progress_window.destroy()
            
            if success:
                messagebox.showinfo(
                    "Başarılı",
                    "Veriler başarıyla aktarıldı!"
                )
            else:
                messagebox.showerror(
                    "Hata",
                    "Veri aktarımı sırasında bir hata oluştu."
                )
                
        except ImportError as e:
            messagebox.showerror(
                "Hata",
                f"Gerekli modül bulunamadı: {e}\n\n"
                "pip install pyodbc komutunu çalıştırın."
            )
            from database import init_database
            init_database()
        except Exception as e:
            messagebox.showerror(
                "Hata",
                f"Veri aktarımı hatası: {e}"
            )
            from database import init_database
            init_database()
    
    def create_ui(self):
        """UI elementlerini oluştur"""
        # Sol panel (navigasyon)
        self.create_sidebar()
        
        # Sağ panel (içerik)
        self.create_content_area()
    
    def create_sidebar(self):
        """Sol navigasyon paneli"""
        self.sidebar = tk.Frame(
            self.main_container,
            bg=COLORS['sidebar'],
            width=250
        )
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        # Logo/Başlık
        header = tk.Label(
            self.sidebar,
            text="🏛️ Cezaevi\nGıda Takip",
            font=("Segoe UI", 16, "bold"),
            bg=COLORS['sidebar'],
            fg="white",
            pady=20
        )
        header.pack(fill=tk.X)
        
        # Menü butonları
        self.menu_buttons = {}
        
        menu_items = [
            ("ana_ekran", "🏠 Ana Sayfa", "Ana ekran ve özet bilgiler"),
            ("urun_yonetimi", "📦 Ürün Yönetimi", "Ürünleri yönet"),
            ("gunluk_tabela", "📋 Günlük Tabela", "Günlük yemek planlaması"),
            ("stok_takibi", "📊 Stok Takibi", "Stok durumu ve uyarılar"),
            ("raporlar", "📈 Raporlar", "Rapor oluştur ve görüntüle"),
            ("ayarlar", "⚙️ Ayarlar", "Sistem ayarları"),
        ]
        
        for module_name, icon_text, tooltip in menu_items:
            btn = tk.Button(
                self.sidebar,
                text=icon_text,
                font=("Segoe UI", 11),
                bg=COLORS['sidebar'],
                fg="white",
                activebackground=COLORS['sidebar_hover'],
                activeforeground="white",
                bd=0,
                pady=15,
                cursor="hand2",
                anchor="w",
                padx=20,
                command=lambda m=module_name: self.show_module(m)
            )
            btn.pack(fill=tk.X, pady=2)
            self.menu_buttons[module_name] = btn
            
            # Hover efekti
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=COLORS['sidebar_hover']))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=COLORS['sidebar']) if b != self.get_active_button() else None)
        
        # Alt bilgi
        footer = tk.Label(
            self.sidebar,
            text="v1.0.0\n© 2025",
            font=("Segoe UI", 8),
            bg=COLORS['sidebar'],
            fg=COLORS['text_light']
        )
        footer.pack(side=tk.BOTTOM, pady=10)
    
    def get_active_button(self):
        """Aktif buton"""
        if self.current_module and self.current_module in self.menu_buttons:
            return self.menu_buttons[self.current_module]
        return None
    
    def create_content_area(self):
        """İçerik alanı"""
        self.content_frame = tk.Frame(
            self.main_container,
            bg=COLORS['background']
        )
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    def show_module(self, module_name):
        """Modül göster"""
        # Önceki modülü temizle
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Buton renklerini güncelle
        for name, btn in self.menu_buttons.items():
            if name == module_name:
                btn.config(bg=COLORS['sidebar_hover'])
            else:
                btn.config(bg=COLORS['sidebar'])
        
        self.current_module = module_name
        
        # Modülü yükle
        try:
            if module_name == "ana_ekran":
                from gui.ana_ekran import AnaEkran
                module = AnaEkran(self.content_frame)
            elif module_name == "urun_yonetimi":
                from gui.urun_yonetimi import UrunYonetimi
                module = UrunYonetimi(self.content_frame)
            elif module_name == "gunluk_tabela":
                from gui.gunluk_tabela import GunlukTabela
                module = GunlukTabela(self.content_frame)
            elif module_name == "stok_takibi":
                from gui.stok_takibi import StokTakibi
                module = StokTakibi(self.content_frame)
            elif module_name == "raporlar":
                from gui.raporlar import Raporlar
                module = Raporlar(self.content_frame)
            elif module_name == "ayarlar":
                from gui.ayarlar import Ayarlar
                module = Ayarlar(self.content_frame)
            else:
                messagebox.showerror("Hata", f"Modül bulunamadı: {module_name}")
                return
            
            self.modules[module_name] = module
            
        except Exception as e:
            messagebox.showerror(
                "Hata",
                f"Modül yüklenirken hata oluştu:\n{e}"
            )
            traceback.print_exc()
    
    def run(self):
        """Uygulamayı başlat"""
        self.root.mainloop()


def main():
    """Ana fonksiyon"""
    try:
        app = CezaeviGidaApp()
        app.run()
    except Exception as e:
        print(f"❌ Hata: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
