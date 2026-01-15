# -*- coding: utf-8 -*-
"""
Ayarlar Modülü
Cezaevi bilgileri ve sistem ayarları
"""

import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from utils.validasyon import validate_integer, parse_int


class Ayarlar:
    """Ayarlar modülü"""
    
    def __init__(self, parent):
        self.parent = parent
        self.create_ui()
        self.load_settings()
    
    def create_ui(self):
        """UI oluştur"""
        # Ana container
        main_frame = tk.Frame(self.parent, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Başlık
        header = tk.Label(
            main_frame,
            text="⚙️ Ayarlar",
            font=("Segoe UI", 20, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        header.pack(anchor='w', pady=(0, 20))
        
        # Scroll container
        canvas = tk.Canvas(main_frame, bg='#f0f0f0', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f0f0')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Cezaevi bilgileri bölümü
        self.create_prison_info_section(scrollable_frame)
        
        # Personel bilgileri bölümü
        self.create_personnel_section(scrollable_frame)
        
        # Günlük yemek sayıları bölümü
        self.create_meal_counts_section(scrollable_frame)
        
        # Ekmek sayıları bölümü
        self.create_bread_counts_section(scrollable_frame)
        
        # Kaydet butonu
        tk.Button(
            scrollable_frame,
            text="💾 Ayarları Kaydet",
            font=("Segoe UI", 12, "bold"),
            bg='#4CAF50',
            fg='white',
            cursor='hand2',
            relief=tk.FLAT,
            command=self.save_settings,
            padx=40,
            pady=12
        ).pack(pady=20)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_prison_info_section(self, parent):
        """Cezaevi bilgileri bölümü"""
        frame = tk.LabelFrame(
            parent,
            text="Cezaevi Bilgileri",
            font=("Segoe UI", 12, "bold"),
            bg='white',
            fg='#2c3e50',
            relief=tk.FLAT,
            bd=2
        )
        frame.pack(fill=tk.X, pady=(0, 15))
        
        content = tk.Frame(frame, bg='white')
        content.pack(fill=tk.BOTH, padx=15, pady=15)
        
        # Cezaevi adı
        tk.Label(
            content,
            text="Cezaevi Adı:",
            font=("Segoe UI", 10, "bold"),
            bg='white'
        ).grid(row=0, column=0, sticky='w', pady=(0, 5))
        
        self.cezaevi_var = tk.StringVar()
        tk.Entry(
            content,
            textvariable=self.cezaevi_var,
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            bg='#ecf0f1',
            width=50
        ).grid(row=1, column=0, sticky='ew', pady=(0, 15), ipady=5)
        
        content.grid_columnconfigure(0, weight=1)
    
    def create_personnel_section(self, parent):
        """Personel bilgileri bölümü"""
        frame = tk.LabelFrame(
            parent,
            text="Personel Bilgileri",
            font=("Segoe UI", 12, "bold"),
            bg='white',
            fg='#2c3e50',
            relief=tk.FLAT,
            bd=2
        )
        frame.pack(fill=tk.X, pady=(0, 15))
        
        content = tk.Frame(frame, bg='white')
        content.pack(fill=tk.BOTH, padx=15, pady=15)
        
        self.personnel_vars = {}
        
        personnel_fields = [
            ("mudur", "Cezaevi Müdürü:"),
            ("ambar_memuru", "Ambar Memuru:"),
            ("uye1", "Komisyon Üye 1:"),
            ("uye2", "Komisyon Üye 2:"),
            ("uye3", "Komisyon Üye 3:")
        ]
        
        for idx, (field_name, label_text) in enumerate(personnel_fields):
            tk.Label(
                content,
                text=label_text,
                font=("Segoe UI", 10, "bold"),
                bg='white'
            ).grid(row=idx*2, column=0, sticky='w', pady=(0, 5))
            
            var = tk.StringVar()
            self.personnel_vars[field_name] = var
            
            tk.Entry(
                content,
                textvariable=var,
                font=("Segoe UI", 10),
                relief=tk.FLAT,
                bg='#ecf0f1',
                width=50
            ).grid(row=idx*2+1, column=0, sticky='ew', pady=(0, 15), ipady=5)
        
        content.grid_columnconfigure(0, weight=1)
    
    def create_meal_counts_section(self, parent):
        """Günlük yemek sayıları bölümü"""
        frame = tk.LabelFrame(
            parent,
            text="Günlük Öğün Kişi Sayıları",
            font=("Segoe UI", 12, "bold"),
            bg='white',
            fg='#2c3e50',
            relief=tk.FLAT,
            bd=2
        )
        frame.pack(fill=tk.X, pady=(0, 15))
        
        content = tk.Frame(frame, bg='white')
        content.pack(fill=tk.BOTH, padx=15, pady=15)
        
        self.meal_vars = {}
        
        meals = [
            ("sabah_miktar", "Sabah Öğünü Kişi Sayısı:", 0),
            ("ogle_miktar", "Öğle Öğünü Kişi Sayısı:", 1),
            ("aksam_miktar", "Akşam Öğünü Kişi Sayısı:", 2),
            ("toplam_miktar", "Toplam Kişi Sayısı:", 3)
        ]
        
        for field_name, label_text, col in meals[:3]:  # İlk 3'ü grid'e yerleştir
            tk.Label(
                content,
                text=label_text,
                font=("Segoe UI", 10, "bold"),
                bg='white'
            ).grid(row=0, column=col, sticky='w', padx=(0, 20))
            
            var = tk.StringVar()
            self.meal_vars[field_name] = var
            
            entry = tk.Entry(
                content,
                textvariable=var,
                font=("Segoe UI", 10),
                relief=tk.FLAT,
                bg='#ecf0f1',
                width=15
            )
            entry.grid(row=1, column=col, sticky='ew', padx=(0, 20), ipady=5)
            
            # Toplam hesaplama için trace ekle
            var.trace('w', lambda *args: self.calculate_total_meals())
        
        # Toplam - Ayrı satırda
        tk.Label(
            content,
            text="Toplam Kişi Sayısı:",
            font=("Segoe UI", 10, "bold"),
            bg='white'
        ).grid(row=2, column=0, sticky='w', pady=(15, 5))
        
        self.meal_vars["toplam_miktar"] = tk.StringVar()
        tk.Entry(
            content,
            textvariable=self.meal_vars["toplam_miktar"],
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            bg='#ecf0f1',
            width=15,
            state='readonly'
        ).grid(row=3, column=0, sticky='w', pady=(0, 0), ipady=5)
    
    def create_bread_counts_section(self, parent):
        """Ekmek sayıları bölümü"""
        frame = tk.LabelFrame(
            parent,
            text="Günlük Ekmek Sayıları",
            font=("Segoe UI", 12, "bold"),
            bg='white',
            fg='#2c3e50',
            relief=tk.FLAT,
            bd=2
        )
        frame.pack(fill=tk.X, pady=(0, 15))
        
        content = tk.Frame(frame, bg='white')
        content.pack(fill=tk.BOTH, padx=15, pady=15)
        
        self.bread_vars = {}
        
        breads = [
            ("sabah_ekmek", "Sabah Ekmeği:", 0),
            ("ogle_ekmek", "Öğle Ekmeği:", 1),
            ("aksam_ekmek", "Akşam Ekmeği:", 2)
        ]
        
        for field_name, label_text, col in breads:
            tk.Label(
                content,
                text=label_text,
                font=("Segoe UI", 10, "bold"),
                bg='white'
            ).grid(row=0, column=col, sticky='w', padx=(0, 20))
            
            var = tk.StringVar()
            self.bread_vars[field_name] = var
            
            entry = tk.Entry(
                content,
                textvariable=var,
                font=("Segoe UI", 10),
                relief=tk.FLAT,
                bg='#ecf0f1',
                width=15
            )
            entry.grid(row=1, column=col, sticky='ew', padx=(0, 20), ipady=5)
            
            # Toplam hesaplama için trace ekle
            var.trace('w', lambda *args: self.calculate_total_bread())
        
        # Toplam - Ayrı satırda
        tk.Label(
            content,
            text="Toplam Ekmek:",
            font=("Segoe UI", 10, "bold"),
            bg='white'
        ).grid(row=2, column=0, sticky='w', pady=(15, 5))
        
        self.bread_vars["toplam_ekmek"] = tk.StringVar()
        tk.Entry(
            content,
            textvariable=self.bread_vars["toplam_ekmek"],
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            bg='#ecf0f1',
            width=15,
            state='readonly'
        ).grid(row=3, column=0, sticky='w', pady=(0, 0), ipady=5)
    
    def calculate_total_meals(self):
        """Toplam öğün sayısını hesapla"""
        try:
            sabah = parse_int(self.meal_vars["sabah_miktar"].get())
            ogle = parse_int(self.meal_vars["ogle_miktar"].get())
            aksam = parse_int(self.meal_vars["aksam_miktar"].get())
            toplam = sabah + ogle + aksam
            self.meal_vars["toplam_miktar"].set(str(toplam))
        except:
            pass
    
    def calculate_total_bread(self):
        """Toplam ekmek sayısını hesapla"""
        try:
            sabah = parse_int(self.bread_vars["sabah_ekmek"].get())
            ogle = parse_int(self.bread_vars["ogle_ekmek"].get())
            aksam = parse_int(self.bread_vars["aksam_ekmek"].get())
            toplam = sabah + ogle + aksam
            self.bread_vars["toplam_ekmek"].set(str(toplam))
        except:
            pass
    
    def load_settings(self):
        """Ayarları yükle"""
        try:
            with Database() as db:
                info = db.get_cezaevi_bilgileri()
                if info:
                    self.cezaevi_var.set(info.get('cezaevi', ''))
                    
                    # Personel
                    self.personnel_vars['mudur'].set(info.get('mudur', ''))
                    self.personnel_vars['ambar_memuru'].set(info.get('ambar_memuru', ''))
                    self.personnel_vars['uye1'].set(info.get('uye1', ''))
                    self.personnel_vars['uye2'].set(info.get('uye2', ''))
                    self.personnel_vars['uye3'].set(info.get('uye3', ''))
                    
                    # Öğünler
                    self.meal_vars['sabah_miktar'].set(str(int(info.get('sabah_miktar', 0))))
                    self.meal_vars['ogle_miktar'].set(str(int(info.get('ogle_miktar', 0))))
                    self.meal_vars['aksam_miktar'].set(str(int(info.get('aksam_miktar', 0))))
                    self.meal_vars['toplam_miktar'].set(str(int(info.get('toplam_miktar', 0))))
                    
                    # Ekmekler
                    self.bread_vars['sabah_ekmek'].set(str(int(info.get('sabah_ekmek', 0))))
                    self.bread_vars['ogle_ekmek'].set(str(int(info.get('ogle_ekmek', 0))))
                    self.bread_vars['aksam_ekmek'].set(str(int(info.get('aksam_ekmek', 0))))
                    self.bread_vars['toplam_ekmek'].set(str(int(info.get('toplam_ekmek', 0))))
                    
        except Exception as e:
            messagebox.showerror("Hata", f"Ayarlar yüklenemedi:\n{e}")
    
    def save_settings(self):
        """Ayarları kaydet"""
        # Validasyon
        meal_counts = ['sabah_miktar', 'ogle_miktar', 'aksam_miktar']
        for field in meal_counts:
            value = self.meal_vars[field].get().strip()
            is_valid, msg = validate_integer(value, f"Öğün sayısı ({field})", min_value=0)
            if not is_valid:
                messagebox.showwarning("Uyarı", msg)
                return
        
        bread_counts = ['sabah_ekmek', 'ogle_ekmek', 'aksam_ekmek']
        for field in bread_counts:
            value = self.bread_vars[field].get().strip()
            is_valid, msg = validate_integer(value, f"Ekmek sayısı ({field})", min_value=0)
            if not is_valid:
                messagebox.showwarning("Uyarı", msg)
                return
        
        try:
            # Verileri hazırla
            data = {
                'cezaevi': self.cezaevi_var.get().strip(),
                'mudur': self.personnel_vars['mudur'].get().strip(),
                'ambar_memuru': self.personnel_vars['ambar_memuru'].get().strip(),
                'uye1': self.personnel_vars['uye1'].get().strip(),
                'uye2': self.personnel_vars['uye2'].get().strip(),
                'uye3': self.personnel_vars['uye3'].get().strip(),
                'sabah_miktar': parse_int(self.meal_vars['sabah_miktar'].get()),
                'ogle_miktar': parse_int(self.meal_vars['ogle_miktar'].get()),
                'aksam_miktar': parse_int(self.meal_vars['aksam_miktar'].get()),
                'toplam_miktar': parse_int(self.meal_vars['toplam_miktar'].get()),
                'sabah_ekmek': parse_int(self.bread_vars['sabah_ekmek'].get()),
                'ogle_ekmek': parse_int(self.bread_vars['ogle_ekmek'].get()),
                'aksam_ekmek': parse_int(self.bread_vars['aksam_ekmek'].get()),
                'toplam_ekmek': parse_int(self.bread_vars['toplam_ekmek'].get())
            }
            
            # Kaydet
            with Database() as db:
                db.update_cezaevi_bilgileri(data)
            
            messagebox.showinfo("Başarılı", "Ayarlar kaydedildi.")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Kayıt hatası:\n{e}")
