#!/bin/bash

# Text colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting Sidekick Installation...${NC}"

# Check if running on macOS or Linux
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS installation
    if ! command -v ollama &> /dev/null; then
        echo -e "${YELLOW}Installing Ollama for macOS...${NC}"
        curl -fsSL https://ollama.ai/install.sh | sh
    fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux installation
    if ! command -v ollama &> /dev/null; then
        echo -e "${YELLOW}Installing Ollama for Linux...${NC}"
        curl -fsSL https://ollama.ai/install.sh | sh
    fi
else
    echo "Unsupported operating system"
    exit 1
fi

# Start Ollama service
echo -e "${YELLOW}Starting Ollama service...${NC}"
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS service start
    ollama serve &
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux service start
    systemctl --user start ollama || ollama serve &
fi

# Wait for Ollama service to start
sleep 5

# Pull the small llama2 model
echo -e "${YELLOW}Downloading Llama2 model (this may take a while)...${NC}"
ollama pull llama2

# Create Python virtual environment
echo -e "${YELLOW}Setting up Python environment...${NC}"
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

# Activate virtual environment and install requirements
source .venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt

# Run PyInstaller
echo -e "${YELLOW}Building executable...${NC}"
pyinstaller --noconfirm --onefile --windowed \
    --add-data "src/images:images" \
    --icon "src/images/sidekick.png" \
    --name "Sidekick" \
    "src/main.py"

echo -e "${GREEN}Installation complete!${NC}"
echo -e "${GREEN}You can find the Sidekick executable in the 'dist' folder.${NC}"

# Deactivate virtual environment
deactivate
