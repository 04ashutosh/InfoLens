from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import APP_TITLE, APP_DESCRIPTION, APP_VERSION, FRONTEND_URL
from routers import health, sources, articles, ai

# Create app
app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers (like component scanning in Spring Boot)
app.include_router(health.router)
app.include_router(sources.router)
app.include_router(articles.router)
app.include_router(ai.router)