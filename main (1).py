import pandas as pd
import numpy as np
import warnings

# Desativar avisos de tipos mistos para uma saída mais limpa
warnings.filterwarnings('ignore', category=pd.errors.DtypeWarning)

# --- SETUP E CARREGAMENTO ---
# Ajustado para ler o arquivo na mesma pasta do script (execução local)
try:
    tabela = pd.read_csv("carteira.csv", encoding="latin1", sep=";", low_memory=False)
except FileNotFoundError:
    # Caso ainda esteja rodando no ambiente Manus
    tabela = pd.read_csv("/home/ubuntu/upload/carteira.csv", encoding="latin1", sep=";", low_memory=False)

# Conversão de datas
tabela['mes_aquisicao'] = pd.to_datetime(tabela['mes_aquisicao'], dayfirst=True, errors='coerce')
tabela['mes_vencimento'] = pd.to_datetime(tabela['mes_vencimento'], dayfirst=True, errors='coerce')
tabela['data_pagamento'] = pd.to_datetime(tabela['data_pagamento'], dayfirst=True, errors='coerce')

# --- ETAPA 1: DISTRIBUIÇÃO DA CARTEIRA ---
print("\n--- ETAPA 1: Distribuição da Carteira ---")
dist_aquisicao = tabela.groupby('mes_aquisicao')[['valor_parcela', 'valor_aquisicao_parcela']].sum()
dist_convenio = tabela.groupby('id_convenio')[['valor_parcela', 'valor_aquisicao_parcela']].sum()

print("Distribuição por Mês de Aquisição (Soma):\n", dist_aquisicao.tail())
print("\nDistribuição por Convênio (Soma):\n", dist_convenio)

# (BÔNUS): Cálculo do Valor Presente (VP) em 31/01/2026
data_base = pd.to_datetime('2026-01-31')

def calcular_vp(row):
    if pd.isna(row['mes_vencimento']) or pd.isna(row['taxa_mensal']):
        return 0
    n = (row['mes_vencimento'].year - data_base.year) * 12 + (row['mes_vencimento'].month - data_base.month)
    return row['valor_parcela'] / ((1 + row['taxa_mensal']) ** n)

tabela['valor_presente'] = tabela.apply(calcular_vp, axis=1)

dist_vp_mes = tabela.groupby('mes_aquisicao')['valor_presente'].sum()
print("\nDistribuição VP por Mês de Aquisição:\n", dist_vp_mes.tail())

# --- ETAPA 2: TAXA MÉDIA DA CARTEIRA ---
print("\n--- ETAPA 2: Taxa Média da Carteira ---")
taxa_total = (tabela['taxa_mensal'] * tabela['valor_aquisicao_parcela']).sum() / tabela['valor_aquisicao_parcela'].sum()
print(f"Taxa Média Total Ponderada: {taxa_total:.4f}")

taxa_convenio = tabela.groupby('id_convenio').apply(
    lambda x: (x['taxa_mensal'] * x['valor_aquisicao_parcela']).sum() / x['valor_aquisicao_parcela'].sum()
)
print("\nTaxa Média por Convênio:\n", taxa_convenio)

# --- ETAPA 3: INADIMPLÊNCIA DA CARTEIRA ---
print("\n--- ETAPA 3: Inadimplência Cash ---")
tabela['vencida'] = tabela['mes_vencimento'] < data_base
inad_df = tabela[tabela['vencida']].copy()
inad_df['valor_pago'] = inad_df['valor_pago'].fillna(0)

def calc_inad_cash(df_group):
    receber = df_group['valor_parcela'].sum()
    pago = df_group['valor_pago'].sum()
    return 1 - (pago / receber) if receber > 0 else 0

inad_total = calc_inad_cash(inad_df)
inad_convenio = inad_df.groupby('id_convenio').apply(calc_inad_cash)
inad_mes_venc = inad_df.groupby('mes_vencimento').apply(calc_inad_cash)

print(f"Inadimplência Cash Total: {inad_total:.4f}")
print("\nInadimplência por Convênio:\n", inad_convenio)
print("\nInadimplência por Mês de Vencimento (últimos 5):\n", inad_mes_venc.tail())

# --- ETAPA 4: IDENTIFICANDO O PROBLEMA ---
print("\n--- ETAPA 4: Diagnóstico para Análise ---")
diagnostico = pd.DataFrame({
    'Taxa_Media': taxa_convenio,
    'Inadimplencia': inad_convenio
})
diagnostico['Spread_Estimado'] = diagnostico['Taxa_Media'] - diagnostico['Inadimplencia']
print(diagnostico.sort_values(by='Inadimplencia', ascending=False))
