import requests

OLLAMA_API_URL = "http://localhost:11434/api"


def generate_chat_completion(messages, model="deepseek-r1", temperature=0.4):
    """
    Generate a chat completion using a local Ollama model
    """
    try:
        response = requests.post(
            f"{OLLAMA_API_URL}/chat",
            json={
                "model": model,
                "messages": messages,
                "stream": True,
                "options": {"temperature": temperature},
            },
            stream=True,
            timeout=30,
        )
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        if "Connection refused" in str(e):
            raise Exception(
                "Could not connect to Ollama. Make sure Ollama is running locally."
            ) from e
        raise Exception(f"Error calling Ollama API: {str(e)}") from e


def list_models():
    """
    Get list of available local models
    """
    try:
        response = requests.get(f"{OLLAMA_API_URL}/tags", timeout=5)
        response.raise_for_status()
        models = response.json().get("models", [])
        return sorted([model["name"] for model in models])
    except requests.RequestException:
        return []
