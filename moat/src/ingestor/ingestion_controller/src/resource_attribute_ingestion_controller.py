from app_logger import Logger, get_logger
from ingestor.connectors import ConnectorBase
from ingestor.models import (
    ResourceAttributeDio,
)
from models import (
    ResourceAttributeStagingDbo,
)
from repositories import (
    ResourceRepository,
)

from .base_ingestion_controller import BaseIngestionController

logger: Logger = get_logger("ingestor.controller.resource_attribute")


class ResourceAttributeIngestionController(BaseIngestionController):

    def retrieve(self, connector: ConnectorBase) -> list[ResourceAttributeDio]:
        resource_attr_dios: list[ResourceAttributeDio] = (
            connector.get_resource_attributes()
        )
        logger.info(f"Retrieved {len(resource_attr_dios)} resources")
        return resource_attr_dios

    def stage(self, session, dios: list[ResourceAttributeDio]) -> None:
        resource_attr_stgs: list[ResourceAttributeStagingDbo] = []

        for dio in dios:
            do_stg: ResourceAttributeStagingDbo = ResourceAttributeStagingDbo(
                fq_name=dio.fq_name,
                attribute_key=dio.attribute_key,
                attribute_value=dio.attribute_value,
            )
            resource_attr_stgs.append(do_stg)
        session.add_all(resource_attr_stgs)
        logger.info(f"Staged {len(resource_attr_stgs)} resources")

    def merge(
        self, session, ingestion_process_id: int, deactivate_omitted: bool = False
    ) -> None:
        logger.info("Starting merge process for resource attributes")

        ResourceRepository.merge_attributes_staging(
            session=session, ingestion_process_id=ingestion_process_id
        )

        logger.info(f"Starting merge deactivate process for principals")
        if deactivate_omitted:
            ResourceRepository.merge_attributes_deactivate_staging(
                session=session, ingestion_process_id=ingestion_process_id
            )
