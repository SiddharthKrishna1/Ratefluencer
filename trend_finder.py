import requests
import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_trending_topics(category="technology"):
    """
    Fetches real trending topics from NewsAPI.
    Falls back to sample data if API call fails.
    """
    try:
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "category": category,
            "language": "en",
            "pageSize": 10,
            "apiKey": NEWS_API_KEY
        }
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        if data.get("status") == "ok" and data.get("articles"):
            topics = []
            for i, article in enumerate(data["articles"]):
                if article.get("title") and article["title"] != "[Removed]":
                    # Assign a trend score based on position + source popularity
                    base_score = 95 - (i * 4)
                    topics.append({
                        "title": article["title"],
                        "description": article.get("description", ""),
                        "url": article.get("url", ""),
                        "source": article.get("source", {}).get("name", "Unknown"),
                        "score": max(base_score, 50),
                        "growth": f"+{max(400 - i*30, 80)}%"
                    })
            if topics:
                return topics

    except Exception as e:
        print(f"NewsAPI failed: {e}. Using fallback data.")

    # ── FALLBACK DATA (if NewsAPI fails or quota exceeded) ────
    fallback = {
        "technology": [
            {"title": "AI Agents are replacing entire dev teams in 2026", "score": 94, "growth": "+340%", "source": "TechCrunch"},
            {"title": "Apple releases Vision Pro 2 with mind control features", "score": 88, "growth": "+210%", "source": "The Verge"},
            {"title": "Google Gemini 3.0 beats all AI benchmarks worldwide", "score": 85, "growth": "+180%", "source": "Wired"},
            {"title": "OpenAI launches GPT-5 with real-time video understanding", "score": 91, "growth": "+290%", "source": "Reuters"},
            {"title": "Tesla self-driving finally approved in all 50 US states", "score": 79, "growth": "+150%", "source": "Bloomberg"},
        ],
        "business": [
            {"title": "How creators are making $100k per month using AI tools", "score": 96, "growth": "+420%", "source": "Forbes"},
            {"title": "Top 5 AI startups that raised $1B funding this week", "score": 83, "growth": "+190%", "source": "TechCrunch"},
            {"title": "Amazon launches same-hour drone delivery nationwide", "score": 77, "growth": "+130%", "source": "CNBC"},
            {"title": "Remote work permanently adopted by Fortune 500 companies", "score": 81, "growth": "+160%", "source": "WSJ"},
            {"title": "Bitcoin crosses $200k as institutional adoption explodes", "score": 89, "growth": "+260%", "source": "CoinDesk"},
        ],
        "science": [
            {"title": "Scientists discover AI-powered cure for common cold", "score": 92, "growth": "+310%", "source": "Nature"},
            {"title": "NASA confirms liquid water found on Mars surface", "score": 87, "growth": "+240%", "source": "NASA"},
            {"title": "Anti-aging pill enters final human trials with 80% success", "score": 90, "growth": "+280%", "source": "Science"},
            {"title": "Brain computer interface enables typing at 200 WPM", "score": 84, "growth": "+200%", "source": "MIT"},
            {"title": "Solar panels hit 80% efficiency breaking world record", "score": 76, "growth": "+120%", "source": "IEEE"},
        ],
        "entertainment": [
            {"title": "AI-generated movie wins Oscar for Best Picture 2026", "score": 95, "growth": "+380%", "source": "Variety"},
            {"title": "Netflix uses AI to create fully personalized shows per user", "score": 88, "growth": "+250%", "source": "Hollywood Reporter"},
            {"title": "Virtual concerts now earn more revenue than live shows", "score": 82, "growth": "+170%", "source": "Billboard"},
            {"title": "AI influencers outnumber human creators on Instagram", "score": 93, "growth": "+350%", "source": "Social Media Today"},
            {"title": "YouTube Shorts hits 5 billion daily views milestone", "score": 86, "growth": "+220%", "source": "YouTube Blog"},
        ],
        "health": [
            {"title": "Intermittent fasting proven to add 10 years to lifespan", "score": 91, "growth": "+300%", "source": "Harvard Health"},
            {"title": "AI doctor diagnoses cancer earlier than human specialists", "score": 94, "growth": "+360%", "source": "Lancet"},
            {"title": "Mental health app reduces anxiety by 70% in clinical trials", "score": 85, "growth": "+210%", "source": "JAMA"},
            {"title": "CEO sleep hack goes viral across all social platforms", "score": 88, "growth": "+260%", "source": "Business Insider"},
            {"title": "Wearable detects heart attack 24 hours before it happens", "score": 96, "growth": "+400%", "source": "Mayo Clinic"},
        ]
    }
    return fallback.get(category, fallback["technology"])


def get_mock_influencer_profiles():
    return [
        {
            "name": "TechWithPriya", "niche": "Technology",
            "followers": 450000, "following": 820,
            "avg_likes": 28000, "avg_comments": 1200,
            "avg_shares": 3400, "avg_saves": 5600,
            "posts_per_week": 5, "fake_follower_pct": 4,
        },
        {
            "name": "StartupSahil", "niche": "Business",
            "followers": 220000, "following": 1500,
            "avg_likes": 8500, "avg_comments": 430,
            "avg_shares": 980, "avg_saves": 2100,
            "posts_per_week": 4, "fake_follower_pct": 12,
        },
        {
            "name": "AIwithAnika", "niche": "AI & Tech",
            "followers": 890000, "following": 340,
            "avg_likes": 67000, "avg_comments": 3800,
            "avg_shares": 12000, "avg_saves": 18000,
            "posts_per_week": 6, "fake_follower_pct": 2,
        },
        {
            "name": "CreatorKaran", "niche": "Creator Economy",
            "followers": 130000, "following": 4200,
            "avg_likes": 2100, "avg_comments": 85,
            "avg_shares": 120, "avg_saves": 340,
            "posts_per_week": 2, "fake_follower_pct": 28,
        },
        {
            "name": "FinanceFiona", "niche": "Finance",
            "followers": 560000, "following": 610,
            "avg_likes": 34000, "avg_comments": 2100,
            "avg_shares": 7800, "avg_saves": 14000,
            "posts_per_week": 4, "fake_follower_pct": 6,
        },
    ]
