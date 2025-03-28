import streamlit as st
from utils import MOEDAS, get_cotacao

st.write("# Conversor de Moedas")

col1, col2, col3 = st.columns(3)
with col1:
    moeda_origem = st.selectbox("Moeda de origem", MOEDAS, index=MOEDAS.index("BRL"))
with col2:
    moeda_destino = st.selectbox("Moeda de destino", MOEDAS, index=MOEDAS.index("USD"))
with col3:
    valor = st.number_input("Valor a converter", min_value=0.0, value=2.0, step=0.01)

st.markdown("---")
cotacao = get_cotacao(moeda_origem, moeda_destino)
if cotacao:
    convertido = valor * cotacao
    st.metric(f"{valor:.2f} {moeda_origem} =", f"{convertido:.2f} {moeda_destino}")
else:
    st.error("⚠️ Não foi possível obter a cotação no momento.")
