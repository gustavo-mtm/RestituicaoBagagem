from dynamsoft_barcode_reader_bundle.cvr import CaptureVisionRouter
from dynamsoft_barcode_reader_bundle.license import LicenseManager
import os

DYNAMSOFT_LICENSE_KEY = "t0087YQEAAC4kh7o/+r9Os+g37yHpw5qCttXSB6fqBjaiN5qkL8fLcJPwzDXwE6uCxvW8DL2+ynwB7cTJHhaej2hvh1N5Hxj1B9M/mtxN5b1ZUpMpvQHdc0mk"

# Inicializa licença
error_code, error_msg = LicenseManager.init_license(DYNAMSOFT_LICENSE_KEY)

# Cria router com formato PADRÃO (detecta TUDO)
router = CaptureVisionRouter()

print("=" * 70)
print("EXPLORAR ATRIBUTOS DE BarcodeResultItem")
print("=" * 70)

# Testa com formato "0" (tenta detectar TUDO)
error_code, error_msg, settings = router.get_simplified_settings("ReadBarcodes_Default")
settings.barcode_settings.barcode_format_ids = 0  # Tenta TODOS os formatos
error_code, error_msg = router.update_settings("ReadBarcodes_Default", settings)

test_paths = [
    "data/raw",
    "data/",
]

found_images = []
for path in test_paths:
    if os.path.isdir(path):
        for file in os.listdir(path):
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                full_path = os.path.join(path, file)
                found_images.append(full_path)

print(f"\n🔍 Procurando barcodes em {len(found_images)} imagem(ns)...\n")

encontrou_barcode = False
for img_path in found_images:
    if encontrou_barcode:
        break
        
    try:
        result = router.capture(img_path, "ReadBarcodes_Default")
        barcode_result = result.get_decoded_barcodes_result()
        
        if barcode_result:
            items = barcode_result.get_items()
            if items:
                print(f"✅ Encontrados {len(items)} barcode(s) em: {img_path}\n")
                
                # Analisa o PRIMEIRO item
                item = items[0]
                encontrou_barcode = True
                
                print(f"Tipo do item: {type(item)}")
                print(f"\n{'='*70}")
                print("TODOS OS ATRIBUTOS DISPONÍVEIS:")
                print(f"{'='*70}\n")
                
                attributes = dir(item)
                
                for attr in attributes:
                    if not attr.startswith('_'):
                        try:
                            value = getattr(item, attr)
                            
                            # Se for callable (método), pule
                            if callable(value):
                                print(f"  {attr:<40} → [método]")
                            else:
                                # Se for muito longo, trunca
                                value_str = str(value)
                                if len(value_str) > 60:
                                    value_str = value_str[:57] + "..."
                                
                                print(f"  {attr:<40} → {value_str}")
                        except Exception as e:
                            print(f"  {attr:<40} → [Erro: {type(e).__name__}]")
                
                print(f"\n{'='*70}")
                print("ATRIBUTOS PRINCIPAIS PARA USAR:")
                print(f"{'='*70}\n")
                
                # Testa os atributos mais comuns
                atributos_comuns = [
                    'barcode_text',
                    'text', 
                    'barcode_format_string',
                    'format_string',
                    'confidence',
                    'barcode_format',
                    'details'
                ]
                
                for attr in atributos_comuns:
                    try:
                        value = getattr(item, attr)
                        if not callable(value):
                            print(f"✅ {attr:<35} = {str(value)[:40]}")
                    except AttributeError:
                        print(f"❌ {attr:<35} (não existe)")
                
    except Exception as e:
        print(f"❌ Erro ao processar {img_path}: {e}\n")

if not encontrou_barcode:
    print("""
⚠️  Nenhum barcode foi detectado nas imagens.

Para testar os atributos, você precisa:
1. De uma imagem com código de barras legível, OU
2. Usar a câmera ao vivo:
   
   python src/main.py
   
   (Aponte para um código de barras real)
""")
