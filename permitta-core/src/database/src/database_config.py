from app_config import AppConfigModelBase


class DatabaseConfig(AppConfigModelBase):
    CONFIG_PREFIX: str = "database"

    @property
    def connection_string(self) -> str:
        return f"{self.protocol}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    protocol: str = None
    user: str = None
    password: str = None
    host: str = None
    port: int = None
    database: str = None
    seed_data_path: str = None
