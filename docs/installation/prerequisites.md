# Prerequisites

Before installing Sidekick, you need to set up Ollama on your system:

1. Install Ollama from [ollama.com](https://ollama.com)
2. You can install AI models in two ways:
   - **Through the UI**: Open Sidekick's settings (⚙️) and use the "Install New Model" section. Enter the model name (e.g., `phi:latest`) and click "Install Model". Please be patient during the download as models can be quite large (several gigabytes).
   - **Through the command line**:
     ```bash
     ollama pull deepseek-r1:latest
     # or
     ollama pull phi:latest
     ```

## System Requirements

- Python 3.10 or higher
- Sufficient disk space for AI models (several GB depending on the model)
- Operating System: Windows, Mac, or Linux
