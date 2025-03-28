# estrutura multipage do Streamlit
# arquivo: app.py
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="InfoCoin", layout="wide")

st.sidebar.title("🧭 Navegação")
st.sidebar.page_link("app.py", label="🏠 Início", icon="🏠")
st.sidebar.page_link("pages/conversor.py", label="💱 Conversor de Moedas", icon="🔁")
st.sidebar.page_link("pages/historico.py", label="📈 Histórico de Cotações", icon="📊")

st.title("💰 InfoCoin – Painel de Moedas Globais")
st.markdown("Escolha uma funcionalidade no menu lateral para começar.")
