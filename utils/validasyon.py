# -*- coding: utf-8 -*-
"""
Validasyon Fonksiyonları
Veri doğrulama işlemleri
"""

import re
from datetime import datetime
from typing import Optional, Tuple


def validate_empty(value: str, field_name: str) -> Tuple[bool, Optional[str]]:
    """
    Boş alan kontrolü
    
    Args:
        value: Kontrol edilecek değer
        field_name: Alan adı
    
    Returns:
        Tuple: (is_valid, error_message)
    """
    if not value or not str(value).strip():
        return False, f"{field_name} boş bırakılamaz!"
    return True, None


def validate_number(value: str, field_name: str, 
                    min_value: float = None, max_value: float = None) -> Tuple[bool, Optional[str]]:
    """
    Sayısal değer kontrolü
    
    Args:
        value: Kontrol edilecek değer
        field_name: Alan adı
        min_value: Minimum değer (opsiyonel)
        max_value: Maximum değer (opsiyonel)
    
    Returns:
        Tuple: (is_valid, error_message)
    """
    try:
        num = float(str(value).replace(',', '.'))
        
        if min_value is not None and num < min_value:
            return False, f"{field_name} en az {min_value} olmalıdır!"
        
        if max_value is not None and num > max_value:
            return False, f"{field_name} en fazla {max_value} olabilir!"
        
        return True, None
    except (ValueError, TypeError):
        return False, f"{field_name} geçerli bir sayı olmalıdır!"


def validate_integer(value: str, field_name: str,
                     min_value: int = None, max_value: int = None) -> Tuple[bool, Optional[str]]:
    """
    Tam sayı kontrolü
    
    Args:
        value: Kontrol edilecek değer
        field_name: Alan adı
        min_value: Minimum değer (opsiyonel)
        max_value: Maximum değer (opsiyonel)
    
    Returns:
        Tuple: (is_valid, error_message)
    """
    try:
        num = int(value)
        
        if min_value is not None and num < min_value:
            return False, f"{field_name} en az {min_value} olmalıdır!"
        
        if max_value is not None and num > max_value:
            return False, f"{field_name} en fazla {max_value} olabilir!"
        
        return True, None
    except (ValueError, TypeError):
        return False, f"{field_name} geçerli bir tam sayı olmalıdır!"


def validate_date(date_str: str, field_name: str = "Tarih") -> Tuple[bool, Optional[str]]:
    """
    Tarih formatı kontrolü
    
    Args:
        date_str: Tarih string'i (YYYY-MM-DD formatında)
        field_name: Alan adı
    
    Returns:
        Tuple: (is_valid, error_message)
    """
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True, None
    except (ValueError, TypeError):
        return False, f"{field_name} geçerli bir tarih olmalıdır! (YYYY-MM-DD)"


def validate_ogun(ogun: str) -> Tuple[bool, Optional[str]]:
    """
    Öğün değeri kontrolü
    
    Args:
        ogun: Öğün değeri
    
    Returns:
        Tuple: (is_valid, error_message)
    """
    valid_ogunler = ['SABAH', 'ÖĞLE', 'AKŞAM']
    
    if ogun not in valid_ogunler:
        return False, f"Öğün şunlardan biri olmalıdır: {', '.join(valid_ogunler)}"
    
    return True, None


def validate_price(price: str, field_name: str = "Fiyat") -> Tuple[bool, Optional[str]]:
    """
    Fiyat kontrolü (pozitif sayı)
    
    Args:
        price: Fiyat değeri
        field_name: Alan adı
    
    Returns:
        Tuple: (is_valid, error_message)
    """
    return validate_number(price, field_name, min_value=0)


def validate_quantity(quantity: str, field_name: str = "Miktar") -> Tuple[bool, Optional[str]]:
    """
    Miktar kontrolü (pozitif sayı)
    
    Args:
        quantity: Miktar değeri
        field_name: Alan adı
    
    Returns:
        Tuple: (is_valid, error_message)
    """
    return validate_number(quantity, field_name, min_value=0)


def validate_form_data(data: dict, required_fields: list) -> Tuple[bool, list]:
    """
    Form verilerini toplu kontrol et
    
    Args:
        data: Form verileri dict'i
        required_fields: Zorunlu alanlar listesi
    
    Returns:
        Tuple: (is_valid, error_messages_list)
    """
    errors = []
    
    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f"{field} alanı zorunludur!")
    
    return len(errors) == 0, errors


def sanitize_string(text: str) -> str:
    """
    String'i temizle (XSS koruması için)
    
    Args:
        text: Temizlenecek metin
    
    Returns:
        str: Temizlenmiş metin
    """
    if not text:
        return ""
    
    # HTML/script tag'lerini temizle
    text = re.sub(r'<[^>]+>', '', str(text))
    
    # Fazla boşlukları temizle
    text = ' '.join(text.split())
    
    return text.strip()


def parse_float(value: str) -> float:
    """
    String'i float'a dönüştür (Türkçe virgül desteği ile)
    
    Args:
        value: Dönüştürülecek değer
    
    Returns:
        float: Dönüştürülmüş değer
    """
    try:
        return float(str(value).replace(',', '.'))
    except (ValueError, TypeError):
        return 0.0


def parse_int(value: str) -> int:
    """
    String'i int'e dönüştür
    
    Args:
        value: Dönüştürülecek değer
    
    Returns:
        int: Dönüştürülmüş değer
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0
