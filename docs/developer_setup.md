# Developer Setup
## Install Dependencies
* `venv` should be at the project root
* requires local installation of OPA, python 3.12
* supporting apps run under docker-compose
* an SQL client (e.g: dbeaver) is also required

```bash
brew install opa
brew install python@3.12

python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

## Formatting
```bash
# in project root
isort --profile black permitta/src
black permitta/src
```
### Running the dev environment
* Run flask on 8000, or it clashes with airplay
* Set the following environment variables

#### Webapp Environment Variables
| Name                             | Purpose                                                                                           |
|----------------------------------|---------------------------------------------------------------------------------------------------|
| FLASK_SECRET_KEY                 | Encrypts the cookies - use a complex, cryptographically secure string                             |
| OIDC_AUTH_PROVIDER_CLIENT_SECRET | The client secret provided by the OIDC server (keycloak) - in docker/keycloak/permitta_realm.json |

#### Starting the dev server
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

## Ingestion
```bash
export CONFIG_FILE_PATH=permitta/config.principal_ingestion.yaml
cli.py ingest --source=ldap --object-type=principal
```

## Documentation
Docs are provided by `mkdocs` using the `mkdocs-material` theme.
The deployment command pushes the built docs to the `gh-pages` branch which triggers a deploy
```bash
# render docs for development
mkdocs serve

# deploy docs
mkdocs gh-deploy

# if it fails, try:
git config http.postBuffer 524288000
```

