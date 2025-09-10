from app_logger import Logger, get_logger
from trino.dbapi import Connection, connect
from trino.exceptions import TrinoUserError

logger: Logger = get_logger("test_script")

information_schema_tables_visibility: list[str] = [
    "applicable_roles",
    "columns",
    "enabled_roles",
    "roles",
    "schemata",
    "table_privileges",
    "tables",
    "views",
]

system_catalog_schemas_visibility: dict = {
    "information_schema": information_schema_tables_visibility,
    "jdbc": [
        "attributes",
        "catalogs",
        "columns",
        "procedure_columns",
        "procedures",
        "pseudo_columns",
        "schemas",
        "super_tables",
        "super_types",
        "table_types",
        "tables",
        "types",
        "udts",
    ],
    "metadata": [
        "analyze_properties",
        "catalogs",
        "column_properties",
        "materialized_view_properties",
        "materialized_views",
        "schema_properties",
        "table_comments",
        "table_properties",
    ],
    "runtime": ["nodes", "optimizer_rule_stats", "queries", "tasks", "transactions"],
}

visible_objects: dict = {
    "alice": {
        "system": system_catalog_schemas_visibility,
        "datalake": {
            "information_schema": information_schema_tables_visibility,
            "logistics": ["shippers", "territories", "regions"],
            "sales": ["orders", "products"],
        },
        "iceberg": {
            "information_schema": information_schema_tables_visibility,
            "workspace": [],  # TODO bring tables in here
        },
    },
    "bob": {
        "system": system_catalog_schemas_visibility,
        "datalake": {
            "information_schema": information_schema_tables_visibility,
            "hr": ["employees", "employee_territories"],
            "logistics": ["shippers", "territories", "regions"],
            "sales": ["products", "customer_demographics"],
        },
    },
    "frank": {
        "system": system_catalog_schemas_visibility,
        "datalake": {
            "information_schema": information_schema_tables_visibility,
            "hr": ["employees", "employee_territories"],
            "logistics": ["shippers", "territories", "regions"],
            "sales": ["products", "customers"],
        },
    },
    "anne": {
        "system": system_catalog_schemas_visibility,
        "datalake": {
            "information_schema": information_schema_tables_visibility,
            "hr": ["employees", "employee_territories"],
            "logistics": ["regions", "suppliers"],
        },
    },
    "janis": {
        "system": system_catalog_schemas_visibility,
        "datalake": {
            "information_schema": information_schema_tables_visibility,
            "sales": ["customer_markets"],
        },
    },
}


def get_connection(username: str) -> Connection:
    connection: Connection = connect(host="localhost", port=8081, user=username)
    logger.info(f"Connecting as {username}:")
    return connection


def execute_single_row_query(query: str, connection: Connection) -> list[str]:
    logger.info(f"Executing query: {query}")
    cur = connection.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    sorted_row: list[str] = sorted([r[0] for r in rows])
    logger.info(f"Results: {sorted_row}")
    return sorted_row


def execute_scalar_query(query: str, connection: Connection) -> str:
    result: list[str] = execute_single_row_query(query=query, connection=connection)
    return result[0]


for username, catalogs in visible_objects.items():
    connection: Connection = get_connection(username=username)
    actual_catalogs: list[str] = execute_single_row_query(
        query="show catalogs", connection=connection
    )
    assert actual_catalogs == sorted(catalogs.keys())

    # schemas
    for catalog, schemas in catalogs.items():
        actual_schemas: list[str] = execute_single_row_query(
            query=f"show schemas from {catalog}", connection=connection
        )
        assert actual_schemas == sorted(schemas.keys())

        for schema, tables in schemas.items():
            actual_tables: list[str] = execute_single_row_query(
                query=f"show tables from {catalog}.{schema}", connection=connection
            )
            assert actual_tables == sorted(tables)


hr_employees_query: str = (
    "select count(*) from datalake.hr.employees where phonenumber = 'XXXX'"
)
logistics_shippers_query: str = (
    "select count(*) from datalake.logistics.shippers where phone is null"
)
sales_customer_markets_query: str = (
    "select count(*) from datalake.sales.customer_markets where type_name is null"
)

count_queries: list[dict] = [
    {
        "username": "bob",
        "query": hr_employees_query,
        "count": 300,
    },
    {
        "username": "alice",
        "query": hr_employees_query,
        "exception": True,
    },
    {
        "username": "frank",
        "query": hr_employees_query,
        "count": 0,
    },
    {
        "username": "anne",
        "query": hr_employees_query,
        "count": 300,
    },
    {"username": "janis", "query": hr_employees_query, "exception": True},
    {
        "username": "bob",
        "query": logistics_shippers_query,
        "count": 0,
    },
    {
        "username": "alice",
        "query": logistics_shippers_query,
        "count": 123,
    },
    {
        "username": "frank",
        "query": logistics_shippers_query,
        "count": 123,
    },
    {
        "username": "anne",
        "query": logistics_shippers_query,
        "exception": True,
    },
    {"username": "janis", "query": logistics_shippers_query, "exception": True},
    {"username": "bob", "query": sales_customer_markets_query, "exception": True},
    {"username": "alice", "query": sales_customer_markets_query, "exception": True},
    {"username": "frank", "query": sales_customer_markets_query, "exception": True},
    {"username": "anne", "query": sales_customer_markets_query, "exception": True},
    {"username": "janis", "query": sales_customer_markets_query, "count": 0},
]

for count_query in count_queries:
    connection: Connection = get_connection(username=count_query.get("username"))

    try:
        actual: str = execute_scalar_query(
            query=count_query.get("query"), connection=connection
        )
        assert count_query.get("count") == actual
    except TrinoUserError as e:
        logger.info(e)
        if not (count_query.get("exception"), False):
            raise


# WRITE POLICIES
connection: Connection = get_connection(username="alice")
# alice should not be able to:
# create schema
try:
    execute_scalar_query(query="create schema iceberg.bad", connection=connection)
    raise ValueError("Alice could create schema")
except TrinoUserError:
    pass

# create table with bad prefix
try:
    execute_scalar_query(
        query="create table iceberg.workspace.a_table as select 1 as a",
        connection=connection,
    )
    raise ValueError("Alice could create table with bad prefix")
except TrinoUserError:
    pass

# clean up
try:
    execute_single_row_query(
        query="drop table iceberg.workspace.v_a_table", connection=connection
    )
    execute_single_row_query(
        query="drop table iceberg.workspace.u_a_table", connection=connection
    )
except Exception:
    pass

# alice should be able to:
# create table in iceberg.workspace with v_ or u_ prefix
execute_single_row_query(
    query="create table iceberg.workspace.v_a_table as select 1 as a",
    connection=connection,
)
execute_single_row_query(
    query="create table iceberg.workspace.u_a_table as select 1 as a",
    connection=connection,
)

# insert, update, delete, select
execute_single_row_query(
    query="insert into iceberg.workspace.u_a_table select 2 as a",
    connection=connection,
)

# update
execute_single_row_query(
    query="update iceberg.workspace.u_a_table set a = 12", connection=connection
)

# delete
execute_single_row_query(
    query="delete from iceberg.workspace.u_a_table where a = 12", connection=connection
)

# select
execute_single_row_query(
    query="select a from iceberg.workspace.u_a_table", connection=connection
)

# drop tables
execute_single_row_query(
    query="drop table iceberg.workspace.v_a_table", connection=connection
)
execute_single_row_query(
    query="drop table iceberg.workspace.u_a_table", connection=connection
)

# API User
