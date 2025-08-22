from dataclasses import dataclass

from app_logger import Logger, get_logger
from database import Database
from ingestor.connectors import ConnectorBase, ConnectorFactory
from ingestor.models import (
    BaseDio,
)
from models import (
    ObjectTypeEnum,
)
from repositories import (
    IngestionProcessRepository,
    PrincipalRepository,
    ResourceRepository,
)
from .base_ingestion_controller import BaseIngestionController

from .principal_ingestion_controller import PrincipalIngestionController
from .principal_attribute_ingestion_controller import (
    PrincipalAttributeIngestionController,
)
from .resource_ingestion_controller import ResourceIngestionController
from .resource_attribute_ingestion_controller import (
    ResourceAttributeIngestionController,
)

logger: Logger = get_logger("ingestor.controller")


@dataclass
class IngestionStats:
    principal_count: int = 0
    principal_attribute_count: int = 0
    resource_count: int = 0
    resource_attribute_count: int = 0


class IngestionController:
    """
    Ingestion controller executes specific ingestion operations from different sources
    It is called by the CLI, probably in a k8s cronjob
    It is responsible for:
    * setting the status of ingestion_process objects
    * maintaining the staging tables
    * creating the ingestion connector classes (e.g ldap / trino)
    * pulling full or partial datasets from source systems into staging tables for:
      * principals
      * principal attributes
      * attribute groups / group attributes
      * data objects (tables & columns)
    * storing the results of ingestion operations, counts, errors etc
    * merging the results with the main tables

    * the ingestion controller will get the DBOs from the relevant connectors, i.e:
      * principals and attributes from LDAP
      * attribute groups from a JSON/YAML file
      * data objects (tables & columns) with attributes from trino

    * this controller should also provide a mutex via the ingestion process table to lock the staging tables
    """

    @staticmethod
    def _get_database() -> Database:
        database: Database = Database()
        database.connect()
        return database

    @staticmethod
    def _get_controller(
        object_type: ObjectTypeEnum,
    ) -> BaseIngestionController:
        if object_type == ObjectTypeEnum.PRINCIPAL:
            return PrincipalIngestionController()
        if object_type == ObjectTypeEnum.PRINCIPAL_ATTRIBUTE:
            return PrincipalAttributeIngestionController()
        if object_type == ObjectTypeEnum.RESOURCE:
            return ResourceIngestionController()
        if object_type == ObjectTypeEnum.RESOURCE_ATTRIBUTE:
            return ResourceAttributeIngestionController()
        raise ValueError(
            f"Object type {object_type} could not be mapped to an ingestion controller"
        )

    def ingest(
        self,
        connector_name: str,
        object_type: ObjectTypeEnum,
        platform: str,
        deactivate_omitted: bool = True,
    ) -> None:
        logger.info("Starting ingestion process")

        # TODO create mutex - in ingestion process table?
        database: Database = self._get_database()

        # create connector
        connector: ConnectorBase = ConnectorFactory.create_by_name(
            connector_name=connector_name
        )

        # create controller
        controller = self._get_controller(object_type=object_type)

        # load data into connector
        connector.acquire_data(platform=platform)

        # create the process id & truncate staging
        process_id: int = self._initialise_ingestion_process(
            database=database, connector_name=connector_name, object_types=[object_type]
        )

        # ingest into staging
        with database.Session.begin() as session:
            try:
                logger.info(f"Starting retrieve")
                dios: list[BaseDio] = controller.retrieve(
                    connector=connector,
                )

                # stage
                logger.info(f"Starting stage")
                controller.stage(session, dios)
                session.commit()
                logger.info(f"Commited data into staging table")
            except Exception as e:
                logger.error(f"Ingestion failed with error: {str(e)}")
                raise
                # TODO return error code

        # merge into main tables
        with database.Session.begin() as session:
            try:
                # merge
                logger.info(f"Starting merge")
                controller.merge(
                    session=session,
                    ingestion_process_id=process_id,
                    deactivate_omitted=deactivate_omitted,
                )

            finally:
                # close ingestion process
                logger.info(
                    f"Completing ingestion process with process ID: {process_id}"
                )
                IngestionProcessRepository.complete_process(
                    session=session, ingestion_process_id=process_id
                )
                session.commit()

    @staticmethod
    def _initialise_ingestion_process(
        database: Database, connector_name: str, object_types: list[ObjectTypeEnum]
    ) -> int:
        with database.Session.begin() as session:
            PrincipalRepository.truncate_staging_tables(session=session)
            ResourceRepository.truncate_staging_tables(session=session)

            process_id: int = IngestionProcessRepository.create(
                session=session,
                source=connector_name,
                object_types=object_types,
            )
            session.commit()

        logger.info(
            f"Created ingestion process with id: {process_id} for object types: {object_types}"
        )
        return process_id

    # def _ingest_principal_attributes(self, session, connector: ConnectorBase) -> int:
    #     principal_attribute_dios: list[PrincipalAttributeDio] = (
    #         connector.get_principal_attributes()
    #     )
    #     principal_attribute_count: int = self._stage_principal_attributes(
    #         session=session, principal_attribute_dios=principal_attribute_dios
    #     )
    #     logger.info(f"Retrieved {principal_attribute_count} principal attributes")
    #     return principal_attribute_count
    #
    # def _ingest_resource_attributes(self, session, connector: ConnectorBase) -> int:
    #     resource_attribute_dios: list[ResourceAttributeDio] = (
    #         connector.get_resource_attributes()
    #     )
    #     resource_attribute_count: int = self._stage_resource_attributes(
    #         session=session, resource_attribute_dios=resource_attribute_dios
    #     )
    #     logger.info(f"Retrieved {resource_attribute_count} resources")
    #     return resource_attribute_count
    #
    # @staticmethod
    # def _stage_principal_attributes(
    #     session, principal_attribute_dios: list[PrincipalAttributeDio]
    # ) -> int:
    #     principal_attribute_stgs: list[PrincipalAttributeStagingDbo] = []
    #     for principal_attribute_dio in principal_attribute_dios:
    #         principal_attribute_stg: PrincipalAttributeStagingDbo = (
    #             PrincipalAttributeStagingDbo()
    #         )
    #         principal_attribute_stg.source_uid = principal_attribute_dio.source_uid
    #         principal_attribute_stg.attribute_key = (
    #             principal_attribute_dio.attribute_key
    #         )
    #         principal_attribute_stg.attribute_value = (
    #             principal_attribute_dio.attribute_value
    #         )
    #         principal_attribute_stgs.append(principal_attribute_stg)
    #     session.add_all(principal_attribute_stgs)
    #     return len(principal_attribute_stgs)
    #
    # @staticmethod
    # def _stage_resource_attributes(
    #     session, resource_attribute_dios: list[ResourceAttributeDio]
    # ) -> int:
    #     resource_attribute_stgs: list[ResourceAttributeDio] = []
    #
    #     for resource_attribute_dio in resource_attribute_dios:
    #         resource_attribute_dio_stg: ResourceAttributeStagingDbo = (
    #             ResourceAttributeStagingDbo(
    #                 fq_name=resource_attribute_dio.fq_name,
    #                 attribute_key=resource_attribute_dio.attribute_key,
    #                 attribute_value=resource_attribute_dio.attribute_value,
    #             )
    #         )
    #         resource_attribute_stgs.append(resource_attribute_dio_stg)
    #     session.add_all(resource_attribute_stgs)
    #     return len(resource_attribute_stgs)
