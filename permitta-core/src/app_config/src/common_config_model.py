from .app_config_model_base import AppConfigModelBase


class CommonConfigModel(AppConfigModelBase):
    CONFIG_PREFIX: str = "common"
    db_connection_string: str = None
    super_secret: str = None
