import os
import requests
from fastapi import APIRouter
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/daily-news", tags=["news"])

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

@router.get("/")
def get_daily_news(q: str = "technology career programming"):
    """Fetch latest news headlines from NewsAPI with personalized query"""
    if not NEWS_API_KEY:
        return get_mock_news()

    try:
        # Fetch news based on personalized query
        url = f"https://newsapi.org/v2/everything?q={q}&sortBy=publishedAt&pageSize=6&language=en&apiKey={NEWS_API_KEY}"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])
            
            news_items = []
            for idx, article in enumerate(articles):
                if not article.get("title") or article.get("title") == "[Removed]":
                    continue

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
                    "description": article.get("description"),
                    "urlToImage": article.get("urlToImage"),
                    "source": {"name": article.get("source", {}).get("name", "Unknown")},
                    "publishedAt": published_at,
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
            "description": "How autonomous coding agents are reshaping the developer experience and accelerating product delivery globally.",
            "urlToImage": "https://images.unsplash.com/photo-1620825937374-87fc1d62c979?auto=format&fit=crop&q=80&w=600&h=400",
            "source": {"name": "TechCrunch"},
            "date": datetime.now().strftime("%b %d, %Y"),
            "url": "https://techcrunch.com"
        },
        {
            "id": 2,
            "title": "Remote Work Trends: Why Hybrid is Winning in 2026",
            "description": "A new industry report shows that 85% of tech companies have optimized their operations around flexible hybrid work models.",
            "urlToImage": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?auto=format&fit=crop&q=80&w=600&h=400",
            "source": {"name": "Forbes"},
            "date": datetime.now().strftime("%b %d, %Y"),
            "url": "https://forbes.com"
        },
        {
            "id": 3,
            "title": "Top 10 Programming Languages to Master This Year",
            "description": "Explore the languages that developers are overwhelmingly adopting to build scalable cloud architectures and AI integrated apps.",
            "urlToImage": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&q=80&w=600&h=400",
            "source": {"name": "HackerNews"},
            "date": datetime.now().strftime("%b %d, %Y"),
            "url": "https://news.ycombinator.com"
        },
        {
            "id": 4,
            "title": "OriginX Launches New Professional Networking Features",
            "description": "The trusted career platform rolls out advanced matching tools connecting job seekers and global employers faster than ever.",
            "urlToImage": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&q=80&w=600&h=400",
            "source": {"name": "OriginX Blog"},
            "date": datetime.now().strftime("%b %d, %Y"),
            "url": "#"
        },
        {
            "id": 5,
            "title": "How to Prepare for Technical Interviews in the AI Era",
            "description": "Mastering system design and algorithmic fundamentals remains crucial even as AI tools streamline coding exercises.",
            "urlToImage": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&q=80&w=600&h=400",
            "source": {"name": "Medium"},
            "date": datetime.now().strftime("%b %d, %Y"),
            "url": "https://medium.com"
        }
    ]
