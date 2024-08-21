########################################################################################################################################
# Importação das bibliotecas
import pandas as pd
import streamlit as st
import Home.Credito as Credito

st.set_page_config(page_title="Empresas", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

# Importando planilhas
df = pd.read_csv('data/df_final.csv')
df['DATA'] = pd.to_datetime(df['DATA'])

df_tarifas = pd.read_csv("data/TARIFA.csv")
df_tarifas['DATA'] = pd.to_datetime(df_tarifas['DATA'], errors='coerce')
df_tarifas['TARIFA'] = df_tarifas['TARIFA'].str.replace(',', '.').astype(float)

st.title('Análise Geral das Empresas 🚌')

# Colunas para realizar cálculos
colunas_para_somar = ['QR / EMV', 'PAGANTE', 'VT', 'ESCOLAR', 'GRATUIDADE', 'PASSE LIVRE', 'DL+INT.VT', 'INT.ESC', 'TOTAL', 'EQUIVALENTE']

with st.container():
    st.subheader("Filtros:")

    col1, col2, col3, col4 = st.columns(4)

    with col1:  # Selecionar a empresa desejada. Por padrão vem todas
        ativo = st.selectbox('Selecione a empresa desejada:', options=['TODAS'] + list(df['EMPRESA'].unique()))

    with col2:  # Selecionar a coluna para análise
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

# Função para obter a tarifa com base no período selecionado
def obter_tarifa(data_inicial, data_final):
    tarifa_filtrada = df_tarifas[(df_tarifas['DATA'] >= data_inicial) & (df_tarifas['DATA'] <= data_final)]
    if not tarifa_filtrada.empty:
        return tarifa_filtrada['TARIFA'].iloc[-1]  # Pega a tarifa mais recente dentro do intervalo
    else:
        return None  # Retorna None se não houver tarifas no intervalo

# Obter a tarifa com base nas datas selecionadas
tarifa = obter_tarifa(data_inicial, data_final)

# Realizar o cálculo da receita com base na tarifa e no número de passageiros
def calcular_receita(df, tarifa):
    if tarifa is not None:
        # Convertendo colunas para numérico
        df['QR / EMV'] = pd.to_numeric(df['QR / EMV'], errors='coerce')
        df['PAGANTE'] = pd.to_numeric(df['PAGANTE'], errors='coerce')
        df['VT'] = pd.to_numeric(df['VT'], errors='coerce')
        df['ESCOLAR'] = pd.to_numeric(df['ESCOLAR'], errors='coerce')
        df['GRATUIDADE'] = pd.to_numeric(df['GRATUIDADE'], errors='coerce')
        df['PASSE LIVRE'] = pd.to_numeric(df['PASSE LIVRE'], errors='coerce')
        df['DL+INT.VT'] = pd.to_numeric(df['DL+INT.VT'], errors='coerce')
        df['INT.ESC'] = pd.to_numeric(df['INT.ESC'], errors='coerce')

        df['RECEITA_QR_EMV'] = df['QR / EMV'] * tarifa
        df['RECEITA_PAGANTE'] = df['PAGANTE'] * tarifa
        df['RECEITA_VT'] = df['VT'] * tarifa
        df['RECEITA_ESCOLAR'] = df['ESCOLAR'] * (tarifa * 0.5)
        df['RECEITA_GRATUIDADE'] = df['GRATUIDADE'] * 0
        df['RECEITA_PASSE_LIVRE'] = df['PASSE LIVRE'] * 0
        df['RECEITA_DL_INT_VT'] = df['DL+INT.VT'] * 0
        df['RECEITA_INT_ESC'] = df['INT.ESC'] * 0
        df['RECEITA_TOTAL'] = df[['RECEITA_QR_EMV', 'RECEITA_PAGANTE', 'RECEITA_VT', 'RECEITA_ESCOLAR', 'RECEITA_GRATUIDADE', 'RECEITA_PASSE_LIVRE', 'RECEITA_DL_INT_VT', 'RECEITA_INT_ESC']].sum(axis=1)
    else:
        df['RECEITA_TOTAL'] = 0
    return df

# Calcular a receita
df_filtrado = calcular_receita(df_filtrado, tarifa)

receita_qr_emv = df_filtrado['RECEITA_QR_EMV'].sum()
receita_pagante = df_filtrado['RECEITA_PAGANTE'].sum()
receita_vt = df_filtrado['RECEITA_VT'].sum()
receita_escolar = df_filtrado['RECEITA_ESCOLAR'].sum()
receita_gratuidade = df_filtrado['RECEITA_GRATUIDADE'].sum()
receita_passe_livre = df_filtrado['RECEITA_PASSE_LIVRE'].sum()
receita_dl_int_vt = df_filtrado['RECEITA_DL_INT_VT'].sum()
receita_int_esc = df_filtrado['RECEITA_INT_ESC'].sum()

# st.write(f"Receita QR / EMV: R$ {receita_qr_emv:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
# st.write(f"Receita Pagante: R$ {receita_pagante:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
# st.write(f"Receita VT: R$ {receita_vt:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
# st.write(f"Receita Escolar: R$ {receita_escolar:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
# st.write(f"Receita Gratuidade: R$ {receita_gratuidade:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
# st.write(f"Receita Passe Livre: R$ {receita_passe_livre:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
# st.write(f"Receita DL+INT.VT: R$ {receita_dl_int_vt:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
# st.write(f"Receita INT.ESC: R$ {receita_int_esc:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
# st.write(f"Receita Total: R$ {df_filtrado['RECEITA_TOTAL'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))


# ['TODAS', 'QR / EMV', 'PAGANTE', 'VT', 'ESCOLAR', 'GRATUIDADE', 'PASSE LIVRE', 'DL+INT.VT', 'INT.ESC', 'TOTAL', 'EQUIVALENTE', 'RECEITA'])

if analise == 'RECEITA':
    st.write(f"Receita Total: R$ {df_filtrado['RECEITA_TOTAL'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
elif analise == 'QR / EMV':
    st.write(f"Receita QR / EMV: R$ {receita_qr_emv:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
elif analise == 'PAGANTE':
    st.write(f"Receita Pagante: R$ {receita_pagante:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
elif analise == 'VT':
    st.write(f"Receita VT: R$ {receita_vt:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
elif analise == 'ESCOLAR':
    st.write(f"Receita Escolar: R$ {receita_escolar:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
elif analise == 'GRATUIDADE':
    st.write(f"Receita Gratuidade: R$ {receita_gratuidade:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
elif analise == 'PASSE LIVRE':
    st.write(f"Receita Passe Livre: R$ {receita_passe_livre:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
elif analise == 'DL+INT.VT':
    st.write(f"Receita DL+INT.VT: R$ {receita_dl_int_vt:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
elif analise == 'INT.ESC':
    st.write(f"Receita INT.ESC: R$ {receita_int_esc:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
elif analise == 'TOTAL':
    st.write(f"Receita Total: R$ {df_filtrado['RECEITA_TOTAL'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
elif analise == 'EQUIVALENTE':
    st.write(f"Receita Total Equivalente: R$ {df_filtrado['EQUIVALENTE'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

    


########################################################################################################################################
# MÉTRICAS DE RECEITA, PASSAGEIROS TOTAIS E EQUIVALENTES.

with st.expander("Métricas de Receita, Passageiros Totais e Passageiros Equivalentes"):
    st.write("Aqui você encontra as métricas de Receita, Passageiros Totais e Passageiros Equivalentes para o período selecionado.")
    error = False
    try:
        valor_total = df_filtrado['RECEITA_TOTAL'].sum()
        passageiro_total = df_filtrado['TOTAL'].sum()
        equivalente_total = df_filtrado['EQUIVALENTE'].sum()

        col1, col2, col3 = st.columns(3)

        # Apresentar na tela
        with st.container():
            with col1:
                st.metric(
                    label="Receita total no período",
                    value="R$ {:,.2f}".format(valor_total).replace(',', 'X').replace('.', ',').replace('X', '.'))

            with col2:
                st.metric(
                    label="Passageiro total no período",
                    value="{:,.2f}".format(passageiro_total).replace(',', 'X').replace('.', ',').replace('X', '.'))

            with col3:
                st.metric(
                    label="Passageiro total equivalente no período",
                    value="{:,.2f}".format(equivalente_total).replace(',', 'X').replace('.', ',').replace('X', '.'))
    except:
        st.error('Não existe dados para o período informado', icon="🚨")
        error = True

########################################################################################################################################
# VISUALIZAÇÃO GRÁFICA
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
with st.sidebar:
    Credito.display_credits()