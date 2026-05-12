"""
Script de Diagnóstico - Verifica se tudo está instalado corretamente
"""

import sys
import os

print("=" * 70)
print("DIAGNÓSTICO DO SISTEMA")
print("=" * 70)

# 1. Verificar Python
print("\n1️⃣  PYTHON:")
print(f"   Versão: {sys.version}")
print(f"   Executável: {sys.executable}")
print(f"   Path: {sys.prefix}")

# 2. Verificar dependências
print("\n2️⃣  DEPENDÊNCIAS INSTALADAS:")

dependencias = [
    'cv2',
    'ultralytics',
    'torch',
    'dynamsoft_barcode_reader'
]

para_instalar = []

for dep in dependencias:
    try:
        __import__(dep)
        print(f"   ✅ {dep}")
    except ImportError:
        print(f"   ❌ {dep} - FALTA INSTALAR!")
        para_instalar.append(dep)

# 3. Sugestões
if para_instalar:
    print("\n3️⃣  FALTAM INSTALAR:")
    for dep in para_instalar:
        if dep == 'dynamsoft_barcode_reader':
            print(f"   pip install dynamsoft-barcode-reader-bundle")
        else:
            print(f"   pip install {dep}")
else:
    print("\n3️⃣  ✅ TUDO INSTALADO!")

# 4. Verificar estrutura de pastas
print("\n4️⃣  ESTRUTURA DE PASTAS:")
pastas = [
    'src',
    'src/modules',
    'data',
    'docs'
]

for pasta in pastas:
    if os.path.exists(pasta):
        print(f"   ✅ {pasta}")
    else:
        print(f"   ❌ {pasta} - FALTA!")

# 5. Verificar arquivos importantes
print("\n5️⃣  ARQUIVOS IMPORTANTES:")
arquivos = [
    'src/main.py',
    'src/modules/deteccao.py',
    'src/modules/leitor_dinamsoft.py',
    'src/modules/config_license.py',
]

for arquivo in arquivos:
    if os.path.exists(arquivo):
        print(f"   ✅ {arquivo}")
    else:
        print(f"   ❌ {arquivo} - FALTA!")

print("\n" + "=" * 70)

if not para_instalar:
    print("✅ SISTEMA PRONTO! Execute: python inicializar_sistema.py")
else:
    print("❌ INSTALE AS DEPENDÊNCIAS ACIMA")

print("=" * 70)
