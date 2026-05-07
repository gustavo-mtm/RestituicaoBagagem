import os
import shutil
import random
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.graphics.barcode import common

def gerar_dados_aleatorios():
    destinos = ["CNF", "GRU", "GIG", "MIA", "JFK", "LHR"]
    companhias = [("001", "AA"), ("047", "TP"), ("115", "LA"), ("126", "G3")]
    nomes = ["SILVA/A", "SANTOS/M", "OLIVEIRA/C", "SOUZA/F"]
    
    cod_num_cia, cod_alfa_cia = random.choice(companhias)
    destino = random.choice(destinos)
    nome = random.choice(nomes)
    
    # Gera serial de 6 dígitos para formar a tag padrão de 10 dígitos
    serial = f"{random.randint(100000, 999999)}"
    
    tag_num = f"{cod_num_cia}2{serial}"
    tag_alfa = f"{cod_alfa_cia} {serial}"
    tag_comb = f"{cod_num_cia}2 {tag_alfa}"
    
    return destino, nome, tag_num, tag_alfa, tag_comb

def desenhar_etiqueta(c, x, y, largura, altura, formato_tipo):
    destino, nome, tag_num, tag_alfa, tag_comb = gerar_dados_aleatorios()
    
    # Contorno
    c.setDash(1, 2)
    c.rect(x, y, largura, altura)
    c.setDash()
    
    # Textos do cabeçalho
    c.setFont("Helvetica-Bold", 16)
    c.drawString(x + 5*mm, y + altura - 25*mm, f"TO: {destino}")
    
    c.setFont("Helvetica", 10)
    c.drawString(x + 5*mm, y + altura - 35*mm, f"NAME: {nome}")
    
    # Para o ITF, o código de barras deve ser sempre apenas numérico (10 dígitos)
    valor_codigo_barras = tag_num 
    texto_inf_1 = ""
    texto_inf_2 = ""
    
    # Define o texto de OCR inferior
    if formato_tipo == 1:
        texto_inf_1 = tag_num
        texto_inf_2 = tag_alfa
    elif formato_tipo == 2:
        texto_inf_1 = tag_num
        texto_inf_2 = tag_comb
    elif formato_tipo == 3:
        texto_inf_1 = tag_comb
    else:
        c.setFont("Helvetica-Bold", 8)
        c.drawString(x + 5*mm, y + altura - 50*mm, "PASSENGER NAME AND ADDRESS")
        texto_inf_1 = tag_alfa

    # Gerador I2of5 (Interleaved 2 of 5)
    try:
        codigo_barras = common.I2of5(valor_codigo_barras, barHeight=18*mm, barWidth=0.35*mm)
        codigo_barras.drawOn(c, x + 3*mm, y + 25*mm)
    except Exception as e:
        c.drawString(x + 5*mm, y + 30*mm, "[Erro Barcode]")

    # Textos do OCR
    c.setFont("Helvetica-Bold", 9)
    if texto_inf_1:
        c.drawString(x + 5*mm, y + 15*mm, texto_inf_1)
    if texto_inf_2:
        c.drawString(x + 5*mm, y + 8*mm, texto_inf_2)

def gerar_pdf(caminho_arquivo):
    c = canvas.Canvas(caminho_arquivo, pagesize=A4)

    largura_etiqueta = 54.0 * mm
    altura_etiqueta = 140.0 * mm

    # Coordenadas ajustadas para o eixo Y não sobrepor
    posicoes = [
        (30*mm, 150*mm),
        (110*mm, 150*mm),
        (30*mm, 5*mm),
        (110*mm, 5*mm)
    ]

    for idx, (x, y) in enumerate(posicoes):
        desenhar_etiqueta(c, x, y, largura_etiqueta, altura_etiqueta, formato_tipo=idx+1)

    c.save()

def executar_pipeline():
    nome_arquivo = "iata_740_dataset_teste.pdf"
    
    pasta_downloads = r"C:\Users\iebt\Downloads"
    pasta_raiz = r"C:\Users\iebt\Documents\Bagagem\RestituicaoBagagem"
    
    caminho_downloads = os.path.join(pasta_downloads, nome_arquivo)
    caminho_raiz = os.path.join(pasta_raiz, nome_arquivo)
    
    # Cria o arquivo em downloads
    gerar_pdf(caminho_downloads)
    
    # Copia para raiz do projeto e deleta a origem
    if os.path.exists(caminho_downloads):
        shutil.copy2(caminho_downloads, caminho_raiz)
        os.remove(caminho_downloads)
        print(f"Dataset salvo e atualizado com sucesso em: {caminho_raiz}")

if __name__ == "__main__":
    executar_pipeline()