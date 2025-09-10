from enum import Enum


class AuthzObjectTypeEnum(Enum):
    POLICY = "POLICY"
    PRINCIPAL = "PRINCIPAL"
    PRINCIPAL_ATTRIBUTE = "PRINCIPAL_ATTRIBUTE"
