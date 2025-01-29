#!/usr/bin/env pwsh
# Sidekick Installation Script

Write-Host "Starting Sidekick Installation..." -ForegroundColor Green

# Check if Ollama is installed
if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Ollama..." -ForegroundColor Yellow
    # Download Ollama installer
    Invoke-WebRequest -Uri "https://ollama.ai/download/ollama-windows-amd64.zip" -OutFile "ollama.zip"
    Expand-Archive -Path "ollama.zip" -DestinationPath "ollama"
    Move-Item -Path "ollama\ollama.exe" -Destination "$env:LOCALAPPDATA\Microsoft\WindowsApps"
    Remove-Item -Path "ollama.zip" -Force
    Remove-Item -Path "ollama" -Recurse -Force
}

# Start Ollama service
Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden

# Wait for Ollama service to start
Start-Sleep -Seconds 5

# Pull the small llama2 model
Write-Host "Downloading Llama2 model (this may take a while)..." -ForegroundColor Yellow
ollama pull llama2

# Create Python virtual environment
Write-Host "Setting up Python environment..." -ForegroundColor Yellow
if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

# Activate virtual environment and install requirements
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

# Run PyInstaller
Write-Host "Building executable..." -ForegroundColor Yellow
pyinstaller --noconfirm --onefile --windowed `
    --add-data "src/images;images" `
    --icon "src/images/sidekick.png" `
    --name "Sidekick" `
    "src/main.py"

Write-Host "Installation complete!" -ForegroundColor Green
Write-Host "You can find the Sidekick executable in the 'dist' folder." -ForegroundColor Green

# Deactivate virtual environment
deactivate
