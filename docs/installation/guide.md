# Installation Guide

Sidekick provides automated installation scripts that will set up everything you need, including Ollama and a default AI model. Choose the appropriate method for your operating system:

## Automated Installation

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

## Manual Installation

If you prefer to install components manually, follow these steps:

1. Create a virtual environment:
```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On Mac/Linux
source venv/bin/activate
```

2. Install the requirements:
```bash
pip install -r requirements.txt
```

## Next Steps

- [Configure Sidekick](configuration.md)
- [Running Sidekick](../usage/running.md)
- [Troubleshooting](../troubleshooting.md)
