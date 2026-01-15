# -*- coding: utf-8 -*-
"""
Ana Ekran Modülü
Dashboard ve özet bilgiler
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from database import Database
from utils.hesaplamalar import format_para, format_kalori


class AnaEkran:
    """Ana ekran modülü"""
    
    def __init__(self, parent):
        self.parent = parent
        self.create_ui()
        self.load_data()
    
    def create_ui(self):
        """UI oluştur"""
        # Ana container
        main_frame = tk.Frame(self.parent, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Başlık
        header = tk.Label(
            main_frame,
            text="📊 Ana Sayfa",
            font=("Segoe UI", 20, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        header.pack(anchor='w', pady=(0, 20))
        
        # Üst kısım - Cezaevi bilgileri
        self.create_prison_info_section(main_frame)
        
        # Orta kısım - İstatistikler
        self.create_statistics_section(main_frame)
        
        # Alt kısım - Bugünün özeti
        self.create_today_summary(main_frame)
    
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
        
        info_frame = tk.Frame(frame, bg='white')
        info_frame.pack(fill=tk.BOTH, padx=15, pady=15)
        
        # Bilgi labelları
        self.lbl_cezaevi = tk.Label(
            info_frame,
            text="Cezaevi: -",
            font=("Segoe UI", 11),
            bg='white',
            anchor='w'
        )
        self.lbl_cezaevi.pack(fill=tk.X, pady=2)
        
        self.lbl_mudur = tk.Label(
            info_frame,
            text="Müdür: -",
            font=("Segoe UI", 10),
            bg='white',
            anchor='w',
            fg='#7f8c8d'
        )
        self.lbl_mudur.pack(fill=tk.X, pady=2)
        
        self.lbl_memur = tk.Label(
            info_frame,
            text="Ambar Memuru: -",
            font=("Segoe UI", 10),
            bg='white',
            anchor='w',
            fg='#7f8c8d'
        )
        self.lbl_memur.pack(fill=tk.X, pady=2)
    
    def create_statistics_section(self, parent):
        """İstatistikler bölümü"""
        stats_frame = tk.Frame(parent, bg='#f0f0f0')
        stats_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 4 kart oluştur
        self.create_stat_card(
            stats_frame, "Günlük Kişi Sayısı", "0", "#3498db", 0
        )
        self.create_stat_card(
            stats_frame, "Sabah Öğünü", "0", "#9b59b6", 1
        )
        self.create_stat_card(
            stats_frame, "Öğle Öğünü", "0", "#e67e22", 2
        )
        self.create_stat_card(
            stats_frame, "Akşam Öğünü", "0", "#e74c3c", 3
        )
        
        # İkinci satır
        stats_frame2 = tk.Frame(parent, bg='#f0f0f0')
        stats_frame2.pack(fill=tk.X, pady=(0, 15))
        
        self.create_stat_card(
            stats_frame2, "Toplam Ekmek", "0 adet", "#27ae60", 0
        )
        self.create_stat_card(
            stats_frame2, "Sabah Ekmeği", "0 adet", "#16a085", 1
        )
        self.create_stat_card(
            stats_frame2, "Öğle Ekmeği", "0 adet", "#f39c12", 2
        )
        self.create_stat_card(
            stats_frame2, "Akşam Ekmeği", "0 adet", "#d35400", 3
        )
    
    def create_stat_card(self, parent, title, value, color, column):
        """İstatistik kartı oluştur"""
        card = tk.Frame(
            parent,
            bg=color,
            relief=tk.FLAT,
            bd=0
        )
        card.grid(row=0, column=column, sticky='nsew', padx=5)
        parent.grid_columnconfigure(column, weight=1)
        
        # Başlık
        lbl_title = tk.Label(
            card,
            text=title,
            font=("Segoe UI", 9),
            bg=color,
            fg='white'
        )
        lbl_title.pack(pady=(15, 5))
        
        # Değer
        lbl_value = tk.Label(
            card,
            text=value,
            font=("Segoe UI", 18, "bold"),
            bg=color,
            fg='white'
        )
        lbl_value.pack(pady=(0, 15))
        
        # Referansı sakla
        if not hasattr(self, 'stat_labels'):
            self.stat_labels = {}
        self.stat_labels[title] = lbl_value
    
    def create_today_summary(self, parent):
        """Bugünün özeti"""
        frame = tk.LabelFrame(
            parent,
            text=f"Bugünün Özeti - {date.today().strftime('%d.%m.%Y')}",
            font=("Segoe UI", 12, "bold"),
            bg='white',
            fg='#2c3e50',
            relief=tk.FLAT,
            bd=2
        )
        frame.pack(fill=tk.BOTH, expand=True)
        
        content_frame = tk.Frame(frame, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Grid oluştur
        labels = [
            ("Toplam Maliyet:", 0),
            ("Toplam Kalori:", 1),
            ("Ürün Çeşidi:", 2),
            ("İşlem Sayısı:", 3)
        ]
        
        self.summary_labels = {}
        
        for text, row in labels:
            lbl_key = tk.Label(
                content_frame,
                text=text,
                font=("Segoe UI", 11, "bold"),
                bg='white',
                anchor='w'
            )
            lbl_key.grid(row=row, column=0, sticky='w', padx=(0, 10), pady=8)
            
            lbl_val = tk.Label(
                content_frame,
                text="-",
                font=("Segoe UI", 11),
                bg='white',
                anchor='w',
                fg='#2196F3'
            )
            lbl_val.grid(row=row, column=1, sticky='w', pady=8)
            
            self.summary_labels[text] = lbl_val
        
        # Yenile butonu
        btn_refresh = tk.Button(
            content_frame,
            text="🔄 Yenile",
            font=("Segoe UI", 10),
            bg='#2196F3',
            fg='white',
            cursor='hand2',
            relief=tk.FLAT,
            command=self.load_data,
            padx=20,
            pady=8
        )
        btn_refresh.grid(row=4, column=0, columnspan=2, pady=(15, 0))
    
    def load_data(self):
        """Verileri yükle"""
        try:
            with Database() as db:
                # Cezaevi bilgileri
                cezaevi_info = db.get_cezaevi_bilgileri()
                if cezaevi_info:
                    self.lbl_cezaevi.config(
                        text=f"Cezaevi: {cezaevi_info.get('cezaevi', '-')}"
                    )
                    self.lbl_mudur.config(
                        text=f"Müdür: {cezaevi_info.get('mudur', '-')}"
                    )
                    self.lbl_memur.config(
                        text=f"Ambar Memuru: {cezaevi_info.get('ambar_memuru', '-')}"
                    )
                    
                    # İstatistikler
                    if hasattr(self, 'stat_labels'):
                        self.stat_labels["Günlük Kişi Sayısı"].config(
                            text=str(int(cezaevi_info.get('toplam_miktar', 0)))
                        )
                        self.stat_labels["Sabah Öğünü"].config(
                            text=str(int(cezaevi_info.get('sabah_miktar', 0)))
                        )
                        self.stat_labels["Öğle Öğünü"].config(
                            text=str(int(cezaevi_info.get('ogle_miktar', 0)))
                        )
                        self.stat_labels["Akşam Öğünü"].config(
                            text=str(int(cezaevi_info.get('aksam_miktar', 0)))
                        )
                        self.stat_labels["Toplam Ekmek"].config(
                            text=f"{cezaevi_info.get('toplam_ekmek', 0)} adet"
                        )
                        self.stat_labels["Sabah Ekmeği"].config(
                            text=f"{cezaevi_info.get('sabah_ekmek', 0)} adet"
                        )
                        self.stat_labels["Öğle Ekmeği"].config(
                            text=f"{cezaevi_info.get('ogle_ekmek', 0)} adet"
                        )
                        self.stat_labels["Akşam Ekmeği"].config(
                            text=f"{cezaevi_info.get('aksam_ekmek', 0)} adet"
                        )
                
                # Bugünün özeti
                today = date.today().strftime('%Y-%m-%d')
                today_records = db.get_tabela_by_date_range(today, today)
                
                total_cost = sum(r.get('tutar', 0) for r in today_records)
                total_calories = sum(r.get('sahis_kalori', 0) for r in today_records)
                unique_products = len(set(r.get('cinsi', '') for r in today_records))
                
                self.summary_labels["Toplam Maliyet:"].config(
                    text=format_para(total_cost)
                )
                self.summary_labels["Toplam Kalori:"].config(
                    text=format_kalori(total_calories)
                )
                self.summary_labels["Ürün Çeşidi:"].config(
                    text=f"{unique_products} çeşit"
                )
                self.summary_labels["İşlem Sayısı:"].config(
                    text=f"{len(today_records)} işlem"
                )
                
        except Exception as e:
            messagebox.showerror("Hata", f"Veri yükleme hatası:\n{e}")
