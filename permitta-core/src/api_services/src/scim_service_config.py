from app_config import AppConfigModelBase


class ScimServiceConfig(AppConfigModelBase):
    CONFIG_PREFIX: str = "scim"
    principal_fq_name_jsonpath: str = "$.userName"
    principal_first_name_jsonpath: str = "$.name.givenName"
    principal_last_name_jsonpath: str = "$.name.familyName"
    principal_user_name_jsonpath: str = "$.userName"
    principal_email_jsonpath: str = "$.emails[?(@.primary)].value"
    principal_source_uid_jsonpath: str = "$.id"

    principal_attributes_jsonpath: str = None
