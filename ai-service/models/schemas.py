from pydantic import BaseModel
from typing import Optional

class ArticleRequest(BaseModel):
    """Input model - what the client sends (like a Java Request DTO)."""
    title: str
    source: str
    content: str
    category: Optional[str] = "General"

class ArticleResponse(BaseModel):
    """Output model - what the server returns (like a Java Response DTO.)"""
    id: int
    title: str
    source: str
    message: str