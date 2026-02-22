import os
import requests
from fastapi import APIRouter
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/daily-news", tags=["news"])

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

@router.get("/")
def get_daily_news():
    """Fetch latest 5 tech/career news headlines from NewsAPI"""
    if not NEWS_API_KEY:
        return get_mock_news()

    try:
        # Fetch news related to technology, career, or software engineering
        url = f"https://newsapi.org/v2/everything?q=technology+OR+career+OR+programming&sortBy=publishedAt&pageSize=5&apiKey={NEWS_API_KEY}"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])
            
            news_items = []
            for idx, article in enumerate(articles):
                # Format date: 2024-02-22T06:34:42Z -> Feb 22, 2024
                published_at = article.get("publishedAt", "")
                formatted_date = datetime.now().strftime("%b %d, %Y")
                if published_at:
                    try:
                        dt = datetime.strptime(published_at[:10], "%Y-%m-%d")
                        formatted_date = dt.strftime("%b %d, %Y")
                    except:
                        pass

                news_items.append({
                    "id": idx + 1,
                    "title": article.get("title"),
                    "source": article.get("source", {}).get("name", "Unknown"),
                    "date": formatted_date,
                    "url": article.get("url")
                })
            
            if news_items:
                return news_items
                
        return get_mock_news()
        
    except Exception as e:
        print(f"Error fetching real news: {e}")
        return get_mock_news()

def get_mock_news():
    """Fallback for when API fails or key is missing"""
    return [
        {
            "id": 1,
            "title": "The Rise of Agentic AI in Modern Software Engineering",
            "source": "TechCrunch",
            "date": datetime.now().strftime("%b %d, %Y"),
            "url": "https://techcrunch.com"
        },
        {
            "id": 2,
            "title": "Remote Work Trends: Why Hybrid is Winning in 2026",
            "source": "Forbes",
            "date": datetime.now().strftime("%b %d, %Y"),
            "url": "https://forbes.com"
        },
        {
            "id": 3,
            "title": "Top 10 Programming Languages to Master This Year",
            "source": "HackerNews",
            "date": datetime.now().strftime("%b %d, %Y"),
            "url": "https://news.ycombinator.com"
        },
        {
            "id": 4,
            "title": "OriginX Launches New Professional Networking Features",
            "source": "OriginX Blog",
            "date": datetime.now().strftime("%b %d, %Y"),
            "url": "#"
        },
        {
            "id": 5,
            "title": "How to Prepare for Technical Interviews in the AI Era",
            "source": "Medium",
            "date": datetime.now().strftime("%b %d, %Y"),
            "url": "https://medium.com"
        }
    ]
