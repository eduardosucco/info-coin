import streamlit as st

st.set_page_config(
    page_title="InfoCoin - Dashboard",
    page_icon="💰",
    # layout="wide"
)

st.write("# Bem-vindo ao InfoCoin!")
st.sidebar.success("Selecione uma página acima.")

st.markdown(
    """
    InfoCoin é uma plataforma inovadora para monitorar e converter moedas globais.
    
    **👈 Selecione uma página na barra lateral** para acessar as funcionalidades:
    
    - 💱 Conversor de Moedas
    - 📈 Histórico de Cotações
    
    Transforme dados em insights estratégicos e potencialize sua visão de mercado!
    """
)
