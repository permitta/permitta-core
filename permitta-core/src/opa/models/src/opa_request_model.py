from pydantic import BaseModel, Field


class OpaRequestModel(BaseModel):
    input: dict = Field(default_factory=dict)
