from dynamsoft_barcode_reader_bundle import dbr
import inspect

print("=" * 60)
print("ESTRUTURA DO MÓDULO DBR")
print("=" * 60)

# Listar todos os atributos do módulo dbr
print("\nTodos os atributos/classes/funções disponíveis em dbr:")
for name in dir(dbr):
    if not name.startswith('_'):
        obj = getattr(dbr, name)
        tipo = type(obj).__name__
        print(f"  {name:<40} ({tipo})")

print("\n" + "=" * 60)
print("PROCURANDO POR CLASSES RELACIONADAS A LICENÇA")
print("=" * 60)

license_related = [name for name in dir(dbr) if 'license' in name.lower() or 'license' in name.lower()]
for name in license_related:
    print(f"\n{name}:")
    obj = getattr(dbr, name)
    if inspect.isclass(obj):
        print(f"  Classe com métodos:")
        for method in dir(obj):
            if not method.startswith('_'):
                print(f"    - {method}")

print("\n" + "=" * 60)
print("PROCURANDO POR ENUMS")
print("=" * 60)

enums = [name for name in dir(dbr) if 'enum' in name.lower() or 'error' in name.lower()]
for name in enums:
    print(f"\n{name}")
