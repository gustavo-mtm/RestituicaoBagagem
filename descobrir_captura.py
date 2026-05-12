from dynamsoft_barcode_reader_bundle.cvr import CaptureVisionRouter
import inspect

print("=" * 60)
print("MÉTODOS DE CAPTURA DO CAPTUREVISIONROUTER")
print("=" * 60)

router = CaptureVisionRouter()

# Métodos que começam com 'capture'
methods = [m for m in dir(router) if 'capture' in m.lower() and not m.startswith('_')]
for method in methods:
    try:
        sig = inspect.signature(getattr(router, method))
        print(f"\n{method}{sig}")
        
        # Mostra a documentação se disponível
        doc = getattr(router, method).__doc__
        if doc:
            lines = doc.strip().split('\n')
            for line in lines[:3]:  # Primeiras 3 linhas
                print(f"  {line.strip()}")
    except:
        print(f"\n{method}")

print("\n" + "=" * 60)
print("TESTANDO CAPTURA DE ARQUIVO DE TESTE")
print("=" * 60)

# Tenta capturar de um arquivo para ver o resultado
try:
    # Primeiro, vamos ver se conseguimos usar um template default
    result = router.capture("test.jpg", "ReadBarcodes_Default")
    print(f"Tipo do resultado: {type(result)}")
    print(f"Métodos do resultado: {[m for m in dir(result) if not m.startswith('_')][:10]}")
except Exception as e:
    print(f"Erro ao capturar: {e}")
    print("Tipos de erro - pode ser esperado se o arquivo não existir")
