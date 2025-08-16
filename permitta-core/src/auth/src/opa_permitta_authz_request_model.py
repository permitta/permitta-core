from enum import Enum

from pydantic import BaseModel


class OpaPermittaAuthzActionEnum(Enum):
    NO_OPERATION = "NO_OPERATION"
    CREATE_POLICY = "CREATE_POLICY"
    EDIT_POLICY = "EDIT_POLICY"
    CLONE_POLICY = "CLONE_POLICY"
    UP_VERSION_POLICY = "UP_VERSION_POLICY"
    REQUEST_PUBLISH_POLICY = "REQUEST_PUBLISH_POLICY"
    REQUEST_DISABLE_POLICY = "REQUEST_DISABLE_POLICY"
    CANCEL_PUBLISH_POLICY = "CANCEL_PUBLISH_POLICY"
    CANCEL_DISABLE_POLICY = "CANCEL_DISABLE_POLICY"
    PUBLISH_POLICY = "PUBLISH_POLICY"
    DISABLE_POLICY = "DISABLE_POLICY"
    DELETE_POLICY = "DELETE_POLICY"


class OpaPermittaAuthzBaseModel(BaseModel):
    class Config:
        use_enum_values = True


class OpaPermittaAuthzAttributeModel(OpaPermittaAuthzBaseModel):
    key: str
    value: str


class OpaPermittaAuthzObjectModel(OpaPermittaAuthzBaseModel):
    type: str
    state: str
    attributes: list[OpaPermittaAuthzAttributeModel]


class OpaPermittaAuthzSubjectModel(OpaPermittaAuthzBaseModel):
    username: str
    attributes: list[OpaPermittaAuthzAttributeModel]


class OpaPermittaAuthzInputModel(OpaPermittaAuthzBaseModel):
    action: OpaPermittaAuthzActionEnum
    subject: OpaPermittaAuthzSubjectModel
    object: OpaPermittaAuthzObjectModel
