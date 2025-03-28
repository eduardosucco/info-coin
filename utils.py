import os
import requests
import pandas as pd
from datetime import datetime, timedelta

# Configurações globais – fortalecendo o ecossistema InfoCoin
MOEDAS = ['USD', 'EUR', 'BRL', 'GBP', 'JPY', 'CNY']
# Utilize a sua API Key fornecida
API_KEY = "dbdc1e27db50145db25e50a05820f2af"
BASE_URL = "http://api.exchangeratesapi.io/v1/latest"
HISTORICAL_URL = "http://api.exchangeratesapi.io/v1"  # para chamadas históricas

def get_cotacao(moeda_base: str, moeda_destino: str) -> float:
    """
    Obtém a cotação da moeda de origem para a moeda de destino
    utilizando o endpoint 'latest'.
    """
    # Constrói a URL para o endpoint latest com os parâmetros necessários
    url = f"{BASE_URL}?access_key={API_KEY}&base={moeda_base}&symbols={moeda_destino}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get("success", False):
            return data["rates"].get(moeda_destino)
    except requests.RequestException as e:
        print(f"Erro ao acessar API de cotação: {e}")
    return None

def get_historico(moeda_base: str, moeda_destino: str, dias: int) -> pd.DataFrame:
    """
    Retorna um DataFrame com o histórico de cotações para o período especificado,
    simulando um endpoint timeseries via múltiplas chamadas ao endpoint 'historical'.
    """
    data_final = datetime.today()
    data_inicial = data_final - timedelta(days=dias)
    rates = {}
    
    for n in range(dias + 1):
        dt = data_inicial + timedelta(days=n)
        date_str = dt.strftime("%Y-%m-%d")
        url = f"{HISTORICAL_URL}/{date_str}?access_key={API_KEY}&base={moeda_base}&symbols={moeda_destino}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data.get("success", False):
                rate = data["rates"].get(moeda_destino)
                if rate is not None:
                    rates[date_str] = {f"{moeda_base}_{moeda_destino}": rate}
        except requests.RequestException as e:
            print(f"Erro na data {date_str}: {e}")
    
    if rates:
        df = pd.DataFrame.from_dict(rates, orient="index")
        df.index = pd.to_datetime(df.index)
        return df.sort_index()
    else:
        return pd.DataFrame()
