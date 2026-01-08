"""
Logging utilities for the Todo Backend
"""
import logging
import sys
from typing import Optional
from logging.handlers import RotatingFileHandler


def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None):
    """
    Set up logging configuration for the application
    """
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper()))

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler if specified
    if log_file:
        file_handler = RotatingFileHandler(
            log_file, maxBytes=10*1024*1024, backupCount=5  # 10MB files, keep 5
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name
    """
    return logging.getLogger(name)