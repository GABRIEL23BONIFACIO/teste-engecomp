from pathlib import Path
import json
# Importamos a função que você estruturou e salvou no seu Módulo 1
from extracao import extrair_dados_fatura 

def executar_sistema():
    pasta_dados = Path("dados")
    
    # Verificação de segurança: confere se a pasta dados realmente existe
    if not pasta_dados.exists():
        print("Erro: A pasta 'dados' não foi encontrada. Crie a pasta e coloque as faturas dentro.")
        return

    # Lista onde guardaremos o dicionário de cada uma das faturas processadas
    faturas_processadas = []
    
    # Encontra todos os arquivos de texto (.txt) dentro da pasta dados
    arquivos_encontrados = list(pasta_dados.glob("*.txt"))
    
    if not arquivos_encontrados:
        print("Aviso: Nenhum arquivo .txt encontrado dentro da pasta 'dados'.")
        return

    for arquivo_path in arquivos_encontrados:
        print(f"Lendo e processando o arquivo: {arquivo_path.name}")
        
        # Abre e lê o texto bruto de cada fatura
        with open(arquivo_path, "r", encoding="utf-8") as arquivo:
            texto_bruto = arquivo.read()
        
        # Executa o seu Módulo 1 (Extração) passando o texto e o nome do arquivo
        dados_da_fatura = extrair_dados_fatura(texto_bruto, arquivo_path.name)
        
        # Guarda o dicionário extraído na nossa lista
        faturas_processadas.append(dados_da_fatura)
            
    # Imprime no terminal o resultado em formato JSON limpo e estruturado para você auditar
    print("\n=======================================================")
    print("      RESULTADO DA EXTRAÇÃO AUTOMATIZADA (MÓDULO 1)     ")
    print("=======================================================")
    print(json.dumps(faturas_processadas, indent=4, ensure_ascii=False, default=str))

if __name__ == "__main__":
    executar_sistema()
