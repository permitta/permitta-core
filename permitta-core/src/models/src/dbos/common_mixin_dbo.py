from sqlalchemy import Boolean, Column, Integer
from sqlalchemy.orm import declared_attr


class IngestionDboMixin:
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    # these cannot be type-hinted or alchemy complains
    ingestion_process_id = Column(Integer)
    active = Column(Boolean, default=True, server_default="t")
