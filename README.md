# Sidekick - Your Local AI Desktop Companion

Sidekick is an intelligent conversational assistant for your desktop, powered by local AI through Ollama. It provides a seamless desktop experience for interacting with various AI models while keeping all your data private and secure on your local machine.

## Key Features

- 🖥️ Standalone desktop application with an intuitive user interface built with Custom Tkinter
- 🚀 Fast responses with local AI processing
- 🔒 Complete privacy - all processing happens on your machine
- 💾 Conversation history stored in local SQLite database
- 🪶 Lightweight and efficient performance
- 🌐 Cross-platform support for Windows, Mac and Linux

## Prerequisites

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

## Installation

Sidekick now provides automated installation scripts that will set up everything you need, including Ollama and a default AI model. Choose the appropriate method for your operating system:

### Windows

1. Open PowerShell as Administrator
2. Navigate to the project directory
3. Run:
```powershell
Set-ExecutionPolicy RemoteSigned -Scope Process; .\install.ps1
```

### Linux/MacOS

1. Open Terminal
2. Navigate to the project directory
3. Run:
```bash
chmod +x install.sh
./install.sh
```

The installation script will:
- Install Ollama if not already installed
- Download and set up a small Llama2 model
- Create a Python virtual environment
- Install all required dependencies
- Build the executable using PyInstaller

After installation completes, you'll find the Sidekick executable in the `dist` folder.

### Manual Installation

If you prefer to install components manually, follow these steps:

Sidekick requires Python 3.10 or higher. We recommend creating a virtual environment:

```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On Mac/Linux
source venv/bin/activate
```

Install the requirements:
```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root:
```env
OLLAMA_HOST="http://localhost:11434"
AI_MODEL="deepseek-r1:latest"  # or your preferred model
```

## Running Sidekick

Start the application:
```bash
python main.py
```

## Building from Source

To create a standalone executable:

```bash
pyinstaller --onefile --windowed --icon="src/images/sidekick.ico" --noconsole --hidden-import=tkinter --name="Sidekick" --add-data="src/images:images" src/main.py
```

The executable will be created in the `dist` directory.

## How It Works

Sidekick provides a text-based conversational interface using Ollama's local AI models. All processing happens on your machine, ensuring privacy and quick response times. The application stores conversation history in a local SQLite database, allowing for context-aware interactions while maintaining data privacy.

## Troubleshooting

1. Ensure Ollama is running in the background
2. Verify your model is properly installed using `ollama list`
3. Check the Ollama host URL in your `.env` file
4. Make sure your system meets the minimum requirements for your chosen model

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the BSD 3-Clause License - see the LICENSE file for details.
