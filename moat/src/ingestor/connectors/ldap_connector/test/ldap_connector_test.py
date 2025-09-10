import json
from unittest import mock

from clients import LdapClient

from ..src.ldap_connector import LdapConnector
from ingestor.models import PrincipalDio, PrincipalAttributeDio

with open("moat/src/ingestor/connectors/ldap_connector/test/ldap_users.json") as f:
    ldap_users: list[dict] = json.load(f)


@mock.patch.object(LdapClient, "connect")
@mock.patch.object(LdapClient, "list_users", return_value=ldap_users)
def test_acquire_data(mock_list_users: mock.MagicMock, mock_connect: mock.MagicMock):
    ldap_connector: LdapConnector = LdapConnector()
    ldap_connector.acquire_data(platform="ad")

    mock_list_users.assert_called_with(
        user_search_base="ou=people,dc=example,dc=com",
        user_search_filter="(&(uid=*)(memberof=cn=moat_users_gl,ou=groups,dc=example,dc=com))",
        attributes=["uid", "uid", "givenname", "sn", "mail", "memberOf"],
    )
    mock_connect.assert_called_once()

    # principals
    principals: list[PrincipalDio] = ldap_connector.get_principals()
    assert len(principals) == 198  # admin is ignored
    assert principals[0].fq_name == "abigail.hamilton"
    assert principals[0].first_name == "Abigail"
    assert principals[0].last_name == "Hamilton"
    assert principals[0].user_name == "abigail.hamilton"
    assert principals[0].email == "abigail.hamilton@example.com"

    # principal attributes (groups)
    principal_attributes: list[PrincipalAttributeDio] = (
        ldap_connector.get_principal_attributes()
    )
    assert len(principal_attributes) == 200  # everyone has one group except abigail

    # abigail is in cn=SALES_SUPERVISORS_GL,ou=groups,dc=example,dc=com, cn=HR_ANALYSTS_GL,ou=groups,dc=example,dc=com
    assert principal_attributes[0].fq_name == "abigail.hamilton"
    assert principal_attributes[0].attribute_key == "ad_group"
    assert principal_attributes[0].attribute_value == "SALES_SUPERVISORS_GL"

    assert principal_attributes[1].fq_name == "abigail.hamilton"
    assert principal_attributes[1].attribute_key == "ad_group"
    assert principal_attributes[1].attribute_value == "HR_ANALYSTS_GL"

    # Adam Porter is in cn=MARKETING_SUPERVISORS_GL,ou=groups,dc=example,dc=com
    assert principal_attributes[3].fq_name == "adam.porter"
    assert principal_attributes[3].attribute_key == "ad_group"
    assert principal_attributes[3].attribute_value == "MARKETING_SUPERVISORS_GL"

    assert principal_attributes[5].fq_name == "ahmet.akyüz"
