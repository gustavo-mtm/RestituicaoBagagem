from dynamsoft_barcode_reader_bundle.cvr import CaptureVisionRouter
from dynamsoft_barcode_reader_bundle.license import LicenseManager
import numpy as np

DYNAMSOFT_LICENSE_KEY = "t0087YQEAAC4kh7o/+r9Os+g37yHpw5qCttXSB6fqBjaiN5qkL8fLcJPwzDXwE6uCxvW8DL2+ynwB7cTJHhaej2hvh1N5Hxj1B9M/mtxN5b1ZUpMpvQHdc0mk"

# Inicializa licença
error_code, error_msg = LicenseManager.init_license(DYNAMSOFT_LICENSE_KEY)

# Cria router
router = CaptureVisionRouter()

print("=" * 70)
print("DESCOBRIR ESTRUTURA DE DecodedBarcodesResult")
print("=" * 70)

# Cria um frame de teste vazio
test_frame = np.zeros((480, 640, 3), dtype=np.uint8)

# Captura do frame vazio (mesmo que não tenha barcodes)
result = router.capture(test_frame, "ReadBarcodes_Default")
barcode_result = result.get_decoded_barcodes_result()

print(f"\nTipo de barcode_result: {type(barcode_result)}")
print(f"barcode_result é None? {barcode_result is None}")

if barcode_result is not None:
    print(f"\n🔍 ATRIBUTOS de DecodedBarcodesResult:")
    print(f"Atributos disponíveis:")
    
    attrs = [attr for attr in dir(barcode_result) if not attr.startswith('_')]
    for attr in attrs:
        try:
            value = getattr(barcode_result, attr)
            if not callable(value):
                print(f"  {attr:<35} = {type(value).__name__:<30} | {str(value)[:40]}")
            else:
                print(f"  {attr:<35} (método/função)")
        except:
            print(f"  {attr:<35} (erro ao acessar)")
    
    print(f"\n🔍 MÉTODOS de DecodedBarcodesResult:")
    methods = [attr for attr in attrs if callable(getattr(barcode_result, attr))]
    for method in methods:
        if not method.startswith('_'):
            print(f"  - {method}")
    
    print("\n" + "=" * 70)
    print("TESTANDO FORMA CORRETA DE ACESSAR OS BARCODES")
    print("=" * 70)
    
    # Tenta diferentes formas
    tentativas = [
        ("barcode_result.items", lambda: barcode_result.items),
        ("barcode_result.barcode_result_items", lambda: barcode_result.barcode_result_items),
        ("barcode_result.get_items()", lambda: barcode_result.get_items() if hasattr(barcode_result, 'get_items') else None),
        ("len(barcode_result)", lambda: len(barcode_result) if hasattr(barcode_result, '__len__') else None),
        ("barcode_result[0]", lambda: barcode_result[0] if hasattr(barcode_result, '__getitem__') else None),
    ]
    
    for descr, func in tentativas:
        try:
            valor = func()
            print(f"\n✅ {descr}")
            print(f"   Tipo: {type(valor)}")
            print(f"   Valor: {valor}")
            if isinstance(valor, (list, tuple)):
                print(f"   Tamanho: {len(valor)}")
        except AttributeError as e:
            print(f"\n❌ {descr}")
            print(f"   Erro: {e}")
        except Exception as e:
            print(f"\n⚠️  {descr}")
            print(f"   Erro: {type(e).__name__}: {e}")
