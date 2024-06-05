import logging


def setup_logging() -> logging.Logger:
    """Sets up the logging configuration for the application.

    This function configures the logging settings with a specific format for log messages,
    a date format, and a log level. It then creates and returns a logger instance with a
    specified name and log level.

    Returns:
        logging.Logger: A configured logger instance named 'pycrossword'.
    """
    logging.basicConfig(
        format="%(asctime)s %(message)s", datefmt="%I:%M:%S", level=logging.ERROR
    )
    logger = logging.getLogger("pycrossword")
    logger.setLevel(logging.DEBUG)
    return logger
