from dynamsoft_barcode_reader_bundle.cvr import CaptureVisionRouter
from dynamsoft_barcode_reader_bundle.license import LicenseManager
import inspect

DYNAMSOFT_LICENSE_KEY = "t0087YQEAAC4kh7o/+r9Os+g37yHpw5qCttXSB6fqBjaiN5qkL8fLcJPwzDXwE6uCxvW8DL2+ynwB7cTJHhaej2hvh1N5Hxj1B9M/mtxN5b1ZUpMpvQHdc0mk"

# Inicializa licença
error_code, error_msg = LicenseManager.init_license(DYNAMSOFT_LICENSE_KEY)

# Cria router
router = CaptureVisionRouter()

print("=" * 70)
print("EXPLORAR CLASSE DecodedBarcodesResult")
print("=" * 70)

# Tenta importar a classe diretamente
try:
    from dynamsoft_barcode_reader_bundle.dbr import DecodedBarcodesResult
    
    print(f"\nClasse encontrada: {DecodedBarcodesResult}")
    print(f"\nAtributos da classe:")
    
    attrs = [attr for attr in dir(DecodedBarcodesResult) if not attr.startswith('_')]
    for attr in attrs:
        try:
            val = getattr(DecodedBarcodesResult, attr)
            if callable(val):
                # Tenta obter a assinatura
                try:
                    sig = inspect.signature(val)
                    print(f"  {attr}{sig}")
                except:
                    print(f"  {attr}() - método")
            else:
                print(f"  {attr} = {val}")
        except:
            print(f"  {attr}")
            
except ImportError as e:
    print(f"Erro ao importar DecodedBarcodesResult: {e}")

print("\n" + "=" * 70)
print("EXPLORAR OBJETO CapturedResult")
print("=" * 70)

try:
    from dynamsoft_barcode_reader_bundle.cvr import CapturedResult
    
    print(f"\nClasse encontrada: {CapturedResult}")
    print(f"\nMétodos disponíveis:")
    
    methods = [m for m in dir(CapturedResult) if not m.startswith('_') and callable(getattr(CapturedResult, m, None))]
    for method in methods:
        if 'barcode' in method.lower():
            print(f"  - {method} 🎯 {inspect.signature(getattr(CapturedResult, method))}")
        else:
            print(f"  - {method}")
            
except ImportError as e:
    print(f"Erro: {e}")

print("\n" + "=" * 70)
print("VER DOCUMENTAÇÃO DO SDK")
print("=" * 70)

print("""
Alternativas conhecidas para acessar barcodes:
1. result.get_barcode_result_items()  (retorna lista)
2. barcode_result == None (sem detecções)
3. barcode_result.barcode_result_items (atributo direto)
4. len(barcode_result) (se suporta __len__)
5. barcode_result[0] (se suporta __getitem__)
""")
