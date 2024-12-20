import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Chemin du fichier des données sociales
INPUT_CSV_PATH = "data/reddit_data.csv"
OUTPUT_CSV_PATH = "data/reddit_data_analyzed.csv"

def analyze_social_data():
    print("Chargement des données sociales...")
    try:
        data = pd.read_csv(INPUT_CSV_PATH)
    except FileNotFoundError:
        print(f"Erreur : Le fichier {INPUT_CSV_PATH} est introuvable.")
        return

    print("Données chargées. Analyse de sentiment en cours...")
    
    # Initialiser l'analyseur de sentiment
    analyzer = SentimentIntensityAnalyzer()
    
    # Ajouter une colonne de sentiment
    sentiments = []
    for title in data['title']:
        sentiment_score = analyzer.polarity_scores(title)
        sentiments.append(sentiment_score['compound'])  # Utiliser le score 'compound'
    
    data['sentiment_score'] = sentiments

    # Sauvegarder les données enrichies
    print("Sauvegarde des données enrichies...")
    data.to_csv(OUTPUT_CSV_PATH, index=False)
    print(f"Données enrichies sauvegardées dans {OUTPUT_CSV_PATH}.")

if __name__ == "__main__":
    analyze_social_data()