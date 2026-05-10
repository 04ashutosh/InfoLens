from fastapi import APIRouter
from pydantic import BaseModel
from services.llm_service import generate_response, generate_embedding

router = APIRouter(prefix="/api/ai", tags=["AI"])

class PromptRequest(BaseModel):
    """What the user sends to the AI"""
    prompt: str
    model: str = "qwen2.5:7b" #Default model for generating responses

class SummaryRequest(BaseModel):
    """Request to summarize an article"""
    title: str
    content: str

class EmbeddingRequest(BaseModel):
    """Request to get embedding for text"""
    text: str

#---Endpoints---
@router.post("/generate")
def ai_generate(request: PromptRequest):
    """Send a raw prompt to the LLM"""
    response = generate_response(request.prompt, request.model)
    return {"response": response, "model": request.model}

@router.post("/summarize")
def ai_summarize(request: SummaryRequest):
    """Summarize a news article using the LLM"""
    prompt = f"""You are a neutral Indian journalist.
    Summarize the following news article in 3-4 concise bullet points.
    Be factual. Do not show political bias.

    Title: {request.title}
    Content: {request.content}

    Respond ONLY with the bullet points, nothing else.
    """

    response = generate_response(prompt)
    return {"summary": response, "title": request.title}

@router.post("/embed")
def ai_embed(request: EmbeddingRequest):
    """Convert text to embedding vector."""
    embedding = generate_embedding(request.text)
    return {
        "embedding": embedding[:5], #Show first 5 numbers only (preview)
        "dimensions": len(embedding),
        "text_preview": request.text[:100]
    }