import json
import os
import uuid
from datetime import datetime
from typing import Type

import yaml
from database import BaseModel, Database
from models import (
    IngestionProcessDbo,
    PrincipalAttributeDbo,
    PrincipalDbo,
    ResourceDbo,
    ResourceAttributeDbo,
)

from .database_config import DatabaseConfig


class DatabaseSeeder:
    def __init__(self, db: Database):
        self.db = db

    @staticmethod
    def _get_principals() -> list[PrincipalDbo]:
        with open(
            os.path.join(DatabaseConfig.load().seed_data_path, "principals.json")
        ) as json_file:
            mock_users: list[dict] = json.load(json_file)
            principals: list[PrincipalDbo] = []

            for mock_user in mock_users:
                principal_dbo: PrincipalDbo = PrincipalDbo()
                principal_dbo.fq_name = str(uuid.uuid4())
                principal_dbo.activated_at = datetime.now()
                principal_dbo.deactivated_at = None
                principal_dbo.first_name = mock_user.get("first_name")
                principal_dbo.last_name = mock_user.get("last_name")
                principal_dbo.user_name = mock_user.get("username")

                # apply groups
                for group in mock_user.get("groups"):
                    principal_attribute_dbo = PrincipalAttributeDbo()
                    principal_attribute_dbo.fq_name = principal_dbo.fq_name
                    principal_attribute_dbo.attribute_key = "ad_group"
                    principal_attribute_dbo.attribute_value = group
                    principal_attribute_dbo.activated_at = datetime.utcnow()
                    principal_dbo.attributes.append(principal_attribute_dbo)

                principals.append(principal_dbo)
            return principals

    @staticmethod
    def _get_attributes(
        object_type: Type[BaseModel], raw_attrs: list[dict]
    ) -> list[BaseModel]:
        attributes: list[object_type] = []
        for raw_attr in raw_attrs:
            attribute = object_type()
            attribute.attribute_key = raw_attr["key"]
            attribute.attribute_value = raw_attr["value"]
            attributes.append(attribute)
        return attributes

    @staticmethod
    def _get_resources() -> list[ResourceDbo]:
        with open(
            os.path.join(DatabaseConfig.load().seed_data_path, "resources.json")
        ) as json_file:
            resources_data: list[dict] = json.load(json_file)
            resources: list[ResourceDbo] = []

            for resource_data in resources_data:
                resource_dbo: ResourceDbo = ResourceDbo()
                resource_dbo.fq_name = resource_data.get("fq_name")
                resource_dbo.platform = resource_data.get("platform")
                resource_dbo.object_type = resource_data.get("object_type")

                # # If there are attributes in the resource data, add them
                # if "attributes" in resource_data:
                #     for attr in resource_data.get("attributes", []):
                #         resource_attr_dbo = ResourceAttributeDbo()
                #         resource_attr_dbo.attribute_key = attr.get("key")
                #         resource_attr_dbo.attribute_value = attr.get("value")
                #         resource_dbo.attributes.append(resource_attr_dbo)
                #
                resources.append(resource_dbo)

            return resources

    def _ingest_resources(self):
        with self.db.Session.begin() as session:
            session.add_all(self._get_resources())
            session.commit()

    def _get_process_id(self, object_type: str) -> int:
        # create the process id
        ingestion_process_dbo: IngestionProcessDbo = IngestionProcessDbo()
        with self.db.Session.begin() as session:
            session.add(ingestion_process_dbo)
            ingestion_process_dbo.source = "Seed"
            ingestion_process_dbo.object_type = object_type
            session.flush()
            ingestion_process_id = ingestion_process_dbo.ingestion_process_id
            session.commit()
        return ingestion_process_id

    def _ingest_objects(self, object_type: str, object_list: list):
        ingestion_process_id = self._get_process_id(object_type)

        for obj in object_list:
            obj.ingestion_process_id = ingestion_process_id

        with self.db.Session.begin() as session:
            session.add_all(object_list)
            ingestion_process_dbo = session.get(
                IngestionProcessDbo, ingestion_process_id
            )
            ingestion_process_dbo.completed_at = datetime.utcnow()
            ingestion_process_dbo.status = "completed"
            session.commit()

    def seed(self):
        self._ingest_objects("Principal", self._get_principals())
        self._ingest_objects("Resources", self._get_resources())
