"""
Logging and Error Handling Module
Centralized logging for all operations
"""

import logging
import os
from datetime import datetime

# Configure logging
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE = os.path.join(LOG_DIR, f"system_{datetime.now().strftime('%Y%m%d')}.log")

# Create logger
logger = logging.getLogger("StudentRecordSystem")
logger.setLevel(logging.DEBUG)

# File handler
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.DEBUG)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)

# Formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


def log_info(message, context=None):
    """Log info level message"""
    if context:
        message = f"{message} | {context}"
    logger.info(message)


def log_error(message, exception=None, context=None):
    """Log error level message"""
    if exception:
        message = f"{message} | Exception: {str(exception)}"
    if context:
        message = f"{message} | {context}"
    logger.error(message)


def log_debug(message):
    """Log debug level message"""
    logger.debug(message)


def log_operation(operation, status, details=None):
    """Log database operation"""
    msg = f"Operation: {operation} | Status: {status}"
    if details:
        msg += f" | Details: {details}"
    if status.lower() == 'success':
        log_info(msg)
    else:
        log_error(msg)
