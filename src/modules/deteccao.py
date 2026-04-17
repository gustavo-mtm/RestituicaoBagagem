import cv2
import os
from datetime import datetime
from ultralytics import YOLO

class DetectorBagagem:
    def __init__(self):
        self.model = YOLO('yolov8n.pt')
        self.classes_interesse = [24, 28]

    def detectar(self, frame):
        # Lembre-se de usar .track para o ID funcionar no main.py
        results = self.model.track(frame, persist=True, classes=self.classes_interesse, verbose=False)
        return results[0]

    def salvar_snapshot(self, frame, resultado):
        # 1. Garante que a pasta existe
        output_dir = "data/raw"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 2. Gera nome único com timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"bagagem_{timestamp}.jpg"
        filepath = os.path.join(output_dir, filename)

        # 3. Salva a imagem no disco
        success = cv2.imwrite(filepath, frame)
        if success:
            print(f"DEBUG: Foto salva com sucesso em {filepath}")
        else:
            print(f"DEBUG: ERRO ao salvar foto em {filepath}")
        
        return filepath