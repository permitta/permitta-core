from ldap3 import ALL, Connection, Server
from ldap3.core.exceptions import LDAPBindError, LDAPException

from .ldap_client_config import LdapClientConfig


class LdapClient:
    _config: LdapClientConfig
    _connection: Connection

    def __init__(self):
        self._config: LdapClientConfig = LdapClientConfig.load()

    def connect(self) -> None:
        try:
            server_uri = f"ldap://{self._config.host}:{int(self._config.port)}"
            server = Server(server_uri, get_info=ALL)

            self._connection = Connection(
                server,
                user=self._config.user_dn,
                password=self._config.password,
            )

            bind_response = self._connection.bind()  # Returns True or False
            # TODO log connection result

            if not bind_response:
                raise LDAPBindError()
        except LDAPBindError as e:
            raise e

    def list_users(
        self, user_search_base: str, user_search_filter: str, attributes: list[str]
    ) -> list[dict]:

        try:
            self._connection.search(
                search_base=user_search_base,
                search_filter=user_search_filter,
                attributes=attributes,
            )
            entries = self._connection.entries
            # TODO make the following use .value instead of a list
            return [e.entry_attributes_as_dict for e in entries]
        except LDAPException as e:
            raise e
