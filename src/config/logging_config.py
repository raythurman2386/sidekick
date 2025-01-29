import os
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).parent.parent

# Logging configuration
LOGGING_CONFIG = {
    "development": {
        "log_level": "DEBUG",
        "log_dir": BASE_DIR / "logs" / "dev",
    },
    "production": {
        "log_level": "INFO",
        "log_dir": BASE_DIR / "logs" / "prod",
    },
    "testing": {
        "log_level": "DEBUG",
        "log_dir": None,  # Console only
    },
}

# Get environment from ENV variable, default to development
ENV = os.getenv("FLASK_ENV", "development")
CURRENT_LOGGING_CONFIG = LOGGING_CONFIG[ENV]
