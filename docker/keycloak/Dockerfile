FROM python:3.12-slim-bookworm AS builder
RUN apt-get update && apt-get install -y wget
RUN wget https://github.com/mitodl/keycloak-scim/releases/download/latest/keycloak-scim-1.0-SNAPSHOT-all.jar -O /keycloak-scim-1.0-SNAPSHOT-all.jar


FROM keycloak/keycloak:latest
COPY --from=builder /keycloak-scim-1.0-SNAPSHOT-all.jar /opt/keycloak/providers/keycloak-scim-1.0-SNAPSHOT-all.jar
