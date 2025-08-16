from unittest import mock

from clients import TrinoClient

from ..src.dbapi_connector import DBAPIConnector
from ingestor.models import ResourceDio, ResourceAttributeDio


# Create a list of 10 representative Trino table names with attributes
mock_resources = [
    {"fq_name": "catalog1.schema1.table1", "attribute_key": "it", "attribute_value": "commercial"},
    {"fq_name": "catalog1.schema1.table2", "attribute_key": "department", "attribute_value": "sales"},
    {"fq_name": "catalog1.schema2.table1", "attribute_key": "sensitivity", "attribute_value": "high"},
    {"fq_name": "catalog2.schema1.table1", "attribute_key": "owner", "attribute_value": "data_team"},
    {"fq_name": "catalog2.schema2.table1", "attribute_key": "retention", "attribute_value": "1year"},
    {"fq_name": "datalake.sales.orders", "attribute_key": "pii", "attribute_value": "false"},
    {"fq_name": "datalake.sales.customers", "attribute_key": "pii", "attribute_value": "true"},
    {"fq_name": "datalake.hr.employees", "attribute_key": "confidential", "attribute_value": "true"},
    {"fq_name": "datalake.finance.transactions", "attribute_key": "region", "attribute_value": "global"},
    {"fq_name": "datalake.marketing.campaigns", "attribute_key": "status", "attribute_value": "active"},
]


# Mock the select_async method to yield a batch of mock table names
def mock_select_async_generator(*args, **kwargs):
    yield mock_resources


@mock.patch.object(TrinoClient, "select_async", side_effect=mock_select_async_generator)
def test_get_resources(mock_select_async):
    # Create an instance of DBAPIConnector
    dbapi_connector = DBAPIConnector()

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
    assert resources == [ResourceDio(fq_name=t, object_type="table") for t in expected_table_names]


@mock.patch.object(TrinoClient, "select_async", side_effect=mock_select_async_generator)
def test_get_resource_attributes(mock_select_async):
    # Create an instance of DBAPIConnector
    dbapi_connector = DBAPIConnector()

    # Call the get_resource_attributes
    resource_attributes: list[ResourceAttributeDio] = dbapi_connector.get_resource_attributes()

    # Assert that select_async was called with the expected query
    mock_select_async.assert_called_once_with(
        query=dbapi_connector.config.data_object_table_column_query
    )

    # Assert that the attributes list contains the expected attributes
    expected_attributes = [
        ResourceAttributeDio(fq_name="catalog1.schema1.table1", attribute_key="it", attribute_value="commercial"),
        ResourceAttributeDio(fq_name="catalog1.schema1.table2", attribute_key="department", attribute_value="sales"),
        ResourceAttributeDio(fq_name="catalog1.schema2.table1", attribute_key="sensitivity", attribute_value="high"),
        ResourceAttributeDio(fq_name="catalog2.schema1.table1", attribute_key="owner", attribute_value="data_team"),
        ResourceAttributeDio(fq_name="catalog2.schema2.table1", attribute_key="retention", attribute_value="1year"),
        ResourceAttributeDio(fq_name="datalake.sales.orders", attribute_key="pii", attribute_value="false"),
        ResourceAttributeDio(fq_name="datalake.sales.customers", attribute_key="pii", attribute_value="true"),
        ResourceAttributeDio(fq_name="datalake.hr.employees", attribute_key="confidential", attribute_value="true"),
        ResourceAttributeDio(fq_name="datalake.finance.transactions", attribute_key="region", attribute_value="global"),
        ResourceAttributeDio(fq_name="datalake.marketing.campaigns", attribute_key="status", attribute_value="active"),
    ]

    assert resource_attributes == expected_attributes
