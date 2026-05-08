from fastapi import APIRouter, HTTPException
from models.schemas import ArticleRequest, ArticleResponse
from services.news_service import get_all_articles, add_article, get_articles_by_source

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