from app_config import AppConfigModelBase


class OpaClientConfig(AppConfigModelBase):
    CONFIG_PREFIX: str = "opa_client"

    scheme: str = "http"
    hostname: str = "localhost"
    port: str = "8181"
    path: str = "/v1/data/moat/authz/allow"
    timeout_seconds: str = "1"
