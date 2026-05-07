import cv2
import os
from datetime import datetime
from ultralytics import YOLO


class DetectorBagagem:
    def __init__(self, tipo_codigo_permitido=None):
        self.model = YOLO('yolov8n.pt')
        self.classes_interesse = [24, 28]

        # Detector de código de barras do OpenCV
        self.barcode_detector = cv2.barcode.BarcodeDetector()
        
        # Tipo(s) de código de barras permitido(s)
        # Pode ser uma string para um único tipo ou lista para múltiplos tipos
        # Exemplos: "EAN_13" ou ["I25", "ITF"]
        if isinstance(tipo_codigo_permitido, str):
            self.tipos_permitidos = [tipo_codigo_permitido]
        elif isinstance(tipo_codigo_permitido, list):
            self.tipos_permitidos = tipo_codigo_permitido
        else:
            self.tipos_permitidos = None  # None = todos os tipos aceitos

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

    def detectar_codigo_barras(self, caminho_imagem, tipo_permitido=None):
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
        
        # Usa o tipo permitido passado como parâmetro, ou os definidos na classe
        tipos_permitidos = self.tipos_permitidos
        if tipo_permitido:
            if isinstance(tipo_permitido, str):
                tipos_permitidos = [tipo_permitido]
            else:
                tipos_permitidos = tipo_permitido

        if ok and decoded_info:
            print("DEBUG: Código(s) de barras encontrado(s).")

            if points is not None:
                indices_validos = []
                
                for i, texto in enumerate(decoded_info):
                    tipo = decoded_type[i] if i < len(decoded_type) else "desconhecido"

                    # Se há tipos específicos permitidos, filtra
                    if tipos_permitidos and tipo not in tipos_permitidos:
                        tipos_str = ", ".join(tipos_permitidos)
                        print(f"DEBUG: ❌ Código descartado - Tipo '{tipo}' não permitido (apenas '{tipos_str}' são aceitos)")
                    else:
                        # Código aceito
                        resultados.append({
                            "valor": texto,
                            "tipo": tipo
                        })
                        indices_validos.append(i)
                        print(f"DEBUG: ✅ Código aceito - Tipo '{tipo}', Valor: {texto}")

                # Desenha contornos apenas dos códigos válidos
                for i in indices_validos:
                    barcode = points[i]
                    pts = barcode.reshape(-1, 2).astype(int)

                    for j in range(len(pts)):
                        p1 = tuple(pts[j])
                        p2 = tuple(pts[(j + 1) % len(pts)])
                        cv2.line(img, p1, p2, (0, 255, 0), 2)

                # Salva imagem anotada apenas se houver códigos válidos
                if resultados:
                    output_dir = "data/processed"
                    if not os.path.exists(output_dir):
                        os.makedirs(output_dir)

                    nome_saida = os.path.basename(caminho_imagem).replace(".jpg", "_barcode.jpg")
                    caminho_saida = os.path.join(output_dir, nome_saida)
                    cv2.imwrite(caminho_saida, img)

                    print(f"DEBUG: Imagem anotada salva em {caminho_saida}")

        else:
            print("DEBUG: Nenhum código de barras encontrado.")

        return resultados

    def detectar_codigo_barras_frame(self, frame, tipo_permitido=None):
        """
        Detecta códigos de barras diretamente em um frame de câmera.
        Filtra por tipo(s) permitido(s).
        Retorna lista de códigos encontrados com seus valores e o frame anotado.
        
        Args:
            frame: Frame da câmera
            tipo_permitido: Tipo(s) de código permitido (ex: "I25", ["I25", "ITF"])
                           Se None, usa o tipo definido na classe. Se ainda for None, aceita todos.
        """
        try:
            ok, decoded_info, decoded_type, points = self.barcode_detector.detectAndDecodeWithType(frame)
        except Exception as e:
            print(f"DEBUG: Erro no detector de código de barras: {e}")
            return [], frame

        resultados = []
        frame_anotado = frame.copy()
        
        # Usa o tipo permitido passado como parâmetro, ou os definidos na classe
        tipos_permitidos = self.tipos_permitidos
        if tipo_permitido:
            if isinstance(tipo_permitido, str):
                tipos_permitidos = [tipo_permitido]
            else:
                tipos_permitidos = tipo_permitido

        if ok and decoded_info:
            if points is not None:
                indices_validos = []
                
                for i, texto in enumerate(decoded_info):
                    tipo = decoded_type[i] if i < len(decoded_type) else "desconhecido"

                    # Se há tipos específicos permitidos, filtra
                    if tipos_permitidos and tipo not in tipos_permitidos:
                        tipos_str = ", ".join(tipos_permitidos)
                        print(f"DEBUG: ❌ Código descartado - Tipo '{tipo}' não permitido (apenas '{tipos_str}' são aceitos)")
                    else:
                        # Código aceito
                        resultados.append({
                            "valor": texto,
                            "tipo": tipo
                        })
                        indices_validos.append(i)
                        print(f"DEBUG: ✅ Código aceito - Tipo '{tipo}', Valor: {texto}")

                # Desenha contornos apenas dos códigos válidos
                for i in indices_validos:
                    barcode = points[i]
                    pts = barcode.reshape(-1, 2).astype(int)

                    for j in range(len(pts)):
                        p1 = tuple(pts[j])
                        p2 = tuple(pts[(j + 1) % len(pts)])
                        cv2.line(frame_anotado, p1, p2, (0, 255, 0), 2)

        return resultados, frame_anotado
