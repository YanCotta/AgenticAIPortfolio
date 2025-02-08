"""Logging configuration using Loguru."""

from loguru import logger
import sys

def configure_logger(log_level: str = "INFO"):
    """
    Configures the global logger settings.

    Args:
        log_level (str, optional): The logging level. Defaults to "INFO".
    """
    logger.remove()  # Remove default handler
    logger.add(
        "logs/app.log",  # Path to the log file
        level=log_level,  # Logging level from settings
        rotation="10 MB",  # Rotate log file when it reaches 10 MB
        retention="1 week",  # Keep logs for one week
        compression="zip",  # Compress the log file
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}:{function}:{line} - {message}",  # Log format
        enqueue=True,  # Make logging thread-safe
    )
    logger.add(sys.stderr, level=log_level, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}:{function}:{line} - {message}")  # Output to console

def get_logger(name: str):
    """
    Retrieves a logger with the specified name.

    Args:
        name (str): The name of the logger.

    Returns:
        loguru.Logger: A logger instance with the specified name.
    """
    return logger.bind(name=name)
