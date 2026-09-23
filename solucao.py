from pathlib import Path
import json
from extracao import extrair_dados_fatura 
from conferencia import conferir_dados_fatura
from regras import aplicar_regras_fatura

def executar_sistema():
    pasta_dados = Path("dados")
    
    if not pasta_dados.exists():
        print("Erro: A pasta 'dados' não foi encontrada.")
        return

    faturas_finais = []
    todas_inconsistencias = []
    
    arquivos_encontrados = list(pasta_dados.glob("*.txt"))
    
    for arquivo_path in arquivos_encontrados:
        with open(arquivo_path, "r", encoding="utf-8") as arquivo:
            texto_bruto = arquivo.read()
        
        # 1. ETAPA DE EXTRAÇÃO (Módulo 1)
        dados_brutos = extrair_dados_fatura(texto_bruto, arquivo_path.name)
        
        # 2. ETAPA DE CONFERÊNCIA (Módulo 2)
        erros_fatura = conferir_dados_fatura(dados_brutos, texto_bruto)
        if erros_fatura:
            todas_inconsistencias.extend(erros_fatura)
            
        # 3. ETAPA DE REGRAS (Módulo 3)
        dados_com_regras = aplicar_regras_fatura(dados_brutos)
        faturas_finais.append(dados_com_regras)
            
    # --- GERAR O ARQUIVO SAÍDA JSON ---
    with open("resultado.json", "w", encoding="utf-8") as f_json:
        json.dump(faturas_finais, f_json, indent=4, ensure_ascii=False, default=str)
        
    # --- EXIBIÇÃO DOS RELATÓRIOS NO TERMINAL ---
    print("\n=======================================================")
    print("      RESULTADO FINAL PROCESSADO (MÓDULOS 1, 2 E 3)     ")
    print("=======================================================")
    print(json.dumps(faturas_finais, indent=4, ensure_ascii=False, default=str))

    print("\n=======================================================")
    print("      RELATÓRIO DE INCONSISTÊNCIAS COMPLETO            ")
    print("=======================================================")
    if todas_inconsistencias:
        print(f"Atenção! Foram encontradas {len(todas_inconsistencias)} inconsistências nos dados:\n")
        for idx, erro in enumerate(todas_inconsistencias, 1):
            print(f"[{idx}] Arquivo: {erro['arquivo']} | Critério: {erro['criterio']}")
            print(f"    Mensagem: {erro['mensagem']}\n")
    else:
        print("Sucesso! Nenhuma inconsistência detectada.")
    print("O arquivo 'resultado.json' foi gerado com sucesso no diretório atual.")

if __name__ == "__main__":
    executar_sistema()
