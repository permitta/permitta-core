from apis.models import StatusDto
from pydantic_core import from_json


def test_validate_minimal():
    with open("permitta-core/src/apis/models/test/status_minimal.json") as json_file:
        status_json: str = json_file.read()

    dto: StatusDto = StatusDto.model_validate(from_json(status_json))
    assert dto
    assert dto.labels.id == "ea6d177f-66fe-4669-9177-2c6bfa5f899c"
    assert dto.bundles.trino.name == "trino"


def test_validate_bundle_update():
    with open(
        "permitta-core/src/apis/models/test/status_bundle_update.json"
    ) as json_file:
        status_json: str = json_file.read()

    dto: StatusDto = StatusDto.model_validate(from_json(status_json))
    assert dto
    assert dto.labels.id == "ea6d177f-66fe-4669-9177-2c6bfa5f899c"
    assert dto.bundles.trino.name == "trino"
