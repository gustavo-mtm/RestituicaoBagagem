import cv2
from modules.deteccao import DetectorBagagem

def main():
    cap = cv2.VideoCapture(0)  # 0 para webcam
    detector = DetectorBagagem()
    
    # Lista para controlar quais IDs já foram fotografados nesta sessão
    ids_processados = set()

    print("Sistema de Monitoramento de Bagagens - ELE634 Iniciado.")
    print("Pressione 'q' para sair.")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        # 1. Realiza a detecção com rastreamento (Track)
        resultado = detector.detectar(frame)
        
        # Debug: mostrar informações sobre o frame e detecções
        if resultado.boxes is not None:
            num_boxes = len(resultado.boxes)
            print(f"DEBUG: Frame processado - {num_boxes} detecções encontradas")
            if num_boxes > 0:
                classes_detectadas = resultado.boxes.cls.int().cpu().tolist() if resultado.boxes.cls is not None else []
                confiancas = resultado.boxes.conf.cpu().tolist() if resultado.boxes.conf is not None else []
                ids_detectados = resultado.boxes.id.int().cpu().tolist() if resultado.boxes.id is not None else []
                nomes_classes = [detector.model.names.get(cls, f"Classe {cls}") for cls in classes_detectadas]
                print(f"DEBUG: Classes: {nomes_classes}, Confianças: {[f'{c:.2f}' for c in confiancas]}, IDs: {ids_detectados}")
        else:
            print("DEBUG: Nenhum resultado de detecção")
        
        # 2. Verifica se houve alguma detecção com ID atribuído
        
        # 2. Verifica se houve alguma detecção com ID atribuído
        if resultado.boxes is not None and resultado.boxes.id is not None:
            # Pegamos os IDs e Confianças de todas as detecções no frame
            ids = resultado.boxes.id.int().cpu().tolist()
            confiancas = resultado.boxes.conf.cpu().tolist()

            print(f"DEBUG: {len(ids)} detecções com ID - IDs: {ids}, Confianças: {[f'{c:.2f}' for c in confiancas]}")

            for i, obj_id in enumerate(ids):
                # Se o objeto é novo e a confiança é alta (ex: > 70%)
                if obj_id not in ids_processados and confiancas[i] > 0.40:
                    print(f"DEBUG: Salvando foto para ID {obj_id} (confiança: {confiancas[i]:.2f})")
                    # Tira a foto
                    caminho_foto = detector.salvar_snapshot(frame, resultado)
                    
                    # Adiciona ao set para não tirar foto da mesma mala no próximo frame
                    ids_processados.add(obj_id)
                    print(f"✅ Nova bagagem (ID {obj_id}) detectada e registrada!")
                else:
                    if obj_id in ids_processados:
                        print(f"DEBUG: ID {obj_id} já foi processado")
                    elif confiancas[i] <= 0.70:
                        print(f"DEBUG: ID {obj_id} confiança baixa ({confiancas[i]:.2f} <= 0.70)")
        else:
            print("DEBUG: Nenhuma detecção com ID encontrada (bagagem não detectada ou confiança baixa)")
        annotated_frame = resultado.plot()
        cv2.imshow("Monitoramento Ejetora (S2)", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()