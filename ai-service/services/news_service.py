from datetime import datetime
from config import NEWS_SOURCES

articles_db = []

def get_all_sources():
    """Return all configured news sources."""
    return NEWS_SOURCES

def get_all_articles():
    """Return all stored articles."""
    return articles_db

def add_article(title: str,source: str, content: str, category: str):
    """Add a new article and return it with an ID."""
    new_id = len(articles_db)+1
    article = {
        "id": new_id,
        "title": title,
        "source": source,
        "content": content,
        "category": category,
        "created_at": datetime.now().isoformat()
    }
    articles_db.append(article)
    return article

def get_articles_by_source(source_name: str):
    """Filter articles by source name."""
    return [a for a in articles_db if a["source"].lower()==source_name.lower()]