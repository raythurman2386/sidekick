# Building from Source

This guide explains how to build Sidekick from source code to create a standalone executable.

## Prerequisites

Ensure you have:
- Python 3.10 or higher installed
- Git (to clone the repository)
- PyInstaller (installed via requirements.txt)

## Building Steps

1. Clone the repository (if you haven't already):
   ```bash
   git clone https://github.com/raythurman2386/sidekick.git
   cd sidekick
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Build the executable:
   ```bash
   pyinstaller --onefile --windowed --icon="src/images/sidekick.ico" --noconsole --hidden-import=tkinter --name="Sidekick" --add-data="src/images:images" src/main.py
   ```

## Build Options Explained

- `--onefile`: Creates a single executable file
- `--windowed`: Prevents a console window from appearing
- `--icon`: Sets the application icon
- `--noconsole`: Hides the console window
- `--hidden-import`: Includes necessary imports
- `--add-data`: Includes additional resources

## Output

The built executable will be located in the `dist` directory. You can run it directly from there.

## Verifying the Build

1. Navigate to the `dist` directory
2. Run the Sidekick executable
3. Verify that:
   - The application starts without errors
   - The UI appears correctly
   - All features are working as expected

## Troubleshooting Build Issues

If you encounter issues during the build:

1. Ensure all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

2. Clear PyInstaller cache:
   ```bash
   # Windows
   rmdir /s /q build
   # Mac/Linux
   rm -rf build/
   ```

3. Try rebuilding with the verbose flag:
   ```bash
   pyinstaller --onefile --windowed --icon="src/images/sidekick.ico" --noconsole --hidden-import=tkinter --name="Sidekick" --add-data="src/images:images" src/main.py -v
   ```
