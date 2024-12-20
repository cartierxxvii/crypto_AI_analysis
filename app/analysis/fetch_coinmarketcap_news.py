import requests
import pandas as pd

# URL du flux RSS en format JSON
RSS_FEED_URL = "https://politepol.com/fd/4dwo9lJKR7CV.json"

def fetch_rss_feed():
    try:
        # Faire la requête pour récupérer le flux RSS
        response = requests.get(RSS_FEED_URL)
        response.raise_for_status()  # Vérifie les erreurs HTTP
        data = response.json()

        # Vérifier si des données sont disponibles
        if not data or "items" not in data:
            print("Aucune donnée disponible dans le flux RSS.")
            return []

        # Extraire les actualités
        news_items = data["items"]
        news_data = []
        for item in news_items:
            news_data.append({
                "title": item.get("title"),
                "link": item.get("link"),
                "description": item.get("description"),
                "pubDate": item.get("pubDate"),
            })

        return news_data

    except requests.exceptions.HTTPError as http_err:
        print(f"Erreur HTTP : {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Erreur de requête : {req_err}")
    except Exception as e:
        print(f"Erreur générale : {e}")
    return []

if __name__ == "__main__":
    news = fetch_rss_feed()
    if news:
        # Sauvegarde dans un fichier CSV
        df = pd.DataFrame(news)
        df.to_csv("data/rss_feed_latest_news.csv", index=False)
        print("Les dernières actualités ont été sauvegardées dans rss_feed_latest_news.csv")
    else:
        print("Aucune actualité récupérée.")