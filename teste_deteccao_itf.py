from src.modules.leitor_dinamsoft import LeitorDynamsoft
import os

print("=" * 70)
print("TESTE DE DETECÇÃO DE CÓDIGO DE BARRAS ITF")
print("=" * 70)

try:
    # Inicializa o leitor
    leitor = LeitorDynamsoft()
    print("\n✅ Leitor inicializado com sucesso!\n")
    
    # Tenta encontrar imagens de teste
    test_paths = [
        "data/raw",
        "data/",
        "teste_imagem.jpg",
        "barcode.jpg",
        "test.jpg"
    ]
    
    print("🔍 Procurando imagens para testar...\n")
    
    found_images = []
    for path in test_paths:
        if os.path.isdir(path):
            for file in os.listdir(path):
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                    full_path = os.path.join(path, file)
                    found_images.append(full_path)
        elif os.path.isfile(path):
            found_images.append(path)
    
    if found_images:
        print(f"📸 Encontradas {len(found_images)} imagem(ns):\n")
        for img_path in found_images[:5]:  # Máximo 5 imagens
            print(f"\n{'='*70}")
            print(f"📷 Testando: {img_path}")
            print(f"{'='*70}\n")
            
            resultados = leitor.detectar_em_imagem(img_path)
            
            if resultados:
                print(f"\n✅ SUCESSO! Detectados {len(resultados)} código(s):")
                for i, codigo in enumerate(resultados, 1):
                    print(f"\n   Código #{i}:")
                    print(f"   • Valor: {codigo['valor']}")
                    print(f"   • Tipo: {codigo['tipo']}")
                    print(f"   • Confiança: {codigo['confianca']}")
            else:
                print(f"\nℹ️  Nenhum código ITF detectado nesta imagem")
    else:
        print("\n⚠️  Nenhuma imagem encontrada para teste!")
        print("\nPara testar com câmera ao vivo, execute:")
        print("   python src/main.py")

except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
