from dynamsoft_barcode_reader_bundle.cvr import CaptureVisionRouter
from dynamsoft_barcode_reader_bundle.license import LicenseManager
import os

DYNAMSOFT_LICENSE_KEY = "t0087YQEAAC4kh7o/+r9Os+g37yHpw5qCttXSB6fqBjaiN5qkL8fLcJPwzDXwE6uCxvW8DL2+ynwB7cTJHhaej2hvh1N5Hxj1B9M/mtxN5b1ZUpMpvQHdc0mk"

# Inicializa licença
error_code, error_msg = LicenseManager.init_license(DYNAMSOFT_LICENSE_KEY)

# Cria router
router = CaptureVisionRouter()

print("=" * 70)
print("TESTE: DETECTAR QUALQUER FORMATO DE BARCODE (NÃO APENAS ITF)")
print("=" * 70)

# Testa com formato "0" (tenta detectar TUDO)
error_code, error_msg, settings = router.get_simplified_settings("ReadBarcodes_Default")
settings.barcode_settings.barcode_format_ids = 0  # Tenta TODOS os formatos
error_code, error_msg = router.update_settings("ReadBarcodes_Default", settings)

print("\n✅ Configurado para: TODOS OS FORMATOS")
print("(Incluindo: CODE_39, CODE_128, QR, PDF417, EAN, ITF, etc)\n")

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

print(f"🔍 Testando {len(found_images)} imagem(ns)...\n")

total_detectados = 0
for img_path in found_images[:5]:  # Máximo 5
    try:
        result = router.capture(img_path, "ReadBarcodes_Default")
        barcode_result = result.get_decoded_barcodes_result()
        
        if barcode_result:
            items = barcode_result.get_items()
            if items:
                total_detectados += len(items)
                print(f"\n✅ {img_path}")
                for i, item in enumerate(items, 1):
                    barcode_text = item.get_text()
                    barcode_format = item.get_format_string()
                    print(f"   Código #{i}: {barcode_text} ({barcode_format})")
            else:
                print(f"❌ {img_path} - Nenhum código detectado")
        else:
            print(f"❌ {img_path} - Nenhum código detectado")
    except Exception as e:
        print(f"❌ {img_path} - Erro: {e}")

print(f"\n{'='*70}")
print(f"TOTAL: {total_detectados} código(s) detectado(s)")
print(f"{'='*70}")

if total_detectados == 0:
    print("""
⚠️  ANÁLISE:
    
Nenhum código de barras foi detectado EM NENHUM formato.
Possíveis causas:

1. Imagens não contêm código de barras legível
   → Verifique qualidade, foco, angulação
   
2. Código está distante/pequeno
   → Tente aproximar/fotografar melhor
   
3. Código com baixo contraste
   → Melhor iluminação pode ajudar
   
4. Tipo de código não suportado
   → Verifique se é um formato conhecido
   
5. Câmera pixelada/desfocada
   → Limpe a lente, use iluminação melhor

PRÓXIMOS PASSOS:
✓ Teste com uma imagem de código de barras conhecido
✓ Use um código ITF/CODE_128 de alta qualidade
✓ Verifique a qualidade das imagens de bagagem

ALTERNATIVA: Teste em tempo real com câmera
$ python src/main.py
""")
else:
    print(f"\n✅ Leitor Dynamsoft está funcionando corretamente!")
    print(f"   Foram detectados códigos em múltiplos formatos.")
