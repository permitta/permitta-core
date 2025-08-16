# Permitta-core
OPA bundle manager for Trino

## Features
* Bundle API for serving data and policy documents to OPA
* Extensible ingestion framework to acquire tables and users from external sources (e.g trino, ldap)
* Decision log capture

## Documentation
https://permitta.github.io/permitta-core/

## Development
The Permitta dev environment relies on a postgres database, OPA, trino, hive-metastore, minio and lldap to run.
All of these dependencies are present in the `docker-compose` in the repo root

[developer_setup.md](docs/developer_setup.md)

It is recommended to run the dependencies under `docker-compose` and debug the python code in your favourite editor 

### Architecture
* Back end is running flask server to serve API
* Unit tests are under `pytest`
* ORM is SQLAlchemy with postgres16, unit tests use `DatabaseJanitor` with dockerised postgres

#### Ingestion
Data ingestion is treated as first-class ETL in Permitta
* Ingestion jobs are asynchronous and CLI-driven. Best deployed using kubernetes CronJobs or similar
* Common ingestion controller instantiates connectors specific to the ingestion source. 
  * Additional sources can easily be added by creating new connectors. Currently supports Trino and LDAP
  * Connectors are python classes based on `ConnectorBase` and yield instances of common ingestion objects
  * Connectors instantiate specific client classes, depending on the use-case. (E.g: LDAP connector instantiates an LDAP client)
* Repository model provides a common `SQL MERGE` tool to provide robust transaction oriented ingestion

### Related Reading
* https://trino.io/docs/current/security/opa-access-control.html
* https://www.openpolicyagent.org/
