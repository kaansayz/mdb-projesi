# -*- coding: utf-8 -*-
"""
Hesaplama Fonksiyonları
Maliyet, kalori ve diğer hesaplamalar
"""

from typing import Tuple

# Stok uyarı eşikleri
STOK_KRITIK_ESIK = 10  # Kırmızı uyarı
STOK_UYARI_ESIK = 50   # Sarı uyarı


def hesapla_tabela(mevcut_kisi: int, verilen_miktar: float, 
                   urun_fiyat: float, urun_kalori: int) -> Tuple[float, float, float, float]:
    """
    Tabela hesaplamaları yapar
    
    Args:
        mevcut_kisi: Mevcut kişi sayısı
        verilen_miktar: Verilen miktar
        urun_fiyat: Ürün fiyatı
        urun_kalori: Ürün kalorisi
    
    Returns:
        Tuple: (tutar, sahis_tutar, sahis_miktar, sahis_kalori)
    """
    if mevcut_kisi <= 0:
        return 0.0, 0.0, 0.0, 0.0
    
    # Toplam tutar
    tutar = verilen_miktar * urun_fiyat
    
    # Kişi başı tutar
    sahis_tutar = tutar / mevcut_kisi
    
    # Kişi başı miktar
    sahis_miktar = verilen_miktar / mevcut_kisi
    
    # Kişi başı kalori
    sahis_kalori = (verilen_miktar * urun_kalori) / mevcut_kisi
    
    return tutar, sahis_tutar, sahis_miktar, sahis_kalori


def hesapla_gunluk_ozet(tabela_kayitlari: list) -> dict:
    """
    Günlük özet hesaplar
    
    Args:
        tabela_kayitlari: Tabela kayıtları listesi
    
    Returns:
        dict: Özet bilgileri
    """
    toplam_maliyet = 0.0
    toplam_kalori = 0.0
    urun_sayisi = len(tabela_kayitlari)
    
    for kayit in tabela_kayitlari:
        toplam_maliyet += kayit.get('tutar', 0)
        toplam_kalori += kayit.get('sahis_kalori', 0)
    
    return {
        'toplam_maliyet': toplam_maliyet,
        'toplam_kalori': toplam_kalori,
        'urun_sayisi': urun_sayisi,
        'ortalama_maliyet': toplam_maliyet / urun_sayisi if urun_sayisi > 0 else 0
    }


def hesapla_aylik_ozet(aylik_kayitlar: list) -> dict:
    """
    Aylık özet hesaplar
    
    Args:
        aylik_kayitlar: Aylık kayıtlar listesi
    
    Returns:
        dict: Aylık özet bilgileri
    """
    toplam_tutar = sum(k.get('tutar', 0) for k in aylik_kayitlar)
    toplam_verilen = sum(k.get('verilen', 0) for k in aylik_kayitlar)
    gun_sayisi = len(set(k.get('tarih') for k in aylik_kayitlar if k.get('tarih') is not None))
    
    return {
        'toplam_tutar': toplam_tutar,
        'toplam_verilen': toplam_verilen,
        'gun_sayisi': gun_sayisi,
        'gunluk_ortalama': toplam_tutar / gun_sayisi if gun_sayisi > 0 else 0
    }


def stok_uyari_durumu(stok_miktari: float) -> str:
    """
    Stok durumuna göre uyarı seviyesi belirler
    
    Args:
        stok_miktari: Stok miktarı
    
    Returns:
        str: 'critical', 'warning', 'normal'
    """
    if stok_miktari <= STOK_KRITIK_ESIK:
        return 'critical'  # Kırmızı
    elif stok_miktari <= STOK_UYARI_ESIK:
        return 'warning'   # Sarı
    else:
        return 'normal'    # Yeşil


def format_para(tutar: float) -> str:
    """
    Para formatı (Türk Lirası)
    
    Args:
        tutar: Tutar
    
    Returns:
        str: Formatlanmış tutar
    """
    return f"{tutar:,.2f} TL"


def format_miktar(miktar: float, birim: str = '') -> str:
    """
    Miktar formatı
    
    Args:
        miktar: Miktar
        birim: Birim (kg, adet, vb.)
    
    Returns:
        str: Formatlanmış miktar
    """
    if birim:
        return f"{miktar:,.3f} {birim}"
    return f"{miktar:,.3f}"


def format_kalori(kalori: float) -> str:
    """
    Kalori formatı
    
    Args:
        kalori: Kalori değeri
    
    Returns:
        str: Formatlanmış kalori
    """
    return f"{kalori:,.0f} kcal"
