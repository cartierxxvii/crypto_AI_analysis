import praw
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="/Users/nasser/crypto_trading_tool/.env")

def fetch_reddit_data(subreddit="cryptocurrency", limit=100):
    """
    Récupère les discussions depuis Reddit.
    """
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_SECRET"),
        user_agent="crypto_trading_tool"
    )
    subreddit = reddit.subreddit(subreddit)
    data = []
    for post in subreddit.hot(limit=limit):
        data.append({
            "title": post.title,
            "score": post.score,
            "comments": post.num_comments,
            "created": post.created_utc,
            "url": post.url
        })
    df = pd.DataFrame(data)
    df['created'] = pd.to_datetime(df['created'], unit='s')
    return df

def save_reddit_to_csv(dataframe, file_path="data/reddit_data.csv"):
    """
    Sauvegarde les données Reddit dans un fichier CSV.
    """
    dataframe.to_csv(file_path, index=False)
    print(f"Données Reddit sauvegardées dans {file_path}")
    print("Aperçu des données :")
    print(dataframe.head())

if __name__ == "__main__":
    reddit_data = fetch_reddit_data()
    save_reddit_to_csv(reddit_data)