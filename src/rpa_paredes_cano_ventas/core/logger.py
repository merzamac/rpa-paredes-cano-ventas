from pathlib import Path
from sys import stderr

from loguru import logger


def set_logger(logger_dir: Path) -> None:

    LOGGER_FORMAT = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "{extra} - <level>{message}</level>"
    )
    logger.remove()
    logger.add(stderr, format=LOGGER_FORMAT)
    logger.add(
        str(logger_dir) + "/{time:YYYY-MM-DD}.log",
        rotation="1 day",
        retention="30 days",
        compression="zip",
        enqueue=True,
        backtrace=False,
        diagnose=True,
        format=LOGGER_FORMAT,
    )
