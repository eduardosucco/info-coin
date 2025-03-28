import os
import requests
import pandas as pd
from datetime import datetime, timedelta

# Configurações globais para o ecossistema InfoCoin
MOEDAS = ['USD', 'EUR', 'BRL', 'GBP', 'JPY', 'CNY']
API_KEY = os.getenv("EXCHANGE_API_KEY", "sua_api_key_default")
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}"
API_URL = "https://api.exchangerate.host"

def get_cotacao(moeda_base: str, moeda_destino: str) -> float:
    """
    Obtém a cotação da moeda de origem para a moeda de destino.
    """
    url = f"{BASE_URL}/latest/{moeda_base}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get('result') == 'success':
            return data['conversion_rates'].get(moeda_destino)
    except requests.RequestException as e:
        print(f"Erro ao acessar API de cotação: {e}")
    return None

def get_historico(moeda_base: str, moeda_destino: str, dias: int) -> pd.DataFrame:
    """
    Retorna um DataFrame com o histórico de cotações para o período especificado.
    """
    data_final = datetime.today()
    data_inicial = data_final - timedelta(days=dias)
    url = (
        f"{API_URL}/timeseries?"
        f"start_date={data_inicial.date()}&end_date={data_final.date()}"
        f"&base={moeda_base}&symbols={moeda_destino}"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get("success", False):
            df = pd.DataFrame(data['rates']).T
            df.index = pd.to_datetime(df.index)
            df.columns = [f"{moeda_base}_{moeda_destino}"]
            return df.sort_index()
    except requests.RequestException as e:
        print(f"Erro ao acessar API de histórico: {e}")
    return pd.DataFrame()
