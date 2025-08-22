from dataclasses import dataclass

from .base_dio import BaseDio


@dataclass
class ResourceDio(BaseDio):
    object_type: str


@dataclass
class ResourceAttributeDio(BaseDio):
    attribute_key: str
    attribute_value: str
