from app_logger import Logger, get_logger
from models import AttributeDto

from opa import OpaClient

from .opa_authz_provider_config import OpaAuthzProviderConfig
from .opa_permitta_authz_request_model import (
    OpaPermittaAuthzActionEnum,
    OpaPermittaAuthzAttributeModel,
    OpaPermittaAuthzInputModel,
    OpaPermittaAuthzObjectModel,
    OpaPermittaAuthzSubjectModel,
)

logger: Logger = get_logger("auth.opa")


class OpaAuthzProvider:
    def __init__(self, user_name: str, user_attributes: list[AttributeDto]) -> None:
        self.config: OpaAuthzProviderConfig = OpaAuthzProviderConfig().load()
        self.user_name: str = user_name
        self.user_attributes: list[AttributeDto] = user_attributes
        self.opa_client: OpaClient = OpaClient()

    def apply_policy_to_opa(self) -> None:
        # push rego to OPA TODO - this should be a bundle
        self.opa_client.put_policy(
            policy_name=self.config.policy_name,
            policy_file_path=self.config.policy_file_path,
        )

    def authorize(
        self,
        action: OpaPermittaAuthzActionEnum,
        object_type: str,
        object_state: str,
        object_attributes: list[AttributeDto],
    ) -> bool:
        request_model: OpaPermittaAuthzInputModel = OpaPermittaAuthzInputModel(
            action=action,
            subject=OpaPermittaAuthzSubjectModel(
                username=self.user_name,
                attributes=[
                    OpaPermittaAuthzAttributeModel(
                        key=a.attribute_key, value=a.attribute_value
                    )
                    for a in self.user_attributes
                ],
            ),
            object=OpaPermittaAuthzObjectModel(
                type=object_type,
                state=object_state,
                attributes=[
                    OpaPermittaAuthzAttributeModel(
                        key=a.attribute_key, value=a.attribute_value
                    )
                    for a in object_attributes
                ],
            ),
        )

        # hand to OPA client
        return self.opa_client.authorise_request(request_model=request_model) or False

    def get_allowed_policy_actions(
        self, object_state: str, object_attributes: list[AttributeDto]
    ) -> list[OpaPermittaAuthzActionEnum]:
        request_model: OpaPermittaAuthzInputModel = OpaPermittaAuthzInputModel(
            action=OpaPermittaAuthzActionEnum.NO_OPERATION,
            subject=OpaPermittaAuthzSubjectModel(
                username=self.user_name,
                attributes=[
                    OpaPermittaAuthzAttributeModel(
                        key=a.attribute_key, value=a.attribute_value
                    )
                    for a in self.user_attributes
                ],
            ),
            object=OpaPermittaAuthzObjectModel(
                type="POLICY",
                state=object_state,
                attributes=[
                    OpaPermittaAuthzAttributeModel(
                        key=a.attribute_key, value=a.attribute_value
                    )
                    for a in object_attributes
                ],
            ),
        )
        return [
            OpaPermittaAuthzActionEnum(a)
            for a in self.opa_client.get_allowed_policy_actions(
                request_model=request_model
            )
        ]
