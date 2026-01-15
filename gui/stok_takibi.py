# -*- coding: utf-8 -*-
"""
Stok Takibi Modülü
Ürün bazlı stok durumu ve uyarılar
"""

import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from utils.hesaplamalar import stok_uyari_durumu


class StokTakibi:
    """Stok takibi modülü"""
    
    def __init__(self, parent):
        self.parent = parent
        self.create_ui()
        self.load_stock()
    
    def create_ui(self):
        """UI oluştur"""
        # Ana container
        main_frame = tk.Frame(self.parent, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Başlık
        header_frame = tk.Frame(main_frame, bg='#f0f0f0')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            header_frame,
            text="📊 Stok Takibi",
            font=("Segoe UI", 20, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50'
        ).pack(side=tk.LEFT)
        
        tk.Button(
            header_frame,
            text="🔄 Yenile",
            font=("Segoe UI", 10),
            bg='#2196F3',
            fg='white',
            cursor='hand2',
            relief=tk.FLAT,
            command=self.load_stock,
            padx=20,
            pady=8
        ).pack(side=tk.RIGHT)
        
        # Uyarı açıklamaları
        legend_frame = tk.Frame(main_frame, bg='white', relief=tk.FLAT, bd=2)
        legend_frame.pack(fill=tk.X, pady=(0, 15))
        
        legend_content = tk.Frame(legend_frame, bg='white')
        legend_content.pack(padx=15, pady=10)
        
        tk.Label(
            legend_content,
            text="Stok Durumu:",
            font=("Segoe UI", 10, "bold"),
            bg='white'
        ).pack(side=tk.LEFT, padx=(0, 15))
        
        # Kritik
        tk.Label(
            legend_content,
            text="🔴 Kritik (≤10)",
            font=("Segoe UI", 9),
            bg='white',
            fg='#f44336'
        ).pack(side=tk.LEFT, padx=10)
        
        # Uyarı
        tk.Label(
            legend_content,
            text="🟡 Uyarı (≤50)",
            font=("Segoe UI", 9),
            bg='white',
            fg='#ff9800'
        ).pack(side=tk.LEFT, padx=10)
        
        # Normal
        tk.Label(
            legend_content,
            text="🟢 Normal (>50)",
            font=("Segoe UI", 9),
            bg='white',
            fg='#4CAF50'
        ).pack(side=tk.LEFT, padx=10)
        
        # Treeview
        list_frame = tk.Frame(main_frame, bg='white', relief=tk.FLAT, bd=2)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Başlık
        tk.Label(
            list_frame,
            text="Ürün Stok Listesi",
            font=("Segoe UI", 12, "bold"),
            bg='white',
            fg='#2c3e50'
        ).pack(anchor='w', padx=15, pady=(15, 10))
        
        # Tree frame
        tree_frame = tk.Frame(list_frame, bg='white')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("urun_no", "cinsi", "birimi", "stok", "durum"),
            show="headings",
            yscrollcommand=scrollbar.set,
            selectmode="browse"
        )
        
        columns_config = [
            ("urun_no", "Ürün No", 100),
            ("cinsi", "Ürün Adı", 300),
            ("birimi", "Birim", 100),
            ("stok", "Stok Miktarı", 150),
            ("durum", "Durum", 150)
        ]
        
        for col, heading, width in columns_config:
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=width, anchor='center' if col != 'cinsi' else 'w')
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)
        
        # Tag renkleri
        self.tree.tag_configure('critical', background='#ffebee', foreground='#f44336')
        self.tree.tag_configure('warning', background='#fff3e0', foreground='#ff9800')
        self.tree.tag_configure('normal', background='#e8f5e9', foreground='#4CAF50')
    
    def load_stock(self):
        """Stok verilerini yükle"""
        try:
            # Treeview'i temizle
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            with Database() as db:
                stocks = db.get_stok_durumu()
                
                for stock in stocks:
                    stok_miktar = stock.get('toplam_stok', 0)
                    durum = stok_uyari_durumu(stok_miktar)
                    
                    # Durum metni
                    if durum == 'critical':
                        durum_text = "🔴 KRİTİK"
                        tag = 'critical'
                    elif durum == 'warning':
                        durum_text = "🟡 UYARI"
                        tag = 'warning'
                    else:
                        durum_text = "🟢 NORMAL"
                        tag = 'normal'
                    
                    self.tree.insert('', 'end', values=(
                        stock.get('urun_no', ''),
                        stock.get('cinsi', ''),
                        stock.get('birimi', ''),
                        f"{stok_miktar:.3f}",
                        durum_text
                    ), tags=(tag,))
                    
        except Exception as e:
            messagebox.showerror("Hata", f"Stok verileri yüklenemedi:\n{e}")
