# -*- coding: utf-8 -*-
"""
Ürün Yönetimi Modülü
Ürün ekleme, düzenleme, silme ve arama
"""

import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from utils.validasyon import validate_empty, validate_number, validate_integer, parse_float, parse_int


class UrunYonetimi:
    """Ürün yönetimi modülü"""
    
    def __init__(self, parent):
        self.parent = parent
        self.selected_urun = None
        self.create_ui()
        self.load_products()
    
    def create_ui(self):
        """UI oluştur"""
        # Ana container
        main_frame = tk.Frame(self.parent, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Başlık
        header = tk.Label(
            main_frame,
            text="📦 Ürün Yönetimi",
            font=("Segoe UI", 20, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        header.pack(anchor='w', pady=(0, 20))
        
        # İki panel (sol: liste, sağ: form)
        content_frame = tk.Frame(main_frame, bg='#f0f0f0')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sol panel - Ürün listesi
        self.create_list_panel(content_frame)
        
        # Sağ panel - Form
        self.create_form_panel(content_frame)
    
    def create_list_panel(self, parent):
        """Ürün listesi paneli"""
        list_frame = tk.Frame(parent, bg='white', relief=tk.FLAT, bd=2)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Arama bölümü
        search_frame = tk.Frame(list_frame, bg='white')
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            search_frame,
            text="🔍 Ara:",
            font=("Segoe UI", 10),
            bg='white'
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.search_products())
        
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            bg='#ecf0f1'
        )
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        
        # Treeview
        tree_frame = tk.Frame(list_frame, bg='white')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview oluştur
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("urun_no", "cinsi", "birimi", "fiyati", "kalorisi", "defter_no"),
            show="headings",
            yscrollcommand=scrollbar.set,
            selectmode="browse"
        )
        
        # Kolonları ayarla
        columns_config = [
            ("urun_no", "No", 50),
            ("cinsi", "Ürün Adı", 200),
            ("birimi", "Birim", 80),
            ("fiyati", "Fiyat", 80),
            ("kalorisi", "Kalori", 80),
            ("defter_no", "Defter No", 80)
        ]
        
        for col, heading, width in columns_config:
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=width, anchor='center' if col != 'cinsi' else 'w')
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)
        
        # Treeview seçim eventi
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        
        # Butonlar
        btn_frame = tk.Frame(list_frame, bg='white')
        btn_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        tk.Button(
            btn_frame,
            text="🗑️ Sil",
            font=("Segoe UI", 10),
            bg='#f44336',
            fg='white',
            cursor='hand2',
            relief=tk.FLAT,
            command=self.delete_product,
            padx=15,
            pady=8
        ).pack(side=tk.RIGHT, padx=(5, 0))
        
        tk.Button(
            btn_frame,
            text="📝 Düzenle",
            font=("Segoe UI", 10),
            bg='#ff9800',
            fg='white',
            cursor='hand2',
            relief=tk.FLAT,
            command=self.edit_product,
            padx=15,
            pady=8
        ).pack(side=tk.RIGHT, padx=(5, 0))
        
        tk.Button(
            btn_frame,
            text="➕ Yeni",
            font=("Segoe UI", 10),
            bg='#4CAF50',
            fg='white',
            cursor='hand2',
            relief=tk.FLAT,
            command=self.new_product,
            padx=15,
            pady=8
        ).pack(side=tk.RIGHT)
    
    def create_form_panel(self, parent):
        """Form paneli"""
        form_frame = tk.LabelFrame(
            parent,
            text="Ürün Bilgileri",
            font=("Segoe UI", 12, "bold"),
            bg='white',
            fg='#2c3e50',
            relief=tk.FLAT,
            bd=2
        )
        form_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(10, 0))
        form_frame.pack_propagate(False)
        form_frame.config(width=350)
        
        content = tk.Frame(form_frame, bg='white')
        content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Form alanları
        self.form_vars = {}
        
        fields = [
            ("cinsi", "Ürün Adı:", "entry"),
            ("birimi", "Birim:", "entry"),
            ("fiyati", "Fiyat (TL):", "entry"),
            ("kalorisi", "Kalori:", "entry"),
            ("defter_no", "Defter No:", "entry")
        ]
        
        row = 0
        for field_name, label_text, field_type in fields:
            tk.Label(
                content,
                text=label_text,
                font=("Segoe UI", 10, "bold"),
                bg='white',
                anchor='w'
            ).grid(row=row, column=0, sticky='w', pady=(0, 5))
            
            var = tk.StringVar()
            self.form_vars[field_name] = var
            
            entry = tk.Entry(
                content,
                textvariable=var,
                font=("Segoe UI", 10),
                relief=tk.FLAT,
                bg='#ecf0f1'
            )
            entry.grid(row=row+1, column=0, sticky='ew', pady=(0, 15), ipady=5)
            
            row += 2
        
        content.grid_columnconfigure(0, weight=1)
        
        # Kaydet butonu
        self.btn_save = tk.Button(
            content,
            text="💾 Kaydet",
            font=("Segoe UI", 11, "bold"),
            bg='#2196F3',
            fg='white',
            cursor='hand2',
            relief=tk.FLAT,
            command=self.save_product,
            pady=10
        )
        self.btn_save.grid(row=row, column=0, sticky='ew', pady=(10, 5))
        
        # İptal butonu
        tk.Button(
            content,
            text="↩️ İptal",
            font=("Segoe UI", 10),
            bg='#95a5a6',
            fg='white',
            cursor='hand2',
            relief=tk.FLAT,
            command=self.clear_form,
            pady=8
        ).grid(row=row+1, column=0, sticky='ew')
    
    def load_products(self):
        """Ürünleri yükle"""
        try:
            # Treeview'i temizle
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            with Database() as db:
                products = db.get_all_urunler()
                
                for product in products:
                    self.tree.insert('', 'end', values=(
                        product.get('urun_no', ''),
                        product.get('cinsi', ''),
                        product.get('birimi', ''),
                        f"{product.get('fiyati', 0):.2f}",
                        product.get('kalorisi', 0),
                        product.get('defter_no', '')
                    ))
        except Exception as e:
            messagebox.showerror("Hata", f"Ürünler yüklenemedi:\n{e}")
    
    def search_products(self):
        """Ürün ara"""
        search_term = self.search_var.get().strip()
        
        try:
            # Treeview'i temizle
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            with Database() as db:
                if search_term:
                    products = db.search_urunler(search_term)
                else:
                    products = db.get_all_urunler()
                
                for product in products:
                    self.tree.insert('', 'end', values=(
                        product.get('urun_no', ''),
                        product.get('cinsi', ''),
                        product.get('birimi', ''),
                        f"{product.get('fiyati', 0):.2f}",
                        product.get('kalorisi', 0),
                        product.get('defter_no', '')
                    ))
        except Exception as e:
            messagebox.showerror("Hata", f"Arama hatası:\n{e}")
    
    def on_tree_select(self, event):
        """Treeview seçim eventi"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            if values:
                self.selected_urun = values[0]  # urun_no
    
    def new_product(self):
        """Yeni ürün"""
        self.selected_urun = None
        self.clear_form()
        self.btn_save.config(text="💾 Kaydet")
    
    def edit_product(self):
        """Ürün düzenle"""
        if not self.selected_urun:
            messagebox.showwarning("Uyarı", "Lütfen düzenlemek için bir ürün seçin.")
            return
        
        try:
            with Database() as db:
                product = db.get_urun(self.selected_urun)
                if product:
                    self.form_vars['cinsi'].set(product.get('cinsi', ''))
                    self.form_vars['birimi'].set(product.get('birimi', ''))
                    self.form_vars['fiyati'].set(str(product.get('fiyati', 0)))
                    self.form_vars['kalorisi'].set(str(product.get('kalorisi', 0)))
                    self.form_vars['defter_no'].set(str(product.get('defter_no', '')))
                    self.btn_save.config(text="💾 Güncelle")
        except Exception as e:
            messagebox.showerror("Hata", f"Ürün yüklenemedi:\n{e}")
    
    def delete_product(self):
        """Ürün sil"""
        if not self.selected_urun:
            messagebox.showwarning("Uyarı", "Lütfen silmek için bir ürün seçin.")
            return
        
        response = messagebox.askyesno(
            "Onay",
            "Seçili ürünü silmek istediğinizden emin misiniz?"
        )
        
        if response:
            try:
                with Database() as db:
                    db.delete_urun(self.selected_urun)
                messagebox.showinfo("Başarılı", "Ürün silindi.")
                self.load_products()
                self.clear_form()
            except Exception as e:
                messagebox.showerror("Hata", f"Ürün silinemedi:\n{e}")
    
    def save_product(self):
        """Ürün kaydet"""
        # Validasyon
        cinsi = self.form_vars['cinsi'].get().strip()
        birimi = self.form_vars['birimi'].get().strip()
        fiyati = self.form_vars['fiyati'].get().strip()
        kalorisi = self.form_vars['kalorisi'].get().strip()
        defter_no = self.form_vars['defter_no'].get().strip()
        
        # Kontroller
        is_valid, msg = validate_empty(cinsi, "Ürün Adı")
        if not is_valid:
            messagebox.showwarning("Uyarı", msg)
            return
        
        is_valid, msg = validate_number(fiyati, "Fiyat", min_value=0)
        if not is_valid:
            messagebox.showwarning("Uyarı", msg)
            return
        
        is_valid, msg = validate_integer(kalorisi, "Kalori", min_value=0)
        if not is_valid:
            messagebox.showwarning("Uyarı", msg)
            return
        
        try:
            with Database() as db:
                if self.selected_urun:
                    # Güncelle
                    db.update_urun(
                        self.selected_urun,
                        cinsi,
                        parse_int(defter_no) if defter_no else None,
                        parse_int(kalorisi),
                        birimi,
                        parse_float(fiyati)
                    )
                    messagebox.showinfo("Başarılı", "Ürün güncellendi.")
                else:
                    # Yeni ekle
                    db.add_urun(
                        cinsi,
                        parse_int(defter_no) if defter_no else None,
                        parse_int(kalorisi),
                        birimi,
                        parse_float(fiyati)
                    )
                    messagebox.showinfo("Başarılı", "Ürün eklendi.")
                
                self.load_products()
                self.clear_form()
        except Exception as e:
            messagebox.showerror("Hata", f"Kayıt hatası:\n{e}")
    
    def clear_form(self):
        """Formu temizle"""
        for var in self.form_vars.values():
            var.set('')
        self.selected_urun = None
        self.btn_save.config(text="💾 Kaydet")
