import streamlit as st
from utils import MOEDAS, get_cotacao, get_historico
import plotly.express as px

# Configuração inicial – definindo o cenário para uma experiência digital inovadora
st.set_page_config(page_title="InfoCoin - Painel Integrado", layout="wide")

# Sidebar personalizada: seu hub de navegação estratégica
with st.sidebar:
    st.image("https://via.placeholder.com/150", use_column_width=True)  # Insira o logo da sua empresa aqui
    st.markdown("## Navegação")
    menu = st.radio("Selecione a opção:", ("Dashboard", "Conversor de Moedas", "Histórico de Cotações"))

# Corpo da aplicação – a central de comando do InfoCoin
if menu == "Dashboard":
    st.title("💰 InfoCoin – Painel Integrado")
    st.markdown(
        """
        Seja bem-vindo ao InfoCoin, a plataforma que une inovação e estratégia para monitorar e converter moedas globais.
        Utilize o menu lateral para acessar funcionalidades avançadas e transformar dados em insights poderosos.
        """
    )
    st.info("Navegue pelas funcionalidades e descubra como a transformação digital pode impulsionar sua visão de mercado.")
    
elif menu == "Conversor de Moedas":
    st.title("💱 Conversor de Moedas")
    col1, col2, col3 = st.columns(3)
    with col1:
        moeda_origem = st.selectbox("Moeda de origem", MOEDAS, index=MOEDAS.index("BRL"))
    with col2:
        moeda_destino = st.selectbox("Moeda de destino", MOEDAS, index=MOEDAS.index("USD"))
    with col3:
        valor = st.number_input("Valor a converter", min_value=0.0, value=1.0, step=0.01)
    
    st.markdown("---")
    cotacao = get_cotacao(moeda_origem, moeda_destino)
    if cotacao:
        convertido = valor * cotacao
        st.metric(f"{valor:.2f} {moeda_origem} =", f"{convertido:.2f} {moeda_destino}")
    else:
        st.error("⚠️ Não foi possível obter a cotação no momento. Por favor, tente novamente mais tarde.")

elif menu == "Histórico de Cotações":
    st.title("📈 Histórico de Cotações")
    col1, col2 = st.columns(2)
    with col1:
        moeda_origem = st.selectbox("Moeda de origem", MOEDAS, key="hist_origem", index=MOEDAS.index("BRL"))
    with col2:
        moeda_destino = st.selectbox("Moeda de destino", MOEDAS, key="hist_destino", index=MOEDAS.index("USD"))
    
    # Mapeamento inovador dos períodos para insights dinâmicos
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
