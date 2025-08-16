from database import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class PrincipalAttributeStagingDbo(BaseModel):
    __tablename__ = "principal_attributes_stg"

    MERGE_KEYS: list[str] = ["fq_name"]
    UPDATE_COLS: list[str] = ["attribute_key", "attribute_value"]

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    fq_name: str = Column(String)
    attribute_key: str = Column(String)
    attribute_value: str = Column(String)
