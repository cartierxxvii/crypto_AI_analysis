import sys
import os
from dotenv import load_dotenv
from binance.client import Client
import numpy as np
from tensorflow.keras.models import load_model
import requests

# Configuration des chemins pour les modules
print("Configuration des chemins PYTHONPATH...")
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
sys.path.append('/Users/nasser/crypto_trading_tool')

from app.data.market_data import MarketData
from app.analysis.data_preparation import prepare_data
from app.analysis.technical_indicators import TechnicalIndicators
from app.decision.strategy import Strategy
from app.data.websocket_data import WebSocketClient
from app.analysis.fetch_reddit_data import fetch_reddit_data, save_reddit_to_csv

# Charger le modèle LSTM sauvegardé
MODEL_PATH = "models/lstm_model.keras"
print(f"Chargement du modèle LSTM depuis {MODEL_PATH}...")
lstm_model = load_model(MODEL_PATH)

# Buffer pour les prix reçus en temps réel
seq_length = 50
price_buffer = []

def handle_realtime_data(data):
    """Traite les données reçues en temps réel."""
    try:
        price = float(data['p'])  # Prix reçu via le WebSocket
        print(f"Prix en temps réel : {price}")

        # Mettre à jour le buffer
        price_buffer.append(price)
        if len(price_buffer) > seq_length:
            price_buffer.pop(0)

        # Effectuer une prédiction si le buffer est plein
        if len(price_buffer) == seq_length:
            input_data = np.array(price_buffer).reshape((1, seq_length, 1))
            predicted_price = lstm_model.predict(input_data)[0, 0]
            print(f"Prédiction du prochain prix : {predicted_price:.2f} USD")

    except KeyError:
        print("Clé 'p' manquante dans les données reçues :", data)

def fetch_latest_news(rss_url):
    """
    Récupère les dernières actualités à partir d'un flux RSS.
    :param rss_url: URL du flux RSS (JSON)
    :return: Liste des articles avec titre, lien, et description
    """
    try:
        response = requests.get(rss_url)
        response.raise_for_status()
        data = response.json()

        news_list = []
        for item in data.get("items", []):
            news = {
                "title": item.get("title"),
                "link": item.get("url"),
                "description": item.get("description"),
                "published_date": item.get("datePublished")
            }
            news_list.append(news)

        return news_list

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération des actualités : {e}")
        return []

def main():
    print("Démarrage de l'application de trading...")

    # Charger les variables d'environnement
    load_dotenv()
    API_KEY = os.getenv("BINANCE_API_KEY")
    API_SECRET = os.getenv("BINANCE_SECRET_KEY")

    # Vérification des clés API
    if not API_KEY or not API_SECRET:
        print("Clés API Binance manquantes dans le fichier .env.")
        return

    # Récupération des actualités Reddit
    print("Récupération des discussions Reddit...")
    try:
        reddit_data = fetch_reddit_data(subreddit="cryptocurrency", limit=10)
        save_reddit_to_csv(reddit_data, "data/reddit_data.csv")
        print("Discussions Reddit récupérées :")
        print(reddit_data.head())
    except Exception as e:
        print(f"Erreur lors de la récupération des discussions Reddit : {e}")

    # Initialisation du client Binance
    print("Initialisation du client Binance...")
    client = Client(API_KEY, API_SECRET)

    # Récupération des actualités via le flux RSS
    rss_url = "https://rss.app/feeds/v1.1/NwlnGRWbp6iFjlca.json"
    print("Récupération des actualités...")
    news_list = fetch_latest_news(rss_url)
    if news_list:
        print("Dernières actualités récupérées :")
        for news in news_list[:5]:  # Limiter l'affichage à 5 articles
            print(f"- {news['title']} ({news['published_date']})")
            print(f"  Lien : {news['link']}")
    else:
        print("Aucune actualité disponible.")

    # 1. Initialisation du WebSocket pour BTC/USDT
    print("Connexion au WebSocket pour les données en temps réel...")
    symbol = "BTCUSDT"
    ws_client = WebSocketClient(symbol=symbol, on_message_callback=handle_realtime_data)
    ws_client.start()

    print("WebSocket démarré. En attente des données en temps réel...")

    # 2. Récupérer les données du marché via HTTP
    print(f"Récupération des données pour {symbol} via HTTP...")
    price_data = MarketData.get_ticker_price(symbol)
    price = float(price_data["price"])
    print(f"Prix actuel (HTTP) : {price} USD")

    # 3. Récupération des données historiques depuis Binance
    print(f"Récupération des données historiques pour {symbol}...")
    interval = Client.KLINE_INTERVAL_1MINUTE  # Intervalle de 1 minute
    limit = seq_length  # Nombre de bougies à récupérer

    try:
        historical_data = client.get_klines(symbol=symbol, interval=interval, limit=limit)
        historical_prices = [float(data[4]) for data in historical_data]
        price_buffer.extend(historical_prices)
        print("Données historiques récupérées :", historical_prices)
    except Exception as e:
        print(f"Erreur lors de la récupération des données historiques : {e}")
        return

    # 4. Calcul des indicateurs techniques
    print("Calcul des indicateurs techniques...")
    
    # Calcul du RSI
    print("Calcul du RSI...")
    rsi_df = TechnicalIndicators.calculate_rsi(historical_prices)
    print(rsi_df.tail())  # Affiche les derniers résultats pour plus de clarté

    # Calcul du MACD
    print("Calcul du MACD...")
    print("Prix de clôture utilisés pour le MACD :", historical_prices)
    macd_df = TechnicalIndicators.calculate_macd(historical_prices)
    print("Résultat du MACD :", macd_df.tail())

    # 5. Calcul des niveaux d'entrée, Take-Profit et Stop-Loss
    print("Calcul des niveaux d'entrée, Take-Profit et Stop-Loss...")
    decision = Strategy.calculate_entry(price, stop_loss_percentage=2, take_profit_percentage=4)
    print(f"Décision de trading : {decision}")

    # 6. Maintenir la connexion WebSocket active
    try:
        print("Connexion WebSocket active. Appuyez sur Ctrl+C pour arrêter.")
        while True:
            pass  # Maintenir la connexion ouverte
    except KeyboardInterrupt:
        print("\nArrêt demandé par l'utilisateur.")
        ws_client.stop()

if __name__ == "__main__":
    main()