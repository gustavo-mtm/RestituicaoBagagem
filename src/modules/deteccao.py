import cv2
import os
from datetime import datetime
from ultralytics import YOLO


class DetectorBagagem:
    def __init__(self):
        self.model = YOLO('yolov8n.pt')
        self.classes_interesse = [24, 28]

        # Detector de código de barras do OpenCV
        self.barcode_detector = cv2.barcode.BarcodeDetector()

    def detectar(self, frame):
        results = self.model.track(
            frame,
            persist=True,
            classes=self.classes_interesse,
            verbose=False
        )
        return results[0]

    def salvar_snapshot(self, frame, resultado):
        output_dir = "data/raw"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"bagagem_{timestamp}.jpg"
        filepath = os.path.join(output_dir, filename)

        success = cv2.imwrite(filepath, frame)
        if success:
            print(f"DEBUG: Foto salva com sucesso em {filepath}")
        else:
            print(f"DEBUG: ERRO ao salvar foto em {filepath}")

        return filepath

    def detectar_codigo_barras(self, caminho_imagem):
        img = cv2.imread(caminho_imagem)

        if img is None:
            print("DEBUG: Erro ao abrir imagem para leitura de código de barras.")
            return []

        try:
            ok, decoded_info, decoded_type, points = self.barcode_detector.detectAndDecodeWithType(img)
        except Exception as e:
            print(f"DEBUG: Erro no detector de código de barras: {e}")
            return []

        resultados = []

        if ok and decoded_info:
            print("DEBUG: Código(s) de barras encontrado(s).")

            if points is not None:
                for i, texto in enumerate(decoded_info):
                    tipo = decoded_type[i] if i < len(decoded_type) else "desconhecido"

                    resultados.append({
                        "valor": texto,
                        "tipo": tipo
                    })

                # desenha os contornos
                for barcode in points:
                    pts = barcode.reshape(-1, 2).astype(int)

                    for j in range(len(pts)):
                        p1 = tuple(pts[j])
                        p2 = tuple(pts[(j + 1) % len(pts)])
                        cv2.line(img, p1, p2, (0, 255, 0), 2)

                # salva imagem anotada
                output_dir = "data/processed"
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                nome_saida = os.path.basename(caminho_imagem).replace(".jpg", "_barcode.jpg")
                caminho_saida = os.path.join(output_dir, nome_saida)
                cv2.imwrite(caminho_saida, img)

                print(f"DEBUG: Imagem anotada salva em {caminho_saida}")

            for item in resultados:
                print(f"DEBUG: Tipo: {item['tipo']} | Valor: {item['valor']}")

        else:
            print("DEBUG: Nenhum código de barras encontrado.")

        return resultados
