import re
from decimal import Decimal

def conferir_dados_fatura(dados_fatura, texto_bruto):
    # Lista onde guardaremos qualquer problema encontrado nesta fatura
    inconsistencias = []
    nome_arq = dados_fatura["arquivo"]
    
    # -------------------------------------------------------------
    # REGRA 1: Coerência da Medição
    # -------------------------------------------------------------
    leitura_ant = dados_fatura["leitura_anterior"]
    leitura_at = dados_fatura["leitura_atual"]
    consumo = dados_fatura["consumo_kwh"]
    
    if leitura_ant is not None and leitura_at is not None and consumo is not None:
        if (leitura_at - leitura_ant) != consumo:
            inconsistencias.append({
                "arquivo": nome_arq,
                "criterio": "Coerência da Medição",
                "mensagem": f"Divergência matemática: Leitura Atual ({leitura_at}) - Leitura Anterior ({leitura_ant}) resulta em {leitura_at - leitura_ant}, mas o consumo declarado é {consumo} kWh."
            })

    # -------------------------------------------------------------
    # REGRA 2: Verificação de Campos Obrigatórios Ausentes
    # -------------------------------------------------------------
    for campo, valor in dados_fatura.items():
        if campo != "bandeira" and valor is None:
            inconsistencias.append({
                "arquivo": nome_arq,
                "criterio": "Campo Ausente",
                "mensagem": f"O campo obrigatório '{campo}' não foi localizado ou não pôde ser extraído."
            })

    # -------------------------------------------------------------
    # REGRA 3: Soma dos Itens Financeiros vs Valor Total
    # -------------------------------------------------------------
    # 1. Isolamos a seção de faturamento do texto para não capturar números de outras áreas
    linhas = texto_bruto.split("\n")
    soma_itens = Decimal("0.00")
    dentro_faturamento = False
    
    for linha in linhas:
        # Se a linha indicar o início da tabela de itens, começamos a somar
        if "FATURAMENTO" in linha.upper() or "DESCRICAO DOS ITENS" in linha.upper() or "ITENS DA FATURA" in linha.upper():
            dentro_faturamento = True
            continue
        
        # Se a linha indicar o fim da tabela (onde aparece o Total), paramos a soma
        if "TOTAL" in linha.upper() or "=====" in linha:
            if dentro_faturamento:
                break
                
        # Se estivermos na região de itens, capturamos os valores em R$ no final da linha
        if dentro_faturamento:
            # Regex que busca por valores numéricos formatados como dinheiro (ex: 1.492,00 ou 74,60)
            busca_valores = re.findall(r"R\$\s*([\d\.,]+)|(?<=\s)([\d\.,]+)$", linha.strip())
            for match in busca_valores:
                # O findall pode retornar tuplas, pegamos o lado que conter o texto
                val_texto = match[0] if match[0] else match[1]
                if val_texto and "," in val_texto:
                    # Padroniza para o formato numérico americano
                    val_limpo = val_texto.replace(".", "").replace(",", ".")
                    soma_itens += Decimal(val_limpo)

    # 2. Comparamos a soma dos itens individuais com o valor_total extraído no Módulo 1
    valor_total_declarado = dados_fatura["valor_total"]
    if valor_total_declarado is not None:
        diferenca = abs(valor_total_declarado - soma_itens)
        # Se a divergência for maior que 1 centavo (R$ 0,01), reportamos o erro
        if diferenca > Decimal("0.01"):
            inconsistencias.append({
                "arquivo": nome_arq,
                "criterio": "Soma dos Itens",
                "mensagem": f"A soma dos itens faturados (R$ {soma_itens}) não bate com o Total Declarado (R$ {valor_total_declarado}). Diferença de R$ {diferenca}."
            })
            
    return inconsistencias
