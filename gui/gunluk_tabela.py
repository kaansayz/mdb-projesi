# -*- coding: utf-8 -*-
"""
Günlük Tabela Modülü
Günlük yemek planlaması ve kayıt
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from tkcalendar import DateEntry
from database import Database
from utils.hesaplamalar import hesapla_tabela, format_para
from utils.validasyon import validate_integer, validate_number, parse_float, parse_int


class GunlukTabela:
    """Günlük tabela modülü"""
    
    def __init__(self, parent):
        self.parent = parent
        self.selected_record = None
        self.create_ui()
        self.load_products()
        self.load_records()
    
    def create_ui(self):
        """UI oluştur"""
        # Ana container
        main_frame = tk.Frame(self.parent, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Başlık
        header = tk.Label(
            main_frame,
            text="📋 Günlük Tabela",
            font=("Segoe UI", 20, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        header.pack(anchor='w', pady=(0, 20))
        
        # İki panel
        content_frame = tk.Frame(main_frame, bg='#f0f0f0')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Üst panel - Form
        self.create_form_panel(content_frame)
        
        # Alt panel - Kayıtlar
        self.create_records_panel(content_frame)
    
    def create_form_panel(self, parent):
        """Form paneli"""
        form_frame = tk.LabelFrame(
            parent,
            text="Yeni Kayıt",
            font=("Segoe UI", 12, "bold"),
            bg='white',
            fg='#2c3e50',
            relief=tk.FLAT,
            bd=2
        )
        form_frame.pack(fill=tk.X, pady=(0, 15))
        
        content = tk.Frame(form_frame, bg='white')
        content.pack(fill=tk.BOTH, padx=15, pady=15)
        
        # Sol taraf - Temel bilgiler
        left_frame = tk.Frame(content, bg='white')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Tarih
        tk.Label(
            left_frame,
            text="Tarih:",
            font=("Segoe UI", 10, "bold"),
            bg='white'
        ).grid(row=0, column=0, sticky='w', pady=(0, 5))
        
        self.date_entry = DateEntry(
            left_frame,
            width=20,
            background='#2196F3',
            foreground='white',
            borderwidth=2,
            date_pattern='dd.mm.yyyy',
            font=("Segoe UI", 10)
        )
        self.date_entry.grid(row=1, column=0, sticky='ew', pady=(0, 10))
        
        # Öğün
        tk.Label(
            left_frame,
            text="Öğün:",
            font=("Segoe UI", 10, "bold"),
            bg='white'
        ).grid(row=2, column=0, sticky='w', pady=(0, 5))
        
        self.ogun_var = tk.StringVar(value='SABAH')
        ogun_combo = ttk.Combobox(
            left_frame,
            textvariable=self.ogun_var,
            values=['SABAH', 'ÖĞLE', 'AKŞAM'],
            state='readonly',
            font=("Segoe UI", 10)
        )
        ogun_combo.grid(row=3, column=0, sticky='ew', pady=(0, 10))
        
        # Mevcut kişi sayısı
        tk.Label(
            left_frame,
            text="Mevcut Kişi Sayısı:",
            font=("Segoe UI", 10, "bold"),
            bg='white'
        ).grid(row=4, column=0, sticky='w', pady=(0, 5))
        
        self.mevcut_var = tk.StringVar()
        tk.Entry(
            left_frame,
            textvariable=self.mevcut_var,
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            bg='#ecf0f1'
        ).grid(row=5, column=0, sticky='ew', pady=(0, 10), ipady=5)
        
        left_frame.grid_columnconfigure(0, weight=1)
        
        # Sağ taraf - Ürün bilgileri
        right_frame = tk.Frame(content, bg='white')
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Ürün seçimi
        tk.Label(
            right_frame,
            text="Ürün:",
            font=("Segoe UI", 10, "bold"),
            bg='white'
        ).grid(row=0, column=0, sticky='w', pady=(0, 5))
        
        self.urun_var = tk.StringVar()
        self.urun_combo = ttk.Combobox(
            right_frame,
            textvariable=self.urun_var,
            state='readonly',
            font=("Segoe UI", 10),
            width=30
        )
        self.urun_combo.grid(row=1, column=0, sticky='ew', pady=(0, 10))
        self.urun_combo.bind('<<ComboboxSelected>>', self.on_product_selected)
        
        # Verilen miktar
        tk.Label(
            right_frame,
            text="Verilen Miktar:",
            font=("Segoe UI", 10, "bold"),
            bg='white'
        ).grid(row=2, column=0, sticky='w', pady=(0, 5))
        
        self.miktar_var = tk.StringVar()
        tk.Entry(
            right_frame,
            textvariable=self.miktar_var,
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            bg='#ecf0f1'
        ).grid(row=3, column=0, sticky='ew', pady=(0, 10), ipady=5)
        
        # Hesaplanan değerler
        self.calc_label = tk.Label(
            right_frame,
            text="Tutar: - | Kişi Başı: - | Kalori: -",
            font=("Segoe UI", 9),
            bg='white',
            fg='#7f8c8d',
            justify='left'
        )
        self.calc_label.grid(row=4, column=0, sticky='w', pady=(0, 10))
        
        right_frame.grid_columnconfigure(0, weight=1)
        
        # Butonlar
        btn_frame = tk.Frame(content, bg='white')
        btn_frame.pack(side=tk.LEFT, padx=(10, 0))
        
        tk.Button(
            btn_frame,
            text="➕ Ekle",
            font=("Segoe UI", 11, "bold"),
            bg='#4CAF50',
            fg='white',
            cursor='hand2',
            relief=tk.FLAT,
            command=self.add_record,
            padx=20,
            pady=30
        ).pack(fill=tk.X)
        
        # Hesapla butonu
        self.miktar_var.trace('w', lambda *args: self.calculate_values())
        self.mevcut_var.trace('w', lambda *args: self.calculate_values())
    
    def create_records_panel(self, parent):
        """Kayıtlar paneli"""
        records_frame = tk.LabelFrame(
            parent,
            text="Günlük Kayıtlar",
            font=("Segoe UI", 12, "bold"),
            bg='white',
            fg='#2c3e50',
            relief=tk.FLAT,
            bd=2
        )
        records_frame.pack(fill=tk.BOTH, expand=True)
        
        # Filtre bölümü
        filter_frame = tk.Frame(records_frame, bg='white')
        filter_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            filter_frame,
            text="Görüntüle:",
            font=("Segoe UI", 10, "bold"),
            bg='white'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            filter_frame,
            text="🔄 Yenile",
            font=("Segoe UI", 9),
            bg='#2196F3',
            fg='white',
            cursor='hand2',
            relief=tk.FLAT,
            command=self.load_records,
            padx=10,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            filter_frame,
            text="🗑️ Sil",
            font=("Segoe UI", 9),
            bg='#f44336',
            fg='white',
            cursor='hand2',
            relief=tk.FLAT,
            command=self.delete_record,
            padx=10,
            pady=5
        ).pack(side=tk.RIGHT)
        
        # Treeview
        tree_frame = tk.Frame(records_frame, bg='white')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("sira_no", "tarih", "ogun", "mevcut", "cinsi", "verilen", 
                     "tutar", "sahis_tutar", "sahis_miktar", "sahis_kalori"),
            show="headings",
            yscrollcommand=scrollbar.set,
            selectmode="browse"
        )
        
        columns_config = [
            ("sira_no", "Sıra", 50),
            ("tarih", "Tarih", 90),
            ("ogun", "Öğün", 70),
            ("mevcut", "Kişi", 60),
            ("cinsi", "Ürün", 150),
            ("verilen", "Miktar", 80),
            ("tutar", "Tutar", 80),
            ("sahis_tutar", "Kişi Tutar", 80),
            ("sahis_miktar", "Kişi Miktar", 80),
            ("sahis_kalori", "Kalori", 80)
        ]
        
        for col, heading, width in columns_config:
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=width, anchor='center' if col != 'cinsi' else 'w')
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)
        
        self.tree.bind('<<TreeviewSelect>>', self.on_record_select)
    
    def load_products(self):
        """Ürünleri yükle"""
        try:
            with Database() as db:
                products = db.get_all_urunler()
                self.products = {p['cinsi']: p for p in products}
                self.urun_combo['values'] = list(self.products.keys())
        except Exception as e:
            messagebox.showerror("Hata", f"Ürünler yüklenemedi:\n{e}")
    
    def load_records(self):
        """Kayıtları yükle"""
        try:
            # Treeview'i temizle
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Seçili tarihteki kayıtları getir
            selected_date = self.date_entry.get_date().strftime('%Y-%m-%d')
            selected_ogun = self.ogun_var.get()
            
            with Database() as db:
                records = db.get_tabela_by_date_and_ogun(selected_date, selected_ogun)
                
                for record in records:
                    self.tree.insert('', 'end', values=(
                        record.get('sira_no', ''),
                        record.get('tarih', ''),
                        record.get('ogun', ''),
                        record.get('mevcut', 0),
                        record.get('cinsi', ''),
                        f"{record.get('verilen', 0):.3f}",
                        f"{record.get('tutar', 0):.2f}",
                        f"{record.get('sahis_tutar', 0):.2f}",
                        f"{record.get('sahis_miktar', 0):.3f}",
                        f"{record.get('sahis_kalori', 0):.0f}"
                    ))
        except Exception as e:
            messagebox.showerror("Hata", f"Kayıtlar yüklenemedi:\n{e}")
    
    def on_product_selected(self, event):
        """Ürün seçildiğinde"""
        self.calculate_values()
    
    def calculate_values(self):
        """Değerleri hesapla"""
        try:
            urun_name = self.urun_var.get()
            if not urun_name or urun_name not in self.products:
                self.calc_label.config(text="Tutar: - | Kişi Başı: - | Kalori: -")
                return
            
            product = self.products[urun_name]
            mevcut = parse_int(self.mevcut_var.get())
            miktar = parse_float(self.miktar_var.get())
            
            if mevcut <= 0 or miktar <= 0:
                self.calc_label.config(text="Tutar: - | Kişi Başı: - | Kalori: -")
                return
            
            tutar, sahis_tutar, sahis_miktar, sahis_kalori = hesapla_tabela(
                mevcut,
                miktar,
                product['fiyati'],
                product['kalorisi']
            )
            
            self.calc_label.config(
                text=f"Tutar: {tutar:.2f} TL | Kişi Başı: {sahis_tutar:.2f} TL | Kalori: {sahis_kalori:.0f} kcal"
            )
        except Exception as e:
            self.calc_label.config(text=f"Hesaplama hatası: {e}")
    
    def add_record(self):
        """Kayıt ekle"""
        # Validasyon
        urun_name = self.urun_var.get()
        if not urun_name:
            messagebox.showwarning("Uyarı", "Lütfen ürün seçin.")
            return
        
        mevcut = self.mevcut_var.get().strip()
        is_valid, msg = validate_integer(mevcut, "Mevcut Kişi Sayısı", min_value=1)
        if not is_valid:
            messagebox.showwarning("Uyarı", msg)
            return
        
        miktar = self.miktar_var.get().strip()
        is_valid, msg = validate_number(miktar, "Verilen Miktar", min_value=0.001)
        if not is_valid:
            messagebox.showwarning("Uyarı", msg)
            return
        
        try:
            product = self.products[urun_name]
            mevcut_int = parse_int(mevcut)
            miktar_float = parse_float(miktar)
            
            # Hesaplamalar
            tutar, sahis_tutar, sahis_miktar, sahis_kalori = hesapla_tabela(
                mevcut_int,
                miktar_float,
                product['fiyati'],
                product['kalorisi']
            )
            
            # Veritabanına kaydet
            with Database() as db:
                record_data = {
                    'tabela_no': 0,
                    'tarih': self.date_entry.get_date().strftime('%Y-%m-%d'),
                    'mevcut': mevcut_int,
                    'ogun': self.ogun_var.get(),
                    'urun_no': product['urun_no'],
                    'cinsi': product['cinsi'],
                    'stok_mevcudu': 0,
                    'verilen': miktar_float,
                    'fiyati': product['fiyati'],
                    'kalorisi': product['kalorisi'],
                    'defter_no': product.get('defter_no'),
                    'tutar': tutar,
                    'sahis_tutar': sahis_tutar,
                    'sahis_miktar': sahis_miktar,
                    'sahis_kalori': sahis_kalori
                }
                
                db.add_tabela_kayit(record_data)
            
            messagebox.showinfo("Başarılı", "Kayıt eklendi.")
            self.load_records()
            self.clear_form()
            
        except Exception as e:
            messagebox.showerror("Hata", f"Kayıt eklenemedi:\n{e}")
    
    def delete_record(self):
        """Kayıt sil"""
        if not self.selected_record:
            messagebox.showwarning("Uyarı", "Lütfen silmek için bir kayıt seçin.")
            return
        
        response = messagebox.askyesno(
            "Onay",
            "Seçili kaydı silmek istediğinizden emin misiniz?"
        )
        
        if response:
            try:
                with Database() as db:
                    db.delete_tabela_kayit(self.selected_record)
                messagebox.showinfo("Başarılı", "Kayıt silindi.")
                self.load_records()
            except Exception as e:
                messagebox.showerror("Hata", f"Kayıt silinemedi:\n{e}")
    
    def on_record_select(self, event):
        """Kayıt seçildiğinde"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            if values:
                self.selected_record = values[0]  # sira_no
    
    def clear_form(self):
        """Formu temizle"""
        self.urun_var.set('')
        self.mevcut_var.set('')
        self.miktar_var.set('')
        self.calc_label.config(text="Tutar: - | Kişi Başı: - | Kalori: -")
