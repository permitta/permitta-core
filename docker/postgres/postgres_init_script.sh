#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER hive_user WITH PASSWORD 'hive_password';
    CREATE DATABASE hive_db;
    GRANT ALL PRIVILEGES ON DATABASE hive_db TO hive_user;
    \c hive_db "$POSTGRES_USER";
    GRANT ALL ON SCHEMA public TO hive_user;
    CREATE USER keycloak_user WITH PASSWORD 'keycloak_password';
    CREATE DATABASE keycloak;
    GRANT ALL PRIVILEGES ON DATABASE keycloak TO keycloak_user;
    \c keycloak "$POSTGRES_USER";
    GRANT ALL ON SCHEMA public TO keycloak_user;
    CREATE USER test_user WITH PASSWORD 'test_password';
    CREATE DATABASE permitta;
    GRANT ALL PRIVILEGES ON DATABASE permitta TO test_user;
    \c permitta "$POSTGRES_USER";
    GRANT ALL ON SCHEMA public TO test_user;
EOSQL