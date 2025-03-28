import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# Configuração global da página
st.set_page_config(page_title="Conversor & Histórico de Moedas"
                #    , layout="wide"
                   , page_icon="💱")
st.title("💱 Conversor de Moedas com Histórico")
st.markdown("Realize conversões e visualize o histórico dos últimos 7 dias de forma intuitiva.")

# Lista de moedas disponíveis
MOEDAS = ["USD", "EUR", "BRL", "GBP", "JPY", "CNY"]

@st.cache_data(show_spinner=False)
def convert_currency(amount: float, from_currency: str, to_currency: str):
    """Converte um valor de uma moeda para outra utilizando a Frankfurter API."""
    url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()["rates"].get(to_currency)
    except Exception as e:
        st.error(f"Erro na conversão: {e}")
        return None

@st.cache_data(show_spinner=False)
def get_historico(from_currency: str, to_currency: str, days: int = 7):
    """Retorna um DataFrame com o histórico dos últimos 'days' dias para o par de moedas."""
    start_date = datetime.today() - timedelta(days=days)
    datas, cotacoes = [], []
    for i in range(days + 1):
        dia = start_date + timedelta(days=i)
        dia_str = dia.strftime("%Y-%m-%d")
        url = f"https://api.frankfurter.app/{dia_str}?from={from_currency}&to={to_currency}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            rate = response.json()["rates"].get(to_currency)
            if rate:
                datas.append(dia)
                cotacoes.append(rate)
        except Exception as e:
            st.error(f"Erro em {dia_str}: {e}")
    df = pd.DataFrame({"Data": datas, "Cotação": cotacoes})
    df.sort_values("Data", inplace=True)
    return df

# Seção de Conversão
st.subheader("Conversão de Moedas")
col1, col2, col3 = st.columns(3)
with col1:
    from_currency = st.selectbox("Moeda de origem", MOEDAS, index=MOEDAS.index("BRL"))
with col2:
    to_currency = st.selectbox("Moeda de destino", MOEDAS, index=MOEDAS.index("USD"))
with col3:
    amount = st.number_input("Valor a converter", min_value=0.0, value=2.0, step=0.01)

if st.button("Converter"):
    resultado = convert_currency(amount, from_currency, to_currency)
    if resultado is not None:
        st.success(f"{amount:.2f} {from_currency} = {resultado:.2f} {to_currency}")
    else:
        st.error("Falha na conversão.")

st.markdown("---")

# Seção de Histórico
st.subheader("Histórico (últimos 7 dias)")
df_hist = get_historico(from_currency, to_currency, days=7)
if not df_hist.empty:
    fig = px.line(df_hist, x="Data", y="Cotação", title=f"Histórico: {from_currency} para {to_currency}")
    fig.update_layout(xaxis_title="Data", yaxis_title="Cotação")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("Dados históricos não disponíveis.")
