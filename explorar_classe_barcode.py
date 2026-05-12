from dynamsoft_barcode_reader_bundle.dbr import BarcodeResultItem
import inspect

print("=" * 70)
print("ESTRUTURA DA CLASSE BarcodeResultItem")
print("=" * 70)

print(f"\nClasse: {BarcodeResultItem}")
print(f"\nAtributos e Métodos disponíveis:")

attributes = dir(BarcodeResultItem)
properties = []
methods = []

for attr in attributes:
    if not attr.startswith('_'):
        obj = getattr(BarcodeResultItem, attr, None)
        
        if isinstance(obj, property):
            properties.append(attr)
        elif callable(obj):
            methods.append(attr)

print(f"\n📋 PROPRIEDADES (Leitura de dados):")
for prop in properties:
    print(f"  ✓ {prop}")

print(f"\n⚙️  MÉTODOS:")
for method in methods:
    try:
        sig = inspect.signature(getattr(BarcodeResultItem, method))
        print(f"  → {method}{sig}")
    except:
        print(f"  → {method}()")

print("\n" + "=" * 70)
print("PROPRIEDADES PROVAVELMENTE ÚTEIS:")
print("=" * 70)

# Lista das propriedades mais relevantes
propriedades_uteis = [
    'barcode_text',
    'text',
    'barcode_format',
    'barcode_format_string', 
    'format_string',
    'confidence',
    'angle',
    'module_size',
    'details',
    'extended_result_array',
    'bytes'
]

print("\nVerificando propriedades comuns:")
for prop in propriedades_uteis:
    if prop in properties:
        print(f"  ✅ {prop:<40} (DISPONÍVEL)")
    else:
        print(f"  ❌ {prop:<40} (não disponível)")

print("\n" + "=" * 70)
print("RESPOSTA À SUA PERGUNTA:")
print("=" * 70)

print("""
Para testar SEM passar atributo específico, use:

# Opção 1: Iterar WITHOUT acessar atributos
for item in items:
    print(f"Item detectado: {item}")

# Opção 2: Usar str() ou repr()
print(f"Item: {str(item)}")

# Opção 3: Listar todos os atributos dinamicamente
for attr in dir(item):
    if not attr.startswith('_'):
        try:
            print(f"{attr}: {getattr(item, attr)}")
        except:
            pass

# Opção 4: Apenas contar detecções
print(f"Total de barcodes: {len(items)}")
""")
