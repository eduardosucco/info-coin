import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

MOEDAS = ['USD', 'EUR', 'BRL', 'GBP', 'JPY', 'CNY']
BASE_URL = 'https://api.exchangerate.host/'

def get_cotacao(moeda_base='USD', moeda_destino='BRL'):
    url = f"{BASE_URL}latest?base={moeda_base}&symbols={moeda_destino}"
    resp = requests.get(url).json()
    return resp['rates'][moeda_destino]

def get_historico(moeda_base, moeda_destino, dias=30):
    data_final = datetime.today()
    data_inicial = data_final - timedelta(days=dias)
    url = f"{BASE_URL}timeseries?start_date={data_inicial.date()}&end_date={data_final.date()}&base={moeda_base}&symbols={moeda_destino}"
    resp = requests.get(url).json()
    df = pd.DataFrame(resp['rates']).T
    df.index = pd.to_datetime(df.index)
    df.columns = [f"{moeda_base}_{moeda_destino}"]
    return df

st.title("💱 Painel de Moedas Globais")

moeda_origem = st.selectbox("Moeda de origem", MOEDAS, index=2)
moeda_destino = st.selectbox("Moeda de destino", MOEDAS, index=0)

cotacao = get_cotacao(moeda_origem, moeda_destino)
st.metric(f"1 {moeda_origem} = ", f"{cotacao:.2f} {moeda_destino}")

df_hist = get_historico(moeda_origem, moeda_destino)
fig = px.line(df_hist, title=f"Histórico: {moeda_origem} → {moeda_destino}")
st.plotly_chart(fig, use_container_width=True)
