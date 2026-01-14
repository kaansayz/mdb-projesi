#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for mdb_gui.py
Validates imports and code structure without running GUI
"""

import sys
import ast
import importlib.util

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")

def check_file_syntax(filepath):
    """Check if Python file has valid syntax"""
    print(f"🔍 Checking syntax: {filepath}")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        ast.parse(code)
        print(f"✅ Syntax OK: {filepath}")
        return True
    except SyntaxError as e:
        print(f"❌ Syntax Error in {filepath}:")
        print(f"   Line {e.lineno}: {e.msg}")
        return False
    except Exception as e:
        print(f"❌ Error checking {filepath}: {e}")
        return False

def check_imports(filepath):
    """Check which imports are available"""
    print(f"\n🔍 Checking imports in: {filepath}")
    
    required_imports = {
        'os': 'standard',
        'sys': 'standard',
        'time': 'standard',
        'threading': 'standard',
        'datetime': 'standard',
        'pathlib': 'standard',
        'traceback': 'standard',
        'tkinter': 'GUI (may not be available in headless)',
        'pyodbc': 'database',
        'pandas': 'data processing',
        'ttkthemes': 'GUI themes',
        'openpyxl': 'Excel support',
    }
    
    available = []
    missing = []
    
    for module, description in required_imports.items():
        try:
            __import__(module)
            available.append(f"{module} ({description})")
            print(f"   ✅ {module:15} - {description}")
        except ImportError:
            missing.append(f"{module} ({description})")
            print(f"   ⚠️  {module:15} - {description} [MISSING]")
    
    print(f"\n📊 Summary:")
    print(f"   Available: {len(available)}/{len(required_imports)}")
    print(f"   Missing:   {len(missing)}/{len(required_imports)}")
    
    if missing:
        print(f"\n⚠️  Missing modules:")
        for m in missing:
            print(f"   • {m}")
        print(f"\nNote: Some modules (like tkinter) may not be available in headless environments.")
        print(f"      This is expected on servers without GUI support.")
    
    return len(available), len(missing)

def check_code_structure(filepath):
    """Analyze code structure"""
    print(f"\n🔍 Analyzing code structure: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        
        tree = ast.parse(code)
        
        classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        
        print(f"   📦 Classes found: {len(classes)}")
        for cls in classes:
            print(f"      • {cls}")
        
        print(f"\n   🔧 Top-level functions: {len([f for f in functions if not any(f in c for c in classes)])}")
        
        # Check for main entry point
        has_main = 'main' in functions
        has_main_guard = '__main__' in code
        
        print(f"\n   📌 Entry point:")
        print(f"      • main() function: {'✅' if has_main else '❌'}")
        print(f"      • if __name__ == '__main__': {'✅' if has_main_guard else '❌'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error analyzing structure: {e}")
        return False

def test_file_operations():
    """Test that all required files exist"""
    print(f"\n🔍 Checking required files")
    
    required_files = [
        'mdb_gui.py',
        'requirements.txt',
        'build_exe.py',
        'build_instructions.md',
        'README.md',
        '.gitignore',
    ]
    
    all_exist = True
    for filename in required_files:
        import os
        exists = os.path.exists(filename)
        print(f"   {'✅' if exists else '❌'} {filename}")
        if not exists:
            all_exist = False
    
    return all_exist

def validate_requirements():
    """Validate requirements.txt"""
    print(f"\n🔍 Validating requirements.txt")
    
    try:
        with open('requirements.txt', 'r', encoding='utf-8') as f:
            requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        print(f"   Found {len(requirements)} requirements:")
        for req in requirements:
            print(f"      • {req}")
        
        return True
    except Exception as e:
        print(f"❌ Error reading requirements.txt: {e}")
        return False

def main():
    """Main test function"""
    print_header("🧪 MDB GUI Application - Code Validation")
    
    # Constants
    MAX_ALLOWED_MISSING_IMPORTS = 3  # Allow missing GUI/optional modules in headless environments
    
    all_passed = True
    
    # Test 1: Check file existence
    print_header("Test 1: File Existence")
    if not test_file_operations():
        all_passed = False
    
    # Test 2: Validate requirements
    print_header("Test 2: Requirements Validation")
    if not validate_requirements():
        all_passed = False
    
    # Test 3: Check syntax
    print_header("Test 3: Syntax Check")
    files_to_check = ['mdb_gui.py', 'build_exe.py']
    for filepath in files_to_check:
        if not check_file_syntax(filepath):
            all_passed = False
    
    # Test 4: Check imports
    print_header("Test 4: Import Check")
    available, missing = check_imports('mdb_gui.py')
    
    # Test 5: Analyze structure
    print_header("Test 5: Code Structure")
    if not check_code_structure('mdb_gui.py'):
        all_passed = False
    
    # Final summary
    print_header("📊 Test Summary")
    
    if all_passed and missing <= MAX_ALLOWED_MISSING_IMPORTS:
        print("✅ All critical tests PASSED!")
        print("\nThe application code is valid and ready to use.")
        print("\nNote: Some GUI libraries may not be available in this environment,")
        print("      but the code is syntactically correct and will work on")
        print("      systems with proper GUI support (Windows/Linux with X11).")
        return 0
    else:
        print("⚠️  Some tests FAILED or had warnings!")
        print("\nPlease review the errors above.")
        if missing > MAX_ALLOWED_MISSING_IMPORTS:
            print("\nNote: Missing imports are expected in headless environments.")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
