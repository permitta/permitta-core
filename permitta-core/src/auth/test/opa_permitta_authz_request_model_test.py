from auth.src.opa_permitta_authz_request_model import (
    OpaPermittaAuthzAttributeModel,
    OpaPermittaAuthzInputModel,
    OpaPermittaAuthzObjectModel,
    OpaPermittaAuthzSubjectModel,
)


def test_model():
    model = OpaPermittaAuthzInputModel(
        action="EDIT_POLICY",
        subject=OpaPermittaAuthzSubjectModel(
            username="alice",
            attributes=[
                OpaPermittaAuthzAttributeModel(key="HR", value="Commercial"),
                OpaPermittaAuthzAttributeModel(key="HR", value="Privacy"),
            ],
        ),
        object=OpaPermittaAuthzObjectModel(
            type="POLICY",
            state="draft",
            attributes=[OpaPermittaAuthzAttributeModel(key="IT", value="Commercial")],
        ),
    )

    assert model.dict() == {
        "action": "EDIT_POLICY",
        "subject": {
            "username": "alice",
            "attributes": [
                {"key": "HR", "value": "Commercial"},
                {"key": "HR", "value": "Privacy"},
            ],
        },
        "object": {
            "type": "POLICY",
            "state": "draft",
            "attributes": [{"key": "IT", "value": "Commercial"}],
        },
    }
