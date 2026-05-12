from dynamsoft_barcode_reader_bundle import license as lic
import inspect

print("=" * 60)
print("ESTRUTURA DO MÓDULO LICENSE")
print("=" * 60)

# Listar todos os atributos do módulo license
print("\nTodos os atributos/classes/funções disponíveis:")
for name in dir(lic):
    if not name.startswith('_'):
        obj = getattr(lic, name)
        tipo = type(obj).__name__
        print(f"  {name:<40} ({tipo})")

print("\n" + "=" * 60)
print("PROCURANDO POR MÉTODOS DE INICIALIZAÇÃO")
print("=" * 60)

license_classes = [name for name in dir(lic) if not name.startswith('_') and name[0].isupper()]
for name in license_classes:
    obj = getattr(lic, name)
    if inspect.isclass(obj):
        print(f"\n{name}:")
        methods = [m for m in dir(obj) if not m.startswith('_') and callable(getattr(obj, m))]
        for method in methods:
            print(f"  - {method}")

print("\n" + "=" * 60)
print("EXEMPLO DE USO")
print("=" * 60)

# Se encontrar LicenseManager, tentar obter assinatura
if hasattr(lic, 'LicenseManager'):
    print("\nLicenseManager encontrado!")
    print("Assinatura do __init__:")
    try:
        sig = inspect.signature(lic.LicenseManager.__init__)
        print(f"  {sig}")
    except:
        print("  (não foi possível obter assinatura)")
        
    print("\nAssinatura do init_license:")
    try:
        sig = inspect.signature(lic.LicenseManager.init_license)
        print(f"  {sig}")
    except:
        print("  (não foi possível obter assinatura)")
