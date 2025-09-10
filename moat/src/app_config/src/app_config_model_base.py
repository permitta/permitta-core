import os
import re

import yaml


class AppConfigModelBase:
    """
    Configuration parameter syntax:
    <module>.<submodule>.<property_name>: <value>
    ingestor.json_file_connector.file_path: ./data.json

    Each module will request its own configuration values and bind them
    to a model class they own

    This class is passed the model dataclass, and <module>.<submodule>
    and the hydrated dataclass is returned
    """

    CONFIG_PREFIX: str = "base"
    BASE_CONFIG_FILENAME_KEY: str = "config.base"

    @staticmethod
    def _load_yaml_file(config_file_path: str = None) -> dict:
        config_file_path: str = config_file_path or os.getenv(
            "CONFIG_FILE_PATH", "moat/config/config.yaml"
        )

        def _load(path: str) -> dict:
            if not os.path.exists(path):
                raise FileNotFoundError(f"Config file not found at {path}")
            with open(path, "r") as f:
                config_content: dict = yaml.load(f, Loader=yaml.SafeLoader)

            # recursively load overrides
            if config_content.get(AppConfigModelBase.BASE_CONFIG_FILENAME_KEY):
                config_content = (
                    _load(config_content[AppConfigModelBase.BASE_CONFIG_FILENAME_KEY])
                    | config_content
                )
            return config_content

        return _load(config_file_path)

    @staticmethod
    def get_value(key: str, default: str = None) -> str:
        config_content: dict = AppConfigModelBase._load_yaml_file()
        return config_content.get(key, default)

    @classmethod
    def load(
        cls, config_file_path: str = None, config_prefix: str = None
    ) -> "AppConfigModelBase":
        config_content: dict = AppConfigModelBase._load_yaml_file(
            config_file_path=config_file_path
        )

        config_prefix = config_prefix or cls.CONFIG_PREFIX
        instance = cls()
        for key, value in config_content.items():
            attr_name: str = key.removeprefix(f"{config_prefix}.")

            # support merging in $ENV_VAR syntax
            for match in re.findall(r"(\$[A-Z_]+)", value):
                value = value.replace(match, os.getenv(match[1:], ""))

            if hasattr(instance, attr_name):
                setattr(instance, attr_name, value)
        return instance
