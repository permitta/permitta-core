from datetime import datetime
from typing import Tuple

from database import Database
from models import IngestionProcessDbo, ObjectTypeEnum
from sqlalchemy import Row, and_
from sqlalchemy.orm import Query
from sqlalchemy.sql.elements import NamedColumn

from .repository_base import RepositoryBase


class IngestionProcessRepository(RepositoryBase):

    @staticmethod
    def get_all(session) -> Tuple[int, list[IngestionProcessDbo]]:
        query: Query = session.query(IngestionProcessDbo)
        return query.count(), query.all()

    @staticmethod
    def create(session, object_types: list[ObjectTypeEnum], source: str) -> int:
        ingestion_process_dbo: IngestionProcessDbo = IngestionProcessDbo()
        ingestion_process_dbo.source = source
        ingestion_process_dbo.object_type = ",".join([o.value for o in object_types])

        session.add(ingestion_process_dbo)
        session.flush()
        return ingestion_process_dbo.ingestion_process_id

    @staticmethod
    def get_by_id(session, ingestion_process_id: int) -> IngestionProcessDbo:
        ingestion_process_dbo: IngestionProcessDbo = (
            session.query(IngestionProcessDbo)
            .filter(IngestionProcessDbo.ingestion_process_id == ingestion_process_id)
            .first()
        )
        return ingestion_process_dbo

    @staticmethod
    def complete_process(session, ingestion_process_id: int) -> None:
        ingestion_process_dbo: IngestionProcessDbo = (
            IngestionProcessRepository.get_by_id(
                session=session, ingestion_process_id=ingestion_process_id
            )
        )
        ingestion_process_dbo.status = "complete"
        ingestion_process_dbo.completed_at = datetime.utcnow()
