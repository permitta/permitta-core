from app_config import AppConfigModelBase


class ApiConfig(AppConfigModelBase):
    CONFIG_PREFIX: str = "api"
    auth_method: str = None
    api_key: str = None
    oauth2_issuer: str = None
    oauth2_audience: str = None

    @classmethod
    def load_by_api_name(cls, api_name: str) -> "ApiConfig":
        return ApiConfig.load(config_prefix=f"{cls.CONFIG_PREFIX}.{api_name}")
