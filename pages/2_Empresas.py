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

st.title('Análise Geral das Empresas 🚌')
# 📈

# Configuração da barra lateral
st.sidebar.markdown('Developer by: [Lucas Falcão](https://GitHub.com/Falkzera)')

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
# Criação de filtros em colunas
with st.container():
    st.subheader("Filtros:")

    col1, col2, col3, col4= st.columns(4)

    with col1: # Selecionar a empresa desejada. Por padrão vem todas
        ativo = st.selectbox('Selecione a empresa desejada:', options=['TODAS'] + list(df['EMPRESA'].unique()))

    with col2:  # Selecionar a coluna para analis entre: QR / EMV	PAGANTE	VT	ESCOLAR	GRATUIDADE	PASSE LIVRE	DL+INT.VT	INT.ESC	TOTAL	EQUIVALENTE.  POR PADRÃO VEM TODAS
        analise = st.selectbox('Selecione a coluna para análise:', options=['TODAS', 'QR / EMV', 'PAGANTE', 'VT', 'ESCOLAR', 'GRATUIDADE', 'PASSE LIVRE', 'DL+INT.VT', 'INT.ESC', 'TOTAL', 'EQUIVALENTE', 'RECEITA'])

    with col3:
        data_inicial = st.date_input('Selecione a data inicial:', df['DATA'].min())
        data_inicial = pd.to_datetime(data_inicial)

    with col4:
        data_final = st.date_input('Selecione a data final:', df['DATA'].max())
        data_final = pd.to_datetime(data_final)

# Filtrando o DataFrame com base nas seleções do usuário
df_filtrado = df[(df['DATA'] >= pd.to_datetime(data_inicial)) & (df['DATA'] <= pd.to_datetime(data_final))]
if ativo != 'TODAS': 
    df_filtrado = df_filtrado[df_filtrado['EMPRESA'] == ativo]

# Criação de tarifária por periodo
# Função para obter a tarifa com base no período selecionado
def obter_tarifa(data_inicial, data_final):
    tarifa_filtrada = df_tarifas[(df_tarifas['DATA'] >= data_inicial) & (df_tarifas['DATA'] <= data_final)]
    if not tarifa_filtrada.empty:
        return tarifa_filtrada['TARIFA'].iloc[-1]  # Pega a tarifa mais recente dentro do intervalo
    else:
        return None  # Retorna None se não houver tarifas no intervalo


########################################################################################################################################
# METRÍCAS DE RECEITA, PASSAGEIROS TOTAIS E EQUIVALENTES.
error = False
try:
    valor_total = df_filtrado['RECEITA'].sum()
    variacao_tarifa = round(((df_filtrado['RECEITA'].iloc[-1] - df_filtrado['RECEITA'].iloc[0]) / df_filtrado['RECEITA'].iloc[0]) * 100, 2)
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
        with col1: # Formatar para :,2f para apresentar com duas casas decimais separados por virgula e o milhar por ponto como usa no brasileiro    
            st.metric(
                label="Receita total no período",   
                value = "R$ {:,.2f}".format(valor_total).replace(',', 'X').replace('.', ',').replace('X', '.'),
                delta=f"Variação {variacao_tarifa:.2f}%"  
            )

        with col2: # Formatar para :,2f para apresentar com duas casas decimais separados por virgula e o milhar por ponto como usa no brasileiro    
            st.metric(
                label="Passageiro total no período",   
                value = "{:,.2f}".format(passageiro_total).replace(',', 'X').replace('.', ',').replace('X', '.'),
                delta=f"Variação {variacao_passageiro:.2f}%",   
            )

        with col3: # Formatar para :,2f para apresentar com duas casas decimais separados por virgula e o milhar por ponto como usa no brasileiro    
            st.metric(
                label="Passageiro total equivalente no período",   
                value = "{:,.2f}".format(equivalente_total).replace(',', 'X').replace('.', ',').replace('X', '.'),
                delta=f"Variação {variacao_equivalente:.2f}%",
            )
except:
    st.error('Não existe dados para o período informado', icon="🚨")
    error = True
########################################################################################################################################
# VISUALIZAÇÃO GRÁFIC
if not error:
    with st.container():
            tipo_grafico = st.selectbox('Selecione o tipo de gráfico:', options=['Gráfico de linha', 'Gráfico de barras', 'Gráfico de área'])
            
            if tipo_grafico == 'Gráfico de linha':
                if analise != 'TODAS':
                    st.line_chart(df_filtrado.groupby('DATA').sum()[analise])
                else:
                
                    df_linha_chart = df_filtrado.groupby(['DATA'])[colunas_para_somar].sum()
                    
                    df_linha_chart = df_linha_chart.reset_index()
                    df_linha_chart.set_index('DATA', inplace=True)
                    st.line_chart(df_linha_chart)
            elif tipo_grafico == 'Gráfico de barras':
                if analise != 'TODAS':
                    st.bar_chart(df_filtrado.groupby('DATA').sum()[analise])
                else:
                    
                    df_bar_chart = df_filtrado.groupby(['DATA'])[colunas_para_somar].sum()
                    st.bar_chart(df_bar_chart)
            else:  
                if analise != 'TODAS':
                    st.area_chart(df_filtrado.groupby('DATA').sum()[analise])
                else:
                
                    df_linha_chart = df_filtrado.groupby(['DATA'])[colunas_para_somar].sum()
        
                    df_linha_chart = df_linha_chart.reset_index()
                    df_linha_chart.set_index('DATA', inplace=True)
                    st.area_chart(df_linha_chart)
########################################################################################################################################