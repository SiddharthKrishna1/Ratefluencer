import requests
import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_trending_topics(category="technology"):
    url = "https://newsapi.org/v2/top-headlines"
    
    params = {
        "category": category,
        "language": "en",
        "pageSize": 10,
        "apiKey": NEWS_API_KEY
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    topics = []
    if data["status"] == "ok":
        for article in data["articles"]:
            topics.append({
                "title": article["title"],
                "description": article["description"],
                "url": article["url"]
            })
    
    return topics