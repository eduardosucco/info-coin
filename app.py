import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.write("# Conversor de Moedas com Histórico")

# Definindo as moedas disponíveis
MOEDAS = ["USD", "EUR", "BRL", "GBP", "JPY", "CNY"]

# Função para conversão utilizando a Frankfurter API
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

# Função para obter histórico de conversões nos últimos 'days' dias
def get_historico(from_currency: str, to_currency: str, days: int) -> pd.DataFrame:
    end_date = datetime.today()
    start_date = end_date - timedelta(days=days)
    rates = {}
    
    for n in range(days + 1):
        day = start_date + timedelta(days=n)
        day_str = day.strftime("%Y-%m-%d")
        url = f"https://api.frankfurter.app/{day_str}?from={from_currency}&to={to_currency}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            rate = data["rates"].get(to_currency)
            if rate:
                rates[day_str] = rate
        except requests.RequestException as e:
            st.error(f"Erro na data {day_str}: {e}")
    
    if rates:
        df = pd.DataFrame(list(rates.items()), columns=["Data", "Cotação"])
        df["Data"] = pd.to_datetime(df["Data"])
        df.sort_values("Data", inplace=True)
        return df
    else:
        return pd.DataFrame()

# Layout da Conversão
st.markdown("## Conversão de Moedas")
col1, col2, col3 = st.columns(3)
with col1:
    moeda_origem = st.selectbox("Moeda de origem", MOEDAS, index=MOEDAS.index("BRL"))
with col2:
    moeda_destino = st.selectbox("Moeda de destino", MOEDAS, index=MOEDAS.index("USD"))
with col3:
    valor = st.number_input("Valor a converter", min_value=0.0, value=2.0, step=0.01)

if st.button("Converter"):
    resultado = convert_currency(valor, moeda_origem, moeda_destino)
    if resultado:
        st.metric(f"{valor:.2f} {moeda_origem}", f"{resultado:.2f} {moeda_destino}")

st.markdown("---")

# Layout do Histórico
st.markdown("## Histórico de Conversão (últimos 7 dias)")
df_hist = get_historico(moeda_origem, moeda_destino, days=7)
if not df_hist.empty:
    fig = px.line(df_hist, x="Data", y="Cotação", 
                  title=f"Histórico: {moeda_origem} para {moeda_destino}")
    fig.update_layout(xaxis_title="Data", yaxis_title="Cotação")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("Não foi possível obter os dados históricos.")
