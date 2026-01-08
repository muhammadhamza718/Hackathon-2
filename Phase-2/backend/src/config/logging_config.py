"""Centralized logging configuration for the Todo Chatbot backend"""
import logging
import sys
import os
from datetime import datetime
from typing import Optional
import json


def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    enable_console: bool = True,
    enable_json: bool = False
) -> logging.Logger:
    """
    Setup centralized logging configuration

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path to write logs to
        enable_console: Whether to output logs to console
        enable_json: Whether to format logs as JSON

    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger("todo_chatbot")
    logger.setLevel(getattr(logging, log_level.upper()))

    # Clear existing handlers
    logger.handlers.clear()

    # Create formatter
    if enable_json:
        formatter = JsonFormatter()
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )

    # Console handler
    if enable_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_level.upper()))
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # File handler
    if log_file:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, log_level.upper()))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


class JsonFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging"""

    def format(self, record):
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
            'file': record.pathname.split('/')[-1] if '/' in record.pathname else record.pathname.split('\\')[-1]
        }

        # Add exception info if present
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)

        # Add extra fields if present
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
        if hasattr(record, 'session_id'):
            log_entry['session_id'] = record.session_id
        if hasattr(record, 'request_id'):
            log_entry['request_id'] = record.request_id

        return json.dumps(log_entry)


# Global logger instance
logger = setup_logging(
    log_level=os.getenv("LOG_LEVEL", "INFO"),
    log_file=os.getenv("LOG_FILE", "logs/todo_chatbot.log"),
    enable_json=os.getenv("LOG_FORMAT_JSON", "false").lower() == "true"
)


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get a logger instance, optionally with a specific name"""
    if name:
        return logger.manager.getLogger(f"todo_chatbot.{name}")
    return logger


def log_api_call(
    endpoint: str,
    method: str,
    status_code: int,
    duration: float,
    user_id: Optional[str] = None,
    request_id: Optional[str] = None
):
    """Log API call with performance metrics"""
    extra = {
        'endpoint': endpoint,
        'method': method,
        'status_code': status_code,
        'duration_ms': duration * 1000,  # Convert to milliseconds
    }

    if user_id:
        extra['user_id'] = user_id
    if request_id:
        extra['request_id'] = request_id

    logger.info("API call completed", extra=extra)


def log_db_operation(
    operation: str,
    table: str,
    duration: float,
    success: bool,
    records_affected: int = 0,
    user_id: Optional[str] = None
):
    """Log database operation with performance metrics"""
    extra = {
        'operation': operation,
        'table': table,
        'duration_ms': duration * 1000,
        'success': success,
        'records_affected': records_affected
    }

    if user_id:
        extra['user_id'] = user_id

    logger.info("Database operation completed", extra=extra)


def log_mcp_call(
    operation: str,
    duration: float,
    success: bool,
    user_id: Optional[str] = None,
    request_id: Optional[str] = None
):
    """Log MCP server call with performance metrics"""
    extra = {
        'mcp_operation': operation,
        'duration_ms': duration * 1000,
        'success': success
    }

    if user_id:
        extra['user_id'] = user_id
    if request_id:
        extra['request_id'] = request_id

    logger.info("MCP operation completed", extra=extra)


def log_error(error: Exception, context: Optional[dict] = None, user_id: Optional[str] = None):
    """Log an error with context"""
    extra = {'error_type': type(error).__name__, 'error_message': str(error)}

    if context:
        extra.update(context)
    if user_id:
        extra['user_id'] = user_id

    logger.error(f"Error occurred: {str(error)}", extra=extra, exc_info=True)