import streamlit as st

# Define as páginas do app utilizando st.Page
conversor_page = st.Page("conversor.py", title="Conversor de Moedas", icon="💱")
historico_page = st.Page("historico.py", title="Histórico de Cotações", icon="📈")

# Configurando a navegação
pg = st.navigation([conversor_page, historico_page])

# Configuração global da página
st.set_page_config(
    page_title="InfoCoin - Multipage App",
    page_icon="💰",
    layout="wide"
)

# Executa a página selecionada pelo usuário
pg.run()
