import re

from app_logger import Logger, get_logger
from clients import LdapClient
from ingestor.connectors.connector_base import ConnectorBase
from ingestor.models import PrincipalAttributeDio, PrincipalDio

from .ldap_connector_config import LdapConnectorConfig

logger: Logger = get_logger("ingestor.connectors.ldap_connector")


class LdapConnector(ConnectorBase):
    CONNECTOR_NAME: str = "ldap"
    AD_GROUP_ATTRIBUTE_KEY: str = "ad_group"

    def __init__(self):
        super().__init__()
        self.ldap_users: list[dict] = []
        self.config: LdapConnectorConfig = LdapConnectorConfig.load()
        logger.info("Created LDAP connector")

    def acquire_data(self) -> None:
        ldap_client: LdapClient = LdapClient()
        ldap_client.connect()
        self.ldap_users: list[dict] = ldap_client.list_users(
            user_search_base=self.config.user_search_base,
            user_search_filter=self.config.user_search_filter,
            attributes=self.config.attributes,
        )
        logger.info(f"Retrieved {len(self.ldap_users)} LDAP users from ldap client")

    def get_principals(self) -> list[PrincipalDio]:
        principals: list[PrincipalDio] = []

        for ldap_user in self.ldap_users:
            try:
                principal: PrincipalDio = PrincipalDio(
                    fq_name=ldap_user.get(self.config.attr_user_id)[
                        0
                    ],  # HACK these should not be arrays
                    first_name=ldap_user.get(self.config.attr_first_name)[0],
                    last_name=ldap_user.get(self.config.attr_last_name)[0],
                    user_name=ldap_user.get(self.config.attr_user_name)[0],
                    email=ldap_user.get(self.config.attr_email)[0],
                )
                principals.append(principal)
            except (KeyError, IndexError):
                self._log_error(f"Error ingesting LDAP user: {ldap_user}")
        return principals

    def get_principal_attributes(self) -> list[PrincipalAttributeDio]:
        attributes: list[PrincipalAttributeDio] = []

        for ldap_user in self.ldap_users:
            try:
                fq_name: str = ldap_user.get(self.config.attr_user_id)[0]
                group_dns: list[str] = ldap_user.get(self.config.attr_groups)

                for group_dn in group_dns:
                    group_cn: str = re.search(
                        self.config.group_name_regex, group_dn, re.IGNORECASE
                    ).group(1)

                    attribute: PrincipalAttributeDio = PrincipalAttributeDio(
                        fq_name=fq_name,
                        attribute_key=self.AD_GROUP_ATTRIBUTE_KEY,
                        attribute_value=group_cn,
                    )
                    attributes.append(attribute)
            except KeyError:
                self._log_error(f"Error ingesting LDAP user: {ldap_user}")
        return attributes
