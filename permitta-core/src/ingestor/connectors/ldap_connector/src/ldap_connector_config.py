from app_config import AppConfigModelBase


class LdapConnectorConfig(AppConfigModelBase):
    CONFIG_PREFIX: str = "ldap_connector"

    @property
    def attributes(self) -> list[str]:
        return [
            self.attr_user_name,
            self.attr_user_id,
            self.attr_first_name,
            self.attr_last_name,
            self.attr_email,
            self.attr_groups,
        ]

    user_search_base: str = None
    user_search_filter: str = None
    attr_user_name: str = None
    attr_user_id: str = None
    attr_first_name: str = None
    attr_last_name: str = None
    attr_email: str = None
    attr_groups: str = None
    group_name_regex: str = r"(.*)"
