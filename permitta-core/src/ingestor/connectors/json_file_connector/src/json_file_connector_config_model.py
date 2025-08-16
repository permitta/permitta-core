from app_config import AppConfigModelBase


class JsonFileConnectorConfigModel(AppConfigModelBase):
    CONFIG_PREFIX: str = "connector.json_file.principals"
    file_path: str = None
