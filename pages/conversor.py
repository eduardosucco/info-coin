import streamlit as st
import requests

st.set_page_config(page_title="Conversor de Moedas", layout="wide")

MOEDAS = ['USD', 'EUR', 'BRL', 'GBP', 'JPY', 'CNY']
API_KEY = "548c578e049658862fbd73d4"
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}"

def get_cotacao(moeda_base, moeda_destino):
    url = f"{BASE_URL}/latest/{moeda_base}"
    try:
        resp = requests.get(url).json()
        if resp['result'] == 'success':
            return resp['conversion_rates'].get(moeda_destino)
        return None
    except:
        return None

st.title("💱 Conversor de Moedas")

col1, col2, col3 = st.columns(3)
with col1:
    moeda_origem = st.selectbox("Moeda de origem", MOEDAS, index=2)
with col2:
    moeda_destino = st.selectbox("Moeda de destino", MOEDAS, index=0)
with col3:
    valor = st.number_input("Valor a converter", min_value=0.0, value=1.0, step=0.01)

cotacao = get_cotacao(moeda_origem, moeda_destino)

if cotacao:
    convertido = valor * cotacao
    st.metric(f"{valor:.2f} {moeda_origem} = ", f"{convertido:.2f} {moeda_destino}")
else:
    st.warning("⚠️ Não foi possível obter a cotação.")
