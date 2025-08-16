from app_config import AppConfigModelBase


class LdapClientConfig(AppConfigModelBase):
    CONFIG_PREFIX: str = "ldap_client"
    host: str = None
    port: int = None
    user_dn: str = None
    password: str = None
    base_dn: str = None
    user_base_dn: str = None
