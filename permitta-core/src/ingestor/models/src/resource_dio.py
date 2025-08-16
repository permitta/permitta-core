from dataclasses import dataclass

from .base_dio import BaseDio


@dataclass
class ResourceDio(BaseDio):
    fq_name: str
    object_type: str


@dataclass
class ResourceAttributeDio(BaseDio):
    fq_name: str
    attribute_key: str
    attribute_value: str
