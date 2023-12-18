import atexit
import logging
import signal
import sys
from logging.handlers import RotatingFileHandler
from concurrent.futures import ThreadPoolExecutor


class AsyncRotatingFileHandler(RotatingFileHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.executor = ThreadPoolExecutor(max_workers=1)

    def emit(self, record):
        self.executor.submit(self._emit, record)

    def _emit(self, record):
        try:
            super().emit(record)
        except Exception:
            self.handleError(record)

    def close(self):
        self.executor.shutdown(wait=True)
        super().close()


# Set up a specific logger with our desired output level
app_logger = logging.getLogger("CogniBotLogger")
app_logger.setLevel(logging.INFO)

try:
    # Add the log message handler to the logger
    handler = AsyncRotatingFileHandler(
        "cognibot.log", maxBytes=1024 * 1024, backupCount=3  # 1 MB
    )

    # Create a formatter and set it for the handler
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    # Add the handler to the logger
    app_logger.addHandler(handler)
except Exception as e:
    print(f"Failed to set up logger: {e}")


# Function to close all handlers
def shutdown_logging():
    handlers = app_logger.handlers[:]
    for handler in handlers:
        handler.close()
        app_logger.removeHandler(handler)


# Register the shutdown function with atexit
atexit.register(shutdown_logging)


# Signal handling
def handle_exit_signal(signum, frame):
    shutdown_logging()
    # Perform other shutdown tasks here
    sys.exit(0)


signal.signal(signal.SIGTERM, handle_exit_signal)
signal.signal(signal.SIGINT, handle_exit_signal)
