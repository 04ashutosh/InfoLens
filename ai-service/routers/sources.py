from fastapi import APIRouter
from services.news_service import get_all_sources

router = APIRouter(prefix="/api",tags=["Sources"])

@router.get("/sources")
def list_sources():
    sources = get_all_sources()
    return {"sources": sources, "count": len(sources)}