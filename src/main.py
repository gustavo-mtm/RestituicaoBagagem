import cv2
from modules.deteccao import DetectorBagagem
from datetime import datetime

def main():
    cap = cv2.VideoCapture(0)  # 0 para webcam
    detector = DetectorBagagem(tipo_codigo_permitido="EAN_13")
    
    # Dicionário para controlar códigos de barras já registrados nesta sessão
    codigos_registrados = set()

    print("Sistema de Leitura de Código de Barras - ELE634 Iniciado.")
    print("Pressione 'q' para sair.")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("DEBUG: Erro ao capturar frame da webcam.")
            break

        # Nova abordagem: Buscar por código de barras diretamente no frame
        codigos, frame_anotado = detector.detectar_codigo_barras_frame(frame)

        if codigos:
            for codigo in codigos:
                valor = codigo['valor']
                tipo = codigo['tipo']
                
                # Registra apenas códigos novos (não duplicados)
                if valor not in codigos_registrados:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                    print(f"✅ [{timestamp}] Código detectado: {valor} (Tipo: {tipo})")
                    codigos_registrados.add(valor)
                    # Aqui você pode adicionar gravação em banco de dados
        else:
            print("DEBUG: Aguardando código de barras...")

        cv2.imshow("Leitor de Código de Barras (S2)", frame_anotado)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()


# === CÓDIGO ANTIGO - DETECÇÃO DE BAGAGENS (COMENTADO PARA TESTES) ===
# 
# def main_antigo():
#     cap = cv2.VideoCapture(0)  # 0 para webcam
#     detector = DetectorBagagem()
#     
#     # Lista para controlar quais IDs já foram fotografados nesta sessão
#     ids_processados = set()
# 
#     print("Sistema de Monitoramento de Bagagens - ELE634 Iniciado.")
#     print("Pressione 'q' para sair.")
# 
#     while cap.isOpened():
#         success, frame = cap.read()
#         if not success:
#             print("DEBUG: Erro ao capturar frame da webcam.")
#             break
# 
#         # 1. Realiza a detecção com rastreamento
#         resultado = detector.detectar(frame)
#         
#         # Debug: mostrar informações sobre o frame e detecções
#         if resultado.boxes is not None:
#             num_boxes = len(resultado.boxes)
#             print(f"DEBUG: Frame processado - {num_boxes} detecções encontradas")
#             if num_boxes > 0:
#                 classes_detectadas = resultado.boxes.cls.int().cpu().tolist() if resultado.boxes.cls is not None else []
#                 confiancas = resultado.boxes.conf.cpu().tolist() if resultado.boxes.conf is not None else []
#                 ids_detectados = resultado.boxes.id.int().cpu().tolist() if resultado.boxes.id is not None else []
#                 nomes_classes = [detector.model.names.get(cls, f"Classe {cls}") for cls in classes_detectadas]
#                 print(f"DEBUG: Classes: {nomes_classes}, Confianças: {[f'{c:.2f}' for c in confiancas]}, IDs: {ids_detectados}")
#         else:
#             print("DEBUG: Nenhum resultado de detecção")
# 
#         # 2. Verifica se houve alguma detecção com ID atribuído
#         if resultado.boxes is not None and resultado.boxes.id is not None:
#             ids = resultado.boxes.id.int().cpu().tolist()
#             confiancas = resultado.boxes.conf.cpu().tolist()
# 
#             print(f"DEBUG: {len(ids)} detecções com ID - IDs: {ids}, Confianças: {[f'{c:.2f}' for c in confiancas]}")
# 
#             for i, obj_id in enumerate(ids):
#                 # Se o objeto é novo e a confiança é alta
#                 if obj_id not in ids_processados and confiancas[i] > 0.40:
#                     print(f"DEBUG: Salvando foto para ID {obj_id} (confiança: {confiancas[i]:.2f})")
#                     
#                     # 3. Salva a imagem da bagagem
#                     caminho_foto = detector.salvar_snapshot(frame, resultado)
# 
#                     # 4. Procura código de barras na imagem salva
#                     codigos = detector.detectar_codigo_barras(caminho_foto)
# 
#                     if codigos:
#                         for codigo in codigos:
#                             print(f"✅ Código detectado: {codigo['valor']} ({codigo['tipo']})")
#                     else:
#                         print("⚠️ Nenhum código de barras encontrado na imagem da bagagem.")
# 
#                     # 5. Marca esse ID como processado
#                     ids_processados.add(obj_id)
#                     print(f"✅ Nova bagagem (ID {obj_id}) detectada e registrada!")
# 
#                 else:
#                     if obj_id in ids_processados:
#                         print(f"DEBUG: ID {obj_id} já foi processado")
#                     elif confiancas[i] <= 0.40:
#                         print(f"DEBUG: ID {obj_id} confiança baixa ({confiancas[i]:.2f} <= 0.40)")
#         else:
#             print("DEBUG: Nenhuma detecção com ID encontrada (bagagem não detectada ou sem rastreamento)")
# 
#         annotated_frame = resultado.plot()
#         cv2.imshow("Monitoramento Ejetora (S2)", annotated_frame)
# 
#         key = cv2.waitKey(1) & 0xFF
#         if key == ord('q'):
#             break
# 
#     cap.release()
#     cv2.destroyAllWindows()
