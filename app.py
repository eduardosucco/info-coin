# arquivo: app.py
import streamlit as st

st.set_page_config(page_title="InfoCoin", layout="wide")

st.title("💰 InfoCoin – Painel de Moedas Globais")
st.markdown("Escolha uma das páginas no menu lateral para começar.")

# O Streamlit multipage não precisa de st.sidebar.page_link.
# Basta criar a pasta pages/ e colocar os arquivos .py lá.
# O próprio Streamlit gerencia o menu lateral automaticamente.
