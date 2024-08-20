# Importação das bibliotecas
import pandas as pd
import streamlit as st
import Home.Credito as Credito


# Importnado planilhas
df = pd.read_csv('data/df_final.csv')
df['DATA'] = pd.to_datetime(df['DATA'])

# Adicionando em outras páginas
st.session_state['df'] = df


# Configuração da página
st.set_page_config(page_title="Intro", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

# Configuração do título
st.title('Dashboard:')
st.header('Transporte Público - Maceió/AL :bus: 📈')
st.button('Atualizar')

st.title("#")
  

st.subheader(" Sobre o projeto 🎯")
st.write(" Este projeto é um Dashboard interativo e dinâmico dedicado à análise do sistema de transporte público em Maceió/AL. O objetivo principal é fornecer uma visão abrangente e detalhada dos dados relacionados ao transporte público na cidade, facilitando a tomada de decisões e a identificação de áreas para melhorias.O projeto está em desenvolvimento e novas funcionalidades serão adicionadas em breve. ")
  
  
st.caption("Desenvolvido por: [Lucas Falcão](https://GitHub.com/Falkzera)")

with st.sidebar:
    Credito.display_credits()
   