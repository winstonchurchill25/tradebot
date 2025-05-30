# utils/live_sentiment.py
import os
import requests
from textblob import TextBlob
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")  # Set this in your .env or shell
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

def fetch_news_sentiment(ticker: str, max_articles: int = 10) -> dict:
    params = {
        "q": ticker,
        "pageSize": max_articles,
        "apiKey": NEWS_API_KEY,
        "sortBy": "publishedAt",
        "language": "en"
    }
    try:
        response = requests.get(NEWS_ENDPOINT, params=params)
        response.raise_for_status()
        articles = response.json().get("articles", [])
        if not articles:
            return {"market": "neutral", "news": "neutral"}

        scores = []
        for article in articles:
            title = article.get("title", "")
            score = TextBlob(title).sentiment.polarity
            scores.append(score)

        avg_score = sum(scores) / len(scores) if scores else 0

        if avg_score > 0.1:
            sentiment = "positive"
        elif avg_score < -0.1:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        return {"market": sentiment, "news": sentiment}

    except Exception as e:
        print(f"[ERROR] Sentiment fetch failed: {e}")
        return {"market": "neutral", "news": "neutral"}

# Example usage
if __name__ == "__main__":
    print(fetch_news_sentiment("PLTR"))
