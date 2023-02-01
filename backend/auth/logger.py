from loguru import logger


def add_loggers():
    logger.add(
        "logs/debug.log",
        format="{time} {level} {message}",
        level="DEBUG",
        rotation="1 week",
        compression="zip",
    )
    logger.add(
        "logs/info.log",
        format="{time} {level} {message}",
        level="INFO",
        rotation="1 week",
        compression="zip",
    )
    logger.add(
        "logs/error.log",
        format="{time} {level} {message}",
        level="ERROR",
        rotation="1 week",
        compression="zip",
    )
