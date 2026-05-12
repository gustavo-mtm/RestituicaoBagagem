"""
Script de Inicialização e Teste do Sistema com Dynamsoft Barcode Reader
Executa este script para verificar se todas as funcionalidades estão operacionais.
"""

import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from modules.config_license import inicializar_licenca, verificar_status_licenca
from modules.leitor_dinamsoft import LeitorDynamsoft
from modules.deteccao import DetectorBagagem


def teste_licenca():
    """Testa e ativa a licença do Dynamsoft"""
    print("\n" + "=" * 70)
    print("TESTE 1: ATIVAÇÃO DE LICENÇA DYNAMSOFT")
    print("=" * 70)
    
    if inicializar_licenca():
        verificar_status_licenca()
        print("✅ Licença ativada com sucesso!")
        return True
    else:
        print("❌ Falha na ativação da licença")
        return False


def teste_leitor_dinamsoft():
    """Testa a inicialização do leitor Dynamsoft"""
    print("\n" + "=" * 70)
    print("TESTE 2: INICIALIZAÇÃO DO LEITOR DYNAMSOFT")
    print("=" * 70)
    
    try:
        leitor = LeitorDynamsoft()
        print("✅ Leitor Dynamsoft inicializado com sucesso!")
        
        print("\n🎯 FORMATO ATIVO:")
        info = leitor.listar_formatos_suportados()
        print(f"   {info['formato_configurado']}")
        
        print("\n✨ Benefícios da otimização:")
        for beneficio in info['beneficios']:
            print(f"   ✓ {beneficio}")
        
        print("\n📚 Formatos alternativos suportados pelo SDK:")
        formatos = leitor.listar_todos_formatos_suportados_pelo_sdk()
        for fmt in formatos[:5]:  # Mostra apenas 5 primeiros
            print(f"   {fmt}")
        print(f"   ... e {len(formatos) - 5} outros formatos")
        
        return True
    except Exception as e:
        print(f"❌ Erro ao inicializar leitor: {e}")
        return False


def teste_detector_bagagem():
    """Testa a integração com a classe DetectorBagagem"""
    print("\n" + "=" * 70)
    print("TESTE 3: INTEGRAÇÃO COM DETECTOR DE BAGAGEM")
    print("=" * 70)
    
    try:
        # Cria detector com Dynamsoft habilitado
        detector = DetectorBagagem(usar_dynamsoft=True)
        print("✅ DetectorBagagem criado com sucesso!")
        
        if detector.usar_dynamsoft:
            print("✅ Usando Dynamsoft para detecção de código de barras")
        else:
            print("⚠️  Usando OpenCV como fallback")
        
        return True
    except Exception as e:
        print(f"❌ Erro ao criar detector: {e}")
        return False


def main():
    """Executa todos os testes"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "    TESTE DE INICIALIZAÇÃO - SISTEMA DE LEITURA DE CÓDIGO    ".center(68) + "║")
    print("║" + "    DYNAMSOFT OTIMIZADO PARA INTERLEAVED 2 OF 5 (ITF)    ".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    
    # Executa testes
    resultados = {
        "Licença Dynamsoft": teste_licenca(),
        "Leitor Dynamsoft": teste_leitor_dinamsoft(),
        "Integração com Detector": teste_detector_bagagem()
    }
    
    # Resumo dos testes
    print("\n" + "=" * 70)
    print("RESUMO DOS TESTES")
    print("=" * 70)
    
    todos_passaram = True
    for teste, resultado in resultados.items():
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"{teste:.<50} {status}")
        if not resultado:
            todos_passaram = False
    
    print("=" * 70)
    
    if todos_passaram:
        print("\n✅ TODOS OS TESTES PASSARAM COM SUCESSO!")
        print("\nO sistema está pronto para uso. Execute: python src/main.py")
    else:
        print("\n❌ ALGUNS TESTES FALHARAM")
        print("\nVerifique:")
        print("  1. A chave de licença está correta")
        print("  2. O pacote Dynamsoft está instalado: pip install dynamsoft-barcode-reader-bundle")
        print("  3. A licença não expirou")
    
    print("\n")
    return todos_passaram


if __name__ == "__main__":
    sucesso = main()
    sys.exit(0 if sucesso else 1)
