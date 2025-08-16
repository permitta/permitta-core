from pydantic import BaseModel, Field


class OpaQueryModel(BaseModel):
    query: str = Field()
    input: dict = Field(default_factory=dict)
