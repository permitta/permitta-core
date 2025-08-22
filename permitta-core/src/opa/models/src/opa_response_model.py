from typing import Optional

from pydantic import BaseModel


class OpaResponseModel(BaseModel):
    result: Optional[bool] = False
