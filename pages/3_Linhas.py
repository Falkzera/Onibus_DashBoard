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

st.title('Análise por Linha 📈')
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
########################################################################################################################################
# Criação da Barra Lateral
empresas = df['EMPRESA'].value_counts().index  # Lista de empresas
controlador_empresas = st.sidebar.selectbox("Selecione a empresa:", options=empresas)  # Controlador de empresas

df_linhas = df[df['EMPRESA'] == controlador_empresas]  # Filtrando o DataFrame
linhas = df_linhas["LINHA"].value_counts().sort_values(ascending=False).index  # Lista das linhas de ônibus
linha = st.sidebar.selectbox("Selecione a linha:", options=linhas)  # Controlador de linhas


linha_dados = df[df["LINHA"] == linha]  # Filtrando o DataFrame


analise = st.sidebar.selectbox('Selecione a coluna para análise:',
                                options=['TODAS', 'QR / EMV', 'PAGANTE', 'VT', 'ESCOLAR',
                                'GRATUIDADE', 'PASSE LIVRE', 'DL+INT.VT', 'INT.ESC', 'TOTAL', 'EQUIVALENTE', 'RECEITA'])


########################################################################################################################################
# SLIDE DATA
########################################################################################################################################
# ANTIGO
data_inicial = st.sidebar.date_input('Selecione a data inicial:', df['DATA'].min())
data_final = st.sidebar.date_input('Selecione a data final:', df['DATA'].max())

########################################################################################################################################

########################################################################################################################################


########################################################################################
# Filtrando o DataFrame com base nas seleções do usuário
df_filtrado = linha_dados[(linha_dados['DATA'] >= pd.to_datetime(data_inicial)) & (linha_dados['DATA'] <= pd.to_datetime(data_final))]
# tarifa = obter_tarifa(pd.to_datetime(data_inicial), pd.to_datetime(data_final))
########################################################################################
# Título da Página
st.markdown(f"# *{linha}* :bus:") # Título da página
st.markdown(f"### Empresa: *{controlador_empresas}*") # Exibindo a empresa selecionada
########################################################################################
# Adição de metrícas
# Adição de métricas
valor_total = df_filtrado['RECEITA'].sum()
variacao_receita = round(((df_filtrado['RECEITA'].iloc[-1] - df_filtrado['RECEITA'].iloc[0]) / df_filtrado['RECEITA'].iloc[0]) * 100, 2)
# Variacao de passageiros
passageiro_total = df_filtrado['TOTAL'].sum()
variacao_passageiro = round(((df_filtrado['TOTAL'].iloc[-1] - df_filtrado['TOTAL'].iloc[0]) / df_filtrado['TOTAL'].iloc[0]) * 100, 2)
# Variação de passageiro equivalente
equivalente_total = df_filtrado['EQUIVALENTE'].sum()
variacao_equivalente = round(((df_filtrado['EQUIVALENTE'].iloc[-1] - df_filtrado['EQUIVALENTE'].iloc[0]) / df_filtrado['EQUIVALENTE'].iloc[0]) * 100, 2)

# Colunas das métricas
col1, col2, col3 = st.columns(3)

# Distribuição das métricas nas colunas
# Apresentar na tela
with st.container():
    with col1:     
        st.metric(
            label="Receita total no período",   
            value = "R$ {:,.2f}".format(valor_total).replace(',', 'X').replace('.', ',').replace('X', '.'),
            delta=f"Variação {variacao_receita:.2f}%"  
        )

    with col2:  
        st.metric(
            label="Passageiro total no período",   
            value = "{:,.2f}".format(passageiro_total).replace(',', 'X').replace('.', ',').replace('X', '.'),
            delta=f"Variação {variacao_passageiro:.2f}%",   
        )

    with col3: 
        st.metric(
            label="Passageiro total equivalente no período",   
            value = "{:,.2f}".format(equivalente_total).replace(',', 'X').replace('.', ',').replace('X', '.'),
            delta=f"Variação {variacao_equivalente:.2f}%",
        )

########################################################################################
# Adicionar o gráfico conforme a seleção do usuário

df_filtrado.set_index('DATA', inplace=True)  # Define a coluna de datas como índice



with st.container():

    tipo_grafico = st.sidebar.selectbox('Selecione o tipo de gráfico:', options=['Gráfico de linha', 'Gráfico de barras', 'Gráfico de área'])


    if tipo_grafico == 'Gráfico de linha':
        if analise == 'TODAS':
            st.line_chart(df_filtrado[colunas_para_somar])
        else:
            st.line_chart(df_filtrado[analise])

    elif tipo_grafico == 'Gráfico de barras':
        if analise == 'TODAS':
            st.bar_chart(df_filtrado[colunas_para_somar])
        else:
            st.bar_chart(df_filtrado[analise])
            
    elif tipo_grafico == 'Gráfico de área':
        if analise == 'TODAS':
            st.area_chart(df_filtrado[colunas_para_somar])
        else:
            st.area_chart(df_filtrado[analise])

# Configuração da barra lateral
st.sidebar.markdown('Developer by: [Lucas Falcão](https://GitHub.com/Falkzera)')
