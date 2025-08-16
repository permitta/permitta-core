from database import Database
from models import IngestionProcessDbo, ObjectTypeEnum

from ..src.ingestion_process_repository import IngestionProcessRepository


def create(database: Database) -> None:
    with database.Session.begin() as session:
        id: int = IngestionProcessRepository.create(
            session=session,
            object_types=[ObjectTypeEnum.PRINCIPAL, ObjectTypeEnum.PRINCIPAL_ATTRIBUTE],
            source="ldap",
        )
        session.commit()

    with database.Session.begin() as session:
        ingestion_process_dbo: IngestionProcessDbo = (
            IngestionProcessRepository.get_by_id(ingestion_process_id=id)
        )
        assert ingestion_process_dbo.object_type == "principal,principal_attribute"
        assert ingestion_process_dbo.source == "ldap"
