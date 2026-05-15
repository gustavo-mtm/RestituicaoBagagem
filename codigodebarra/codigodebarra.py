import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.graphics.barcode import common


# Coloque aqui quantos códigos quiser.
# O PDF vai colocar até 10 códigos por página.
CODIGOS_FIXOS = [
    "7961159984",
    "6096424733",
    "7602713077",
    "0520251249",
    "3233607109",
    "0370612969",
    "5413396687",
    "3809050203",
    "6731914187",
    "2996258765",
    "1005179296",
    "8162562063",
    "6070960599",
    "4817469531",
    "8559422353",
    "7360188409",
    "6940373662",
    "9284936815",
    "5340413987",
    "3109539300",
]


def validar_codigo(codigo):
    if not codigo.isdigit():
        raise ValueError(f"O código '{codigo}' contém caracteres não numéricos.")

    if len(codigo) != 10:
        raise ValueError(f"O código '{codigo}' precisa ter exatamente 10 dígitos.")


def desenhar_codigo_barras(c, x, y, codigo):
    validar_codigo(codigo)

    barcode = common.I2of5(
        codigo,
        barHeight=25 * mm,
        barWidth=0.45 * mm,
        bearers=0
    )

    barcode.drawOn(c, x, y)

    c.setFont("Helvetica-Bold", 10)
    c.drawString(x, y - 7 * mm, codigo)


def gerar_pdf(caminho_arquivo):
    c = canvas.Canvas(caminho_arquivo, pagesize=A4)

    largura_pagina, altura_pagina = A4

    # Grade: 2 colunas x 5 linhas = 10 códigos por página
    colunas = 2
    linhas = 5

    margem_x = 25 * mm
    margem_y = 25 * mm

    espacamento_x = 95 * mm
    espacamento_y = 50 * mm

    for i, codigo in enumerate(CODIGOS_FIXOS):
        posicao_na_pagina = i % 10

        if i > 0 and posicao_na_pagina == 0:
            c.showPage()

        coluna = posicao_na_pagina % colunas
        linha = posicao_na_pagina // colunas

        x = margem_x + coluna * espacamento_x

        # Começa de cima para baixo
        y = altura_pagina - margem_y - linha * espacamento_y - 25 * mm

        desenhar_codigo_barras(c, x, y, codigo)

    c.save()


def executar_pipeline():
    nome_arquivo = "codigos_barras_10_por_pagina.pdf"

    pasta_saida = r"C:\Users\Gustavo\Downloads\teste"
    os.makedirs(pasta_saida, exist_ok=True)

    caminho_pdf = os.path.join(pasta_saida, nome_arquivo)

    gerar_pdf(caminho_pdf)

    print(f"PDF gerado com sucesso em: {caminho_pdf}")


if __name__ == "__main__":
    executar_pipeline()