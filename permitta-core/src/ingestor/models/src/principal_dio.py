from dataclasses import dataclass

from .base_dio import BaseDio


@dataclass
class PrincipalDio(BaseDio):
    fq_name: str
    first_name: str
    last_name: str
    user_name: str
    email: str


@dataclass
class PrincipalAttributeDio(BaseDio):
    fq_name: str
    attribute_key: str
    attribute_value: str
