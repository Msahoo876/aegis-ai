"""
Enterprise Logging Configuration

Provides a centralized logging configuration
for the Aegis AI platform.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from rich.console import Console
from rich.logging import RichHandler

from app.core.config import settings

# ==========================================================
# Directories
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

LOG_DIR = BASE_DIR / "logs"

LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"

# ==========================================================
# Console
# ==========================================================

console = Console()

# ==========================================================
# Logger
# ==========================================================

LOGGER_NAME = settings.APP_NAME

logger = logging.getLogger(LOGGER_NAME)

logger.setLevel(settings.LOG_LEVEL.upper())

logger.handlers.clear()

# ==========================================================
# Formatter
# ==========================================================

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
)

# ==========================================================
# Rich Console Handler
# ==========================================================

console_handler = RichHandler(
    rich_tracebacks=True,
    show_time=True,
    show_level=True,
    show_path=False,
)

console_handler.setFormatter(formatter)

# ==========================================================
# File Handler
# ==========================================================

file_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=5 * 1024 * 1024,
    backupCount=5,
    encoding="utf-8",
)

file_handler.setFormatter(formatter)

# ==========================================================
# Register Handlers
# ==========================================================

logger.addHandler(console_handler)

logger.addHandler(file_handler)

logger.propagate = False