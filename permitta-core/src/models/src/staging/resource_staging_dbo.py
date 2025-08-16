from database import BaseModel
from sqlalchemy import Column, Integer, String


class ResourceStagingDbo(BaseModel):
    __tablename__ = "resources_stg"

    MERGE_KEYS: list[str] = ["fq_name"]
    UPDATE_COLS: list[str] = ["platform", "object_type"]

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    fq_name: str = Column(String)
    platform: str = Column(String)
    object_type: str = Column(String)


class ResourceAttributeStagingDbo(BaseModel):
    __tablename__ = "resource_attributes_stg"

    MERGE_KEYS: list[str] = ["fq_name", "attribute_key"]
    UPDATE_COLS: list[str] = ["attribute_key", "attribute_value"]

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    fq_name: str = Column(String)
    attribute_key: str = Column(String)
    attribute_value: str = Column(String)
