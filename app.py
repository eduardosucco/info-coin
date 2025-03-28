import streamlit as st
import requests

st.write("# Conversor de Moedas - Frankfurter API")

def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
    url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data["rates"].get(to_currency)
    except requests.RequestException as e:
        st.error(f"Erro ao converter: {e}")
        return None

MOEDAS = ["USD", "EUR", "BRL", "GBP", "JPY", "CNY"]

col1, col2, col3 = st.columns(3)
with col1:
    moeda_origem = st.selectbox("Moeda de origem", MOEDAS, index=MOEDAS.index("BRL"))
with col2:
    moeda_destino = st.selectbox("Moeda de destino", MOEDAS, index=MOEDAS.index("USD"))
with col3:
    valor = st.number_input("Valor a converter", min_value=0.0, value=2.0, step=0.01)

st.markdown("---")
cotacao = convert_currency(valor, moeda_origem, moeda_destino)
if cotacao:
    st.metric(f"{valor:.2f} {moeda_origem} =", f"{cotacao:.2f} {moeda_destino}")
else:
    st.error("⚠️ Não foi possível obter a cotação no momento.")
