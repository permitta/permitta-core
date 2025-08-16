from unittest import mock

from database import Database
from ingestor.connectors import ConnectorFactory
from ingestor.models import PrincipalAttributeDio, PrincipalDio
from models import (
    IngestionProcessDbo,
    ObjectTypeEnum,
    PrincipalAttributeDbo,
    PrincipalDbo,
)
from repositories import IngestionProcessRepository, PrincipalRepository

from ..src.ingestion_controller import IngestionController


class TestConnector:
    NAME = "test"

    def acquire_data(self) -> None:
        pass

    def get_principals(self) -> list[PrincipalDio]:
        return [
            PrincipalDio(
                fq_name="1",
                first_name="bob",
                last_name="hawke",
                email="bob@bob.net",
                user_name="bobiscool34",
            ),
            PrincipalDio(
                fq_name="2",
                first_name="richard",
                last_name="fyneman",
                email="richard@bob.net",
                user_name="richardiscool76",
            ),
        ]

    def get_principal_attributes(self) -> list[PrincipalAttributeDio]:
        return [
            PrincipalAttributeDio(
                fq_name="1", attribute_key="group", attribute_value="bobs"
            ),
            PrincipalAttributeDio(
                fq_name="1", attribute_key="group", attribute_value="mechanics"
            ),
            PrincipalAttributeDio(
                fq_name="2", attribute_key="group", attribute_value="florists"
            ),
        ]

    def get_data_objects(self) -> list[PrincipalDio]:
        return []

    def get_data_object_attributes(self) -> list[PrincipalAttributeDio]:
        return []


def test_ingest(database_empty: Database):
    ingestion_controller = IngestionController()

    with mock.patch.object(
        ConnectorFactory, "create_by_name", return_value=TestConnector()
    ) as mock_create_by_name:
        ingestion_controller.ingest(
            connector_name="test",
            object_type=ObjectTypeEnum.PRINCIPAL,
        )
        mock_create_by_name.assert_called_once()

    with database_empty.Session.begin() as session:
        # ensure that the process id was created, then updated correctly
        ingestion_process_count, ingestion_processes = (
            IngestionProcessRepository.get_all(session=session)
        )
        assert ingestion_process_count == 1
        ingestion_process: IngestionProcessDbo = ingestion_processes[0]
        assert ingestion_process.status == "complete"
        assert ingestion_process.started_at < ingestion_process.completed_at

        # test that the right principals and attrs are in the DB transaction tables
        principal_count, principals = PrincipalRepository.get_all(session=session)
        assert principal_count == 2

        bob: PrincipalDbo = [p for p in principals if p.first_name == "bob"][0]
        assert bob.fq_name == "1"
        assert bob.last_name == "hawke"
        assert bob.user_name == "bobiscool34"

        assert len(bob.attributes) == 2
        assert [a.attribute_value for a in bob.attributes] == [
            "bobs",
            "mechanics",
        ]

        richard: PrincipalDbo = [p for p in principals if p.first_name == "richard"][0]
        assert richard.fq_name == "2"
        assert richard.last_name == "feynman"
        assert richard.user_name == "richardiscool76"
        assert len(bob.attributes) == 1

        # ensure the records in the DB have the right process ID
        assert all(
            [
                p.ingestion_process_id == ingestion_process.ingestion_process_id
                for p in principals
            ]
        )
        for principal in principals:
            for attribute in principal.attributes:
                assert (
                    attribute.ingestion_process_id
                    == ingestion_process.ingestion_process_id
                )
