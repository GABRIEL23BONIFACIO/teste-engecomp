import re
from decimal import Decimal, InvalidOperation

def extrair_dados_fatura(texto_bruto, nome_arquivo):
    # 1. Inicialização do dicionário
    dados = {
        "arquivo": nome_arquivo,
        "distribuidora": None,
        "cliente": None,
        "documento": None,
        "unidade_consumidora": None,
        "referencia": None,
        "vencimento": None,
        "leitura_anterior": None,
        "leitura_atual": None,
        "consumo_kwh": None,
        "bandeira": None,
        "valor_total": None
    }
    
    # 2. Extração do Cliente
    padrao_cliente = r"(?:CLIENTE:|Titular\.*:|Nome/Razao Social\s*:)\s*(.*)"
    busca_cliente = re.search(padrao_cliente, texto_bruto, re.IGNORECASE)
    if busca_cliente:
        dados["cliente"] = busca_cliente.group(1).strip()

    # --- LOGICA DE EXTRAÇÃO E TRATAMENTO DO VALOR TOTAL ---
    padrao_valor = r"(?:TOTAL A PAGAR|VALOR TOTAL DA FATURA|TOTAL DA FATURA)\s*(?:R\$)?\s*\.*\s*(?:R\s*\$)?\s*([\d\.,]+)"
    busca_valor = re.search(padrao_valor, texto_bruto, re.IGNORECASE)
    
    if busca_valor:
        texto_bruto_valor = busca_valor.group(1).strip()
        texto_sem_milhar = texto_bruto_valor.replace(".", "")
        texto_padrao_americano = texto_sem_milhar.replace(",", ".")
        try:
            dados["valor_total"] = Decimal(texto_padrao_americano)
        except InvalidOperation:
            dados["valor_total"] = None

        # --- LÓGICA DE EXTRAÇÃO E TRATAMENTO DA DATA DE VENCIMENTO ---
    padrao_vencimento = r"(?:DATA DE VENCIMENTO|Vencimento|Data Vencimento)\s*\.*:\s*([\d/]+)"
    busca_vencimento = re.search(padrao_vencimento, texto_bruto, re.IGNORECASE)
    
    if busca_vencimento:
        texto_vencimento = busca_vencimento.group(1).strip() # Ex: "15/08/2026"
        partes = texto_vencimento.split("/") # Transforma em ["15", "08", "2026"]
        if len(partes) == 3:
            # Organiza no formato exigido: AAAA-MM-DD
            dados["vencimento"] = f"{partes[2]}-{partes[1]}-{partes[0]}"

    # --- LÓGICA DE EXTRAÇÃO E TRATAMENTO DO MÊS DE REFERÊNCIA ---
    padrao_referencia = r"(?:MES DE REFERENCIA|Referencia|Mes/Ano Referencia)\s*\.*:\s*([\w/]+)"
    busca_referencia = re.search(padrao_referencia, texto_bruto, re.IGNORECASE)
    
    if busca_referencia:
        texto_ref = busca_referencia.group(1).strip().upper() # Ex: "07/2026" ou "AGOSTO/2026"
        partes_ref = texto_ref.split("/") # Divide no caractere '/'
        
        if len(partes_ref) == 2:
            mes = partes_ref[0]
            ano = partes_ref[1]
            
            # Dicionário tradutor para o caso da distribuidora que escreve por extenso
            meses_extenso = {
                "JANEIRO": "01", "FEVEREIRO": "02", "MARÇO": "03", "ABRIL": "04",
                "MAIO": "05", "JUNHO": "06", "JULHO": "07", "AGOSTO": "08",
                "SETEMBRO": "09", "OUTUBRO": "10", "NOVEMBRO": "11", "DEZEMBRO": "12"
            }
            
            # Se o mês extraído estiver por extenso, substitui pelo número correspondente
            if mes in meses_extenso:
                mes = meses_extenso[mes]
                
            # Organiza no formato exigido: AAAA-MM
            dados["referencia"] = f"{ano}-{mes}"

    # --- LÓGICA DE EXTRAÇÃO DO DOCUMENTO (CPF/CNPJ) DO CLIENTE ---
    # Este padrão busca especificamente as linhas ligadas ao cliente, ignorando o CNPJ da distribuidora no topo
    padrao_documento = r"(?:CPF/CNPJ|Documento|CNPJ/CPF)\s*\.*:\s*([\d\./-]+)"
    busca_documento = re.search(padrao_documento, texto_bruto, re.IGNORECASE)
    
    if busca_documento:
        # Pega o documento extraído e limpa espaços extras nas pontas
        dados["documento"] = busca_documento.group(1).strip()

    return dados
