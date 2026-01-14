#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build script for creating MDB-Analiz executable
Automatically builds the application using PyInstaller
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def print_step(step_num, text):
    """Print formatted step"""
    print(f"\n[{step_num}] {text}")
    print("-" * 60)


def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        result = subprocess.run(
            ['pyinstaller', '--version'],
            capture_output=True,
            text=True,
            check=True
        )
        version = result.stdout.strip()
        print(f"✅ PyInstaller bulundu: {version}")
        return True
    except FileNotFoundError:
        print("❌ PyInstaller bulunamadı!")
        print("\nKurmak için:")
        print("  pip install pyinstaller")
        return False
    except subprocess.CalledProcessError as e:
        print(f"❌ PyInstaller kontrolü başarısız: {e}")
        return False


def clean_build_files():
    """Clean previous build files"""
    dirs_to_clean = ['build', 'dist']
    files_to_clean = ['MDB-Analiz.spec', 'mdb_gui.spec']
    
    print("🗑️  Eski build dosyaları temizleniyor...")
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"   ✓ {dir_name}/ klasörü silindi")
            except Exception as e:
                print(f"   ⚠️  {dir_name}/ silinemedi: {e}")
    
    for file_name in files_to_clean:
        if os.path.exists(file_name):
            try:
                os.remove(file_name)
                print(f"   ✓ {file_name} silindi")
            except Exception as e:
                print(f"   ⚠️  {file_name} silinemedi: {e}")


def check_icon_file():
    """Check if icon file exists"""
    icon_files = ['app_icon.ico', 'icon.ico', 'mdb_icon.ico']
    
    for icon_file in icon_files:
        if os.path.exists(icon_file):
            print(f"✅ İkon dosyası bulundu: {icon_file}")
            return icon_file
    
    print("⚠️  İkon dosyası bulunamadı (opsiyonel)")
    return None


def build_executable(icon_file=None):
    """Build the executable using PyInstaller"""
    print("🔨 Executable oluşturuluyor...")
    print("   Bu işlem birkaç dakika sürebilir...\n")
    
    # Build command
    cmd = [
        'pyinstaller',
        '--onefile',           # Single executable
        '--windowed',          # No console window
        '--name=MDB-Analiz',   # Output name
    ]
    
    # Add icon if available
    if icon_file:
        cmd.append(f'--icon={icon_file}')
    
    # Add hidden imports
    hidden_imports = [
        'pyodbc',
        'pandas',
        'ttkthemes',
        'openpyxl',
        'PIL',
    ]
    
    for imp in hidden_imports:
        cmd.extend(['--hidden-import', imp])
    
    # Add main script
    cmd.append('mdb_gui.py')
    
    print(f"Komut: {' '.join(cmd)}\n")
    
    try:
        # Run PyInstaller
        result = subprocess.run(
            cmd,
            check=True,
            text=True
        )
        
        print("\n✅ Build başarılı!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build başarısız!")
        print(f"Hata kodu: {e.returncode}")
        return False
    except Exception as e:
        print(f"\n❌ Beklenmeyen hata: {e}")
        return False


def verify_build():
    """Verify that the executable was created"""
    exe_path = Path('dist') / 'MDB-Analiz.exe'
    
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"\n✅ Executable oluşturuldu!")
        print(f"   Konum: {exe_path}")
        print(f"   Boyut: {size_mb:.2f} MB")
        return True
    else:
        print(f"\n❌ Executable bulunamadı: {exe_path}")
        return False


def show_instructions():
    """Show post-build instructions"""
    print("\n" + "=" * 60)
    print("  📋 BİTTİ - KULLANIM TALİMATLARI")
    print("=" * 60)
    
    print("\n✅ Build işlemi tamamlandı!")
    print("\n📁 Dosya konumu:")
    print("   dist/MDB-Analiz.exe")
    
    print("\n🚀 Çalıştırmak için:")
    print("   1. dist/ klasörüne gidin")
    print("   2. MDB-Analiz.exe dosyasını çift tıklayın")
    
    print("\n💾 Dağıtım için:")
    print("   • Sadece MDB-Analiz.exe dosyasını paylaşın")
    print("   • Diğer dosyalar gerekmez")
    
    print("\n⚠️  Önemli notlar:")
    print("   • İlk çalıştırmada antivirüs uyarısı olabilir")
    print("   • Windows Defender'a istisna ekleyebilirsiniz")
    print("   • Microsoft Access Database Engine gereklidir")
    
    print("\n📚 Daha fazla bilgi için:")
    print("   build_instructions.md dosyasına bakın")
    
    print("\n" + "=" * 60 + "\n")


def main():
    """Main build process"""
    print_header("🏗️  MDB-Analiz Executable Builder")
    
    # Check if main file exists
    if not os.path.exists('mdb_gui.py'):
        print("❌ Hata: mdb_gui.py dosyası bulunamadı!")
        print("   Bu scripti proje ana dizininde çalıştırın.")
        return 1
    
    # Step 1: Check PyInstaller
    print_step(1, "PyInstaller kontrolü")
    if not check_pyinstaller():
        return 1
    
    # Step 2: Clean old files
    print_step(2, "Eski build dosyalarını temizle")
    clean_build_files()
    
    # Step 3: Check for icon
    print_step(3, "İkon dosyası kontrolü")
    icon_file = check_icon_file()
    
    # Step 4: Build executable
    print_step(4, "Executable oluştur")
    if not build_executable(icon_file):
        print("\n❌ Build başarısız oldu!")
        print("\nSorun giderme:")
        print("  1. Tüm bağımlılıkları yükleyin: pip install -r requirements.txt")
        print("  2. PyInstaller'ı güncelleyin: pip install --upgrade pyinstaller")
        print("  3. Hata mesajlarını kontrol edin")
        return 1
    
    # Step 5: Verify build
    print_step(5, "Build doğrulama")
    if not verify_build():
        return 1
    
    # Show instructions
    show_instructions()
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Build iptal edildi (Ctrl+C)")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Beklenmeyen hata: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
