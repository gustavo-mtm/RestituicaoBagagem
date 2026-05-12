from dynamsoft_barcode_reader_bundle.cvr import CaptureVisionRouter
from dynamsoft_barcode_reader_bundle.dbr import SimplifiedBarcodeReaderSettings

print("=" * 60)
print("PROPRIEDADES DO SimplifiedBarcodeReaderSettings")
print("=" * 60)

router = CaptureVisionRouter()
error_code, error_msg, settings = router.get_simplified_settings('read_barcodes')

barcode_settings = settings.barcode_settings

print(f"\nTipo: {type(barcode_settings)}")
print(f"Atributos/Propriedades disponíveis:")

for attr in dir(barcode_settings):
    if not attr.startswith('_'):
        try:
            value = getattr(barcode_settings, attr)
            if not callable(value):
                tipo = type(value).__name__
                value_str = str(value)
                if len(value_str) > 50:
                    value_str = value_str[:50] + "..."
                print(f"  {attr:<40} ({tipo:<20}) = {value_str}")
        except Exception as e:
            print(f"  {attr:<40} (erro: {str(e)[:20]})")

print("\n" + "=" * 60)
print("TESTANDO ATUALIZAÇÃO DE BARCODE_FORMATS")
print("=" * 60)

try:
    barcode_settings.barcode_formats = 0x8  # ITF
    print("✅ barcode_formats pode ser atualizado!")
    print(f"   Novo valor: {barcode_settings.barcode_formats}")
except Exception as e:
    print(f"❌ Erro ao atualizar barcode_formats: {e}")
