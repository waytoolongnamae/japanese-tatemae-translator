"""
Central logging configuration.
"""
import logging
import os
from logging.handlers import RotatingFileHandler

from config.settings import (
    LOG_DIR,
    LOG_FILE_BACKUPS,
    LOG_FILE_MAX_BYTES,
    LOG_FILE_NAME,
    LOG_LEVEL,
    LOG_TO_FILE
)


def configure_logging() -> None:
    """Configure application logging once at startup."""
    log_level = getattr(logging, LOG_LEVEL, logging.INFO)
    handlers = [logging.StreamHandler()]

    if LOG_TO_FILE:
        os.makedirs(LOG_DIR, exist_ok=True)
        log_path = os.path.join(LOG_DIR, LOG_FILE_NAME)
        handlers.append(
            RotatingFileHandler(
                log_path,
                maxBytes=LOG_FILE_MAX_BYTES,
                backupCount=LOG_FILE_BACKUPS
            )
        )

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=handlers,
        force=True
    )
