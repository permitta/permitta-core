from datetime import datetime

from database import BaseModel
from sqlalchemy import Boolean, Column, DateTime, String


class DecisionLogDbo(BaseModel):
    __tablename__ = "decision_logs"

    @property
    def f_q_object_name(self) -> str:
        return ".".join(
            f for f in [self.database, self.schema, self.table, self.column] if f
        )

    decision_log_id: str = Column(String, primary_key=True)
    path: str = Column(String)
    operation: str = Column(String)
    username: str = Column(String)
    database: str = Column(String)
    schema: str = Column(String)
    table: str = Column(String)
    column: str = Column(String)
    permitted: bool = Column(Boolean)
    expression: str = Column(String)
    timestamp: datetime = Column(DateTime(timezone=True))
