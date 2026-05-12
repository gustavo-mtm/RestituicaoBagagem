"""
Script para descobrir a estrutura correta do pacote Dynamsoft
"""

import sys
import os

print("=" * 70)
print("DESCOBRINDO ESTRUTURA DO DYNAMSOFT")
print("=" * 70)

# 1. Encontrar onde está instalado
print("\n1️⃣  Procurando pacote Dynamsoft...")
site_packages = None
for path in sys.path:
    if 'site-packages' in path and os.path.exists(path):
        site_packages = path
        break

if site_packages:
    print(f"   Site-packages: {site_packages}")
    
    # 2. Listar pastas no site-packages que contêm 'dynamsoft'
    print("\n2️⃣  Pastas relacionadas a Dynamsoft:")
    for item in os.listdir(site_packages):
        if 'dynamsoft' in item.lower():
            full_path = os.path.join(site_packages, item)
            print(f"   📁 {item}")
            
            # Se for pasta, listar conteúdo
            if os.path.isdir(full_path):
                print(f"      Conteúdo:")
                try:
                    for subitem in os.listdir(full_path)[:10]:  # Primeiros 10
                        sub_path = os.path.join(full_path, subitem)
                        if os.path.isdir(sub_path):
                            print(f"      📁 {subitem}/")
                        else:
                            print(f"      📄 {subitem}")
                except:
                    pass

# 3. Tentar diferentes imports
print("\n3️⃣  Tentando diferentes imports:")

imports_para_testar = [
    "dynamsoft_barcode_reader",
    "dynamsoft",
    "dynamsoft.barcode_reader",
    "dbr",
    "DynamsoftBarcodeReader"
]

for imp in imports_para_testar:
    try:
        modulo = __import__(imp)
        print(f"   ✅ '{imp}' - FUNCIONA!")
        print(f"      Localização: {modulo.__file__}")
    except ImportError:
        print(f"   ❌ '{imp}' - Falhando")

print("\n" + "=" * 70)
