import dynamsoft_barcode_reader_bundle as bundle
import inspect

print("=" * 60)
print("MÓDULOS DISPONÍVEIS NA BUNDLE")
print("=" * 60)

# Listar todos os atributos do módulo principal
for name in dir(bundle):
    if not name.startswith('_'):
        obj = getattr(bundle, name)
        tipo = type(obj).__name__
        if inspect.ismodule(obj):
            print(f"  {name:<40} (módulo)")

print("\n" + "=" * 60)
print("PROCURANDO POR LICENSA EM CADA MÓDULO")
print("=" * 60)

# Verificar core
try:
    from dynamsoft_barcode_reader_bundle import core
    print("\nMódulo CORE:")
    license_items = [name for name in dir(core) if 'license' in name.lower()]
    if license_items:
        for name in license_items:
            print(f"  {name}")
    else:
        print("  (nenhum item relacionado a license encontrado)")
except ImportError as e:
    print(f"  Erro importando core: {e}")

# Verificar cvr
try:
    from dynamsoft_barcode_reader_bundle import cvr
    print("\nMódulo CVR:")
    license_items = [name for name in dir(cvr) if 'license' in name.lower()]
    if license_items:
        for name in license_items:
            print(f"  {name}")
    else:
        print("  (nenhum item relacionado a license encontrado)")
except ImportError as e:
    print(f"  Erro importando cvr: {e}")

# Verificar dip
try:
    from dynamsoft_barcode_reader_bundle import dip
    print("\nMódulo DIP:")
    license_items = [name for name in dir(dip) if 'license' in name.lower()]
    if license_items:
        for name in license_items:
            print(f"  {name}")
    else:
        print("  (nenhum item relacionado a license encontrado)")
except ImportError as e:
    print(f"  Erro importando dip: {e}")

# Verificar dbr especificamente
try:
    from dynamsoft_barcode_reader_bundle import dbr
    print("\nMódulo DBR:")
    license_items = [name for name in dir(dbr) if 'license' in name.lower() or 'module' in name.lower()]
    if license_items:
        print("  Itens encontrados:")
        for name in license_items:
            print(f"    - {name}")
            obj = getattr(dbr, name)
            if inspect.isclass(obj):
                methods = [m for m in dir(obj) if not m.startswith('_') and callable(getattr(obj, m))]
                if methods:
                    print(f"      Métodos: {', '.join(methods[:5])}")
    else:
        print("  (nenhum item encontrado)")
        print("  BarcodeReaderModule disponível? ", hasattr(dbr, 'BarcodeReaderModule'))
except ImportError as e:
    print(f"  Erro importando dbr: {e}")
