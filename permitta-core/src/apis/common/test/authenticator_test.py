from apis.models import ApiConfig
from apis._common.src.authenticator import authenticate


def test_authenticator():
    config: ApiConfig = ApiConfig()
    config.auth_method = "none"
    assert authenticate(config).__name__ == "no_auth_decorator"

    config.auth_method = "api-key"
    assert authenticate(config).__name__ == "api_key_auth_decorator"

    config.auth_method = "oauth2"
    assert authenticate(config).__name__ == "oauth2_auth_decorator"
