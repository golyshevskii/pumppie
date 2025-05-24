import time
import logging

from core.settings import settings

def get_logger(name: str, level: int = settings.LOG_LEVEL) -> logging.Logger:
    """Get a custom logger."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    logs_path = f"{settings.LOGS_DIR}/{settings.NOW_DT_UTC.strftime('%Y-%m-%d')}.log"
    file_handler = logging.FileHandler(logs_path)
    file_handler.setLevel(level)

    formatter = logging.Formatter("%(asctime)s | %(name)s:%(lineno)d | %(levelname)s: %(message)s")
    formatter.converter = time.gmtime

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
