from fastapi import FastAPI
from models.schemas import ArticleRequest, ArticleResponse
from fastapi.middleware.cors import CORSMiddleware

# Create app FIRST, then add middleware
app = FastAPI(
    title="Infolens AI Service",
    description="AI platform for Indian news intelligence",
    version="0.1.0"
)

# CORS must come AFTER app is created
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (temporary — replaced by MongoDB in Phase 10)
articles_db = []

# Health check
@app.get("/health")
def health_check():
    return {"status": "running", "service": "InfoLens AI"}

# Get all news sources
@app.get("/api/sources")
def get_sources():
    sources = [
        {"name": "The Hindu", "category": "Mainstream"},
        {"name": "NDTV", "category": "Mainstream"},
        {"name": "Republic TV", "category": "English"},
        {"name": "The Wire", "category": "Digital"},
        {"name": "Zee News", "category": "English"},
    ]
    return {"sources": sources, "count": len(sources)}

# Add article
@app.post("/api/articles", response_model=ArticleResponse)
def create_article(article: ArticleRequest):
    new_id = len(articles_db) + 1
    articles_db.append(article.model_dump())
    return ArticleResponse(
        id=new_id,
        title=article.title,
        source=article.source,
        message="Article added successfully"
    )

@app.get("/api/articles")
def get_articles():
    return {"articles": articles_db, "total": len(articles_db)}