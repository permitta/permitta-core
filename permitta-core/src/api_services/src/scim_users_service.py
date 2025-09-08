import copy
from app_logger import Logger, get_logger
from models import PrincipalDbo, PrincipalAttributeDbo
from .scim_service_config import ScimServiceConfig
from .scim_service_base import ScimServiceBase

logger: Logger = get_logger("scim2.service")
scim_service_config = ScimServiceConfig.load()


class ScimUsersService(ScimServiceBase):
    SOURCE_TYPE = "scim"

    @staticmethod
    def create_user(session, scim_payload: dict) -> dict:
        """
        Returns the updated payload which came from the original request
        """
        principal: PrincipalDbo = PrincipalDbo()
        principal = ScimUsersService.update_user(
            session=session,
            scim_payload=scim_payload,
            principal=principal,
        )

        session.add(principal)
        for attribute in principal.attributes:
            session.add(attribute)

        return scim_payload

    @staticmethod
    def update_user(
        session, principal: PrincipalDbo, scim_payload: dict
    ) -> PrincipalDbo:
        principal.fq_name = ScimServiceBase._get_jsonpath_attribute(
            scim_payload, scim_service_config.principal_fq_name_jsonpath
        )

        principal.first_name = ScimServiceBase._get_jsonpath_attribute(
            scim_payload, scim_service_config.principal_first_name_jsonpath
        )

        principal.last_name = ScimServiceBase._get_jsonpath_attribute(
            scim_payload, scim_service_config.principal_last_name_jsonpath
        )

        principal.user_name = ScimServiceBase._get_jsonpath_attribute(
            scim_payload, scim_service_config.principal_user_name_jsonpath
        )

        principal.email = ScimServiceBase._get_jsonpath_attribute(
            scim_payload, scim_service_config.principal_email_jsonpath
        )

        principal.source_uid = ScimServiceBase._get_jsonpath_attribute(
            scim_payload, scim_service_config.principal_source_uid_jsonpath
        )
        principal.source_type = ScimUsersService.SOURCE_TYPE
        principal.scim_payload = scim_payload

        # attributes
        if scim_service_config.principal_attributes_jsonpath:
            attributes: dict = (
                ScimServiceBase._get_jsonpath_attribute(
                    copy.deepcopy(scim_payload),
                    scim_service_config.principal_attributes_jsonpath,
                )
                or {}
            )

            # attributes should be a dict, with scalar or simple list values
            for attribute_key, attribute_value in attributes.items():
                if isinstance(attribute_value, list):  # flatten
                    attributes[attribute_key] = ",".join([a for a in attribute_value])

            # diff against existing attrs on the principal
            scim_attributes = [(k, v) for k, v in attributes.items()]
            principal_attributes = [
                (a.attribute_key, a.attribute_value) for a in principal.attributes
            ]

            # delete the removed attributes
            [
                session.delete(pa)
                for pa in principal.attributes
                if (pa.attribute_key, pa.attribute_value) not in scim_attributes
            ]

            added_attributes = [
                a for a in scim_attributes if a not in principal_attributes
            ]

            for attribute_key, attribute_value in added_attributes:
                attribute: PrincipalAttributeDbo = PrincipalAttributeDbo()
                attribute.fq_name = principal.fq_name
                attribute.attribute_key = attribute_key
                attribute.attribute_value = attribute_value
                principal.attributes.append(attribute)

        return principal
