from datetime import datetime
from config import NEWS_SOURCES, MONGO_URI, DB_NAME
import feedparser
import math
from services.llm_service import generate_embedding
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
articles_collection = db["articles"]

def get_all_sources():
    """Return all configured news sources."""
    return NEWS_SOURCES

def get_all_articles():
    """Return all sorted articles directly from MongoDB."""
    # Convert MongoDB cursor to list and remove the internal_id for the API
    articles = list(articles_collection.find({},{"_id":0}))
    return articles

def get_articles_by_source(source_name: str):
    """Filter artciles by source name in MongoDB."""
    articles = list(articles_collection.find({"source": source_name},{"_id": 0}))
    return articles

def fetch_rss_news():
    """
        Go through our configured sources, fetch their RSS feeds,
        and add the latest 5 articles from each to the database.
    """
    news_articles_count = 0

    for source in NEWS_SOURCES:
        rss_url = source.get("rss_url")

        if not rss_url:
            continue

        try:
            feed = feedparser.parse(rss_url)

            for entry in feed.entries[:5]:
                title = entry.get("title","No Title")
                content = entry.get("summary","No Content")

                # Check MongoDB instead of in-memory list
                exists = articles_collection.find_one({"title": title})
                if not exists:
                    add_article(title, source["name"], content, source["category"])
                    news_articles_count+=1

        except Exception as e:
            print(f"Error fetching from {source['name']}: {e}")

    return {"message": f"Successfully fetched {news_articles_count} new articles."}

def cosine_similarity(v1,v2):
    """Calculate how close two vectors (lists of numbers) are to each other."""
    if not v1 or not v2:
        return 0.0
    
    dot_product = sum(a*b for a,b in zip(v1,v2))
    magnitude1 = math.sqrt(sum(a*a for a in v1))
    magnitude2 = math.sqrt(sum(b*b for b in v2))

    if magnitude1==0 or magnitude2==0:
        return 0.0
    
    return dot_product / (magnitude1 * magnitude2)

def add_article(title: str,source: str,content: str,category: str):
    """Add a new article add save it to MongoDB."""

    # We create our own integer IDs so we don't break our API routes
    total_docs = articles_collection.count_documents({})
    new_id = total_docs + 1

    # Generate vector
    text_to_embed = f"{title}. {content}"
    vector = generate_embedding(text_to_embed)

    article = {
        "id": new_id,
        "title": title,
        "source": source,
        "content": content,
        "category": category,
        "embedding": vector,
        "created_at": datetime.now().isoformat()
    }

    # Insert into MongoDB
    articles_collection.insert_one(article)

    # Remove the MongoDB internal _id before returning to FastAPI
    if "_id" in article:
        del article["_id"]

    return article

def find_similar_articles(target_article_id: int,threshold: float=0.8):
    """Find other articles that are about the exact same news story."""

    target_article = articles_collection.find_one({"id": target_article_id})

    if not target_article or not target_article.get("embedding"):
        return []
    
    similar_articles = []

    # Get all other articles that have an embedding from MongoDB directly
    all_other_articles = articles_collection.find({
        "id": {"$ne": target_article_id},
        "embedding": {"$exists": True, "$ne": []}
    })

    for article in all_other_articles:
        score = cosine_similarity(target_article["embedding"], article["embedding"])

        if score > threshold:
            similar_articles.append({
                "id": article["id"],
                "title": article["title"],
                "source": article["source"],
                "similarity_score": round(score,2)
            })

    similar_articles.sort(key=lambda x : x["similarity_score"],reverse=True)
    return similar_articles