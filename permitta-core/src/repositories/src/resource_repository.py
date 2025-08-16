from typing import Tuple

from database import BaseModel
from models import (
    ResourceAttributeStagingDbo,
    ResourceDbo,
    ResourceStagingDbo,
    ResourceAttributeDbo,
)
from sqlalchemy.orm import Query
from sqlalchemy.sql import text

from .repository_base import RepositoryBase


class ResourceRepository(RepositoryBase):
    # TODO base class
    @staticmethod
    def get_all(session) -> Tuple[int, list[ResourceDbo]]:
        query: Query = session.query(ResourceDbo)
        return query.count(), query.all()

    @staticmethod
    def get_all_by_platform(session, platform: str) -> Tuple[int, list[ResourceDbo]]:
        query: Query = (
            session.query(ResourceDbo)
            .filter(ResourceDbo.platform == platform)
            .order_by(ResourceDbo.fq_name)
        )
        return query.count(), query.all()

    # TODO base class
    @staticmethod
    def get_by_id(session, resource_id: int) -> ResourceDbo:
        resource: ResourceDbo = (
            session.query(ResourceDbo).filter(ResourceDbo.id == resource_id).first()
        )
        return resource

    # TODO base class
    @staticmethod
    def truncate_staging_tables(session) -> None:
        models: list[type[BaseModel]] = [
            ResourceStagingDbo,
            ResourceAttributeStagingDbo,
        ]
        session.execute(
            text(f"truncate {','.join([model.__tablename__ for model in models])}")
        )
        for model in models:
            session.execute(
                text(f"alter sequence {model.__tablename__}_id_seq restart with 1")
            )

    @staticmethod
    def merge_staging(session, ingestion_process_id: int) -> int:
        merge_stmt: str = RepositoryBase._get_merge_statement(
            source_model=ResourceStagingDbo,
            target_model=ResourceDbo,
            merge_keys=ResourceStagingDbo.MERGE_KEYS,
            update_cols=ResourceStagingDbo.UPDATE_COLS,
            ingestion_process_id=ingestion_process_id,
        )
        result = session.execute(text(merge_stmt))
        return result.rowcount

    @staticmethod
    def merge_deactivate_staging(session, ingestion_process_id: int) -> int:
        merge_stmt: str = RepositoryBase._get_merge_deactivate_statement(
            source_model=ResourceStagingDbo,
            target_model=ResourceDbo,
            merge_keys=ResourceStagingDbo.MERGE_KEYS,
            ingestion_process_id=ingestion_process_id,
        )
        result = session.execute(text(merge_stmt))
        return result.rowcount

    @staticmethod
    def merge_attributes_staging(session, ingestion_process_id: int) -> int:
        merge_stmt: str = RepositoryBase._get_merge_statement(
            source_model=ResourceAttributeStagingDbo,
            target_model=ResourceAttributeDbo,
            merge_keys=ResourceAttributeStagingDbo.MERGE_KEYS,
            update_cols=ResourceAttributeStagingDbo.UPDATE_COLS,
            ingestion_process_id=ingestion_process_id,
        )
        result = session.execute(text(merge_stmt))
        return result.rowcount

    @staticmethod
    def merge_attributes_deactivate_staging(session, ingestion_process_id: int) -> int:
        merge_stmt: str = RepositoryBase._get_merge_deactivate_statement(
            source_model=ResourceAttributeStagingDbo,
            target_model=ResourceAttributeDbo,
            merge_keys=ResourceAttributeStagingDbo.MERGE_KEYS,
            ingestion_process_id=ingestion_process_id,
        )
        result = session.execute(text(merge_stmt))
        return result.rowcount
