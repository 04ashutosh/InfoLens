from fastapi import APIRouter
from config import APP_VERSION

# APIRouter = like a mini @RestController for one domain
router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "running",
        "service": "InfoLens AI",
        "version": APP_VERSION
    }