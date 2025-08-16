import click
from ingestor import IngestionController
from models import ObjectTypeEnum


@click.group()
def cli():
    pass


@cli.command()
@click.option("--source", default="ldap", help="Source to ingest from")
@click.option(
    "--object-type",
    type=click.Choice([e.value for e in ObjectTypeEnum]),
    default=ObjectTypeEnum.RESOURCE.value,
    help="Type of object to ingest",
)
def ingest(source, object_type):
    ingestion_controller = IngestionController()
    ingestion_controller.ingest(
        connector_name=source,
        object_type=ObjectTypeEnum(object_type),
    )


@cli.command()
def ingest_all():
    """
    This is a temporary hack to ingest all data from LDAP and DBAPI sources.
    """
    import os
    from _scripts.create_db import create_db

    create_db()

    ingestion_controller = IngestionController()

    os.environ["CONFIG_FILE_PATH"] = "permitta/config/config.principal_ingestion.yaml"
    ingestion_controller.ingest(
        connector_name="ldap",
        object_type=ObjectTypeEnum.PRINCIPAL,
    )

    os.environ["CONFIG_FILE_PATH"] = "permitta/config/config.principal_ingestion.yaml"
    ingestion_controller.ingest(
        connector_name="ldap",
        object_type=ObjectTypeEnum.PRINCIPAL_ATTRIBUTE,
    )

    os.environ["CONFIG_FILE_PATH"] = "permitta/config/config.resource_ingestion.yaml"
    ingestion_controller.ingest(
        connector_name="dbapi",
        object_type=ObjectTypeEnum.RESOURCE,
    )

    os.environ["CONFIG_FILE_PATH"] = (
        "permitta/config/config.resource_attribute_ingestion.yaml"
    )
    ingestion_controller.ingest(
        connector_name="dbapi",
        object_type=ObjectTypeEnum.RESOURCE_ATTRIBUTE,
    )


if __name__ == "__main__":
    cli()
