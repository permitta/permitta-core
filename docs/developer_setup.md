# Developer Setup

## Application Components
* **API server** is very lightweight and is based on `flask`
* **Unit tests** are under `pytest`
* **ORM** is SQLAlchemy with postgres16, unit tests use `DatabaseJanitor` with dockerised postgres

### Installation of dependencies
* Virtual environment should be at the project root
* Requires local installation of OPA and python 3.12
* Supporting apps run under docker-compose
* An SQL client (e.g: dbeaver) is also required

```bash
brew install opa
brew install python@3.12

python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

## Code Formatting
```bash
# in project root
isort --profile black permitta/src
black permitta/src
```
## Running the dev environment
* Run flask on 8000

### Starting the dev server
```bash
# if using podman
podman machine init
podman machine start
podman-compose up -d

# run dependencies
docker-compose up -d

# populate LLDAP:
docker compose exec lldap /bootstrap/bootstrap.sh

export PYTHONPATH=permitta/src
flask --app permitta.src.app run --debug --port 8000

# seed the database
python permitta/permitta/src/seed_db.py

# nuking a bad flask process
kill $(pgrep -f flask)

# all the data for lldap and postgres is stored in the `instance` dir. nuke it to reset the app
rm -rf instance
```

### Running the container
```bash
podman run --rm -p 3000:8000 permitta/permitta-core:0.0.1
curl localhost:3000/api/v1/healthcheck
```

### Running with Docker Compose
To run the Permitta Core application along with its dependencies (OPA, PostgreSQL, etc.), you can add the following service to your `docker-compose.yaml` file:

```yaml
services:

  permitta-core:
    build: .
    ports:
      - "8000:8000"
    environment:
      - FLASK_SECRET_KEY=your_secret_key
      - OIDC_AUTH_PROVIDER_CLIENT_SECRET=your_client_secret
    depends_on:
      - opa
      - postgres
```

## Building the container image
```bash
docker build -t permitta/permitta-core
```

## Running Ingestion
```bash
export CONFIG_FILE_PATH=permitta/config.principal_ingestion.yaml
cli.py ingest --source=ldap --object-type=principal

# or in the container
docker run permitta-core ingest --connector-name=ldap --object-type=principal
```

## Database Migrations
`alembic` is used to migrate the database schema

```bash
# create a new revision (in project root)
export PYTHONPATH=./permitta-core/src
alembic -c permitta-core/alembic.ini revision --autogenerate -m "message about the revision"
# or
./entrypoint.sh migrate revision "message about the revision"

# upgrade
alembic upgrade head
# or
./entrypoint.sh migrate upgrade
```

## Documentation
Docs are provided by `mkdocs` using the `mkdocs-material` theme.
The documentation is automatically deployed to GitHub Pages via GitHub Actions when changes are pushed to the main branch.

For local development:
```bash
# render docs for development
mkdocs serve
```

Manual deployment (not needed for normal workflow as it's automated):
```bash
# deploy docs manually
mkdocs gh-deploy

# if it fails, try:
git config http.postBuffer 524288000
```

## Keycloak
```bash
# export the realm

```

## SCIM test tool
```bash
pip install scim2-cli

./test.sh scim
```