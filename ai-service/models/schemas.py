from pydantic import BaseModel
from typing import Optional, List

# ---Request Models (what client sends)---
class ArticleRequest(BaseModel):
    """Input model - what the client sends (like a Java Request DTO)."""
    title: str
    source: str
    content: str
    category: Optional[str] = "General"

# ---Response Models (what server returns)---
class ArticleResponse(BaseModel):
    """Output model - what the server returns (like a Java Response DTO.)"""
    id: int
    title: str
    source: str
    message: str

class SourceInfo(BaseModel):
    """Single news source info."""
    name: str
    category: str
    rss_url: str

class SourcesListResponse(BaseModel):
    """Response for /api/sources"""
    sources: List[SourceInfo]
    count: int

class ArticleDetail(BaseModel):
    """Full article with all fields."""
    id: int
    title: str
    source: str
    content: str
    category: str
    created_at: str

class ArticlesListResponse(BaseModel):
    """Response for /api/articles."""
    articles: List[ArticleDetail]
    total: int

class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    service: str
    version: str

class ErrorResponse(BaseModel):
    """Standard error response."""
    error: str
    detail: str