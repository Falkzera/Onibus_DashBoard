import streamlit as st
import pandas as pd
import plotly.express as px
import Home.Credito as Credito

# COnfiguração da página
st.set_page_config(page_title="Tarifa", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

df = pd.read_excel('data/Domingo/Gasto_Domingo.xlsx', sheet_name='GASTO_ANUAL')


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
    }, height=600, width=800)

########################################################################################################################################
with st.sidebar:
    Credito.display_credits()
   