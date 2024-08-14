########################################################################################################################################
# Importação das bibliotecas
import pandas as pd
import streamlit as st

# Importnado planilhas
df = pd.read_csv('data/df_final.csv')
df['DATA'] = pd.to_datetime(df['DATA'])

# Adicionando em outras páginas
st.session_state['df'] = df

# Dados das tarifas
dados_tarifas = {
    'TARIFA': [2.75, 3.15, 3.50, 3.65, 3.35, 4.00, 3.49],
    'DATA': ['06/02/2015', '07/01/2016', '23/02/2017', '09/02/2018', '21/01/2021', '29/05/2023', '29/05/2023']
}
df_tarifas = pd.DataFrame(dados_tarifas)
# Converter datas para datetime (formato dd/mm/yyyy)
df_tarifas['DATA'] = pd.to_datetime(df_tarifas['DATA'], format='%d/%m/%Y')

# Configuração da página
st.set_page_config(page_title="Empresas", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

st.title('Análise Metrícas 📈')
# 📈



# Colunas para realizar cálculos
colunas_para_somar = [
    'QR / EMV', 'PAGANTE', 'VT', 'ESCOLAR', 'GRATUIDADE', 
    'PASSE LIVRE', 'DL+INT.VT', 'INT.ESC', 'TOTAL', 
    'EQUIVALENTE'
]
########################################################################################################################################
# CONFIGURAÇÕES DAQUI PARA BAIXO:
# CONFIGURAÇÕES DAQUI PARA BAIXO:
# CONFIGURAÇÕES DAQUI PARA BAIXO:
# CONFIGURAÇÕES DAQUI PARA BAIXO:
# CONFIGURAÇÕES DAQUI PARA BAIXO:

