# Running Sidekick

## Starting the Application

After installation, you can start Sidekick in one of two ways:

### Using the Executable

If you installed Sidekick using the automated installation scripts, you'll find the executable in the `dist` folder. Simply double-click the executable to start the application.

### Using Python

If you installed Sidekick manually, you can start it using Python:

```bash
# Ensure you're in the virtual environment
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# Start the application
python main.py
```

## First Run

1. When you first start Sidekick, it will:
   - Check for Ollama installation
   - Verify the configured AI model is available
   - Initialize the local SQLite database for conversation history

2. The main interface will appear, showing:
   - Chat input area
   - Settings button (⚙️)
   - Conversation history (if any)

## Using Sidekick

1. Type your message in the input area
2. Press Enter or click Send to start a conversation
3. The AI will process your input locally and respond
4. Your conversation will be automatically saved

## Settings

Access settings by clicking the ⚙️ button:
- Change AI models
- Install new models
- Configure system settings

## Next Steps

- [Building from Source](building.md)
- [How It Works](how-it-works.md)
- [Troubleshooting](../troubleshooting/troubleshooting.md)
