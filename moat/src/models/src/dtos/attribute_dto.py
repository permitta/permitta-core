from dataclasses import dataclass


@dataclass
class AttributeDto:
    attribute_key: str | None
    attribute_value: str
