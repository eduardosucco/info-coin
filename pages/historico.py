import streamlit as st
import plotly.express as px
from utils import MOEDAS, get_historico

st.set_page_config(
    page_title="Histórico de Cotações",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Histórico de Cotações")

col1, col2 = st.columns(2)
with col1:
    moeda_origem = st.selectbox("Moeda de origem", MOEDAS, key="hist_origem", index=MOEDAS.index("BRL"))
with col2:
    moeda_destino = st.selectbox("Moeda de destino", MOEDAS, key="hist_destino", index=MOEDAS.index("USD"))

# Mapeamento inovador dos períodos para insights estratégicos
periodos = {
    "1d": 1,
    "3d": 3,
    "5d": 5,
    "1s (1 semana)": 7,
    "2s (2 semanas)": 14,
    "1m (1 mês)": 30,
    "3m (3 meses)": 90
}
periodo = st.selectbox("Período", list(periodos.keys()))
dias = periodos[periodo]

df_hist = get_historico(moeda_origem, moeda_destino, dias)
if not df_hist.empty:
    fig = px.line(df_hist, title=f"Histórico de {moeda_origem} para {moeda_destino} ({periodo})")
    fig.update_layout(xaxis_title="Data", yaxis_title="Cotação")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("📉 Dados históricos não disponíveis no momento.")
