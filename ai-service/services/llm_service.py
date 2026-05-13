import requests
from config import OLLAMA_BASE_URL
import json

def generate_response(prompt: str, model: str = "qwen2.5:7b")-> str:
    """
    Send a prompt to Ollama and get a response.
    """

    url = f"{OLLAMA_BASE_URL}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False, #Get full response at once
        "options": {
            "temperature": 0.3, #Low = more factual, less creative
            "num_predict": 1024 #Max tokens in response
        }
    }

    try:
        response = requests.post(url,json=payload,timeout=120)
        response.raise_for_status() # Raise an error for bad status codes
        result = response.json()
        return result.get("response", "No response from model.")
    except requests.exceptions.ConnectionError:
        return "ERROR: Ollama is not running. Start it with 'ollama serve'."
    except Exception as e:
        return f"ERROR: {str(e)}"
    
def generate_embedding(text: str, model: str = "nomic-embed-text")-> list: #Generate an embedding vector for the given text using Ollama
    """
    Convert text into a vector (list of numbers).
    Used later for clustering similar news stories
    """

    url = f"{OLLAMA_BASE_URL}/api/embed"
    payload = {
        "model": model,
        "input": text
    }
    try:
        response = requests.post(url,json=payload,timeout=60)
        response.raise_for_status()
        result = response.json()
        return result.get("embeddings", [[]])[0] #Return the first embedding vector
    except requests.exceptions.ConnectionError:
        return [] #Return empty list if Ollama is not running
    except Exception as e:
        print(f"Embedding error: {e}")
        return []

def analyze_article_bias(title: str, content: str) -> dict:
    """Uses Ollama to estimate the bias and tone of an article, returning strict JSON."""

    prompt = f"""
You are an impartial media analyst. Read the following news article and estimate its political bias and emotional tone.
You MUST respond in strict JSON format matching this schema exactly:
{{
    "bias_rating": "Left-Leaning" | "Center" | "Right-Leaning",
    "reasoning": "A 1-2 sentence explanation of why.",
    "emotional_tone": "Neutral" | "Sensationalized" | "Defensive"
}}

Article Title: {title}
Article Content: {content}
"""
    
    payload = {
        "model": "qwen2.5:7b",
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }

    try:
        response = requests.post(f"{OLLAMA_BASE_URL}/api/generate", json=payload)
        response.raise_for_status()
        result = response.json()

        # Parse the JSON string returned by Ollama into a Python dictionary
        return json.loads(result["response"])
    except Exception as e:
        print(f"Error analyzing bias: {e}")
        return{
            "bias_rating": "Unknown",
            "reasoning": "Failed to analyze bias due to an error.",
            "emotional_tone": "Unknown"
        }