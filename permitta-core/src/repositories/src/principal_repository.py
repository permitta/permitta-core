from typing import Tuple

from database import Database
from models import (
    AttributeDto,
    PrincipalAttributeDbo,
    PrincipalAttributeStagingDbo,
    PrincipalDbo,
    PrincipalStagingDbo,
)
from sqlalchemy import Row, and_, func, or_
from sqlalchemy.orm import Query
from sqlalchemy.sql import Subquery, text
from sqlalchemy.sql.elements import NamedColumn

from .repository_base import RepositoryBase


class PrincipalRepository(RepositoryBase):

    @staticmethod
    def truncate_staging_tables(session) -> None:
        for model in [PrincipalStagingDbo, PrincipalAttributeStagingDbo]:
            session.execute(text(f"truncate {model.__tablename__}"))
            session.execute(
                text(f"alter sequence {model.__tablename__}_id_seq restart with 1")
            )

    @staticmethod
    def get_all(session) -> Tuple[int, list[PrincipalDbo]]:
        query: Query = session.query(PrincipalDbo)
        return query.count(), query.all()

    @staticmethod
    def get_by_id(session, principal_id: int) -> PrincipalDbo:
        principal: PrincipalDbo = (
            session.query(PrincipalDbo)
            .filter(PrincipalDbo.principal_id == principal_id)
            .first()
        )
        return principal

    @staticmethod
    def get_by_username(session, user_name: str) -> PrincipalDbo:
        principal: PrincipalDbo = (
            session.query(PrincipalDbo)
            .filter(PrincipalDbo.user_name == user_name)
            .first()
        )
        return principal

    @staticmethod
    def merge_staging(session, ingestion_process_id: int) -> int:
        merge_stmt: str = PrincipalRepository._get_merge_statement(
            source_model=PrincipalStagingDbo,
            target_model=PrincipalDbo,
            merge_keys=PrincipalStagingDbo.MERGE_KEYS,
            update_cols=PrincipalStagingDbo.UPDATE_COLS,
            ingestion_process_id=ingestion_process_id,
        )
        result = session.execute(text(merge_stmt))
        return result.rowcount

    @staticmethod
    def merge_deactivate_staging(session, ingestion_process_id: int) -> int:
        merge_stmt: str = PrincipalRepository._get_merge_deactivate_statement(
            source_model=PrincipalStagingDbo,
            target_model=PrincipalDbo,
            merge_keys=PrincipalStagingDbo.MERGE_KEYS,
            ingestion_process_id=ingestion_process_id,
        )
        result = session.execute(text(merge_stmt))
        return result.rowcount

    @staticmethod
    def merge_attributes_staging(session, ingestion_process_id: int) -> int:
        merge_stmt: str = PrincipalRepository._get_merge_statement(
            source_model=PrincipalAttributeStagingDbo,
            target_model=PrincipalAttributeDbo,
            merge_keys=PrincipalAttributeStagingDbo.MERGE_KEYS,
            update_cols=PrincipalAttributeStagingDbo.UPDATE_COLS,
            ingestion_process_id=ingestion_process_id,
        )
        result = session.execute(text(merge_stmt))
        return result.rowcount

    @staticmethod
    def merge_attributes_deactivate_staging(session, ingestion_process_id: int) -> int:
        merge_stmt: str = PrincipalRepository._get_merge_deactivate_statement(
            source_model=PrincipalAttributeStagingDbo,
            target_model=PrincipalAttributeDbo,
            merge_keys=PrincipalAttributeStagingDbo.MERGE_KEYS,
            ingestion_process_id=ingestion_process_id,
        )
        result = session.execute(text(merge_stmt))
        return result.rowcount
