import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

MOEDAS = ['USD', 'EUR', 'BRL', 'GBP', 'JPY', 'CNY']

# ✅ API de cotação atual com chave
API_KEY = "548c578e049658862fbd73d4"
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}"

def get_cotacao(moeda_base='USD', moeda_destino='BRL'):
    url = f"{BASE_URL}/latest/{moeda_base}"
    try:
        resp = requests.get(url).json()
        if resp['result'] == 'success':
            return resp['conversion_rates'].get(moeda_destino)
        else:
            st.error("❌ Erro ao buscar cotação.")
            st.json(resp)
            return None
    except Exception as e:
        st.error(f"Erro na API: {e}")
        return None

# ❌ Comentado pois essa API não fornece histórico gratuito
# def get_historico(moeda_base, moeda_destino, dias=30):
#     data_final = datetime.today()
#     data_inicial = data_final - timedelta(days=dias)
#     url = f"{BASE_URL}timeseries?start_date={data_inicial.date()}&end_date={data_final.date()}&base={moeda_base}&symbols={moeda_destino}"
#     resp = requests.get(url).json()
#     df = pd.DataFrame(resp['rates']).T
#     df.index = pd.to_datetime(df.index)
#     df.columns = [f"{moeda_base}_{moeda_destino}"]
#     return df

st.title("💱 Painel de Moedas Globais")

col1, col2 = st.columns(2)
with col1:
    moeda_origem = st.selectbox("Moeda de origem", MOEDAS, index=2)
with col2:
    moeda_destino = st.selectbox("Moeda de destino", MOEDAS, index=0)

cotacao = get_cotacao(moeda_origem, moeda_destino)

if cotacao:
    st.metric(f"1 {moeda_origem} = ", f"{cotacao:.4f} {moeda_destino}")
else:
    st.warning("⚠️ Cotação não disponível no momento.")

# Aviso sobre histórico
st.info("📉 A API gratuita usada não fornece histórico. Para visualizar histórico e previsões, será necessário integrar uma nova fonte de dados como o Alpha Vantage, Yahoo Finance ou Exchangerate.host.")
