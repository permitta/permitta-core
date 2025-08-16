import logging
from logging import Logger

"""
Functionality:
* Provide a consistent logger
* Allow an entire http transaction to be identified
* Allow an entire ingestion to be identified with its process id
* Provide an event push interface? (maybe th job of something else?

"""

from app_config import AppConfigModelBase


class LoggerConfig(AppConfigModelBase):
    CONFIG_PREFIX: str = "logger"
    root_level: str = "INFO"


root_logger_name: str = "permitta"
logger_config: LoggerConfig = LoggerConfig().load()

root_logger = logging.getLogger(root_logger_name)  # root logger?
root_logger.setLevel(logger_config.root_level)

ch = logging.StreamHandler()

# create formatter and add it to the handler
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)

# add the handler to the logger
root_logger.addHandler(ch)


def get_logger(name: str) -> Logger:
    logger: Logger = logging.getLogger(f"{root_logger_name}.{name}")
    logger.setLevel(AppConfigModelBase.get_value(f"logger.{name}_level", "INFO"))
    return logger
