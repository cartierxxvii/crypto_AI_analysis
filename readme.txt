## activer l'environnement virtuel

source trading_env/bin/activate
deactivate pour déactiver

## Lancer le projet 

python app/main.py

## générer des données historiques 

python app/analysis/fetch_historical_data.py

## analyze_social_data.py (dans app/analysis)

Ce fichier va :
	•	Charger les données sociales depuis reddit_data.csv.
	•	Effectuer une analyse de sentiment pour chaque post.
	•	Enregistrer les données enrichies dans un fichier comme reddit_data_analyzed.csv.


# Crypto Trading Tool

Crypto Trading Tool est une application complète d'analyse et de trading automatisé de cryptomonnaies. Ce projet utilise des données en temps réel, des analyses techniques, des actualités sociales et des modèles d'apprentissage profond pour prendre des décisions de trading informées.

---

## Fonctionnalités principales

1. **Collecte de données** :
   - Récupération des données historiques depuis Binance.
   - Suivi en temps réel des flux de trading via WebSocket.
   - Collecte des actualités à partir de **CoinMarketCap** et des discussions sur Reddit.
   
2. **Préparation et analyse des données** :
   - Nettoyage, normalisation et préparation des données pour les modèles prédictifs.
   - Analyse technique avec des indicateurs comme RSI et MACD.

3. **Modèle prédictif LSTM** :
   - Entraînement d'un modèle de type **LSTM (Long Short-Term Memory)** pour prédire les tendances du marché.
   - Sauvegarde et chargement du modèle pour les prédictions futures.

4. **Prise de décision** :
   - Définition des niveaux d'entrée, de take-profit et de stop-loss basés sur des prédictions et des analyses.

5. **Organisation structurée** :
   - Toutes les fonctionnalités sont organisées dans des modules Python bien définis.

---

## Structure du projet

### Dossiers principaux

1. **`app/`** : Contient tous les modules Python du projet.
   - **`analysis/`** : 
     - **`data_preparation.py`** : Prépare les données (normalisation, séquençage, etc.).
     - **`fetch_coinmarketcap_news.py`** : Récupère les dernières actualités de CoinMarketCap via un flux RSS.
     - **`fetch_reddit_data.py`** : Récupère les discussions Reddit pertinentes pour l'analyse sociale.
     - **`technical_indicators.py`** : Calcule les indicateurs techniques comme RSI et MACD.
     - **`train_lstm.py`** : Script pour entraîner le modèle LSTM.
     - **`lstm_model.py`** : Contient la définition et l'utilisation du modèle LSTM.
     - **`fetch_historical_data.py`** : Récupère les données historiques des prix sur Binance.
   - **`decision/`** : 
     - **`strategy.py`** : Implémente les règles de prise de décision en trading.
   - **`main.py`** : Point d’entrée principal pour exécuter le projet.

2. **`data/`** : Stocke toutes les données collectées :
   - **`historical_data_*.csv`** : Données historiques des prix des cryptomonnaies.
   - **`reddit_data.csv`** : Discussions Reddit collectées.
   - **`rss_feed_latest_news.csv`** : Actualités provenant du flux RSS de CoinMarketCap.

3. **`models/`** : Contient le modèle entraîné :
   - **`lstm_model.keras`** : Modèle LSTM sauvegardé après l’entraînement.

4. **`trading_env/`** : Contient les fichiers de configuration pour l’environnement Python virtuel.

---

## Installation

### 1. Cloner le dépôt
```bash
git clone https://github.com/username/crypto_trading_tool.git
cd crypto_trading_tool
```

### 2. Créer un environnement virtuel
```bash
python3 -m venv trading_env
source trading_env/bin/activate  # Sous Linux/Mac
trading_env\Scripts\activate     # Sous Windows
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configurer l'environnement
Créez un fichier **`.env`** contenant vos clés API (Binance, CoinMarketCap, etc.).
```env
BINANCE_API_KEY=your_binance_api_key
BINANCE_SECRET_KEY=your_binance_secret_key
```

---

## Utilisation

### Étape 1 : Collecter les données
- Récupérez les données historiques :
  ```bash
  python app/analysis/fetch_historical_data.py
  ```
- Récupérez les actualités et les données sociales :
  ```bash
  python app/analysis/fetch_coinmarketcap_news.py
  python app/analysis/fetch_reddit_data.py
  ```

### Étape 2 : Entraîner le modèle
- Entraînez le modèle LSTM avec les données collectées :
  ```bash
  python app/analysis/train_lstm.py
  ```

### Étape 3 : Lancer l’application
- Démarrez l’application principale pour analyser les données et exécuter les stratégies :
  ```bash
  python app/main.py
  ```

---

## Notes importantes

1. **Fichiers requis** :
   - Les fichiers de données doivent être dans le dossier `data/`.
   - Le modèle LSTM est sauvegardé dans `models/lstm_model.keras`.

2. **Logs et résultats** :
   - Les prédictions et décisions de trading sont affichées dans la console.
   - Les résultats de l’analyse sont sauvegardés dans des fichiers CSV.

3. **Extensibilité** :
   - Vous pouvez ajouter d'autres sources de données (API, flux RSS) dans `analysis/`.
   - Les stratégies de trading peuvent être modifiées dans `decision/strategy.py`.

---

## Exemple de prédictions

Exemple de sortie après l'entraînement du modèle :
```bash
Prix actuel : 97431.45 USD
Prix prédit : 98100.67 USD
Take-Profit : 100626.24 USD
Stop-Loss : 95482.821 USD
```

---

## Contributions

Les contributions sont les bienvenues ! Veuillez ouvrir une issue ou une pull request pour discuter des changements que vous souhaitez apporter.

---

## Auteur

Créé par cartier.xxvi
