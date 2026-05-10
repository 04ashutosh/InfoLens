import requests
from config import OLLAMA_BASE_URL

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