from app_config import AppConfigModelBase
from app_logger import Logger, get_logger
from database import Database
from ingestor.connectors import ConnectorBase, ConnectorFactory
from ingestor.models import (
    BaseDio,
    PrincipalAttributeDio,
    PrincipalDio,
    ResourceAttributeDio,
    ResourceDio,
)
from models import (
    IngestionProcessDbo,
    ObjectTypeEnum,
    PrincipalAttributeStagingDbo,
    PrincipalStagingDbo,
    ResourceAttributeStagingDbo,
    ResourceStagingDbo,
)
from repositories import (
    IngestionProcessRepository,
    PrincipalRepository,
    RepositoryBase,
    ResourceRepository,
)

from .base_ingestion_controller import BaseIngestionController

logger: Logger = get_logger("ingestor.controller.principal_attributes")


class PrincipalAttributeIngestionController(BaseIngestionController):

    def retrieve(self, connector: ConnectorBase) -> list[PrincipalAttributeDio]:
        principal_attr_dios: list[PrincipalAttributeDio] = (
            connector.get_principal_attributes()
        )
        logger.info(
            f"Retrieved {len(principal_attr_dios)} principal attributes from connector"
        )
        return principal_attr_dios

    def stage(self, session, principal_attr_dios: list[PrincipalAttributeDio]) -> None:
        stgs: list[PrincipalAttributeStagingDbo] = []
        for dio in principal_attr_dios:
            stg: PrincipalAttributeStagingDbo = PrincipalAttributeStagingDbo()
            stg.fq_name = dio.fq_name
            stg.attribute_key = dio.attribute_key
            stg.attribute_value = dio.attribute_value
            stgs.append(stg)
        session.add_all(stgs)
        logger.info(f"Staged {len(stgs)} principall attributes")

    def merge(
        self, session, ingestion_process_id: int, deactivate_omitted: bool = False
    ) -> None:
        logger.info("Starting merge process for principal attributes")
        PrincipalRepository.merge_attributes_staging(
            session=session, ingestion_process_id=ingestion_process_id
        )

        logger.info(f"Starting merge deactivate process for principal attributes")
        if deactivate_omitted:
            PrincipalRepository.merge_attributes_deactivate_staging(
                session=session, ingestion_process_id=ingestion_process_id
            )
