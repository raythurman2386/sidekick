# Configuration

## Environment Setup

Create a `.env` file in the project root with the following settings:

```env
OLLAMA_HOST="http://localhost:11434"
AI_MODEL="deepseek-r1:latest"  # or your preferred model
```

## Configuration Options

### OLLAMA_HOST
- Default: `http://localhost:11434`
- Description: The URL where Ollama is running
- Note: Change this if you're running Ollama on a different port or host

### AI_MODEL
- Default: `deepseek-r1:latest`
- Description: The AI model to use for conversations
- Available options:
  - `deepseek-r1:latest`
  - `phi:latest`
  - Any other model installed through Ollama

## Verifying Configuration

1. Ensure Ollama is running in the background
2. Verify your model is properly installed:
   ```bash
   ollama list
   ```
3. Check that your `.env` file is in the correct location
4. Make sure the model specified in your `.env` file matches an installed model

## Next Steps

- [Running Sidekick](../usage/running.md)
- [Troubleshooting Configuration Issues](../troubleshooting.md)
