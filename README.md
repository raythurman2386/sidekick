# Sidekick - Your Desktop Companion

Sidekick is an intelligent conversational assistant for your desktop, powered by advanced chatGPT technology. It allows you to have natural conversations on a wide range of topics for an engaging and productive experience.

## Key Features

- Standalone desktop application with an intuitive user interface built with Custom Tkinter
- Seamlessly integrates into your workflow for on-demand assistance
- Conversations powered by OpenAI's robust natural language processing capabilities
- Recalls previous conversations using a local SQLite database for chat logs
- Lightweight and performs well even on low-powered machines
- Cross-platform support for Windows, Mac and Linux

## Installation

Sidekick requires Python 3.6 or higher. It is recommended to create a virtual environment before installation.

```
python3 -m venv venv
source venv/bin/activate
```

Install the requirements:

```
pip install -r requirements.txt
```

You will need an OpenAI API key to use this project. You can get one for free from the OpenAI website [here](https://platform.openai.com/account/api-keys).

Once you have an API key, create a .env file and set your env variable:

```
OPENAI_API_KEY="<your_key_here>"
```

You can then run sidekick:

```
python main.py
```

## How It Works

Sidekick provides a text-based conversational interface using OpenAI's advanced models under the hood. You can ask questions, seek opinions or advice, or simply have free-flowing discussions on various topics. Sidekick remembers important context from previous conversations using a local SQLite database, allowing it to provide relevant and personalized responses.

The application has a compact footprint and responsive performance even on low-powered machines. The Python-based architecture makes it highly cross-platform as well, supporting Windows, MacOS and Linux with the same codebase.

Overall, Sidekick aims to be an engaging, intelligent and productive addition to your desktop environment. Its conversational capabilities help augment your work, learning, research or even casual interests that you discuss with it.

### Build

If you want to build your own and pin it to your taskbar or startmenu

Pyinstaller is currently in the requirements.txt, so if you properly installed the dependencies you should be able to run:

`pyinstaller --onefile --windowed --icon="images/sidekick.ico" --noconsole --hidden-import=tkinter --name="Sidekick" --add-data="images:images"  main.py`
