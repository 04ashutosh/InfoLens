from datetime import datetime
from config import NEWS_SOURCES
import feedparser

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

def fetch_rss_news():
    """
    Go through our configured sources, fetch their RSS feeds,
    and add the latest 5 articles from each to the database.
    """

    news_articles_count = 0

    for source in NEWS_SOURCES:
        rss_url = source.get("rss_url")

        # Skip sources where we haven't added an RSS link yet
        if not rss_url:
            continue

        try:
            # feedparser reads the URL and converts the XML to Python object
            feed = feedparser.parse(rss_url)

            # Grab just the top 5 newest entries
            for entry in feed.entries[:5]:
                # feedparser gives us safe defaults if a field is missing
                title = entry.get("title","No Title")
                content = entry.get("summary","No Content")

                # Check if we already have this article to avoid duplicates
                exists = any(a["title"]==title for a in articles_db)
                if not exists:
                    add_article(title, source["name"], content, source["category"])
                    news_articles_count += 1

        except Exception as e:
            print(f"Error fetching from {source['name']}: {e}")

    return {"message": f"Successfully fetched {news_articles_count} new articles."}