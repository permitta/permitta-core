from logging import Logger

from app_logger import get_logger

logger: Logger = get_logger("ingestor")

from .connectors.ldap_connector.src.ldap_connector import LdapConnector
from .ingestion_controller.src.ingestion_controller import IngestionController
