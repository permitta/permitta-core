from abc import abstractmethod

from app_logger import Logger, get_logger
from ingestor.connectors import ConnectorBase
from ingestor.models import BaseDio

logger: Logger = get_logger("ingestor.controller.base")


class BaseIngestionController:

    def __init__(self):
        logger.info(f"Created controller of type {type(self)}")

    @abstractmethod
    def retrieve(self, connector: ConnectorBase) -> list[BaseDio]:
        pass

    @abstractmethod
    def stage(self, session, dios: list[BaseDio]) -> None:
        pass

    @abstractmethod
    def merge(
        self, session, ingestion_process_id: int, deactivate_omitted: bool = False
    ) -> None:
        pass
