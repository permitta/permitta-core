from app_logger import Logger, get_logger
from ingestor.connectors import ConnectorBase
from ingestor.models import (
    PrincipalDio,
)
from models import (
    PrincipalStagingDbo,
)
from repositories import (
    PrincipalRepository,
)

from .base_ingestion_controller import BaseIngestionController

logger: Logger = get_logger("ingestor.controller.principal")


class PrincipalIngestionController(BaseIngestionController):

    def retrieve(self, connector: ConnectorBase) -> list[PrincipalDio]:
        principal_dios: list[PrincipalDio] = connector.get_principals()
        logger.info(f"Retrieved {len(principal_dios)} principals from connector")
        return principal_dios

    def stage(self, session, principal_dios: list[PrincipalDio]) -> None:
        principal_stgs: list[PrincipalStagingDbo] = []
        for principal_dio in principal_dios:
            principal_stg: PrincipalStagingDbo = PrincipalStagingDbo()
            principal_stg.fq_name = principal_dio.fq_name
            principal_stg.first_name = principal_dio.first_name
            principal_stg.last_name = principal_dio.last_name
            principal_stg.user_name = principal_dio.user_name
            principal_stg.email = principal_dio.email
            principal_stgs.append(principal_stg)
        session.add_all(principal_stgs)
        logger.info(f"Staged {len(principal_stgs)} principals")

    def merge(
        self, session, ingestion_process_id: int, deactivate_omitted: bool = False
    ) -> None:
        logger.info("Starting merge process for principals")
        PrincipalRepository.merge_staging(
            session=session, ingestion_process_id=ingestion_process_id
        )

        logger.info(f"Starting merge deactivate process for principals")
        if deactivate_omitted:
            PrincipalRepository.merge_deactivate_staging(
                session=session, ingestion_process_id=ingestion_process_id
            )
