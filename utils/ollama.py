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


def install_model(model_name, progress_callback=None):
    """
    Install a model using Ollama's pull endpoint with progress tracking
    
    Args:
        model_name (str): Name of the model to install
        progress_callback (callable): Optional callback function that receives progress updates
        
    Returns:
        bool: True if installation was successful, False otherwise
    """
    try:
        response = requests.post(
            f"{OLLAMA_API_URL}/pull",
            json={"name": model_name},
            stream=True,
            timeout=600  # 10 minute timeout for large models
        )
        response.raise_for_status()
        
        for line in response.iter_lines():
            if not line:
                continue
            
            try:
                data = requests.compat.json.loads(line)
                status = data.get("status", "")
                
                if progress_callback and status:
                    # Extract download progress if available
                    if "downloading" in data:
                        total = data["downloading"].get("total", 0)
                        completed = data["downloading"].get("completed", 0)
                        if total > 0:
                            progress = (completed / total) * 100
                            progress_callback(f"Downloading: {progress:.1f}% - {status}")
                        else:
                            progress_callback(f"Downloading - {status}")
                    # Extract other status updates
                    else:
                        progress_callback(status)
                        
            except requests.compat.json.JSONDecodeError:
                continue
                
        return True
        
    except requests.RequestException as e:
        if progress_callback:
            progress_callback(f"Error: {str(e)}")
        return False
