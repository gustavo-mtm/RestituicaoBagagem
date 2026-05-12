"""
Script para verificar e instalar Dynamsoft corretamente
"""

import subprocess
import sys

print("=" * 70)
print("VERIFICAÇÃO E INSTALAÇÃO DO DYNAMSOFT")
print("=" * 70)

# 1. Verificar pip
print("\n1️⃣  Verificando pip...")
print(f"   Python: {sys.executable}")
print(f"   Versão: {sys.version}")

# 2. Listar pacotes instalados
print("\n2️⃣  Pacotes instalados (busca por 'dynamsoft'):")
resultado = subprocess.run([sys.executable, "-m", "pip", "list"], capture_output=True, text=True)
for linha in resultado.stdout.split('\n'):
    if 'dynamsoft' in linha.lower():
        print(f"   ✅ {linha}")

# 3. Tentar importar
print("\n3️⃣  Tentando importar Dynamsoft...")
try:
    import dynamsoft_barcode_reader
    print(f"   ✅ Importação bem-sucedida!")
    print(f"   Localização: {dynamsoft_barcode_reader.__file__}")
except ImportError as e:
    print(f"   ❌ Falha na importação: {e}")
    print(f"\n4️⃣  Instalando Dynamsoft...")
    print("   Aguarde, isso pode levar alguns minutos...")
    
    # Instala Dynamsoft
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "dynamsoft-barcode-reader-bundle"], check=False)
    
    # Tenta importar novamente
    print("\n5️⃣  Testando importação após instalação...")
    try:
        import dynamsoft_barcode_reader
        print(f"   ✅ Importação bem-sucedida!")
        print(f"   Localização: {dynamsoft_barcode_reader.__file__}")
    except ImportError as e:
        print(f"   ❌ Ainda falhando: {e}")

print("\n" + "=" * 70)
print("✅ Script concluído. Agora rode: python inicializar_sistema.py")
print("=" * 70)
