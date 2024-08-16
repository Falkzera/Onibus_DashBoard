########################################################################################################################################
# Importação das bibliotecas
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu

# Importnado planilhas
df = pd.read_excel('data/SJ/SJ24_BI.xlsx')

# Converter coluna data para datetime



st.set_page_config(page_title="Empresas", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

st.title('Análise por Linha 📈')



# Menu de Navegação 
with st.container():
    selected = option_menu(
        menu_title = None,
        options = ["Power BI", "Gool System", 'Comparativo'],
        icons = ['person', 'globe'],
        orientation='horizontal',
    )
st.write("---")

########################################################################################
if selected == "Power BI":
    # 📈
    # COLUNAS PRESENTES NO MEU DATAFRAME 
    # EMPRESA	LINHAS	NOME_LINHA	PREVISTOS	REALIZADOS	TAXA_PARTIDA	KM_LINHA	KM_OCIOSA	FROTA	CUSTO/KM	KM_TOTAL	KM/DIA	CUSTO_VIAGEM	CUSTO_TOTAL	DATA
    #
    # Colunas para realizar cálculos
    colunas_para_somar = [
        'PREVISTOS', 'REALIZADOS', 'TAXA_PARTIDA', 'KM/DIA', 'CUSTO_VIAGEM', 'CUSTO_TOTAL'
    ]

    colunas_para_somar_2 = [
        'PREVISTOS', 'REALIZADOS', 'TAXA_PARTIDA', 'KM_LINHA', 'KM_OCIOSA', 'FROTA', 'CUSTO/KM', 'KM_TOTAL', 'KM/DIA', 'CUSTO_VIAGEM', 'CUSTO_TOTAL'
    ]
    empresas = df.groupby('EMPRESA').sum(numeric_only=True).reset_index()

    # Controlador de empresas
    controlador_empresas = st.sidebar.selectbox("Selecione a empresa:", options=empresas)

    # Filtrar o DataFrame com base na seleção
    if controlador_empresas == 'TODAS':
        df_filtered = df
    else:
        df_filtered = df[df['EMPRESA'] == controlador_empresas]


    df_linhas = df[df['EMPRESA'] == controlador_empresas]  # Filtrando o DataFrame
    linhas = df_linhas["LINHAS"].value_counts().sort_values(ascending=False).index  # Lista das linhas de ônibus
    linha = st.sidebar.selectbox("Selecione a linha:", options=linhas)  # Controlador de linhas
    linha_dados = df[df["LINHAS"] == linha]  # Filtrando o DataFrame


    analise = st.sidebar.selectbox('Selecione a coluna para análise:',
                                    options=['TODAS', 'PREVISTOS', 'REALIZADOS', 'TAXA_PARTIDA', 'KM_LINHA', 'KM_OCIOSA', 'FROTA', 'CUSTO/KM', 'KM_TOTAL', 'KM/DIA', 'CUSTO_VIAGEM', 'CUSTO_TOTAL'])


    # Criar a coluna DIA com valores de 22 a 28
    dias = [22, 23, 24, 25, 26, 27, 28]
    repeticoes = (len(df) // len(dias)) + 1
    df['DIA'] = (dias * repeticoes)[:len(df)]  # Garantir que o comprimento corresponda ao DataFrame

    # Transformar a coluna DIA em coluna de DATA
    df['DATA'] = pd.to_datetime(df['DIA'].astype(str) + '-06-2024', format='%d-%m-%Y')

    # Verificar se a coluna DATA está corretamente convertida
    assert df['DATA'].dtype == 'datetime64[ns]', "A coluna DATA não está no formato datetime"

    # Adicionar um slider de intervalo de datas na barra lateral
    data_inicial, data_final = st.sidebar.slider(
        'Selecione o intervalo de datas:',
        min_value=df['DATA'].min().date(),
        max_value=df['DATA'].max().date(),
        value=(df['DATA'].min().date(), df['DATA'].max().date()),
        format="DD-MM-YYYY"
    )

    # Filtrando o DataFrame com base nas seleções do usuário
    linha_dados = df[df["LINHAS"] == linha]  # Filtrando o DataFrame
    df_filtrado = linha_dados[(linha_dados['DATA'] >= pd.to_datetime(data_inicial)) & (linha_dados['DATA'] <= pd.to_datetime(data_final))]

    # Filtrando o DataFrame com base nas seleções do usuário
    df_filtrado = linha_dados[(linha_dados['DATA'] >= pd.to_datetime(data_inicial)) & (linha_dados['DATA'] <= pd.to_datetime(data_final))]
    # tarifa = obter_tarifa(pd.to_datetime(data_inicial), pd.to_datetime(data_final))

    df_filtrado = linha_dados[(linha_dados['DATA'] >= pd.to_datetime(data_inicial)) & (linha_dados['DATA'] <= pd.to_datetime(data_final))]
    # tarifa = obter_tarifa(pd.to_datetime(data_inicial), pd.to_datetime(data_final))
    ########################################################################################
    # Título da Página
    st.markdown(f"# *{linha}* :bus:") # Título da página
    st.markdown(f"### Empresa: *{controlador_empresas}*") # Exibindo a empresa selecionada
    ########################################################################################
    # Adição de metrícas
    # Adição de métricas
    valor_total = df_filtrado['CUSTO_TOTAL'].sum()

    valor_viagem = df_filtrado['CUSTO_VIAGEM'].sum()

    previstos = df_filtrado['PREVISTOS'].sum()

    realizados = df_filtrado['REALIZADOS'].sum()

    taxa_partida = df_filtrado['TAXA_PARTIDA'].mean()

    # Variação de passageiro equivalente
    km_dia = df_filtrado['KM/DIA'].sum()

    # Colunas das métricas
    col1, col2, col3, col4, col5, col6 = st.columns((1, 1, 1, 1, 1, 1))

    # Distribuição das métricas nas colunas
    # Apresentar na tela
    with st.container():
        with col1:     
            st.metric(
                label="Custo total no período",   
                value = "R$ {:,.2f}".format(valor_total).replace(',', 'X').replace('.', ',').replace('X', '.'),
            )

        with col2:     
            st.metric(
                label="Custo total por viagem",   
                value = "R$ {:,.2f}".format(valor_viagem).replace(',', 'X').replace('.', ',').replace('X', '.'),
            )

        with col3:     
            st.metric(
                label="Partidas Previstas",   
                value = "{:,.0f}".format(previstos).replace(',', 'X').replace('.', ',').replace('X', '.'),
            )

        with col4:     
            st.metric(
                label="Partidas Realizadas",   
                value = "{:,.0f}".format(realizados).replace(',', 'X').replace('.', ',').replace('X', '.'),
            )


        with col5:  
            st.metric(
                label="Índice de Cumprimento de viagem",   
                value = "{:,.2f} %".format(taxa_partida).replace(',', 'X').replace('.', ',').replace('X', '.'),
            )

        with col6: 
            st.metric(
                label="KM por dia no período",   
                value = "{:,.2f}".format(km_dia).replace(',', 'X').replace('.', ',').replace('X', '.'),
            )

    ########################################################################################
    # Adicionar o gráfico conforme a seleção do usuário

    df_filtrado.set_index('DATA', inplace=True)  # Define a coluna de datas como índice

    with st.container():

        st.markdown(f'## {controlador_empresas}')

        if analise == 'TODAS':
            with st.expander('DETALHAMENTO', expanded=True):
                st.dataframe(df_filtrado[colunas_para_somar], column_config={
                    #dropar coluna KM_TOTAL do df_filtrado

                    "PREVISTOS": st.column_config.ProgressColumn("PREVISTOS", format= "%.2f" ,min_value=0, max_value=float(df_filtrado['PREVISTOS'].max())),
                    
                    "REALIZADOS": st.column_config.ProgressColumn("REALIZADOS", format="%.2f" ,min_value=0, max_value=float(df_filtrado['REALIZADOS'].max())), 

                    "TAXA_PARTIDA": st.column_config.ProgressColumn("TAXA_PARTIDA", format="%.2f", min_value=0, max_value=float(df_filtrado['TAXA_PARTIDA'].max())), 

                    "KM/DIA": st.column_config.ProgressColumn("KM/DIA", format="%.2f", min_value=0, max_value=float(df_filtrado['KM/DIA'].max())), 

                    "CUSTO_VIAGEM": st.column_config.ProgressColumn("CUSTO_VIAGEM", format="%.2f", min_value=0, max_value=float(df_filtrado['CUSTO_VIAGEM'].max())), 

                    "CUSTO_TOTAL": st.column_config.ProgressColumn("RE", format="%.2f", min_value=0, max_value=float(df_filtrado['CUSTO_TOTAL'].max()))
                })

        else:
            pass


    # Configuração da barra lateral
    st.sidebar.markdown('Developer by: [Lucas Falcão](https://GitHub.com/Falkzera)')

############################################################################################################
elif selected == "Gool System":

    # Importnado planilhas
    df = pd.read_excel('data/SJ/GOOLSYSTEM.xlsx')

    # Converter coluna data para datetime

    colunas_para_somar = [
        'PREVISTOS', 'REALIZADOS', 'TAXA_PARTIDA', 'KM/DIA', 'CUSTO_VIAGEM', 'CUSTO_TOTAL'
    
    ]

    colunas_para_somar_2 = [
        'PREVISTOS', 'REALIZADOS', 'TAXA_PARTIDA', 'KM_LINHA', 'KM_OCIOSA', 'FROTA', 'CUSTO/KM', 'KM_TOTAL', 'KM/DIA', 'CUSTO_VIAGEM', 'CUSTO_TOTAL'
    
    ]

    ########################################################################################################################################
    empresas = df.groupby('EMPRESA').sum(numeric_only=True).reset_index()

    # Controlador de empresas
    controlador_empresas = st.sidebar.selectbox("Selecione a empresa:", options=empresas)

    # Filtrar o DataFrame com base na seleção
    if controlador_empresas == 'TODAS':
        df_filtered = df
    else:
        df_filtered = df[df['EMPRESA'] == controlador_empresas]


    df_linhas = df[df['EMPRESA'] == controlador_empresas]  # Filtrando o DataFrame
    linhas = df_linhas["LINHAS"].value_counts().sort_values(ascending=False).index  # Lista das linhas de ônibus
    linha = st.sidebar.selectbox("Selecione a linha:", options=linhas)  # Controlador de linhas
    linha_dados = df[df["LINHAS"] == linha]  # Filtrando o DataFrame


    analise = st.sidebar.selectbox('Selecione a coluna para análise:',
                                    options=['TODAS', 'PREVISTOS', 'REALIZADOS', 'TAXA_PARTIDA', 'KM_LINHA', 'KM_OCIOSA', 'FROTA', 'CUSTO/KM', 'KM_TOTAL', 'KM/DIA', 'CUSTO_VIAGEM', 'CUSTO_TOTAL'])


    # Criar a coluna DIA com valores de 22 a 28
    dias = [22, 23, 24, 25, 26, 27, 28]
    repeticoes = (len(df) // len(dias)) + 1
    df['DIA'] = (dias * repeticoes)[:len(df)]  # Garantir que o comprimento corresponda ao DataFrame

    # Transformar a coluna DIA em coluna de DATA
    df['DATA'] = pd.to_datetime(df['DIA'].astype(str) + '-06-2024', format='%d-%m-%Y')

    # Verificar se a coluna DATA está corretamente convertida
    assert df['DATA'].dtype == 'datetime64[ns]', "A coluna DATA não está no formato datetime"

    # Adicionar um slider de intervalo de datas na barra lateral
    data_inicial, data_final = st.sidebar.slider(
        'Selecione o intervalo de datas:',
        min_value=df['DATA'].min().date(),
        max_value=df['DATA'].max().date(),
        value=(df['DATA'].min().date(), df['DATA'].max().date()),
        format="DD-MM-YYYY"
    )

    # Filtrando o DataFrame com base nas seleções do usuário
    linha_dados = df[df["LINHAS"] == linha]  # Filtrando o DataFrame
    df_filtrado = linha_dados[(linha_dados['DATA'] >= pd.to_datetime(data_inicial)) & (linha_dados['DATA'] <= pd.to_datetime(data_final))]

    # Filtrando o DataFrame com base nas seleções do usuário
    df_filtrado = linha_dados[(linha_dados['DATA'] >= pd.to_datetime(data_inicial)) & (linha_dados['DATA'] <= pd.to_datetime(data_final))]
    # tarifa = obter_tarifa(pd.to_datetime(data_inicial), pd.to_datetime(data_final))

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
    valor_total = df_filtrado['CUSTO_TOTAL'].sum()

    valor_viagem = df_filtrado['CUSTO_VIAGEM'].sum()

    previstos = df_filtrado['PREVISTOS'].sum()

    realizados = df_filtrado['REALIZADOS'].sum()

    taxa_partida = df_filtrado['TAXA_PARTIDA'].mean()

    # Variação de passageiro equivalente
    km_dia = df_filtrado['KM/DIA'].sum()

    # Colunas das métricas
    col1, col2, col3, col4, col5, col6 = st.columns((1, 1, 1, 1, 1, 1))

    # Distribuição das métricas nas colunas
    # Apresentar na tela
    with st.container():
        with col1:     
            st.metric(
                label="Custo total no período",   
                value = "R$ {:,.2f}".format(valor_total).replace(',', 'X').replace('.', ',').replace('X', '.'),
            )

        with col2:     
            st.metric(
                label="Custo total por viagem",   
                value = "R$ {:,.2f}".format(valor_viagem).replace(',', 'X').replace('.', ',').replace('X', '.'),
            )

        with col3:     
            st.metric(
                label="Partidas Previstas",   
                value = "{:,.0f}".format(previstos).replace(',', 'X').replace('.', ',').replace('X', '.'),
            )

        with col4:     
            st.metric(
                label="Partidas Realizadas",   
                value = "{:,.0f}".format(realizados).replace(',', 'X').replace('.', ',').replace('X', '.'),
            )


        with col5:  
            st.metric(
                label="Índice de Cumprimento de viagem",   
                value = "{:,.2f} %".format(taxa_partida).replace(',', 'X').replace('.', ',').replace('X', '.'),
            )

        with col6: 
            st.metric(
                label="KM por dia no período",   
                value = "{:,.2f}".format(km_dia).replace(',', 'X').replace('.', ',').replace('X', '.'),
            )

    ########################################################################################
    # Adicionar o gráfico conforme a seleção do usuário

    df_filtrado.set_index('DATA', inplace=True)  # Define a coluna de datas como índice



    with st.container():

        st.markdown(f'## {controlador_empresas}')

        if analise == 'TODAS':
            with st.expander('DETALHAMENTO', expanded=True):
                st.dataframe(df_filtrado[colunas_para_somar], column_config={
                    #dropar coluna KM_TOTAL do df_filtrado

                    "PREVISTOS": st.column_config.ProgressColumn("PREVISTOS", format= "%.2f" ,min_value=0, max_value=float(df_filtrado['PREVISTOS'].max())),
                    
                    "REALIZADOS": st.column_config.ProgressColumn("REALIZADOS", format="%.2f" ,min_value=0, max_value=float(df_filtrado['REALIZADOS'].max())), 

                    "TAXA_PARTIDA": st.column_config.ProgressColumn("TAXA_PARTIDA", format="%.2f", min_value=0, max_value=float(df_filtrado['TAXA_PARTIDA'].max())), 

                    "KM/DIA": st.column_config.ProgressColumn("KM/DIA", format="%.2f", min_value=0, max_value=float(df_filtrado['KM/DIA'].max())), 

                    "CUSTO_VIAGEM": st.column_config.ProgressColumn("CUSTO_VIAGEM", format="%.2f", min_value=0, max_value=float(df_filtrado['CUSTO_VIAGEM'].max())), 

                    "CUSTO_TOTAL": st.column_config.ProgressColumn("RE", format="%.2f", min_value=0, max_value=float(df_filtrado['CUSTO_TOTAL'].max()))
                })

        else:
            pass

    # Configuração da barra lateral
    st.sidebar.markdown('Developer by: [Lucas Falcão](https://GitHub.com/Falkzera)')











# ############################################################################################################
elif selected == "Comparativo":

    # Converter coluna data para datetime

    colunas_para_somar = [
        'PREVISTOS', 'REALIZADOS', 'TAXA_PARTIDA', 'KM/DIA', 'CUSTO_VIAGEM', 'CUSTO_TOTAL'
    
    ]

    colunas_para_somar_2 = [
        'PREVISTOS', 'REALIZADOS', 'TAXA_PARTIDA', 'KM_LINHA', 'KM_OCIOSA', 'FROTA', 'CUSTO/KM', 'KM_TOTAL', 'KM/DIA', 'CUSTO_VIAGEM', 'CUSTO_TOTAL'
    
    ]

    ########################################################################################################################################

    # Carregar os dados
    df_empresa_bi = pd.read_excel('data/SJ/BI_EMPRESA.xlsx')
    df_empresa_gool = pd.read_excel('data/SJ/GOOLSYSTEM_EMPRESA.xlsx')

    # Selecionar a fonte de dados
    fonte = st.sidebar.selectbox("Selecione a fonte:", options=['Power BI', 'Gool System'])

    # if fonte == 'Power BI':
    #     empresas = df_empresa_bi['EMPRESA'].unique()
    #     df_selecionado = df_empresa_bi
    #     fonte_nome = "Power BI"
    # elif fonte == 'Gool System':
    #     empresas = df_empresa_gool['EMPRESA'].unique()
    #     df_selecionado = df_empresa_gool
    #     fonte_nome = "Gool System"


    empresas = df_empresa_bi['EMPRESA'].unique()
    df_selecionado = df_empresa_bi
    fonte_nome = "Power BI"

    # Controlador de empresas
    controlador_empresas = st.sidebar.selectbox("Selecione a empresa:", options=empresas)

    # Filtrar o DataFrame com base na empresa selecionada
    df_filtrado = df_selecionado[df_selecionado['EMPRESA'] == controlador_empresas]

    # Dividir a coluna 'TAXA_PARTIDA' por 100
    df_filtrado['TAXA_PARTIDA'] = df_filtrado['TAXA_PARTIDA']

    # Selecionar a coluna para análise
    analise = st.sidebar.selectbox('Selecione a coluna para análise:',
                                options=['TODAS', 'PREVISTOS', 'REALIZADOS', 'TAXA_PARTIDA', 'KM_LINHA', 'KM_OCIOSA', 'FROTA', 'CUSTO/KM', 'KM_TOTAL', 'KM/DIA', 'CUSTO_VIAGEM', 'CUSTO_TOTAL'])

    # Exibir a empresa e a fonte selecionadas
    st.markdown(f"### Empresa: *{controlador_empresas}*")
    st.markdown(f"### FONTE: {fonte_nome}")

    # Exibir os dados filtrados com base na coluna selecionada
    if analise == 'TODAS':
        st.dataframe(df_filtrado)
    else:
        st.dataframe(df_filtrado[[analise]])

    # Adição de metrícas
    # Adição de métricas
    valor_total = df_filtrado['CUSTO_TOTAL'].sum()

    valor_viagem = df_filtrado['CUSTO_VIAGEM'].sum()

    previstos = df_filtrado['PREVISTOS'].sum()

    realizados = df_filtrado['REALIZADOS'].sum()

    taxa_partida = df_filtrado['TAXA_PARTIDA'].mean() / 100

    # Variação de passageiro equivalente
    km_dia = df_filtrado['KM/DIA'].sum()

    # Colunas das métricas
    col1, col2, col3, col4, col5, col6 = st.columns((1, 1, 1, 1, 1, 1))

    # Distribuição das métricas nas colunas
    # Apresentar na tela
    with st.container():
        with col1:     
            st.metric(
                label="Custo total no período",   
                value = "R$ {:,.2f}".format(valor_total).replace(',', 'X').replace('.', ',').replace('X', '.'),
            )

        with col2:     
            st.metric(
                label="Custo total por viagem",   
                value = "R$ {:,.2f}".format(valor_viagem).replace(',', 'X').replace('.', ',').replace('X', '.'),
            )

        with col3:     
            st.metric(
                label="Partidas Previstas",   
                value = "{:,.0f}".format(previstos).replace(',', 'X').replace('.', ',').replace('X', '.'),
            )

        with col4:     
            st.metric(
                label="Partidas Realizadas",   
                value = "{:,.0f}".format(realizados).replace(',', 'X').replace('.', ',').replace('X', '.'),
            )

        with col5:  
            st.metric(
                label="Índice de Cumprimento de viagem",   
                value = "{:,.2f} %".format(taxa_partida).replace(',', 'X').replace('.', ',').replace('X', '.'),
            )

        with col6: 
            st.metric(
                label="KM por dia no período",   
                value = "{:,.2f}".format(km_dia).replace(',', 'X').replace('.', ',').replace('X', '.'),
            )

    
    # Configuração da barra lateral
    st.sidebar.markdown('Developer by: [Lucas Falcão](https://GitHub.com/Falkzera)')
