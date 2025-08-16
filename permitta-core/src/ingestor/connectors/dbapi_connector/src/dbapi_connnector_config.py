from app_config import AppConfigModelBase


class DBAPIConnectorConfig(AppConfigModelBase):
    CONFIG_PREFIX: str = "dbapi_connector"
    client_type: str = None
    data_object_table_column_query: str = None
    table_key: str = None
