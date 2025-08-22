
from pydantic import BaseModel


class OpaQueryResponseModel(BaseModel):
    result: list[dict]
