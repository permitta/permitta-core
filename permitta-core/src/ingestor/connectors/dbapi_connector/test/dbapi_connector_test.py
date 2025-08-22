from unittest import mock

from clients import TrinoClient

from ..src.dbapi_connector import DBAPIConnector
from ingestor.models import ResourceDio, ResourceAttributeDio


# Create a list of 10 representative Trino table names with attributes
mock_resources = [
    {
        "fq_name": "catalog1.schema1.table1",
        "attribute_key": "it",
        "attribute_value": "commercial",
        "object_type": "table",
        "platform": "trino",
    },
    {
        "fq_name": "catalog1.schema1.table2",
        "attribute_key": "department",
        "attribute_value": "sales",
        "object_type": "table",
        "platform": "trino",
    },
    {
        "fq_name": "catalog1.schema2.table1",
        "attribute_key": "sensitivity",
        "attribute_value": "high",
        "object_type": "table",
        "platform": "trino",
    },
    {
        "fq_name": "catalog2.schema1.table1",
        "attribute_key": "owner",
        "attribute_value": "data_team",
        "object_type": "table",
        "platform": "trino",
    },
    {
        "fq_name": "catalog2.schema2.table1",
        "attribute_key": "retention",
        "attribute_value": "1year",
        "object_type": "table",
        "platform": "trino",
    },
    {
        "fq_name": "datalake.sales.orders",
        "attribute_key": "pii",
        "attribute_value": "false",
        "object_type": "table",
        "platform": "trino",
    },
    {
        "fq_name": "datalake.sales.customers",
        "attribute_key": "pii",
        "attribute_value": "true",
        "object_type": "table",
        "platform": "trino",
    },
    {
        "fq_name": "datalake.hr.employees",
        "attribute_key": "confidential",
        "attribute_value": "true",
        "object_type": "table",
        "platform": "trino",
    },
    {
        "fq_name": "datalake.finance.transactions",
        "attribute_key": "region",
        "attribute_value": "global",
        "object_type": "table",
        "platform": "trino",
    },
    {
        "fq_name": "datalake.marketing.campaigns",
        "attribute_key": "status",
        "attribute_value": "active",
        "object_type": "table",
        "platform": "trino",
    },
]


# Mock the select_async method to yield a batch of mock table names
def mock_select_async_generator(*args, **kwargs):
    yield mock_resources


@mock.patch.object(TrinoClient, "select_async", side_effect=mock_select_async_generator)
def test_get_resources(mock_select_async):
    # Create an instance of DBAPIConnector
    dbapi_connector = DBAPIConnector()
    dbapi_connector.acquire_data(platform="trino")

    # Call the get_resources
    resources: list[ResourceDio] = dbapi_connector.get_resources()

    # Assert that select_async was called with the expected query
    mock_select_async.assert_called_once_with(
        query=dbapi_connector.config.data_object_table_column_query
    )

    # Assert that the tables list contains the expected table names
    expected_table_names = [
        "catalog1.schema1.table1",
        "catalog1.schema1.table2",
        "catalog1.schema2.table1",
        "catalog2.schema1.table1",
        "catalog2.schema2.table1",
        "datalake.sales.orders",
        "datalake.sales.customers",
        "datalake.hr.employees",
        "datalake.finance.transactions",
        "datalake.marketing.campaigns",
    ]
    assert resources == [
        ResourceDio(fq_name=t, object_type="table", platform="trino")
        for t in expected_table_names
    ]


@mock.patch.object(TrinoClient, "select_async", side_effect=mock_select_async_generator)
def test_get_resource_attributes(mock_select_async):
    # Create an instance of DBAPIConnector
    dbapi_connector = DBAPIConnector()
    dbapi_connector.acquire_data(platform="trino")

    # Call the get_resource_attributes
    resource_attributes: list[ResourceAttributeDio] = (
        dbapi_connector.get_resource_attributes()
    )

    # Assert that select_async was called with the expected query
    mock_select_async.assert_called_once_with(
        query=dbapi_connector.config.data_object_table_column_query
    )

    # Assert that the attributes list contains the expected attributes
    expected_attributes = [
        ResourceAttributeDio(
            fq_name="catalog1.schema1.table1",
            attribute_key="it",
            attribute_value="commercial",
            platform="trino",
        ),
        ResourceAttributeDio(
            fq_name="catalog1.schema1.table2",
            attribute_key="department",
            attribute_value="sales",
            platform="trino",
        ),
        ResourceAttributeDio(
            fq_name="catalog1.schema2.table1",
            attribute_key="sensitivity",
            attribute_value="high",
            platform="trino",
        ),
        ResourceAttributeDio(
            fq_name="catalog2.schema1.table1",
            attribute_key="owner",
            attribute_value="data_team",
            platform="trino",
        ),
        ResourceAttributeDio(
            fq_name="catalog2.schema2.table1",
            attribute_key="retention",
            attribute_value="1year",
            platform="trino",
        ),
        ResourceAttributeDio(
            fq_name="datalake.sales.orders",
            attribute_key="pii",
            attribute_value="false",
            platform="trino",
        ),
        ResourceAttributeDio(
            fq_name="datalake.sales.customers",
            attribute_key="pii",
            attribute_value="true",
            platform="trino",
        ),
        ResourceAttributeDio(
            fq_name="datalake.hr.employees",
            attribute_key="confidential",
            attribute_value="true",
            platform="trino",
        ),
        ResourceAttributeDio(
            fq_name="datalake.finance.transactions",
            attribute_key="region",
            attribute_value="global",
            platform="trino",
        ),
        ResourceAttributeDio(
            fq_name="datalake.marketing.campaigns",
            attribute_key="status",
            attribute_value="active",
            platform="trino",
        ),
    ]

    assert resource_attributes == expected_attributes
