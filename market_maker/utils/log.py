import logging
from market_maker.settings import settings


def setup_custom_logger(name, log_level=settings.LOG_LEVEL):
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    
    fileHandler = logging.FileHandler('fundonebot.log')
    fileHandler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    logger.addHandler(handler)
    logger.addHandler(fileHandler)
    return logger
