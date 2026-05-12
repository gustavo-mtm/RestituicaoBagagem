from dynamsoft_barcode_reader_bundle.cvr import CaptureVisionRouter, SimplifiedCaptureVisionSettings
import inspect

print("=" * 60)
print("PROPRIEDADES DO SimplifiedCaptureVisionSettings")
print("=" * 60)

router = CaptureVisionRouter()
error_code, error_msg, settings = router.get_simplified_settings('read_barcodes')

print(f"\nTipo: {type(settings)}")
print(f"Atributos/Propriedades disponíveis:")

for attr in dir(settings):
    if not attr.startswith('_'):
        try:
            value = getattr(settings, attr)
            tipo = type(value).__name__
            print(f"  {attr:<40} ({tipo}) = {str(value)[:50]}")
        except:
            print(f"  {attr}")

print("\n" + "=" * 60)
print("TEMPLATES DISPONÍVEIS")
print("=" * 60)

template_count = router.get_parameter_template_count()
print(f"\nTotal de templates: {template_count}")

for i in range(template_count):
    error_code, template_name = router.get_parameter_template_name(i)
    print(f"  {i}: {template_name}")
