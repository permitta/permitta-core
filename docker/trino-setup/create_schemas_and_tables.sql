CREATE SCHEMA IF NOT EXISTS datalake.hr;
CREATE SCHEMA IF NOT EXISTS datalake.logistics;
CREATE SCHEMA IF NOT EXISTS datalake.sales;

CREATE SCHEMA IF NOT EXISTS iceberg.workspace;

CREATE TABLE IF NOT EXISTS datalake.hr.employees
(
    Id
    VARCHAR,
    FirstName
    VARCHAR,
    LastName
    VARCHAR,
    Email
    VARCHAR,
    PhoneNumber
    VARCHAR
)
    WITH
        (
        format = 'CSV',
        skip_header_line_count = 1,
        external_location = 's3://datalake/employees/'
        );


CREATE TABLE IF NOT EXISTS datalake.hr.employee_territories
(
    EmployeeId
    VARCHAR,
    TerritoryId
    VARCHAR
)
    WITH
        (
        format = 'CSV',
        skip_header_line_count = 1,
        external_location = 's3://datalake/employee_territories/'
        );


CREATE TABLE IF NOT EXISTS datalake.logistics.shippers
(
    Id
    VARCHAR,
    CompanyName
    VARCHAR,
    Phone
    VARCHAR
)
    WITH
        (
        format = 'CSV',
        skip_header_line_count = 1,
        external_location = 's3://datalake/shippers/'
        );


CREATE TABLE IF NOT EXISTS datalake.logistics.territories
(
    Id
    VARCHAR,
    TerritoryDescription
    VARCHAR,
    RegionId
    VARCHAR
)
    WITH
        (
        format = 'CSV',
        skip_header_line_count = 1,
        external_location = 's3://datalake/territories/'
        );


CREATE TABLE IF NOT EXISTS datalake.logistics.regions
(
    Id
    VARCHAR,
    RegionDescription
    VARCHAR
)
    WITH
        (
        format = 'CSV',
        skip_header_line_count = 1,
        external_location = 's3://datalake/regions/'
        );


CREATE TABLE IF NOT EXISTS datalake.logistics.suppliers
(
    Id
    VARCHAR,
    CompanyName
    VARCHAR,
    ContactName
    VARCHAR,
    Address
    VARCHAR,
    City
    VARCHAR,
    PostalCode
    VARCHAR,
    Country
    VARCHAR,
    Phone
    VARCHAR
)
    WITH
        (
        format = 'CSV',
        skip_header_line_count = 1,
        external_location = 's3://datalake/suppliers/'
        );


CREATE TABLE IF NOT EXISTS datalake.sales.orders
(
    Id
    VARCHAR,
    CustomerId
    VARCHAR,
    EmployeeId
    VARCHAR,
    OrderDate
    VARCHAR
)
    WITH
        (
        format = 'CSV',
        skip_header_line_count = 1,
        external_location = 's3://datalake/orders/'
        );


CREATE TABLE IF NOT EXISTS datalake.sales.products
(
    Id
    VARCHAR,
    ProductName
    VARCHAR,
    SupplierId
    VARCHAR,
    QuantityPerUnit
    VARCHAR
)
    WITH
        (
        format = 'CSV',
        skip_header_line_count = 1,
        external_location = 's3://datalake/products/'
        );


CREATE TABLE IF NOT EXISTS datalake.sales.customers
(
    Id
    VARCHAR,
    CompanyName
    VARCHAR,
    ContactName
    VARCHAR,
    ContactTitle
    VARCHAR,
    Address
    VARCHAR,
    City
    VARCHAR,
    Region
    VARCHAR,
    PostalCode
    VARCHAR,
    Country
    VARCHAR,
    Phone
    VARCHAR
)
    WITH
        (
        format = 'CSV',
        skip_header_line_count = 1,
        external_location = 's3://datalake/customers/'
        );

CREATE TABLE IF NOT EXISTS datalake.sales.customer_markets
(
    Id
    VARCHAR,
    type_name
    VARCHAR,
    ContactName
    VARCHAR,
    ContactTitle
    VARCHAR,
    Address
    VARCHAR,
    City
    VARCHAR,
    Region
    VARCHAR,
    PostalCode
    VARCHAR,
    Country
    VARCHAR,
    Phone
    VARCHAR
)
    WITH
        (
        format = 'CSV',
        skip_header_line_count = 1,
        external_location = 's3://datalake/customer_markets/'
        );


CREATE TABLE IF NOT EXISTS datalake.sales.customer_demographics
(
    Id
    VARCHAR,
    CustomerDesc
    VARCHAR
)
    WITH
        (
        format = 'CSV',
        skip_header_line_count = 1,
        external_location = 's3://datalake/customer_demographics/'
        );
