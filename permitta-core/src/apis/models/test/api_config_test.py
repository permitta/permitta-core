from ..src.api_config import ApiConfig


def test_load():
    config: ApiConfig = ApiConfig.load_by_api_name(api_name="healthcheck")
    assert config.auth_method == "none"

    config: ApiConfig = ApiConfig.load_by_api_name(api_name="opa")
    assert config.auth_method == "api-key"
    assert config.api_key == "bearer-token"

    config: ApiConfig = ApiConfig.load_by_api_name(api_name="resources")
    assert config.auth_method == "oauth2"
    assert config.oauth2_issuer == "https://idp.com/oauth2/"
    assert config.oauth2_audience == "audience"
