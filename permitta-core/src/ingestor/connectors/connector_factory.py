from app_logger import Logger, get_logger

from .connector_base import ConnectorBase

logger: Logger = get_logger("ingestor.connectors.connector_factory")


class ConnectorFactory:
    @staticmethod
    def create_by_name(connector_name: str) -> ConnectorBase:
        for subclass in ConnectorBase.__subclasses__():
            if getattr(subclass, "CONNECTOR_NAME", None) == connector_name:
                logger.debug(f"Creating instance of connector class: {subclass}")
                return subclass()

        raise ValueError(f"Connector with name {connector_name} could not be found")
