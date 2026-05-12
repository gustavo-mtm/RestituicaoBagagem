from dynamsoft_barcode_reader_bundle.license import LicenseManager
import inspect

print("=" * 60)
print("MÉTODOS DO LicenseManager")
print("=" * 60)

# Listar todos os métodos
methods = [m for m in dir(LicenseManager) if not m.startswith('_') and callable(getattr(LicenseManager, m))]
for method in methods:
    try:
        sig = inspect.signature(getattr(LicenseManager, method))
        print(f"{method}{sig}")
    except:
        print(f"{method}")

print("\n" + "=" * 60)
print("ASSINATURA DO get_device_uuid")
print("=" * 60)

try:
    sig = inspect.signature(LicenseManager.get_device_uuid)
    print(f"Assinatura: {sig}")
    
    # Tenta descobrir quais são os enums disponíveis
    from dynamsoft_barcode_reader_bundle import license as lic
    print("\nEnums/Constantes no módulo license:")
    for name in dir(lic):
        if not name.startswith('_') and name[0].isupper():
            obj = getattr(lic, name)
            if not callable(obj) or (hasattr(obj, '__mro__') and 'Enum' in str(obj.__mro__)):
                print(f"  - {name}: {type(obj)}")
except Exception as e:
    print(f"Erro: {e}")
