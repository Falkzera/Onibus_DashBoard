import streamlit as st
import pandas as pd
import plotly.express as px
import Home.Credito as Credito

# COnfiguração da página
st.set_page_config(page_title="Tarifa", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

df = pd.read_excel('data/Domingo/Gasto_Domingo.xlsx', sheet_name='GASTO_ANUAL')


df['PREFEITO'] = 'KATIA BORN'
df.loc[df['ANO'] >= 2005, 'PREFEITO'] = 'CÍCERO ALMEIDA'
df.loc[df['ANO'] >= 2013, 'PREFEITO'] = 'RUI PALMEIRA'
df.loc[df['ANO'] >= 2017, 'PREFEITO'] = 'JHC'



st.title('Análise da série histórica tarifária de Maceió')
st.subheader('Considerando os dados de 1994 a 2024')
st.write('Análise da série histórica tarifária de Maceió, considerando os dados de 1994 a 2024. A análise é dividida em duas partes:')
st.write('1. Comparação Acumulada do Total Pago com e sem Gratuidades')
st.write('2. Comparação Acumulada do Gasto da Renda Anual')


########################################################################################################################################
with st.expander('Comparação Acumulada do Total Pago com e Gratuidades'):
    # Adicionar um selectbox para escolher entre série temporal e ano específico
    tipo_visualizacao = st.selectbox('Escolha o tipo de visualização', ['Série Temporal', 'Ano Específico'])

    # Adicionar um selectbox para escolher o tipo de gráfico
    if tipo_visualizacao == 'Ano Específico':
        tipo_grafico = 'Barra'  # Forçar o tipo de gráfico para 'Barra'
    else:
        tipo_grafico = st.selectbox('Escolha o tipo de gráfico', ['Barra', 'Linha'])

    # Se o usuário escolher "Ano Específico", adicionar um slider para escolher o ano
    if tipo_visualizacao == 'Ano Específico':
        ano_especifico = st.slider('Escolha o ano', min_value=1994, max_value=int(df['ANO'].max()), value=2017)
        df_filtered = df[df['ANO'] == ano_especifico]
    else:
        ano_inicial = st.slider('Ano Inicial', min_value=1994, max_value=int(df['ANO'].max()), value=2017)
        df_filtered = df[df['ANO'] >= ano_inicial]

    # Calcular a diferença e a porcentagem de economia
    total_pago = df_filtered['TOTAL_PAGO'].sum()
    total_pago_sem_domingos = df_filtered['TOTAL_PAGO_SEM_GRATUIDADE_DOMINGOS'].sum()
    economia_bruta = total_pago_sem_domingos - total_pago
    porcentagem_economia = (economia_bruta / total_pago_sem_domingos) * 100

    # Criar o gráfico com base na escolha do usuário
    if tipo_visualizacao == 'Ano Específico':
        fig = px.bar(df_filtered, x='ANO', y=['TOTAL_PAGO', 'TOTAL_PAGO_SEM_GRATUIDADE_DOMINGOS'],
                    labels={'value': 'Valores', 'variable': 'Tipo de Pagamento'},
                    title=f'Total Pago e Total Pago Sem Gratuidades no ano {ano_especifico}')
        fig.update_layout(xaxis_title='Ano', yaxis_title='Valores', barmode='group')  # Ajustar para barras agrupadas
        fig.update_traces(marker_line_width=1.5, marker_line_color='black')  # Ajustar a largura das barras

        st.plotly_chart(fig)

    else:
        if tipo_grafico == 'Barra':
            fig = px.bar(df_filtered, x='ANO', y=['TOTAL_PAGO', 'TOTAL_PAGO_SEM_GRATUIDADE_DOMINGOS'],
                         labels={'value': 'Valores', 'variable': 'Tipo de Pagamento'},
                         title=f'Comparação do Total Pago com e sem Gratuidades a partir do ano {ano_inicial}')
            fig.update_layout(xaxis_title='Ano', yaxis_title='Valores', barmode='stack')

        else:
            fig = px.line(df_filtered, x='ANO', y=['TOTAL_PAGO', 'TOTAL_PAGO_SEM_GRATUIDADE_DOMINGOS'],
                          labels={'value': 'Valores', 'variable': 'Tipo de Pagamento'},
                          title=f'Comparação do Total Pago com e sem Gratuidades a partir do ano {ano_inicial}')
            fig.update_layout(xaxis_title='Ano', yaxis_title='Valores')
        

        # Renderizar o gráfico no Streamlit
        st.plotly_chart(fig)

    # Mostrar a economia
    st.write(f'Para o período a partir de {ano_inicial if tipo_visualizacao == "Série Temporal" else ano_especifico}, o cidadão economizou R$ {economia_bruta:.2f}, o que representa uma economia de {porcentagem_economia:.2f}%.')
########################################################################################################################################


########################################################################################################################################
with st.expander('Comparação Acumulada do Gasto da Renda Anual'):
    # Adicionar um selectbox para escolher o tipo de gráfico
    tipo_grafico_2 = st.selectbox('Escolha o tipo de gráfico', ['Barra', 'Linha'], key='tipo_grafico_2')

    # Adicionar um slider para escolher o ano inicial
    ano_inicial_2 = st.slider('Ano Inicial', min_value=1994, max_value=int(df['ANO'].max()), value=1994, key='ano_inicial_2')
    df_filtered_2 = df[df['ANO'] >= ano_inicial_2]

    # Calcular a proporção de TOTAL_PAGO em relação ao SALARIO_MINIMO_ANUAL
    df_filtered_2['GASTO_RENDA_ANUAL'] = (df_filtered_2['TOTAL_PAGO'] / df_filtered_2['SALARIO_MINIMO_ANUAL']) * 100

    # Calcular a diferença e a porcentagem de economia
    total_pago_2 = df_filtered_2['TOTAL_PAGO'].sum()
    total_pago_sem_domingos_2 = df_filtered_2['TOTAL_PAGO_SEM_GRATUIDADE_DOMINGOS'].sum()
    economia_bruta_2 = total_pago_sem_domingos_2 - total_pago_2
    porcentagem_economia_2 = (economia_bruta_2 / total_pago_sem_domingos_2) * 100

    # Criar o gráfico com base na escolha do usuário
    if tipo_grafico_2 == 'Barra':
        fig_2 = px.bar(df_filtered_2, x='ANO', y='GASTO_RENDA_ANUAL',
                     labels={'GASTO_RENDA_ANUAL': 'Proporção do Gasto da Renda Anual', 'ANO': 'Ano'},
                     title=f'Proporção do Gasto da Renda Anual a partir do ano {ano_inicial_2}')
        fig_2.update_layout(xaxis_title='Ano', yaxis_title='Proporção do Gasto da Renda Anual', barmode='stack')
        st.write(f'Para o período a partir de {ano_inicial_2}, o cidadão gastou em média {df_filtered_2["GASTO_RENDA_ANUAL"].mean():.2f}% da sua renda anual com tarifa.')

    else:
        fig_2 = px.line(df_filtered_2, x='ANO', y='GASTO_RENDA_ANUAL',
                      labels={'GASTO_RENDA_ANUAL': 'Proporção do Gasto da Renda Anual', 'ANO': 'Ano'},
                      title=f'Proporção do Gasto da Renda Anual a partir do ano {ano_inicial_2}')
        fig_2.update_layout(xaxis_title='Ano', yaxis_title='Proporção do Gasto da Renda Anual')
        st.write(f'Para o período a partir de {ano_inicial_2}, o cidadão gastou em média {df_filtered_2["GASTO_RENDA_ANUAL"].mean():.2f}% da sua renda anual com tarifa.')


    # Renderizar o gráfico no Streamlit
    st.plotly_chart(fig_2)

    # Mostrar a mensagem


    df_filtered_2['GASTO_RENDA_ANUAL'] = df_filtered_2['GASTO_RENDA_ANUAL'].apply(lambda x: f'{x:.2f}%')
    # Calcular a coluna 'GASTO_RENDA_ANUAL'
    df_filtered_2['GASTO_RENDA_ANUAL'] = (df_filtered_2['TOTAL_PAGO'] / df_filtered_2['SALARIO_MINIMO_ANUAL']) * 100

    # Verificar se a coluna 'GASTO_RENDA_ANUAL' está no formato numérico
    if not pd.api.types.is_numeric_dtype(df_filtered_2['GASTO_RENDA_ANUAL']):
        df_filtered_2['GASTO_RENDA_ANUAL'] = pd.to_numeric(df_filtered_2['GASTO_RENDA_ANUAL'], errors='coerce')

    # Remover o índice
    df_filtered_2.reset_index(drop=True, inplace=True)

    # Formatar a coluna 'ANO' como string para evitar vírgulas
    df_filtered_2['ANO'] = df_filtered_2['ANO'].astype(str)

    # Usar st.dataframe com colunas de progresso e expandir o tamanho
    st.dataframe(df_filtered_2[['ANO', 'GASTO_RENDA_ANUAL']], column_config={
        "GASTO_RENDA_ANUAL": st.column_config.ProgressColumn(
            "Gasto da Renda Anual (%)", 
            format="%.2f%%", 
            min_value=0, 
            max_value=float(df_filtered_2['GASTO_RENDA_ANUAL'].max())
        )
    }, height=500, width=900)

########################################################################################################################################   
########################################################################################################################################



# Configuração da página

# Título
st.title('Transporte Público - Prefeitura de Maceió :bus:')
st.subheader("Comparativo do percentual de gastos anuais com transporte público em Maceió por gestão")
with st.expander('Sobre o Projeto', expanded=True):
    st.subheader('Objetivo:')
    st.write('O objetivo central é visualizar o quanto que os cidadões Maceioenses precisam desembolsar anualmente, com base no salário minimo de cada época, para se locomover através do Transporte Público de Maceió. Foi considerado duas passagens por dia (Ida e Volta, de domingo a domingo) e adicionado o cenário de dependentes: (01 filho, 02 filhos e 03 filhos).')
    st.write('Considerando o salário minimo de cada época, foi calculado o percentual do salário minimo que o cidadão precisaria desembolsar para se locomover através do transporte público de Maceió.')


with st.container():
    # Carregar o novo DataFrame
    df_novo = pd.read_excel("data/GASTOS_GROUPED.xlsx")
    # Remover de PREFEITO as '[]' e as aspas
    df_novo['PREFEITO'] = df_novo['PREFEITO'].str.replace('[', '').str.replace(']', '').str.replace("'", '')

    # Colunas de gasto para comparação
    colunas_gasto1 = ['GASTO_1_PESSOA_FILHO_3_PERCENT', 'GASTO_1_PESSOA_FILHO_2_PERCENT', 'GASTO_1_PESSOA_FILHO_1_PERCENT', 'GASTO_ANUAL_SEM_FILHO_PERCENT']
    colunas_gasto = ['3 filhos', '2 filhos', '1 filho', 'sem filhos']

    mapeamento_colunas = dict(zip(colunas_gasto1, colunas_gasto))

    # Renomear as colunas no DataFrame
    df_novo.rename(columns=mapeamento_colunas, inplace=True)

    # Adicionar um selectbox para selecionar a coluna a ser visualizada
    coluna_selecionada = st.selectbox('Selecione os cenários', colunas_gasto)

    # Adicionar um slider para filtrar o DataFrame por ano
    ano_inicial = st.slider('Selecione o périodo de análise', min_value=2000, max_value=2024, value=2000)
    df_novo = df_novo[df_novo['ANO'] >= ano_inicial]

    # Fazer a comparação de gestão para a coluna selecionada
    df_gestao = df_novo.groupby(['PREFEITO', 'ANO'])[coluna_selecionada].mean().reset_index()

    # Ordenar os prefeitos pelos seus anos de gestão
    df_gestao = df_gestao.sort_values(by='ANO')

    # Adicionar uma checkbox para permitir a seleção de exibir pontos ou não
    exibir_pontos = st.checkbox('Exibir pontos no gráfico', value=True)

    # Criar o gráfico de linha com ou sem pontos
    fig_gestao = px.line(df_gestao, x='ANO', y=coluna_selecionada, color='PREFEITO',
                        labels={coluna_selecionada: f'Proporção do Gasto ({coluna_selecionada})', 'ANO': 'Ano de Gestão'},
                        title=f'Proporção do gasto anual com transporte público possuíndo {coluna_selecionada} por gestão ao Longo dos Anos',
                        markers=exibir_pontos)

    # Adicionar anotações de texto para cada ponto, se a opção de exibir pontos estiver selecionada
    if exibir_pontos:
        for i in range(len(df_gestao)):
            fig_gestao.add_annotation(x=df_gestao['ANO'][i], y=df_gestao[coluna_selecionada][i],
                                    text=f"{df_gestao[coluna_selecionada][i]:.2f}%",
                                    showarrow=True, arrowhead=2, ax=0, ay=-20)

    # Atualizar a cor da linha para cada prefeito
    fig_gestao.for_each_trace(
        lambda trace: trace.update(line=dict(color='green')) if trace.name == 'JHC' else (
            trace.update(line=dict(color='darkred')) if trace.name == 'KATIA BORN' else (
                trace.update(line=dict(color='red')) if trace.name == 'CÍCERO ALMEIDA' else (
                    trace.update(line=dict(color='darkorange')) if trace.name == 'RUI PALMEIRA' else ()
                )
            )
        )
    )

    fig_gestao.update_layout(xaxis_title=None, yaxis_title=None)
    st.plotly_chart(fig_gestao)

# Adicionar um selectbox para escolher entre visualizar por prefeito ou por ano
opcao_visualizacao = st.selectbox('Escolha a visualização', ['Por Prefeito', 'Por Ano'])

df_novo = df_novo.sort_values(by=['ANO', 'PREFEITO'])

if opcao_visualizacao == 'Por Prefeito':
    # Calcular a média dos indicadores por prefeito
    df_media_prefeito = df_novo.groupby('PREFEITO').mean().reset_index()
    
    # Definir a ordem específica dos prefeitos
    ordem_prefeitos = ['KATIA BORN', 'CÍCERO ALMEIDA', 'RUI PALMEIRA', 'JHC']
    df_media_prefeito['PREFEITO'] = pd.Categorical(df_media_prefeito['PREFEITO'], categories=ordem_prefeitos, ordered=True)
    df_media_prefeito = df_media_prefeito.sort_values('PREFEITO')
    
    # Exibir os dados tabulados por prefeito com colunas de progresso
    st.dataframe(df_media_prefeito[['PREFEITO', '3 filhos', '2 filhos', '1 filho', 'sem filhos']], column_config={
        "3 filhos": st.column_config.ProgressColumn(
            "Gasto da Renda Anual (3 filhos)", 
            format="%.2f%%", 
            min_value=0, 
            max_value=float(df_media_prefeito['3 filhos'].max())
        ),
        "2 filhos": st.column_config.ProgressColumn(
            "Gasto da Renda Anual (2 filhos)", 
            format="%.2f%%", 
            min_value=0, 
            max_value=float(df_media_prefeito['2 filhos'].max())
        ),
        "1 filho": st.column_config.ProgressColumn(
            "Gasto da Renda Anual (1 filho)", 
            format="%.2f%%", 
            min_value=0, 
            max_value=float(df_media_prefeito['1 filho'].max())
        ),
        "sem filhos": st.column_config.ProgressColumn(
            "Gasto da Renda Anual (sem filhos)", 
            format="%.2f%%", 
            min_value=0, 
            max_value=float(df_media_prefeito['sem filhos'].max())
        )
    }, height=178, width=1500)
else:
    # Exibir os dados tabulados por ano com colunas de progresso
    df_novo['ANO'] = df_novo['ANO'].astype(str).str.replace(',', '')
    st.dataframe(df_novo[['ANO', 'PREFEITO', '3 filhos', '2 filhos', '1 filho', 'sem filhos']], column_config={
        "3 filhos": st.column_config.ProgressColumn(
            "Gasto da Renda Anual (3 filhos)", 
            format="%.2f%%", 
            min_value=0, 
            max_value=float(df_novo['3 filhos'].max())
        ),
        "2 filhos": st.column_config.ProgressColumn(
            "Gasto da Renda Anual (2 filhos)", 
            format="%.2f%%", 
            min_value=0, 
            max_value=float(df_novo['2 filhos'].max())
        ),
        "1 filho": st.column_config.ProgressColumn(
            "Gasto da Renda Anual (1 filho)", 
            format="%.2f%%", 
            min_value=0, 
            max_value=float(df_novo['1 filho'].max())
        ),
        "sem filhos": st.column_config.ProgressColumn(
            "Gasto da Renda Anual (sem filhos)", 
            format="%.2f%%", 
            min_value=0, 
            max_value=float(df_novo['sem filhos'].max())
        )
    }, height=913, width=1500)

    st.write('De acordo com os dados, é nítido que a gestão do Prefeito JHC foi o que mais benéficiou os cidadão Maceioense com o transporte público, em comparação com as gestões anteriores.')
    st.write('Diversas políticas públicas foram empregadas durante esse período, como a implantação do Domingo é Livre e o Passa Gratuito para estudantes e diversas opções de integração entre linhas.')

# Expander para formato tabular por prefeito
with st.expander('Formato tabular por prefeito'):
    # Calcular a média dos indicadores por prefeito
    df_media_prefeito = df_novo.groupby('PREFEITO').mean().reset_index()
    
    # Definir a ordem específica dos prefeitos
    ordem_prefeitos = ['KATIA BORN', 'CÍCERO ALMEIDA', 'RUI PALMEIRA', 'JHC']
    df_media_prefeito['PREFEITO'] = pd.Categorical(df_media_prefeito['PREFEITO'], categories=ordem_prefeitos, ordered=True)
    df_media_prefeito = df_media_prefeito.sort_values('PREFEITO')
    
    # Formatar os valores com duas casas decimais e adicionar o sinal de %
    df_media_prefeito[['3 filhos', '2 filhos', '1 filho', 'sem filhos']] = df_media_prefeito[['3 filhos', '2 filhos', '1 filho', 'sem filhos']].applymap(lambda x: f"{x:.2f}%")
    
    # Exibir os dados tabulados por prefeito sem a coluna de índice
    st.table(df_media_prefeito[['PREFEITO', '3 filhos', '2 filhos', '1 filho', 'sem filhos']])

# Expander para formato tabular por ano
with st.expander('Formato tabular por ano'):
    # Remover a vírgula dos anos
    df_novo['ANO'] = df_novo['ANO'].astype(str).str.replace(',', '')
    
    # Formatar os valores com duas casas decimais e adicionar o sinal de %
    df_novo[['3 filhos', '2 filhos', '1 filho', 'sem filhos']] = df_novo[['3 filhos', '2 filhos', '1 filho', 'sem filhos']].applymap(lambda x: f"{x:.2f}%")
    
    # Exibir os dados tabulados por ano
    st.table(df_novo[['ANO', 'PREFEITO', '3 filhos', '2 filhos', '1 filho', 'sem filhos']])

# créditos
with st.sidebar:
    Credito.display_credits()