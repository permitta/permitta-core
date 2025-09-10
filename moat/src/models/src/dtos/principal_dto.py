from dataclasses import dataclass

from .attribute_dto import AttributeDto


@dataclass
class PrincipalDto:
    principal_id: int
    first_name: str
    last_name: str
    user_name: str
    direct_attributes: list[AttributeDto]
    inherited_attributes: list[AttributeDto]
