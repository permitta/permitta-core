from ..src.json_file_connector_config_model import JsonFileConnectorConfigModel


def test_constructor():
    config_model: JsonFileConnectorConfigModel = JsonFileConnectorConfigModel.load()
    assert config_model.file_path == "config/principals.json"
