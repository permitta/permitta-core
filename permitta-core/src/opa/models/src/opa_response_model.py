from typing import Optional

from pydantic import BaseModel, Field


class OpaResponseModel(BaseModel):
    result: Optional[bool] = False
