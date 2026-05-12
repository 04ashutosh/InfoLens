from fastapi import APIRouter, HTTPException
from models.schemas import ArticleRequest, ArticleResponse
from services.news_service import get_all_articles, add_article, get_articles_by_source
from services.news_service import fetch_rss_news
from services.llm_service import generate_response
from services.news_service import find_similar_articles

router = APIRouter(prefix="/api", tags=["Articles"])

@router.post("/articles", response_model=ArticleResponse)
def create_article(article: ArticleRequest):
    result = add_article(
        title=article.title,
        source=article.source,
        content=article.content,
        category=article.category
    )

    return ArticleResponse(
        id=result["id"],
        title=result["title"],
        source=result["source"],
        message="Article added successfully"
    )

@router.get("/articles")
def list_articles(source: str = None):
    """Get all articles, optionally filtered by source."""
    if source:
        articles = get_articles_by_source(source)
    else:
        articles = get_all_articles()
    return {"articles": articles, "total": len(articles)}

@router.post("/articles/fetch-latest")
def trigger_news_fetch():
    """Trigger the system to go out and download the latest news from all sources."""
    result = fetch_rss_news()
    return result

@router.get("/daily-brief")
def generate_daily_brief():
    """Take the latest 3 articles and generate a multi-perspective AI summary."""
    articles = get_all_articles()

    # Check if we have enough articles
    if len(articles)<3:
        return {"error": "Not enough articles. Run /fetch-latest first."}
    
    # Grab the top 3 latest articles
    top_3 = articles[:3]

    # Combine their text into a single prompt for the LLM
    combined_text = ""
    for idx, art in enumerate(top_3):
        combined_text+=f"\n--- Article {idx+1} ({art['source']}) ---\n"
        combined_text+=f"Title: {art['title']}\n"
        combined_text+=f"Content: {art['content']}\n"

    # Construct the Prompt
    prompt = f"""
    You are an elite, unbiased Indian news editor.
    I am going to give you 3 recent news articles from different sources. 
    Your task is to write a single, balanced "Daily Brief" summarizing the key events.
    - Focus ONLY on the facts.
    - Do NOT include the journalists' opinions.
    - If the sources disagree, mention that there are differing reports.
    - Output exactly 3 bullet points.
    Here are the articles:
    {combined_text}
    """

    # Send to our local Ollama model
    ai_summary = generate_response(prompt)

    return {
        "sources_used": [a['source'] for a in top_3],
        "titles_analyzed": [a['title'] for a in top_3],
        "daily_brief": ai_summary
    }

@router.get("/articles/{article_id}/similar")
def get_similar_articles(article_id: int, threshold: float = 0.5):
    """Find articles about the exact same topic"""
    similar = find_similar_articles(article_id, threshold=threshold)
    return {"target_id": article_id, "threshold": threshold, "similar_articles": similar}