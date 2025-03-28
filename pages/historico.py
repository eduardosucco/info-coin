import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="Histórico de Cotações", layout="wide")

MOEDAS = ['USD', 'EUR', 'BRL', 'GBP', 'JPY', 'CNY']
API_URL = "https://api.exchangerate.host"

def get_historico(moeda_base, moeda_destino, dias):
    data_final = datetime.today()
    data_inicial = data_final - timedelta(days=dias)
    url = f"{API_URL}/timeseries?start_date={data_inicial.date()}&end_date={data_final.date()}&base={moeda_base}&symbols={moeda_destino}"
    resp = requests.get(url).json()
    if not resp.get("success", False):
        return None
    df = pd.DataFrame(resp['rates']).T
    df.index = pd.to_datetime(df.index)
    df.columns = [f"{moeda_base}_{moeda_destino}"]
    df = df.sort_index()
    return df

st.title("📈 Histórico de Cotações")

col1, col2 = st.columns(2)
with col1:
    moeda_origem = st.selectbox("Moeda de origem", MOEDAS, index=2)
with col2:
    moeda_destino = st.selectbox("Moeda de destino", MOEDAS, index=0)

periodo = st.selectbox(
    "Período",
    options={
        "1d": 1,
        "3d": 3,
        "5d": 5,
        "1s (1 semana)": 7,
        "2s (2 semanas)": 14,
        "1m (1 mês)": 30,
        "3m (3 meses)": 90
    }.keys()
)

dias = {
    "1d": 1,
    "3d": 3,
    "5d": 5,
    "1s (1 semana)": 7,
    "2s (2 semanas)": 14,
    "1m (1 mês)": 30,
    "3m (3 meses)": 90
}[periodo]

df_hist = get_historico(moeda_origem, moeda_destino, dias)

if df_hist is not None and not df_hist.empty:
    fig = px.line(df_hist, title=f"Histórico de {moeda_origem} para {moeda_destino} ({periodo})")
    fig.update_layout(xaxis_title="Data", yaxis_title="Cotação")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("📉 Dados históricos não disponíveis.")
