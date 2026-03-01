"""
Logging utility module for ZURU Company Assistant.
Provides standardized, configurable logging setup across all modules.
"""

import logging
from logging.handlers import RotatingFileHandler
import os
import sys
from datetime import datetime
from pathlib import Path

# Project path configuration
PROJECT_ROOT: Path = Path(__file__).parent.parent.parent
LOG_DIR: Path = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)  # Create log directory if not exists

# Log file naming (date-based)
LOG_FILE_NAME: Path = LOG_DIR / f"zuru_assistant_{datetime.now().strftime('%Y%m%d')}.log"

# Log format configuration (includes timestamp, module, line number for debugging)
LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s"
DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"

# Log level mapping (standard Python logging levels)
LOG_LEVEL_MAP: dict[str, int] = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}

# Default log level (overridable via environment variable)
DEFAULT_LOG_LEVEL: str = os.getenv("ZURU_LOG_LEVEL", "INFO").upper()


def get_logger(name: str) -> logging.Logger:
    """
    Create and configure a logger instance with standardized settings.
    
    This function ensures consistent logging format and behavior across the application,
    avoiding duplicate handlers and providing both console and file output.
    
    Args:
        name: Name of the logger (typically __name__ of the calling module)
    
    Returns:
        Configured logging.Logger instance with console and file handlers
    
    Example:
        >>> from utils.logger import get_logger
        >>> logger = get_logger(__name__)
        >>> logger.info("Application started successfully")
    """
    # Prevent duplicate handlers when logger is imported multiple times
    logger: logging.Logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    # Set base log level (fallback to INFO if invalid level is provided)
    logger.setLevel(LOG_LEVEL_MAP.get(DEFAULT_LOG_LEVEL, logging.INFO))
    logger.propagate = False  # Disable propagation to root logger

    # 1. Console handler (output to stdout, INFO level and above)
    console_handler: logging.StreamHandler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(LOG_LEVEL_MAP.get(DEFAULT_LOG_LEVEL, logging.INFO))
    console_formatter: logging.Formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    console_handler.setFormatter(console_formatter)

    # 2. Rotating file handler (output to file, DEBUG level and above)
    # Rotates at 10MB per file, keeps up to 5 backup files
    file_handler: RotatingFileHandler = RotatingFileHandler(
        LOG_FILE_NAME,
        maxBytes=10 * 1024 * 1024,  # 10 MB per file
        backupCount=5,              # Keep up to 5 backup logs
        encoding="utf-8"            # Ensure universal character support
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(console_formatter)

    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# Default logger for quick import across modules
logger: logging.Logger = get_logger("zuru_company_assistant")