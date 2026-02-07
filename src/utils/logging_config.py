"""
Logging Configuration with Rotation

Provides structured logging with automatic log rotation to prevent disk space issues
"""

import logging
import os
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pathlib import Path


def setup_logging(
    log_dir: str = "logs",
    log_level: str = "INFO",
    max_bytes: int = 10 * 1024 * 1024,  # 10 MB
    backup_count: int = 5,
    use_json: bool = False
):
    """
    Configure application logging with rotation

    Args:
        log_dir: Directory to store log files
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        max_bytes: Maximum size of each log file before rotation
        backup_count: Number of backup files to keep
        use_json: Whether to use JSON formatting (for log aggregation)

    Returns:
        Configured logger
    """
    # Create logs directory
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)

    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # Remove existing handlers
    logger.handlers = []

    # Console handler (always use)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler with rotation (size-based)
    file_handler = RotatingFileHandler(
        filename=log_path / "nba_api.log",
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)

    if use_json:
        # JSON formatter for structured logging (ELK, Splunk, etc.)
        try:
            import json_log_formatter

            json_formatter = json_log_formatter.JSONFormatter()
            file_handler.setFormatter(json_formatter)
        except ImportError:
            # Fallback to standard formatter
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
    else:
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
        )
        file_handler.setFormatter(file_formatter)

    logger.addHandler(file_handler)

    # Error log file (separate file for errors only)
    error_handler = RotatingFileHandler(
        filename=log_path / "nba_api_errors.log",
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    )
    error_handler.setFormatter(error_formatter)
    logger.addHandler(error_handler)

    # Time-based rotation (daily logs)
    daily_handler = TimedRotatingFileHandler(
        filename=log_path / "nba_api_daily.log",
        when='midnight',
        interval=1,
        backupCount=30,  # Keep 30 days
        encoding='utf-8'
    )
    daily_handler.setLevel(logging.INFO)
    daily_handler.setFormatter(file_formatter)
    logger.addHandler(daily_handler)

    logger.info(f"Logging configured: level={log_level}, dir={log_dir}, rotation={max_bytes} bytes")

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the specified name"""
    return logging.getLogger(name)


# Example usage
if __name__ == "__main__":
    logger = setup_logging(log_level="DEBUG")
    logger.info("Test info message")
    logger.error("Test error message")
    logger.debug("Test debug message")
