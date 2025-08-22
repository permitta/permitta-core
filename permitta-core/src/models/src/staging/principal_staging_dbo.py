from database import BaseModel
from sqlalchemy import Column, Integer, String


class PrincipalStagingDbo(BaseModel):
    __tablename__ = "principals_staging"

    MERGE_KEYS: list[str] = ["fq_name"]
    UPDATE_COLS: list[str] = ["first_name", "last_name", "user_name", "email"]

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    fq_name: str = Column(String)
    first_name: str = Column(String)
    last_name: str = Column(String)
    user_name: str = Column(String)
    email: str = Column(String)
