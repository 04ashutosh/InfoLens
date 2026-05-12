from datetime import datetime
from config import NEWS_SOURCES
import feedparser
import math
from services.llm_service import generate_embedding

articles_db = []

def get_all_sources():
    """Return all configured news sources."""
    return NEWS_SOURCES

def get_all_articles():
    """Return all stored articles."""
    return articles_db



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

def cosine_similarity(v1,v2):
    """Calculates how close two vectors (lists of numbers) are to each other."""
    if not v1 or not v2:
        return 0.0
    
    dot_product = sum(a*b for a,b in zip(v1,v2))
    magnitude1 = math.sqrt(sum(a*a for a in v1))
    magnitude2 = math.sqrt(sum(b*b for b in v2))

    if magnitude1==0 or magnitude2==0:
        return 0.0
    
    return dot_product/(magnitude1*magnitude2)

def add_article(title: str,source: str,content: str,category: str):
    """Add a new article and return it with an ID."""
    new_id = len(articles_db)+1

    # Generate the vector coordinate using Ollama!
    text_to_embed = f"{title}. {content}"
    vector = generate_embedding(text_to_embed)

    article = {
        "id": new_id,
        "title": title,
        "source": source,
        "content": content,
        "category": category,
        "embedding": vector, #<--- Save the vector
        "created_at": datetime.now().isoformat()
    }
    articles_db.append(article)
    return article

def find_similar_articles(target_article_id: int,threshold: float = 0.75):
    """Find other articles that are about the exact same news story."""
    target_article = next((a for a in articles_db if a["id"] == target_article_id), None)

    if not target_article or not target_article.get("embedding"):
        return []
    
    similar_articles = []

    for article in articles_db:
        # Don't compare it to itself
        if article["id"] == target_article_id:
            continue

        if not article.get("embedding"):
            continue

        # Calculate the distance!
        score = cosine_similarity(target_article["embedding"], article["embedding"])

        # If the score is higher than 0.75, they are likely the same story
        if score > threshold:
            similar_articles.append({
                "id": article["id"],
                "title": article["title"],
                "source": article["source"],
                "similarity_score": round(score,2)
            })

    # Sort so the highest matches are at the top
    similar_articles.sort(key=lambda x : x["similarity_score"],reverse=True)
    return similar_articles
