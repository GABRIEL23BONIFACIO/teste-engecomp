from decimal import Decimal, ROUND_HALF_UP

def aplicar_regras_fatura(dados_fatura):
    # Se o consumo não foi extraído por algum motivo, não fazemos a conta
    consumo_original = dados_fatura["consumo_kwh"]
    if consumo_original is None:
        dados_fatura["consumo_ajustado_kwh"] = None
        return dados_fatura

    distribuidora = dados_fatura["distribuidora"]
    
    # Lista de concessionárias que sofrem o acréscimo de 1%
    concessionarias_com_perda = ["CIA LUZ DO VALE", "COMPANHIA ELETRICA SUDESTE"]
    
    if distribuidora in concessionarias_com_perda:
        # Conversão para Decimal para garantir precisão matemática no arredondamento
        consumo_dec = Decimal(str(consumo_original))
        perda_kwh = consumo_dec * Decimal("0.01")
        consumo_ajustado = consumo_dec + perda_kwh
        
        # Arredonda estritamente para 2 casas decimais conforme o enunciado
        consumo_ajustado = consumo_ajustado.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        
        # Converte de volta para float ou mantém decimal para o JSON final
        dados_fatura["consumo_ajustado_kwh"] = float(consumo_ajustado)
    else:
        # Para as demais distribuidoras, o consumo ajustado é igual ao faturado original
        dados_fatura["consumo_ajustado_kwh"] = float(consumo_original)
        
    return dados_fatura
