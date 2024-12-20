import os
import praw
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Charger les variables d'environnement
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_SECRET = os.getenv("REDDIT_SECRET")
REDDIT_REDIRECT_URI = os.getenv("REDDIT_REDIRECT_URI")

# Initialiser Reddit avec PRAW
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_SECRET,
    user_agent="crypto_trading_tool by /u/your_username",  # Remplacez par votre pseudo Reddit
    redirect_uri=REDDIT_REDIRECT_URI,
)

def fetch_crypto_discussions(subreddit_name, limit=10):
    """Récupérer les posts les plus récents d'un subreddit"""
    subreddit = reddit.subreddit(subreddit_name)
    posts = []

    print(f"Fetching {limit} posts from r/{subreddit_name}...")
    for post in subreddit.new(limit=limit):
        posts.append({
            "title": post.title,
            "score": post.score,
            "created_utc": post.created_utc,
            "comments": post.num_comments,
            "url": post.url,
        })
    return posts

if __name__ == "__main__":
    # Tester la récupération de discussions liées à la crypto
    subreddit_name = "cryptocurrency"  # Exemple de subreddit
    data = fetch_crypto_discussions(subreddit_name, limit=5)
    for idx, post in enumerate(data):
        print(f"{idx+1}. {post['title']} (Score: {post['score']}, Comments: {post['comments']})")