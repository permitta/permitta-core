from app_logger import Logger, get_logger
from clients import TrinoClient
from ingestor.connectors.connector_base import ConnectorBase
from ingestor.models import ResourceAttributeDio, ResourceDio

from .dbapi_connnector_config import DBAPIConnectorConfig

logger: Logger = get_logger("ingestor.connectors.dbapi_connector")


class DBAPIConnector(ConnectorBase):
    CONNECTOR_NAME: str = "dbapi"

    def __init__(self):
        super().__init__()
        self.config: DBAPIConnectorConfig = DBAPIConnectorConfig.load()
        logger.info("Created DBAPI connector")
        self.tables: list[str] = []

        if not self.config.client_type == "trino":
            raise ValueError("Only trino clients are available")

        self.trino_client: TrinoClient = TrinoClient()

    def acquire_data(self) -> None:
        pass

    def get_resources(self) -> list[ResourceDio]:
        """
        The get tables function brings in all table objects from the source system e.g trino regardless of applied auth rules
        Query for the source system is supplied in the config
        """
        # Get the SQL query from the config
        query = self.config.data_object_table_column_query

        # Execute the query and process the results
        tables: list[str] = []
        try:
            for batch in self.trino_client.select_async(query=query):
                tables.extend([record.get(self.config.table_key) for record in batch])

            logger.info(f"Ingested {len(tables)} table records")
        except Exception as e:
            self._log_error(str(e))
            raise

        return [ResourceDio(fq_name=fq_name, object_type="table") for fq_name in tables]

    def get_resource_attributes(self) -> list[ResourceAttributeDio]:
        """
        Gets the attributes of a table and returns them as a list.
        This will allow merge of attributes without removing objects

        Returns:
            list[DataObjectAttributeDio]: A list of table attributes.
        """
        resource_attrs: list[dict] = []
        query = self.config.data_object_table_column_query
        try:
            for batch in self.trino_client.select_async(query=query):
                resource_attrs.extend(batch)

            logger.info(f"Ingested {len(resource_attrs)} table records")
        except Exception as e:
            self._log_error(str(e))
            raise

        return [ResourceAttributeDio(**ta) for ta in resource_attrs]
