########################################################################################################################################
# Importação das bibliotecas
import pandas as pd
import streamlit as st
import Home.Credito as Credito

# Importnado planilhas
df = pd.read_csv('data/df_final.csv')
df['DATA'] = pd.to_datetime(df['DATA'])



# # Adicionando em outras páginas
# st.session_state['df'] = df

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


# Filtros resumidos


# Criando uma cópia do df original
df_filtered = df.copy()

# Separo ANO E MÊS
df_filtered['ANO'] = df['DATA'].dt.year
df_filtered['MÊS'] = df['DATA'].dt.month

df_resumo = df_filtered.groupby(['ANO', 'MÊS', 'LINHA', 'EMPRESA']).agg({
    'TOTAL': 'sum',
    'GRATUIDADE': 'sum',
    'EQUIVALENTE': 'sum',
    'TARIFA': 'mean',
    'RECEITA': 'sum',
}).reset_index()

# Ordem
df_resumo = df_resumo[['ANO', 'MÊS', 'EMPRESA', 'LINHA', 'TOTAL', 'GRATUIDADE', 'EQUIVALENTE', 'RECEITA']]

# Convertendo colunas para tipos nativos do Python
df_resumo["TOTAL"] = df_resumo["TOTAL"].astype(int)
df_resumo["EQUIVALENTE"] = df_resumo["EQUIVALENTE"].astype(int)
df_resumo["GRATUIDADE"] = df_resumo["GRATUIDADE"].astype(int)
df_resumo["RECEITA"] = df_resumo["RECEITA"].astype(float)
 

#########################################################################################
# Configuração da barra lateral
empresas = df['EMPRESA'].value_counts().index  # Lista de empresas
controlador_empresas = st.sidebar.selectbox("Selecione a empresa:", options=empresas)  # Controlador de empresas

# df_filtered = df_resumo[df_resumo['EMPRESA'] == controlador_empresas].set_index("LINHA")

st.markdown(f'## {controlador_empresas}')

columns = ['ANO', 'MÊS', 'EMPRESA', 'LINHA', 'TOTAL', 'GRATUIDADE', 'EQUIVALENTE', 'RECEITA']

st.dataframe(df_filtered[columns], column_config={

     "RECEITA": st.column_config.ProgressColumn("RECEITA", format="R$ %.2f" ,min_value=0, max_value=float(df_filtered['RECEITA'].max())),
     
     "TOTAL": st.column_config.ProgressColumn("TOTAL", format="%.2f" ,min_value=0, max_value=float(df_filtered['TOTAL'].max())), 

     "EQUIVALENTE": st.column_config.ProgressColumn("EQUIVALENTE", format="%.2f", min_value=0, max_value=float(df_filtered['EQUIVALENTE'].max())), 

     "GRATUIDADE": st.column_config.ProgressColumn("GRATUIDADE", format="%.2f", min_value=0, max_value=float(df_filtered['GRATUIDADE'].max()))
})

# Configuração da barra lateral
with st.sidebar:
    Credito.display_credits()
   