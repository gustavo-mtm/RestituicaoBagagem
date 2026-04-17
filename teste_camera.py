import cv2
from ultralytics import YOLO

# Teste simples da câmera e detecção
print("Testando câmera...")
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("ERRO: Não conseguiu abrir a câmera!")
    exit()

print("Câmera OK. Testando modelo...")
model = YOLO('yolov8n.pt')

# Captura um frame
success, frame = cap.read()
if not success:
    print("ERRO: Não conseguiu capturar frame!")
    cap.release()
    exit()

print(f"Frame capturado: {frame.shape}")

# Faz detecção
results = model(frame, classes=[24, 28], verbose=True)  # backpack, suitcase
result = results[0]

if result.boxes is not None and len(result.boxes) > 0:
    print(f"SUCESSO: {len(result.boxes)} detecções encontradas!")
    for i, box in enumerate(result.boxes):
        cls = int(box.cls.item())
        conf = box.conf.item()
        print(f"  Detecção {i+1}: Classe {cls}, Confiança {conf:.2f}")
else:
    print("Nenhuma detecção encontrada no frame atual")

cap.release()
print("Teste concluído.")