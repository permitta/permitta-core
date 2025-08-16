
from app_config import AppConfigModelBase


class OpaAuthzProviderConfig(AppConfigModelBase):
    CONFIG_PREFIX: str = "opa_authz_provider"

    policy_name: str = "permitta/authz"
    policy_file_path: str = None
