from jsonpath_ng.ext import parse
from app_logger import Logger, get_logger
from models import PrincipalDbo, PrincipalAttributeDbo
from .scim_service_config import ScimServiceConfig

logger: Logger = get_logger("scim2.service")
scim_service_config = ScimServiceConfig.load()


class ScimServiceBase:

    @staticmethod
    def _get_jsonpath_attribute(content: dict, expression: str) -> str | dict | None:
        try:
            jsonpath_expression = parse(expression)
            matches = jsonpath_expression.find(content)
            if matches:
                return matches[0].value
        except Exception as e:
            logger.error(f"Error parsing jsonpath expression: {e}")
        return None
