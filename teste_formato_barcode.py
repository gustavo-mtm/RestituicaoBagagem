from dynamsoft_barcode_reader_bundle.cvr import CaptureVisionRouter
from dynamsoft_barcode_reader_bundle.license import LicenseManager
from dynamsoft_barcode_reader_bundle.dbr import EnumErrorCode

# Chave de licença
DYNAMSOFT_LICENSE_KEY = "t0087YQEAAC4kh7o/+r9Os+g37yHpw5qCttXSB6fqBjaiN5qkL8fLcJPwzDXwE6uCxvW8DL2+ynwB7cTJHhaej2hvh1N5Hxj1B9M/mtxN5b1ZUpMpvQHdc0mk"

# Inicializa licença
error_code, error_msg = LicenseManager.init_license(DYNAMSOFT_LICENSE_KEY)
print(f"Licença: {error_code} - {error_msg}\n")

# Cria router
router = CaptureVisionRouter()

print("=" * 70)
print("TESTE 1: DETECTAR SEM RESTRIÇÃO DE FORMATO (DEFAULT)")
print("=" * 70)

try:
    error_code, error_msg, settings = router.get_simplified_settings("ReadBarcodes_Default")
    print(f"Status: {error_code}")
    print(f"Barcode Format IDs antes: {settings.barcode_settings.barcode_format_ids}")
    
    # Não muda nada - usa configuração padrão
    error_code, error_msg = router.update_settings("ReadBarcodes_Default", settings)
    print(f"Update status: {error_code}\n")
    
except Exception as e:
    print(f"Erro: {e}\n")

print("=" * 70)
print("TESTE 2: VALORES DE barcode_format_ids POSSÍVEIS")
print("=" * 70)

# Tenta descobrir quais são os valores válidos
try:
    from dynamsoft_barcode_reader_bundle.dbr import EnumBarcodeFormat
    
    print("Valores de formato disponíveis:")
    for name in dir(EnumBarcodeFormat):
        if not name.startswith('_'):
            value = getattr(EnumBarcodeFormat, name)
            if isinstance(value, int):
                print(f"  {name:<40} = {value:15} (0x{value:X})")
except Exception as e:
    print(f"Erro ao listar formatos: {e}\n")

print("\n" + "=" * 70)
print("TESTE 3: TESTAR COM DIFERENTES CONFIGURAÇÕES")
print("=" * 70)

configs_to_test = [
    ("Padrão (0)", 0),
    ("ITF apenas (0x8)", 0x8),
    ("ITF + CODE_128 (0x8 | 0x80)", 0x8 | 0x80),
    ("Todos exceto ITF", 0xFFFFFFF7),  # Máximo menos ITF
]

for descr, value in configs_to_test:
    print(f"\n🧪 {descr}:")
    try:
        error_code, error_msg, settings = router.get_simplified_settings("ReadBarcodes_Default")
        settings.barcode_settings.barcode_format_ids = value
        error_code, error_msg = router.update_settings("ReadBarcodes_Default", settings)
        
        # Verifica se foi atualizado
        error_code, error_msg, settings_check = router.get_simplified_settings("ReadBarcodes_Default")
        print(f"   Valor configurado: {settings_check.barcode_settings.barcode_format_ids}")
        print(f"   Status: {'✅ OK' if settings_check.barcode_settings.barcode_format_ids == value else '⚠️ Diferente'}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")

print("\n" + "=" * 70)
print("RESUMO")
print("=" * 70)
print("""
Possibilidades:
1. barcode_format_ids = 0 → Tenta detectar TODOS os formatos
2. barcode_format_ids = 0x8 → ITF apenas
3. A configuração talvez esteja sendo aplicada mas o leitor não está achando ITF
4. Pode ser que a câmera/imagem não tenha código de barras ITF válido
""")
