import pandas as pd
from binance.client import Client
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone
from time import sleep
from binance.exceptions import BinanceAPIException

# Charger les variables d'environnement
load_dotenv(dotenv_path="/Users/nasser/crypto_trading_tool/.env")

def retry_request(func, retries=5, delay=10, **kwargs):
    """
    Réessayer une requête API en cas d'échec.
    """
    for attempt in range(retries):
        try:
            return func(**kwargs)
        except requests.exceptions.ReadTimeout as e:
            print(f"Timeout lors de la tentative {attempt + 1}/{retries}. Nouvelle tentative dans {delay} secondes...")
            sleep(delay)
        except Exception as e:
            print(f"Erreur inattendue : {e}")
            break
    raise Exception("Échec après plusieurs tentatives")

def fetch_historical_data(symbol="PEPEUSDT", interval="1m", start_time="5 years ago UTC"):
    """
    Récupère les données historiques de Binance pour une paire donnée.
    """
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_SECRET_KEY")
    if not api_key or not api_secret:
        raise ValueError("Les clés API Binance ne sont pas configurées.")

    client = Client(api_key=api_key, api_secret=api_secret, requests_params={"timeout": 60})

    if "ago" in start_time:
        years = int(start_time.split(" ")[0])
        start_datetime = datetime.now(timezone.utc) - timedelta(days=years * 365)
    else:
        start_datetime = pd.to_datetime(start_time).tz_localize("UTC")

    klines = []
    end_datetime = datetime.now(timezone.utc)
    current_start = start_datetime

    while current_start < end_datetime:
        try:
            current_end = min(current_start + timedelta(minutes=1000), end_datetime)
            print(f"Récupération des données de {current_start} à {current_end}...")
            klines += retry_request(
                client.get_historical_klines,
                symbol=symbol,
                interval=interval,
                start_str=current_start.strftime("%d %b %Y %H:%M:%S"),
                end_str=current_end.strftime("%d %b %Y %H:%M:%S")
            )
            current_start = current_end
        except BinanceAPIException as e:
            print(f"Erreur API Binance : {e}. Attente de 60 secondes...")
            sleep(60)

    df = pd.DataFrame(klines, columns=[
        "timestamp", "open", "high", "low", "close", "volume", "close_time",
        "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume",
        "taker_buy_quote_asset_volume", "ignore"
    ])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df["type"] = "historical"
    return df[["timestamp", "type", "open", "high", "low", "close", "volume"]]

def fetch_order_book(symbol="PEPEUSDT", limit=100):
    """
    Récupère les données du carnet d'ordres pour une paire donnée.
    """
    client = Client(api_key=os.getenv("BINANCE_API_KEY"), api_secret=os.getenv("BINANCE_SECRET_KEY"))
    order_book = retry_request(client.get_order_book, symbol=symbol, limit=limit)
    bids = pd.DataFrame(order_book["bids"], columns=["price", "quantity"])
    bids["type"] = "order_book_bid"
    asks = pd.DataFrame(order_book["asks"], columns=["price", "quantity"])
    asks["type"] = "order_book_ask"
    return pd.concat([bids, asks], ignore_index=True)

def fetch_funding_rate(symbol="PEPEUSDT"):
    """
    Récupère les taux de financement des contrats perpétuels.
    """
    client = Client(api_key=os.getenv("BINANCE_API_KEY"), api_secret=os.getenv("BINANCE_SECRET_KEY"))
    try:
        funding_rates = retry_request(client.futures_funding_rate, symbol=symbol)
        
        if not funding_rates:
            print(f"Aucune donnée de financement trouvée pour {symbol}.")
            return pd.DataFrame()

        df = pd.DataFrame(funding_rates)
        df["type"] = "funding_rate"
        return df[["fundingTime", "fundingRate", "type"]]
    except BinanceAPIException as e:
        print(f"Erreur Binance API : {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return pd.DataFrame()

def fetch_aggregate_trades(symbol="PEPEUSDT", limit=500):
    """
    Récupère les données de trading agrégées.
    """
    client = Client(api_key=os.getenv("BINANCE_API_KEY"), api_secret=os.getenv("BINANCE_SECRET_KEY"))
    trades = retry_request(client.get_aggregate_trades, symbol=symbol, limit=limit)
    df = pd.DataFrame(trades)
    df["type"] = "trades"
    return df[["T", "type", "p", "q"]]

def fetch_liquidations(symbol="PEPEUSDT", limit=50):
    """
    Récupère les liquidations massives sur Binance.
    """
    client = Client(api_key=os.getenv("BINANCE_API_KEY"), api_secret=os.getenv("BINANCE_SECRET_KEY"))
    try:
        liquidations = retry_request(client.futures_liquidation_orders, symbol=symbol, limit=limit)
        if not liquidations:
            print(f"Aucune liquidation trouvée pour {symbol}.")
            return pd.DataFrame()
        df = pd.DataFrame(liquidations)

        required_columns = ["time", "price", "origQty", "side"]
        available_columns = [col for col in required_columns if col in df.columns]
        if available_columns:
            df["type"] = "liquidations"
            return df[available_columns + ["type"]]
        else:
            print("Les colonnes attendues ne sont pas disponibles.")
            return pd.DataFrame()
    except Exception as e:
        print(f"Erreur lors de la récupération des liquidations : {e}")
        return pd.DataFrame()

def save_combined_data(file_path, *dataframes):
    """
    Combine et sauvegarde plusieurs DataFrames dans un seul fichier CSV.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    combined_df = pd.concat(dataframes, ignore_index=True)
    combined_df.to_csv(file_path, index=False)
    print(f"Données combinées sauvegardées dans {file_path}")

if __name__ == "__main__":
    print("Récupération des données depuis Binance...")
    historical_data = fetch_historical_data()
    order_book_data = fetch_order_book()
    funding_rate_data = fetch_funding_rate()
    trades_data = fetch_aggregate_trades()
    liquidations_data = fetch_liquidations()

    save_combined_data("data/combined_data_PEPEUSDT.csv", historical_data, order_book_data, funding_rate_data, trades_data, liquidations_data)