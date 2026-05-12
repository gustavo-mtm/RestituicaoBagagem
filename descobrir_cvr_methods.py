from dynamsoft_barcode_reader_bundle.cvr import CaptureVisionRouter
import inspect

print("=" * 60)
print("MÉTODOS DO CAPTUREVISIONROUTER")
print("=" * 60)

router = CaptureVisionRouter()

# Listar todos os métodos
print("\nMétodos disponíveis:")
methods = [m for m in dir(router) if not m.startswith('_') and callable(getattr(router, m))]
for method in methods:
    print(f"  - {method}")

print("\n" + "=" * 60)
print("PROCURANDO MÉTODOS DE CONFIGURAÇÃO")
print("=" * 60)

config_methods = [m for m in methods if 'setting' in m.lower() or 'config' in m.lower() or 'runtime' in m.lower()]
if config_methods:
    print("\nMétodos relacionados a configuração:")
    for method in config_methods:
        try:
            sig = inspect.signature(getattr(router, method))
            print(f"  {method}{sig}")
        except:
            print(f"  {method}")
else:
    print("\nNenhum método de configuração encontrado")

print("\n" + "=" * 60)
print("PROCURANDO MÉTODOS DE TEMPLATE/PRESET")
print("=" * 60)

template_methods = [m for m in methods if 'template' in m.lower() or 'preset' in m.lower()]
if template_methods:
    print("\nMétodos relacionados a template/preset:")
    for method in template_methods:
        try:
            sig = inspect.signature(getattr(router, method))
            print(f"  {method}{sig}")
        except:
            print(f"  {method}")
else:
    print("\nNenhum método de template encontrado")
